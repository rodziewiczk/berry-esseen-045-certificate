from types import SimpleNamespace
import unittest
from unittest.mock import patch
from .archive_guard import install,HostRAMUnavailable,MIB


def require(value,message):
    if not value:raise ValueError(message)


class ArchiveCoordinatorGuardTests(unittest.TestCase):
    def setUp(self):
        self.runner = SimpleNamespace(require=require,WORK_LIMIT=256*MIB,DISK_FLOOR=4*1024**3,
            LAUNCH_FLOOR=1536*MIB,HOST_FLOOR=768*MIB,own_peak=lambda:128*MIB,available_ram=lambda:2048*MIB)

    def test_explicit_metadata_peak64_to256_is_allowed_not_hidden(self):
        install(self.runner)
        for peak in (64*MIB,65*MIB,128*MIB,256*MIB):
            self.runner.own_peak = lambda:peak
            self.runner.parent_guard()
        self.assertEqual(self.runner.HOST_FLOOR,1024*MIB)

    def test_above256_and_host_below1024_fail_closed(self):
        install(self.runner)
        self.runner.own_peak = lambda:256*MIB+1
        with self.assertRaisesRegex(ValueError,'256MiB'):self.runner.parent_guard()
        self.runner.own_peak = lambda:128*MIB
        self.runner.available_ram = lambda:1024*MIB-1
        with self.assertRaises(HostRAMUnavailable):self.runner.parent_guard()

    def test_original_work_disk_and_tiny_cpu_checks_remain(self):
        install(self.runner)
        with patch('reproduction.continuations.archive_guard.shutil.disk_usage',return_value=SimpleNamespace(free=5*1024**3)), \
             patch('reproduction.continuations.archive_guard.stable_inventory') as scan:
            self.runner.parent_guard(work='private-test-root')
            scan.assert_called_once_with('private-test-root',256*MIB)
        with patch('reproduction.continuations.archive_guard.shutil.disk_usage',return_value=SimpleNamespace(free=3*1024**3)):
            with self.assertRaisesRegex(ValueError,'disk'):self.runner.parent_guard(work='private-test-root')
        with patch('reproduction.continuations.archive_guard.time.process_time',return_value=11):
            with self.assertRaisesRegex(ValueError,'CPU10s'):self.runner.parent_guard(tiny=True)

    def test_weakened_original_limits_or_double_install_are_rejected(self):
        self.runner.LAUNCH_FLOOR = 1024*MIB
        with self.assertRaises(ValueError):install(self.runner)
        self.runner.LAUNCH_FLOOR = 1536*MIB;install(self.runner)
        with self.assertRaises(ValueError):install(self.runner)


if __name__ == '__main__':unittest.main()
