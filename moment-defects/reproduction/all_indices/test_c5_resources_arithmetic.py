"""Bounded metadata/control-plane tests; no resource or numerical oracle runs."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from . import c5_resource_accept_port as port
from . import c5_resources_arithmetic as arithmetic
from .c5_acquisition_plan import RESOURCE_JOBS, INITIAL_JOBS


class ResourcePortTests(unittest.TestCase):
    def test_arithmetic_source_edit_is_not_whitelisted(self):
        with self.assertRaises(ValueError):
            port.transform(b'target=1\n','resource5_selected_accept_v1','replay')

    def test_only_metadata_source_keys_change(self):
        source=("x=source['files_sha256'].get(str(path.relative_to(R)))\n"
                "source['files_sha256'].pop(str(path.relative_to(R)))\n"
                "need(m['command'][1:]==['-B','replay.py'],'capture')\n"
                "score=2+3\n")
        tree,edits=port.transform(source.encode(),'resource5_gamma_accept_v1','accept',verify_pin=False)
        import ast
        text=ast.unparse(tree)
        self.assertEqual([e['kind']for e in edits],['get','pop','capture_command'])
        self.assertIn('as_posix()',text);self.assertIn('score = 2 + 3',text)
        self.assertIn('source_semantic_command',text)

    def test_unapproved_extra_source_lookup_rejected(self):
        source=("a['files_sha256'].get(str(p.relative_to(R)))\n"*2+
                "need(m['command'],'capture')\n")
        with self.assertRaises(ValueError):
            port.transform(source.encode(),'resource5_gamma_accept_v1','accept',verify_pin=False)

    def test_nonmetadata_and_nonR_relative_operations_are_not_rewritten(self):
        source=("x=str(path.relative_to(R))\n"
                "x=data['other'].get(str(path.relative_to(R)))\n"
                "x=data['files_sha256'].get(str(path.relative_to(Q)))\n"
                "need(m['command'],'capture')\n")
        tree,edits=port.transform(source.encode(),'resource5_selected_accept_v1','accept',verify_pin=False)
        import ast
        self.assertNotIn('as_posix()',ast.unparse(tree))
        self.assertEqual([e['kind']for e in edits],['capture_command'])

    def test_only_named_initial_reference_writer_changes(self):
        source=b"result=dict(initial_receipt=str(ip.relative_to(R)),other=str(ip.relative_to(R)))\n"
        tree,edits=port.transform(source,'resource5_gamma_accept_v1','replay',verify_pin=False)
        import ast
        text=ast.unparse(tree)
        self.assertIn('initial_receipt=ip.relative_to(R).as_posix()',text)
        self.assertIn('other=str(ip.relative_to(R))',text)
        self.assertEqual(len(edits),1)

    def test_all_ten_available_frozen_source_ports_parse_without_execution(self):
        archive=Path(__file__).resolve().parents[5]/'tmp/drive_2026-10-20/cutoff5_20261020.zip'
        if not archive.exists():self.skipTest('Optional local source asset is not installed')
        prefix='cutoff5_20261020/root/delivery_extract_v1/work/cutoff5_20261020/entry/'
        with zipfile.ZipFile(archive)as source:
            for family in port.PINS:
                for stage in('replay','accept'):
                    raw=source.read(prefix+family+'/'+stage+'.py')
                    tree,edits=port.transform(raw,family,stage)
                    compile(tree,'synthetic-no-execution','exec')
                    self.assertEqual(bool(edits),stage=='accept'or family!='resource5_selected_accept_v1')
                    with self.assertRaises(ValueError):
                        port.transform(raw+b'\nchanged_math=1\n',family,stage)


class ResourceCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.epoch=Path(self.temp.name)
        self.directory=self.epoch/'work/case';self.directory.mkdir(parents=True)
        self.adapter=self.epoch/'port.py';self.adapter.write_bytes(b'# synthetic adapter\n')
        self.script=self.directory/'replay.py';self.script.write_bytes(b'# synthetic replay\n')
        self.script_pin=port.digest(self.script)
        self.result=self.directory/'REPLAY.json';self.result.write_text('{}')
        self.job=dict(directory='work/case',family='synthetic',arguments=['B0'],
                      capture='runs/fresh',outputs=['work/case/REPLAY.json'])
        self.request=dict(job=self.job,adapter_sha256=port.digest(self.adapter),
            source_files_sha256={'work/case/replay.py':self.script_pin})
        self.request_path=self.epoch/'REQUEST.json';self.request_path.write_text(json.dumps(self.request))
        self.request_pin=port.digest(self.request_path)
        report=dict(original_source_sha256=self.script_pin,adapter_sha256=port.digest(self.adapter),
            request_sha256=self.request_pin,stage='replay',original_source_bytes_modified=False,
            exact_ast_transforms=[],old_json_or_hashes_modified=False,
            mathematical_expressions_and_all_native_negative_controls_unchanged=True,
            scope='NEW_METADATA_ONLY_SOURCE_PORT_NOT_UNCHANGED_NATIVE_WINDOWS_EXECUTION')
        (self.epoch/'PORT_REPLAY_REPORT.json').write_text(json.dumps(report))
        self.cap=self.epoch/'runs/fresh';self.cap.mkdir(parents=True)
        (self.cap/'stdout.txt').write_bytes(b'synthetic actual stdout\n')
        (self.cap/'stderr.txt').write_bytes(b'')
        self.meta=dict(returncode=0,changed_inputs=[],
            command=port.worker_command(self.adapter,self.request_path,self.request_pin,'replay'),
            source_semantic_command=[port.sys.executable,'-B','replay.py','B0'],
            source_semantic_command_is_os_command=False,cwd=str(self.directory.resolve()),
            adapter_sha256=port.digest(self.adapter),request_sha256=self.request_pin,
            original_script='work/case/replay.py',original_script_sha256=self.script_pin,
            stdout_sha256=port.digest(self.cap/'stdout.txt'),stderr_sha256=port.digest(self.cap/'stderr.txt'),
            input_sha256={'replay.py':self.script_pin},
            source_port_report_sha256=port.digest(self.epoch/'PORT_REPLAY_REPORT.json'),
            result_sha256=port.digest(self.result))

    def tearDown(self):self.temp.cleanup()

    def check(self,meta):
        (self.cap/'metadata.json').write_text(json.dumps(meta))
        with patch.dict(port.PINS,{'synthetic':(self.script_pin,'unused',(0,0),(0,0))}):
            return port.preflight_capture(self.epoch,self.request,self.request_path,self.request_pin,self.adapter)

    def test_real_command_and_explicit_semantic_command_are_distinct(self):
        self.check(self.meta)
        self.assertNotEqual(self.meta['command'],self.meta['source_semantic_command'])

    def test_every_damaged_actual_capture_is_rejected(self):
        changes=[lambda x:x.update(command=x['source_semantic_command']),
                 lambda x:x.update(source_semantic_command_is_os_command=True),
                 lambda x:x.update(cwd='old/mac/cwd'),lambda x:x.update(returncode=True),
                 lambda x:x.update(input_sha256={}),lambda x:x.update(adapter_sha256='0'*64),
                 lambda x:x.update(original_script_sha256='0'*64),
                 lambda x:x.update(result_sha256='0'*64),
                 lambda x:x.update(source_port_report_sha256='0'*64)]
        for change in changes:
            meta=deepcopy(self.meta);change(meta)
            with self.assertRaises(ValueError):self.check(meta)

    def test_rehashed_nonwhitelisted_source_port_report_is_rejected(self):
        path=self.epoch/'PORT_REPLAY_REPORT.json'
        report=json.loads(path.read_text());report['exact_ast_transforms']=[{'kind':'changed_math'}]
        path.write_text(json.dumps(report))
        meta=deepcopy(self.meta);meta['source_port_report_sha256']=port.digest(path)
        with self.assertRaises(ValueError):self.check(meta)


class ResourceCanonicalFactsTests(unittest.TestCase):
    def setUp(self):
        self.job=RESOURCE_JOBS[0]
        self.replay=dict(n=5,band='B0',status=arithmetic.REPLAY_STATUS[self.job.family][0],
            negative_controls=[str(i)for i in range(23)],
            computed={str(i):dict(excluded=False,result={'D':'1'},history=[])for i in self.job.indices})

    def test_whole_canonical_answers_not_just_flags_are_exported(self):
        rows=arithmetic.replay_rows(self.job,self.replay)
        self.assertEqual(len(rows),91)
        self.assertEqual(rows[0]['result'],self.replay['computed']['0'])
        self.assertEqual(rows[0]['canonical_result_sha256'],arithmetic.canonical_sha(rows[0]['result']))
        self.assertEqual(rows[-1]['p'],['99/100','1'])

    def test_damaged_resource_inventory_is_rejected(self):
        changes=[lambda x:x.update(n=True),lambda x:x['computed'].pop('0'),
            lambda x:x['negative_controls'].pop(),lambda x:x['negative_controls'].__setitem__(0,'1'),
            lambda x:x['computed']['0'].update(excluded=0)]
        for change in changes:
            replay=deepcopy(self.replay);change(replay)
            with self.assertRaises(ValueError):arithmetic.replay_rows(self.job,replay)

    def test_summary_remains_conditional_and_preserves_full_parent_identity(self):
        parent=next(p for p in INITIAL_JOBS if p.job_id==self.job.initial_parent)
        with tempfile.TemporaryDirectory()as directory:
            epoch=Path(directory)
            candidate=epoch/self.job.case_directory/'INITIAL.json'
            candidate.parent.mkdir(parents=True)
            initial=dict(n=5,band='B0',physical_defect_seed=False,failure=None,
                stages=[dict(cover=dict(panels=[{}for _ in range(100)],total=2592,
                    active=2,gap_active=2))for _ in range(parent.stages)],
                profile=dict(n=5,cap=parent.owncap,radius='3'),
                assumed_HIGH=parent.high,final_invariants=dict(D='1/20'))
            candidate.write_text(json.dumps(initial))
            prepared=dict(initial_sha256=port.digest(candidate))
            prepared_path=epoch/self.job.prepared
            prepared_path.parent.mkdir(parents=True,exist_ok=True)
            prepared_path.write_text(json.dumps(prepared))
            for path in self.job.output_paths:
                (epoch/path).write_text('{}')
            replay=deepcopy(self.replay)
            replay.update(initial_receipt='old/INITIAL_CHECKED.json',initial_receipt_sha256='a'*64)
            accepted=dict(status=self.job.expected_status,n=5,band='B0',
                selected=list(self.job.indices),excluded=[],retained=list(self.job.indices),
                negative_controls=[str(i)for i in range(31)],rho_interval=['1','28/25'])
            result=arithmetic.summarize_job(epoch,self.job,prepared,initial,replay,accepted)
            self.assertEqual(result['scope'],'CONDITIONAL_RESOURCE_ARITHMETIC_ONLY')
            self.assertTrue(result['fresh_resource_arithmetic'])
            for key in('fresh_arithmetic','register_as_c5_resources',
                       'fresh_parent_fact_joins_verified','all_index_conclusion_verified'):
                self.assertIs(result[key],False)
            facts=result['parent_initial']
            self.assertEqual(facts['candidate_sha256'],port.digest(candidate))
            self.assertEqual(facts['profile'],initial['profile'])
            self.assertEqual(facts['stages'],parent.stages)
            self.assertEqual(facts['rho_interval'],accepted['rho_interval'])
            self.assertEqual(facts['final_cover_sha256'],
                             arithmetic.canonical_sha(initial['stages'][-1]['cover']))
            self.assertIs(facts['historical_receipt_is_fresh_parent_proof'],False)
            self.assertEqual(result['full_canonical_resource_rows'][0]['result'],
                             replay['computed']['0'])
            for change in(lambda x:x.update(c5_proved=True),
                          lambda x:x['selected'].pop(),
                          lambda x:x['negative_controls'].pop(),
                          lambda x:x.update(excluded=[0],retained=list(self.job.indices)[1:])):
                damaged=deepcopy(accepted);change(damaged)
                with self.assertRaises(ValueError):
                    arithmetic.summarize_job(epoch,self.job,prepared,initial,replay,damaged)


if __name__=='__main__':unittest.main()
