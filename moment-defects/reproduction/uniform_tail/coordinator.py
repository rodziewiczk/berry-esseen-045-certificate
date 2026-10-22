"""Explicit archive256MiB / owned complete numerical-branch512MiB guards.

The original launcher creates the wrapper suspended, assigns it to an owned
kill-on-close Windows Job, and resumes it only afterwards. Nested native Jobs
retain their original limits. This avoids terminate-before-inner-Job races.
"""
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))
from reproduction.continuations.archive_guard import install as install_archive_guard
from reproduction.all_indices.supervised import run_recorded


def require_supported_branch(runner, requested=True):
    if requested:
        runner.require(runner.NATIVE is not None,
                       "Numerical tail coordinator requires Windows whole-process-tree Job containment")


def run_branch(runner, command, work, label):
    require_supported_branch(runner)
    runner.launch_gate()
    # 512MiB is for the ENTIRE wrapper+native branch, not512+64. The wrapper
    # still enforces its own64MiB peak and the native7200CPU/512MiB ceiling;
    # the outer Job is deliberately the stronger complete-branch restriction.
    return run_recorded(runner, command, work, label, 7200, 512 * runner.MIB)
