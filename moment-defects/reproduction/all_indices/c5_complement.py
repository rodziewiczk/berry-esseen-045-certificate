"""Prepare original complement inputs, then run conditional arithmetic only.

This is deliberately not registered as the completed c5.complement proof
obligation: fresh support/Fourier parents and their same-witness joins remain.
"""
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
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--archive", type=Path)
    inputs.add_argument("--cache", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    if args.archive is not None:
        cache = extended(BASE / "reproduction_inputs" / ("c5-" + ARCHIVE_SHA[:16]))
        result = subprocess.call([sys.executable, "-B", "-S", str(here / "c5_inputs.py"),
                                  "--archive", str(args.archive.resolve()), "--destination", str(cache)])
        if result:
            return result
    else:
        cache = extended(args.cache.resolve())
    command = [sys.executable, "-B", "-S", str(here / "c5_complement_one.py"), "--cache", str(cache)]
    if args.prepare_only:
        command.append("--inspect")
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
