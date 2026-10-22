from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import re
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from . import hosted_c5 as hosted


def manifest():
    return dict(schema='berry-esseen-source-archives-v1',repository='rodziewiczk/berry-esseen-045-certificate',
        release_tag='cutoff5-sources-2026-10-20',archives=[
            dict(name=hosted.ARCHIVE,bytes=hosted.ARCHIVE_BYTES,sha256=hosted.ARCHIVE_SHA),
            dict(name='cutoff6_20261020.zip',bytes=1,sha256='0'*64)])


def owncaps():
    return dict(status='FRESH_COARSE_AND_SELECTED_OWNCAPS_ACCEPTED',fresh_arithmetic=True,
        receipts=[dict(variant='owncaps5_v3'),dict(variant='owncap_B3_ext_v1')],
        coarse_429=dict(fresh_arithmetic=True),all_index_conclusion_verified=False)


class SourceAndScopeTests(unittest.TestCase):
    def test_fetch_selects_only_hardcoded_c5_asset_not_all_manifest_entries(self):
        selected = hosted.selected_asset(manifest())
        self.assertEqual(selected['name'],hosted.ARCHIVE)
        for key,value in (('sha256','0'*64),('bytes',hosted.ARCHIVE_BYTES+1),('bytes',float(hosted.ARCHIVE_BYTES))):
            bad = manifest();bad['archives'][0][key] = value
            with self.subTest(key=key),self.assertRaises(ValueError):hosted.selected_asset(bad)
        bad = manifest();bad['repository'] = 'arbitrary/fetch'
        with self.assertRaises(ValueError):hosted.selected_asset(bad)

    def test_exact_stage_choices_use_existing_native_adapters_without_edits(self):
        self.assertEqual(set(hosted.STAGES),{'owncaps','initial','resources','complement','counts','support','high'})
        for stage,filename in hosted.STAGES.items():
            command = hosted.stage_command(stage,Path('pinned-cache'),Path('pinned-source.zip'))
            self.assertEqual(command[1:3],['-B','-S']);self.assertTrue(command[3].endswith(filename))
            self.assertEqual(command[4],'--archive' if stage == 'counts' else '--cache')
            self.assertNotIn('--inspect',command)
        with self.assertRaises(ValueError):hosted.stage_command('all',Path('cache'),Path('source'))

    def test_old_pass_source_inspection_or_global_flag_cannot_finish_stage(self):
        hosted.stage_summary('owncaps',json.dumps(owncaps()))
        for change in (lambda result:result.update(status='PASS_OLD'),lambda result:result.update(fresh_arithmetic=False),
                       lambda result:result.update(all_index_conclusion_verified=True),lambda result:result['receipts'].pop()):
            result = owncaps();change(result)
            with self.subTest(change=change),self.assertRaises(ValueError):hosted.stage_summary('owncaps',json.dumps(result))

    def test_complete_initial_resource_and_count_censuses_are_literal(self):
        initial = dict(scope='FRESH_INITIAL_ARITHMETIC_BATCH_NOT_ACQUIRED_C5_THEOREM',jobs_recomputed=12,
                       reports=[{}]*12,fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)
        resources = dict(scope='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY',selected_jobs=15,complete_15_job_arithmetic=True,
            jobs=[{}]*15,resource_probability_panel_obligations=1200,fresh_parent_fact_joins_verified=False,
            register_as_c5_resources=False,all_index_conclusion_verified=False)
        counts = dict(scope='ALL_295_C5_COUNT_FORESTS_FRESHLY_REPLAYED',forests=295,original_count_roots=1770,
            nodes=148586,leaves=75178,resource_support_fourier_initial_and_gapfree_verified_by_this_stage=False,
            all_index_conclusion_verified=False)
        for stage,result,key in (('initial',initial,'jobs_recomputed'),('resources',resources,'selected_jobs'),('counts',counts,'leaves')):
            hosted.stage_summary(stage,json.dumps(result));bad = deepcopy(result);bad[key] = float(result[key])
            with self.subTest(stage=stage),self.assertRaises(ValueError):hosted.stage_summary(stage,json.dumps(bad))


class GuardedHostedFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name);self.run = self.root/'work'/'private';self.run.mkdir(parents=True)
        self.runner = SimpleNamespace(HOST_FLOOR=0,parent_guard=lambda **kwargs:None,verify_sources=lambda:None,
            private_work=lambda:self.run,launch_gate=lambda:None)
        self.spec = SimpleNamespace(loader=SimpleNamespace(exec_module=lambda module:None))

    def test_download_prep_and_math_are_three_separate_original_guarded_children(self):
        calls = []
        def recorded(runner,command,work,label,cpu,memory):
            calls.append((command,label,cpu,memory))
            packet = owncaps() if label == 'arithmetic' else (
                dict(scope='COMPLETE_PINNED_C5_INPUTS_PREPARED_ONLY',arithmetic_replayed=False) if label == 'prepare' else {})
            stdout = json.dumps(packet)+'\n';(work/(label+'.stdout.txt')).write_text(stdout,encoding='utf-8');return stdout
        with patch.object(hosted,'BASE',self.root),patch.object(hosted.sys,'platform','win32'), \
             patch.object(hosted.importlib.util,'spec_from_file_location',return_value=self.spec), \
             patch.object(hosted.importlib.util,'module_from_spec',return_value=self.runner), \
             patch.object(hosted,'install'),patch.object(hosted,'implementation_pins',return_value={}), \
             patch.object(hosted,'verify_implementation'),patch.object(hosted,'run_recorded',side_effect=recorded):
            hosted.execute('owncaps')
        self.assertEqual([call[1] for call in calls],['fetch','prepare','arithmetic'])
        self.assertEqual([call[2] for call in calls],[600,3600,19800])
        self.assertTrue(all(call[3] == 512*hosted.MIB for call in calls))
        self.assertIn('--internal-fetch',calls[0][0]);self.assertTrue(calls[1][0][3].endswith('c5_inputs.py'))
        self.assertTrue(calls[2][0][3].endswith('c5_owncaps_one.py'))
        result = json.loads((self.run/'HOSTED_STAGE_RESULT.json').read_text())
        self.assertTrue(result['execution_observed_by_this_controller'])
        self.assertFalse(result['fresh_parent_fact_joins_verified']);self.assertFalse(result['all_index_conclusion_verified'])

    def test_failure_records_diagnostics_but_never_stage_acceptance(self):
        with patch.object(hosted,'BASE',self.root),patch.object(hosted.sys,'platform','win32'), \
             patch.object(hosted.importlib.util,'spec_from_file_location',return_value=self.spec), \
             patch.object(hosted.importlib.util,'module_from_spec',return_value=self.runner), \
             patch.object(hosted,'install'),patch.object(hosted,'implementation_pins',return_value={}), \
             patch.object(hosted,'verify_implementation'),patch.object(hosted,'run_recorded',side_effect=ValueError('native rejected')):
            with self.assertRaisesRegex(ValueError,'native rejected'):hosted.execute('counts')
        self.assertFalse((self.run/'HOSTED_STAGE_RESULT.json').exists())
        failure = json.loads((self.run/'HOSTED_STAGE_FAILURE.json').read_text())
        self.assertEqual(failure['status'],'INCOMPLETE_NO_COMPONENT_ACCEPTANCE')
        self.assertFalse(failure['execution_observed_by_this_controller'])


class BoundedArtifactsTests(unittest.TestCase):
    def test_public_work_and_logs_only_no_hidden_credentials_archives_or_large_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary);work = root/'work';work.mkdir();(work/'proof.json').write_text('{}')
            (work/'stage.log').write_text('ok');(work/'.env').write_text('PRIVATE_SECRET')
            (work/'credential.pem').write_text('PRIVATE_SECRET');(work/'source.zip').write_bytes(b'not-an-artifact')
            (work/'big.txt').write_bytes(b'x'*17)
            (work/'.git').mkdir();(work/'.git'/'config').write_text('PRIVATE_SECRET')
            with patch.object(hosted,'BASE',root),patch.object(hosted,'ARTIFACT_FILE_LIMIT',16):
                destination = hosted.collect_artifacts()
            collected = json.loads((destination/'COLLECTION.json').read_text())
            self.assertEqual({item['path'] for item in collected['files']},{'work/proof.json','work/stage.log'})
            self.assertFalse(collected['all_index_conclusion_verified'])
            for path in destination.rglob('*'):
                if path.is_file():self.assertNotIn(b'PRIVATE_SECRET',path.read_bytes())

    def test_total_artifact_budget_and_copy_growth_shrink_guards(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary);work = root/'work';work.mkdir()
            (work/'a.txt').write_bytes(b'123456');(work/'b.txt').write_bytes(b'123456')
            with patch.object(hosted,'BASE',root),patch.object(hosted,'ARTIFACT_LIMIT',10):destination = hosted.collect_artifacts()
            collected = json.loads((destination/'COLLECTION.json').read_text())
            self.assertEqual(collected['bytes'],6);self.assertEqual(len(collected['files']),1)
        for raw,size in ((b'ab',3),(b'abcd',3)):
            target = BytesIO()
            with self.subTest(raw=raw),self.assertRaises(ValueError):hosted.bounded_copy(BytesIO(raw),target,size)
            self.assertLessEqual(len(target.getvalue()),size)

    def test_workflow_is_manual_pinned_windows_and_preserves_failed_outputs(self):
        root = Path(__file__).resolve().parents[2]
        source = (root/'.github/workflows/c5-native-replay.yml').read_text(encoding='utf-8')
        self.assertIn('workflow_dispatch:',source);self.assertNotIn('  push:',source);self.assertNotIn('pull_request:',source)
        self.assertIn('runs-on: windows-2022',source);self.assertIn('timeout-minutes: 355',source)
        self.assertIn('timeout-minutes: 330',source);self.assertGreaterEqual(source.count('if: always()'),2)
        self.assertEqual(set(re.findall(r'^          - (\w+)$',source,flags=re.M)),set(hosted.STAGES))
        for action in ('actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5',
                       'actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065',
                       'actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02'):
            self.assertIn(action,source)
        self.assertIn('persist-credentials: false',source)


if __name__ == '__main__':unittest.main()
