"""Small protected supervisor; archive metadata is not loaded in this process."""
import argparse
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--work",type=Path,required=True)
    args = p.parse_args()
    work = args.work.resolve()
    spec = importlib.util.spec_from_file_location("original_runner",BASE/"run_reproduction.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)

    from supervised import run_recorded
    def run_checked(*argv, **options):
        return run_recorded(r,*argv,**options)
    r.HOST_FLOOR = 1024*r.MIB
    r.require(work.parent == (BASE/"work").resolve() and not work.is_symlink(),
              "Explicit repository-owned work")
    r.parent_guard(work=work)
    r.verify_sources()
    worker = work/"capsule/c5_gapfree_worker.py"
    r.require(worker.is_file() and not (worker.parent/"FRESH_GAPFREE_RESULT.json").exists(),
              "Fresh independent gap-free epoch")
    prefix = work/"gapfree-fresh-pycache"
    r.launch_gate()
    run_checked(r.python_command(worker,[],prefix),work,"c5-gapfree-independent",
                7200,512*r.MIB,prefix=prefix)
    r.parent_guard(work=work)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_GAPFREE_PROCESS_INCOMPLETE: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
