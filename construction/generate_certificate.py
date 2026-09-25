"""Deterministically construct compact certificate geometry from the parameter bank.

This module is untrusted.  It selects exact rational recipes and may use Arb to
avoid emitting candidates that are known to fail, but only
``proof.check_certificate`` can accept the resulting certificate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
import os
from pathlib import Path
import sys
from typing import Any

from proof.berry_core import (
    A,
    CertificateError,
    RHO0_Q,
    TARGET_Q,
    build_constants,
    evaluate_cell,
    lb,
    qstr,
    self_test_global_reductions,
)

from .parameter_bank import ParameterBank, ParameterSeed


CERTIFICATE_FORMAT = "berry-esseen-045-cert-v2"
PYTHON_FLINT_VERSION = "0.9.0"
REGULARIZED_COT_TERMS = 100


@dataclass(frozen=True)
class Candidate:
    seed: ParameterSeed
    pieces: int
    cell: dict[str, Any]
    ratio_upper: Any


def normalize_seed(
    seed: ParameterSeed,
    *,
    rho_lo: Fraction,
) -> ParameterSeed | None:
    """Apply the exact Section 6 parameter guards to a bank recipe."""
    if seed.q <= 0 or not (0 < seed.t0 < 1):
        return None
    eta_cap = min(seed.t0, Fraction(1, 2), (rho_lo + 1) / seed.q)
    eta = min(seed.eta, eta_cap)
    lam = min(seed.lam, seed.t0, Fraction(1, 2))
    if eta <= 0 or lam <= 0:
        return None
    return ParameterSeed(
        q=seed.q,
        t0=seed.t0,
        eta=eta,
        lam=lam,
        pieces=seed.pieces,
        grid_power=seed.grid_power,
        rank=seed.rank,
    )


def make_cell(
    rho_lo: Fraction,
    rho_hi: Fraction,
    seed: ParameterSeed,
    pieces: int | None = None,
) -> dict[str, Any]:
    """Serialize one compact format-v2 cell using only exact proof data."""
    selected_pieces = seed.pieces if pieces is None else pieces
    return {
        "rho": [qstr(rho_lo), qstr(rho_hi)],
        "q": qstr(seed.q),
        "t0": qstr(seed.t0),
        "eta": qstr(seed.eta),
        "lambda": qstr(seed.lam),
        "grid": {
            "pieces": selected_pieces,
            "power": seed.grid_power,
        },
    }


def evaluate_candidate(
    n: int,
    rho_lo: Fraction,
    rho_hi: Fraction,
    seed: ParameterSeed,
    pieces: int,
    constants: Any,
) -> Candidate:
    cell = make_cell(rho_lo, rho_hi, seed, pieces)
    result = evaluate_cell(
        n,
        cell,
        constants,
        regularized_cot_terms=REGULARIZED_COT_TERMS,
    )
    return Candidate(seed, pieces, cell, result.ratio_upper)


def select_cell(
    n: int,
    row: int,
    bank: ParameterBank,
    constants: Any,
    max_pieces: int,
) -> tuple[dict[str, Any], int, int]:
    """Select the first certified recipe, then refine failed recipes if needed."""
    rho_lo, rho_hi = bank.exact_cell(row)
    target = lb(A(TARGET_Q))
    attempted: list[Candidate] = []

    for raw_seed in bank.candidates(row):
        seed = normalize_seed(raw_seed, rho_lo=rho_lo)
        if seed is None:
            continue
        candidate = evaluate_candidate(
            n, rho_lo, rho_hi, seed, seed.pieces, constants
        )
        attempted.append(candidate)
        if candidate.ratio_upper <= target:
            return candidate.cell, seed.rank, candidate.pieces

    if not attempted:
        raise CertificateError(f"n={n}, row={row}: no structurally valid recipe")

    attempted.sort(
        key=lambda item: float(item.ratio_upper.str(24, radius=False))
    )
    for initial in attempted:
        pieces = initial.pieces * 2
        while pieces <= max_pieces:
            candidate = evaluate_candidate(
                n, rho_lo, rho_hi, initial.seed, pieces, constants
            )
            if candidate.ratio_upper <= target:
                return candidate.cell, initial.seed.rank, pieces
            pieces *= 2

    best = attempted[0]
    raise CertificateError(
        f"n={n}, rho=[{qstr(rho_lo)},{qstr(rho_hi)}]: all parameter-bank "
        f"recipes failed; best upper={best.ratio_upper.str(30, radius=False)}"
    )


def construct_n(
    n: int,
    bank: ParameterBank,
    constants: Any,
    max_pieces: int,
    progress_every: int,
) -> list[dict[str, Any]]:
    rows = bank.rows_for_n(n)
    cells: list[dict[str, Any]] = []
    expected = Fraction(1)
    routes = {"rank0": 0, "other_rank": 0, "refined": 0}
    for position, row in enumerate(rows, 1):
        rho_lo, rho_hi = bank.exact_cell(row)
        if rho_lo != expected:
            raise CertificateError(f"parameter-bank rho gap or overlap for n={n}")
        cell, rank, pieces = select_cell(n, row, bank, constants, max_pieces)
        cells.append(cell)
        bank_pieces = int(bank.pieces[row, rank])
        if pieces != bank_pieces:
            routes["refined"] += 1
        elif rank == 0:
            routes["rank0"] += 1
        else:
            routes["other_rank"] += 1
        expected = rho_hi
        if progress_every and (
            position % progress_every == 0 or position == len(rows)
        ):
            print(
                f"n={n}: selected {position}/{len(rows)} cells",
                file=sys.stderr,
                flush=True,
            )
    if expected != RHO0_Q:
        raise CertificateError(f"parameter-bank rho cover for n={n} is incomplete")
    print(
        f"n={n}: constructed {len(cells)} cells; routes={routes}",
        file=sys.stderr,
        flush=True,
    )
    return cells


def atomic_write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(
            value,
            stream,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--parameter-bank", type=Path, required=True)
    parser.add_argument("--n-start", type=int, default=2)
    parser.add_argument("--n-end", type=int, default=8123)
    parser.add_argument("--precision-bits", type=int, default=192)
    parser.add_argument("--max-pieces", type=int, default=4096)
    parser.add_argument("--progress-every", type=int, default=0)
    args = parser.parse_args()

    if not (2 <= args.n_start <= args.n_end <= 8123):
        parser.error("require 2 <= n-start <= n-end <= 8123")
    if not (1 <= args.max_pieces <= 4096):
        parser.error("max-pieces must lie in [1,4096]")
    if args.progress_every < 0:
        parser.error("progress-every must be nonnegative")
    if args.output.exists():
        parser.error("output already exists; refusing to overwrite")

    bank = ParameterBank(args.parameter_bank)
    constants = build_constants(args.precision_bits)
    self_test_global_reductions(constants)
    blocks = []
    for n in range(args.n_start, args.n_end + 1):
        cells = construct_n(
            n, bank, constants, args.max_pieces, args.progress_every
        )
        blocks.append({"n": n, "cells": cells})

    certificate = {
        "format": CERTIFICATE_FORMAT,
        "target": "9/20",
        "rho0": qstr(RHO0_Q),
        "precision_bits": args.precision_bits,
        "python_flint": PYTHON_FLINT_VERSION,
        "scope": {"n_start": args.n_start, "n_end": args.n_end},
        "n_blocks": blocks,
    }
    atomic_write_json(args.output, certificate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
