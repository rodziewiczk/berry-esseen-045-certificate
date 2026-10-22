"""Serial284-job native count queue with bounded branches and resumable receipts.

Only an observed, successful invocation of the frozen one-job controller may
add a completion. Host-RAM interruptions discard that attempt and wait/retry;
native rejection, source changes and branch quota/CPU/memory failures stop
closed. Resume revalidates saved execution records/artifacts; checkpoint files
are not advertised as adversarially authenticated execution histories.
No support/resource/global C_n or all-index theorem is claimed.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import sys
import time
import uuid

if not __package__:sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from reproduction.all_indices.c5_counts import BASE,digest,need,unique
from reproduction.all_indices.supervised import run_recorded
from reproduction.continuations.archive_guard import install,HostRAMUnavailable,HOST_RAM_MESSAGE,MIB
from reproduction.continuations.catalog import Sources,CUTOFF6,COMBINED,FINAL_SHA
from reproduction.continuations.count_catalog import CountJob,count_jobs,acceptance_schema
from reproduction.continuations.count_replay import same,validate_result,verify_capsule

sys.dont_write_bytecode = True
SCHEMA = 'SERIAL_NATIVE_CONTINUATION_COUNTS6_9_V1'
LAUNCH_RAM_MESSAGE = 'Launch requires TWO available1536MiB readings5s apart'
LEGACY_RAM_MESSAGE = 'Available host RAM below768MiB: no success result'


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def stamp():return datetime.now(timezone.utc).isoformat()


def regular(root,path,*,directory=False):
    root,path = Path(root).absolute(),Path(path).absolute()
    need(path.is_relative_to(root) and '..' not in path.relative_to(root).parts,'Owned batch artifact path')
    for item in (root,*[root.joinpath(*path.relative_to(root).parts[:i]) for i in range(1,len(path.relative_to(root).parts)+1)]):
        value = item.lstat()
        need(not stat.S_ISLNK(value.st_mode) and not(getattr(value,'st_file_attributes',0)&0x400),
             'No batch artifact symlink/reparse point')
    need(path.is_dir() if directory else path.is_file(),'Regular batch artifact exists')
    need(path.resolve().is_relative_to(root.resolve()),'Resolved batch artifact contained')
    return path


def read(root,path,pin=None):
    path = regular(root,path)
    need(path.stat().st_size <= 16*MIB,'Bounded metadata/checkpoint JSON; never read a forest here')
    before = digest(path);need(pin is None or pin == before,'Exact saved artifact identity')
    value = json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    need(digest(path) == before,'Unchanged artifact while reading')
    return value


@contextmanager
def exclusive_queue(run):
    """OS lock auto-releases on process exit; never kill a PID to reclaim a lock."""
    path = run/'QUEUE.lock'
    if path.exists():regular(run,path)
    stream = path.open('a+b')
    try:
        if stream.seek(0,2) == 0:stream.write(b'0');stream.flush()
        stream.seek(0)
        if sys.platform == 'win32':
            import msvcrt
            try:msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            except OSError as exc:raise ValueError('This exact queue is already owned by a live controller') from exc
        else:
            import fcntl
            try:fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError as exc:raise ValueError('This exact queue is already owned by a live controller') from exc
        yield
    finally:
        # Closing also releases the lock, including when acquisition failed.
        stream.close()


def save(run,state,event):
    state['updated_utc'] = stamp()
    event = dict(event=event,time_utc=state['updated_utc'],status=state['status'],
                 job_id=state.get('current_job'),completed=len(state.get('completed',[])))
    journal = run/'JOURNAL.jsonl'
    if journal.exists():regular(run,journal)
    with journal.open('a',encoding='utf-8') as stream:
        stream.write(json.dumps(event,separators=(',',':'))+'\n');stream.flush()
    temporary = run/('CHECKPOINT-writing-'+uuid.uuid4().hex+'.json')
    with temporary.open('x',encoding='utf-8') as stream:json.dump(state,stream,indent=2)
    destination = run/'CHECKPOINT.json'
    if destination.exists():regular(run,destination)
    temporary.replace(destination)


def is_ram_interruption(error,stderr=''):
    """Only exact guard failures retry; a generic failure during low RAM does not."""
    if isinstance(error,HostRAMUnavailable):return True
    if type(error) is ValueError and str(error) in (HOST_RAM_MESSAGE,LEGACY_RAM_MESSAGE,LAUNCH_RAM_MESSAGE):return True
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    return bool(lines and lines[-1] in tuple('CONTINUATION_NATIVE_COUNT_INCOMPLETE: '+message
                for message in (HOST_RAM_MESSAGE,LEGACY_RAM_MESSAGE,LAUNCH_RAM_MESSAGE)))


def wait_launch(runner,waiting,*,sleep=time.sleep):
    while True:
        try:runner.launch_gate();return
        except Exception as error:
            if not is_ram_interruption(error):raise
            waiting(str(error));sleep(5)


def code_pins():
    relative = ('reproduction/continuations/batch_counts.py','reproduction/continuations/count_replay.py',
        'reproduction/continuations/count_catalog.py','reproduction/continuations/catalog.py',
        'reproduction/continuations/archive_guard.py','reproduction/all_indices/c5_counts.py',
        'reproduction/all_indices/c5_inputs.py','reproduction/all_indices/stable_guard.py',
        'reproduction/all_indices/supervised.py','run_reproduction.py')
    return {name:digest(BASE/name) for name in relative}


def verify_code(pins):
    need(all(digest(BASE/name) == pin for name,pin in pins.items()),'Frozen batch/one-job/guard implementation sources')


def normalize_job(value):
    args = dict(value)
    args['command'] = tuple(args['command']);args['band_rho'] = tuple(args['band_rho'])
    return CountJob(**args)


def check_completion(event,expected,*,started_event=None):
    """Metadata/binding validation after this controller observed successful execution."""
    work_root = BASE/'work'
    need(event.get('event') == 'native_continuation_count_finished' and event.get('job_id') == expected['job_id'],
         'One exact completed native count job event')
    report_path = regular(work_root,Path(event['report']))
    epoch = report_path.parent
    need(epoch.parent.resolve() == work_root.resolve() and epoch.name.startswith('c69-')
         and report_path.name == 'FRESH_NATIVE_COUNT_RESULT.json','Actual private one-job result namespace')
    if started_event is not None:
        need(started_event.get('job_id') == expected['job_id']
             and Path(started_event['work']).resolve() == epoch.resolve(),'Observed start/finish share the new exact private epoch')
    report = read(epoch,report_path,event['sha256'])
    need(report['schema'] == 'FRESH_NATIVE_CONTINUATION_COUNT_ARITHMETIC_V1'
         and report['scope'] == 'COMPLETE_UNCHANGED_NATIVE_COUNT_ARITHMETIC_ONLY_RESOURCE_PARENTS_NOT_DISCHARGED'
         and same(report['job'],expected),'Exact conditional one-job controller report')
    for key,value in (('unchanged_native_checker',True),('source_port_used',False),('old_own_acceptance_copied',False),
                      ('execution_observed_by_this_controller',True),('fresh_count_arithmetic',True),
                      ('fresh_parent_fact_joins_verified',False),('any_global_Cn_conclusion_verified',False),
                      ('all_index_conclusion_verified',False)):
        need(report.get(key) is value,'No promoted or weakened one-job scope: '+key)
    need(report['original_source_composer_sha256'] == FINAL_SHA
         and report['source_assets_sha256'] == {CUTOFF6.name:CUTOFF6.sha256,COMBINED.name:COMBINED.sha256},
         'Exact original composer and both source assets')
    expected_adapters = {name:digest(BASE/'reproduction/continuations'/name)
                         for name in ('count_replay.py','count_catalog.py','catalog.py','archive_guard.py')}
    need(report['adapter_files_sha256'] == expected_adapters,'Exact current frozen one-job orchestration helpers')
    job = normalize_job(expected);directory = epoch/'capsule';prefix = job.capsule+'/'
    verify_capsule(directory,report['source_files_sha256'],prefix)
    need(report['source_files_sha256'][prefix+job.forest_name] == job.forest_pin
         and report['source_files_sha256'][prefix+'contract.json'] == job.contract_pin,'Same original candidate inputs')
    output = regular(epoch,Path(report['native_result_path']))
    need(output == directory/job.receipt_name,'Actual unchanged native output file')
    native = read(epoch,output,report['native_result_sha256'])
    declaration = acceptance_schema((directory/'count_protocol.py').read_text(encoding='utf-8'))
    inspection = dict(native_schema=declaration,source_files_sha256=report['source_files_sha256'],old_schema_reference=None)
    facts = validate_result(job,inspection,native)
    need(same(facts,report['facts']),'Entire fresh native census rechecked, not its PASS label')
    capture = regular(epoch,Path(report['capture_path']),directory=True)
    need(capture == epoch/'capture','Actual private native capture')
    metadata = read(epoch,capture/'metadata.json',report['capture_metadata_sha256'])
    need(metadata['command'] == [sys.executable,*job.command]
         and Path(metadata['cwd']).resolve() == directory.resolve()
         and type(metadata['returncode']) is int and metadata['returncode'] == 0,
         'Real unchanged native command/cwd and successful termination')
    need(same(metadata['input_sha256'],report['source_files_sha256'])
         and metadata['native_result_sha256'] == digest(output),'Full native capture input/output bindings')
    for name in ('stdout','stderr'):
        path = regular(epoch,capture/(name+'.txt'))
        need(path.stat().st_size <= 16*MIB and digest(path) == metadata[name+'_sha256'],'Exact bounded native stream capture')
    need((capture/'stderr.txt').stat().st_size == 0,'Native success has empty stderr')
    printed = json.loads((capture/'stdout.txt').read_text(encoding='utf-8'),object_pairs_hook=unique)
    need(same(printed,native),'Whole native JSON was actually captured')
    need(same(read(epoch,directory/'contract.json',job.contract_pin),report['complete_conditional_contract']),
         'Whole unresolved same-law mathematical parent contract remains explicit')
    return dict(job_id=job.job_id,report=str(report_path),sha256=digest(report_path),facts=facts,
                source_port_used=False,fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)


def revalidate_saved(run,state,job_map,*,guard=lambda:None):
    completed = state['completed']
    need(type(completed) is list and len({row['job_id'] for row in completed}) == len(completed),'No duplicate saved completions')
    for row in completed:
        guard()
        need(row['job_id'] in job_map and row.get('observed_successful_wrapper_exit') is True,
             'Saved completion was an explicit prior batch observation')
        observed = row['observed_execution']
        attempt = regular(run,Path(observed['attempt_directory']),directory=True)
        for channel in ('stdout','stderr'):
            log = regular(run,attempt/('attempt.'+channel+'.txt'))
            need(log.stat().st_size <= 16*MIB and digest(log) == observed[channel+'_sha256'],
                 'Saved successful bounded wrapper capture unchanged')
        need((attempt/'attempt.stderr.txt').stat().st_size == 0,'Prior successful wrapper stderr was empty')
        events = json_events((attempt/'attempt.stdout.txt').read_text(encoding='utf-8'))
        starts = [item for item in events if item.get('event') == 'native_continuation_count_started']
        finishes = [item for item in events if item.get('event') == 'native_continuation_count_finished']
        need(len(starts) == len(finishes) == 1 and finishes[0]['report'] == row['report']
             and finishes[0]['sha256'] == row['sha256'],'Saved complete observed wrapper start/finish')
        checked = check_completion(finishes[0],job_map[row['job_id']],started_event=starts[0])
        need(same(checked,{key:row[key] for key in checked}),'Saved numerical completion still bound to the exact same job')
        guard()


def json_events(stdout):
    events = []
    for line in stdout.splitlines():
        try:value = json.loads(line,object_pairs_hook=unique)
        except (ValueError,TypeError):continue
        if type(value) is dict and 'event' in value:events.append(value)
    return events


def failed_stderr(attempt):
    path = attempt/'attempt.failed.stderr.txt'
    if not path.exists():return ''
    regular(attempt,path)
    with path.open('rb') as stream:
        stream.seek(max(0,path.stat().st_size-256*1024))
        return stream.read().decode('utf-8',errors='replace')


def execute_job(runner,run,state,expected,archives,pins):
    job_id = expected['job_id']
    while True:
        state['current_job'] = job_id;state['status'] = 'WAITING_FOR_TWO_LAUNCH_RAM_READINGS'
        save(run,state,'WAITING_FOR_LAUNCH')
        wait_launch(runner,lambda reason:None)
        verify_code(pins)
        attempt = run/'attempts'/(job_id.replace('.','-').lower()+'-'+uuid.uuid4().hex[:12])
        attempt.mkdir(parents=True,exist_ok=False)
        command = [sys.executable,'-B','-S',str(BASE/'reproduction/continuations/count_replay.py'),
            '--cutoff6-archive',archives['cutoff6'],'--combined-archive',archives['combined'],'--job',job_id]
        record = dict(job_id=job_id,attempt_directory=str(attempt),command=command,started_utc=stamp())
        state['status'] = 'RUNNING_ONE_NATIVE_COUNT';state['current_attempt'] = record
        save(run,state,'NATIVE_ATTEMPT_STARTED')
        try:
            stdout = run_recorded(runner,command,attempt,'attempt',7260,512*MIB)
            # The unchanged runner requires empty stderr but only saves stdout.
            # Persist that already observed empty channel, never invent it on failure.
            with (attempt/'attempt.stderr.txt').open('xb'):pass
            verify_code(pins)
            events = json_events(stdout)
            starts = [item for item in events if item.get('event') == 'native_continuation_count_started']
            finishes = [item for item in events if item.get('event') == 'native_continuation_count_finished']
            need(len(starts) == len(finishes) == 1,'Exactly one newly observed native wrapper start and finish')
            checked = check_completion(finishes[0],expected,started_event=starts[0])
            runner.parent_guard(work=run)
            record.update(finished_utc=stamp(),observed_wrapper_returncode=0,
                stdout_sha256=digest(attempt/'attempt.stdout.txt'),stderr_sha256=digest(attempt/'attempt.stderr.txt'))
            checked.update(observed_successful_wrapper_exit=True,observed_execution=record)
            state['completed'].append(checked);state['attempts'].append(dict(record,outcome='OBSERVED_NATIVE_COUNT_ACCEPTED'))
            state.pop('current_attempt',None);state['status'] = 'COMPLETED_ONE_NATIVE_COUNT'
            save(run,state,'NATIVE_COUNT_ACCEPTED')
            print(json.dumps(dict(event='serial_count_accepted',job_id=job_id,completed=len(state['completed']),
                total=284,fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)),flush=True)
            return
        except Exception as error:
            retry = is_ram_interruption(error,failed_stderr(attempt))
            record.update(finished_utc=stamp(),error=str(error),outcome='HOST_RAM_INTERRUPTED_NO_ACCEPTANCE' if retry else 'FAILED_CLOSED_NO_ACCEPTANCE')
            state['attempts'].append(record);state.pop('current_attempt',None)
            state['status'] = 'WAITING_AFTER_HOST_RAM_INTERRUPTION' if retry else 'STOPPED_FAIL_CLOSED'
            save(run,state,'HOST_RAM_RETRY' if retry else 'NATIVE_OR_INTEGRITY_FAILURE')
            if not retry:raise
            print(json.dumps(dict(event='serial_count_waiting_for_ram',job_id=job_id,
                reason=str(error),completed=len(state['completed']),all_index_conclusion_verified=False)),flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cutoff6-archive',type=Path,required=True)
    parser.add_argument('--combined-archive',type=Path,required=True)
    parser.add_argument('--resume',type=Path,help='Exact prior CHECKPOINT.json from this queue')
    args = parser.parse_args()
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary Python -B')
    spec = importlib.util.spec_from_file_location('serial_native_count_batch_guard',BASE/'run_reproduction.py')
    runner = importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024*MIB;install(runner);runner.verify_sources()
    need(runner.NATIVE is not None,
         'Serial numerical batch requires the Windows whole-process-tree Job guard')
    pins = code_pins();archives = {'cutoff6':str(args.cutoff6_archive.resolve()),'combined':str(args.combined_archive.resolve())}
    work = (BASE/'work').resolve()
    need(work.parent == BASE.resolve() and not (BASE/'work').is_symlink(),'Owned regular batch work root')
    work.mkdir(exist_ok=True)
    if args.resume:
        checkpoint = regular(work,args.resume.resolve());run = checkpoint.parent
        need(run.parent == work and run.name.startswith('c69batch-') and checkpoint.name == 'CHECKPOINT.json','Exact private batch checkpoint')
        state = read(run,checkpoint)
        need(state.get('schema') == SCHEMA and same(state['implementation_sources_sha256'],pins)
             and state['source_assets_sha256'] == {CUTOFF6.name:CUTOFF6.sha256,COMBINED.name:COMBINED.sha256},
             'Resume only the same source-pinned queue and assets')
    else:
        run = work/('c69batch-'+uuid.uuid4().hex[:12]);run.mkdir(exist_ok=False)
        state = dict(schema=SCHEMA,scope='SERIAL_COUNT_ARITHMETIC_ONLY_NOT_GLOBAL_PROOF',status='STARTING',
            created_utc=stamp(),implementation_sources_sha256=pins,
            source_assets_sha256={CUTOFF6.name:CUTOFF6.sha256,COMBINED.name:COMBINED.sha256},
            completed=[],attempts=[],fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)
    with exclusive_queue(run):
        original_guard = runner.parent_guard
        def full_batch_guard(tiny=False,work=None):
            return original_guard(tiny=tiny,work=run if work is not None else None)
        runner.parent_guard = full_batch_guard
        save(run,state,'QUEUE_OPENED')
        print(json.dumps(dict(event='serial_count_queue_opened',checkpoint=str(run/'CHECKPOINT.json'),
            completed=len(state['completed']),total=284,all_index_conclusion_verified=False)),flush=True)
        while True:
            try:
                wait_launch(runner,lambda reason:None)
                with Sources(archives['cutoff6'],archives['combined'],guard=runner.parent_guard) as sources:
                    jobs,graph = count_jobs(sources)
                    catalog = json.loads(json.dumps([asdict(job) for job in jobs]))
                del graph
                runner.parent_guard();break
            except Exception as error:
                if not is_ram_interruption(error):raise
                state['status'] = 'WAITING_FOR_RAM_DURING_SOURCE_CATALOG';save(run,state,'SOURCE_CATALOG_RAM_WAIT')
                time.sleep(5)
        if 'catalog_sha256' in state:need(state['catalog_sha256'] == canonical_sha(catalog),'Exactly the same284 selected jobs on resume')
        state['catalog_sha256'] = canonical_sha(catalog);state['job_ids'] = [row['job_id'] for row in catalog]
        need(len(catalog) == len(set(state['job_ids'])) == 284,'All284 original source-selected jobs')
        while True:
            try:
                verify_code(pins)
                revalidate_saved(run,state,{row['job_id']:row for row in catalog},guard=runner.parent_guard)
                runner.parent_guard(work=run);break
            except Exception as error:
                if not is_ram_interruption(error):raise
                state['status'] = 'WAITING_FOR_RAM_DURING_RESUME_REVALIDATION'
                save(run,state,'RESUME_REVALIDATION_RAM_WAIT');time.sleep(5)
        finished = {row['job_id'] for row in state['completed']}
        for expected in catalog:
            if expected['job_id'] not in finished:execute_job(runner,run,state,expected,archives,pins)
        need(len(state['completed']) == len({row['job_id'] for row in state['completed']}) == 284,'Every distinct native job observed accepted')
        runner.parent_guard(work=run)
        state['status'] = 'ALL284_NATIVE_COUNT_ARITHMETIC_ACCEPTED_PARENTS_STILL_OPEN';state['current_job'] = None
        save(run,state,'ALL_SELECTED_COUNT_ARITHMETIC_FINISHED')
        print(json.dumps(dict(event='serial_counts_finished',checkpoint=str(run/'CHECKPOINT.json'),
            completed=284,fresh_parent_fact_joins_verified=False,any_global_Cn_conclusion_verified=False,
            all_index_conclusion_verified=False)),flush=True)


if __name__ == '__main__':
    try:main()
    except Exception as exc:
        print('SERIAL_NATIVE_COUNTS_STOPPED_FAIL_CLOSED: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
