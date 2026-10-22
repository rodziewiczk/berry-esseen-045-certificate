"""Fresh native count replays for the pinned n31--39 archival sub-DAG.

Default mode inspects the complete selection. Explicit --run executes actual
unchanged acceptors serially. No composer, old PASS or hash is treated as leaf
recomputation. This does not yet replay n40--48 or the uniform infinite tail.
"""
from __future__ import annotations

import argparse
import gc
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "reproduction"))
from uniform_tail.count_catalog import (ARCHIVE_BYTES, ARCHIVE_SHA, RECORD_SHA, STAGES,
                                       canonical, catalog, member, need, select, sha)
from uniform_tail.coordinator import install_archive_guard, require_supported_branch, run_branch


def prepare(archive, graph, job, work):
    capsule = work / "capsule"
    capsule.mkdir(exist_ok=False)
    inputs = dict(job["sources_sha256"])
    inputs[job["candidate"]] = job["candidate_sha256"]
    total = 0
    for name, pin in inputs.items():
        relative = job["folder"] + "/" + name
        need(graph.get(relative) == pin, "Explicit native input is bound by final pinned graph")
        raw = member(archive, relative, pin)
        total += len(raw)
        need(total <= 128 * 1024 ** 2, "Minimal per-job source/candidate mirror at most128MiB")
        with (capsule / name).open("xb") as stream:
            stream.write(raw)
    need(not (capsule / job["output"]).exists(), "Old accepted output never copied")
    document = {"schema": "PINNED_TAIL_STRICT_COUNT_JOB_V1", "job": job,
                "original_final_record_sha256": RECORD_SHA, "archive_sha256": ARCHIVE_SHA}
    with (work / "JOB.json").open("xb") as stream:
        stream.write(canonical(document))
    return sha(work / "JOB.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--job", help="Exactly one id from the pinned full stage catalog")
    parser.add_argument("--run", action="store_true", help="Execute actual expensive native arithmetic")
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary unoptimized Python")
    path = args.archive.resolve()
    need(path.is_file() and not path.is_symlink() and path.stat().st_size == ARCHIVE_BYTES
         and sha(path) == ARCHIVE_SHA, "Exact public cutoff25_20261011.zip source asset")
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    install_archive_guard(runner)
    require_supported_branch(runner, args.run)
    def guard():
        runner.parent_guard()
    guard()
    with zipfile.ZipFile(path) as archive:
        jobs, graph = catalog(archive)
        selected = select(jobs, args.stage, args.job)
        if not args.run:
            print(json.dumps({"scope": "PINNED_TAIL_COUNT_CATALOG_NOT_ARITHMETIC",
                              "stage": args.stage, "jobs": [{"id": j["id"], "n": j["n"],
                              "index": j["index"], "original_receipt": j["original_receipt"]}
                              for j in selected], "fresh_arithmetic": False,
                              "infinite_tail_verified": False}), flush=True)
            return
        ledger = runner.private_work()
        results = []
        for ordinal, job in enumerate(selected):
            guard()
            work = runner.private_work()
            pin = prepare(archive, graph, job, work)
            gc.collect()
            command = [sys.executable, "-B", "-S", str(Path(__file__).with_name("count_one.py")),
                       "--work", str(work), "--job-sha256", pin]
            run_branch(runner, command, work, "tail-count-supervisor")
            result_path = work / "FRESH_TAIL_COUNT_RESULT.json"
            result = json.loads(result_path.read_text())
            need(result["status"] == "PASS_FRESH_PINNED_TAIL_NATIVE_COUNT_ONLY"
                 and result["job_id"] == job["id"], "Fresh successful job-specific result")
            results.append({"job_id": job["id"], "receipt": str(result_path), "sha256": sha(result_path)})
            with (ledger / ("JOB_" + str(ordinal) + ".json")).open("x", encoding="utf-8") as stream:
                json.dump(results[-1], stream, indent=2)
            print(json.dumps({"event": "fresh_tail_count_replayed", "ordinal": ordinal,
                              "n": job["n"], **results[-1]}), flush=True)
        report = {"status": "FRESH_PINNED_TAIL_COUNT_SUBDAG_REPLAYED", "stage": args.stage,
                  "jobs": results, "whole_selected_count_stage": args.job is None,
                  "fresh_support_INITIAL_resource_Fourier_and_composition_verified": False,
                  "uniform_infinite_tail_verified": False, "all_index_conclusion_verified": False}
        with (ledger / "FRESH_TAIL_COUNT_STAGE_RESULT.json").open("x", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2)
        print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("TAIL_COUNT_SUBDAG_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
