"""Synthetic source-transform controls only; no numerical evaluator is run."""
import ast
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).with_name('prepare_b3_v14_epoch_2026_10_22.py')
SPEC = importlib.util.spec_from_file_location('conditional_v14_preparer_test', SOURCE)
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)


def original(index=31, controls=24):
    return ("from rho_signed_moment_tightener import cell35\n"
            "LIMIT=10000\n"
            "def load():\n cfg=contract['rows'][0]\n return cfg\n"
            "def rootbox(cfg):\n return cfg\n"
            "def children(box,axis,cut):\n return box,box\n"
            "def evaluate(cfg,k,b):\n return F(z['score_upper'])<CE_LO\n"
            "def replay(x,cfg,bound,cache):\n return depth<=128\n"
            "def first(x,kind):\n return x\n"
            "def construct():\n return None\n"
            f"def header(bound):\n return dict(schema='LOW25_B3_GLOBAL_ALPHA_STOPLOSS2_V12_PANEL{index}_RIGHT_HALF_CLOSED_COUNT_FOREST_V1')\n"
            f"def accept():\n mutations={[(str(i), None) for i in range(controls)]!r}\n"
            f" return dict(status='PASS_FRESH_CONDITIONAL_EXACT_COUNT{index}')\n").encode()


class ConditionalV14SourceTests(unittest.TestCase):
    def test_both_new_honest_source_identities(self):
        for index in (31, 32):
            source, schema, status = P.derive_protocol(original(index), index)
            ast.parse(source)
            self.assertIn('NEW_CONDITIONAL_B3_V14_EPOCH_20261022', schema)
            self.assertEqual(status, f'PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT{index}')
            self.assertIn(b'validate_premise(cfg)', source)
            self.assertIn(b'exact original B3 row plus explicit contact hypotheses', source)

    def test_missing_native_mutation_control_rejected(self):
        with self.assertRaises(ValueError):
            P.derive_protocol(original(controls=23), 31)

    def test_node_limit_not_relaxed(self):
        with self.assertRaises(ValueError):
            P.derive_protocol(original().replace(b'LIMIT=10000', b'LIMIT=20000'), 31)

    def test_depth_limit_not_relaxed(self):
        with self.assertRaises(ValueError):
            P.derive_protocol(original().replace(b'depth<=128', b'depth<=256'), 31)

    def test_strict_score_not_relaxed(self):
        with self.assertRaises(ValueError):
            P.derive_protocol(original().replace(b"F(z['score_upper'])<CE_LO",
                                                b"F(z['score_upper'])<=CE_LO"), 31)

    def test_ambiguous_import_rejected(self):
        source = original() + b'from rho_signed_moment_tightener import cell35\n'
        with self.assertRaises(ValueError):
            P.derive_protocol(source, 31)

    def test_wrong_original_identity_rejected(self):
        with self.assertRaises(ValueError):
            P.derive_protocol(original(31), 32)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaises(ValueError):
            P.parsed('{"n":25,"n":24}')


if __name__ == '__main__':
    unittest.main()
