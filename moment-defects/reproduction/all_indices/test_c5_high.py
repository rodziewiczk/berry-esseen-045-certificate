"""Lightweight native-epoch plumbing tests, not mathematical acceptances."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

from . import c5_high_one as high


class HighEpochTests(unittest.TestCase):
    def fixture(self, root):
        prefix = high.HIGH_ROOT + "high5_v1/"
        directory = root / prefix
        directory.mkdir(parents=True)
        pins = {}
        for name in ("bound.py", "accept.py", "kernel.py", "universal.py", "PROOF.txt"):
            path = directory / name
            path.write_bytes(("frozen fixture " + name).encode())
            pins[prefix + name] = high.digest(path)
        manifest = directory / "MANIFEST.json"
        manifest.write_text(json.dumps({"files_sha256": dict(pins)}))
        pins[prefix + "MANIFEST.json"] = high.digest(manifest)
        return prefix, directory, pins

    def test_collects_manifest_closure_and_native_acceptance_source(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            _, _, pins = self.fixture(root)
            self.assertEqual(high.collect_sources(root, pins, "high5_v1"), pins)

    def test_altered_source_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            _, directory, pins = self.fixture(root)
            (directory / "kernel.py").write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "Exact native HIGH source"):
                high.collect_sources(root, pins, "high5_v1")

    def test_manifest_cannot_introduce_unbound_source(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            prefix, directory, pins = self.fixture(root)
            manifest = directory / "MANIFEST.json"
            data = high.read(manifest)
            data["files_sha256"]["unbound.py"] = "0" * 64
            manifest.write_text(json.dumps(data))
            pins[prefix + "MANIFEST.json"] = high.digest(manifest)
            with self.assertRaisesRegex(ValueError, "binds every native source"):
                high.collect_sources(root, pins, "high5_v1")

    def test_fresh_capture_records_actual_cwd_command_and_bytes(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            _, directory, _ = self.fixture(root)
            stdout = directory / "real.stdout.txt"
            stdout.write_bytes(b"real guarded output\n")
            inputs = {"bound.py": high.digest(directory / "bound.py")}
            command = [sys.executable, "-B", "bound.py", "CONSTRUCTED.json"]
            capture = high.persist_capture(root, directory, "high5", "construct", command,
                                           inputs, stdout, "fixture time", 0.01)
            metadata = high.read(capture / "metadata.json")
            self.assertEqual(metadata["cwd"], str(directory.resolve()))
            self.assertEqual(metadata["command"], command)
            self.assertEqual(metadata["stdout_sha256"], high.digest(stdout))
            self.assertEqual((capture / "stdout.txt").read_bytes(), stdout.read_bytes())
            self.assertEqual((capture / "stderr.txt").read_bytes(), b"")
            with self.assertRaises(FileExistsError):
                high.persist_capture(root, directory, "high5", "construct", command,
                                     inputs, stdout, "fixture time", 0.01)

    def test_wrong_command_is_not_recorded_as_native(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            _, directory, _ = self.fixture(root)
            stdout = directory / "real.stdout.txt"
            stdout.write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "Exact actual native HIGH command"):
                high.persist_capture(root, directory, "high5", "construct",
                                     [sys.executable, "-B", "other.py", "CONSTRUCTED.json"],
                                     {}, stdout, "fixture", 0)


if __name__ == "__main__":
    unittest.main()
