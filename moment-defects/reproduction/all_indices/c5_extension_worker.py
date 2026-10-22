"""Run the complete Fourier-only subproof of the pinned independent review.

The original main also contains a disjoint B3 count-preparer source audit.
That historical preparer's inputs are not in the selected C5 delivery. This
adapter runs the original unchanged Fourier subproof in full: source-edit
reconstruction, all exact inequalities, all 25 cotangent comparisons, all
mutation controls, and the fresh FOURIER_CHECKED writer. It neither executes
nor claims the unrelated B3 preparer audit, and suppresses its misleading
combined status-print. No mathematical statement is inserted or changed.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
CHECK_SHA = "437bda0171e41f362879ee1c1d91c5c0be2871b20d005ef105967f0e55292cde"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def subproof(tree):
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "main"]
    need(len(functions) == 1, "One original independent review main")
    body = functions[0].body
    starts = [index for index, node in enumerate(body)
              if isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "src"]
    need(len(starts) == 1, "One explicit independent Fourier-subproof boundary")
    final = body[-1]
    need(isinstance(final, ast.Expr) and isinstance(final.value, ast.Call)
         and isinstance(final.value.func, ast.Name) and final.value.func.id == "print"
         and final.value.args and isinstance(final.value.args[0], ast.Constant)
         and final.value.args[0].value == "PASS_B3_PORT_AND_FOURIER_EXTENSION",
         "Only the combined nonmathematical final print is omitted")
    selected = body[starts[0]:-1]
    need(selected and isinstance(selected[-1], ast.Expr)
         and isinstance(selected[-1].value, ast.Call)
         and isinstance(selected[-1].value.func, ast.Name)
         and selected[-1].value.func.id == "write"
         and selected[-1].value.args[0].value == "FOURIER_CHECKED.json",
         "Complete Fourier subproof retains its original fresh receipt writer")
    return ast.Module(body=selected, type_ignores=[])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "No optimized proof execution")
    path = args.check.resolve()
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == CHECK_SHA, "Exact frozen independent-review source")
    need(not (path.parent / "FOURIER_CHECKED.json").exists(), "Fresh Fourier-review output")
    tree = ast.parse(raw, filename=str(path))
    selected = subproof(tree)
    spec = importlib.util.spec_from_file_location("frozen_fourier_review", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # The original guarded main is not called.
    exec(compile(selected, str(path), "exec"), module.__dict__)
    need(hashlib.sha256(path.read_bytes()).hexdigest() == CHECK_SHA,
         "Frozen review source unchanged after its complete Fourier subproof")
    result = json.loads((path.parent / "FOURIER_CHECKED.json").read_text())
    need(result["status"] == "PASS_INDEPENDENT_COTANGENT_AND_STABLE_RANGE_EXTENSION"
         and result["cotangent_comparisons"] == 25 and len(result["negative_controls"]) == 3,
         "All original Fourier-extension comparisons and controls")
    print(json.dumps({"scope": "FRESH_COMPLETE_FOURIER_SUBPROOF_NOT_B3_PREPARER_AUDIT",
                      "original_check_sha256": CHECK_SHA,
                      "cotangent_comparisons": 25, "negative_controls": 3,
                      "all_index_conclusion_verified": False}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FOURIER_EXTENSION_SUBPROOF_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
