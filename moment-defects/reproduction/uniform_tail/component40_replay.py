"""List or serially replay ten actual native n40--42 mathematical components.

Unlike the old global40 composer, --run executes complete native object and
phase-cell reconstruction, not just saved captures or mathematical interfaces.
The resulting component theorem hypotheses remain explicitly conditional.
"""
import argparse
import gc
import hashlib
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
from uniform_tail.count_catalog import ARCHIVE_BYTES, ARCHIVE_SHA, canonical, member, need, sha
from uniform_tail.component40_catalog import catalog
from uniform_tail.coordinator import install_archive_guard, require_supported_branch, run_branch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--job", help="Exactly one literal job id from the catalog")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Unoptimized ordinary Python")
    source = args.archive.resolve()
    need(source.is_file() and not source.is_symlink() and source.stat().st_size == ARCHIVE_BYTES
         and sha(source) == ARCHIVE_SHA, "Exact original public cutoff25_20261011.zip")
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    install_archive_guard(runner)
    require_supported_branch(runner, args.run)
    def guard():
        runner.parent_guard()
    guard()
    with zipfile.ZipFile(source) as archive:
        jobs, graph = catalog(archive)
        selected = jobs if args.job is None else [job for job in jobs if job["id"] == args.job]
        need(selected and (args.job is None or len(selected) == 1), "Exact original native component selection")
        if not args.run:
            print(json.dumps({"scope": "ACTUAL40_42_NATIVE_SOURCE_CATALOG_ONLY", "jobs":
                [{"id": j["id"], "native": [j["script"], *j["argv"]], "source_files": len(j["sources_sha256"])}
                 for j in selected], "fresh_arithmetic": False}), flush=True)
            return
        ledger = runner.private_work()
        results = []
        for job in selected:
            guard()
            work = runner.private_work()
            capsule = work / "capsule"
            capsule.mkdir(exist_ok=False)
            total = 0
            for name, pin in job["sources_sha256"].items():
                raw = member(archive, job["folder"] + "/" + name, pin)
                total += len(raw)
                need(total <= 128 * runner.MIB, "Whole minimal component mirror <=128MiB")
                with (capsule / name).open("xb") as stream:
                    stream.write(raw)
            document = canonical({"schema": "ORIGINAL_NATIVE_ACTUAL40_42_JOB_V1", "job": job})
            with (work / "JOB.json").open("xb") as stream:
                stream.write(document)
            pin = hashlib.sha256(document).hexdigest()
            del raw, document
            gc.collect()
            command = [sys.executable, "-B", "-S", str(Path(__file__).with_name("component40_one.py")),
                       "--work", str(work), "--job-sha256", pin]
            run_branch(runner, command, work, "actual40-42-supervisor")
            result_path = work / "FRESH_COMPONENT40_RESULT.json"
            result = json.loads(result_path.read_text())
            need(result["status"] == "PASS_FRESH_NATIVE_ACTUAL40_42_COMPONENT_ONLY"
                 and result["job_id"] == job["id"], "New successful native component receipt")
            item = {"job_id": job["id"], "receipt": str(result_path), "sha256": sha(result_path)}
            results.append(item)
            with (ledger / (job["id"] + ".json")).open("x", encoding="utf-8") as stream:
                json.dump(item, stream, indent=2)
            print(json.dumps({"event": "fresh_native_actual40_42_component_accepted", **item}), flush=True)
        report = {"status": "FRESH_NATIVE_ACTUAL40_42_SELECTED_COMPONENTS_REPLAYED", "results": results,
                  "all_ten_native_components": args.job is None,
                  "same_witness_INITIAL_contact_and_parent_acquisition_joins_verified": False,
                  "global_sharp_bridge40_48_verified": False, "all_index_conclusion_verified": False}
        with (ledger / "FRESH_COMPONENT40_STAGE_RESULT.json").open("x", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2)
        print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("NATIVE_ACTUAL40_42_STAGE_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
