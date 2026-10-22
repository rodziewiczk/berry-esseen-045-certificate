"""One protected, complete original INITIAL replay in its own fresh source epoch."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import sys
import time
import uuid

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, need, digest
    from .c5_high_one import read, source_at, verify_sources
    from .c5_inputs import extended, safe_relative
    from .c5_acquisition_plan import INITIAL_JOBS, inspect_job
    from .stable_guard import install
    from .supervised import run_recorded
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, need, digest
    from c5_high_one import read, source_at, verify_sources
    from c5_inputs import extended, safe_relative
    from c5_acquisition_plan import INITIAL_JOBS, inspect_job
    from stable_guard import install
    from supervised import run_recorded

sys.dont_write_bytecode = True


def control_names(source):
    """Read the original literal corruption-test inventory without importing it."""
    tree = ast.parse(source)
    assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == "mutations"
                           for target in node.targets)]
    need(len(assignments) == 1 and isinstance(assignments[0].value, ast.List),
         "One complete literal native INITIAL mutation inventory")
    names = []
    for row in assignments[0].value.elts:
        need(isinstance(row, ast.Tuple) and row.elts and isinstance(row.elts[0], ast.Constant)
             and type(row.elts[0].value) is str, "Literal original INITIAL mutation name")
        names.append(row.elts[0].value)
    names.append("duplicate JSON key")
    need(names and len(set(names)) == len(names), "All distinct original INITIAL corruption controls")
    return names


def canonical_native_sources(values):
    """Interpret fresh host-native path spellings, without rewriting a receipt.

    The archived replay adds str(relative_path) keys, which use backslashes on
    Windows. Existing frozen keys use POSIX spelling. Both must designate the
    same safe relative file and, if aliased, the same hash. This is metadata
    interpretation only; neither native source nor old/new JSON is edited.
    """
    need(type(values) is dict and values, "Complete fresh native source dictionary")
    normalized = {}
    for name, pin in values.items():
        need(type(name) is str and type(pin) is str and len(pin) == 64
             and all(x in "0123456789abcdef" for x in pin), "Typed exact native source commitment")
        relative = name.replace("\\", "/")
        safe_relative(relative)
        need(relative not in normalized or normalized[relative] == pin,
             "Host-native source aliases must have identical bytes")
        normalized[relative] = pin
    return normalized


def expected_rho(job):
    bounds = {"B0": (F(1), F(11, 10)), "BN": (F(11, 10), F(23, 20)),
              "B2": (F(23, 20), F(237, 200)), "B3": (F(237, 200), F(6, 5))}
    lo, hi = bounds[job.band]
    if job.sector is not None:
        middle = (lo + hi) / 2
        return (lo, middle) if job.sector < 2 else (middle, hi)
    return lo, hi


def validate_receipt(job, receipt, prepared, controls):
    need(receipt["status"] == job.expected_status and type(receipt["n"]) is int
         and receipt["n"] == 5 and receipt["band"] == job.band,
         "Original complete native INITIAL acceptance for this exact job")
    if job.sector is not None:
        need(type(receipt["sector"]) is int and receipt["sector"] == job.sector,
             "Literal freshly computed INITIAL sector")
    for name, expected in (("stages", job.stages), ("total_cells_per_stage", 2592), ("panels", 100)):
        need(type(receipt[name]) is int and receipt[name] == expected,
             "Complete native INITIAL census: " + name)
    need(type(receipt["final_active"]) is int and type(receipt["final_gap_active"]) is int
         and 0 <= receipt["final_active"] == receipt["final_gap_active"] <= 2592,
         "All final active moment cells are gap licensed")
    need(receipt["negative_controls"] == controls, "Every original mutation and duplicate-key control")
    need(receipt["input_sha256"] == prepared["input_sha256"], "Recomputed exact original INPUT identity")
    need(receipt["numerical_premises"] == {
        "predecessor_theorem": "user_assumed_C4_le_CE", "contact_error": "0",
        "owncap": job.owncap, "HIGH": job.high}, "Explicit unchanged conditional numerical premises")
    profile = receipt["profile"]
    radius = {"B0": "23/10", "BN": "12/5", "B2": "49/20", "B3": "99/40"}[job.band]
    need(type(profile["n"]) is int and type(profile["nmax"]) is int
         and profile["n"] == profile["nmax"] == 5, "Actual literal profile sample size")
    need(profile["q_contact"] == profile["barrier"] == "0" and profile["cap"] == job.owncap
         and all(profile[key] == radius for key in ("radius", "radius_minus", "radius_plus")),
         "Exact original support/contact/owncap profile")
    need(type(profile["grid"]) is list and profile["grid"] == [12, 12, 6, 3]
         and all(type(x) is int for x in profile["grid"]), "Complete original moment-cell grid")
    lo, hi = expected_rho(job)
    need(receipt["rho_interval"] == [str(lo), str(hi)]
         and profile["invariants"]["rho_lo"] == str(lo)
         and profile["invariants"]["rho"] == str(hi), "Exact closed rho domain")
    inv = profile["invariants"]
    beta = [inv["beta_lo"], inv["beta_hi"]]
    need(all(type(x) is str for x in beta) and -1 <= F(beta[0]) <= F(beta[1]) <= 1,
         "Explicit original closed signed-moment domain")
    if job.sector is not None:
        need(receipt["beta_interval"] == beta, "Same exact profile and exported beta domain")
    if job.family == "initial5_B3_top_accept_v3":
        need(receipt["partition_kind"] == "B3_TOP_BETA_1_5_3_10_B", "Actual selected top-beta partition")
    if job.family == "initial5_B3_T3lower_accept_v1":
        need(receipt["partition_kind"] == "B3_UPPER_RHO_BETA_3_10_17_50", "Actual selected T3lower partition")
    need(type(receipt["final_raw"]) is str and type(receipt["final_D"]) is str
         and 0 < F(receipt["final_raw"]) < 2 and 0 < F(receipt["final_D"]) < 6,
         "Complete original positive-density and physical-D domains")
    need(type(receipt["signed_support_rows"]) is int and receipt["signed_support_rows"] >= 0,
         "Typed complete signed-support inventory")
    return {"n": 5, "band": job.band, "sector": job.sector,
            "rho_interval": receipt["rho_interval"], "beta_interval": beta,
            "profile": profile, "numerical_premises": receipt["numerical_premises"],
            "stages": receipt["stages"], "cells_per_stage": 2592,
            "validated_closed_p_indices": list(range(100)),
            "final_active": receipt["final_active"], "final_gap_active": receipt["final_gap_active"],
            "final_raw": receipt["final_raw"], "final_D": receipt["final_D"],
            "signed_support_rows": receipt["signed_support_rows"],
            "input_candidate_sha256": receipt["input_sha256"],
            "partition_kind": receipt.get("partition_kind")}


def new_epoch(runner):
    root = (BASE / "work").resolve()
    need(root.parent == BASE.resolve() and not (BASE / "work").is_symlink(),
         "Repository-owned scratch root")
    root.mkdir(exist_ok=True)
    epoch = root / ("i5-" + uuid.uuid4().hex[:12])
    epoch.mkdir(exist_ok=False)
    need(epoch.resolve().parent == root and runner.inside(epoch, BASE), "Exclusive private INITIAL epoch")
    need(shutil.disk_usage(epoch).free >= runner.DISK_FLOOR + runner.WORK_LIMIT,
         "Scratch quota plus4GiB free disk")
    runner.RETAINED_WORK = epoch
    return epoch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--job", choices=tuple(job.job_id for job in INITIAL_JOBS), required=True)
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "No optimized mathematical replay")
    job = next(job for job in INITIAL_JOBS if job.job_id == args.job)
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024 * runner.MIB
    install(runner)
    runner.parent_guard()
    runner.verify_sources()
    cache = extended(args.cache)
    final = source_at(cache, FINAL)
    need(digest(final) == FINAL_SHA, "Pinned original complete C5 graph")
    graph = read(final)["files_sha256"]
    need(len(graph) == 16576, "Complete original selected source graph")
    inspection = inspect_job(cache, graph, job, guard=runner.parent_guard, include_sources=True)
    pins = inspection["source_files_sha256"]
    runner.launch_gate()
    epoch = new_epoch(runner)
    full_guard = runner.parent_guard
    def epoch_guard(tiny=False, work=None):
        return full_guard(tiny=tiny, work=epoch if work is not None else None)
    runner.parent_guard = epoch_guard
    for name in pins:
        target = epoch.joinpath(*safe_relative(name))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_at(cache, name), target)
    verify_sources(epoch, pins)
    runner.parent_guard(work=epoch)
    directory = epoch / job.directory
    output = epoch / job.output_paths[0]
    need(not output.exists(), "No old own INITIAL acceptance in the new source epoch")
    prepared = read(epoch / job.prepared)
    candidate = epoch / job.case_directory / "INPUT.json"
    need(digest(candidate) == prepared["input_sha256"], "Exact committed original candidate, not an assumed PASS")
    controls = control_names((directory / "replay.py").read_text())
    command = [sys.executable, "-B", "replay.py", *job.arguments]
    print(json.dumps({"event": "fresh_initial_arithmetic_started", "job_id": job.job_id,
                      "work": str(epoch), "source_files": len(pins),
                      "fresh_parent_fact_joins_verified": False}), flush=True)
    runner.launch_gate()
    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    run_recorded(runner, command, directory, "native-initial", 7200, 512 * runner.MIB)
    elapsed = time.monotonic() - started
    verify_sources(epoch, pins)
    verify_sources(cache, pins)
    native = read(output)
    facts = validate_receipt(job, native, prepared, controls)
    for name, pin in canonical_native_sources(native["files_sha256"]).items():
        need(digest(source_at(epoch, name)) == pin, "Fresh native INITIAL source graph unchanged")
    facts.update(input_candidate_path=str(candidate),
                 validated_p_export_json_pointer="/stages/" + str(job.stages - 1) + "/cover/panels")
    capture = epoch / "capture"
    capture.mkdir(exist_ok=False)
    shutil.copyfile(directory / "native-initial.stdout.txt", capture / "stdout.txt")
    with (capture / "stderr.txt").open("xb"):
        pass  # The original guarded runner accepts only successful empty-stderr stages.
    metadata = {"command": command, "cwd": str(directory.resolve()),
                "python": sys.version, "platform": platform.platform(),
                "started_utc": started_utc, "finished_utc": datetime.now(timezone.utc).isoformat(),
                "elapsed_seconds": elapsed, "returncode": 0, "input_sha256": pins,
                "stdout_sha256": digest(capture / "stdout.txt"),
                "stderr_sha256": digest(capture / "stderr.txt"),
                "native_result_sha256": digest(output)}
    with (capture / "metadata.json").open("x", encoding="utf-8") as stream:
        json.dump(metadata, stream, indent=2)
    runner.verify_sources()
    runner.parent_guard(work=epoch)
    report_path = epoch / "FRESH_INITIAL_ARITHMETIC_RESULT.json"
    report = {"schema": "C5_FRESH_CONDITIONAL_INITIAL_ARITHMETIC_V1",
              "scope": "FRESH_NATIVE_INITIAL_ARITHMETIC_ONLY_PARENT_FACT_JOINS_NOT_DISCHARGED",
              "job_id": job.job_id, "fresh_arithmetic": True,
              "fresh_parent_fact_joins_verified": False,
              "required_fresh_parent_fact_joins": job.required_fresh_fact_joins,
              "all_index_conclusion_verified": False,
              "original_final_graph_sha256": FINAL_SHA,
              "source_files_sha256": pins,
              "native_result_path": str(output), "native_result_sha256": digest(output),
              "capture_path": str(capture), "capture_metadata_sha256": digest(capture / "metadata.json"),
              "negative_controls": controls, "facts": facts,
              "elapsed_seconds": elapsed, "report_path": str(report_path)}
    with report_path.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    runner.parent_guard(work=epoch)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_INITIAL_NATIVE_ARITHMETIC_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
