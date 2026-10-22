"""One guarded UNCHANGED native count acceptance, with all roots/24 controls.

The source composer selects284 jobs at n6..9. This command executes one chosen
job, never treats the old PASS as numerical work, and never proves its resource
parent or a global C_n statement. A stored forest is an input candidate; every
leaf is recomputed by the unmodified pinned native count_protocol.py accept.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
from datetime import datetime,timezone
from fractions import Fraction as F
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys
import time
import uuid

if not __package__:sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from reproduction.all_indices.c5_counts import BASE,digest,need,unique
from reproduction.continuations.archive_guard import install
from reproduction.all_indices.supervised import run_recorded
from reproduction.continuations.catalog import Sources,CUTOFF6,COMBINED,FINAL_SHA
from reproduction.continuations.count_catalog import count_jobs,job_sources

sys.dont_write_bytecode = True


def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys() == b.keys() and all(same(a[key],b[key]) for key in a)
    if type(a) is list:return len(a) == len(b) and all(same(x,y) for x,y in zip(a,b))
    return a == b


def validate_result(job,inspection,result):
    declaration = inspection['native_schema'];prefix = job.capsule+'/'
    need(type(result) is dict and sorted(result) == declaration['fields'],'Entire unchanged native acceptance schema')
    for key in ('status','n','index','scope'):
        need(same(result[key],declaration[key]),'Exact literal native writer field: '+key)
    need(result['contract_sha256'] == job.contract_pin and result['forest_sha256'] == job.forest_pin
         and result['checker_sha256'] == inspection['source_files_sha256'][prefix+'count_protocol.py'],
         'Fresh acceptance binds the selected immutable candidate and unchanged checker')
    expected_kernel = {path[len(prefix):]:pin for path,pin in inspection['source_files_sha256'].items()
                       if path[len(prefix):] not in ('KERNEL_COPY_MANIFEST.json','contract.json',job.forest_name,'count_protocol.py')}
    need(same(result['kernel_sha256'],expected_kernel),'Every actual native kernel helper has its original pinned bytes')
    need(same(result['negative_controls'],declaration['controls']),'All24 exact native corruption controls')
    stats = result['statistics']
    need(type(stats) is dict and set(stats) == {'nodes','leaves','closed_statuses','maximum_score','maximum_depth'},
         'Whole original reconstructed forest census')
    for key in ('nodes','leaves','maximum_depth'):
        need(type(stats[key]) is int and stats[key] >= 0,'Literal nonnegative forest census: '+key)
    need(stats['leaves'] >= job.n+1 and stats['nodes'] == 2*stats['leaves']-(job.n+1)
         and stats['maximum_depth'] <= 128,'Every one of the original n+1 roots and both children')
    need(type(result['fresh_leaf_evaluations']) is int and result['fresh_leaf_evaluations'] == stats['leaves'],
         'Every original leaf actually evaluated in this unchanged native acceptance')
    need(type(stats['closed_statuses']) is dict and stats['closed_statuses']
         and all(type(value) is int and value >= 0 for value in stats['closed_statuses'].values())
         and sum(stats['closed_statuses'].values()) == stats['leaves'],'Complete fresh leaf-decision inventory')
    need(type(stats['maximum_score']) is str and F(stats['maximum_score']) < F(job.target),
         'Original strict sharp target, no rounded or weakened substitute')
    need(type(result['seconds']) in (int,float) and math.isfinite(result['seconds']) and result['seconds'] >= 0,
         'Only execution duration is nondeterministic metadata')
    old = inspection['old_schema_reference']
    if old is not None:
        need(same({key:value for key,value in result.items() if key != 'seconds'},
                  {key:value for key,value in old.items() if key != 'seconds'}),
             'Whole fresh answer agrees with the optional immutable reference, not just its PASS')
    return dict(n=job.n,band=job.band,index=job.index,statistics=stats,
                native_negative_controls=24,all_original_roots=job.n+1,
                fresh_leaf_evaluations=result['fresh_leaf_evaluations'])


def verify_capsule(directory,pins,prefix):
    for origin,pin in pins.items():
        need(origin.startswith(prefix) and '/' not in origin[len(prefix):],'One flat native manifest namespace')
        path = directory/origin[len(prefix):]
        need(path.is_file() and not path.is_symlink() and path.resolve().parent == directory.resolve()
             and digest(path) == pin,'Unchanged complete native input: '+origin)


def write(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cutoff6-archive',type=Path,required=True)
    parser.add_argument('--combined-archive',type=Path,required=True)
    parser.add_argument('--job',help='Exact composer-selected identity, e.g. n7.B0.p37')
    parser.add_argument('--inspect-only',action='store_true')
    args = parser.parse_args()
    need(args.inspect_only or args.job is not None,'Choose exactly one numerical job; no accidental all-job launch')
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary Python -B')
    spec = importlib.util.spec_from_file_location('native_continuation_count_guard',BASE/'run_reproduction.py')
    runner = importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024*runner.MIB
    install(runner);runner.parent_guard();runner.verify_sources()
    here = Path(__file__).resolve().parent
    helper_pins = {name:digest(here/name) for name in ('count_replay.py','count_catalog.py','catalog.py','archive_guard.py')}
    with Sources(args.cutoff6_archive,args.combined_archive,guard=runner.parent_guard) as sources:
        jobs,graph = count_jobs(sources)
        selected = [job for job in jobs if args.job is None or job.job_id == args.job]
        need(selected and (args.job is None or len(selected) == 1),'Selected original count job exists uniquely')
        inspections = [job_sources(sources,job,graph,verify_bytes=args.job is not None) for job in selected]
        if args.inspect_only:
            print(json.dumps(dict(scope='NATIVE_COUNT_CATALOG_SOURCE_INSPECTION_ONLY',
                jobs=[dict(**asdict(item['job']),source_files=item['source_files'],source_bytes=item['source_bytes'],
                           old_acceptance_present_but_not_input=item['old_schema_reference'] is not None)
                      for item in inspections],selected_jobs=len(inspections),arithmetic_executed=False,
                source_member_bytes_individually_verified=args.job is not None,
                fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)),flush=True);return
        inspection = inspections[0];job = selected[0];pins = inspection['source_files_sha256']
        root = (BASE/'work').resolve()
        need(root.parent == BASE.resolve() and not (BASE/'work').is_symlink(),'Owned regular scratch root')
        root.mkdir(exist_ok=True);epoch = root/('c69-'+uuid.uuid4().hex[:12]);epoch.mkdir(exist_ok=False)
        need(epoch.parent == root and runner.inside(epoch,BASE),'Exclusive private count epoch')
        runner.RETAINED_WORK = epoch
        need(shutil.disk_usage(epoch).free >= runner.DISK_FLOOR+runner.WORK_LIMIT,'Private quota and free-disk reserve')
        directory = epoch/'capsule';directory.mkdir()
        prefix = job.capsule+'/'
        for origin,pin in pins.items():
            target = directory/origin[len(prefix):]
            with target.open('xb') as stream:stream.write(sources.read(origin,pin,max_bytes=64*1024**2))
    # Drop large archive catalogs before the numerical process starts.
    full_guard = runner.parent_guard
    def epoch_guard(tiny=False,work=None):return full_guard(tiny=tiny,work=epoch if work is not None else None)
    runner.parent_guard = epoch_guard
    verify_capsule(directory,pins,prefix)
    output = directory/job.receipt_name
    need(not output.exists(),'No historical own PASS in the new count epoch')
    command = [sys.executable,*job.command]
    runner.parent_guard(work=epoch);runner.launch_gate()
    print(json.dumps(dict(event='native_continuation_count_started',job_id=job.job_id,work=str(epoch),
        unchanged_native_checker=True,fresh_parent_fact_joins_verified=False)),flush=True)
    started = datetime.now(timezone.utc).isoformat();tick = time.monotonic()
    stdout = run_recorded(runner,command,directory,'native-count',7200,512*runner.MIB)
    need(output.is_file(),'Unchanged native acceptor produced its new receipt')
    native = json.loads(output.read_text(encoding='utf-8'),object_pairs_hook=unique)
    need(same(json.loads(stdout,object_pairs_hook=unique),native),'Complete captured real native JSON result')
    facts = validate_result(job,inspection,native)
    verify_capsule(directory,pins,prefix)
    need(all(digest(here/name) == pin for name,pin in helper_pins.items()),'Published adapter code frozen throughout execution')
    capture = epoch/'capture';capture.mkdir()
    shutil.copyfile(directory/'native-count.stdout.txt',capture/'stdout.txt')
    with (capture/'stderr.txt').open('xb'):pass
    metadata = dict(command=command,cwd=str(directory.resolve()),returncode=0,
        started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,
        input_sha256=pins,stdout_sha256=digest(capture/'stdout.txt'),stderr_sha256=digest(capture/'stderr.txt'),
        native_result_sha256=digest(output),scope='ACTUAL_GUARDED_UNCHANGED_NATIVE_COUNT_ACCEPTANCE')
    write(capture/'metadata.json',metadata)
    runner.verify_sources();runner.parent_guard(work=epoch)
    report = dict(schema='FRESH_NATIVE_CONTINUATION_COUNT_ARITHMETIC_V1',
        scope='COMPLETE_UNCHANGED_NATIVE_COUNT_ARITHMETIC_ONLY_RESOURCE_PARENTS_NOT_DISCHARGED',
        job=asdict(job),facts=facts,source_files_sha256=pins,adapter_files_sha256=helper_pins,
        original_source_composer_sha256=FINAL_SHA,
        source_assets_sha256={CUTOFF6.name:CUTOFF6.sha256,COMBINED.name:COMBINED.sha256},
        unchanged_native_checker=True,source_port_used=False,old_own_acceptance_copied=False,
        old_acceptance_present_but_not_input=inspection['old_schema_reference'] is not None,
        complete_conditional_contract=inspection['contract'],
        required_fresh_parent_fact_joins=['Exact same-law resource/acquisition contract, including every installed budget and rho/p/support domain.',
            'The selected kernel/count analytic inequalities and global predecessor/contact hypotheses.',
            'Whole-band and sequential global composition; isolated count acceptance supplies none of them.'],
        native_result_path=str(output),native_result_sha256=digest(output),
        capture_path=str(capture),capture_metadata_sha256=digest(capture/'metadata.json'),
        execution_observed_by_this_controller=True,fresh_count_arithmetic=True,
        fresh_parent_fact_joins_verified=False,any_global_Cn_conclusion_verified=False,all_index_conclusion_verified=False)
    destination = epoch/'FRESH_NATIVE_COUNT_RESULT.json';write(destination,report)
    print(json.dumps(dict(event='native_continuation_count_finished',job_id=job.job_id,report=str(destination),
        sha256=digest(destination),**facts,fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)),flush=True)


if __name__ == '__main__':
    try:main()
    except Exception as exc:
        print('CONTINUATION_NATIVE_COUNT_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
