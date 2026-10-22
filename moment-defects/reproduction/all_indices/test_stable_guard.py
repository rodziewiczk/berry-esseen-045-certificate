"""Control-plane tests, not numerical proof acceptances."""
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

from . import stable_guard as guard


class StableGuardTests(unittest.TestCase):
    def test_stable_complete_inventory(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "a").write_bytes(b"abc")
            (root / "sub").mkdir()
            (root / "sub" / "b").write_bytes(b"12345")
            result = guard.stable_inventory(root, 8)
            self.assertEqual(result.total_bytes, 8)
            self.assertEqual(sum(row[1] == "file" for row in result.entries), 2)

    def test_atomic_rename_restarts_entire_inventory(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / "first").write_bytes(b"123")
            incomplete = root / "z.incomplete"
            incomplete.write_bytes(b"4567")
            original = guard._file_stat
            renamed = False
            visits = []

            def racing_file(path, expected, resolved_root):
                nonlocal renamed
                visits.append(path.name)
                if path.name == "z.incomplete" and not renamed:
                    renamed = True
                    incomplete.rename(root / "z.final")
                return original(path, expected, resolved_root)

            with patch.object(guard, "_file_stat", side_effect=racing_file):
                result = guard.stable_inventory(root, 7)
            self.assertTrue(renamed)
            self.assertEqual(result.total_bytes, 7)
            self.assertGreaterEqual(visits.count("first"), 3)
            self.assertIn("z.final", [row[0] for row in result.entries])
            self.assertNotIn("z.incomplete", [row[0] for row in result.entries])

    def test_quota_is_not_relaxed(self):
        with tempfile.TemporaryDirectory() as name:
            (Path(name) / "too-big").write_bytes(b"12345")
            with self.assertRaisesRegex(guard.StableScanError, "quota"):
                guard.stable_inventory(Path(name), 4)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            target = root / "target"
            target.write_bytes(b"x")
            try:
                (root / "link").symlink_to(target)
            except OSError as exc:
                self.skipTest("Host does not permit unprivileged symlinks: " + str(exc))
            with self.assertRaisesRegex(guard.StableScanError, "symlink"):
                guard.stable_inventory(root, 100)

    def test_windows_reparse_attribute_rejected(self):
        value = types.SimpleNamespace(st_mode=0o100644, st_file_attributes=0x400)
        with self.assertRaisesRegex(guard.StableScanError, "reparse"):
            guard._safe_stat(value)

    def test_symlink_mode_rejected_without_host_privileges(self):
        value = types.SimpleNamespace(st_mode=0o120777, st_file_attributes=0)
        with self.assertRaisesRegex(guard.StableScanError, "symlink"):
            guard._safe_stat(value)

    def test_vanished_scan_invalidates_previous_complete_snapshot(self):
        snapshot = guard.Inventory((("a", "file"),), 1)
        with patch.object(guard, "_scan_once",
                          side_effect=[snapshot, guard._ChangedDuringScan(), snapshot]):
            with self.assertRaisesRegex(guard.StableScanError, "No two identical"):
                guard.stable_inventory(Path("unused"), 10, max_scans=3)

    def test_persistent_identity_changes_fail_closed(self):
        snapshots = [guard.Inventory(((str(index), "file"),), 1) for index in range(6)]
        with patch.object(guard, "_scan_once", side_effect=snapshots) as scan:
            with self.assertRaisesRegex(guard.StableScanError, "No two identical"):
                guard.stable_inventory(Path("unused"), 10, max_scans=6)
        self.assertEqual(scan.call_count, 6)

    def test_persistently_vanishing_files_fail_closed(self):
        with patch.object(guard, "_scan_once", side_effect=guard._ChangedDuringScan):
            with self.assertRaisesRegex(guard.StableScanError, "No two identical"):
                guard.stable_inventory(Path("unused"), 10, max_scans=4)

    def test_installer_retains_original_resource_checks(self):
        calls = []
        def original(tiny=False, work=None):
            calls.append((tiny, work))
        def require(condition, message):
            if not condition:
                raise RuntimeError(message)
        runner = types.SimpleNamespace(parent_guard=original, require=require,
                                       DISK_FLOOR=0, WORK_LIMIT=100)
        guard.install(runner)
        with tempfile.TemporaryDirectory() as name:
            runner.parent_guard(tiny=True, work=Path(name))
        self.assertEqual(calls, [(True, None), (True, None)])
        with self.assertRaisesRegex(guard.StableScanError, "once"):
            guard.install(runner)


if __name__ == "__main__":
    unittest.main()
