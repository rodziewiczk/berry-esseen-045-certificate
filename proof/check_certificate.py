"""Fail-closed checker for the complete Berry--Esseen 0.45 certificate bundle.

The public protocol accepts only a directory covering every ``n=2,...,8123``.
Each compact shard contains exact rational parameters and deterministic grid
recipes; all analytic bounds are recomputed with python-flint/Arb.  No bound
stored by the constructor or the A100 parameter search is trusted.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
from typing import Any

import flint

if __package__:
    from .berry_core import (
        A,
        CertificateError,
        RHO0_Q,
        TARGET_Q,
        build_constants,
        evaluate_cell,
        lb,
        parse_q,
        qstr,
        self_test_global_reductions,
    )
else:
    # The canonical verifier launches this file directly.  In that mode Python
    # searches this directory for berry_core.py without executing
    # proof/__init__.py first.  This keeps the executable trust boundary equal
    # to the source files whose digests the bundle records.
    from berry_core import (  # type: ignore[no-redef]
        A,
        CertificateError,
        RHO0_Q,
        TARGET_Q,
        build_constants,
        evaluate_cell,
        lb,
        parse_q,
        qstr,
        self_test_global_reductions,
    )


SHARD_FORMAT = "berry-esseen-045-cert-v2"
BUNDLE_FORMAT = "berry-esseen-045-certificate-bundle-v2"
REQUIRED_PYTHON_FLINT = "0.9.0"
REQUIRED_FLINT = "3.6.0"
REGULARIZED_COT_TERMS = 100
AUDIT_FILENAME = "verification.json"
MAX_BUNDLE_MANIFEST_BYTES = 8 << 20
MAX_SHARD_BYTES = 4 << 20
MAX_CELLS_PER_SHARD = 4096
MAX_RATIONAL_CHARACTERS = 256
MAX_WORKERS = 64
BUNDLE_SOURCE_PATHS = {
    "checker_sha256": Path("proof/check_certificate.py"),
    "core_sha256": Path("proof/berry_core.py"),
    "proof_package_sha256": Path("proof/__init__.py"),
    "constructor_sha256": Path("construction/generate_certificate.py"),
    "parameter_bank_loader_sha256": Path("construction/parameter_bank.py"),
    "construction_package_sha256": Path("construction/__init__.py"),
    "verification_launcher_sha256": Path("construction/verify.py"),
}
SHARD_KEYS = {
    "format",
    "target",
    "rho0",
    "precision_bits",
    "python_flint",
    "scope",
    "n_blocks",
}
BUNDLE_KEYS = {
    "format",
    "target",
    "rho0",
    "precision_bits",
    "python_flint",
    "flint",
    "scope",
    "checker_sha256",
    "core_sha256",
    "proof_package_sha256",
    "constructor_sha256",
    "parameter_bank_loader_sha256",
    "construction_package_sha256",
    "verification_launcher_sha256",
    "parameter_bank_manifest_sha256",
    "certificate_set_sha256",
    "certificates",
}
SCOPE_KEYS = {"n_start", "n_end"}
BLOCK_KEYS = {"n", "cells"}
CELL_KEYS = {"rho", "q", "t0", "eta", "lambda", "grid"}
GRID_KEYS = {"pieces", "power"}
ENTRY_KEYS = {"n", "file", "bytes", "sha256"}


def progress_due(n: int, completed: int, total: int, every: int) -> bool:
    """Report early values, fixed ``n`` milestones, and final completion."""
    return bool(
        every
        and (
            n <= 10
            or n % every == 0
            or (completed == total and n == total + 1)
        )
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bundle_source_hashes(repository: Path) -> dict[str, str]:
    """Hash every repository Python source involved in construction/launch."""
    hashes: dict[str, str] = {}
    for field, relative_path in BUNDLE_SOURCE_PATHS.items():
        path = repository / relative_path
        if not path.is_file():
            raise CertificateError(f"missing repository source {relative_path.as_posix()}")
        hashes[field] = sha256_file(path)
    return hashes


def is_sha256(value: object) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def certificate_set_digest(entries: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for entry in entries:
        digest.update(f"{entry['n']}:{entry['sha256']}\n".encode("ascii"))
    return digest.hexdigest()


def dyadic_fraction(mantissa: int, exponent: int) -> Fraction:
    """Return the exact rational represented by ``mantissa * 2**exponent``."""
    if exponent >= 0:
        return Fraction(mantissa << exponent)
    return Fraction(mantissa, 1 << -exponent)


def arb_upper_dyadic(value: Any) -> tuple[int, int]:
    """Extract Arb's rigorous upper endpoint as an exact dyadic rational."""
    mantissa, exponent = value.upper().man_exp()
    return int(mantissa), int(exponent)


def format_dyadic_upper(mantissa: int, exponent: int, places: int = 30) -> str:
    """Format a dyadic endpoint with directed decimal rounding toward +infinity."""
    if not (1 <= places <= 1000):
        raise ValueError("places must lie in [1,1000]")
    value = dyadic_fraction(mantissa, exponent)
    scale = 10**places
    scaled_ceiling = -(-value.numerator * scale // value.denominator)
    sign = "-" if scaled_ceiling < 0 else ""
    whole, fractional = divmod(abs(scaled_ceiling), scale)
    return f"{sign}{whole}.{fractional:0{places}d}"


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise CertificateError(f"non-standard JSON constant {value!r} is forbidden")


def _reject_json_float(value: str) -> None:
    raise CertificateError(f"JSON floating-point number {value!r} is forbidden")


def load_json_bytes(
    path: Path,
    description: str,
    *,
    max_bytes: int = MAX_BUNDLE_MANIFEST_BYTES,
) -> tuple[dict[str, Any], str, int]:
    """Read once, then derive both the parsed value and SHA-256 from those bytes."""
    try:
        reported_size = path.stat().st_size
        if reported_size > max_bytes:
            raise CertificateError(
                f"{description} exceeds the {max_bytes}-byte protocol limit"
            )
        raw_bytes = path.read_bytes()
        if len(raw_bytes) > max_bytes:
            raise CertificateError(
                f"{description} exceeds the {max_bytes}-byte protocol limit"
            )
        data = json.loads(
            raw_bytes.decode("utf-8"),
            object_pairs_hook=_no_duplicate_keys,
            parse_constant=_reject_json_constant,
            parse_float=_reject_json_float,
        )
    except CertificateError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise CertificateError(f"cannot read {description}: {exc}") from exc
    if not isinstance(data, dict):
        raise CertificateError(f"{description} root must be a JSON object")
    return data, hashlib.sha256(raw_bytes).hexdigest(), len(raw_bytes)


def require_exact_keys(
    value: object,
    expected: set[str],
    where: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CertificateError(f"{where} must be a JSON object")
    actual = set(value)
    if actual != expected:
        raise CertificateError(
            f"{where}: key mismatch; missing={sorted(expected-actual)}, "
            f"extra={sorted(actual-expected)}"
        )
    return value


def json_int(value: object, where: str, lower: int, upper: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise CertificateError(f"{where} must be a JSON integer")
    if not (lower <= value <= upper):
        raise CertificateError(f"{where} must lie in [{lower},{upper}]")
    return value


def bounded_rational(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise CertificateError(f"{where} must be a rational string")
    if len(value) > MAX_RATIONAL_CHARACTERS:
        raise CertificateError(
            f"{where} exceeds the {MAX_RATIONAL_CHARACTERS}-character limit"
        )
    return value


def installed_flint_version() -> str:
    try:
        installed = importlib.metadata.version("python-flint")
    except importlib.metadata.PackageNotFoundError as exc:
        raise CertificateError("python-flint distribution metadata not found") from exc
    if installed != REQUIRED_PYTHON_FLINT:
        raise CertificateError(
            f"installed python-flint is {installed}, expected {REQUIRED_PYTHON_FLINT}"
        )
    if flint.__FLINT_VERSION__ != REQUIRED_FLINT:
        raise CertificateError(
            f"bundled FLINT is {flint.__FLINT_VERSION__}, expected {REQUIRED_FLINT}"
        )
    return installed


def validate_common_header(
    data: dict[str, Any],
    expected_keys: set[str],
    expected_format: str,
) -> tuple[int, int, int]:
    require_exact_keys(data, expected_keys, "certificate")
    if data["format"] != expected_format:
        raise CertificateError(f"format must equal {expected_format!r}")
    if parse_q(bounded_rational(data["target"], "target"), "target") != TARGET_Q:
        raise CertificateError("target must be exactly 9/20")
    if parse_q(bounded_rational(data["rho0"], "rho0"), "rho0") != RHO0_Q:
        raise CertificateError(f"rho0 must be exactly {qstr(RHO0_Q)}")
    precision = json_int(data["precision_bits"], "precision_bits", 96, 16384)
    if data["python_flint"] != REQUIRED_PYTHON_FLINT:
        raise CertificateError(
            f"python_flint must equal {REQUIRED_PYTHON_FLINT!r}"
        )
    scope = require_exact_keys(data["scope"], SCOPE_KEYS, "scope")
    n_start = json_int(scope["n_start"], "scope.n_start", 2, 8123)
    n_end = json_int(scope["n_end"], "scope.n_end", 2, 8123)
    if n_start > n_end:
        raise CertificateError("scope.n_start must not exceed scope.n_end")
    return precision, n_start, n_end


def validate_cell_shape(n: int, index: int, value: object) -> dict[str, Any]:
    cell = require_exact_keys(value, CELL_KEYS, f"n={n}.cells[{index}]")
    rho = cell["rho"]
    if not isinstance(rho, list) or len(rho) != 2:
        raise CertificateError(f"n={n}.cells[{index}].rho must contain two values")
    for endpoint, rho_value in enumerate(rho):
        bounded_rational(rho_value, f"n={n}.cells[{index}].rho[{endpoint}]")
    for field in ("q", "t0", "eta", "lambda"):
        bounded_rational(cell[field], f"n={n}.cells[{index}].{field}")
    grid = require_exact_keys(
        cell["grid"], GRID_KEYS, f"n={n}.cells[{index}].grid"
    )
    json_int(grid["pieces"], f"n={n}.cells[{index}].grid.pieces", 1, 4096)
    json_int(grid["power"], f"n={n}.cells[{index}].grid.power", 1, 8)
    return cell


def check_rho_cover(n: int, value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise CertificateError(f"n={n}: cells must be a nonempty list")
    if len(value) > MAX_CELLS_PER_SHARD:
        raise CertificateError(
            f"n={n}: cells exceeds the {MAX_CELLS_PER_SHARD}-cell protocol limit"
        )
    cells: list[dict[str, Any]] = []
    expected = Fraction(1)
    for index, value_cell in enumerate(value):
        cell = validate_cell_shape(n, index, value_cell)
        rho_lo = parse_q(cell["rho"][0], f"n={n}.cells[{index}].rho[0]")
        rho_hi = parse_q(cell["rho"][1], f"n={n}.cells[{index}].rho[1]")
        if rho_lo != expected:
            raise CertificateError(
                f"n={n}: rho gap or overlap before cell {index}; "
                f"expected {qstr(expected)}, got {qstr(rho_lo)}"
            )
        if not rho_lo < rho_hi:
            raise CertificateError(f"n={n}, cell={index}: degenerate rho interval")
        expected = rho_hi
        cells.append(cell)
    if expected != RHO0_Q:
        raise CertificateError(
            f"n={n}: rho cover ends at {qstr(expected)}, expected {qstr(RHO0_Q)}"
        )
    return cells


@dataclass(frozen=True)
class ShardSummary:
    n: int
    cells: int
    worst_upper: str
    worst_upper_exact: str
    worst_upper_mantissa: int
    worst_upper_exponent: int
    worst_location: dict[str, Any]
    sha256: str
    bytes: int


_WORKER_CONSTANTS: Any = None
_WORKER_PRECISION: int | None = None


def initialize_worker(precision_bits: int) -> None:
    global _WORKER_CONSTANTS, _WORKER_PRECISION
    installed_flint_version()
    _WORKER_PRECISION = precision_bits
    _WORKER_CONSTANTS = build_constants(precision_bits)
    self_test_global_reductions(_WORKER_CONSTANTS)


def verify_shard(
    path: Path,
    *,
    expected_n: int,
    expected_sha256: str | None,
    expected_bytes: int | None,
    expected_precision: int,
    constants: Any,
) -> ShardSummary:
    data, file_sha256, file_bytes = load_json_bytes(
        path, f"shard for n={expected_n}", max_bytes=MAX_SHARD_BYTES
    )
    if expected_sha256 is not None and file_sha256 != expected_sha256:
        raise CertificateError(f"n={expected_n}: shard SHA-256 mismatch")
    if expected_bytes is not None and file_bytes != expected_bytes:
        raise CertificateError(f"n={expected_n}: shard byte count mismatch")
    precision, n_start, n_end = validate_common_header(
        data, SHARD_KEYS, SHARD_FORMAT
    )
    if precision != expected_precision:
        raise CertificateError(f"n={expected_n}: precision differs from the bundle")
    if (n_start, n_end) != (expected_n, expected_n):
        raise CertificateError(f"shard scope must be exactly n={expected_n}")

    blocks = data["n_blocks"]
    if not isinstance(blocks, list) or len(blocks) != 1:
        raise CertificateError(f"n={expected_n}: shard must contain one n block")
    block = require_exact_keys(blocks[0], BLOCK_KEYS, "n_blocks[0]")
    if json_int(block["n"], "n_blocks[0].n", 2, 8123) != expected_n:
        raise CertificateError(f"n={expected_n}: block number mismatch")
    cells = check_rho_cover(expected_n, block["cells"])
    target = lb(A(TARGET_Q))
    worst = None
    worst_location: dict[str, Any] | None = None
    for index, cell in enumerate(cells):
        result = evaluate_cell(
            expected_n,
            cell,
            constants,
            regularized_cot_terms=REGULARIZED_COT_TERMS,
        )
        if not (result.ratio_upper <= target):
            mantissa, exponent = arb_upper_dyadic(result.ratio_upper)
            raise CertificateError(
                f"n={expected_n}, cell={index}, rho={cell['rho']}: certified "
                f"upper {format_dyadic_upper(mantissa, exponent)} exceeds 9/20"
            )
        if worst is None or worst <= result.ratio_upper:
            worst = result.ratio_upper
            worst_location = {
                "n": expected_n,
                "cell": index,
                "rho": cell["rho"],
            }
    assert worst is not None and worst_location is not None
    worst_mantissa, worst_exponent = arb_upper_dyadic(worst)
    worst_fraction = dyadic_fraction(worst_mantissa, worst_exponent)
    return ShardSummary(
        n=expected_n,
        cells=len(cells),
        worst_upper=format_dyadic_upper(worst_mantissa, worst_exponent),
        worst_upper_exact=qstr(worst_fraction),
        worst_upper_mantissa=worst_mantissa,
        worst_upper_exponent=worst_exponent,
        worst_location=worst_location,
        sha256=file_sha256,
        bytes=file_bytes,
    )


def worker_verify_shard(task: tuple[str, int, str, int]) -> ShardSummary:
    if _WORKER_CONSTANTS is None or _WORKER_PRECISION is None:
        raise RuntimeError("checker worker was not initialized")
    path, n, expected_sha256, expected_bytes = task
    return verify_shard(
        Path(path),
        expected_n=n,
        expected_sha256=expected_sha256,
        expected_bytes=expected_bytes,
        expected_precision=_WORKER_PRECISION,
        constants=_WORKER_CONSTANTS,
    )


def safe_bundle_file(bundle: Path, relative: str, n: int) -> Path:
    expected = f"n/{n:04d}.json"
    if relative != expected:
        raise CertificateError(f"n={n}: file must be exactly {expected!r}")
    path = (bundle / relative).resolve()
    root = bundle.resolve()
    if root not in path.parents:
        raise CertificateError(f"n={n}: shard path escapes the bundle")
    if not path.is_file():
        raise CertificateError(f"n={n}: missing shard {relative}")
    return path


def validate_bundle_manifest(
    bundle: Path,
    data: dict[str, Any],
    checker_path: Path,
    core_path: Path,
) -> tuple[int, list[dict[str, Any]]]:
    precision, n_start, n_end = validate_common_header(
        data, BUNDLE_KEYS, BUNDLE_FORMAT
    )
    if (n_start, n_end) != (2, 8123):
        raise CertificateError("the public bundle scope must be exactly n=2,...,8123")
    if data["flint"] != REQUIRED_FLINT:
        raise CertificateError(f"flint must equal {REQUIRED_FLINT!r}")
    repository = checker_path.parents[1]
    expected_core_path = repository / BUNDLE_SOURCE_PATHS["core_sha256"]
    if core_path.resolve() != expected_core_path.resolve():
        raise CertificateError("internal checker source-path inconsistency")
    current_sources = bundle_source_hashes(repository)
    for field, current_sha256 in current_sources.items():
        if not is_sha256(data[field]):
            raise CertificateError(f"{field} must be a lowercase SHA-256 string")
        if data[field] != current_sha256:
            source = BUNDLE_SOURCE_PATHS[field].as_posix()
            raise CertificateError(f"bundle is bound to a different {source} source")
    for field in (
        "parameter_bank_manifest_sha256",
        "certificate_set_sha256",
    ):
        value = data[field]
        if not is_sha256(value):
            raise CertificateError(f"{field} must be a lowercase SHA-256 string")

    raw_entries = data["certificates"]
    if not isinstance(raw_entries, list) or len(raw_entries) != 8122:
        raise CertificateError("certificates must contain exactly 8122 entries")
    entries: list[dict[str, Any]] = []
    for expected_n, raw_entry in zip(range(2, 8124), raw_entries):
        entry = require_exact_keys(raw_entry, ENTRY_KEYS, f"certificates[{expected_n-2}]")
        n = json_int(entry["n"], "certificate entry n", 2, 8123)
        if n != expected_n:
            raise CertificateError("certificate entries must be ordered n=2,...,8123")
        file_name = entry["file"]
        if not isinstance(file_name, str):
            raise CertificateError(f"n={n}: file must be a string")
        path = safe_bundle_file(bundle, file_name, n)
        byte_count = json_int(entry["bytes"], f"n={n}.bytes", 1, 1 << 31)
        sha256 = entry["sha256"]
        if not is_sha256(sha256):
            raise CertificateError(f"n={n}: invalid SHA-256")
        entries.append(
            {"n": n, "file": file_name, "path": path, "bytes": byte_count, "sha256": sha256}
        )
    digest_entries = [
        {"n": entry["n"], "sha256": entry["sha256"]} for entry in entries
    ]
    if certificate_set_digest(digest_entries) != data["certificate_set_sha256"]:
        raise CertificateError("certificate-set digest mismatch")

    expected_files = {entry["path"] for entry in entries}
    shard_directory = bundle / "n"
    try:
        directory_entries = list(shard_directory.iterdir())
    except OSError as exc:
        raise CertificateError(f"cannot enumerate bundle shard directory: {exc}") from exc
    if any(not path.is_file() for path in directory_entries):
        raise CertificateError("bundle n directory may contain only shard files")
    actual_files = {path.resolve() for path in directory_entries}
    if actual_files != expected_files:
        raise CertificateError("bundle n directory contains missing or extra shards")
    return precision, entries


def canonical_audit_path(bundle: Path) -> Path:
    return bundle.resolve() / AUDIT_FILENAME


def prepare_audit_path(bundle: Path, requested: Path | None) -> Path | None:
    """Validate and invalidate the sole full-bundle audit output.

    The checker deliberately cannot write to an arbitrary user-selected path.
    This prevents an accepted audit from replacing a source, manifest, or shard.
    Removing an earlier ordinary audit before verification also makes failures
    leave no stale ``ACCEPTED_FULL`` receipt behind.
    """
    if requested is None:
        return None
    expected = canonical_audit_path(bundle)
    try:
        requested_parent = requested.parent.resolve()
    except OSError as exc:
        raise CertificateError(f"cannot resolve audit directory: {exc}") from exc
    if requested.name != AUDIT_FILENAME or requested_parent != expected.parent:
        raise CertificateError(
            f"--audit must be exactly the bundle-local {AUDIT_FILENAME!r}"
        )
    if expected.is_symlink():
        raise CertificateError("audit output must not be a symbolic link")
    if expected.exists():
        try:
            metadata = expected.stat()
        except OSError as exc:
            raise CertificateError(f"cannot inspect previous audit: {exc}") from exc
        if not expected.is_file() or metadata.st_nlink != 1:
            raise CertificateError("existing audit must be a regular, unlinked file")
        try:
            expected.unlink()
        except OSError as exc:
            raise CertificateError(f"cannot invalidate previous audit: {exc}") from exc
    return expected


def atomic_write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=True, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def verify_bundle(
    bundle: Path,
    *,
    workers: int,
    progress_every: int,
    audit_path: Path | None,
) -> dict[str, Any]:
    started = time.time()
    audit_path = prepare_audit_path(bundle, audit_path)
    checker_path = Path(__file__).resolve()
    core_path = checker_path.with_name("berry_core.py")
    manifest_path = bundle / "manifest.json"
    manifest, manifest_sha256, _ = load_json_bytes(
        manifest_path,
        "bundle manifest",
        max_bytes=MAX_BUNDLE_MANIFEST_BYTES,
    )
    installed = installed_flint_version()
    precision, entries = validate_bundle_manifest(
        bundle, manifest, checker_path, core_path
    )
    constants = build_constants(precision)
    self_test_global_reductions(constants)

    tasks = [
        (str(entry["path"]), entry["n"], entry["sha256"], entry["bytes"])
        for entry in entries
    ]
    summaries: list[ShardSummary] = []
    if workers == 1:
        for task in tasks:
            summaries.append(
                verify_shard(
                    Path(task[0]),
                    expected_n=task[1],
                    expected_sha256=task[2],
                    expected_bytes=task[3],
                    expected_precision=precision,
                    constants=constants,
                )
            )
            if progress_due(
                summaries[-1].n,
                len(summaries),
                len(tasks),
                progress_every,
            ):
                print(f"VERIFIED n={summaries[-1].n}; {len(summaries)}/8122", flush=True)
    else:
        with ProcessPoolExecutor(
            max_workers=workers,
            initializer=initialize_worker,
            initargs=(precision,),
        ) as executor:
            for summary in executor.map(worker_verify_shard, tasks, chunksize=1):
                summaries.append(summary)
                if progress_due(
                    summary.n,
                    len(summaries),
                    len(tasks),
                    progress_every,
                ):
                    print(
                        f"VERIFIED n={summary.n}; {len(summaries)}/8122",
                        flush=True,
                    )

    if [summary.n for summary in summaries] != list(range(2, 8124)):
        raise CertificateError("checker did not receive every n in order")
    worst_summary = max(
        summaries,
        key=lambda item: dyadic_fraction(
            item.worst_upper_mantissa, item.worst_upper_exponent
        ),
    )
    total_cells = sum(summary.cells for summary in summaries)
    source_hashes = bundle_source_hashes(checker_path.parents[1])
    audit = {
        "status": "ACCEPTED_FULL",
        "format": BUNDLE_FORMAT,
        "scope": {"n_start": 2, "n_end": 8123},
        "target": "9/20",
        "precision_bits": precision,
        "regularized_cot_terms": REGULARIZED_COT_TERMS,
        "python": sys.version,
        "python_flint": installed,
        "flint": flint.__FLINT_VERSION__,
        "platform": platform.platform(),
        "workers": workers,
        "verification_process": "fresh process sharing proof/berry_core.py",
        "manifest": str(manifest_path),
        "manifest_sha256": manifest_sha256,
        "certificate_set_sha256": manifest["certificate_set_sha256"],
        **source_hashes,
        "total_cells": total_cells,
        "worst_upper": worst_summary.worst_upper,
        "worst_upper_exact": worst_summary.worst_upper_exact,
        "worst_location": worst_summary.worst_location,
        "completed_at_utc": (
            datetime.now(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        ),
        "elapsed_seconds": time.time() - started,
        "n_summaries": [
            {
                "n": summary.n,
                "cells": summary.cells,
                "worst_upper": summary.worst_upper,
                "worst_upper_exact": summary.worst_upper_exact,
            }
            for summary in summaries
        ],
    }
    if audit_path is not None:
        atomic_write_json(audit_path, audit)
    return audit


def main() -> int:
    if __package__:
        print(
            "REJECTED: invoke proof/check_certificate.py directly; "
            "module execution would run an unverified package initializer",
            file=sys.stderr,
        )
        return 2
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--audit", type=Path)
    parser.add_argument(
        "--shard",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be at least 1")
    if args.workers > MAX_WORKERS:
        parser.error(f"workers must not exceed {MAX_WORKERS}")
    if args.progress_every < 0:
        parser.error("progress-every must be nonnegative")

    try:
        if args.shard:
            if args.audit is not None:
                raise CertificateError("--audit is available only for a full bundle")
            if not args.certificate.is_file():
                raise CertificateError("--shard requires one certificate JSON file")
            data, _, _ = load_json_bytes(
                args.certificate,
                "certificate shard",
                max_bytes=MAX_SHARD_BYTES,
            )
            precision, n_start, n_end = validate_common_header(
                data, SHARD_KEYS, SHARD_FORMAT
            )
            if n_start != n_end:
                raise CertificateError("--shard accepts exactly one n")
            installed_flint_version()
            constants = build_constants(precision)
            self_test_global_reductions(constants)
            summary = verify_shard(
                args.certificate,
                expected_n=n_start,
                expected_sha256=None,
                expected_bytes=None,
                expected_precision=precision,
                constants=constants,
            )
            print(
                f"ACCEPTED_SHARD n={summary.n} cells={summary.cells} "
                f"worst={summary.worst_upper}"
            )
            return 0

        if not args.certificate.is_dir():
            raise CertificateError(
                "the public checker requires a complete certificate bundle directory"
            )
        audit = verify_bundle(
            args.certificate,
            workers=args.workers,
            progress_every=args.progress_every,
            audit_path=args.audit,
        )
        print("ACCEPTED_FULL")
        print(f"cells: {audit['total_cells']}")
        print(
            f"worst certified upper: {audit['worst_upper']} "
            f"at {audit['worst_location']}"
        )
        print(f"certificate set sha256: {audit['certificate_set_sha256']}")
        return 0
    except Exception as exc:
        print(f"REJECTED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
