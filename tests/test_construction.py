from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

from construction.generate_certificate import make_cell, normalize_seed
from construction.parameter_bank import ParameterSeed
from construction.verify import (
    LEGACY_MARKER_FORMAT,
    MARKER_FORMAT,
    acquire_run_lock,
    configuration_digest,
    marker_is_current,
    marker_source_state,
    release_run_lock,
    sha256_file,
)
from proof.berry_core import A, TARGET_Q, build_constants, evaluate_cell, lb


class ConstructionTests(unittest.TestCase):
    def test_artifact_tree_lock_rejects_a_concurrent_run(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "verification.lock"
            first = acquire_run_lock(path)
            try:
                with self.assertRaises(OSError):
                    acquire_run_lock(path)
            finally:
                release_run_lock(first)
            second = acquire_run_lock(path)
            release_run_lock(second)

    @classmethod
    def setUpClass(cls):
        cls.constants = build_constants(192)

    def test_normalization_enforces_section_6_guards(self):
        raw = ParameterSeed(
            q=Fraction(100),
            t0=Fraction(1, 2),
            eta=Fraction(1, 2),
            lam=Fraction(1, 2),
            pieces=96,
            grid_power=3,
            rank=0,
        )
        normalized = normalize_seed(raw, rho_lo=Fraction(1))
        self.assertIsNotNone(normalized)
        assert normalized is not None
        self.assertLessEqual(normalized.q * normalized.eta, Fraction(2))

    def test_n8123_published_bank_recipe(self):
        seed = ParameterSeed(
            q=Fraction(6588397, 1048576),
            t0=Fraction(1, 4),
            eta=Fraction(1, 524288),
            lam=Fraction(1, 524288),
            pieces=96,
            grid_power=3,
            rank=0,
        )
        cell = make_cell(
            Fraction(41773777, 37696000),
            Fraction(20948673, 18848000),
            seed,
        )
        result = evaluate_cell(8123, cell, self.constants)
        self.assertTrue(result.ratio_upper <= lb(A(TARGET_Q)))

    def test_n10_published_bank_recipe_with_dyadic_tail_cutoff(self):
        seed = ParameterSeed(
            q=Fraction(1649555, 262144),
            t0=Fraction(21, 64),
            eta=Fraction(7, 262144),
            lam=Fraction(7, 262144),
            pieces=192,
            grid_power=2,
            rank=5,
        )
        cell = make_cell(
            Fraction(42762329, 37696000),
            Fraction(21442949, 18848000),
            seed,
        )
        result = evaluate_cell(10, cell, self.constants)
        self.assertTrue(result.ratio_upper <= lb(A(TARGET_Q)))

    def test_legacy_marker_remains_reusable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shard = root / "0002.json"
            shard.write_bytes(b"existing certificate bytes\n")
            config_sha256 = "a" * 64
            marker = root / "marker.json"
            marker.write_text(
                json.dumps(
                    {
                        "format": LEGACY_MARKER_FORMAT,
                        "n": 2,
                        "config_sha256": config_sha256,
                        "certificate_sha256": sha256_file(shard),
                        "bytes": shard.stat().st_size,
                        "generated_utc": "2026-08-05T00:00:00+00:00",
                    }
                ),
                encoding="utf-8",
            )
            self.assertTrue(
                marker_is_current(
                    marker,
                    shard,
                    2,
                    config_sha256,
                    marker_source_sha256="b" * 64,
                    allow_legacy=True,
                )
            )
            self.assertFalse(
                marker_is_current(
                    marker,
                    shard,
                    2,
                    config_sha256,
                    marker_source_sha256="b" * 64,
                    allow_legacy=False,
                )
            )

    def test_v2_marker_binds_previously_untracked_generator_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shard = root / "0002.json"
            shard.write_bytes(b"existing certificate bytes\n")
            marker = root / "marker.json"
            marker.write_text(
                json.dumps(
                    {
                        "format": MARKER_FORMAT,
                        "n": 2,
                        "config_sha256": "a" * 64,
                        "marker_source_sha256": "b" * 64,
                        "certificate_sha256": sha256_file(shard),
                        "bytes": shard.stat().st_size,
                    }
                ),
                encoding="utf-8",
            )
            self.assertTrue(
                marker_is_current(
                    marker,
                    shard,
                    2,
                    "a" * 64,
                    marker_source_sha256="b" * 64,
                    allow_legacy=False,
                )
            )
            self.assertFalse(
                marker_is_current(
                    marker,
                    shard,
                    2,
                    "a" * 64,
                    marker_source_sha256="c" * 64,
                    allow_legacy=True,
                )
            )

    def test_current_release_is_eligible_for_legacy_marker_reuse(self):
        repository = Path(__file__).resolve().parents[1]
        digest, allowed = marker_source_state(repository)
        self.assertTrue(allowed)
        self.assertRegex(digest, r"^[0-9a-f]{64}$")

    def test_restart_digest_keeps_the_v1_compatibility_inputs(self):
        repository = Path(__file__).resolve().parents[1]
        record = {
            "precision_bits": 192,
            "max_pieces": 4096,
            "constructor_sha256": sha256_file(
                repository / "construction" / "generate_certificate.py"
            ),
            "core_sha256": sha256_file(repository / "proof" / "berry_core.py"),
            "parameter_bank_manifest_sha256": sha256_file(
                repository / "data" / "parameter_bank" / "manifest.json"
            ),
        }
        self.assertEqual(
            configuration_digest(record),
            "5fcee55d6c4205ddd74ad6647a3360845a59e13d7263d887729667602c523559",
        )


if __name__ == "__main__":
    unittest.main()
