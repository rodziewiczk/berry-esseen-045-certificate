"""Guarded, fresh conditional complement arithmetic; parent joins remain open."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import uuid

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, need, digest
    from .c5_high_one import read, source_at, verify_sources
    from .c5_inputs import extended, safe_relative
    from .c5_owncaps_one import add_binding, add_manifest, invoke, persist_capture
    from .stable_guard import install
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, need, digest
    from c5_high_one import read, source_at, verify_sources
    from c5_inputs import extended, safe_relative
    from c5_owncaps_one import add_binding, add_manifest, invoke, persist_capture
    from stable_guard import install

sys.dont_write_bytecode = True
COMPLEMENT = "work/cutoff5_20261020/high/complement5_v1/"
REVIEW = "work/cutoff5_20261020/audit/complement5_readback_v1/"


def selected_sources(cache, graph):
    pins = {}
    add_manifest(cache, graph, pins, COMPLEMENT,
                 ("protocol.py", "accept.py", "PLAN.json", "MANIFEST.json",
                  "kernel.py", "batch.py", "integrate.py", "jet.py", "scalar.py", "pilot.py"))
    for name in ("check.py", "support_helper.py", "SOURCE_COPY.json", "PROOF.txt"):
        add_binding(cache, graph, pins, REVIEW + name)
    source = read(source_at(cache, REVIEW + "SOURCE_COPY.json"))
    need(source["sha256"] == graph.get(source["source"])
         == graph[REVIEW + "support_helper.py"], "Pinned independent helper source-copy equality")
    add_binding(cache, graph, pins, source["source"])
    forbidden = ("CONSTRUCTED.json", "REPLAY.json", "COMPLEMENT_CHECKED.json")
    need(not any(COMPLEMENT + name in pins for name in forbidden),
         "No historical selected integration/acceptance output copied")
    need(not any(name.startswith("runs/") or name.endswith("READBACK.json") for name in pins),
         "No old execution capture or independent acceptance is a fresh input")
    return pins


def private_epoch(runner):
    root = (BASE / "work").resolve()
    need(root.parent == BASE.resolve() and not (BASE / "work").is_symlink(), "Owned scratch root")
    root.mkdir(exist_ok=True)
    epoch = root / ("x5-" + uuid.uuid4().hex[:12])
    epoch.mkdir(exist_ok=False)
    need(epoch.resolve().parent == root and runner.inside(epoch, BASE), "Exclusive private complement epoch")
    need(shutil.disk_usage(epoch).free >= runner.DISK_FLOOR + runner.WORK_LIMIT,
         "Scratch quota plus original free-disk reserve")
    runner.RETAINED_WORK = epoch
    return epoch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary Python without -O/-OO")
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
    need(len(graph) == 16576, "Complete original selected graph")
    pins = selected_sources(cache, graph)
    if args.inspect:
        print(json.dumps({"scope": "C5_COMPLEMENT_SOURCE_SELECTION_ONLY",
                          "source_files": len(pins), "fresh_arithmetic": False}), flush=True)
        return
    runner.launch_gate()
    epoch = private_epoch(runner)
    guard = runner.parent_guard
    runner.parent_guard = lambda tiny=False, work=None: guard(tiny=tiny, work=epoch if work is not None else None)
    for name in pins:
        destination = epoch.joinpath(*safe_relative(name))
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_at(cache, name), destination)
    verify_sources(epoch, pins)
    document = {"schema": "C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_INPUTS_V1",
                "original_final_graph_sha256": FINAL_SHA, "source_files_sha256": pins}
    with (epoch / "COMPLEMENT_INPUTS.json").open("x", encoding="utf-8") as stream:
        json.dump(document, stream, indent=2)
    directory = epoch / COMPLEMENT
    print(json.dumps({"event": "fresh_conditional_complement_started", "work": str(epoch),
                      "source_files": len(pins), "arithmetic_accepted": False}), flush=True)
    captures = []
    for action, output in (("construct", "CONSTRUCTED.json"), ("replay", "REPLAY.json")):
        need(not (directory / output).exists(), "New complete integration output only")
        inputs = {p.name: digest(p) for p in directory.iterdir() if p.is_file()}
        command = [sys.executable, "-B", "protocol.py", action, "PLAN.json", output]
        stdout, started, elapsed = invoke(runner, epoch, directory, command, "complement-" + action)
        relative = "runs/cutoff5_20261020/high/complement_" + action + "01"
        capture = persist_capture(epoch, directory, relative, command, inputs, stdout, started, elapsed)
        captures.append({"action": action, "actual_metadata": str(capture / "metadata.json"),
                         "sha256": digest(capture / "metadata.json")})
        verify_sources(epoch, pins)
    worker = Path(__file__).with_name("c5_complement_worker.py")
    copied_worker = epoch / worker.name
    shutil.copyfile(worker, copied_worker)
    worker_pin = digest(copied_worker)
    invoke(runner, epoch, epoch, [sys.executable, "-B", "-S", str(copied_worker),
                                "--epoch", str(epoch)], "complement-independent-arithmetic")
    need(digest(copied_worker) == worker_pin, "Frozen arithmetic-only adapter unchanged")
    report_path = epoch / "FRESH_COMPLEMENT_ARITHMETIC_RESULT.json"
    report = read(report_path)
    need(report["status"] == "PASS_FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ONLY"
         and report["strips"] == 41 and report["attempts"] == 42
         and report["fresh_support_and_fourier_parent_joins_verified"] is False,
         "Complete conditional arithmetic receipt, not parent acquisition")
    verify_sources(epoch, pins)
    verify_sources(cache, pins)
    runner.verify_sources()
    runner.parent_guard(work=epoch)
    summary = {"scope": "C5_COMPLEMENT_ARITHMETIC_ONLY_NOT_FULL_C5_COMPLEMENT_COMPONENT",
               "status": "FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ACCEPTED",
               "fresh_arithmetic": True, "receipt": str(report_path), "sha256": digest(report_path),
               "source_files_sha256": pins, "adapter_worker_sha256": worker_pin,
               "actual_execution_captures": captures,
               "fresh_support_and_fourier_parent_joins_verified": False,
               "all_index_conclusion_verified": False}
    with (epoch / "FRESH_COMPLEMENT_SUPERVISOR_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(summary, stream, indent=2)
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
