"""Prepare inputs, then recompute selected C5 owncaps and the coarse .429 input."""
import argparse
from pathlib import Path
import subprocess
import sys

if __package__:
    from .c5_counts import BASE, ARCHIVE_SHA
    from .c5_inputs import extended
else:
    from c5_counts import BASE, ARCHIVE_SHA
    from c5_inputs import extended

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    cache = extended(BASE / "reproduction_inputs" / ("c5-" + ARCHIVE_SHA[:16]))
    result = subprocess.call([sys.executable, "-B", "-S", str(here / "c5_inputs.py"),
                              "--archive", str(args.archive.resolve()),
                              "--destination", str(cache)])
    if result or args.prepare_only:
        return result
    return subprocess.call([sys.executable, "-B", "-S", str(here / "c5_owncaps_one.py"),
                            "--cache", str(cache)])


if __name__ == "__main__":
    raise SystemExit(main())
