"""Small protected supervisor for one native, freshly recomputed tail count."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "reproduction"))
from all_indices.stable_guard import install
from uniform_tail.count_catalog import load, need, sha, verify_fresh_receipt, safe
from uniform_tail.coordinator import run_native_in_capsule


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--job-sha256", required=True)
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary unoptimized Python")
    work = args.work.resolve()
    need(work.parent == (BASE / "work").resolve() and not work.is_symlink(), "Owned fresh private work")
    raw = (work / "JOB.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.job_sha256, "Exact job selected by parent coordinator")
    document = load(raw)
    job = document["job"]
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024 * runner.MIB
    install(runner)
    runner.parent_guard(work=work)
    runner.verify_sources()
    capsule = work / "capsule"
    need(capsule.is_dir() and not capsule.is_symlink(), "Owned source capsule")
    inputs = dict(job["sources_sha256"])
    inputs[job["candidate"]] = job["candidate_sha256"]
    for name, pin in inputs.items():
        need(len(safe(name)) == 1 and sha(capsule / name) == pin, "Exact original native input")
    output = capsule / job["output"]
    need(not output.exists(), "No historical output in the fresh native capsule")
    prefix = work / "nonexistent-native-pycache"
    command = runner.python_command(capsule / job["script"], [str(job["index"])], prefix)
    run_native_in_capsule(runner, command, work, capsule, "tail-count-native", prefix)
    need(output.is_file() and not output.is_symlink(), "Full native acceptance output required")
    summary = verify_fresh_receipt(job, load(output.read_bytes()))
    for name, pin in inputs.items():
        need(sha(capsule / name) == pin, "Native source/candidate unchanged after full replay")
    runner.parent_guard(work=work)
    result = {"status": "PASS_FRESH_PINNED_TAIL_NATIVE_COUNT_ONLY", "job_id": job["id"],
              "fresh_arithmetic": True, **summary, "native_receipt": str(output),
              "native_receipt_sha256": sha(output), "job_document_sha256": args.job_sha256,
              "native_command": command,
              "support_INITIAL_resource_Fourier_and_same_witness_joins_verified": False,
              "uniform_infinite_tail_or_all_law_conclusion_verified": False}
    with (work / "FRESH_TAIL_COUNT_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("TAIL_COUNT_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
