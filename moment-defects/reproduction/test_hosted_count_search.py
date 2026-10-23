"""Small command/schema/mutation fixtures; no archive, download or evaluator."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch

from . import hosted_count_search as hosted


class HostedCountTests(unittest.TestCase):
    def hint_fixture(self,root,mutate=None,extra=False):
        capsule=root/'capsule';capsule.mkdir()
        (capsule/'count_protocol.py').write_text("def header(bound):return dict(schema='FIXTURE',n=25,index=29)\n")
        (capsule/'contract.json').write_text('{}')
        (capsule/'kernel.py').write_text('# fixed SOURCE FIXTURE, never executed\n')
        (capsule/'KERNEL_COPY_MANIFEST.json').write_text(json.dumps(dict(files={'kernel.py':hosted.digest(capsule/'kernel.py')})))
        header=hosted.native_header_sources(capsule,'b4-q0');payloads={};rows={}
        for name,(_,index,design)in hosted.TARGETS.items():
            value=dict(schema='UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1',
                binding=dict(design_sha256=design,alpha_priority='4',native_header=dict(header,index=index)),
                roots=[dict(k=k,tree={'kind':'pending'})for k in range(26)],arithmetic_accepted=False)
            if name=='b4-q0'and mutate is not None:mutate(value)
            raw=json.dumps(value,separators=(',',':')).encode()
            member='checkpoints/'+name+'/CHECKPOINT.json';payloads[member]=raw
            rows[name]=dict(member=member,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),design_sha256=design,n=25,index=index)
        manifest=dict(schema=hosted.HINT_SCHEMA,arithmetic_accepted=False,targets=rows)
        archive=root/'hints.zip'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED)as zipped:
            zipped.writestr('manifest.json',json.dumps(manifest))
            for name,raw in payloads.items():zipped.writestr(name,raw)
            if extra:zipped.writestr('unexpected.txt','no')
        return capsule,archive,payloads[rows['b4-q0']['member']]

    def test_full_untrusted_hint_bytes_preserved_without_any_evaluator(self):
        with tempfile.TemporaryDirectory()as directory:
            root=Path(directory);capsule,archive,raw=self.hint_fixture(root)
            with patch.object(hosted,'run_recorded',side_effect=AssertionError('No process in a fixture')):
                result=hosted.extract_hint(archive,hosted.digest(archive),'b4-q0',capsule,root/'hint.json')
            self.assertEqual((root/'hint.json').read_bytes(),raw)
            self.assertTrue(result['saved_leaf_results_are_untrusted'])
            self.assertFalse(result['native_acceptance_verified'])

    def test_rehashed_bad_hint_geometry_or_source_epoch_is_rejected(self):
        changes=[lambda x:x.update(arithmetic_accepted=True),
            lambda x:x['roots'].pop(),lambda x:x['roots'][0].update(k=False),
            lambda x:x['binding'].update(design_sha256='0'*64),
            lambda x:x['binding']['native_header'].update(checker_sha256='0'*64),
            lambda x:x['binding'].update(alpha_priority='1')]
        for change in changes:
            with tempfile.TemporaryDirectory()as directory:
                root=Path(directory);capsule,archive,_=self.hint_fixture(root,change)
                with self.assertRaises(ValueError):
                    hosted.extract_hint(archive,hosted.digest(archive),'b4-q0',capsule,root/'hint.json')
        with tempfile.TemporaryDirectory()as directory:
            root=Path(directory);capsule,archive,_=self.hint_fixture(root,extra=True)
            with self.assertRaises(ValueError):hosted.extract_hint(archive,hosted.digest(archive),'b4-q0',capsule,root/'hint.json')

    def test_event_is_durable_and_cannot_promote_global_claim(self):
        with tempfile.TemporaryDirectory()as directory:
            root=Path(directory)
            hosted.event(root,'fixture_started',target='b4-q0',native_acceptance_verified=False,
                         all_index_conclusion_verified=False)
            value=json.loads((root/'HOSTED_EVENTS.jsonl').read_text())
            self.assertEqual(value['event'],'fixture_started')
            self.assertFalse(value['all_index_conclusion_verified'])
            with self.assertRaises(ValueError):hosted.event(root,'bad',all_index_conclusion_verified=True)

    def test_exact_seven_targets_distinct_v14_identity(self):
        self.assertEqual(len(hosted.TARGETS),7)
        self.assertEqual(sum(v[0]=='original-v12'for v in hosted.TARGETS.values()),5)
        self.assertEqual(sum(v[0]=='new-conditional-v14'for v in hosted.TARGETS.values()),2)
        self.assertEqual(len({v[2]for v in hosted.TARGETS.values()}),7)
        self.assertIn('NOT_HISTORICAL',hosted.scope('b3-p31-v14-new'))
        self.assertIn('ORIGINAL_V12',hosted.scope('b3-p33'))

    def test_original_source_preparer_commands_only(self):
        old=hosted.preparation_command('b4-q0',Path('archives'),Path('capsule'))
        new=hosted.preparation_command('b3-p31-v14-new',Path('archives'),Path('capsule'))
        self.assertEqual(Path(old[3]).name,'prepare_missing_count.py')
        self.assertEqual(Path(new[3]).name,'prepare_b3_v14_epoch_2026_10_22.py')
        self.assertIn('archives\\cutoff25_20261011.zip'if hosted.sys.platform=='win32'else'archives/cutoff25_20261011.zip',old)
        self.assertEqual(new[new.index('--index')+1],'31')
        self.assertIn('--base13-archive',new)

    def test_discovery_preserves_api_and_untrusted_resume(self):
        command=hosted.discovery_command('b3-p32-v14-new',Path('capsule'),1800,Path('candidate.json'))
        self.assertEqual(Path(command[3]).name,'discover_count.py')
        self.assertEqual(command[command.index('--design-sha256')+1],hosted.TARGETS['b3-p32-v14-new'][2])
        self.assertEqual(command[command.index('--resume')+1],'candidate.json')
        self.assertEqual(command[command.index('--order')+1],'root-first')
        self.assertEqual(command[command.index('--alpha-priority')+1],'4')
        for invalid in(True,0,7201,10800):
            with self.assertRaises(ValueError):hosted.discovery_command('b4-q0',Path('capsule'),invalid)

    def test_partial_is_never_accepted(self):
        value=dict(status='SEARCH_CHECKPOINTED_INCOMPLETE',arithmetic_accepted=False,nodes=26,leaves=0,pending=26)
        self.assertFalse(hosted.validate_slice(value))
        for change in(lambda x:x.update(arithmetic_accepted=True),lambda x:x.update(pending=0),
                      lambda x:x.update(nodes=True),lambda x:x.update(all_index_conclusion_verified=True),
                      lambda x:x.update(status='CANDIDATE_COMPLETE_NOT_ACCEPTED')):
            bad=deepcopy(value);change(bad)
            with self.assertRaises(ValueError):hosted.validate_slice(bad)

    def test_native_accept_requires_full_literal_census(self):
        value=dict(status='NATIVE_COUNT_ACCEPTED',arithmetic_accepted=True,nodes=26,leaves=26,pending=0,
                   all_index_conclusion_verified=False)
        self.assertTrue(hosted.validate_slice(value))
        for change in(lambda x:x.update(leaves=True),lambda x:x.update(pending=1),
                      lambda x:x.update(arithmetic_accepted=False),lambda x:x.update(nodes=25)):
            bad=deepcopy(value);change(bad)
            with self.assertRaises(ValueError):hosted.validate_slice(bad)

    def test_no_math_acceptance_for_arbitrary_receipt_path(self):
        value=dict(status='NATIVE_COUNT_ACCEPTED',arithmetic_accepted=True,nodes=26,leaves=26,pending=0,
            native_receipt='outside/COUNT31_ACCEPTED.json',work='outside')
        with self.assertRaises(ValueError):hosted.acceptance_summary('b3-p31-v14-new',value)

    def test_budget_allocation_uses_unchanged_small_slices(self):
        remaining=hosted.SEARCH_MAX;requests=[]
        while remaining:
            request=min(remaining,1800);requests.append(request);remaining-=request
        self.assertEqual(requests,[1800]*6)
        self.assertEqual(sum(requests),10800)
        self.assertEqual(hosted.BRANCH_SECONDS,19800)
        self.assertEqual(hosted.ACCEPT_SECONDS,7200)

    def test_two_original_source_archives_are_pinned_not_proof_inputs(self):
        self.assertEqual([e['name']for e in hosted.ASSETS],['cutoff25_20261011.zip','cutoff25_20261013.zip'])
        self.assertEqual(sum(e['bytes']for e in hosted.ASSETS),1044516490)
        self.assertTrue(all(len(e['sha256'])==64 for e in hosted.ASSETS))


if __name__=='__main__':unittest.main()
