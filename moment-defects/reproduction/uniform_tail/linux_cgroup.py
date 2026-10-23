"""Fail-closed observer for one isolated Docker cgroup-v2 numerical job.

No per-process rlimit is represented as an aggregate guarantee. The kernel
cgroup contains the controller, Docker init and every native descendant.
Numerical entry is permitted only as Docker init's direct child; exiting the
controller also ends the container's init and its remaining PID namespace.
"""
from __future__ import annotations

from contextlib import contextmanager
import errno
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import time

from .count_catalog import need
from ..all_indices.stable_guard import stable_inventory

MIB = 1024**2
MEMORY = 512*MIB
WORK_LIMIT = 256*MIB
OUTPUT_LIMIT = 16*MIB
DISK_FLOOR = 4*1024**3
HOST_FLOOR = 1024*MIB
LAUNCH_FLOOR = 1536*MIB
CPU_USEC = 7200*1000000
WALL_SECONDS = 7800


def bounded_text(path, maximum=65536):
    """Read small kernel pseudo-files, never a supplied native result."""
    path = Path(path)
    value = path.lstat()
    need(stat.S_ISREG(value.st_mode) and not path.is_symlink(), "Regular kernel control file: " + str(path))
    with path.open('rb') as stream:
        raw = stream.read(maximum+1)
    need(len(raw) <= maximum, "Bounded kernel control read")
    return raw.decode('ascii')


def natural(text):
    need(re.fullmatch(r'0|[1-9][0-9]*', text) is not None, "Literal nonnegative kernel integer")
    return int(text)


def counters(text):
    result = {}
    for line in text.splitlines():
        fields = line.split()
        need(len(fields) == 2 and fields[0] not in result, "Unique kernel counter row")
        result[fields[0]] = natural(fields[1])
    return result


def host_available(meminfo=Path('/proc/meminfo')):
    rows = {}
    for line in bounded_text(meminfo).splitlines():
        name, separator, value = line.partition(':')
        need(separator and name not in rows, "Unique proc meminfo field")
        rows[name] = value.strip()
    fields = rows.get('MemAvailable', '').split()
    need(len(fields) == 2 and fields[1] == 'kB', "Actual host MemAvailable in kB")
    return natural(fields[0])*1024


def require_docker_init(proc=Path('/proc'), marker=Path('/.dockerenv')):
    need(sys.platform == 'linux' and os.name == 'posix', "Linux Docker execution only")
    need(marker.is_file() and not marker.is_symlink(), "Docker container marker required")
    need(os.getppid() == 1 and bounded_text(proc/'1/comm').strip() in ('docker-init', 'tini'),
         "Controller must be the direct main child of Docker --init PID1")


def process_identity(proc, pid):
    """Linux PID plus immutable birth tick; comm may itself contain spaces or ')'."""
    raw = bounded_text(Path(proc)/str(pid)/'stat')
    opening = raw.find(' (')
    closing = raw.rfind(')')
    need(opening > 0 and closing > opening and natural(raw[:opening]) == pid,
         "Exact native /proc PID identity")
    fields = raw[closing+1:].split()
    need(len(fields) >= 20 and fields[0] in ('R','S','D','Z','T','t','X','x','K','W','P','I'),
         "Actual Linux process state and birth counter")
    return natural(fields[19]), fields[0]


class PinnedProcess:
    """Signal the same observed process; use a Linux pidfd when supported."""
    def __init__(self, proc, pid):
        self.proc, self.pid, self.fd = Path(proc), pid, None
        self.birth, _ = process_identity(proc, pid)
        if hasattr(os, 'pidfd_open') and hasattr(signal, 'pidfd_send_signal'):
            try:
                self.fd = os.pidfd_open(pid, 0)
            except OSError as exc:
                if exc.errno not in (errno.ENOSYS, errno.EINVAL, errno.EPERM):
                    raise
        try:
            need(process_identity(proc, pid)[0] == self.birth, "PID birth unchanged while pinning native process")
        except BaseException:
            self.close()
            raise

    def send(self, signum):
        if self.fd is not None:
            signal.pidfd_send_signal(self.fd, signum, None, 0)
        else:
            need(process_identity(self.proc, self.pid)[0] == self.birth,
                 "Never signal a reused native PID")
            os.kill(self.pid, signum)

    def state(self):
        birth, state = process_identity(self.proc, self.pid)
        need(birth == self.birth, "Native PID identity unchanged during quiescence")
        return state

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


@contextmanager
def quiesce_numerical(guard):
    """Scheduling-only bounded stop/scan/resume, never a partial inventory.

The private container cgroup guarantees that every PID except init and the
controller is part of this numerical job. Native writers are paused until
two complete ordinary stable_inventory scans agree. No source is changed.
"""
    pinned = {}
    stopped = set()
    previous = None
    deadline = time.monotonic()+5

    def targets():
        rows = [natural(line) for line in guard.text('cgroup.procs').splitlines()]
        need(len(rows) == len(set(rows)) and len(rows) <= 128, "Bounded private native PID census")
        result = set(rows)-guard.baseline
        need(all(pid > 1 for pid in result), "Only visible individual native PIDs; never PID0 or init")
        return result

    try:
        # No child is running during initial source preparation. Avoid needless
        # signals in that case, but still reject a child appearing during scan.
        native = targets()
        if not native:
            yield
            need(not targets(), "No numerical process appeared during an idle source snapshot")
            return
        for attempt in range(64):
            guard.sample()
            need(time.monotonic() <= deadline, "Native writer quiescence within five seconds")
            native = targets()
            for pid in sorted(native):
                try:
                    if pid not in pinned:
                        pinned[pid] = PinnedProcess(guard.proc, pid)
                    item = pinned[pid]
                    if item.state() != 'Z':
                        # Record before attempting STOP: even an asynchronous
                        # stop or an exception must be paired with finally CONT.
                        stopped.add(pid)
                        item.send(signal.SIGSTOP)
                except (FileNotFoundError, ProcessLookupError):
                    pass
            current = []
            quiet = True
            for pid in sorted(targets()):
                try:
                    item = pinned.get(pid)
                    if item is None:
                        quiet = False
                        continue
                    state = item.state()
                    quiet = quiet and state in ('T','t','Z')
                    if state != 'Z':
                        current.append((pid,item.birth))
                except (FileNotFoundError, ProcessLookupError):
                    quiet = False
            signature = tuple(current)
            if quiet and signature == previous:
                guard.sample()
                yield
                need(time.monotonic() <= deadline, "Complete quiescent private inventory within five seconds")
                after = []
                for pid in sorted(targets()):
                    item = pinned.get(pid)
                    state = item.state() if item is not None else process_identity(guard.proc,pid)[1]
                    if state == 'Z':
                        continue  # init may reap a non-writing zombie at any instant.
                    need(item is not None and state in ('T','t'),
                         "All numerical writers remain pinned and stopped throughout the full snapshot")
                    after.append((pid,item.birth))
                need(tuple(after) == signature, "Complete quiescent numerical PID census unchanged across snapshot")
                guard.sample()
                return
            previous = signature if quiet else None
            time.sleep(0.01)
        raise ValueError("No bounded complete stopped native process census; no snapshot accepted")
    finally:
        failures = []
        for pid in sorted(stopped):
            try:
                pinned[pid].send(signal.SIGCONT)
            except (FileNotFoundError, ProcessLookupError):
                pass
            except Exception as exc:
                failures.append(str(exc))
        for item in pinned.values():
            try:
                item.close()
            except Exception as exc:
                failures.append(str(exc))
        need(not failures, "All stopped live native processes resumed and handles closed: "+'; '.join(failures))


class CgroupGuard:
    def __init__(self, root=Path('/sys/fs/cgroup'), proc=Path('/proc'), clock=time.monotonic):
        self.root, self.proc, self.clock = Path(root), Path(proc), clock
        self.started = clock()
        value = self.root.lstat()
        need(stat.S_ISDIR(value.st_mode) and not self.root.is_symlink(), "Actual cgroup-v2 mount directory")
        self.identity = value.st_dev, value.st_ino
        self.previous = None
        self.samples = 0
        self.maximum_memory_current = 0
        self.baseline = {1, os.getpid()}

    def text(self, name):
        return bounded_text(self.root/name).strip()

    def validate_mount(self):
        need(bounded_text(self.proc/'self/cgroup').strip() == '0::/',
             "Private unified cgroup namespace, no inherited non-root membership")
        rows = [line.split() for line in bounded_text(self.proc/'self/mountinfo', 256*1024).splitlines()]
        matches = [row for row in rows if len(row) >= 10 and row[4] == str(self.root)
                   and '-' in row and row[row.index('-')+1] == 'cgroup2']
        need(len(matches) == 1 and matches[0][3] == '/', "Root-mounted actual cgroup-v2 filesystem")
        value = self.root.lstat()
        need((value.st_dev, value.st_ino) == self.identity and not self.root.is_symlink(),
             "Cgroup mount identity unchanged")
        need(self.text('cgroup.type') == 'domain', "One aggregate cgroup domain")

    def sample(self, host_floor=HOST_FLOOR, idle=False):
        self.validate_mount()
        need(natural(self.text('memory.max')) == MEMORY, "Entire-container memory.max must equal512MiB")
        need(natural(self.text('memory.swap.max')) == 0, "Entire-container swap disabled")
        cpu = self.text('cpu.max').split()
        need(len(cpu) == 2 and 0 < natural(cpu[0]) <= natural(cpu[1])
             and 1000 <= natural(cpu[1]) <= 1000000, "Hard aggregate CPU bandwidth at most one CPU")
        pids_max = natural(self.text('pids.max'))
        need(0 < pids_max <= 128, "Hard aggregate process/thread bound at most128")
        pids = natural(self.text('pids.current'))
        need(pids <= pids_max, "Observed cgroup process/thread count within kernel bound")
        memory = natural(self.text('memory.current'))
        need(memory <= MEMORY, "Observed whole-container charged memory within512MiB")
        events = counters(self.text('memory.events'))
        need(all(name in events and events[name] == 0 for name in ('oom', 'oom_kill'))
             and events.get('oom_group_kill', 0) == 0, "No cgroup OOM or OOM kill during this container")
        pids_events = counters(self.text('pids.events'))
        need(pids_events.get('max') == 0, "No cgroup process-limit exhaustion")
        cpu_stat = counters(self.text('cpu.stat'))
        need(all(name in cpu_stat for name in ('usage_usec', 'user_usec', 'system_usec')),
             "Actual aggregate cgroup CPU accounting")
        need(cpu_stat['usage_usec'] <= CPU_USEC, "Aggregate container CPU budget7200 seconds")
        current = {'cpu_usage_usec': cpu_stat['usage_usec'], 'oom': events['oom'],
                   'oom_kill': events['oom_kill'], 'pids_limit_events': pids_events['max']}
        if self.previous is not None:
            need(all(current[name] >= value for name, value in self.previous.items()),
                 "No reset/migration of aggregate cgroup counters")
        self.previous = current
        self.maximum_memory_current = max(self.maximum_memory_current, memory)
        self.samples += 1
        need(self.clock()-self.started <= WALL_SECONDS, "Container wall-clock budget7800 seconds")
        available = host_available(self.proc/'meminfo')
        need(available >= host_floor, "Actual host free-RAM reserve")
        processes = [natural(line) for line in self.text('cgroup.procs').splitlines()]
        need(len(processes) == len(set(processes)) and len(processes) <= 128,
             "Bounded unique PID-namespace cgroup process census")
        if idle:
            need(set(processes) == self.baseline, "Only Docker init and this controller before/after native execution")
        return {'cpu_usage_usec': current['cpu_usage_usec'], 'memory_current_bytes': memory,
                'pids_current': pids, 'host_MemAvailable_bytes': available,
                'memory_events': events, 'pids_events': pids_events}

    def launch_gate(self, sleep=time.sleep):
        self.sample(LAUNCH_FLOOR, idle=True)
        sleep(5)
        self.sample(LAUNCH_FLOOR, idle=True)

    def work_guard(self, work):
        self.sample()
        need(shutil.disk_usage(work).free >= DISK_FLOOR, "Private scratch disk reserve4GiB")
        with quiesce_numerical(self):
            inventory = stable_inventory(work, WORK_LIMIT)
        diagnostic = sum(entry[5] for entry in inventory.entries
                         if entry[1] == 'file' and entry[0].endswith(('.stdout.txt', '.stderr.txt')))
        need(diagnostic <= OUTPUT_LIMIT, "Entire private native stdout/stderr diagnostics within16MiB")
        self.sample()
        return inventory

    def receipt(self):
        return {'kind': 'LINUX_DOCKER_CGROUP_V2_AGGREGATE', 'memory_max_bytes': MEMORY,
                'memory_swap_max_bytes': 0, 'cpu_total_limit_seconds': 7200,
                'wall_limit_seconds': WALL_SECONDS, 'pids_max_upper_bound': 128,
                'host_ram_reserve_bytes': HOST_FLOOR, 'launch_host_ram_bytes': LAUNCH_FLOOR,
                'launch_interval_seconds': 5, 'private_file_limit_bytes': WORK_LIMIT,
                'disk_free_reserve_bytes': DISK_FLOOR, 'diagnostic_limit_bytes': OUTPUT_LIMIT,
                'samples': self.samples, 'last_counters': self.previous,
                'maximum_observed_memory_current_bytes': self.maximum_memory_current}


def cleanup_group(process):
    """Always terminate the entire owned native session, even after rc0."""
    for signum in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, signum)
        except ProcessLookupError:
            pass
        if signum == signal.SIGTERM:
            try:
                process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                pass
    process.wait(timeout=5)


def run_owned(command, work, guard, env):
    """Observe one real command; no caller-supplied PASS substitutes for it."""
    process = None
    label = 'be49-original-full-suite'
    stdout, stderr = work/(label+'.stdout.txt'), work/(label+'.stderr.txt')
    guard.work_guard(work)
    try:
        with stdout.open('xb') as output, stderr.open('xb') as error:
            process = subprocess.Popen(command, cwd=work, env=env, stdin=subprocess.DEVNULL,
                                       stdout=output, stderr=error, start_new_session=True,
                                       close_fds=True)
            while process.poll() is None:
                guard.work_guard(work)
                time.sleep(0.5)
            need(type(process.returncode) is int and process.returncode == 0,
                 "Observed successful original FULL suite subprocess")
    finally:
        if process is not None:
            cleanup_group(process)
    # Docker init asynchronously reaps any orphaned grandchildren. A live or
    # unreaped extra PID never qualifies as a successful isolated full run.
    for attempt in range(20):
        try:
            final = guard.sample(idle=True)
            break
        except ValueError:
            if attempt == 19:
                raise
            time.sleep(0.1)
    guard.work_guard(work)
    need(stderr.stat().st_size == 0, "No wrapper stderr on a successful full run")
    return {'execution_observed_by_this_controller': True, 'returncode': process.returncode,
            'command': command, 'cwd': str(work), 'final_cgroup_sample': final}
