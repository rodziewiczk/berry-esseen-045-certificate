"""Check two new complement integrations, not their unacquired analytic parents.

The original complete integration protocol is run twice by the supervisor.
This worker executes the unchanged arithmetic prefix of the pinned native
acceptor and calls the pinned independent ``fourier``/``rowcheck`` functions.
Historical capture paths and support receipts are never imported as evidence.
The three independent support-corruption tests belong to the separate parent
acquisition and are explicitly not claimed by this arithmetic-only receipt.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
NATIVE_SHA = "501b32d4770864dc76ea5ec01705773b4cfd9ae3e2405bd77f5f6a429c48a420"
READBACK_SHA = "14f7dba5e6423017e29047b895d5fdaf327fa97dc128a48173980dd24df0a54c"
HELPER_SHA = "a7db823efa7181da209fda02e2ea96ac2adfbe3cd3b43c48081bafcbb5f06d05"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def safe_source(epoch, name):
    """Standalone worker equivalent of the supervisor's closed relative paths."""
    need(type(name) is str and name and not any(c in name for c in ("\\", ":", "\x00")),
         "Canonical portable relative source name")
    parts = name.split("/")
    need(all(part not in ("", ".", "..") for part in parts), "No absolute path or parent traversal")
    for index in range(1, len(parts) + 1):
        need(not epoch.joinpath(*parts[:index]).is_symlink(), "No source symlink")
    path = epoch.joinpath(*parts)
    need(path.is_file() and path.resolve().is_relative_to(epoch.resolve()), "Source inside current epoch")
    return path


def captured_integration(epoch, directory, action):
    """Bind honest supervisor captures, never relocate historical macOS metadata.

    Metadata is evidence from the reviewed supervisor, not a mathematical
    substitute for executing the producer; it cannot certify its own history.
    """
    need(action in ("construct", "replay"), "One actual original integration action")
    capture = epoch / ("runs/cutoff5_20261020/high/complement_" + action + "01")
    meta = read(capture / "metadata.json")
    output = "CONSTRUCTED.json" if action == "construct" else "REPLAY.json"
    need(type(meta["returncode"]) is int and meta["returncode"] == 0
         and meta["cwd"] == str(directory.resolve())
         and meta["command"] == [sys.executable, "-B", "protocol.py", action, "PLAN.json", output]
         and meta["scope"] == "NEW_ACTUAL_GUARDED_NATIVE_EXECUTION"
         and meta["changed_inputs"] == [], "Exact current successful native integration capture")
    for stream in ("stdout", "stderr"):
        need(sha(capture / (stream + ".txt")) == meta[stream + "_sha256"], "Real captured stream bytes")
    need(not (capture / "stderr.txt").read_bytes(), "No successful native stderr")
    lines = (capture / "stdout.txt").read_text(encoding="utf-8").splitlines()
    need(lines and lines[-1].startswith("EXACT_SUPPORTED_COMPLEMENT5_WHOLE_COVER_PASS STRIPS 41"),
         "Complete native 41-strip terminal")
    need(type(meta["input_sha256"]) is dict and
         {"protocol.py", "PLAN.json", "MANIFEST.json"} <= meta["input_sha256"].keys(),
         "Actual producer and complete finite plan captured")
    for name, pin in meta["input_sha256"].items():
        need(type(name) is str and Path(name).name == name and name not in ("", ".", "..")
             and sha(directory / name) == pin, "Actual captured native input unchanged")
    return {"action": action, "metadata_sha256": sha(capture / "metadata.json"),
            "result_sha256": sha(directory / output)}


def assigned(node, name):
    return (isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name) and node.targets[0].id == name)


def native_arithmetic_prefix(tree):
    """Retain every original native arithmetic comparison and all ten controls."""
    boundaries = [i for i, node in enumerate(tree.body) if assigned(node, "manifest")]
    need(len(boundaries) == 1, "Unique native manifest/parent boundary")
    stop = boundaries[0]
    boundary = tree.body[stop]
    need(isinstance(boundary.value, ast.Call)
         and isinstance(boundary.value.func, ast.Name) and boundary.value.func.id == "read"
         and "MANIFEST.json" in ast.unparse(boundary.value), "Exact original boundary")
    selected = tree.body[:stop]
    need(any(isinstance(n, ast.FunctionDef) and n.name == "verify" for n in selected),
         "Full native arithmetic verifier retained")
    need(any(assigned(n, "controls") for n in selected)
         and isinstance(selected[-1], ast.For), "All native mutation controls retained")
    need(not any(assigned(n, "out") for n in selected), "No full native acceptance claimed")
    return ast.Module(body=selected, type_ignores=[])


def independent_arithmetic_controls(tree):
    """Keep the two complete Fourier mutation loops and duplicate-JSON test.

    The next loop in the original main tests support parents, not Fourier
    arithmetic. It is excluded together with all old receipt/capture reads.
    """
    mains = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
    need(len(mains) == 1, "Unique independent readback main")
    body = mains[0].body
    starts = [i for i, node in enumerate(body) if assigned(node, "controls")]
    need(len(starts) == 1, "Unique independent controls block")
    start = starts[0]
    selected = body[start:start + 4]
    need(len(selected) == 4 and isinstance(selected[1], ast.FunctionDef)
         and selected[1].name == "reject"
         and all(isinstance(n, ast.For) for n in selected[2:]),
         "Both complete independent Fourier mutation loops")
    need(not any(isinstance(n, ast.Name) and n.id == "supportobjects"
                 for n in ast.walk(ast.Module(body=selected, type_ignores=[]))),
         "Support mutation tests are not silently relabelled as arithmetic")
    duplicate = body[start + 5] if len(body) > start + 5 else None
    need(isinstance(duplicate, ast.Expr) and isinstance(duplicate.value, ast.Call)
         and isinstance(duplicate.value.func, ast.Name) and duplicate.value.func.id == "reject"
         and duplicate.value.args[-1].value == "duplicate JSON key",
         "Original duplicate-JSON negative control retained")
    return ast.Module(body=[*selected, duplicate], type_ignores=[])


def validate_two_results(native, readback, directory):
    """Run pinned mathematical acceptor functions on newly computed outputs."""
    raw_native = native.read_bytes()
    raw_readback = readback.read_bytes()
    need(hashlib.sha256(raw_native).hexdigest() == NATIVE_SHA, "Exact original native acceptor")
    need(hashlib.sha256(raw_readback).hexdigest() == READBACK_SHA,
         "Exact original independent readback")
    helper = readback.parent / "support_helper.py"
    need(sha(helper) == HELPER_SHA, "Exact independent arithmetic helper")
    namespace = {"__file__": str(native), "__name__": "frozen_complement_arithmetic"}
    prefix = native_arithmetic_prefix(ast.parse(raw_native, filename=str(native)))
    exec(compile(prefix, str(native), "exec"), namespace)
    need(len(namespace["controls"]) == len(set(namespace["controls"])) == 10,
         "All ten original native arithmetic controls")
    # Import only defines the original functions; its guarded main is not run.
    original_import_paths = list(sys.path)
    try:
        sys.path.insert(0, str(readback.parent))
        spec = importlib.util.spec_from_file_location("frozen_complement_readback", readback)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = original_import_paths
    need(Path(module.s.__file__).resolve() == helper.resolve(), "Original helper, not an import alias")
    plan = read(directory / "PLAN.json")
    constructed, replay = read(directory / "CONSTRUCTED.json"), read(directory / "REPLAY.json")
    need(module.s.exact(module.untimed(constructed), module.untimed(replay)),
         "All untimed results independently recomputed, including failed mesh attempt")
    need(replay["plan_sha256"] == sha(directory / "PLAN.json")
         and replay["manifest_sha256"] == sha(directory / "MANIFEST.json"),
         "Fresh results bind the exact finite plan and complete arithmetic manifest")
    summary = module.fourier(plan, replay)
    scope = dict(module.__dict__)
    scope.update(plan=plan, z=replay)
    controls = independent_arithmetic_controls(ast.parse(raw_readback, filename=str(readback)))
    exec(compile(controls, str(readback), "exec"), scope)
    need(len(scope["controls"]) == len(set(scope["controls"])) == 16,
         "All sixteen original Fourier/JSON independent controls")
    tail = Fraction(3031, 10000) * (1 + Fraction(323, 500) / Fraction(7361, 4000))
    need(tail == Fraction(819, 2000) < Fraction(4097, 10000),
         "Exact decreasing Shevtsova tail seam; theorem remains a cited input")
    need(sha(native) == NATIVE_SHA and sha(readback) == READBACK_SHA and sha(helper) == HELPER_SHA,
         "Original acceptance sources unchanged")
    return {"bands": summary, "native_controls": namespace["controls"],
            "independent_fourier_controls": scope["controls"],
            "published_tail_upper_at_start": str(tail)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epoch", type=Path, required=True)
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary unoptimized Python")
    epoch = args.epoch.resolve()
    inputs = read(epoch / "COMPLEMENT_INPUTS.json")
    need(inputs["schema"] == "C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_INPUTS_V1", "Input schema")
    pins = inputs["source_files_sha256"]
    need(type(pins) is dict and 0 < len(pins) <= 256, "Bounded unique source inventory")
    for name, pin in pins.items():
        need(type(pin) is str and len(pin) == 64 and set(pin) <= set("0123456789abcdef"),
             "Exact lowercase SHA-256 source pin")
        need(sha(safe_source(epoch, name)) == pin, "Complete pinned source remains inside current epoch")
    directory = epoch / "work/cutoff5_20261020/high/complement5_v1"
    review = epoch / "work/cutoff5_20261020/audit/complement5_readback_v1"
    captures = [captured_integration(epoch, directory, action) for action in ("construct", "replay")]
    result = validate_two_results(directory / "accept.py", review / "check.py", directory)
    report = {"status": "PASS_FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ONLY",
              "scope": "Supported n5 Fourier complement; all 41 closed strips, 42 attempts",
              "fresh_arithmetic": True, "n": 5, "strips": 41, "attempts": 42,
              "rho_finite": ["6/5", "7361/4000"], "target": "4097/10000", **result,
              "two_complete_native_integrations": True,
              "actual_native_captures": captures,
              "execution_freshness_requires_owning_supervisor_observation": True,
              "constructed_sha256": sha(directory / "CONSTRUCTED.json"),
              "replay_sha256": sha(directory / "REPLAY.json"),
              "native_arithmetic_acceptor_sha256": NATIVE_SHA,
              "independent_arithmetic_readback_sha256": READBACK_SHA,
              "input_document_sha256": sha(epoch / "COMPLEMENT_INPUTS.json"),
              "fresh_support_and_fourier_parent_joins_verified": False,
              "C4_attainment_contact_Prawitz_and_Shevtsova_inputs_verified": False,
              "conditional_parent_requirements": [
                  "The same unrestricted attained positive closed-CDF contrary n5 witness",
                  "Global all-law C4<=CE and the fixed-index contact/support theorem",
                  "Acquired support on each of the six exact closed rho bands",
                  "Reviewed Prawitz/global scalar profile and extended Fourier formulas",
                  "The cited Shevtsova2013 all-n iid .3031*(1+.646/rho) tail inequality"],
              "independent_support_controls_not_claimed": 3,
              "historical_captures_or_PASS_used_as_mathematical_premise": False,
              "native_full_complement_acceptance_claimed": False,
              "unrestricted_C5_or_all_indices_verified_by_this_stage": False}
    for name, pin in pins.items():
        need(sha(safe_source(epoch, name)) == pin, "All original source bytes unchanged")
    with (epoch / "FRESH_COMPLEMENT_ARITHMETIC_RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_COMPLEMENT_ARITHMETIC_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
