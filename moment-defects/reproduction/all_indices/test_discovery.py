"""Synthetic search-engine tests, not numerical proof acceptances."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest
from . import count_discovery as d


class Oracle:
    LIMIT = 10000
    @staticmethod
    def rootbox(cfg):
        return [[F(0),F(1)] for _ in range(5)]
    @staticmethod
    def enc(value):
        if isinstance(value,F): return str(value)
        if isinstance(value,list): return [Oracle.enc(x) for x in value]
        return value
    @staticmethod
    def same(a,b): return type(a) is type(b) and a == b
    @staticmethod
    def children(box,axis,cut):
        d.need(type(axis) is int and 0 <= axis < 5,'axis')
        d.need(type(cut) is F and box[axis][0] < cut < box[axis][1],'cut')
        a,b = deepcopy(box),deepcopy(box)
        a[axis][1],b[axis][0] = cut,cut
        return a,b
    @staticmethod
    def evaluate(cfg,k,box):
        return ('SYNTHETIC_CLOSE',{}) if box[0][1]-box[0][0] <= F(1,2) else (None,{})


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {'n':1,'Lambda':'1'}
        self.roots = [dict(k=k,tree={'kind':'pending'}) for k in range(2)]
    def test_complete_roots_required(self):
        with self.assertRaises(ValueError): d.census(Oracle,self.cfg,self.roots[:1])
    def test_boolean_root_rejected(self):
        self.roots[0]['k'] = False
        with self.assertRaises(ValueError): d.census(Oracle,self.cfg,self.roots)
    def test_saved_pending_cannot_claim_success(self):
        self.roots[0]['tree']['accepted'] = True
        with self.assertRaises(ValueError): d.census(Oracle,self.cfg,self.roots)
    def test_closed_children_and_fresh_leaf_conversion(self):
        pending,nodes,_ = d.census(Oracle,self.cfg,self.roots)
        d.advance(Oracle,self.cfg,pending[0],nodes,F(1))
        pending,nodes,_ = d.census(Oracle,self.cfg,self.roots)
        self.assertEqual(nodes,4)
        self.assertEqual(pending[0][3][0][1],pending[1][3][0][0])
        self.assertEqual(d.advance(Oracle,self.cfg,pending[0],nodes,F(1))[0],'leaf')
        self.assertEqual(d.census(Oracle,self.cfg,self.roots)[2],1)
    def test_node_limit_not_relaxed(self):
        pending,_,_ = d.census(Oracle,self.cfg,self.roots)
        with self.assertRaises(ValueError): d.advance(Oracle,self.cfg,pending[0],10000,F(1))
    def test_breadth_first_does_not_starve_original_roots(self):
        frontier = [(6,'LLR',{},[]),(7,'',{},[]),(8,'',{},[])]
        self.assertEqual(d.choose_pending(frontier,'breadth'),1)
        self.assertEqual(d.choose_pending(frontier,'depth'),0)
        self.assertEqual(d.choose_pending(frontier,'root-first'),1)
        self.assertEqual(d.choose_pending([(6,'LR',{},[]),(7,'R',{},[])],'root-first'),0)
    def test_corrupt_saved_leaf_box_rejected(self):
        self.roots[0]['tree'] = dict(kind='leaf',box=[['0','0']]*5,decision='fake',result={})
        with self.assertRaises(ValueError): d.census(Oracle,self.cfg,self.roots)
    def test_two_slot_snapshot_is_untrusted(self):
        with tempfile.TemporaryDirectory() as directory:
            packet = dict(schema=d.SCHEMA,roots=self.roots,arithmetic_accepted=False)
            d.save(Path(directory),packet)
            d.save(Path(directory),packet)
            saved = json.loads((Path(directory)/'CHECKPOINT.json').read_text())
            self.assertFalse(saved['arithmetic_accepted'])
            self.assertEqual(saved,json.loads((Path(directory)/'CHECKPOINT.backup.json').read_text()))
            self.assertFalse((Path(directory)/'CHECKPOINT.writing.json').exists())


if __name__ == '__main__': unittest.main()
