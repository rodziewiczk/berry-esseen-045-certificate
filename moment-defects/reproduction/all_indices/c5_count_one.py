"""Internal small supervisor for one fresh C5 count acceptance."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    spec = importlib.util.spec_from_file_location("pinned_runner", BASE/"run_reproduction.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)

    from supervised import run_recorded
    def run_checked(*argv, **options):
        return run_recorded(r,*argv,**options)
    r.HOST_FLOOR = 1024*r.MIB
    r.require(work.parent == (BASE/"work").resolve() and not work.is_symlink(),
              "One explicit repository-owned private work directory")
    r.parent_guard(work=work)
    r.verify_sources()
    capsule = work/"capsule"
    r.require(capsule.is_dir() and not capsule.is_symlink() and
              not (capsule/"COUNT_ACCEPTED.json").exists(), "Fresh capsule, no prior receipt")
    prefix = work/"count-fresh-pycache"
    r.launch_gate()
    run_checked(r.python_command(capsule/"count_protocol.py", ["accept"], prefix),
                work, "c5-count-native", 7200, 512*r.MIB, prefix=prefix)
    r.parent_guard(work=work)
    print(json.dumps({"event":"fresh_native_count_process_completed",
                      "receipt":str(capsule/"COUNT_ACCEPTED.json"),
                      "all_index_conclusion_verified":False}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_SINGLE_COUNT_INCOMPLETE: "+str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
