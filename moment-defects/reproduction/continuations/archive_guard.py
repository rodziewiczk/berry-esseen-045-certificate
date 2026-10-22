"""Explicit256MiB archive-coordinator guard; native child limits are unchanged.

Opening116k immutable ZIP entries exceeds the original tiny coordinator's
64MiB peak allowance. This disclosed orchestration guard allows256MiB ONLY
for the coordinator. It retains or strengthens the original host reserve,
tiny CPU, free disk, private quota, containment and regular-file checks.
The original run_child and its512MiB native Job/RLIMIT limits are not edited.
"""
from __future__ import annotations
import shutil
import time

from ..all_indices.stable_guard import stable_inventory

MIB = 1024**2
HOST_RAM_MESSAGE = 'Available host RAM below1024MiB: no success result'


class HostRAMUnavailable(ValueError):
    """A resource interruption, never numerical acceptance or native rejection."""


def install(runner):
    runner.require(not getattr(runner,'_archive_coordinator_guard_installed',False),
                   'Archive-coordinator guard installed once')
    runner.require(runner.WORK_LIMIT == 256*MIB and runner.DISK_FLOOR >= 4*1024**3,
                   'Original private256MiB quota and4GiB disk reserve remain')
    runner.require(runner.LAUNCH_FLOOR >= 1536*MIB,'Original two-reading1536MiB launch gate remains')
    runner.HOST_FLOOR = max(runner.HOST_FLOOR,1024*MIB)

    def scalar_guard(tiny):
        peak = runner.own_peak()
        runner.require(type(peak) is int and peak <= 256*MIB,'Archive coordinator itself exceeds256MiB peak RSS')
        if runner.available_ram() < runner.HOST_FLOOR:
            raise HostRAMUnavailable(HOST_RAM_MESSAGE)
        if tiny:runner.require(time.process_time() < 10,'Entire tiny process CPU10s including imports')

    def parent_guard(tiny=False,work=None):
        scalar_guard(tiny)
        if work is not None:
            runner.require(shutil.disk_usage(work).free >= runner.DISK_FLOOR,'Private scratch disk floor4GiB')
            stable_inventory(work,runner.WORK_LIMIT)
            scalar_guard(tiny)

    runner.parent_guard = parent_guard
    runner._archive_coordinator_guard_installed = True
