from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import tempfile
import unittest

from .c5_counts import FINAL_SHA, digest
from .c5_parent_evidence import (ParentEvidence, checked_json, exact_int, regular_owned,
                                 report_epoch, validate_wrapper, verify_capture, verify_graph)
from .c5_parent_facts import BoundFact,GlobalOwncapFact
from .c5_initial_join import numeric_join,canonical_sha

PIN = '1'*64


class InitialNumericJoinTests(unittest.TestCase):
    def setUp(self):
        self.facts = dict(n=5,profile=dict(n=5,nmax=5,q_contact='0',radius='99/40',
            radius_minus='99/40',radius_plus='99/40',invariants=dict(rho_lo='237/200',rho='6/5')),
            numerical_premises=dict(HIGH='193/500',owncap='207/500'))
        parents = (
            BoundFact('support',5,F(237,200),F(6,5),F(99,40),None,PIN),
            BoundFact('HIGH',5,F(1),F(6,5),F(3),F(385,1000),PIN),
            BoundFact('owncap',5,F(237,200),F(6,5),F(99,40),F(411,1000),PIN))
        self.evidence = ParentEvidence(parents,GlobalOwncapFact(F(428,1000),PIN),(),())

    def test_exact_numeric_join_never_claims_executed_fresh_parents(self):
        joined = numeric_join(self.facts,self.evidence)
        self.assertTrue(joined['source_bound_parent_implications_verified'])
        self.assertFalse(joined['execution_observed_by_this_reader'])
        self.assertFalse(joined['fresh_parent_fact_joins_verified'])
        self.assertFalse(joined['all_index_conclusion_verified'])
        self.assertNotIn('fresh_run',joined)
        self.assertEqual(len(joined['retained_analytic_premises']),4)
        self.assertEqual(joined['numerical_parent_edges'][2]['actual_upper'],'411/1000')

    def test_regional_moment_gap_is_not_a_numeric_join(self):
        facts = deepcopy(self.facts);facts['profile']['invariants']['rho_lo'] = '1'
        with self.assertRaises(ValueError): numeric_join(facts,self.evidence)

    def test_recorded_parent_evidence_remains_explicitly_posthoc(self):
        declared = self.evidence.declaration()
        self.assertFalse(declared['execution_observed_by_this_reader'])
        self.assertFalse(declared['fresh_parent_fact_joins_verified'])

    def test_canonical_candidate_cover_hash_ignores_dictionary_order_only(self):
        self.assertEqual(canonical_sha({'a':1,'b':2}),canonical_sha({'b':2,'a':1}))
        self.assertNotEqual(canonical_sha({'a':1}),canonical_sha({'a':1.0}))


class ParentArtifactEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.epoch = self.work/'h5-test';self.epoch.mkdir()
        self.directory = self.epoch/'native';self.directory.mkdir()
        self.source = self.directory/'bound.py';self.source.write_text('pass\n',encoding='utf-8')
        self.capture = self.epoch/'capture';self.capture.mkdir()
        (self.capture/'stdout.txt').write_text('PASS\n',encoding='utf-8')
        (self.capture/'stderr.txt').write_bytes(b'')
        self.metadata = dict(command=[sys.executable,'-B','bound.py','REPLAY.json'],
            cwd=str(self.directory.resolve()),returncode=0,started_utc='2026-10-22T10:00:00+00:00',
            finished_utc='2026-10-22T10:00:01+00:00',elapsed_seconds=1,
            input_sha256={'bound.py':digest(self.source)},
            stdout_sha256=digest(self.capture/'stdout.txt'),stderr_sha256=digest(self.capture/'stderr.txt'))
        self.save_metadata()

    def save_metadata(self):
        (self.capture/'metadata.json').write_text(json.dumps(self.metadata),encoding='utf-8')

    def verify(self):
        return verify_capture(self.epoch,self.capture,self.directory,['-B','bound.py','REPLAY.json'])

    def test_complete_capture_is_artifact_evidence_not_authenticated_execution(self):
        result = self.verify()
        self.assertEqual(result['scope'],'RECORDED_BYTES_AND_COMMAND_ONLY_NOT_EXECUTION_AUTHENTICATION')
        self.assertNotIn('fresh_run',result)

    def test_recorded_wrong_command_or_historical_cwd_is_rejected(self):
        for field,value in [('command',[sys.executable,'bound.py','REPLAY.json']),
                            ('cwd',str(self.work)),('returncode',False),('elapsed_seconds',True)]:
            original = self.metadata[field];self.metadata[field] = value;self.save_metadata()
            with self.subTest(field=field),self.assertRaises(ValueError): self.verify()
            self.metadata[field] = original;self.save_metadata()

    def test_changed_source_or_log_is_rejected(self):
        self.source.write_text('changed\n',encoding='utf-8')
        with self.assertRaises(ValueError): self.verify()
        self.source.write_text('pass\n',encoding='utf-8')
        (self.capture/'stdout.txt').write_text('rewritten\n',encoding='utf-8')
        with self.assertRaises(ValueError): self.verify()

    def test_no_escaping_artifact_or_historical_report(self):
        with self.assertRaises(ValueError): regular_owned(self.epoch,self.work/'anything')
        with self.assertRaises(ValueError): regular_owned(self.epoch,self.epoch/'..'/'anything')
        with self.assertRaises(ValueError): validate_wrapper({'status':'PASS_OLD'},'scope','status')
        wrapper = dict(scope='scope',status='status',fresh_arithmetic=True,
                       original_final_graph_sha256=FINAL_SHA,all_index_conclusion_verified=False)
        validate_wrapper(wrapper,'scope','status')
        wrapper['all_index_conclusion_verified'] = True
        with self.assertRaises(ValueError): validate_wrapper(wrapper,'scope','status')

    def test_complete_native_source_graph_and_no_float_census(self):
        pins = {'native/bound.py':digest(self.source)}
        self.assertEqual(verify_graph(self.epoch,pins),pins)
        with self.assertRaises(ValueError): verify_graph(self.epoch,{'../outside':'1'*64})
        with self.assertRaises(ValueError): exact_int(2592.0,2592)

    def test_duplicate_json_keys_or_changed_pin_are_rejected(self):
        path = self.epoch/'bad.json';path.write_text('{"a":1,"a":2}',encoding='utf-8')
        with self.assertRaises(ValueError): checked_json(self.epoch,path)
        path.write_text('{}',encoding='utf-8')
        with self.assertRaises(ValueError): checked_json(self.epoch,path,'0'*64)

    def test_report_must_be_immediate_private_epoch_child(self):
        path = self.epoch/'FRESH_HIGH_RESULT.json';path.write_text('{}',encoding='utf-8')
        self.assertEqual(report_epoch(path,path.name,self.work),self.epoch)
        with self.assertRaises(ValueError): report_epoch(path,'OLD.json',self.work)


if __name__ == '__main__':
    unittest.main()
