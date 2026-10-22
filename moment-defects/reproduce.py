#!/usr/bin/env python3
"""Explicit full-proof coverage and fresh finite arithmetic entry point.

No-argument mode is a PLAN, not a success result. --all fails closed until
every required numerical adapter is implemented and available.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/"reproduction"))
from all_indices.coverage import LITERATURE, obligations, order

IMPLEMENTED = {
    "n2": ("finite.py", ["--stage","n2"]),
    "n3": ("finite.py", ["--stage","n3-python"]),
    "n4": ("finite.py", ["--stage","n4"]),
    "c5.counts": ("c5_counts.py", []),
    "c5.gapfree": ("c5_gapfree.py", []),
    "c5.support": ("c5_support.py", []),
    "c5.high": ("c5_high.py", []),
    "c5.owncaps": ("c5_owncaps.py", []),
}


def plan():
    nodes = obligations()
    return {
        "scope":"REPRODUCTION_PLAN_NOT_MATHEMATICAL_VERIFICATION",
        "all_computational_obligations_verified":False,
        "literature_inputs":LITERATURE,
        "nodes":[dict(id=name, **nodes[name],
                      executable_adapter_present=name in IMPLEMENTED)
                 for name in order(nodes)],
        "known_missing_source_obligations":[
            "Seven selected n25 B3/B4 count forests require supply or fresh reconstruction.",
        ],
        "original_count_sources": [
            "https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff20-sources-2026-10-17",
            "https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff25-base-sources-2026-10-22",
        ],
        "composition_or_hashes_are_not_arithmetic_replay":True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--plan", action="store_true")
    modes.add_argument("--all", action="store_true")
    modes.add_argument("--component", choices=tuple(IMPLEMENTED))
    parser.add_argument("--archive", type=Path,
                        help="Exact public cutoff5_20261020.zip for c5.counts")
    parser.add_argument("--inspect", action="store_true",
                        help="Input catalog only; never mathematical acceptance")
    parser.add_argument("--backend", choices=("auto","cpp","python"), default="auto",
                        help="n3 backend; both rebuild/check the complete original certificate")
    parser.add_argument("--compiler-dir", type=Path, help="Private directory containing g++")
    parser.add_argument("--boost-dir", type=Path, help="Directory containing boost/multiprecision")
    args = parser.parse_args()
    if sys.flags.optimize:
        raise ValueError("Run without -O/-OO")
    if args.all:
        missing = [n for n in order(obligations()) if n not in IMPLEMENTED]
        if missing:
            print(json.dumps({"status":"INCOMPLETE_NO_ALL_INDEX_REPRODUCTION",
                              "missing_adapters":missing,
                              "all_computational_obligations_verified":False},indent=2))
            return 2
        raise RuntimeError("Global executor must be explicitly reviewed before enabling --all")
    if not args.component:
        print(json.dumps(plan(),indent=2))
        return 0
    name, extra = IMPLEMENTED[args.component]
    environment = dict(os.environ)
    if args.compiler_dir is not None:
        compiler_dir = args.compiler_dir.resolve()
        if not compiler_dir.is_dir():
            raise ValueError("Missing explicit compiler directory")
        environment["PATH"] = str(compiler_dir)+os.pathsep+environment.get("PATH","")
    if args.boost_dir is not None:
        boost_dir = args.boost_dir.resolve()
        if not (boost_dir/"boost/multiprecision/cpp_int.hpp").is_file():
            raise ValueError("Missing explicit Boost.Multiprecision headers")
        environment["CPLUS_INCLUDE_PATH"] = str(boost_dir)
    if args.component == "n3":
        compiler = shutil.which("g++",path=environment.get("PATH"))
        if args.backend == "cpp" and compiler is None:
            raise ValueError("Requested C++ backend has no compiler")
        use_cpp = args.backend == "cpp" or (args.backend == "auto" and compiler is not None)
        extra = ["--stage", "n3" if use_cpp else "n3-python"]
    command = [sys.executable,"-B","-S",str(BASE/"reproduction/all_indices"/name),*extra]
    if args.component in ("c5.counts","c5.gapfree","c5.support","c5.high","c5.owncaps"):
        if args.archive is None:
            parser.error("This component requires --archive; use the pinned public source asset")
        command += ["--archive",str(args.archive.resolve())]
        if args.inspect:
            command += ["--inspect" if args.component == "c5.counts" else "--prepare-only"]
    elif args.inspect:
        parser.error("--inspect is an input-catalog mode for c5.counts only")
    print(json.dumps({"event":"starting_explicit_component", "component":args.component,
                      "all_computational_obligations_verified":False}),flush=True)
    return subprocess.call(command,cwd=BASE,env=environment)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("REPRODUCTION_INCOMPLETE: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
