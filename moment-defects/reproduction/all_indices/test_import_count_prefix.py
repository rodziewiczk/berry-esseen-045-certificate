"""Bounded synthetic prefix topology tests; not numerical acceptances."""
from copy import deepcopy
from fractions import Fraction as F
import unittest

from . import import_count_prefix as imp
from .test_discovery import Oracle


class NeverEvaluate(Oracle):
    @staticmethod
    def evaluate(*args, **kwargs):
        raise AssertionError('Importer must never evaluate a mathematical cell')


class PrefixImportTests(unittest.TestCase):
    def setUp(self):
        self.cfg = dict(n=1, Lambda='1')
        self.header = dict(n=1, index=0, target='1/3', kernel_sha256={'source': 'pin'})
        self.box = NeverEvaluate.enc(NeverEvaluate.rootbox(self.cfg))
        self.packet = dict(schema=imp.OLD_SCHEMA, header=self.header,
                           discovery_source_sha256={}, origin=None, run={},
                           roots=[dict(k=k, tree=dict(kind='pending', box=deepcopy(self.box)))
                                  for k in range(2)])

    def test_pending_geometry_imported_without_acceptance(self):
        roots, stats = imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)
        self.assertEqual(roots[0]['tree'], {'kind': 'pending'})
        self.assertEqual(stats, dict(nodes=2, leaves=0, pending=2,
                                    arithmetic_accepted=False))
        self.assertIn('box', self.packet['roots'][0]['tree'])

    def test_changed_pending_box_rejected(self):
        self.packet['roots'][0]['tree']['box'][0][1] = '1/2'
        with self.assertRaises(ValueError):
            imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)

    def test_forged_header_rejected(self):
        with self.assertRaises(ValueError):
            imp.convert_prefix(self.packet, NeverEvaluate, self.cfg,
                               dict(self.header, target='2/3'))

    def test_missing_root_rejected(self):
        self.packet['roots'].pop()
        with self.assertRaises(ValueError):
            imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)

    def test_boolean_count_rejected(self):
        self.packet['roots'][0]['k'] = False
        with self.assertRaises(ValueError):
            imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)

    def test_saved_leaf_arithmetic_is_not_accepted(self):
        self.packet['roots'][0]['tree'] = dict(kind='leaf', box=self.box,
                                              decision='UNTRUSTED_FAKE',
                                              result={'score_upper': '0'})
        roots, stats = imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)
        self.assertEqual(roots[0]['tree']['decision'], 'UNTRUSTED_FAKE')
        self.assertFalse(stats['arithmetic_accepted'])

    def test_extra_success_claim_rejected(self):
        self.packet['roots'][0]['tree']['accepted'] = True
        with self.assertRaises(ValueError):
            imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)

    def test_both_closed_children_required(self):
        box = NeverEvaluate.rootbox(self.cfg)
        left, right = NeverEvaluate.children(box, 0, F(1, 2))
        self.packet['roots'][0]['tree'] = dict(
            kind='split', axis=0, cut='1/2',
            left=dict(kind='pending', box=NeverEvaluate.enc(left)),
            right=dict(kind='pending', box=NeverEvaluate.enc(right)))
        roots, stats = imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)
        self.assertEqual(stats['nodes'], 4)
        self.assertEqual(stats['pending'], 3)
        del self.packet['roots'][0]['tree']['right']
        with self.assertRaises(ValueError):
            imp.convert_prefix(self.packet, NeverEvaluate, self.cfg, self.header)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaises(ValueError):
            imp.unique([('accepted', False), ('accepted', True)])


if __name__ == '__main__':
    unittest.main()
