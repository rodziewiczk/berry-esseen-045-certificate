"""Restart-safe one-shot construction and verification of the full certificate.

Certificate construction is parallelized by ``n`` and never uses cross-process
warm starts.  After all compact shards are present, a fresh fail-closed checker
process recomputes the complete bundle and is the only component allowed to
emit ``ACCEPTED_FULL``.  Construction and verification intentionally share the
published numerical implementation in ``proof/berry_core.py``.
"""
from __future__ import annotations

import argparse
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, BinaryIO

from proof.check_certificate import (
    BUNDLE_FORMAT,
    MAX_WORKERS,
    REQUIRED_FLINT,
    REQUIRED_PYTHON_FLINT,
    bundle_source_hashes,
    canonical_audit_path,
    certificate_set_digest,
    prepare_audit_path,
    progress_due,
    sha256_file,
)

from .parameter_bank import ParameterBank


MARKER_FORMAT = "berry-esseen-045-generated-shard-v2"
LEGACY_MARKER_FORMAT = "berry-esseen-045-generated-shard-v1"
# The v1 marker digest omitted these generator-time imports.  Existing v1
# markers are reusable only while the files still match the release that
# created the running computation.  New markers record their combined digest.
LEGACY_MARKER_SOURCE_HASHES = {
    "proof_package_sha256": (
        "afdc6a4abe8d3a98440d9dc5a9bac376b6b347cbaebe1646a5886c813b372afb"
    ),
    "parameter_bank_loader_sha256": (
        "1f261cd2a7613551e9f0ef9e734dcb418e696fd0a6e1b3f4fd4091d30374dbd4"
    ),
    "construction_package_sha256": (
        "762120bdd870f385e2edb7ddf3d3230331028680f781a9aa2dce0496faa66439"
    ),
}
PROGRESS_EVERY = 10


def acquire_run_lock(path: Path) -> BinaryIO:
    """Acquire a nonblocking process lock for the shared artifact tree."""
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = path.open("a+b")
    try:
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        record = (
            json.dumps(
                {
                    "pid": os.getpid(),
                    "started_utc": datetime.now(timezone.utc).isoformat(),
                },
                sort_keys=True,
            )
            + "\n"
        ).encode("ascii")
        stream.seek(0)
        stream.truncate()
        stream.write(record)
        stream.flush()
        os.fsync(stream.fileno())
        return stream
    except BaseException:
        stream.close()
        raise


def release_run_lock(stream: BinaryIO) -> None:
    if stream.closed:
        return
    try:
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
    finally:
        stream.close()


def atomic_write_json(path: Path, value: object, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(
            value,
            stream,
            ensure_ascii=True,
            sort_keys=True,
            **({"separators": (",", ":")} if compact else {"indent": 2}),
        )
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def configuration_digest(value: dict[str, Any]) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def marker_source_state(repository: Path) -> tuple[str, bool]:
    packaged = bundle_source_hashes(repository)
    marker_sources = {
        field: packaged[field] for field in LEGACY_MARKER_SOURCE_HASHES
    }
    return (
        configuration_digest(marker_sources),
        marker_sources == LEGACY_MARKER_SOURCE_HASHES,
    )


def child_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        environment[name] = "1"
    environment["PYTHONUNBUFFERED"] = "1"
    return environment


@dataclass(frozen=True)
class RunConfiguration:
    repository: Path
    bundle: Path
    work: Path
    parameter_bank: Path
    precision_bits: int
    max_pieces: int
    config_sha256: str
    marker_source_sha256: str
    allow_legacy_markers: bool


@dataclass(frozen=True)
class ConstructionResult:
    n: int
    status: str
    message: str


def marker_is_current(
    marker_path: Path,
    shard_path: Path,
    n: int,
    config_sha256: str,
    *,
    marker_source_sha256: str,
    allow_legacy: bool,
) -> bool:
    marker = load_json(marker_path)
    if marker is None or not shard_path.is_file():
        return False
    try:
        common_matches = (
            marker.get("n") == n
            and marker.get("config_sha256") == config_sha256
            and marker.get("certificate_sha256") == sha256_file(shard_path)
            and marker.get("bytes") == shard_path.stat().st_size
        )
        if not common_matches:
            return False
        if marker.get("format") == MARKER_FORMAT:
            return marker.get("marker_source_sha256") == marker_source_sha256
        return bool(
            marker.get("format") == LEGACY_MARKER_FORMAT and allow_legacy
        )
    except OSError:
        return False


def construct_one_n(n: int, config: RunConfiguration) -> ConstructionResult:
    shard = config.bundle / "n" / f"{n:04d}.json"
    marker = config.work / "markers" / f"{n:04d}.json"
    log = config.work / "logs" / f"{n:04d}.log"
    if marker_is_current(
        marker,
        shard,
        n,
        config.config_sha256,
        marker_source_sha256=config.marker_source_sha256,
        allow_legacy=config.allow_legacy_markers,
    ):
        return ConstructionResult(n, "reused", "hash-verified geometry already exists")

    temporary_dir = config.work / "temporary" / f"n{n:04d}"
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir(parents=True)
    temporary_shard = temporary_dir / f"{n:04d}.json"
    temporary_log = temporary_dir / f"{n:04d}.log"
    command = [
        sys.executable,
        "-m",
        "construction.generate_certificate",
        str(temporary_shard),
        "--parameter-bank",
        str(config.parameter_bank),
        "--n-start",
        str(n),
        "--n-end",
        str(n),
        "--precision-bits",
        str(config.precision_bits),
        "--max-pieces",
        str(config.max_pieces),
    ]
    with temporary_log.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("COMMAND: " + subprocess.list2cmdline(command) + "\n\n")
        stream.flush()
        process = subprocess.run(
            command,
            cwd=config.repository,
            env=child_environment(),
            stdout=stream,
            stderr=subprocess.STDOUT,
        )
    log.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(temporary_log, log)
    if process.returncode != 0 or not temporary_shard.is_file():
        return ConstructionResult(n, "failed", f"construction failed; see {log}")

    shard.parent.mkdir(parents=True, exist_ok=True)
    staging = shard.with_name(shard.name + ".tmp")
    shutil.copy2(temporary_shard, staging)
    os.replace(staging, shard)
    atomic_write_json(
        marker,
        {
            "format": MARKER_FORMAT,
            "n": n,
            "config_sha256": config.config_sha256,
            "marker_source_sha256": config.marker_source_sha256,
            "certificate_sha256": sha256_file(shard),
            "bytes": shard.stat().st_size,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
        },
    )
    shutil.rmtree(temporary_dir)
    return ConstructionResult(n, "generated", "new geometry constructed")


def build_manifest(config: RunConfiguration) -> Path:
    entries: list[dict[str, Any]] = []
    for n in range(2, 8124):
        shard = config.bundle / "n" / f"{n:04d}.json"
        if not shard.is_file():
            raise RuntimeError(f"missing certificate shard for n={n}")
        entries.append(
            {
                "n": n,
                "file": f"n/{n:04d}.json",
                "bytes": shard.stat().st_size,
                "sha256": sha256_file(shard),
            }
        )
    manifest = {
        "format": BUNDLE_FORMAT,
        "target": "9/20",
        "rho0": "712569/589000",
        "precision_bits": config.precision_bits,
        "python_flint": REQUIRED_PYTHON_FLINT,
        "flint": REQUIRED_FLINT,
        "scope": {"n_start": 2, "n_end": 8123},
        **bundle_source_hashes(config.repository),
        "parameter_bank_manifest_sha256": sha256_file(
            config.parameter_bank / "manifest.json"
        ),
        "certificate_set_sha256": certificate_set_digest(entries),
        "certificates": entries,
    }
    manifest_path = config.bundle / "manifest.json"
    atomic_write_json(manifest_path, manifest)
    return manifest_path


def run_checker(
    repository: Path,
    bundle: Path,
    work: Path,
    workers: int,
) -> int:
    audit = canonical_audit_path(bundle)
    prepare_audit_path(bundle, audit)
    log = work / "full_verification.log"
    command = [
        sys.executable,
        str(repository / "proof" / "check_certificate.py"),
        str(bundle),
        "--workers",
        str(workers),
        "--progress-every",
        str(PROGRESS_EVERY),
        "--audit",
        str(audit),
    ]
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("COMMAND: " + subprocess.list2cmdline(command) + "\n\n")
        stream.flush()
        process = subprocess.Popen(
            command,
            cwd=repository,
            env=child_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            stream.write(line)
            stream.flush()
            print(line, end="", flush=True)
        return process.wait()


def main() -> int:
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=repository / "artifacts" / "certificate",
    )
    parser.add_argument(
        "--parameter-bank",
        type=Path,
        default=repository / "data" / "parameter_bank",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(6, os.cpu_count() or 1),
    )
    parser.add_argument("--precision-bits", type=int, default=192)
    parser.add_argument(
        "--max-pieces",
        type=int,
        choices=(4096,),
        default=4096,
        help="fixed archival grid cap (4096)",
    )
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be at least 1")
    if args.workers > MAX_WORKERS:
        parser.error(f"workers must not exceed {MAX_WORKERS}")
    if not (96 <= args.precision_bits <= 16384):
        parser.error("precision-bits must lie in [96,16384]")
    bundle = args.output.resolve()
    parameter_bank = args.parameter_bank.resolve()
    work = bundle.parent / "work"
    core = repository / "proof" / "berry_core.py"
    constructor = repository / "construction" / "generate_certificate.py"

    try:
        run_lock = acquire_run_lock(work / "verification.lock")
    except OSError as exc:
        print(
            "ERROR: another verification is already using this artifacts tree "
            f"or its lock cannot be acquired: {exc}",
            file=sys.stderr,
        )
        return 2

    try:
        # Invalidate a receipt from any prior run before validation or construction
        # starts.  Once orchestration begins, failure leaves no ACCEPTED_FULL file.
        prepare_audit_path(bundle, canonical_audit_path(bundle))

        print(f"VALIDATING parameter bank: {parameter_bank}", flush=True)
        bank = ParameterBank(parameter_bank)
        bank.validate()
        print(f"PARAMETER BANK OK: {len(bank):,} cells", flush=True)

        # This compatibility digest is deliberately unchanged from bundle v1.  It
        # protects the mathematical inputs to generated shards and permits the
        # already-computed restart markers to be reused.  Previously omitted
        # generator imports are bound separately by v2 markers, and all packaged
        # source hashes are recorded and checked in the v2 bundle manifest.
        config_record = {
            "precision_bits": args.precision_bits,
            "max_pieces": args.max_pieces,
            "constructor_sha256": sha256_file(constructor),
            "core_sha256": sha256_file(core),
            "parameter_bank_manifest_sha256": sha256_file(
                parameter_bank / "manifest.json"
            ),
        }
        marker_source_sha256, allow_legacy_markers = marker_source_state(repository)
        config = RunConfiguration(
            repository=repository,
            bundle=bundle,
            work=work,
            parameter_bank=parameter_bank,
            precision_bits=args.precision_bits,
            max_pieces=args.max_pieces,
            config_sha256=configuration_digest(config_record),
            marker_source_sha256=marker_source_sha256,
            allow_legacy_markers=allow_legacy_markers,
        )
        for directory in (
            bundle / "n",
            work / "markers",
            work / "logs",
            work / "temporary",
        ):
            directory.mkdir(parents=True, exist_ok=True)

        pending = list(range(2, 8124))
        futures: dict[Future[ConstructionResult], int] = {}
        next_index = 0
        completed = 0
        completed_ns: set[int] = set()
        reported_through = 1
        failed = False
        print(
            f"CONSTRUCTING 8122 shards with {args.workers} workers; "
            "the run is restart-safe",
            flush=True,
        )
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            while next_index < len(pending) and len(futures) < args.workers:
                n = pending[next_index]
                futures[executor.submit(construct_one_n, n, config)] = n
                next_index += 1
            while futures:
                done, _ = wait(futures, return_when=FIRST_COMPLETED)
                for future in done:
                    n = futures.pop(future)
                    try:
                        result = future.result()
                    except Exception as exc:
                        result = ConstructionResult(n, "failed", repr(exc))
                    if result.status == "failed":
                        print(
                            f"FAILED n={n}: {result.message}",
                            file=sys.stderr,
                            flush=True,
                        )
                        failed = True
                    else:
                        completed += 1
                        completed_ns.add(n)
                        while reported_through + 1 in completed_ns:
                            reported_through += 1
                            if progress_due(
                                reported_through,
                                completed,
                                len(pending),
                                PROGRESS_EVERY,
                            ):
                                print(
                                    f"CONSTRUCTED through n={reported_through}; "
                                    f"successful={completed}/{len(pending)}",
                                    flush=True,
                                )
                    if not failed and next_index < len(pending):
                        next_n = pending[next_index]
                        futures[executor.submit(construct_one_n, next_n, config)] = next_n
                        next_index += 1
        if failed or completed != 8122:
            print(
                "Construction stopped before the complete bundle was available. "
                "Run the same command to resume.",
                file=sys.stderr,
            )
            return 2

        manifest = build_manifest(config)
        print(f"MANIFEST READY: {manifest}", flush=True)
        print("STARTING separate full verification process", flush=True)
        return_code = run_checker(repository, bundle, work, args.workers)
        if return_code != 0:
            print(
                f"Full verification failed; see {work / 'full_verification.log'}",
                file=sys.stderr,
            )
            return 2
        print(f"CERTIFICATE ACCEPTED: {bundle / 'verification.json'}", flush=True)
        return 0
    finally:
        release_run_lock(run_lock)


if __name__ == "__main__":
    raise SystemExit(main())
