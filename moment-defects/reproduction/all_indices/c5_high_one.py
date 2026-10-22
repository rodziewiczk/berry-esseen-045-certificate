"""Fresh native HIGH epoch: unchanged arithmetic, checkers and honest captures.

Historical captures contain an absolute macOS cwd. They are not rewritten or
accepted as current executions. Instead this supervisor creates a new minimal
source epoch, runs both native actions, records their real captures, and then
runs the unchanged native acceptance code. Original candidate outputs are not
copied into that epoch. Analytic Fourier and acquired-support premises remain
external to these HIGH computations.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import sys
import time
import uuid

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, need, digest, unique
    from .c5_inputs import safe_relative, extended
    from .stable_guard import install
    from .supervised import run_recorded
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, need, digest, unique
    from c5_inputs import safe_relative, extended
    from stable_guard import install
    from supervised import run_recorded

sys.dont_write_bytecode = True
HIGH_ROOT = "work/cutoff5_20261020/high/"
VARIANTS = (
    ("high5_v1", "high5", "PASS_FRESH_LITERAL5_SUPPORTED_HIGH3", 3, 8),
    ("high5_eta_v1", "high5_eta", "PASS_FRESH_LITERAL5_SUPPORTED_ETA_HIGH4", 4, 9),
)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def source_at(root, name):
    parts = safe_relative(name)
    need(not any(root.joinpath(*parts[:j]).is_symlink()
                 for j in range(1, len(parts) + 1)), "No cached source symlink")
    path = root.joinpath(*parts)
    need(path.is_file() and path.resolve().is_relative_to(root.resolve()),
         "Source remains within its pinned cache")
    return path


def collect_sources(cache, graph, variant):
    """Select the exact native manifest closure, not a heuristic import search."""
    prefix = HIGH_ROOT + variant + "/"
    manifest_name = prefix + "MANIFEST.json"
    need(manifest_name in graph, "Selected native manifest is in the final graph")
    manifest = source_at(cache, manifest_name)
    need(digest(manifest) == graph[manifest_name], "Pinned native manifest bytes")
    pins = dict(read(manifest)["files_sha256"])
    for name in ("bound.py", "accept.py", "kernel.py", "universal.py", "MANIFEST.json"):
        original = prefix + name
        need(original in graph, "Complete original HIGH input: " + original)
        need(original not in pins or pins[original] == graph[original],
             "Manifest/final source binding agreement")
        pins[original] = graph[original]
    for name, pin in pins.items():
        need(graph.get(name) == pin, "Complete selected graph binds every native source")
        need(digest(source_at(cache, name)) == pin, "Exact native HIGH source: " + name)
    return pins


def verify_sources(root, pins):
    for name, pin in pins.items():
        need(digest(source_at(root, name)) == pin, "Unchanged selected HIGH source: " + name)


def persist_capture(epoch, directory, capture_prefix, action, command, input_pins,
                    stdout_file, started_utc, elapsed):
    """Record an already successful guarded native action, never an old receipt."""
    need(action in ("construct", "replay"), "Native HIGH action")
    output = "CONSTRUCTED.json" if action == "construct" else "REPLAY.json"
    need(command == [sys.executable, "-B", "bound.py", output],
         "Exact actual native HIGH command, including its cwd-relative script")
    need(directory.resolve().is_relative_to(epoch.resolve()), "Fresh owned native cwd")
    need(stdout_file.is_file(), "Real guarded stdout capture exists")
    for name, pin in input_pins.items():
        need(Path(name).name == name and digest(directory / name) == pin,
             "Native input bytes unchanged after the actual command")
    capture = epoch / "runs/cutoff5_20261020/high" / (capture_prefix + "_" + action + "01")
    capture.mkdir(parents=True, exist_ok=False)
    stdout = capture / "stdout.txt"
    shutil.copyfile(stdout_file, stdout)
    with (capture / "stderr.txt").open("xb"):
        pass  # The original guarded runner requires a successful empty stderr.
    metadata = {
        "command": command, "cwd": str(directory.resolve()),
        "python": sys.version, "platform": platform.platform(),
        "started_utc": started_utc,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": elapsed, "returncode": 0,
        "input_sha256": dict(input_pins), "stdout_sha256": digest(stdout),
        "stderr_sha256": digest(capture / "stderr.txt"),
        "scope": "NEW_ACTUAL_GUARDED_EXECUTION_NOT_RELOCATED_HISTORICAL_CAPTURE",
    }
    with (capture / "metadata.json").open("x", encoding="utf-8") as stream:
        json.dump(metadata, stream, indent=2)
    return capture


def private_epoch(runner):
    """Same repository-owned exclusive scratch invariants, with a short name."""
    root = (BASE / "work").resolve()
    need(not (BASE / "work").is_symlink() and root.parent == BASE.resolve(),
         "Repository-owned scratch root only")
    root.mkdir(exist_ok=True)
    epoch = root / ("h5-" + uuid.uuid4().hex[:12])
    epoch.mkdir(exist_ok=False)
    need(epoch.resolve().parent == root and not epoch.is_symlink()
         and runner.inside(epoch, BASE), "Exclusive private HIGH epoch inside the catalog")
    runner.require(shutil.disk_usage(epoch).free >= runner.DISK_FLOOR + runner.WORK_LIMIT,
                   "Scratch quota plus4GiB free disk")
    runner.RETAINED_WORK = epoch
    return epoch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
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
    need(digest(final) == FINAL_SHA, "Pinned complete selected C5 source graph")
    graph = read(final)["files_sha256"]
    need(len(graph) == 16576, "Complete original selected source graph")
    pins_by_variant = {row[0]: collect_sources(cache, graph, row[0]) for row in VARIANTS}
    pins = {}
    for selected in pins_by_variant.values():
        for name, pin in selected.items():
            need(name not in pins or pins[name] == pin, "Consistent combined native source closure")
            pins[name] = pin
    runner.launch_gate()
    epoch = private_epoch(runner)
    # The numerical child must have cwd=H for the untouched native capture
    # checker; its resource scan must nevertheless cover the ENTIRE epoch.
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
    print(json.dumps({"event": "fresh_native_high_epoch_started", "work": str(epoch),
                      "source_files": len(pins), "arithmetic_accepted": False}), flush=True)
    receipts = []
    for variant, capture_prefix, status, row_count, control_count in VARIANTS:
        directory = epoch / HIGH_ROOT / variant
        need(not any((directory / name).exists() for name in
                     ("CONSTRUCTED.json", "REPLAY.json", "HIGH_CHECKED.json")),
             "No historical numerical result in the fresh native epoch")
        for action, output in (("construct", "CONSTRUCTED.json"), ("replay", "REPLAY.json")):
            local_inputs = {p.name: digest(p) for p in directory.iterdir() if p.is_file()}
            command = [sys.executable, "-B", "bound.py", output]
            label = capture_prefix.replace("_", "-") + "-" + action
            runner.launch_gate()
            started_utc = datetime.now(timezone.utc).isoformat()
            started = time.monotonic()
            run_recorded(runner, command, directory, label, 7200, 512 * runner.MIB)
            persist_capture(epoch, directory, capture_prefix, action, command, local_inputs,
                            directory / (label + ".stdout.txt"), started_utc,
                            time.monotonic() - started)
            verify_sources(epoch, pins)
            runner.parent_guard(work=epoch)
        runner.launch_gate()
        label = capture_prefix.replace("_", "-") + "-accept"
        run_recorded(runner, [sys.executable, "-B", "accept.py"], directory,
                     label, 7200, 512 * runner.MIB)
        result = read(directory / "HIGH_CHECKED.json")
        need(result["status"] == status and type(result["n"]) is int and result["n"] == 5,
             "Original complete native HIGH acceptance")
        need(len(result["rows"]) == row_count and
             len(result["negative_controls"]) == control_count,
             "All native closed scopes and mutation controls")
        verify_sources(epoch, pins)
        verify_sources(cache, pins)
        receipts.append({"variant": variant, "status": status,
                         "native_receipt": str(directory / "HIGH_CHECKED.json"),
                         "sha256": digest(directory / "HIGH_CHECKED.json"),
                         "rows": row_count, "negative_controls": control_count})
        print(json.dumps({"event": "fresh_native_high_accepted", **receipts[-1]}), flush=True)
    runner.verify_sources()
    runner.parent_guard(work=epoch)
    report = {"scope": "C5_HIGH_NATIVE_FRESH_EPOCH_CONDITIONAL_ON_SUPPORT_AND_ANALYTIC_INPUTS",
              "status": "FRESH_BOTH_NATIVE_HIGH_PROTOCOLS_ACCEPTED", "fresh_arithmetic": True,
              "original_final_graph_sha256": FINAL_SHA, "source_files_sha256": pins,
              "receipts": receipts, "historical_captures_rewritten": False,
              "all_index_conclusion_verified": False}
    with (epoch / "FRESH_HIGH_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_HIGH_NATIVE_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
