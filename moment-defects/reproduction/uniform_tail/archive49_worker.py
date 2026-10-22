"""Execute the unchanged full original BE49 driver inside the guarded Job.

Only invocation/environment bookkeeping is new. No mathematical statement,
native job, acceptance condition, source file or archived receipt is edited.
All subprocesses inherit the enclosing Job's CPU/memory limits and owned TMP.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pycache-prefix", type=Path, required=True)
    args = parser.parse_args()
    if sys.flags.optimize or not __debug__:
        raise ValueError("Ordinary Python without optimization")
    root, output, prefix = args.root.resolve(), args.output.resolve(), args.pycache_prefix.resolve()
    if output.exists() or prefix.exists() or output.parent != root.parent or prefix.parent != root.parent:
        raise ValueError("New owned sibling output and never-created bytecode prefix")
    # -B prevents writes; this separate absent prefix also excludes all old
    # bytecode reads in nested original Python commands which omit -X.
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["PYTHONPYCACHEPREFIX"] = str(prefix)
    os.environ["PYTHONNOUSERSITE"] = "1"
    os.environ.pop("PYTHONOPTIMIZE", None)
    script = root / "verify.py"
    actual = list(sys.argv)
    semantic = [str(script), "--output", str(output)]
    print(json.dumps({"event": "starting_unchanged_full_BE49_driver", "actual_wrapper_argv": actual,
                      "source_semantic_argv": semantic, "quick_mode": False}), flush=True)
    sys.argv = semantic
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        sys.argv = actual
    if prefix.exists():
        raise ValueError("Fresh bytecode prefix was polluted")


if __name__ == "__main__":
    main()
