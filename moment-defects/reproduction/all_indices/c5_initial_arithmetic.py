"""Serial fresh INITIAL arithmetic only; fresh-parent theorem joins stay open.

This entry is deliberately not registered as the complete c5.initial proof
obligation. Each native replay recomputes its entire fixed candidate, while
its numerical/contact/predecessor hypotheses remain explicit and unjoined.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

if __package__:
    from .c5_counts import BASE, ARCHIVE_SHA, digest, need, unique
    from .c5_inputs import extended
    from .c5_acquisition_plan import INITIAL_JOBS
else:
    from c5_counts import BASE, ARCHIVE_SHA, digest, need, unique
    from c5_inputs import extended
    from c5_acquisition_plan import INITIAL_JOBS

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument("--archive", type=Path)
    sources.add_argument("--cache", type=Path)
    parser.add_argument("--job", choices=tuple(job.job_id for job in INITIAL_JOBS))
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary nonoptimized runtime")
    here = Path(__file__).resolve().parent
    cache = extended(args.cache or BASE / "reproduction_inputs" / ("c5-" + ARCHIVE_SHA[:16]))
    if args.archive is not None:
        result = subprocess.call([sys.executable, "-B", "-S", str(here / "c5_inputs.py"),
                                  "--archive", str(args.archive.resolve()), "--destination", str(cache)])
        if result:
            return result
    jobs = [job for job in INITIAL_JOBS if args.job is None or job.job_id == args.job]
    if args.prepare_only:
        command = [sys.executable, "-B", "-S", str(here / "c5_acquisition_plan.py"),
                   "--inspect-cache", str(cache)]
        if args.job is not None:
            command += ["--job", args.job]
        return subprocess.call(command)
    reports = []
    for job in jobs:
        command = [sys.executable, "-B", "-S", str(here / "c5_initial_one.py"),
                   "--cache", str(cache), "--job", job.job_id]
        result = subprocess.run(command, capture_output=True)
        need(len(result.stdout) + len(result.stderr) <= 4 * 1024**2, "Bounded INITIAL supervisor output")
        if result.stdout:
            sys.stdout.buffer.write(result.stdout)
            sys.stdout.buffer.flush()
        if result.stderr:
            sys.stderr.buffer.write(result.stderr)
            sys.stderr.buffer.flush()
        if result.returncode:
            print(json.dumps({"scope": "INITIAL_ARITHMETIC_BATCH_INCOMPLETE",
                              "completed_job_reports": reports, "failed_job": job.job_id,
                              "fresh_parent_fact_joins_verified": False,
                              "all_index_conclusion_verified": False}), flush=True)
            return result.returncode
        report = json.loads(result.stdout.splitlines()[-1], object_pairs_hook=unique)
        need(report["job_id"] == job.job_id and report["fresh_arithmetic"] is True
             and report["fresh_parent_fact_joins_verified"] is False,
             "Exact successful conditional arithmetic receipt, not a parent theorem")
        path = Path(report["report_path"]).resolve()
        need(path.parent.parent == (BASE / "work").resolve()
             and path.name == "FRESH_INITIAL_ARITHMETIC_RESULT.json", "Owned fresh INITIAL report")
        need(json.loads(path.read_text(), object_pairs_hook=unique) == report,
             "Printed and saved INITIAL facts agree")
        reports.append({"job_id": job.job_id, "path": str(path), "sha256": digest(path)})
    print(json.dumps({"scope": "FRESH_INITIAL_ARITHMETIC_BATCH_NOT_ACQUIRED_C5_THEOREM",
                      "jobs_recomputed": len(reports), "reports": reports,
                      "fresh_parent_fact_joins_verified": False,
                      "all_index_conclusion_verified": False}), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("C5_INITIAL_ARITHMETIC_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
