"""Fresh, serial, memory-bounded finite certificate replay using the pinned runner."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "run_reproduction.py"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("n2", "n3", "n3-python", "n4", "scalars"), required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("pinned_reproduction", RUNNER)
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)

    from supervised import run_recorded
    def run_checked(*argv, **options):
        return run_recorded(r,*argv,**options)
    r.HOST_FLOOR = 1024 * r.MIB  # Stronger than the published runner's floor.
    r.parent_guard()
    rows, size = r.verify_sources()
    r.launch_gate()
    work = r.private_work()
    if args.stage == "n4" and os.name == "nt":
        # Preserve the archival code; permit its legitimate deep checkpoints.
        work = Path("\\\\?\\"+str(work))
    source = r.copied_code(work, rows)
    print(json.dumps({"event": "fresh_replay_started", "stage": args.stage,
                      "private_work": str(work), "source_files": len(rows),
                      "memory_cap_MiB": 512, "host_floor_MiB": 1024}), flush=True)
    started = time.monotonic()
    if args.stage == "scalars":
        result = r.scalar_mode(work, source)
    elif args.stage == "n3-python":
        identity_prefix = work / "n3-identities-fresh-pycache"
        identity_output = run_checked(
            r.python_command(source/"n3/BE_three_summand_certificate/audit_initial_polynomials.py",
                             [], identity_prefix),
            work, "n3-initial-identities", 7200, 512*r.MIB,
            prefix=identity_prefix, source_root=source)
        r.require("ACCEPTED_ALL_INITIAL_IDENTITIES cells=111 orthants=444 exact_grid_identities=95904"
                  in identity_output.splitlines(), "All initial n3 polynomial identities")
        r.launch_gate()
        worker = Path(__file__).with_name("n3_integer.py")
        frozen_worker = work / worker.name
        shutil.copyfile(worker, frozen_worker)
        worker_sha = hashlib.sha256(frozen_worker.read_bytes()).hexdigest()
        prefix = work / "n3-python-fresh-pycache"
        output = run_checked(
            r.python_command(frozen_worker, ["--source", str(source/"n3/BE_three_summand_certificate"),
                                            "--progress", str(work/"n3-progress.jsonl")], prefix),
            work, "n3-python-integer", 7200, 512*r.MIB, prefix=prefix, source_root=source)
        r.require(hashlib.sha256(frozen_worker.read_bytes()).hexdigest() == worker_sha,
                  "Unchanged frozen independent Python worker")
        accepted = "ACCEPTED_FULL_N3_PYTHON 111 501156 219860 349"
        r.require(accepted in output.splitlines(), "Complete fresh Python integer n3 acceptance")
        result = {"scope":"FRESH_PYTHON_INTEGER_N3_REPLAY_NOT_CPP_EXECUTION",
                  "acceptance":accepted, "worker_result":json.loads(output.splitlines()[-1]),
                  "whole_paper_reproduced":False}
    elif args.stage in ("n2", "n3"):
        plans = {
            "n2": [
                ("n2/BE_two_summand_certificate/tensor_certificate.py", ["check"],
                 "n2-primary", "ACCEPTED_ALL_70_TENSOR_CELLS 35878 134"),
                ("n2/BE_two_summand_certificate/independent_integer_check.py", [],
                 "n2-independent", "ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK 35878 18426 134"),
            ],
            "n3": [
                ("n3/BE_three_summand_certificate/audit_initial_polynomials.py", [],
                 "n3-identities", "ACCEPTED_ALL_INITIAL_IDENTITIES cells=111 orthants=444 exact_grid_identities=95904"),
                ("n3/BE_three_summand_certificate/verify.py", [],
                 "n3-full", "ACCEPTED_FULL_N3 111 501156 219860 349"),
            ],
        }
        completed = []
        for name, argv, label, expected in plans[args.stage]:
            r.launch_gate()
            prefix = work / (label + "-fresh-pycache")
            print(json.dumps({"event": "checker_started", "checker": label}), flush=True)
            t0 = time.monotonic()
            output = run_checked(r.python_command(source / name, argv, prefix),
                                 work, label, 7200, 512 * r.MIB,
                                 prefix=prefix, source_root=source)
            r.require(expected in output.splitlines(), "Exact full acceptance line: " + label)
            completed.append({"checker": label, "acceptance": expected,
                              "wall_seconds": time.monotonic() - t0})
            print(json.dumps({"event": "checker_accepted", **completed[-1]}), flush=True)
        result = {"scope": "FRESH_COMPLETE_FINITE_" + args.stage.upper(),
                  "completed": completed, "whole_paper_reproduced": False}
    else:
        # Keep the original full ROOT4 contract, including both fresh passes.
        entry = source / "n4/research/all_n" / r.ENTRY
        receipt = entry.with_name(entry.stem + "_ALL260_W20_B13_N256_H1_8_ETA16_five_budget.json")
        r.require(not receipt.exists(), "No historical ROOT4 receipt as input")
        packets = []
        for index, flag in enumerate(("--produce", "--replay-existing")):
            r.launch_gate()
            prefix = work / ("n4-fresh-" + str(index) + "-pycache")
            print(json.dumps({"event": "checker_started", "checker": flag}), flush=True)
            output = run_checked(r.python_command(entry, [flag], prefix), work,
                                 "n4-fresh-" + str(index), 43200, 256 * r.MIB,
                                 prefix=prefix, source_root=source)
            packet = json.loads(output.splitlines()[-1], object_pairs_hook=r.unique_object)
            r.require(Path(packet["result"]).resolve() == receipt.resolve(),
                      "Fresh owned ROOT4 result path")
            expected = ("EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_PORTFOLIO"
                        if index == 0 else "READ_ONLY_REPLAY_ALL_NONRESOURCE_FIELDS_MATCH")
            r.require(packet["status"] == expected, "Exact fresh ROOT4 acceptance")
            summary = packet["summary"]
            r.require(summary["geometry_classes_total"] == summary["closed_geometry_classes"] == 260
                      and summary["unresolved_geometry_classes"] == 0
                      and summary["ALL_high_request_slots_accounted"] == 1300
                      and summary["fixed_geometry_max_depth"] == 1
                      and packet["unresolved_geometry_indices"] == []
                      and r.Fraction(summary["entire_conditional_root_score_upper_exact"]) <= r.TARGET,
                      "Complete all-260 ROOT4 at the original target")
            packets.append(packet)
            print(json.dumps({"event": "checker_accepted", "checker": flag}), flush=True)
        result = {"scope": "TWO_FRESH_CONDITIONAL_ROOT4_PASSES",
                  "upper_exact": packets[-1]["summary"]["entire_conditional_root_score_upper_exact"],
                  "whole_paper_reproduced": False}
    r.verify_sources()
    r.verify_sources(source)
    r.parent_guard(work=work)
    result.update(stage=args.stage, wall_seconds=time.monotonic() - started,
                  private_work=str(work), source_bytes=size,
                  all_index_conclusion_verified=False)
    report = work / "FRESH_REPLAY_RESULT.json"
    with report.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps({"event": "fresh_replay_complete", "result": result,
                      "report": str(report)}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("REPLAY_INCOMPLETE_NO_ACCEPTANCE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
