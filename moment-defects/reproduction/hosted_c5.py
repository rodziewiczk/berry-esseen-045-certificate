"""Manually selected hosted C5 arithmetic, guarded as one512MiB process branch.

Fetch ONLY the pinned original C5 archive, prepare its immutable inputs in a
separate guarded child, then execute an existing all_indices entry unchanged.
No source hash, archived PASS, or completed component is promoted to a global
C5/all-index theorem. This module never edits native or all_indices sources.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import time
import uuid

if not __package__:sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reproduction.all_indices.c5_counts import BASE,digest,need,unique
from reproduction.all_indices.supervised import run_recorded
from reproduction.continuations.archive_guard import install

sys.dont_write_bytecode = True
ARCHIVE = 'cutoff5_20261020.zip'
ARCHIVE_SHA = '8428002462d4e650613ea6e2ff673cb1e69c2079572cc40546d125349d582419'
ARCHIVE_BYTES = 141304365
FIVE = 'five-summands-2026-10-20'
STAGES = {
    'owncaps':'c5_owncaps_one.py',
    'initial':'c5_initial_arithmetic.py',
    'resources':'c5_resources_arithmetic.py',
    'complement':'c5_complement_one.py',
    'counts':'c5_counts.py',
    'support':'c5_support_one.py',
    'high':'c5_high_one.py',
}
MIB = 1024**2
ARTIFACT_LIMIT = 1024**3
ARTIFACT_FILE_LIMIT = 64*MIB


def load(path):
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)


def write(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,indent=2)


def selected_asset(manifest):
    need(manifest.get('schema') == 'berry-esseen-source-archives-v1'
         and manifest.get('repository') == 'rodziewiczk/berry-esseen-045-certificate'
         and manifest.get('release_tag') == 'cutoff5-sources-2026-10-20','Fixed public source release, no arbitrary URL')
    selected = [entry for entry in manifest['archives'] if entry.get('name') == ARCHIVE]
    need(len(selected) == 1,'Exactly one selected C5 source asset')
    entry = selected[0]
    need(type(entry['bytes']) is int and entry['bytes'] == ARCHIVE_BYTES
         and entry['sha256'] == ARCHIVE_SHA,'Hard-coded C5 size/SHA, never a supplied proof replacement')
    return entry


def fetch_only(destination):
    destination = destination.resolve()
    root = (BASE/'reproduction_inputs').resolve()
    need(destination.parent == root and destination.name == 'hosted-c5-archives'
         and not destination.is_symlink(),'Only the repository-owned hosted source cache')
    root.mkdir(exist_ok=True);destination.mkdir(exist_ok=True)
    helper = BASE/FIVE/'download_sources.py';manifest = load(BASE/FIVE/'source_archives.json')
    entry = selected_asset(manifest)
    spec = importlib.util.spec_from_file_location('pinned_public_c5_download',helper)
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    # Do not call the helper's main: it would download all three archives.
    module.download(manifest,entry,destination)
    need((destination/ARCHIVE).stat().st_size == ARCHIVE_BYTES and digest(destination/ARCHIVE) == ARCHIVE_SHA,
         'Only the exact complete original C5 asset was fetched')
    print(json.dumps(dict(scope='PINNED_C5_SOURCE_FETCH_ONLY',archive=str(destination/ARCHIVE),
        archive_sha256=ARCHIVE_SHA,arithmetic_executed=False,all_index_conclusion_verified=False)),flush=True)


def stage_command(stage,cache,archive):
    need(stage in STAGES,'One enumerated existing C5 arithmetic entry')
    source = BASE/'reproduction/all_indices'/STAGES[stage]
    arguments = ['--archive',str(archive)] if stage == 'counts' else ['--cache',str(cache)]
    return [sys.executable,'-B','-S',str(source),*arguments]


def stage_summary(stage,stdout):
    """Check complete selected arithmetic scope after observing guarded exit0."""
    lines = [line for line in stdout.splitlines() if line.strip()]
    need(lines,'A freshly executed component must print its complete result')
    result = json.loads(lines[-1],object_pairs_hook=unique)
    need(type(result) is dict and result.get('all_index_conclusion_verified') is False,
         'No all-index promotion in the selected native component')
    if stage in ('owncaps','support','high','complement'):
        statuses = {
            'owncaps':'FRESH_COARSE_AND_SELECTED_OWNCAPS_ACCEPTED',
            'support':'FRESH_SUPPORT_PROTOCOLS_ACCEPTED',
            'high':'FRESH_BOTH_NATIVE_HIGH_PROTOCOLS_ACCEPTED',
            'complement':'FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ACCEPTED'}
        need(result.get('status') == statuses[stage] and result.get('fresh_arithmetic') is True,
             'Complete selected component arithmetic, not a source inspection')
        if stage == 'owncaps':
            need([item['variant'] for item in result['receipts']] == ['owncaps5_v3','owncap_B3_ext_v1']
                 and result['coarse_429']['fresh_arithmetic'] is True,'Global coarse plus both original selected owncaps')
        elif stage == 'support':
            need([item['protocol'] for item in result['receipts']] == ['support_v1','support_v2','support_A0_v1'],
                 'All original selected support protocols')
        elif stage == 'high':
            need([item['variant'] for item in result['receipts']] == ['high5_v1','high5_eta_v1'],
                 'Both original selected HIGH protocols')
        else:need(result['fresh_support_and_fourier_parent_joins_verified'] is False,'Complement remains arithmetic-only')
    elif stage == 'initial':
        need(result['scope'] == 'FRESH_INITIAL_ARITHMETIC_BATCH_NOT_ACQUIRED_C5_THEOREM'
             and type(result['jobs_recomputed']) is int and result['jobs_recomputed'] == 12
             and len(result['reports']) == 12 and result['fresh_parent_fact_joins_verified'] is False,
             'All12 complete INITIAL arithmetic candidates, no parent theorem')
    elif stage == 'resources':
        need(result['scope'] == 'CONDITIONAL_RESOURCE_ARITHMETIC_ONLY'
             and type(result['selected_jobs']) is int and result['selected_jobs'] == 15
             and result['complete_15_job_arithmetic'] is True and len(result['jobs']) == 15
             and type(result['resource_probability_panel_obligations']) is int
             and result['resource_probability_panel_obligations'] == 1200
             and result['fresh_parent_fact_joins_verified'] is False and result['register_as_c5_resources'] is False,
             'All15 resource jobs/1200 panel obligations, no fresh-parent composition')
    else:
        need(result['scope'] == 'ALL_295_C5_COUNT_FORESTS_FRESHLY_REPLAYED'
             and all(type(result[key]) is int and result[key] == value for key,value in
                     (('forests',295),('original_count_roots',1770),('nodes',148586),('leaves',75178)))
             and result['resource_support_fourier_initial_and_gapfree_verified_by_this_stage'] is False,
             'All original295 full count forests; no resource/parent inference')
    return result


def implementation_pins():
    files = [Path(__file__).resolve(),BASE/'run_reproduction.py',BASE/FIVE/'download_sources.py',BASE/FIVE/'source_archives.json']
    files.extend(sorted((BASE/'reproduction/all_indices').glob('*.py')))
    files.append(BASE/'reproduction/continuations/archive_guard.py')
    return {path.relative_to(BASE).as_posix():digest(path) for path in files}


def verify_implementation(pins):
    need(all(digest(BASE/name) == pin for name,pin in pins.items()),'Entire selected orchestration/native-adapter code unchanged')


def execute(stage):
    need(sys.platform == 'win32','This hosted native branch uses the existing Windows job guards')
    spec = importlib.util.spec_from_file_location('original_hosted_c5_guard',BASE/'run_reproduction.py')
    runner = importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024*MIB;install(runner)
    runner.parent_guard();runner.verify_sources()
    pins = implementation_pins()
    run = runner.private_work()
    source_dir = BASE/'reproduction_inputs/hosted-c5-archives'
    archive = source_dir/ARCHIVE
    cache = BASE/'reproduction_inputs'/('c5-'+ARCHIVE_SHA[:16])
    report = dict(schema='HOSTED_C5_SELECTED_STAGE_V1',scope='SELECTED_COMPONENT_ARITHMETIC_ONLY',stage=stage,
        started_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=pins,
        source_archive_sha256=ARCHIVE_SHA,observed_guarded_steps=[],fresh_parent_fact_joins_verified=False,
        any_global_C5_conclusion_verified=False,all_index_conclusion_verified=False)
    write(run/'HOSTED_STAGE_START.json',report)
    commands = [
        ('fetch',[sys.executable,'-B','-S',str(Path(__file__).resolve()),'--internal-fetch','--archive-directory',str(source_dir)],600),
        ('prepare',[sys.executable,'-B','-S',str(BASE/'reproduction/all_indices/c5_inputs.py'),
                    '--archive',str(archive),'--destination',str(cache)],3600),
        ('arithmetic',stage_command(stage,cache,archive),19800),
    ]
    try:
        for label,command,cpu in commands:
            verify_implementation(pins);runner.launch_gate()
            tick = time.monotonic();started = datetime.now(timezone.utc).isoformat()
            print(json.dumps(dict(event='hosted_c5_step_started',stage=stage,step=label,
                started_utc=started,arithmetic_accepted=False,
                all_index_conclusion_verified=False)),flush=True)
            # ORIGINAL attach-before-resume Job covers the wrapper and every
            # descendant, even when an unchanged adapter uses its own Popen.
            stdout = run_recorded(runner,command,run,label,cpu,512*MIB)
            verify_implementation(pins);runner.parent_guard(work=run)
            item = dict(label=label,command=command,cwd=str(run),observed_returncode=0,
                started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),
                elapsed_seconds=time.monotonic()-tick,stdout_sha256=digest(run/(label+'.stdout.txt')),
                branch_memory_limit_bytes=512*MIB,branch_cpu_limit_seconds=cpu)
            report['observed_guarded_steps'].append(item)
            write(run/('HOSTED_OBSERVED_'+label.upper()+'.json'),item)
            print(json.dumps(dict(event='hosted_c5_step_terminated_successfully',stage=stage,
                step=label,elapsed_seconds=item['elapsed_seconds'],
                selected_component_scope_still_requires_validation=True,
                all_index_conclusion_verified=False)),flush=True)
            if label == 'prepare':
                prepared = json.loads(stdout.splitlines()[-1],object_pairs_hook=unique)
                need(prepared['scope'] == 'COMPLETE_PINNED_C5_INPUTS_PREPARED_ONLY'
                     and prepared['arithmetic_replayed'] is False,'Complete immutable source prep, never mathematical acceptance')
            elif label == 'arithmetic':report['component_result'] = stage_summary(stage,stdout)
        report.update(status='SELECTED_C5_ARITHMETIC_STAGE_EXECUTED',execution_observed_by_this_controller=True,
                      finished_utc=datetime.now(timezone.utc).isoformat())
        write(run/'HOSTED_STAGE_RESULT.json',report)
        print(json.dumps(dict(event='hosted_c5_stage_finished',stage=stage,report=str(run/'HOSTED_STAGE_RESULT.json'),
            fresh_parent_fact_joins_verified=False,any_global_C5_conclusion_verified=False,all_index_conclusion_verified=False)),flush=True)
    except BaseException as exc:
        report.update(status='INCOMPLETE_NO_COMPONENT_ACCEPTANCE',error=str(exc),
                      execution_observed_by_this_controller=False,finished_utc=datetime.now(timezone.utc).isoformat())
        write(run/'HOSTED_STAGE_FAILURE.json',report)
        raise


def collect_artifacts():
    """Bounded public work/log mirror; no environment, credentials or source ZIP."""
    source = BASE/'work';root = BASE/'hosted_artifacts'
    need(not root.is_symlink() and root.resolve().parent == BASE.resolve(),'Owned artifact destination only')
    if root.exists():need(not(getattr(root.lstat(),'st_file_attributes',0)&0x400),'No artifact-root reparse point')
    root.mkdir(exist_ok=True);destination = root/('c5-'+uuid.uuid4().hex[:12]);destination.mkdir(exist_ok=False)
    copied,omitted,total = [],[],0
    allowed = {'.py','.json','.jsonl','.txt','.log','.md','.diff','.csv'}
    if source.exists():
        need(source.is_dir() and not source.is_symlink() and source.resolve().parent == BASE.resolve(),'Owned proof-work tree only')
        need(not(getattr(source.lstat(),'st_file_attributes',0)&0x400),'No proof-work-root reparse point')
        for folder,directories,files in os.walk(source,followlinks=False):
            directory = Path(folder)
            for name in list(directories):
                value = (directory/name).lstat()
                if name.startswith('.') or stat.S_ISLNK(value.st_mode) or getattr(value,'st_file_attributes',0)&0x400:
                    directories.remove(name);omitted.append(dict(path=str((directory/name).relative_to(source)),reason='unsafe-or-hidden-directory'))
            for name in sorted(files):
                path = directory/name;relative = path.relative_to(source)
                reason = None;created = False;target = None
                try:
                    value = path.lstat()
                    if (name.startswith('.') or path.suffix.lower() not in allowed or not stat.S_ISREG(value.st_mode)
                        or getattr(value,'st_file_attributes',0)&0x400 or not path.resolve().is_relative_to(source.resolve())):
                        reason = 'unsafe-hidden-or-nonpublic-file-type'
                    elif value.st_size > ARTIFACT_FILE_LIMIT:reason = 'per-file64MiB-artifact-bound'
                    elif total+value.st_size > ARTIFACT_LIMIT or len(copied) >= 20000:reason = 'total1GiB-or20000-file-artifact-bound'
                    if reason is not None:omitted.append(dict(path=relative.as_posix(),reason=reason));continue
                    flags = os.O_RDONLY|getattr(os,'O_BINARY',0)|getattr(os,'O_NOFOLLOW',0)
                    descriptor = os.open(path,flags)
                    with os.fdopen(descriptor,'rb') as stream:
                        actual = os.fstat(stream.fileno())
                        identity = lambda z:(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns)
                        need(identity(actual) == identity(value),'Stable regular artifact before reading')
                        target = destination/'work'/relative;target.parent.mkdir(parents=True,exist_ok=True)
                        with target.open('xb') as output:
                            created = True
                            bounded_copy(stream,output,value.st_size)
                        need(identity(os.fstat(stream.fileno())) == identity(value)
                             and identity(path.lstat()) == identity(value),'Stable artifact after copying')
                    total += value.st_size
                    copied.append(dict(path='work/'+relative.as_posix(),bytes=value.st_size,sha256=digest(target)))
                except (OSError,ValueError) as exc:
                    if created and target is not None:
                        # Remove only this collector's incomplete exclusive copy.
                        need(target.resolve().is_relative_to(destination.resolve()),'Owned partial artifact only')
                        target.unlink()
                    omitted.append(dict(path=relative.as_posix(),reason='unstable-or-unreadable',detail=str(exc)))
    write(destination/'COLLECTION.json',dict(scope='BOUNDED_PUBLIC_WORK_AND_LOG_ARTIFACTS_NOT_PROOF_ACCEPTANCE',
        files=copied,bytes=total,omitted=omitted[:20000],omitted_count=len(omitted),
        source_zip_or_environment_uploaded=False,all_index_conclusion_verified=False))
    print(json.dumps(dict(artifact_directory=str(destination),files=len(copied),bytes=total,
        omitted=len(omitted),all_index_conclusion_verified=False)),flush=True)
    return destination


def bounded_copy(source,output,size):
    remaining = size
    while remaining:
        block = source.read(min(MIB,remaining))
        need(block,'Artifact did not shrink during copying')
        output.write(block);remaining -= len(block)
    need(not source.read(1),'Artifact did not grow beyond its checked size')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=tuple(STAGES))
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--internal-fetch',action='store_true',help=argparse.SUPPRESS)
    parser.add_argument('--archive-directory',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--collect-artifacts',action='store_true')
    args = parser.parse_args()
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary Python -B')
    if args.collect_artifacts:collect_artifacts();return
    if args.internal_fetch:
        need(args.archive_directory is not None,'Explicit guarded internal source destination')
        fetch_only(args.archive_directory);return
    need(args.stage is not None,'Select one manual component')
    if args.run:execute(args.stage)
    else:print(json.dumps(dict(scope='HOSTED_C5_EXECUTION_PLAN_ONLY',stage=args.stage,
        existing_entry=STAGES[args.stage],archive_sha256=ARCHIVE_SHA,arithmetic_executed=False,
        all_index_conclusion_verified=False)),flush=True)


if __name__ == '__main__':
    try:main()
    except Exception as exc:
        print('HOSTED_C5_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
