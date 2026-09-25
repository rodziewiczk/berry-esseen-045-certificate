import hashlib
import importlib
import inspect
import json
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def import_builder_without_cuda():
    """Import the builder for CPU-only integrity tests."""
    cupy = types.ModuleType("cupy")
    cupy.__version__ = "test-only"
    cupy.RawKernel = lambda *args, **kwargs: object()
    cupyx = types.ModuleType("cupyx")
    cupyx.__path__ = []
    scipy = types.ModuleType("cupyx.scipy")
    scipy.__path__ = []
    special = types.ModuleType("cupyx.scipy.special")
    special.exp1 = lambda value: value
    pandas = types.ModuleType("pandas")
    pandas.__version__ = "test-only"
    modules = {
        "cupy": cupy,
        "cupyx": cupyx,
        "cupyx.scipy": scipy,
        "cupyx.scipy.special": special,
        "pandas": pandas,
    }
    with mock.patch.dict(sys.modules, modules):
        builder = importlib.import_module("reproduction.build_parameter_bank")
    sys.modules.pop("reproduction.build_parameter_bank", None)
    sys.modules.pop("reproduction.gpu_search", None)
    package = sys.modules.get("reproduction")
    if package is not None:
        package.__dict__.pop("build_parameter_bank", None)
        package.__dict__.pop("gpu_search", None)
    return builder


class ReproductionIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = import_builder_without_cuda()

    def test_publication_geometry_digest_matches_committed_arrays(self):
        bank = ROOT / "data" / "parameter_bank"
        n = np.load(bank / "n.npy", mmap_mode="r", allow_pickle=False)
        depth = np.load(bank / "depth.npy", mmap_mode="r", allow_pickle=False)
        index = np.load(bank / "cell_index.npy", mmap_mode="r", allow_pickle=False)
        manifest = json.loads((bank / "manifest.json").read_text(encoding="utf-8"))

        actual = self.builder.geometry_digest(n, depth, index)

        self.assertEqual(actual, manifest["geometry_sha256"])
        self.assertEqual(actual, self.builder.EXPECTED_GEOMETRY_SHA256)

    def test_authenticated_manifest_preserves_reference_bytes(self):
        reference_bytes = b'{\n  "z": [1, 2],\n  "a": 3\n}\n'
        generated = {"a": 3, "z": [1, 2]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference = root / "reference.json"
            output = root / "manifest.json"
            reference.write_bytes(reference_bytes)

            digest = self.builder.write_authenticated_manifest(
                output, generated, reference
            )

            self.assertEqual(output.read_bytes(), reference_bytes)
            self.assertEqual(digest, hashlib.sha256(reference_bytes).hexdigest())
            self.assertIn(
                "write_authenticated_manifest(",
                inspect.getsource(self.builder.write_final_bank),
            )

    def test_authenticated_manifest_rejects_semantic_difference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference = root / "reference.json"
            output = root / "manifest.json"
            reference.write_text('{"arrays": {"n": 1}}\n', encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "does not match"):
                self.builder.write_authenticated_manifest(
                    output, {"arrays": {"n": 2}}, reference
                )

            self.assertFalse(output.exists())

    def test_drive_publication_pointer_exposes_only_authenticated_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bank = root / "bank"
            mirror = root / "mirror"
            bank.mkdir()
            (bank / "manifest.json").write_text('{"version": 1}\n', encoding="utf-8")
            (bank / "payload.bin").write_bytes(b"complete payload")

            pointer = self.builder.publish_bank_to_mirror(bank, mirror)
            published = mirror / pointer["artifact"]

            self.assertTrue(published.is_dir())
            self.assertEqual(
                pointer["tree_sha256"], self.builder.directory_digest(published)
            )
            self.assertEqual(
                json.loads(
                    (mirror / "published_parameter_bank.json").read_text(
                        encoding="utf-8"
                    )
                ),
                pointer,
            )

            (bank / "payload.bin").write_bytes(b"different payload")
            with self.assertRaisesRegex(RuntimeError, "different content"):
                self.builder.publish_bank_to_mirror(bank, mirror)

    def test_colab_notebook_requires_and_verifies_full_commit_sha(self):
        notebook = json.loads(
            (ROOT / "notebooks" / "build_parameter_bank_colab.ipynb").read_text(
                encoding="utf-8"
            )
        )
        code = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        self.assertIn(r'[0-9a-fA-F]{40}', code)
        self.assertIn("RESOLVED_COMMIT != REQUESTED_COMMIT", code)
        self.assertIn("published_parameter_bank.json", code)
        self.assertIn("pip_freeze_sha256", code)
        self.assertIn("locked_distribution_fingerprints", code)
        self.assertIn('"--force-reinstall"', code)
        self.assertIn('"reproduction_package"', code)
        self.assertIn("if cuda_major != 12", code)
        self.assertIn(
            '"reproduction_package"',
            inspect.getsource(self.builder.publication_identity),
        )
        self.assertIn(
            "cuda_runtime // 1000 != 12",
            inspect.getsource(self.builder.build_publication_bank),
        )
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), "colab-cell", "exec")

    def test_gpu_dependency_closure_is_exact_and_known_compatible(self):
        requirements = (ROOT / "requirements-gpu.txt").read_text(encoding="utf-8")
        pinned = {}
        hashes = {}
        for line in requirements.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("--"):
                continue
            match = re.fullmatch(
                r"([A-Za-z0-9_.-]+)==([^\s]+) "
                r"--hash=sha256:([0-9a-f]{64})",
                line,
            )
            self.assertIsNotNone(match, f"GPU dependency is not exactly pinned: {line}")
            pinned[match.group(1).lower()] = match.group(2)
            hashes[match.group(1).lower()] = match.group(3)

        self.assertIn("--only-binary=:all:", requirements)
        self.assertIn("--require-hashes", requirements)
        self.assertEqual(
            pinned,
            {
                "cupy-cuda12x": "14.0.1",
                "cuda-pathfinder": "1.3.3",
                "numpy": "2.0.2",
                "pandas": "2.2.3",
                "python-dateutil": "2.9.0.post0",
                "pytz": "2025.2",
                "six": "1.17.0",
                "tzdata": "2025.2",
            },
        )
        self.assertEqual(set(hashes), set(pinned))
        numpy_major, numpy_minor, *_ = map(int, pinned["numpy"].split("."))
        self.assertGreaterEqual((numpy_major, numpy_minor), (2, 0))
        self.assertLess((numpy_major, numpy_minor), (2, 6))


if __name__ == "__main__":
    unittest.main()
