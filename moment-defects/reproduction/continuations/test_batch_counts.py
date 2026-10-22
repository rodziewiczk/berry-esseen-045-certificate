from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from . import batch_counts as batch
from .archive_guard import HostRAMUnavailable,HOST_RAM_MESSAGE,MIB


class ResourceRetryPolicyTests(unittest.TestCase):
    def test_only_exact_host_resource_guards_retry(self):
        self.assertTrue(batch.is_ram_interruption(HostRAMUnavailable(HOST_RAM_MESSAGE)))
        self.assertTrue(batch.is_ram_interruption(ValueError(batch.LAUNCH_RAM_MESSAGE)))
        self.assertTrue(batch.is_ram_interruption(ValueError('wrapper exit'),
            'CONTINUATION_NATIVE_COUNT_INCOMPLETE: '+HOST_RAM_MESSAGE+'\n'))
        for error,stderr in ((ValueError('Whole owned Job CPU/active peak-memory bound'),''),
            (ValueError('fresh leaf must close'),''),
            (ValueError('wrapper exit'),'ValueError: numerical rejection while RAM is low\n'),
            (ValueError('wrapper exit'),'prefix '+HOST_RAM_MESSAGE+'\n')):
            with self.subTest(error=error,stderr=stderr):self.assertFalse(batch.is_ram_interruption(error,stderr))

    def test_two_failed_host_gates_wait_then_retry_not_abort(self):
        calls,sleeps,waits = [],[],[]
        def gate():
            calls.append(1)
            if len(calls) < 3:raise HostRAMUnavailable(HOST_RAM_MESSAGE)
        batch.wait_launch(SimpleNamespace(launch_gate=gate),waits.append,sleep=sleeps.append)
        self.assertEqual(len(calls),3);self.assertEqual(sleeps,[5,5]);self.assertEqual(len(waits),2)

    def test_non_ram_gate_failure_stops_closed(self):
        def gate():raise ValueError('source hash changed')
        with self.assertRaisesRegex(ValueError,'source hash'):
            batch.wait_launch(SimpleNamespace(launch_gate=gate),lambda reason:None,sleep=lambda seconds:None)


class SerialBatchFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name);self.state = dict(status='STARTING',completed=[],attempts=[])
        self.expected = dict(job_id='n7.B0.p37')
        self.runner = SimpleNamespace(launch_gate=lambda:None,parent_guard=lambda **kwargs:None)
        self.archives = dict(cutoff6='exact-six.zip',combined='exact-combined.zip')

    def test_ram_interruption_retries_with_unique_logs_then_one_acceptance(self):
        calls = []
        started = dict(event='native_continuation_count_started',job_id=self.expected['job_id'],work='private-fresh-epoch')
        finished = dict(event='native_continuation_count_finished',job_id=self.expected['job_id'],report='new-report',sha256='1'*64)
        output = json.dumps(started)+'\n'+json.dumps(finished)+'\n'
        def native(runner,command,attempt,label,cpu_limit,memory_limit):
            calls.append((attempt,cpu_limit,memory_limit))
            if len(calls) == 1:raise HostRAMUnavailable(HOST_RAM_MESSAGE)
            (attempt/'attempt.stdout.txt').write_text(output,encoding='utf-8')
            return output
        checked = dict(job_id=self.expected['job_id'],report='new-report',sha256='1'*64,
                       fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)
        with patch.object(batch,'run_recorded',side_effect=native),patch.object(batch,'verify_code'), \
             patch.object(batch,'check_completion',return_value=checked):
            batch.execute_job(self.runner,self.run,self.state,self.expected,self.archives,{})
        self.assertEqual(len(calls),2);self.assertNotEqual(calls[0][0],calls[1][0])
        self.assertTrue(all(cpu == 7260 and memory == 512*MIB for _,cpu,memory in calls))
        self.assertEqual(len(self.state['completed']),1)
        self.assertEqual(self.state['attempts'][0]['outcome'],'HOST_RAM_INTERRUPTED_NO_ACCEPTANCE')
        self.assertTrue(self.state['completed'][0]['observed_successful_wrapper_exit'])
        self.assertFalse(self.state['completed'][0]['fresh_parent_fact_joins_verified'])

    def test_native_rejection_stops_without_retry_or_acceptance(self):
        with patch.object(batch,'run_recorded',side_effect=ValueError('fresh leaf must close')) as native, \
             patch.object(batch,'verify_code'):
            with self.assertRaisesRegex(ValueError,'fresh leaf'):
                batch.execute_job(self.runner,self.run,self.state,self.expected,self.archives,{})
        self.assertEqual(native.call_count,1);self.assertEqual(self.state['completed'],[])
        self.assertEqual(self.state['status'],'STOPPED_FAIL_CLOSED')
        self.assertEqual(self.state['attempts'][0]['outcome'],'FAILED_CLOSED_NO_ACCEPTANCE')

    def test_successful_exit_without_both_new_events_is_not_acceptance(self):
        def native(runner,command,attempt,*unused):
            (attempt/'attempt.stdout.txt').write_text('PASS_OLD\n',encoding='utf-8');return 'PASS_OLD\n'
        with patch.object(batch,'run_recorded',side_effect=native),patch.object(batch,'verify_code'):
            with self.assertRaisesRegex(ValueError,'newly observed'):
                batch.execute_job(self.runner,self.run,self.state,self.expected,self.archives,{})
        self.assertEqual(self.state['completed'],[]);self.assertEqual(self.state['status'],'STOPPED_FAIL_CLOSED')

    def test_atomic_checkpoint_and_lock_are_private_recoverable_records(self):
        batch.save(self.run,self.state,'ONE');self.state['status'] = 'WAITING';batch.save(self.run,self.state,'TWO')
        saved = json.loads((self.run/'CHECKPOINT.json').read_text(encoding='utf-8'))
        self.assertEqual(saved['status'],'WAITING')
        self.assertEqual(len((self.run/'JOURNAL.jsonl').read_text().splitlines()),2)
        self.assertEqual(list(self.run.glob('CHECKPOINT-writing-*')),[])
        with batch.exclusive_queue(self.run):
            with self.assertRaises(ValueError):
                with batch.exclusive_queue(self.run):pass
        with batch.exclusive_queue(self.run):pass

    def test_saved_pass_or_duplicate_job_cannot_be_resumed_as_an_observation(self):
        state = dict(completed=[dict(job_id='n7.B0.p37',observed_successful_wrapper_exit=False)])
        with self.assertRaisesRegex(ValueError,'prior batch observation'):
            batch.revalidate_saved(self.run,state,{'n7.B0.p37':self.expected})
        state = dict(completed=[dict(job_id='n7.B0.p37'),dict(job_id='n7.B0.p37')])
        with self.assertRaisesRegex(ValueError,'duplicate'):
            batch.revalidate_saved(self.run,state,{'n7.B0.p37':self.expected})


if __name__ == '__main__':unittest.main()
