"""Loader for the untrusted parameter bank used during certificate construction.

The bank supplies candidate smoothing parameters discovered on an NVIDIA A100.
It is never part of the proof authority: every selected recipe is serialized as
exact rational data and independently recomputed by :mod:`proof.berry_core`.
Hashes in the manifest provide reproducibility and corruption detection only.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Iterator

import numpy as np


BANK_FORMAT = "berry-esseen-parameter-bank-v1"
RECIPE_DENOMINATOR = 1 << 20
RHO0 = Fraction(712569, 589000)
REQUIRED_ARRAYS = (
    "n",
    "depth",
    "cell_index",
    "q",
    "t0",
    "eta",
    "lam",
    "pieces",
    "grid_power",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dyadic_fraction(value: float) -> Fraction:
    """Convert a quantized float64 recipe value to its specified dyadic value."""
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("parameter-bank recipe contains a non-finite value")
    return Fraction(round(number * RECIPE_DENOMINATOR), RECIPE_DENOMINATOR)


@dataclass(frozen=True)
class ParameterSeed:
    q: Fraction
    t0: Fraction
    eta: Fraction
    lam: Fraction
    pieces: int
    grid_power: int
    rank: int


class ParameterBank:
    """Memory-mapped access to the publication parameter bank."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        manifest_path = self.path / "manifest.json"
        if not manifest_path.is_file():
            raise ValueError(f"parameter bank is missing {manifest_path}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read parameter-bank manifest: {exc}") from exc
        if not isinstance(manifest, dict) or manifest.get("format") != BANK_FORMAT:
            raise ValueError(f"parameter-bank format must be {BANK_FORMAT!r}")
        if manifest.get("version") != 1:
            raise ValueError("unsupported parameter-bank version")
        arrays = manifest.get("arrays")
        if not isinstance(arrays, dict) or set(arrays) != set(REQUIRED_ARRAYS):
            raise ValueError("parameter-bank manifest has an invalid array set")

        self.manifest = manifest
        self.manifest_path = manifest_path
        self.rows = self._manifest_int("rows", 1)
        self.candidates_per_cell = self._manifest_int("candidates_per_cell", 1)
        if manifest.get("n_min") != 2 or manifest.get("n_max") != 8123:
            raise ValueError("parameter bank must cover n=2,...,8123")
        if manifest.get("rho0") != "712569/589000":
            raise ValueError("parameter bank has an unexpected rho0")

        for name in REQUIRED_ARRAYS:
            metadata = arrays[name]
            if not isinstance(metadata, dict):
                raise ValueError(f"invalid metadata for array {name}")
            file_name = metadata.get("file")
            if file_name != f"{name}.npy":
                raise ValueError(f"invalid file name for array {name}")
            path = self.path / file_name
            if not path.is_file():
                raise ValueError(f"parameter bank is missing {file_name}")
            array = np.load(path, mmap_mode="r", allow_pickle=False)
            expected_shape = metadata.get("shape")
            if list(array.shape) != expected_shape:
                raise ValueError(f"shape mismatch for {file_name}")
            if array.dtype.str != metadata.get("dtype"):
                raise ValueError(f"dtype mismatch for {file_name}")
            setattr(self, name, array)

        for name in ("n", "depth", "cell_index"):
            if getattr(self, name).shape != (self.rows,):
                raise ValueError(f"{name}.npy must have shape (rows,)")
        recipe_shape = (self.rows, self.candidates_per_cell)
        for name in ("q", "t0", "eta", "lam", "pieces", "grid_power"):
            if getattr(self, name).shape != recipe_shape:
                raise ValueError(f"{name}.npy must have shape (rows,candidates)")

        if self.rows and np.any(self.n[1:] < self.n[:-1]):
            raise ValueError("parameter-bank rows must be grouped by increasing n")
        starts = np.flatnonzero(np.r_[True, self.n[1:] != self.n[:-1]])
        ends = np.r_[starts[1:], self.rows]
        self._ranges = {
            int(self.n[start]): (int(start), int(end))
            for start, end in zip(starts, ends)
        }
        if sorted(self._ranges) != list(range(2, 8124)):
            raise ValueError("parameter bank does not contain every n=2,...,8123")

    def _manifest_int(self, key: str, minimum: int) -> int:
        value = self.manifest.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ValueError(f"manifest field {key!r} must be an integer >= {minimum}")
        return value

    def rows_for_n(self, n: int) -> list[int]:
        """Return row indices in exact increasing rho order."""
        try:
            start, end = self._ranges[n]
        except KeyError as exc:
            raise ValueError(f"parameter bank has no rows for n={n}") from exc
        rows = list(range(start, end))
        max_depth = max(int(self.depth[row]) for row in rows)
        rows.sort(
            key=lambda row: int(self.cell_index[row])
            << (max_depth - int(self.depth[row]))
        )
        return rows

    def exact_cell(self, row: int) -> tuple[Fraction, Fraction]:
        depth = int(self.depth[row])
        index = int(self.cell_index[row])
        if not (0 <= depth <= 30 and 0 <= index < 1 << depth):
            raise ValueError(f"invalid dyadic cell at row {row}")
        width = (RHO0 - 1) / (1 << depth)
        return 1 + index * width, 1 + (index + 1) * width

    def candidates(self, row: int) -> Iterator[ParameterSeed]:
        """Yield unique, structurally valid recipes in rank order."""
        seen: set[tuple[Fraction, Fraction, Fraction, Fraction, int, int]] = set()
        for rank in range(self.candidates_per_cell):
            pieces = int(self.pieces[row, rank])
            power = int(self.grid_power[row, rank])
            q = dyadic_fraction(self.q[row, rank])
            t0 = dyadic_fraction(self.t0[row, rank])
            eta = dyadic_fraction(self.eta[row, rank])
            lam = dyadic_fraction(self.lam[row, rank])
            key = (q, t0, eta, lam, pieces, power)
            if key in seen:
                continue
            seen.add(key)
            if not (
                q > 0
                and 0 < lam <= t0 < 1
                and 0 < eta <= min(t0, Fraction(1, 2))
                and 1 <= pieces <= 4096
                and 1 <= power <= 8
            ):
                continue
            yield ParameterSeed(q, t0, eta, lam, pieces, power, rank)

    def validate_geometry(self) -> None:
        """Require an exact, gap-free dyadic tiling for every n."""
        for n in range(2, 8124):
            rows = self.rows_for_n(n)
            max_depth = max(int(self.depth[row]) for row in rows)
            expected = 0
            for row in rows:
                depth = int(self.depth[row])
                index = int(self.cell_index[row])
                scale = 1 << (max_depth - depth)
                lo = index * scale
                hi = (index + 1) * scale
                if lo != expected:
                    raise ValueError(f"rho gap or overlap for n={n} at row {row}")
                expected = hi
            if expected != 1 << max_depth:
                raise ValueError(f"rho tiling for n={n} does not end at rho0")

    def validate_hashes(self) -> None:
        """Validate every NPY byte string against the canonical manifest."""
        arrays = self.manifest["arrays"]
        for name in REQUIRED_ARRAYS:
            expected = arrays[name].get("sha256")
            if not isinstance(expected, str) or len(expected) != 64:
                raise ValueError(f"missing SHA-256 for {name}.npy")
            actual = sha256_file(self.path / f"{name}.npy")
            if actual != expected:
                raise ValueError(f"SHA-256 mismatch for {name}.npy")

    def validate(self) -> None:
        self.validate_hashes()
        self.validate_geometry()

    def __len__(self) -> int:
        return self.rows
