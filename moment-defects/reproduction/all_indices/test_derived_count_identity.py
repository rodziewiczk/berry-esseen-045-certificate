"""Derived source identities are not historical receipt identities."""
import json
from pathlib import Path
import tempfile
import unittest
from .discover_count import acceptance_identity,DERIVED_V14_DESIGNS


class DerivedIdentityTests(unittest.TestCase):
    def test_original_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            status,scope = acceptance_identity(Path(directory),29,'unused')
            self.assertEqual(status,'PASS_FRESH_CONDITIONAL_EXACT_COUNT29')
            self.assertIn('ORIGINAL',scope)
    def test_derived_requires_reviewed_design(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path/'B3_V14_SOURCE_EPOCH.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'reviewed exact design'):
                acceptance_identity(path,31,'0'*64)
    def test_derived_never_uses_historical_label(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            packet = dict(schema='NEW_CONDITIONAL_B3_V14_SOURCE_EPOCH_20261022_V1',n=25,index=31,
                          native_schema='NEW_CONDITIONAL_B3_V14_EPOCH_20261022_PANEL31_FULL_ROOTS_V1',
                          expected_native_status='PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT31',
                          helper_manifest_sha256='ba80569735e7042a588eba6c8219fbd68c4deae354c3983ea518dbbb2d9a8336',
                          arithmetic_accepted=False)
            (path/'B3_V14_SOURCE_EPOCH.json').write_text(json.dumps(packet))
            status,scope = acceptance_identity(path,31,DERIVED_V14_DESIGNS[31])
            self.assertIn('EPOCH_20261022',status)
            self.assertIn('DERIVED',scope)
            packet['expected_native_status'] = 'PASS_FRESH_CONDITIONAL_EXACT_COUNT31'
            (path/'B3_V14_SOURCE_EPOCH.json').write_text(json.dumps(packet))
            with self.assertRaises(ValueError): acceptance_identity(path,31,DERIVED_V14_DESIGNS[31])
