"""Owncap epoch/control-plane tests; no numerical theorem is asserted here."""
import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest

from . import c5_extension_worker as extension
from . import c5_owncaps_one as own


class OwncapEpochTests(unittest.TestCase):
    def fixture(self, root):
        relative = "work/cutoff5_20261020/high/owncaps5_v3/"
        directory = root / relative
        directory.mkdir(parents=True)
        graph = {}
        for name in own.RUNTIME:
            if name == "MANIFEST.json":
                continue
            path = directory / name
            path.write_text(json.dumps({"fixture": name}) if name == "PLAN.json" else "fixture")
            graph[relative + name] = own.digest(path)
        manifest = directory / "MANIFEST.json"
        manifest.write_text(json.dumps({"files_sha256": dict(graph)}))
        graph[relative + "MANIFEST.json"] = own.digest(manifest)
        return relative, directory, graph

    def test_complete_plan_and_runtime_are_bound(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            prefix, _, graph = self.fixture(root)
            pins = {}
            own.add_manifest(root, graph, pins, prefix, own.RUNTIME)
            self.assertEqual(pins, graph)

    def test_changed_plan_fails_before_any_execution(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            prefix, directory, graph = self.fixture(root)
            (directory / "PLAN.json").write_text('{"changed":true}')
            with self.assertRaisesRegex(ValueError, "Exact selected source"):
                own.add_manifest(root, graph, {}, prefix, own.RUNTIME)

    def test_native_capture_exact_command_actual_cwd(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            _, directory, _ = self.fixture(root)
            stdout = directory / "actual.stdout.txt"
            stdout.write_bytes(b"guarded result\n")
            command = [sys.executable, "-B", "protocol.py", "construct", "PLAN.json", "CONSTRUCTED.json"]
            pins = {"PLAN.json": own.digest(directory / "PLAN.json")}
            relative = "runs/cutoff5_20261020/high/owncaps_construct01"
            capture = own.persist_capture(root, directory, relative, command, pins,
                                          stdout, "fixture", 0.1)
            metadata = own.read(capture / "metadata.json")
            self.assertEqual(metadata["command"][1:], command[1:])
            self.assertEqual(metadata["cwd"], str(directory.resolve()))
            self.assertEqual(metadata["input_sha256"], pins)
            self.assertEqual((capture / "stdout.txt").read_bytes(), stdout.read_bytes())
            with self.assertRaises(ValueError):
                own.persist_capture(root, directory, relative, command, pins,
                                    stdout, "fixture", 0.1)

    def test_native_command_cannot_hide_extra_interpreter_options(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            _, directory, _ = self.fixture(root)
            stdout = directory / "actual.stdout.txt"
            stdout.write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "Actual ordinary native"):
                own.persist_capture(root, directory, "runs/invalid",
                                    [sys.executable, "-B", "-S", "protocol.py", "construct", "PLAN.json", "CONSTRUCTED.json"],
                                    {}, stdout, "fixture", 0)

    def test_coarse_capture_binds_full_workspace_graph_and_fresh_result(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            relative, directory, _ = self.fixture(root)
            capture_relative = "runs/cutoff6_20261018/fourier/auxiliary5_v2/construct01"
            capture = root / capture_relative
            capture.mkdir(parents=True)
            result = capture / "RESULT.json"
            result.write_bytes(b"fresh calculated fixture")
            plan = directory / "PLAN.json"
            stdout = directory / "actual.stdout.txt"
            stdout.write_bytes(b"fresh native output\n")
            command = [sys.executable, "-B", "protocol.py", "construct", str(plan), str(result)]
            pins = {relative + "PLAN.json": own.digest(plan)}
            own.persist_capture(root, directory, capture_relative, command, pins,
                                stdout, "fixture", 0.1, workspace_inputs=True, result_path=result)
            metadata = own.read(capture / "metadata.json")
            self.assertEqual(metadata["RESULT.json_sha256"], own.digest(result))
            self.assertEqual(metadata["input_sha256"], pins)
            self.assertEqual(metadata["changed_inputs"], [])

    def test_coarse_native_windows_keys_are_not_rewritten(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            relative, directory, _ = self.fixture(root)
            capture_relative = "runs/cutoff6_20261018/fourier/auxiliary5_v2/replay01"
            capture = root / capture_relative
            capture.mkdir(parents=True)
            result = capture / "RESULT.json"
            result.write_bytes(b"fixture result, not numerical acceptance")
            plan = directory / "PLAN.json"
            stdout = directory / "actual.stdout.txt"
            stdout.write_bytes(b"fixture captured output\n")
            native_key = (relative + "PLAN.json").replace("/", "\\")
            pins = {native_key: own.digest(plan)}
            command = [sys.executable, "-B", "protocol.py", "replay", str(plan), str(result)]
            own.persist_capture(root, directory, capture_relative, command, pins,
                                stdout, "fixture", 0.1, workspace_inputs=True, result_path=result)
            metadata = own.read(capture / "metadata.json")
            self.assertEqual(metadata["input_sha256"], pins)
            self.assertNotIn(relative + "PLAN.json", metadata["input_sha256"])

    def test_fourier_subproof_excludes_unrelated_b3_code_but_keeps_writer(self):
        tree = ast.parse('''
def main():
    raise RuntimeError("unrelated missing historical B3 preparer")
    src = "source"
    dst = "target"
    write("FOURIER_CHECKED.json", {"fixture": True})
    print("PASS_B3_PORT_AND_FOURIER_EXTENSION", 25)
''')
        writes = []
        scope = {"write": lambda name, value: writes.append((name, value))}
        exec(compile(extension.subproof(tree), "fixture", "exec"), scope)
        self.assertEqual(writes, [("FOURIER_CHECKED.json", {"fixture": True})])

    def test_fourier_subproof_rejects_missing_final_receipt_writer(self):
        tree = ast.parse('''
def main():
    src = "source"
    incomplete = True
    print("PASS_B3_PORT_AND_FOURIER_EXTENSION", 25)
''')
        with self.assertRaisesRegex(ValueError, "retains its original fresh receipt writer"):
            extension.subproof(tree)


if __name__ == "__main__":
    unittest.main()
