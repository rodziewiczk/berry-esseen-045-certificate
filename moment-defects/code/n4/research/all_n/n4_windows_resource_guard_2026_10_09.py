"""Read-only Windows working-set monitor with STATIC ctypes bindings.

The original helper created a NEW Structure class and POINTER class on
EVERY call. CPython's ctypes pointer-type cache retains those classes,
so frequent guard checks artificially increased the monitored memory.
Here the PROCESS_MEMORY_COUNTERS class, pointer type, DLL handles and
function bindings are created ONCE at module import. EACH read allocates
only a small local instance; there is no shared mutable counters instance
and no per-call class/type definition or POINTER construction.

peak_bytes() returns the SAME Windows GetProcessMemoryInfo field
PeakWorkingSetSize as the old helper, in bytes, or None if that API read
fails. current_working_set_bytes() optionally returns WorkingSetSize.
On non-NT platforms both return None, exactly as the old peak helper.
No limit is raised or disabled: callers retain their existing256MiB limit.
No source monkeypatch, old edit, process launch, external write or math.

CLI performs2000 small read-only peak queries, checks the diagnostic
ctypes pointer-type cache count is unchanged, and checks no artificial
large growth in this isolated tiny test. Resource variation is diagnostic,
not a proof premise. No CDF/proof producer or numerical search is run.
"""

from __future__ import annotations

import ctypes
import json
import os
import time


if os.name == "nt":
    from ctypes import wintypes

    class _Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
            (name, ctypes.c_size_t) for name in (
                "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]

    # ALL classes/types/DLL objects/bindings below are constructed ONCE.
    _CountersPointer = ctypes.POINTER(_Counters)
    _kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    _psapi = ctypes.WinDLL("psapi", use_last_error=True)
    _get_current_process = _kernel.GetCurrentProcess
    _get_current_process.argtypes = []
    _get_current_process.restype = wintypes.HANDLE
    _get_process_memory_info = _psapi.GetProcessMemoryInfo
    _get_process_memory_info.argtypes = [wintypes.HANDLE, _CountersPointer, wintypes.DWORD]
    _get_process_memory_info.restype = wintypes.BOOL
    _current_process = _get_current_process()
    _counters_size = ctypes.sizeof(_Counters)
else:
    _Counters = _CountersPointer = _kernel = _psapi = None
    _get_current_process = _get_process_memory_info = _current_process = None
    _counters_size = None


def _read_counters():
    if os.name != "nt":
        return None
    counters = _Counters()  # small per-call INSTANCE, never a new class/type
    counters.cb = _counters_size
    if not _get_process_memory_info(_current_process, ctypes.byref(counters), counters.cb):
        return None
    return counters


def peak_bytes():
    """SAME WinAPI PeakWorkingSetSize in bytes; no class/cache growth."""
    counters = _read_counters()
    return None if counters is None else int(counters.PeakWorkingSetSize)


def current_working_set_bytes():
    """Optional read-only current WorkingSetSize in bytes."""
    counters = _read_counters()
    return None if counters is None else int(counters.WorkingSetSize)


# Friendly optional spelling; local new alias, no old namespace mutation.
current_working_set = current_working_set_bytes


def _pointer_cache_count():
    cache = getattr(ctypes, "_pointer_type_cache", None)
    return None if cache is None else len(cache)


def tiny_regressions(reads=2000):
    if type(reads) is not int or not 1 <= reads <= 2000:
        raise ValueError("At most2000 exact positive integer read-only queries")
    started = time.monotonic()
    # Warm the fixed bindings once before the diagnostic cache snapshot.
    first_peak, first_current = peak_bytes(), current_working_set_bytes()
    before_cache = _pointer_cache_count()
    maximum_peak, valid_reads = first_peak, 0
    for _ in range(reads):
        value = peak_bytes()
        if value is not None:
            if type(value) is not int or value <= 0:
                raise RuntimeError("Invalid WinAPI peak byte count")
            maximum_peak = value if maximum_peak is None else max(maximum_peak, value)
            valid_reads += 1
    after_cache = _pointer_cache_count()
    final_peak, final_current = peak_bytes(), current_working_set_bytes()
    if before_cache is not None and after_cache != before_cache:
        raise RuntimeError("Static monitor unexpectedly grew ctypes pointer-type cache")
    if os.name == "nt":
        if any(type(value) is not int or value <= 0 for value in
               (first_peak, first_current, final_peak, final_current)) or valid_reads != reads:
            raise RuntimeError("Windows resource-query tiny test requires available WinAPI reads")
        if final_peak < first_peak or final_peak < final_current or first_peak < first_current:
            raise RuntimeError("Peak/current WorkingSetSize fields inconsistent")
        growth = final_peak - first_peak
        # Tiny standalone diagnostic bound: the OLD 2000-type leak was
        # approximately16MiB. This is NOT a new proof memory allowance.
        if growth > 8 * 1024 * 1024:
            raise RuntimeError("Unexpected large working-set growth in isolated2000read test")
    else:
        if any(value is not None for value in (first_peak, first_current, final_peak, final_current)) or valid_reads:
            raise RuntimeError("Non-NT monitor must match old None semantics")
        growth = None
    return {"status": "STATIC_WINDOWS_RESOURCE_READ_ONLY_TINY_TEST",
            "platform": os.name, "read_only_peak_queries": reads, "successful_peak_queries": valid_reads,
            "ctypes_pointer_cache_count_before": before_cache,
            "ctypes_pointer_cache_count_after": after_cache,
            "pointer_cache_stable": before_cache == after_cache,
            "peak_before_bytes": first_peak, "peak_after_bytes": final_peak,
            "maximum_peak_bytes_diagnostic": maximum_peak,
            "current_before_bytes": first_current, "current_after_bytes": final_current,
            "peak_growth_bytes_diagnostic": growth,
            "elapsed_seconds_diagnostic": time.monotonic() - started,
            "memory_limit_changed": False, "old_modules_monkeypatched": False,
            "CDF_or_math_producer_called": False}


if __name__ == "__main__":
    print(json.dumps(tiny_regressions(), sort_keys=True))
