import hashlib
from fractions import Fraction
import os
from pathlib import Path
import tempfile
import unittest

from proof.berry_core import CertificateError, RHO0_Q, qstr
from proof.check_certificate import (
    BUNDLE_FORMAT,
    BUNDLE_SOURCE_PATHS,
    MAX_CELLS_PER_SHARD,
    arb_upper_dyadic,
    bounded_rational,
    bundle_source_hashes,
    certificate_set_digest,
    check_rho_cover,
    dyadic_fraction,
    format_dyadic_upper,
    load_json_bytes,
    prepare_audit_path,
    progress_due,
    validate_cell_shape,
)


def format_v2_cell(rho_lo: str = "1", rho_hi: str | None = None) -> dict:
    return {
        "rho": [rho_lo, rho_hi or qstr(RHO0_Q)],
        "q": "6",
        "t0": "3/4",
        "eta": "1/1024",
        "lambda": "1/1024",
        "grid": {"pieces": 32, "power": 3},
    }


class CheckerProtocolTests(unittest.TestCase):
    def test_progress_reports_early_values_and_multiples_of_ten(self):
        reported = [
            n
            for n in range(2, 32)
            if progress_due(n, n - 1, 8122, 10)
        ]
        self.assertEqual(
            reported,
            [2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30],
        )
        self.assertTrue(progress_due(8123, 8122, 8122, 10))
        self.assertFalse(progress_due(8122, 8122, 8122, 10))
        self.assertFalse(progress_due(20, 19, 8122, 0))

    def test_format_v2_grid_cell_shape_is_accepted(self):
        cell = format_v2_cell()
        self.assertIs(validate_cell_shape(2, 0, cell), cell)

    def test_partitions_field_is_rejected(self):
        cell = format_v2_cell()
        del cell["grid"]
        cell["partitions"] = {
            "first": ["1/1024", "3/4"],
            "second": ["3/4", "1"],
            "third": ["1/1024", "3/4"],
        }
        with self.assertRaisesRegex(CertificateError, "key mismatch"):
            validate_cell_shape(2, 0, cell)

    def test_json_floats_and_duplicate_keys_are_rejected(self):
        payloads = {
            "float": b'{"value": 0.5}',
            "duplicate": b'{"value": "1", "value": "2"}',
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, payload in payloads.items():
                with self.subTest(name=name):
                    path = root / f"{name}.json"
                    path.write_bytes(payload)
                    with self.assertRaises(CertificateError):
                        load_json_bytes(path, name)

    def test_certificate_set_digest_is_deterministic(self):
        entries = [
            {"n": 2, "sha256": "a" * 64},
            {"n": 3, "sha256": "b" * 64},
        ]
        canonical = (
            f"2:{'a' * 64}\n"
            f"3:{'b' * 64}\n"
        ).encode("ascii")
        expected = hashlib.sha256(canonical).hexdigest()
        self.assertEqual(certificate_set_digest(entries), expected)
        self.assertEqual(certificate_set_digest([dict(entry) for entry in entries]), expected)

    def test_rho_cover_requires_exact_final_endpoint(self):
        decimal_truncation = "1209794567/1000000000"
        self.assertNotEqual(decimal_truncation, qstr(RHO0_Q))
        with self.assertRaisesRegex(CertificateError, "rho cover ends"):
            check_rho_cover(2, [format_v2_cell(rho_hi=decimal_truncation)])

    def test_bundle_v2_binds_all_packaged_executable_sources(self):
        repository = Path(__file__).resolve().parents[1]
        hashes = bundle_source_hashes(repository)
        self.assertEqual(BUNDLE_FORMAT, "berry-esseen-045-certificate-bundle-v2")
        self.assertEqual(set(hashes), set(BUNDLE_SOURCE_PATHS))
        for value in hashes.values():
            self.assertRegex(value, r"^[0-9a-f]{64}$")

    def test_directed_decimal_is_never_below_exact_dyadic(self):
        from decimal import Decimal, localcontext

        cases = [(1, -10), (3, -10), (-3, -10), (7, -193)]
        with localcontext() as context:
            context.prec = 100
            for mantissa, exponent in cases:
                with self.subTest(mantissa=mantissa, exponent=exponent):
                    rendered = format_dyadic_upper(mantissa, exponent, places=3)
                    exact = dyadic_fraction(mantissa, exponent)
                    rendered_q = Decimal(rendered)
                    exact_q = Decimal(exact.numerator) / Decimal(exact.denominator)
                    self.assertGreaterEqual(rendered_q, exact_q)
                    self.assertLess(rendered_q - exact_q, Decimal("0.001"))

    def test_arb_endpoint_is_preserved_as_an_exact_dyadic(self):
        from flint import arb, ctx

        previous_precision = ctx.prec
        try:
            ctx.prec = 192
            value = arb(1) / 3
            mantissa, exponent = arb_upper_dyadic(value)
            exact_upper = dyadic_fraction(mantissa, exponent)
            self.assertGreater(exact_upper, Fraction(1, 3))
        finally:
            ctx.prec = previous_precision

    def test_json_size_limit_is_checked_before_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "oversize.json"
            path.write_bytes(b"{}   ")
            with self.assertRaisesRegex(CertificateError, "protocol limit"):
                load_json_bytes(path, "oversize", max_bytes=4)

    def test_rational_and_cell_count_resource_limits(self):
        with self.assertRaisesRegex(CertificateError, "character limit"):
            bounded_rational("1" * 257, "q")
        cell = format_v2_cell()
        with self.assertRaisesRegex(CertificateError, "cell protocol limit"):
            check_rho_cover(2, [cell] * (MAX_CELLS_PER_SHARD + 1))

    def test_audit_is_restricted_and_previous_receipt_is_invalidated(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "bundle"
            bundle.mkdir()
            manifest = bundle / "manifest.json"
            manifest.write_text("protected", encoding="utf-8")
            with self.assertRaisesRegex(CertificateError, "must be exactly"):
                prepare_audit_path(bundle, manifest)
            self.assertEqual(manifest.read_text(encoding="utf-8"), "protected")

            audit = bundle / "verification.json"
            audit.write_text('{"status":"ACCEPTED_FULL"}', encoding="utf-8")
            self.assertEqual(prepare_audit_path(bundle, audit), audit.resolve())
            self.assertFalse(audit.exists())

    def test_hard_link_cannot_disguise_a_protected_file_as_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory) / "bundle"
            bundle.mkdir()
            manifest = bundle / "manifest.json"
            manifest.write_text("protected", encoding="utf-8")
            audit = bundle / "verification.json"
            try:
                os.link(manifest, audit)
            except OSError as exc:
                self.skipTest(f"hard links unavailable: {exc}")
            with self.assertRaisesRegex(CertificateError, "regular, unlinked"):
                prepare_audit_path(bundle, audit)
            self.assertEqual(manifest.read_text(encoding="utf-8"), "protected")


if __name__ == "__main__":
    unittest.main()
