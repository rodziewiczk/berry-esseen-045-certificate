"""Fresh, guarded full native arithmetic for one literal n40--42 component."""
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
from all_indices.supervised import run_recorded
from uniform_tail.count_catalog import load, need, safe, sha
from uniform_tail.component40_catalog import final_json, validate_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--job-sha256", required=True)
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary unoptimized Python")
    work = args.work.resolve()
    need(work.parent == (BASE / "work").resolve() and not work.is_symlink(), "Owned private native epoch")
    raw = (work / "JOB.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.job_sha256, "Exact independently selected native job")
    job = load(raw)["job"]
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024 * runner.MIB
    install(runner)
    runner.parent_guard(work=work)
    runner.verify_sources()
    capsule = work / "capsule"
    need(capsule.is_dir() and not capsule.is_symlink(), "Private original source capsule")
    for name, pin in job["sources_sha256"].items():
        need(len(safe(name)) == 1 and sha(capsule / name) == pin, "All exact source/proof inputs")
    # Native build functions use cwd-relative mathematical inputs. Keep that
    # original cwd contract while scanning the ENTIRE private epoch for quotas.
    full_guard = runner.parent_guard
    epoch = work
    def epoch_guard(tiny=False, work=None):
        return full_guard(tiny=tiny, work=epoch)
    runner.parent_guard = epoch_guard
    prefix = work / "never-created-component-pycache"
    command = runner.python_command(capsule / job["script"], job["argv"], prefix)
    runner.launch_gate()
    stdout = run_recorded(runner, command, capsule, "component40-native", 7200,
                          512 * runner.MIB, prefix=prefix)
    result = validate_result(job, final_json(stdout))
    for name, pin in job["sources_sha256"].items():
        need(sha(capsule / name) == pin, "Original mathematical inputs unchanged after complete native rebuild")
    runner.parent_guard(work=work)
    report = {"status": "PASS_FRESH_NATIVE_ACTUAL40_42_COMPONENT_ONLY", "job_id": job["id"],
              "fresh_arithmetic": True, "native_result": result, "actual_native_command": command,
              "job_document_sha256": args.job_sha256, "native_stdout_sha256": sha(capsule / "component40-native.stdout.txt"),
              "source_files_sha256": job["sources_sha256"],
              "same_witness_INITIAL_contact_and_parent_acquisition_joins_verified": False,
              "global_sharp_C40_42_or_bridge40_48_verified": False,
              "all_index_conclusion_verified": False}
    with (work / "FRESH_COMPONENT40_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ACTUAL40_42_NATIVE_COMPONENT_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
