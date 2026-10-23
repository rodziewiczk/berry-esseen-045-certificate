"""Small mocked kernel fixtures only; never execute a mathematical producer."""
from pathlib import Path
import os
import signal
import subprocess
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from . import linux_cgroup as linux


class CgroupFixtures(unittest.TestCase):
    def fixture(self, directory):
        root, proc = directory/'cgroup', directory/'proc'
        root.mkdir()
        (proc/'self').mkdir(parents=True)
        (proc/'self/cgroup').write_text('0::/\n')
        (proc/'self/mountinfo').write_text('29 1 0:26 / '+str(root)+' ro,nosuid,nodev,noexec - cgroup2 cgroup rw\n')
        (proc/'meminfo').write_text('MemTotal: 8388608 kB\nMemAvailable: 2097152 kB\n')
        values = {'cgroup.type': 'domain', 'memory.max': str(linux.MEMORY), 'memory.swap.max': '0',
                  'memory.current': str(48*linux.MIB), 'memory.events': 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0',
                  'cpu.max': '100000 100000', 'cpu.stat': 'usage_usec 1000\nuser_usec 700\nsystem_usec 300',
                  'pids.max': '128', 'pids.current': '2', 'pids.events': 'max 0',
                  'cgroup.procs': '1\n'+str(os.getpid())}
        for name, value in values.items(): (root/name).write_text(value+'\n')
        return root, proc, linux.CgroupGuard(root, proc, clock=lambda: 100)

    def test_exact_kernel_limits_and_real_accounting_fixture(self):
        with tempfile.TemporaryDirectory() as name:
            _, _, guard = self.fixture(Path(name))
            result = guard.sample(idle=True)
            self.assertEqual(result['cpu_usage_usec'], 1000)
            self.assertEqual(guard.receipt()['memory_max_bytes'], 512*1024**2)

    def test_unlimited_weaker_or_per_process_limits_decline(self):
        mutations = [('memory.max', 'max'), ('memory.max', str(1024*linux.MIB)),
                     ('memory.max', str(256*linux.MIB)), ('memory.swap.max', '1'),
                     ('cpu.max', 'max 100000'), ('cpu.max', '200000 100000'),
                     ('pids.max', 'max'), ('pids.max', '129'), ('pids.max', '0')]
        for field, value in mutations:
            with self.subTest(field=field,value=value), tempfile.TemporaryDirectory() as name:
                root, _, guard = self.fixture(Path(name))
                (root/field).write_text(value+'\n')
                with self.assertRaises(ValueError): guard.sample()

    def test_oom_oomkill_process_exhaustion_or_over_budget_decline(self):
        mutations = [('memory.events', 'oom 1\noom_kill 0'),
                     ('memory.events', 'oom 0\noom_kill 1'),
                     ('memory.events', 'oom 0\noom_kill 0\noom_group_kill 1'),
                     ('pids.events', 'max 1'), ('pids.current', '129'),
                     ('memory.current', str(linux.MEMORY+1)),
                     ('cpu.stat', 'usage_usec 7200000001\nuser_usec 1\nsystem_usec 1')]
        for field, value in mutations:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as name:
                root, _, guard = self.fixture(Path(name))
                (root/field).write_text(value+'\n')
                with self.assertRaises(ValueError): guard.sample()

    def test_cgroup_mount_namespace_and_source_counters_cannot_be_faked_by_old_receipt(self):
        with tempfile.TemporaryDirectory() as name:
            root, proc, guard = self.fixture(Path(name))
            guard.sample()
            (root/'cpu.stat').write_text('usage_usec 999\nuser_usec 700\nsystem_usec 299\n')
            with self.assertRaisesRegex(ValueError, 'reset/migration'): guard.sample()
            (root/'cpu.stat').write_text('usage_usec 1001\nuser_usec 700\nsystem_usec 301\n')
            (proc/'self/cgroup').write_text('0::/unbounded-parent\n')
            with self.assertRaisesRegex(ValueError, 'Private unified'): guard.sample()
            (proc/'self/cgroup').write_text('0::/\n')
            (proc/'self/mountinfo').write_text('29 1 0:26 / '+str(root)+' rw - tmpfs cgroup rw\n')
            with self.assertRaisesRegex(ValueError, 'actual cgroup-v2'): guard.sample()

    def test_idle_census_requires_only_container_init_and_controller(self):
        with tempfile.TemporaryDirectory() as name:
            root, _, guard = self.fixture(Path(name))
            (root/'cgroup.procs').write_text('1\n'+str(os.getpid())+'\n424242\n')
            guard.sample()
            with self.assertRaisesRegex(ValueError, 'Only Docker init'): guard.sample(idle=True)

    def test_two_launch_readings_five_seconds_apart_and_host_reserve(self):
        with tempfile.TemporaryDirectory() as name:
            _, proc, guard = self.fixture(Path(name))
            sleep = Mock()
            guard.launch_gate(sleep=sleep)
            sleep.assert_called_once_with(5)
            self.assertEqual(guard.samples, 2)
            (proc/'meminfo').write_text('MemAvailable: 1500000 kB\n')
            guard.sample()
            with self.assertRaisesRegex(ValueError, 'host free-RAM'): guard.launch_gate(sleep=sleep)
            (proc/'meminfo').write_text('MemAvailable: 500000 kB\n')
            with self.assertRaisesRegex(ValueError, 'host free-RAM'): guard.sample()

    def test_wall_clock_and_diagnostic_quota_fail_closed(self):
        with tempfile.TemporaryDirectory() as name:
            root, proc, guard = self.fixture(Path(name))
            guard.clock = lambda: 100+linux.WALL_SECONDS+1
            with self.assertRaisesRegex(ValueError, 'wall-clock'): guard.sample()
            guard.clock = lambda: 100
            inventory = Mock(entries=(('native.stdout.txt','file',1,2,0,linux.OUTPUT_LIMIT+1,0,0),))
            with patch.object(linux, 'stable_inventory', return_value=inventory), patch.object(
                    linux.shutil, 'disk_usage', return_value=Mock(free=linux.DISK_FLOOR)):
                with self.assertRaisesRegex(ValueError, 'diagnostics'): guard.work_guard(root)

    def test_process_group_is_always_terminated_even_after_success(self):
        process = Mock(pid=1234)
        with patch.object(linux.os, 'killpg', create=True) as kill, patch.object(
                linux.signal, 'SIGKILL', 9, create=True):
            linux.cleanup_group(process)
        self.assertEqual(kill.call_args_list[0].args, (1234,signal.SIGTERM))
        self.assertEqual(kill.call_args_list[1].args, (1234,9))
        self.assertEqual(process.wait.call_count, 2)

    def test_guard_failure_cleans_whole_group_before_exception_escapes(self):
        with tempfile.TemporaryDirectory() as name:
            guard = Mock()
            guard.work_guard.side_effect = [None, ValueError('host RAM unavailable')]
            process = Mock(pid=1234)
            process.poll.return_value = None
            with patch.object(linux.subprocess, 'Popen', return_value=process) as start, patch.object(
                    linux, 'cleanup_group') as cleanup:
                with self.assertRaisesRegex(ValueError, 'host RAM'):
                    linux.run_owned(['not-executed-fixture'],Path(name),guard,{})
                self.assertTrue(start.call_args.kwargs['start_new_session'])
                self.assertTrue(start.call_args.kwargs['close_fds'])
                cleanup.assert_called_once_with(process)

    def test_duplicate_or_noninteger_kernel_counters_decline(self):
        for value in ('oom 0\noom 0', 'oom True', 'oom -1', 'oom 00'):
            with self.subTest(value=value), self.assertRaises(ValueError): linux.counters(value)

    def fake_native_guard(self, pids=(424242,)):
        guard = SimpleNamespace(proc=Path('mock-proc'), baseline={1,os.getpid()}, sample=Mock())
        states, processes = {pid:'R' for pid in pids}, {}
        guard.text = lambda name: '\n'.join(map(str, sorted(guard.baseline|set(states))))
        def pin(proc,pid):
            self.assertNotIn(pid,guard.baseline)
            def send(signum):
                states[pid] = 'T' if signum == 19 else 'R'
            item = SimpleNamespace(pid=pid,birth=pid+7,state=lambda:states[pid],send=Mock(side_effect=send),close=Mock())
            processes[pid] = item
            return item
        return guard,states,processes,pin

    def test_all_live_numeric_pids_stopped_and_finally_resumed_not_init_or_controller(self):
        guard,states,processes,pin = self.fake_native_guard((424242,424243))
        with patch.object(linux,'PinnedProcess',side_effect=pin) as created, patch.object(
                linux.signal,'SIGSTOP',19,create=True), patch.object(linux.signal,'SIGCONT',18,create=True):
            with linux.quiesce_numerical(guard):
                self.assertEqual(set(states.values()),{'T'})
            self.assertEqual(set(states.values()),{'R'})
            self.assertEqual(created.call_count,2)
            for item in processes.values():
                self.assertEqual(item.send.call_args_list[-1].args,(18,))
                item.close.assert_called_once_with()

    def test_snapshot_failure_still_continues_every_stopped_process(self):
        guard,states,processes,pin = self.fake_native_guard((424242,424243))
        with patch.object(linux,'PinnedProcess',side_effect=pin), patch.object(
                linux.signal,'SIGSTOP',19,create=True), patch.object(linux.signal,'SIGCONT',18,create=True):
            with self.assertRaisesRegex(ValueError,'full inventory failed'):
                with linux.quiesce_numerical(guard):
                    raise ValueError('full inventory failed')
            self.assertEqual(set(states.values()),{'R'})
            self.assertTrue(all(item.send.call_args_list[-1].args == (18,) for item in processes.values()))

    def test_unstoppable_writer_is_bounded_and_no_inventory_yielded(self):
        guard,states,processes,pin = self.fake_native_guard()
        def uncooperative(proc,pid):
            item = pin(proc,pid)
            item.send.side_effect = lambda signum: None
            return item
        with patch.object(linux,'PinnedProcess',side_effect=uncooperative), patch.object(
                linux.signal,'SIGSTOP',19,create=True), patch.object(linux.signal,'SIGCONT',18,create=True), patch.object(
                linux.time,'sleep'):
            with self.assertRaisesRegex(ValueError,'bounded complete stopped'):
                with linux.quiesce_numerical(guard):
                    self.fail('A running writer must never yield a successful snapshot')
            self.assertEqual(processes[424242].send.call_args_list[-1].args,(18,))

    def test_new_child_during_freeze_is_also_stopped_before_snapshot(self):
        guard,states,processes,pin = self.fake_native_guard()
        def forking(proc,pid):
            item = pin(proc,pid)
            original = item.send.side_effect
            def send(signum):
                original(signum)
                if pid == 424242 and signum == 19:
                    states.setdefault(424243,'R')
            item.send.side_effect = send
            return item
        with patch.object(linux,'PinnedProcess',side_effect=forking), patch.object(
                linux.signal,'SIGSTOP',19,create=True), patch.object(linux.signal,'SIGCONT',18,create=True):
            with linux.quiesce_numerical(guard):
                self.assertEqual(states,{424242:'T',424243:'T'})
        self.assertEqual(states,{424242:'R',424243:'R'})

    def test_small_concurrent_writer_is_quiet_for_the_complete_original_inventory(self):
        guard,states,processes,pin = self.fake_native_guard()
        running,done,ready = threading.Event(),threading.Event(),threading.Event()
        running.set()
        with tempfile.TemporaryDirectory() as name:
            path=Path(name)/'native-progress.txt'
            def writer():
                value=0
                while not done.is_set():
                    if running.wait(0.01):
                        path.write_text(str(value));value+=1;ready.set()
                    time.sleep(0.001)
            thread=threading.Thread(target=writer)
            thread.start()
            self.assertTrue(ready.wait(2))
            def scheduled(proc,pid):
                item=pin(proc,pid)
                original=item.send.side_effect
                def send(signum):
                    original(signum)
                    running.clear() if signum == 19 else running.set()
                item.send.side_effect=send
                return item
            try:
                with patch.object(linux,'PinnedProcess',side_effect=scheduled), patch.object(
                        linux.signal,'SIGSTOP',19,create=True), patch.object(linux.signal,'SIGCONT',18,create=True):
                    with linux.quiesce_numerical(guard):
                        first=linux.stable_inventory(Path(name),linux.WORK_LIMIT)
                        time.sleep(0.01)
                        self.assertEqual(first,linux.stable_inventory(Path(name),linux.WORK_LIMIT))
                    self.assertTrue(running.is_set())
            finally:
                done.set();running.set();thread.join(timeout=2)
            self.assertFalse(thread.is_alive())

    def test_process_birth_and_pidfd_prevent_signalling_reused_pids(self):
        with tempfile.TemporaryDirectory() as name:
            proc=Path(name)
            (proc/'424242').mkdir()
            path=proc/'424242/stat'
            def statline(birth):
                return '424242 (native fixture with )) R '+' '.join(['0']*18+[str(birth)]+['0']*4)
            path.write_text(statline(101))
            self.assertEqual(linux.process_identity(proc,424242),(101,'R'))
            with patch.object(linux.os,'pidfd_open',return_value=77,create=True) as opened, patch.object(
                    linux.signal,'pidfd_send_signal',create=True) as sent, patch.object(linux.os,'close') as closed:
                item=linux.PinnedProcess(proc,424242)
                item.send(19)
                sent.assert_called_once_with(77,19,None,0)
                path.write_text(statline(102))
                with self.assertRaisesRegex(ValueError,'identity unchanged'): item.state()
                item.close()
                opened.assert_called_once_with(424242,0)
                closed.assert_called_once_with(77)

    def test_pid_zero_is_never_signalled(self):
        guard,_,_,pin=self.fake_native_guard((0,))
        with patch.object(linux,'PinnedProcess',side_effect=pin) as created:
            with self.assertRaisesRegex(ValueError,'never PID0'):
                with linux.quiesce_numerical(guard): self.fail('must reject PID0')
            created.assert_not_called()


if __name__ == '__main__':
    unittest.main()
