"""Prepare or guardedly replay the exact original cutoff49 FULL native suite.

--run is explicit: 14 original top-level executions, including the complete
41-component retained suite. No quick-only success is promoted to a full run.
This remains relative to the package's written analytic and literature inputs.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import stat
import sys
import zipfile

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "reproduction"))
from all_indices.c5_inputs import extended
from all_indices.stable_guard import install
from all_indices.supervised import run_recorded
from uniform_tail.archive49_catalog import (ARCHIVE_BYTES, ARCHIVE_SHA, PREFIX, MANIFEST_SHA,
    FILE_COUNT, EXPANDED_BYTES, manifest, source_jobs, verify_sources, validate_full_result)
from uniform_tail.count_catalog import need, safe, sha


def require_supported_full_guard(runner, requested):
    if requested:
        need(runner.NATIVE is not None,
             "FULL BE49 currently requires the Windows whole-process-tree Job guard; no per-process POSIX substitute")


def prepare(archive, root, guard=lambda: None):
    """Copy the exact full capsule; no original file or old receipt is changed."""
    pins = manifest(archive.read(PREFIX + "MANIFEST.json"))
    pins = {**pins, "MANIFEST.json": MANIFEST_SHA}
    actual = {info.filename[len(PREFIX):] for info in archive.infolist()
              if info.filename.startswith(PREFIX) and not info.is_dir()}
    need(actual == set(pins) and len(actual) == FILE_COUNT, "Exact complete original archive inventory")
    total = 0
    root.mkdir(exist_ok=False)
    for index, (name, pin) in enumerate(pins.items()):
        if index % 32 == 0:
            guard()
        info = archive.getinfo(PREFIX + name)
        need(not stat.S_ISLNK(info.external_attr >> 16) and info.file_size <= 4 * 1024 ** 2,
             "Bounded original regular source file")
        raw = archive.read(info)
        need(hashlib.sha256(raw).hexdigest() == pin, "Exact original capsule file: " + name)
        total += len(raw)
        need(total <= EXPANDED_BYTES, "Exact full capsule byte census")
        destination = root.joinpath(*safe(name))
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(raw)
    need(total == EXPANDED_BYTES, "All original source bytes preserved")
    return pins


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--run", action="store_true", help="Run the complete native mathematical suite")
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Unoptimized ordinary Python")
    source = args.archive.resolve()
    need(source.is_file() and not source.is_symlink() and source.stat().st_size == ARCHIVE_BYTES
         and sha(source) == ARCHIVE_SHA, "Exact externally pinned original BE49 source archive")
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024 * runner.MIB
    install(runner)
    require_supported_full_guard(runner, args.run)
    runner.parent_guard()
    runner.verify_sources()
    # The source ZIP is small and the complete pinned capsule is only33.25MB.
    work = extended(runner.private_work())
    root = work / "original-BE49"
    with zipfile.ZipFile(source) as archive:
        prepare(archive, root, lambda: runner.parent_guard(work=work))
    new, retained = source_jobs(root)
    verify_sources(root)
    print(json.dumps({"event": "original_BE49_source_epoch_prepared", "work": str(work),
                      "files": FILE_COUNT, "bytes": EXPANDED_BYTES,
                      "native_arithmetic_executed": False}), flush=True)
    if not args.run:
        return
    worker = Path(__file__).with_name("archive49_worker.py")
    frozen_worker = work / worker.name
    shutil.copyfile(worker, frozen_worker)
    worker_sha = sha(frozen_worker)
    output = work / "fresh-full-result"
    prefix = work / "never-created-native-pycache"
    command = runner.python_command(frozen_worker,
        ["--root", str(root), "--output", str(output), "--pycache-prefix", str(prefix)], prefix)
    gc.collect()
    runner.launch_gate()
    # A single owned Job includes all nested native subprocesses, including
    # their aggregate CPU and memory. Original disk/pipe guards are retained.
    run_recorded(runner, command, work, "be49-original-full-suite", 7200,
                 512 * runner.MIB, prefix=prefix)
    need(sha(frozen_worker) == worker_sha, "Frozen invocation adapter unchanged")
    summary = validate_full_result(root, output, new, retained)
    verify_sources(root)
    runner.verify_sources()
    runner.parent_guard(work=work)
    report = {"status": "PASS_FRESH_ORIGINAL_BE49_SELECTED_FULL_SUITE",
              "scope": "Exact original package's FULL selected native acceptance suite, not an analytic formalization",
              "fresh_selected_native_suite": True, **summary,
              "source_archive_sha256": ARCHIVE_SHA, "original_manifest_sha256": MANIFEST_SHA,
              "original_capsule_files": FILE_COUNT, "original_source_bytes": EXPANDED_BYTES,
              "actual_guarded_wrapper_command": command,
              "original_driver_semantic_argv": [str(root / "verify.py"), "--output", str(output)],
              "invocation_adapter_sha256": worker_sha,
              "owned_job_cpu_limit_seconds": 7200, "owned_job_memory_limit_bytes": 512 * runner.MIB,
              "required_host_free_ram_bytes": 1024 * runner.MIB,
              "native_source_files_or_historical_receipts_edited": False,
              "all_analytic_and_literature_inputs_verified": False,
              "full_cutoff31_or_all_index_composition_verified": False,
              "all_index_conclusion_verified": False}
    with (work / "FRESH_BE49_FULL_SUITE_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("BE49_FULL_SUITE_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
