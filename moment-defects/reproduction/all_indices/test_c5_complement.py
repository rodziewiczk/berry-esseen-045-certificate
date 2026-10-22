"""Complement adapter structural tests, not numerical certificate acceptance."""
import ast
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

from . import c5_complement as frontend
from . import c5_complement_one as supervisor
from . import c5_complement_worker as worker


NATIVE_FIXTURE = '''
from pathlib import Path
def read(p):
    return {}
def verify(z):
    return z
plan = read("PLAN.json")
controls = []
for label in ["fixture"]:
    controls.append(label)
manifest = read(Path("MANIFEST.json"))
raise RuntimeError("Parent metadata must not be executed")
'''

INDEPENDENT_FIXTURE = '''
def main():
    raise RuntimeError("Old captures must not be executed")
    controls = []
    def reject(fun, label):
        controls.append(label)
    for label, change in [("Fourier A", None), ("Fourier B", None)]:
        controls.append(label)
    for label, change in [("Fourier C", None)]:
        controls.append(label)
    for label, change in [("support parent", None)]:
        supportobjects[label] = change
    reject(lambda: None, "duplicate JSON key")
    raise RuntimeError("Old parent writers must not be executed")
'''


class ComplementAdapterTests(unittest.TestCase):
    def test_cache_prepare_only_calls_source_selection_inspection(self):
        with tempfile.TemporaryDirectory() as name:
            with patch.object(sys, "argv", ["c5_complement.py", "--cache", name, "--prepare-only"]), \
                    patch.object(frontend.subprocess, "call", return_value=0) as call:
                self.assertEqual(frontend.main(), 0)
            command = call.call_args.args[0]
            self.assertIn("c5_complement_one.py", Path(command[3]).name)
            self.assertEqual(command[-1], "--inspect")

    def test_frontend_does_not_accept_archive_and_cache_together(self):
        with patch.object(sys, "argv", ["c5_complement.py", "--cache", "cache", "--archive", "archive"]), \
                patch("sys.stderr"), self.assertRaises(SystemExit) as error:
            frontend.main()
        self.assertEqual(error.exception.code, 2)

    def test_worker_source_names_are_closed_relative_paths(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            source = root / "work/source.py"
            source.parent.mkdir()
            source.write_bytes(b"source")
            self.assertEqual(worker.safe_source(root, "work/source.py"), source)
            for bad in ("/work/source.py", "work/../work/source.py", "work\\source.py", "C:/work/source.py", "work//source.py"):
                with self.subTest(path=bad), self.assertRaises(ValueError):
                    worker.safe_source(root, bad)

    def capture_fixture(self, root):
        directory = root / "work/cutoff5_20261020/high/complement5_v1"
        directory.mkdir(parents=True)
        pins = {}
        for name in ("protocol.py", "PLAN.json", "MANIFEST.json"):
            path = directory / name
            path.write_bytes(b"schema fixture, not arithmetic")
            pins[name] = worker.sha(path)
        (directory / "CONSTRUCTED.json").write_bytes(b"not a certificate")
        capture = root / "runs/cutoff5_20261020/high/complement_construct01"
        capture.mkdir(parents=True)
        (capture / "stdout.txt").write_bytes(b"EXACT_SUPPORTED_COMPLEMENT5_WHOLE_COVER_PASS STRIPS 41 fixture\n")
        (capture / "stderr.txt").write_bytes(b"")
        metadata = {"returncode": 0, "cwd": str(directory.resolve()),
                    "command": [sys.executable, "-B", "protocol.py", "construct", "PLAN.json", "CONSTRUCTED.json"],
                    "scope": "NEW_ACTUAL_GUARDED_NATIVE_EXECUTION", "changed_inputs": [],
                    "input_sha256": pins, "stdout_sha256": worker.sha(capture / "stdout.txt"),
                    "stderr_sha256": worker.sha(capture / "stderr.txt")}
        (capture / "metadata.json").write_text(json.dumps(metadata))
        return directory, capture, metadata

    def test_capture_metadata_schema_binds_exact_command_and_sources(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            directory, _, _ = self.capture_fixture(root)
            result = worker.captured_integration(root, directory, "construct")
            self.assertEqual(result["action"], "construct")
            self.assertEqual(result["result_sha256"], worker.sha(directory / "CONSTRUCTED.json"))

    def test_old_absolute_capture_path_cannot_be_relabelled_current(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            directory, capture, metadata = self.capture_fixture(root)
            metadata["cwd"] = "/old/macOS/workspace"
            (capture / "metadata.json").write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "current successful"):
                worker.captured_integration(root, directory, "construct")

    def test_capture_cannot_hide_modified_native_inputs(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            directory, _, _ = self.capture_fixture(root)
            (directory / "PLAN.json").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "input unchanged"):
                worker.captured_integration(root, directory, "construct")

    def test_failed_or_boolean_returncode_cannot_be_accepted(self):
        for returncode in (1, False):
            with self.subTest(returncode=returncode), tempfile.TemporaryDirectory() as name:
                root = Path(name)
                directory, capture, metadata = self.capture_fixture(root)
                metadata["returncode"] = returncode
                (capture / "metadata.json").write_text(json.dumps(metadata))
                with self.assertRaisesRegex(ValueError, "current successful"):
                    worker.captured_integration(root, directory, "construct")

    def test_native_prefix_retains_arithmetic_but_not_parent_metadata(self):
        selected = worker.native_arithmetic_prefix(ast.parse(NATIVE_FIXTURE))
        scope = {}
        exec(compile(selected, "native fixture", "exec"), scope)
        self.assertEqual(scope["controls"], ["fixture"])
        self.assertNotIn("manifest", scope)
        self.assertIsNotNone(scope["verify"])

    def test_native_missing_manifest_boundary_fails(self):
        with self.assertRaisesRegex(ValueError, "Unique native"):
            worker.native_arithmetic_prefix(ast.parse(NATIVE_FIXTURE.replace("manifest =", "other =")))

    def test_native_boundary_cannot_be_an_unrelated_assignment(self):
        bad = NATIVE_FIXTURE.replace('manifest = read(Path("MANIFEST.json"))', 'manifest = True')
        with self.assertRaisesRegex(ValueError, "Exact original boundary"):
            worker.native_arithmetic_prefix(ast.parse(bad))

    def test_native_final_mutation_loop_cannot_be_omitted(self):
        bad = NATIVE_FIXTURE.replace('manifest = read', 'unrelated = True\nmanifest = read')
        with self.assertRaisesRegex(ValueError, "All native mutation"):
            worker.native_arithmetic_prefix(ast.parse(bad))

    def test_independent_all_fourier_and_json_controls_no_support_claim(self):
        selected = worker.independent_arithmetic_controls(ast.parse(INDEPENDENT_FIXTURE))
        scope = {}
        exec(compile(selected, "readback fixture", "exec"), scope)
        self.assertEqual(scope["controls"], ["Fourier A", "Fourier B", "Fourier C", "duplicate JSON key"])
        self.assertNotIn("supportobjects", scope)

    def test_independent_duplicate_json_control_cannot_be_dropped(self):
        bad = INDEPENDENT_FIXTURE.replace('reject(lambda: None, "duplicate JSON key")', 'pass')
        with self.assertRaisesRegex(ValueError, "duplicate-JSON"):
            worker.independent_arithmetic_controls(ast.parse(bad))

    def test_support_parent_cannot_be_silently_counted_as_fourier_control(self):
        bad = INDEPENDENT_FIXTURE.replace('controls.append(label)\n    for label, change in [("Fourier C"',
                                           'supportobjects[label] = change\n    for label, change in [("Fourier C"')
        with self.assertRaisesRegex(ValueError, "not silently relabelled"):
            worker.independent_arithmetic_controls(ast.parse(bad))

    def test_mutated_native_source_fails_before_loading_any_results(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            native = root / "accept.py"
            independent = root / "check.py"
            native.write_text(NATIVE_FIXTURE)
            independent.write_text(INDEPENDENT_FIXTURE)
            with self.assertRaisesRegex(ValueError, "Exact original native acceptor"):
                worker.validate_two_results(native, independent, root)

    def test_json_duplicate_keys_fail(self):
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            json.loads('{"n":5,"n":6}', object_pairs_hook=worker.unique)

    def test_forbidden_old_receipt_source_is_not_a_valid_selected_manifest(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            original = supervisor.COMPLEMENT + "CONSTRUCTED.json"
            target = root / original
            target.parent.mkdir(parents=True)
            target.write_bytes(b"old status")
            # No complete verified final graph/manifest closure is supplied.
            with self.assertRaises(ValueError):
                supervisor.selected_sources(root, {original: supervisor.digest(target)})


if __name__ == "__main__":
    unittest.main()
