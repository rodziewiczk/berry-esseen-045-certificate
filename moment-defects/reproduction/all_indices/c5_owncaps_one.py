"""Fresh native selected owncaps, including the independently needed .429 input.

The stronger selected B3 extended cap .412 replaces the old .414 cap. Missing
historical B3_v2 plans/outputs are not invented or claimed to be replayed.
Every selected native integration runs twice and its unchanged acceptance
checker consumes genuinely new execution captures. The separate coarse .429
bound runs all87 strips and its complete original independent readback.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
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
    from .stable_guard import install
    from .supervised import run_recorded
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, need, digest
    from c5_high_one import read, source_at, verify_sources
    from c5_inputs import extended, safe_relative
    from stable_guard import install
    from supervised import run_recorded

sys.dont_write_bytecode = True
HIGH = "work/cutoff5_20261020/high/"
EXTENSION = "work/cutoff5_20261020/audit/extensions_review_v2/"
AUX = "work/cutoff6_20261018/fourier/auxiliary5_v2/"
AUX_REVIEW = "work/cutoff6_20261018/audit/auxiliary5_readback_v1/"
AUX_PLAN = "runs/cutoff6_20261018/fourier/auxiliary5_v2/plan01/PLAN.json"
VARIANTS = (
    ("owncaps5_v3", "owncaps", "PASS_FRESH_LITERAL5_SUPPORTED_OWNCAPS3", 3),
    ("owncap_B3_ext_v1", "owncap_B3_ext", "PASS_FRESH_LITERAL5_EXTENDED_SUPPORTED_B3_OWNCAP", 1),
)
RUNTIME = ("protocol.py", "accept.py", "PLAN.json", "MANIFEST.json",
           "kernel.py", "batch.py", "integrate.py", "jet.py", "scalar.py", "pilot.py")


def add_binding(cache, graph, pins, name):
    need(name in graph, "Missing selected original source: " + name)
    pin = graph[name]
    need(name not in pins or pins[name] == pin, "Consistent selected source binding")
    need(digest(source_at(cache, name)) == pin, "Exact selected source: " + name)
    pins[name] = pin


def add_manifest(cache, graph, pins, prefix, required):
    add_binding(cache, graph, pins, prefix + "MANIFEST.json")
    manifest = read(source_at(cache, prefix + "MANIFEST.json"))["files_sha256"]
    for name, pin in manifest.items():
        need(graph.get(name) == pin, "Original manifest/final graph agreement")
        add_binding(cache, graph, pins, name)
    for name in required:
        add_binding(cache, graph, pins, prefix + name)


def selected_sources(cache, graph):
    pins = {}
    for variant, _, _, _ in VARIANTS:
        add_manifest(cache, graph, pins, HIGH + variant + "/", RUNTIME)
    # Only the Fourier part of this independent review is a parent of the
    # extended kernel. Its output is freshly recreated, never copied here.
    old_review = EXTENSION + "FOURIER_CHECKED.json"
    add_binding(cache, graph, pins, old_review)
    review = read(source_at(cache, old_review))
    need(review["status"] == "PASS_INDEPENDENT_COTANGENT_AND_STABLE_RANGE_EXTENSION",
         "Original selected Fourier-review identity")
    for name, pin in review["files_sha256"].items():
        need(graph.get(name) == pin, "Original Fourier-review source commitment")
        add_binding(cache, graph, pins, name)
    del pins[old_review]  # The old status is provenance, not a fresh mathematical premise.
    add_manifest(cache, graph, pins, AUX,
                 ("protocol.py", "batch.py", "integrate.py", "jet.py", "kernel.py"))
    for name in (AUX_PLAN, AUX_REVIEW + "readback.py", AUX_REVIEW + "REVIEW.txt"):
        add_binding(cache, graph, pins, name)
    for variant, _, _, _ in VARIANTS:
        need(not any(HIGH + variant + "/" + name in pins for name in
                     ("CONSTRUCTED.json", "REPLAY.json", "OWNCAPS_CHECKED.json")),
             "No old selected numerical output copied as a fresh premise")
    return pins


def persist_capture(epoch, directory, capture_relative, command, input_pins,
                    stdout_path, started_utc, elapsed, *, workspace_inputs=False,
                    result_path=None):
    """Persist only actual successful native commands; never edit old metadata."""
    need(command and command[0] == sys.executable and command[1:3] == ["-B", "protocol.py"],
         "Actual ordinary native protocol command")
    need(len(command) == 6 and command[3] in ("construct", "replay"),
         "Exact native action/plan/output command")
    action = command[3]
    if not workspace_inputs:
        need(command[4:] == ["PLAN.json", "CONSTRUCTED.json" if action == "construct" else "REPLAY.json"],
             "Exact original supported-owncap command")
    else:
        need(result_path is not None and command[5] == str(result_path)
             and Path(command[4]).is_absolute(), "Exact coarse absolute plan/result paths")
    need(directory.resolve().is_relative_to(epoch.resolve()), "Owned current native cwd")
    for name, pin in input_pins.items():
        # Original readback captures include str(relative_to(ROOT)) keys,
        # hence backslashes on Windows. Interpret that spelling locally;
        # preserve the actual native key bytes in metadata.input_sha256.
        path = epoch.joinpath(*safe_relative(name.replace("\\", "/"))) if workspace_inputs else directory / name
        need(workspace_inputs or Path(name).name == name, "Local captured source name")
        need(digest(path) == pin, "Actual native inputs unchanged after execution")
    capture = epoch.joinpath(*safe_relative(capture_relative))
    if capture.exists():
        need(workspace_inputs and result_path.parent == capture
             and {p.name for p in capture.iterdir()} == {"RESULT.json"},
             "Only the newly computed coarse result may preexist its capture")
    else:
        capture.mkdir(parents=True, exist_ok=False)
    with stdout_path.open("rb") as source, (capture / "stdout.txt").open("xb") as target:
        shutil.copyfileobj(source, target)
    with (capture / "stderr.txt").open("xb"):
        pass  # The guarded runner already requires empty stderr on success.
    metadata = {"command": command, "cwd": str(directory.resolve()),
                "python": sys.version, "platform": platform.platform(),
                "started_utc": started_utc, "finished_utc": datetime.now(timezone.utc).isoformat(),
                "elapsed_seconds": elapsed, "returncode": 0, "changed_inputs": [],
                "input_sha256": dict(input_pins),
                "stdout_sha256": digest(capture / "stdout.txt"),
                "stderr_sha256": digest(capture / "stderr.txt"),
                "scope": "NEW_ACTUAL_GUARDED_NATIVE_EXECUTION"}
    if result_path is not None:
        metadata["RESULT.json_sha256"] = digest(result_path)
    with (capture / "metadata.json").open("x", encoding="utf-8") as stream:
        json.dump(metadata, stream, indent=2)
    return capture


def new_epoch(runner):
    root = (BASE / "work").resolve()
    need(root.parent == BASE.resolve() and not (BASE / "work").is_symlink(),
         "Repository-owned scratch root")
    root.mkdir(exist_ok=True)
    epoch = root / ("o5-" + uuid.uuid4().hex[:12])
    epoch.mkdir(exist_ok=False)
    need(epoch.resolve().parent == root and runner.inside(epoch, BASE), "Exclusive private epoch")
    need(shutil.disk_usage(epoch).free >= runner.DISK_FLOOR + runner.WORK_LIMIT,
         "Scratch quota plus4GiB free disk")
    runner.RETAINED_WORK = epoch
    return epoch


def invoke(runner, epoch, directory, command, label):
    runner.launch_gate()
    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    run_recorded(runner, command, directory, label, 7200, 512 * runner.MIB)
    runner.parent_guard(work=epoch)
    return directory / (label + ".stdout.txt"), started_utc, time.monotonic() - started


def auxiliary(runner, epoch, pins):
    directory = epoch / AUX
    plan = epoch / AUX_PLAN
    manifest = read(directory / "MANIFEST.json")
    input_pins = dict(manifest["files_sha256"])
    input_pins[str((directory / "MANIFEST.json").relative_to(epoch))] = digest(directory / "MANIFEST.json")
    input_pins[str(plan.relative_to(epoch))] = digest(plan)
    captures = {}
    for action in ("construct", "replay"):
        relative = "runs/cutoff6_20261018/fourier/auxiliary5_v2/" + action + "01"
        capture = epoch / relative
        capture.mkdir(parents=True, exist_ok=False)
        result = capture / "RESULT.json"
        command = [sys.executable, "-B", "protocol.py", action, str(plan), str(result)]
        label = "owncap-coarse-" + action
        stdout, started, elapsed = invoke(runner, epoch, directory, command, label)
        captures[action] = persist_capture(epoch, directory, relative, command, input_pins,
                                           stdout, started, elapsed, workspace_inputs=True,
                                           result_path=result)
        verify_sources(epoch, pins)
    review = epoch / AUX_REVIEW
    request = {"plan": AUX_PLAN, "plan_sha256": digest(plan),
               "manifest_sha256": digest(directory / "MANIFEST.json"),
               "output": AUX_REVIEW + "RESULT.json"}
    for action, capture in captures.items():
        request[action + "_capture"] = capture.relative_to(epoch).as_posix()
        request[action + "_metadata_sha256"] = digest(capture / "metadata.json")
    request_path = review / "FRESH_REQUEST.json"
    with request_path.open("x", encoding="utf-8") as stream:
        json.dump(request, stream, indent=2)
    invoke(runner, epoch, review, [sys.executable, "-B", "readback.py", str(request_path)],
           "owncap-coarse-readback")
    result = read(review / "RESULT.json")
    need(result["status"] == "PASS_INDEPENDENT_GLOBAL_AUXILIARY5_READBACK"
         and result["n"] == [5] and type(result["n"][0]) is int
         and result["strips"] == result["exact_rows"] == 87
         and result["negative_controls"] == 24
         and Fraction(result["uniform_upper"]) < Fraction(429, 1000),
         "Complete independently accepted fresh global .429 input")
    return {"scope": "FRESH_GLOBAL_COARSE_C5_LT_429_1000", "fresh_arithmetic": True,
            "native_receipt": str(review / "RESULT.json"),
            "sha256": digest(review / "RESULT.json"), "strips": 87,
            "negative_controls": 24, "uniform_upper": result["uniform_upper"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "No optimized proof execution")
    spec = importlib.util.spec_from_file_location("original_runner", BASE / "run_reproduction.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024 * runner.MIB
    install(runner)
    runner.parent_guard()
    runner.verify_sources()
    cache = extended(args.cache)
    final = source_at(cache, FINAL)
    need(digest(final) == FINAL_SHA, "Pinned complete selected C5 graph")
    graph = read(final)["files_sha256"]
    need(len(graph) == 16576, "Complete original selected source graph")
    pins = selected_sources(cache, graph)
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
    print(json.dumps({"event": "fresh_owncaps_epoch_started", "work": str(epoch),
                      "source_files": len(pins), "arithmetic_accepted": False}), flush=True)
    coarse = auxiliary(runner, epoch, pins)
    print(json.dumps({"event": "fresh_coarse_owncap_accepted", **coarse}), flush=True)
    worker = Path(__file__).with_name("c5_extension_worker.py")
    frozen_worker = epoch / worker.name
    shutil.copyfile(worker, frozen_worker)
    worker_pin = digest(frozen_worker)
    review = epoch / EXTENSION
    invoke(runner, epoch, review,
           [sys.executable, "-B", str(frozen_worker), "--check", str(review / "check.py")],
           "owncap-fourier-extension")
    need(digest(frozen_worker) == worker_pin, "Frozen Fourier-subproof adapter unchanged")
    receipts = []
    for variant, capture_prefix, status, bands in VARIANTS:
        directory = epoch / HIGH / variant
        need(not any((directory / name).exists() for name in
                     ("CONSTRUCTED.json", "REPLAY.json", "OWNCAPS_CHECKED.json")),
             "Fresh supported-owncap epoch without old selected outputs")
        for action, output in (("construct", "CONSTRUCTED.json"), ("replay", "REPLAY.json")):
            input_pins = {p.name: digest(p) for p in directory.iterdir() if p.is_file()}
            command = [sys.executable, "-B", "protocol.py", action, "PLAN.json", output]
            label = capture_prefix.replace("_", "-") + "-" + action
            stdout, started, elapsed = invoke(runner, epoch, directory, command, label)
            relative = "runs/cutoff5_20261020/high/" + capture_prefix + "_" + action + "01"
            persist_capture(epoch, directory, relative, command, input_pins,
                            stdout, started, elapsed)
            verify_sources(epoch, pins)
        invoke(runner, epoch, directory, [sys.executable, "-B", "accept.py"],
               capture_prefix.replace("_", "-") + "-accept")
        result = read(directory / "OWNCAPS_CHECKED.json")
        need(result["status"] == status and type(result["n"]) is int and result["n"] == 5
             and len(result["bands"]) == bands and len(result["negative_controls"]) == 10,
             "Complete original selected owncap acceptance and all controls")
        receipts.append({"variant": variant, "status": status,
                         "native_receipt": str(directory / "OWNCAPS_CHECKED.json"),
                         "sha256": digest(directory / "OWNCAPS_CHECKED.json"),
                         "bands": bands, "negative_controls": 10})
        verify_sources(epoch, pins)
        verify_sources(cache, pins)
        print(json.dumps({"event": "fresh_selected_owncap_accepted", **receipts[-1]}), flush=True)
    need(Fraction(103, 250) < Fraction(207, 500), "Selected .412 implies the required old .414 cap")
    runner.verify_sources()
    runner.parent_guard(work=epoch)
    report = {"scope": "C5_COARSE_AND_SELECTED_OWNCAPS_CONDITIONAL_ON_EXPLICIT_ANALYTIC_AND_SUPPORT_INPUTS",
              "status": "FRESH_COARSE_AND_SELECTED_OWNCAPS_ACCEPTED", "fresh_arithmetic": True,
              "original_final_graph_sha256": FINAL_SHA, "source_files_sha256": pins,
              "coarse_429": coarse, "receipts": receipts,
              "B3_replacement": {"fresh_cap": "103/250", "implied_old_cap": "207/500",
                                  "historical_B3_v2_replay_claimed": False},
              "fresh_fourier_extension_review": str(review / "FOURIER_CHECKED.json"),
              "fourier_subproof_adapter_sha256": worker_pin,
              "historical_captures_rewritten": False, "all_index_conclusion_verified": False}
    with (epoch / "FRESH_OWNCAPS_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_OWNCAPS_NATIVE_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
