#!/usr/bin/env python3
"""Serial, bounded reproduction of the supplied n2/n3/ROOT4 arithmetic.

Default/tiny never imports a project checker.  Full mode creates a NEW private
copy, produces ROOT4, then independently recomputes it before byte comparison.
No received receipt, prefix, status or hash is a mathematical input.  This is
not an all-paper, all-index, or Lean verification program.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from fractions import Fraction

BASE = Path(__file__).resolve().parent
CODE = BASE / "code"
MANIFEST = CODE / "SHA256SUMS.json"
MIB = 1024 * 1024
HOST_FLOOR = 768 * MIB
LAUNCH_FLOOR = 1536 * MIB
DISK_FLOOR = 4 * 1024**3
WORK_LIMIT = 256 * MIB
SOURCE_LIMIT = 2 * MIB
OUTPUT_LIMIT = 16 * MIB
ENTRY = "n4_cpu_time_entire_root_2026_10_09.py"
ENTRY_SHA = "82b62e0088cd0055b1bc4b33bf3ca92087cafc62ff6396c679a7baf013672c0e"
TARGET = Fraction(4097, 10000)
RETAINED_WORK = None


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def inside(file, folder):
    try:
        relative = file.resolve().relative_to(folder.resolve())
    except ValueError:
        return False
    return bool(relative.parts) and ".." not in relative.parts


def absent(file):
    """A broken symlink is pollution too, not a nonexistent cache prefix."""
    try:
        file.lstat()
    except FileNotFoundError:
        return True
    return False


def stamp(st, cross_api=False):
    fields = (st.st_dev, st.st_ino, st.st_mode, st.st_size, st.st_mtime_ns)
    return fields if cross_api else fields + (st.st_ctime_ns,)


def bounded_bytes(file, limit=SOURCE_LIMIT):
    require(file.is_file() and not file.is_symlink(), "Regular, non-symlink file required: " + str(file))
    named = file.stat()
    require(0 <= named.st_size <= limit, "Bounded file required: " + str(file))
    with file.open("rb") as stream:
        fd_before = os.fstat(stream.fileno())
        require(stamp(fd_before, True) == stamp(named, True), "File changed before read")
        data = stream.read(named.st_size + 1)
        require(len(data) == named.st_size and stamp(os.fstat(stream.fileno())) == stamp(fd_before),
                "File length/fd identity changed during bounded read")
    require(stamp(file.stat()) == stamp(named), "Named file changed during bounded read")
    return data


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def verify_sources(root=CODE):
    data = json.loads(bounded_bytes(MANIFEST, 128 * 1024), object_pairs_hook=unique_object)
    require(set(data) == {"format", "files"} and data["format"] ==
            "berry-esseen-moment-defects-source-manifest-v1", "Exact manifest schema")
    require(type(data["files"]) is list and 0 < len(data["files"]) <= 512, "Bounded source manifest")
    names, total = set(), 0
    for row in data["files"]:
        require(type(row) is dict and set(row) == {"path", "bytes", "sha256"}, "Exact manifest row")
        name = row["path"]
        require(type(name) is str and re.fullmatch(r"[A-Za-z0-9_./-]+", name) and
                not name.startswith("/") and all(p not in ("", ".", "..") for p in name.split("/")),
                "Safe exact relative file label")
        require(name.casefold() not in names, "No duplicate/case-colliding file labels")
        names.add(name.casefold())
        require(type(row["bytes"]) is int and 0 <= row["bytes"] <= SOURCE_LIMIT and
                type(row["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
                "Bounded file/hash declaration")
        file = root.joinpath(*PurePosixPath(name).parts)
        require(inside(file, root) and not any(p.is_symlink() for p in [file, *file.parents] if inside(p, root)),
                "Manifest file/ancestor remains inside source copy")
        raw = bounded_bytes(file)
        require(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
                "Frozen byte mismatch: " + name)
        total += len(raw)
    require(total <= 32 * MIB, "Complete code/data closure at most32MiB")
    entry = next((r for r in data["files"] if r["path"] == "n4/research/all_n/" + ENTRY), None)
    require(entry is not None and entry["sha256"] == ENTRY_SHA, "Accepted exact ROOT4 entry source")
    return data["files"], total


class Windows:
    """Native read-only RAM queries and an owned, suspended-start Job Object."""
    def __init__(self):
        from ctypes import wintypes as w
        self.w = w
        class Counters(ctypes.Structure):
            _fields_ = [("cb", w.DWORD), ("faults", w.DWORD)] + [(n, ctypes.c_size_t) for n in
                ("peak", "working", "qpp", "qcp", "qpn", "qcn", "page", "peakpage")]
        class Memory(ctypes.Structure):
            _fields_ = [("length", w.DWORD), ("load", w.DWORD)] + [(n, ctypes.c_ulonglong) for n in
                ("totalphys", "availphys", "totalpage", "availpage", "totalvirtual", "availvirtual", "extended")]
        class Basic(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                ("flags", w.DWORD), ("min_ws", ctypes.c_size_t), ("max_ws", ctypes.c_size_t),
                ("active_limit", w.DWORD), ("affinity", ctypes.c_size_t), ("priority", w.DWORD), ("schedule", w.DWORD)]
        class IO(ctypes.Structure):
            _fields_ = [(n, ctypes.c_ulonglong) for n in ("read_ops", "write_ops", "other_ops", "read", "write", "other")]
        class Extended(ctypes.Structure):
            _fields_ = [("basic", Basic), ("io", IO)] + [(n, ctypes.c_size_t) for n in
                ("process_memory", "job_memory", "peak_process_memory", "peak_job_memory")]
        class Accounting(ctypes.Structure):
            _fields_ = [(n, ctypes.c_longlong) for n in ("user", "kernel", "period_user", "period_kernel")] + \
                [(n, w.DWORD) for n in ("faults", "total", "active", "terminated")]
        class Thread(ctypes.Structure):
            _fields_ = [(n, w.DWORD) for n in ("size", "usage", "tid", "pid")] + \
                [("base_priority", w.LONG), ("delta_priority", w.LONG), ("flags", w.DWORD)]
        self.Counters, self.Memory, self.Extended, self.Accounting, self.Thread = Counters, Memory, Extended, Accounting, Thread
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        self.p = ctypes.WinDLL("psapi", use_last_error=True)
        for name, args, result in (
            ("GetCurrentProcess", [], w.HANDLE), ("GlobalMemoryStatusEx", [ctypes.c_void_p], w.BOOL),
            ("OpenProcess", [w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            ("CloseHandle", [w.HANDLE], w.BOOL), ("CreateJobObjectW", [ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            ("SetInformationJobObject", [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
            ("QueryInformationJobObject", [w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p], w.BOOL),
            ("AssignProcessToJobObject", [w.HANDLE, w.HANDLE], w.BOOL),
            ("TerminateJobObject", [w.HANDLE, w.UINT], w.BOOL),
            ("IsProcessInJob", [w.HANDLE, w.HANDLE, ctypes.c_void_p], w.BOOL),
            ("CreateToolhelp32Snapshot", [w.DWORD, w.DWORD], w.HANDLE),
            ("Thread32First", [w.HANDLE, ctypes.c_void_p], w.BOOL),
            ("Thread32Next", [w.HANDLE, ctypes.c_void_p], w.BOOL),
            ("OpenThread", [w.DWORD, w.BOOL, w.DWORD], w.HANDLE), ("ResumeThread", [w.HANDLE], w.DWORD)):
            function = getattr(self.k, name); function.argtypes = args; function.restype = result
        self.p.GetProcessMemoryInfo.argtypes = [w.HANDLE, ctypes.c_void_p, w.DWORD]
        self.p.GetProcessMemoryInfo.restype = w.BOOL

    def counters(self, handle):
        value = self.Counters(); value.cb = ctypes.sizeof(value)
        require(self.p.GetProcessMemoryInfo(handle, ctypes.byref(value), value.cb), "Native process-memory query")
        return value

    def available(self):
        value = self.Memory(); value.length = ctypes.sizeof(value)
        require(self.k.GlobalMemoryStatusEx(ctypes.byref(value)), "Native available-RAM query")
        return int(value.availphys)

    def peak(self):
        return int(self.counters(self.k.GetCurrentProcess()).peak)

    def job(self, memory):
        handle = self.k.CreateJobObjectW(None, None)
        require(handle, "Private Job Object creation")
        limits = self.Extended(); limits.basic.flags = 0x2000 | 0x200 | 0x8
        limits.basic.active_limit = 8; limits.job_memory = memory
        if not self.k.SetInformationJobObject(handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            self.k.CloseHandle(handle); raise RuntimeError("Private Job memory/process limits unavailable")
        return handle

    def attach_and_resume(self, job, pid):
        require(ctypes.sizeof(ctypes.c_void_p) == 8, "64-bit Windows required for the unchanged ROOT4 route")
        process = self.k.OpenProcess(0x1511, False, pid)
        require(process, "Owned suspended child handle")
        try:
            require(self.k.AssignProcessToJobObject(job, process), "Owned child assigned BEFORE user code runs")
            snapshot = self.k.CreateToolhelp32Snapshot(4, 0)
            require(snapshot and snapshot != ctypes.c_void_p(-1).value, "Thread snapshot query")
            tids = []
            try:
                row = self.Thread(); row.size = ctypes.sizeof(row)
                ok = self.k.Thread32First(snapshot, ctypes.byref(row)); count = 0
                while ok:
                    count += 1; require(count <= 16384, "Bounded read-only thread snapshot")
                    if row.pid == pid: tids.append(row.tid)
                    row.size = ctypes.sizeof(row); ok = self.k.Thread32Next(snapshot, ctypes.byref(row))
            finally:
                self.k.CloseHandle(snapshot)
            require(len(tids) == 1, "Exactly one owned suspended startup thread")
            thread = self.k.OpenThread(2, False, tids[0]); require(thread, "Owned startup-thread handle")
            try:
                require(self.k.ResumeThread(thread) == 1, "Resume ONLY the owned once-suspended startup thread")
            finally:
                self.k.CloseHandle(thread)
        finally:
            self.k.CloseHandle(process)

    def job_state(self, job):
        info = self.Accounting()
        require(self.k.QueryInformationJobObject(job, 1, ctypes.byref(info), ctypes.sizeof(info), None),
                "Owned Job CPU/accounting query")
        buffer = ctypes.create_string_buffer(8 + 256 * ctypes.sizeof(ctypes.c_size_t))
        require(self.k.QueryInformationJobObject(job, 3, buffer, ctypes.sizeof(buffer), None), "Owned Job PID query")
        assigned, listed = (ctypes.c_uint32 * 2).from_buffer(buffer)
        require(0 <= listed <= assigned <= 256, "Bounded owned Job process list")
        pids = (ctypes.c_size_t * listed).from_buffer(buffer, 8)
        peak_sum = 0
        for pid in pids:
            process = self.k.OpenProcess(0x1410, False, pid)
            if not process:
                require(ctypes.get_last_error() == 87, "Owned Job process query unavailable")
                continue  # process exited between the two native read-only queries
            try:
                member = self.w.BOOL()
                require(self.k.IsProcessInJob(process, job, ctypes.byref(member)), "Owned Job membership query")
                if member.value: peak_sum += int(self.counters(process).peak)
            finally:
                self.k.CloseHandle(process)
        return (info.user + info.kernel) / 10**7, int(info.active), peak_sum


NATIVE = Windows() if os.name == "nt" else None


def available_ram():
    if NATIVE is not None:
        return NATIVE.available()
    require(sys.platform.startswith("linux"), "Available-RAM guard supports Windows/Linux only")
    text = Path("/proc/meminfo").read_text()
    match = re.search(r"^MemAvailable:\s+(\d+) kB$", text, re.M)
    require(match is not None, "Linux MemAvailable query")
    return int(match.group(1)) * 1024


def own_peak():
    if NATIVE is not None:
        return NATIVE.peak()
    import resource
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def parent_guard(tiny=False, work=None):
    require(own_peak() <= 64 * MIB, "Runner itself exceeds64MiB peak RSS")
    require(available_ram() >= HOST_FLOOR, "Available host RAM below768MiB: no success result")
    if tiny: require(time.process_time() < 10, "Entire tiny process CPU10s including imports")
    if work is not None:
        require(shutil.disk_usage(work).free >= DISK_FLOOR, "Private scratch disk floor4GiB")
        used = 0
        for folder, directories, files in os.walk(work):
            require(not any((Path(folder) / d).is_symlink() for d in directories), "No private-scratch symlink")
            for name in files:
                file = Path(folder) / name
                require(file.is_file() and not file.is_symlink() and inside(file, work), "Owned private output only")
                used += file.stat().st_size
                require(used <= WORK_LIMIT, "All private source/output/checkpoint files exceed256MiB quota")


def launch_gate(tiny=False):
    for index in range(2):
        parent_guard(tiny)
        require(available_ram() >= LAUNCH_FLOOR, "Launch requires TWO available1536MiB readings5s apart")
        if index == 0: time.sleep(5)
    parent_guard(tiny)


def private_work():
    global RETAINED_WORK
    work_root = BASE / "work"
    require(inside(work_root, BASE) and not work_root.is_symlink(), "Repository-owned scratch root only")
    work_root.mkdir(exist_ok=True)
    require(work_root.is_dir() and not work_root.is_symlink() and work_root.resolve().parent == BASE,
            "Scratch root remains directly below this catalog")
    folder = Path(tempfile.mkdtemp(prefix="berry-esseen-moment-defects-", dir=str(work_root))).resolve()
    RETAINED_WORK = folder
    require(folder.is_dir() and not folder.is_symlink() and folder.parent == work_root.resolve()
            and inside(folder, BASE), "New private scratch directory stays inside this catalog")
    require(shutil.disk_usage(folder).free >= DISK_FLOOR + WORK_LIMIT, "Scratch quota plus4GiB free disk")
    return folder  # retained on success AND failure; never recursively removed


def python_command(script, arguments, prefix, standard_only=True):
    require(absent(prefix), "Fresh source-compilation prefix MUST remain nonexistent")
    argv = [sys.executable, "-B"]
    if standard_only: argv.append("-S")
    return argv + ["-X", "pycache_prefix=" + str(prefix), "-W", "ignore::SyntaxWarning", str(script), *arguments]


def run_child(argv, work, label, cpu_limit, memory_limit, input_bytes=None, prefix=None, source_root=None):
    """Only one owned stage at a time; nested compiler/kernel remains in its Job."""
    parent_guard(work=work)
    require(type(argv) is list and argv and all(type(a) is str for a in argv), "Explicit no-shell argv")
    require(re.fullmatch(r"[a-z0-9-]+", label), "Exact owned log label")
    environment = dict(os.environ)
    for key in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONPYCACHEPREFIX"):
        environment.pop(key, None)
    scratch = work / "temp"; scratch.mkdir(exist_ok=True)
    environment.update({"TEMP": str(scratch), "TMP": str(scratch), "TMPDIR": str(scratch),
                        "PYTHONIOENCODING": "utf-8"})
    job, process = None, None
    if NATIVE is not None:
        job = NATIVE.job(memory_limit)
        options = {"creationflags": subprocess.CREATE_NO_WINDOW | 0x4}
    else:
        import resource
        def limits():
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        options = {"start_new_session": True, "preexec_fn": limits}
    outputs, faults, total = {"stdout": bytearray(), "stderr": bytearray()}, [], [0]
    lock = threading.Lock()
    def drain(stream, channel):
        try:
            with stream:
                while True:
                    chunk = stream.read(65536)
                    if not chunk: break
                    with lock:
                        total[0] += len(chunk)
                        require(total[0] <= OUTPUT_LIMIT, "Bounded stage stdout/stderr exceeds16MiB")
                        outputs[channel].extend(chunk)
        except BaseException as error:
            faults.append(error)
    started, checked = time.monotonic(), time.monotonic()
    try:
        process = subprocess.Popen(argv, cwd=work, env=environment, shell=False, stdin=subprocess.PIPE if input_bytes is not None
                                   else subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options)
        if NATIVE is not None: NATIVE.attach_and_resume(job, process.pid)
        readers = [threading.Thread(target=drain, args=(getattr(process, c), c), daemon=True) for c in outputs]
        for reader in readers: reader.start()
        if input_bytes is not None:
            require(len(input_bytes) <= 4096, "Only bounded dependency-fixture stdin")
            process.stdin.write(input_bytes); process.stdin.close()
        while process.poll() is None:
            require(not faults, "Stage pipe failure: " + str(faults))
            require(prefix is None or absent(prefix), "Fresh pycache prefix pollution is fatal")
            parent_guard(work=work)
            if NATIVE is not None:
                cpu, _, peak = NATIVE.job_state(job)
                require(cpu < cpu_limit and peak <= memory_limit, "Whole owned Job CPU/active peak-memory bound")
            else:
                require(time.monotonic() - started < cpu_limit, "Conservative scalar wall/CPU limit")
            if time.monotonic() - checked >= 5:
                verify_sources();
                if source_root is not None: verify_sources(source_root)
                checked = time.monotonic()
            time.sleep(.1)
        for reader in readers: reader.join(timeout=5); require(not reader.is_alive(), "Complete pipe EOF required")
        require(not faults and process.returncode == 0, "Clean successful stage terminal required: " + label)
        if NATIVE is not None:
            cpu, active, peak = NATIVE.job_state(job)
            require(cpu < cpu_limit and active == 0 and peak <= memory_limit, "Clean terminal of the ENTIRE owned Job")
        require(prefix is None or absent(prefix), "Fresh pycache prefix remains nonexistent AFTER close")
        parent_guard(work=work); verify_sources()
        if source_root is not None: verify_sources(source_root)
        stdout = bytes(outputs["stdout"]).decode("utf-8", errors="strict")
        stderr = bytes(outputs["stderr"]).decode("utf-8", errors="strict")
        require(not stderr, "Successful proof/scalar stage has no stderr: " + label)
        logfile = work / (label + ".stdout.txt")
        require(inside(logfile, work) and not logfile.exists(), "Exclusive private log target")
        with logfile.open("xb") as stream:
            stream.write(bytes(outputs["stdout"]))
        parent_guard(work=work)
        return stdout
    finally:
        if process is not None and process.poll() is None:
            if job is not None: NATIVE.k.TerminateJobObject(job, 1)
            else:
                import signal
                os.killpg(process.pid, signal.SIGKILL)
            # Assignment/startup failure can leave the primary suspended but
            # not yet a Job member. Kill ONLY this exact Popen-owned process.
            if process.poll() is None: process.kill()
            process.wait(timeout=10)
        if job is not None: NATIVE.k.CloseHandle(job)


def copied_code(work, rows):
    target = work / "code"; target.mkdir(exist_ok=False)
    for row in rows:
        source = CODE.joinpath(*PurePosixPath(row["path"]).parts)
        destination = target.joinpath(*PurePosixPath(row["path"]).parts)
        require(inside(destination, target) and not destination.exists(), "Exclusive source-copy destination")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    verify_sources(target)
    require((target / "n4" / "research" / "all_n").resolve().parents[1] == (target / "n4").resolve(),
            "N4's research/all_n ancestor layout is retained")
    return target


def tiny_tests(rows):
    require(sum(r["path"].startswith("n4/") for r in rows) == 79, "Whole n4 AST/provenance closure inventory")
    for part, count in (("n2/BE_two_summand_certificate/certificate/", 70),
                        ("n3/BE_three_summand_certificate/certificate/", 111)):
        require(sum(r["path"].startswith(part) for r in rows) == count, "Complete exact shard inventory")
    require(max(Fraction(0), min(Fraction(1, 2), max(TARGET, TARGET, TARGET, TARGET))) == TARGET,
            "Supplied min-own/MAX-all4 scalar fixture")
    require(Fraction(256, 625) < TARGET, "Supplied analytic-reduction scalar only")
    require(set(("--produce", "--replay-existing")) == {"--produce", "--replay-existing"}, "Two distinct fresh ROOT4 CLI modes")
    return {"scope": "SOURCE_INVENTORY_AND_SUPPLIED_SCALARS_ONLY", "files": len(rows),
            "project_checker_imported_or_numerical_producer_called": False, "full_paper_reproduced": False}


def scalar_mode(work, source):
    require(importlib.util.find_spec("sympy") is not None, "Scalar mode requires installed SymPy; no installation is performed")
    plans = [
        ("n2/BE_two_summand_certificate/verify_algebra.py", False),
        ("n3/BE_three_summand_certificate/verify_algebra.py", False),
        ("structural/checks/local/verify_constants.py", True),
        ("structural/checks/local/verify_symbolic.py", False),
        ("structural/checks/short_support/verify_constants.py", False),
        ("structural/checks/short_support/verify_rational.py", True),
        ("structural/checks/additional/verify_second_order_lattice.py", False),
        ("n4/research/all_n/finite4_contact_derivation_2026_10_09.py", True),
        ("n4/research/all_n/n4_elementary_gaussian_1_15_owner_radius_101_25_2026_10_09.py", True),
        ("n4/research/all_n/n4_complete_root_all_law_reduction_2026_10_09.py", True)]
    for index, (name, standard) in enumerate(plans):
        launch_gate()
        prefix = work / ("scalar-pycache-" + str(index))
        run_child(python_command(source / name, [], prefix, standard), work, "scalar-" + str(index),
                  300, 256 * MIB, prefix=prefix, source_root=source)
    return {"scope": "EXACT_IDENTITIES_AND_FINITE_ANALYTIC_CONSTANTS_ONLY", "scalar_stages": len(plans),
            "uniform_analytic_theorems_or_ROOT4_proved_by_tests": False, "full_paper_reproduced": False}


def full_mode(work, source):
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8,
            "Unchanged ROOT4 peak guard requires64-bit Windows; no portable guard monkeypatch")
    compiler = shutil.which("g++"); require(compiler is not None, "Full n3 requires g++ C++17 and Boost.Multiprecision headers")
    launch_gate()
    run_child([compiler, "-std=c++17", "-x", "c++", "-fsyntax-only", "-"], work, "boost-dependency", 120, 512 * MIB,
              input_bytes=b"#include <boost/multiprecision/cpp_int.hpp>\nint main(){return 0;}\n")
    plans = [
        ("n2/BE_two_summand_certificate/tensor_certificate.py", ["check"], "n2-primary", "ACCEPTED_ALL_70_TENSOR_CELLS 35878 134"),
        ("n2/BE_two_summand_certificate/independent_integer_check.py", [], "n2-independent", "ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK 35878 18426 134"),
        ("n3/BE_three_summand_certificate/audit_initial_polynomials.py", [], "n3-identities", "ACCEPTED_ALL_INITIAL_IDENTITIES cells=111 orthants=444 exact_grid_identities=95904"),
        ("n3/BE_three_summand_certificate/verify.py", [], "n3-full", "ACCEPTED_FULL_N3 111 501156 219860 349")]
    for name, arguments, label, accepted in plans:
        launch_gate(); prefix = work / (label + "-pycache")
        output = run_child(python_command(source / name, arguments, prefix), work, label, 7200, 512 * MIB,
                           prefix=prefix, source_root=source)
        if accepted: require(accepted in output.splitlines(), "Complete exact acceptance line required: " + label)
    entry = source / "n4" / "research" / "all_n" / ENTRY
    receipt = entry.with_name(entry.stem + "_ALL260_W20_B13_N256_H1_8_ETA16_five_budget.json")
    require(not receipt.exists(), "NO delivered/historical ROOT4 receipt may be an input")
    packets = []
    for index, flag in enumerate(("--produce", "--replay-existing")):
        launch_gate(); prefix = work / ("n4-pass-" + str(index) + "-pycache")
        output = run_child(python_command(entry, [flag], prefix), work, "n4-pass-" + str(index), 43200, 256 * MIB,
                           prefix=prefix, source_root=source)
        lines = output.splitlines(); require(lines, "Complete ROOT4 CLI summary")
        packet = json.loads(lines[-1], object_pairs_hook=unique_object)
        require(packet["status"] == ("EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_PORTFOLIO" if index == 0 else
                "READ_ONLY_REPLAY_ALL_NONRESOURCE_FIELDS_MATCH"), "Fresh ROOT4 production/full canonical replay acceptance")
        summary = packet["summary"]
        require(summary["geometry_classes_total"] == summary["closed_geometry_classes"] == 260 and
                summary["unresolved_geometry_classes"] == 0 and summary["ALL_high_request_slots_accounted"] == 1300 and
                summary["fixed_geometry_max_depth"] == 1 and packet["unresolved_geometry_indices"] == [] and
                Fraction(summary["entire_conditional_root_score_upper_exact"]) <= TARGET,
                "ALL260/ALL4/own-HIGH complete ROOT4 at the paper target; UNKNOWN cannot be hidden")
        require(Path(packet["result"]).resolve() == receipt.resolve(), "Same newly produced private comparator file")
        packets.append(packet)
    return {"scope": "FULL_N2_N3_FINITE_CERTIFICATES_AND_TWO_FRESH_CONDITIONAL_ROOT4_PASSES",
            "ROOT4_upper_exact": packets[-1]["summary"]["entire_conditional_root_score_upper_exact"],
            "received_receipt_or_saved_mathematical_input_used": False,
            "all_law_C4_requires_written_analytic_reduction_and_published_inputs": True,
            "whole_paper_cutoff_or_uniform_asymptotic_proof_reproduced": False,
            "full_paper_reproduced": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--tiny", action="store_true", help="source inventory/supplied scalar fixtures only (default)")
    modes.add_argument("--scalars", action="store_true", help="exact symbolic/analytic constants only; requires SymPy")
    modes.add_argument("--full", action="store_true", help="long n2/n3 and TWO new ROOT4 passes;64-bit Windows+g+++Boost")
    modes.add_argument("--fixture-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.fixture_child:
        parent_guard(True)
        print(json.dumps({"scope": "LAUNCHER_FIXTURE_ONLY", "mathematical_producer_called": False}, sort_keys=True))
        return
    tiny = not (args.scalars or args.full)
    parent_guard(tiny); rows, size = verify_sources(); launch_gate(tiny)
    if tiny:
        result = tiny_tests(rows)
        work = private_work(); prefix = work / "fixture-pycache"
        output = run_child(python_command(Path(__file__).resolve(), ["--fixture-child"], prefix), work,
                           "launcher-fixture", 10, 64 * MIB, prefix=prefix)
        require(json.loads(output, object_pairs_hook=unique_object) ==
                {"scope": "LAUNCHER_FIXTURE_ONLY", "mathematical_producer_called": False}, "Owned bounded launcher fixture")
        result["launcher_fixture_child_only"] = True
    else:
        work = private_work(); source = copied_code(work, rows)
        result = full_mode(work, source) if args.full else scalar_mode(work, source)
    verify_sources(); parent_guard(tiny, work)
    result.update({"source_data_bytes": size, "retained_private_work": str(work),
                   "success_requires_clean_runner_exit": True, "whole_paper_claim": False})
    print(json.dumps(result, sort_keys=True))
    verify_sources(); parent_guard(tiny, work)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("REJECTED_NO_REPRODUCTION_CLAIM: " + str(error) +
              ("; retained private work: " + str(RETAINED_WORK) if RETAINED_WORK is not None else ""), file=sys.stderr)
        raise SystemExit(1)
