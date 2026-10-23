"""Hosted reconstruction of ONE missing n25 count forest, not the all-index proof.

Five targets preserve original V12 source designs. Two use explicitly NEW
conditional V14 epochs, never historical V14 identities. The existing source
preparers, discovery supervisor and canonical native acceptors run unchanged.
Downloads and mathematics require --run; default invocation is a plan only.
"""
from __future__ import annotations
import argparse
import ast
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time
import zipfile

if not __package__:sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reproduction.all_indices.c5_counts import BASE,digest,need,unique
from reproduction.all_indices.download_count_sources import ASSETS
from reproduction.all_indices.supervised import run_recorded
from reproduction.continuations.archive_guard import install

sys.dont_write_bytecode=True
MIB=1024**2
PUBLIC=BASE/'reproduction/all_indices'
PREPARER_SHA='4116a054c2f725794d82cc4bd7b954023c9b8525d8f943c6cea2a8096aceb647'
TARGETS={
    'b4-q0':('original-v12',29,'4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7'),
    'b4-q1':('original-v12',29,'a3cbdb1852bc51054ecc8cd3c71bd1c7121b6b201385e481b73195ad729189c4'),
    'b4-q2':('original-v12',29,'2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a'),
    'b4-q3':('original-v12',29,'c8555b500c3e7d1ca1240b5f229f7fff5ed307571012209e022431ecd195b7ac'),
    'b3-p33':('original-v12',33,'e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08'),
    'b3-p31-v14-new':('new-conditional-v14',31,'6ca73188c5a6969c1f0ec69f41cb0fac660003cf0515fdcadeeda83afcf654f0'),
    'b3-p32-v14-new':('new-conditional-v14',32,'230a6bb37696c1e79d62847d89090d4187d78d41aa6c98ccbe91c54e1f8f950b'),
}
SEARCH_MAX=10800
ACCEPT_SECONDS=7200
BRANCH_SECONDS=19800
HINT_SCHEMA='UNTRUSTED_COUNT_SEARCH_HINTS_V1'
HINT_MAX=8*MIB
PUBLISHED_HINTS=dict(repository='rodziewiczk/berry-esseen-045-certificate',
    release_tag='count-search-hints-2026-10-22',name='untrusted_count_search_hints_2026-10-22.zip',
    bytes=161372,sha256='9e9e45befa5590d2166f4aa5c55edd6d2595b1eb6c4ac6adcd1fd24855aead2a')


def read(path,maximum=16*MIB):
    need(path.is_file()and not path.is_symlink()and path.stat().st_size<=maximum,'Bounded regular metadata')
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)


def write(path,value):
    with path.open('x',encoding='utf-8')as stream:json.dump(value,stream,indent=2)


def event(directory,label,**values):
    """Durable observed step/slice progress, not a predicted completion status."""
    path=directory/'HOSTED_EVENTS.jsonl'
    need(not path.is_symlink()and(not path.exists()or path.stat().st_size<=MIB),'Owned bounded event log')
    need(values.get('all_index_conclusion_verified',False)is False,'No global conclusion in progress events')
    value=dict(values);value.update(event=label,utc=datetime.now(timezone.utc).isoformat(),
                                   all_index_conclusion_verified=False)
    with path.open('a',encoding='utf-8')as stream:
        stream.write(json.dumps(value,separators=(',',':'))+'\n');stream.flush();os.fsync(stream.fileno())
    print(json.dumps(value),flush=True)


def implementation_pins():
    files=[Path(__file__).resolve(),BASE/'run_reproduction.py',
        BASE/'five-summands-2026-10-20/download_sources.py',
        BASE/'reproduction/continuations/archive_guard.py']
    files+=list(PUBLIC.glob('*.py'))
    return {p.relative_to(BASE).as_posix():digest(p)for p in files}


def verify_implementation(pins):
    need(all(digest(BASE/name)==pin for name,pin in pins.items()),'Frozen hosted/controller/preparer/discovery code')
    need(digest(PUBLIC/'prepare_b3_v14_epoch_2026_10_22.py')==PREPARER_SHA,
         'The public V14 preparer has its reviewed byte identity; do not manufacture old design hashes')


def scope(target):
    return ('NEW_CONDITIONAL_V14_SOURCE_EPOCH_NOT_HISTORICAL_V14'
            if TARGETS[target][0]=='new-conditional-v14'else'ORIGINAL_V12_CONDITIONAL_COUNT_ONLY')


def fetch_published_hints(destination):
    root=(BASE/'reproduction_inputs').resolve();destination=Path(destination).resolve()
    need(destination.parent==root and destination.name=='hosted-count-hints'
         and not destination.is_symlink(),'Only the fixed repository-owned public hints cache')
    root.mkdir(exist_ok=True);destination.mkdir(exist_ok=True)
    helper=BASE/'five-summands-2026-10-20/download_sources.py'
    spec=importlib.util.spec_from_file_location('original_pinned_hint_download',helper)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.download(dict(repository=PUBLISHED_HINTS['repository'],release_tag=PUBLISHED_HINTS['release_tag']),
        {k:PUBLISHED_HINTS[k]for k in('name','bytes','sha256')},destination)
    path=destination/PUBLISHED_HINTS['name']
    need(path.stat().st_size==PUBLISHED_HINTS['bytes']and digest(path)==PUBLISHED_HINTS['sha256'],
         'Exact published UNTRUSTED checkpoint hints, never an acceptance receipt')
    print(json.dumps(dict(scope='PUBLISHED_UNTRUSTED_HINT_SOURCE_AVAILABILITY_ONLY',archive=str(path),
        sha256=digest(path),native_acceptance_verified=False,all_index_conclusion_verified=False)),flush=True)


def preparation_command(target,archives,capsule):
    kind,index,_=TARGETS[target]
    old=archives/'cutoff25_20261011.zip';base13=archives/'cutoff25_20261013.zip'
    if kind=='original-v12':
        return [sys.executable,'-B','-S',str(PUBLIC/'prepare_missing_count.py'),
                '--archive',str(old),'--target',target,'--output',str(capsule)]
    return [sys.executable,'-B','-S',str(PUBLIC/'prepare_b3_v14_epoch_2026_10_22.py'),
            '--old-archive',str(old),'--base13-archive',str(base13),'--index',str(index),'--output',str(capsule)]


def validate_source_epoch(target,capsule):
    kind,index,pin=TARGETS[target]
    need(digest(capsule/'FROZEN_DESIGN.json')==pin,'Exact target-dependent output source design')
    design=read(capsule/'FROZEN_DESIGN.json',MIB)
    need(type(design['files'])is dict and 1<=len(design['files'])<=256,'Complete bounded flat source closure')
    for name,expected in design['files'].items():
        need(type(name)is str and Path(name).name==name and '/'not in name and '\\'not in name
             and(capsule/name).stat().st_size<=16*MIB and digest(capsule/name)==expected,
             'Every prepared original/new native source byte')
    need(not(capsule/f'COUNT{index}_ACCEPTED.json').exists()
         and not(capsule/f'COUNT{index}_FOREST.json').exists(),'No historical own count acceptance/forest is a fresh input')
    if kind=='new-conditional-v14':
        epoch=read(capsule/'B3_V14_SOURCE_EPOCH.json')
        need(epoch['schema']=='NEW_CONDITIONAL_B3_V14_SOURCE_EPOCH_20261022_V1'
             and type(epoch['n'])is int and epoch['n']==25 and type(epoch['index'])is int and epoch['index']==index
             and epoch['preparer_sha256']==PREPARER_SHA and epoch['arithmetic_accepted']is False
             and epoch['native_acceptance_run']is False
             and epoch['expected_native_status']==f'PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT{index}',
             'Explicit new conditional source epoch, NOT an old V14 PASS or acquired parent')
    return dict(target=target,scope=scope(target),design_sha256=pin,source_files=len(design['files']),
                source_preparation_only=True,native_acceptance_verified=False,all_index_conclusion_verified=False)


def discovery_command(target,capsule,seconds,checkpoint=None):
    need(type(seconds)is int and 1<=seconds<=7200,'Unchanged discover_count bounded-slice API')
    command=[sys.executable,'-B','-S',str(PUBLIC/'discover_count.py'),'--capsule',str(capsule),
        '--design-sha256',TARGETS[target][2],'--seconds',str(seconds),'--alpha-priority','4','--order','root-first']
    if checkpoint is not None:command+=['--resume',str(checkpoint)]
    return command


def native_header_sources(capsule,target):
    """Extract literal header identity and file commitments WITHOUT importing a kernel."""
    tree=ast.parse((capsule/'count_protocol.py').read_bytes())
    headers=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='header']
    need(len(headers)==1 and len(headers[0].body)==1 and isinstance(headers[0].body[0],ast.Return),
         'Original simple literal native header')
    call=headers[0].body[0].value
    need(isinstance(call,ast.Call)and isinstance(call.func,ast.Name)and call.func.id=='dict',
         'Original native dict header')
    values={kw.arg:kw.value for kw in call.keywords}
    literal={key:ast.literal_eval(values[key])for key in('schema','n','index')}
    need(type(literal['n'])is int and literal['n']==25 and type(literal['index'])is int
         and literal['index']==TARGETS[target][1],'Same literal native25/header panel')
    return dict(literal,contract_sha256=digest(capsule/'contract.json'),
                checker_sha256=digest(capsule/'count_protocol.py'),
                kernel_sha256=read(capsule/'KERNEL_COPY_MANIFEST.json')['files'])


def extract_hint(archive,archive_sha,target,capsule,output):
    """Saved leaf payloads are UNTRUSTED hints; final native accept recomputes ALL."""
    need(type(archive_sha)is str and len(archive_sha)==64
         and all(c in'0123456789abcdef'for c in archive_sha),'Explicit complete hints ZIP SHA-256')
    archive=Path(archive).resolve();output=Path(output)
    need(archive.is_file()and not archive.is_symlink()and archive.stat().st_size<=64*MIB
         and digest(archive)==archive_sha,'Exact small published hints asset, never accepted arithmetic')
    with zipfile.ZipFile(archive)as zipped:
        names=zipped.namelist()
        need(names.count('manifest.json')==1,'Unique hints manifest')
        info=zipped.getinfo('manifest.json')
        need(info.file_size<=MIB,'Bounded hints manifest')
        manifest=json.loads(zipped.read(info),object_pairs_hook=unique)
        need(manifest['schema']==HINT_SCHEMA and manifest['arithmetic_accepted']is False
             and set(manifest['targets'])==set(TARGETS),'All seven exact untrusted target hints')
        expected={'manifest.json'}
        for name,row in manifest['targets'].items():
            member='checkpoints/'+name+'/CHECKPOINT.json';expected.add(member)
            need(row['member']==member and row['design_sha256']==TARGETS[name][2]
                 and type(row['bytes'])is int and 1<=row['bytes']<=HINT_MAX,
                 'Each hint is bound to its reviewed target/source epoch')
            if'n'in row:need(type(row['n'])is int and row['n']==25,'Literal hint metadata sample size')
            if'index'in row:need(type(row['index'])is int and row['index']==TARGETS[name][1],
                                 'Literal hint metadata panel')
        need(len(names)==len(expected)and set(names)==expected,'Only unique manifest plus seven checkpoint members')
        need(all(not zipped.getinfo(name).is_dir()and not stat.S_ISLNK(zipped.getinfo(name).external_attr>>16)
                 for name in names),'Only regular byte members, no ZIP symlink/directory hints')
        row=manifest['targets'][target];info=zipped.getinfo(row['member'])
        need(not info.is_dir()and info.file_size==row['bytes']and info.file_size<=HINT_MAX
             and not stat.S_ISLNK(info.external_attr>>16),'Exact bounded regular selected checkpoint')
        raw=zipped.read(info);need(hashlib.sha256(raw).hexdigest()==row['sha256'],'Selected hint bytes match explicit manifest')
    candidate=json.loads(raw,object_pairs_hook=unique)
    binding=candidate['binding']
    need(candidate['schema']=='UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1'and candidate['arithmetic_accepted']is False
         and binding['design_sha256']==TARGETS[target][2]and binding['alpha_priority']=='4',
         'Same exact native design/strategy, and explicitly NOT acceptance')
    source_header=native_header_sources(capsule,target)
    need(all(binding['native_header'].get(k)==v for k,v in source_header.items()),
         'Original contract/checker/full-kernel/literal-header agreement, never cross-epoch leaf reuse')
    roots=candidate['roots']
    need(type(roots)is list and len(roots)==26 and all(type(root)is dict and set(root)=={'k','tree'}
         and type(root['k'])is int and root['k']==i and type(root['tree'])is dict
         for i,root in enumerate(roots)),'ALL26 original ordered count roots, no absent seam')
    need(not output.exists(),'Exclusive new untrusted hint path')
    with output.open('xb')as stream:stream.write(raw)
    return dict(checkpoint=str(output.resolve()),sha256=row['sha256'],source_archive_sha256=archive_sha,
        target=target,design_sha256=TARGETS[target][2],saved_leaf_results_are_untrusted=True,
        native_acceptance_verified=False,all_index_conclusion_verified=False)


def validate_slice(result):
    need(type(result)is dict and result.get('all_index_conclusion_verified',False)is False,
         'No global conclusion from one untrusted search/native count')
    need(result.get('status')in('SEARCH_CHECKPOINTED_INCOMPLETE','NATIVE_COUNT_ACCEPTED'),
         'No discovery-complete candidate promoted before separate native acceptance')
    accepted=result['status']=='NATIVE_COUNT_ACCEPTED'
    need(result.get('arithmetic_accepted')is accepted,'Literal partial/accepted distinction')
    for key in('nodes','leaves','pending'):
        need(type(result[key])is int and result[key]>=0,'Literal finite search census')
    need(result['nodes']==2*result['leaves']+2*result['pending']-26,'Whole26-root binary candidate census')
    need(result['pending']==0 if accepted else result['pending']>0,'All roots closed before acceptance')
    return accepted


def acceptance_summary(target,result):
    """Only after our guarded discover supervisor completed successfully."""
    need(validate_slice(result),'Actual full native acceptance required')
    kind,index,_=TARGETS[target]
    path=Path(result['native_receipt']).resolve();work=Path(result['work']).resolve();capsule=work/'capsule'
    need(work.parent==(BASE/'work').resolve()and path==capsule/f'COUNT{index}_ACCEPTED.json'
         and not work.is_symlink()and not capsule.is_symlink(),'Actual owned new acceptance epoch')
    native=read(path)
    expected=(f'PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT{index}'
              if kind=='new-conditional-v14'else f'PASS_FRESH_CONDITIONAL_EXACT_COUNT{index}')
    need(native['status']==expected and type(native['fresh_leaf_evaluations'])is int
         and native['fresh_leaf_evaluations']==result['leaves']
         and type(native['negative_controls'])is list and len(native['negative_controls'])==24
         and len(set(native['negative_controls']))==24,'Every fresh canonical leaf and all24 original corruption controls')
    need(type(native['statistics']['nodes'])is int and type(native['statistics']['leaves'])is int
         and native['statistics']['nodes']==result['nodes']
         and native['statistics']['leaves']==result['leaves'],'Full freshly accepted count and discovered26-root census agree')
    for name,key in((f'COUNT{index}_FOREST.json','forest_sha256'),('contract.json','contract_sha256'),
                    ('count_protocol.py','checker_sha256')):
        need(native[key]==digest(capsule/name),'Exact new native acceptance input bytes')
    manifest=read(capsule/'KERNEL_COPY_MANIFEST.json')['files']
    need(native['kernel_sha256']==manifest and all(digest(capsule/name)==pin for name,pin in manifest.items()),
         'Full unchanged/explicitly derived native mathematical source closure')
    return dict(status=expected,native_receipt=str(path),native_receipt_sha256=digest(path),
        canonical_leaf_evaluations=result['leaves'],negative_controls=24,
        native_acceptance_verified=True,scope=scope(target),fresh_parent_acquisitions_verified=False,
        all_index_conclusion_verified=False)


def runner_instance():
    need(sys.platform=='win32','Hosted full-tree count execution requires Windows Job Objects')
    spec=importlib.util.spec_from_file_location('hosted_missing_count_guard',BASE/'run_reproduction.py')
    runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    runner.HOST_FLOOR=1024*MIB;install(runner)
    need(runner.NATIVE is not None,'No per-process substitute for whole512MiB Job guarding')
    runner.parent_guard();runner.verify_sources()
    return runner


def internal_search(target,capsule,output,search_seconds,slice_seconds,initial_checkpoint=None):
    runner=runner_instance();pins=implementation_pins();verify_implementation(pins)
    capsule=Path(capsule).resolve();output=Path(output).resolve()
    need(output.is_relative_to((BASE/'work').resolve())and not output.exists(),'New owned search-chain report directory')
    output.mkdir();validate_source_epoch(target,capsule)
    remaining=search_seconds;checkpoint=Path(initial_checkpoint)if initial_checkpoint is not None else None
    attempts=[];accepted=None
    if checkpoint is not None:
        need(checkpoint.is_file()and not checkpoint.is_symlink()and checkpoint.stat().st_size<=HINT_MAX,
             'Only the complete previously checked untrusted initial hint')
    event(output,'hosted_count_search_chain_started',target=target,source_epoch_scope=scope(target),
          allocated_search_budget_seconds=search_seconds,native_acceptance_verified=False)
    try:
        while remaining>0:
            seconds=min(remaining,slice_seconds);remaining-=seconds
            verify_implementation(pins);runner.launch_gate()
            command=discovery_command(target,capsule,seconds,checkpoint)
            label='slice-'+str(len(attempts)+1);started=time.monotonic()
            event(output,'hosted_count_slice_started',target=target,slice=label,command=command,
                  assigned_search_seconds=seconds,resume_checkpoint=str(checkpoint)if checkpoint is not None else None,
                  native_acceptance_verified=False)
            stdout=run_recorded(runner,command,output,label,min(BRANCH_SECONDS,seconds+ACCEPT_SECONDS+120),512*MIB)
            verify_implementation(pins)
            result=json.loads(stdout.splitlines()[-1],object_pairs_hook=unique)
            closed=validate_slice(result)
            work=Path(result['work']).resolve()
            need(work.parent==(BASE/'work').resolve()and not work.is_symlink(),'Our actual new discovery epoch')
            candidate_checkpoint=work/'search/CHECKPOINT.json'
            if candidate_checkpoint.is_file():
                need(not candidate_checkpoint.is_symlink()and candidate_checkpoint.stat().st_size<=128*MIB,
                     'Complete regular candidate checkpoint, not a reduced summary')
                checkpoint=candidate_checkpoint
            else:
                need(closed,'Incomplete search must preserve its full candidate checkpoint')
                # Count discovery currently always writes its final checkpoint.
                # A complete independently accepted native forest is sufficient
                # even if a future unchanged producer omits this auxiliary copy.
                checkpoint=None
            if closed:accepted=acceptance_summary(target,result)
            attempt=dict(label=label,command=command,requested_search_seconds=seconds,
                observed_returncode=0,elapsed_seconds=time.monotonic()-started,work=str(work),
                result=result,checkpoint=str(checkpoint)if checkpoint is not None else None,
                checkpoint_sha256=digest(checkpoint)if checkpoint is not None else None,
                complete_candidate_checkpoint_is_not_acceptance=not closed)
            attempts.append(attempt);write(output/(label+'-OBSERVED.json'),attempt)
            event(output,'hosted_count_slice_finished',target=target,slice=label,status=result['status'],
                  nodes=result['nodes'],leaves=result['leaves'],pending=result['pending'],
                  checkpoint=attempt['checkpoint'],observed_returncode=0,
                  elapsed_seconds=attempt['elapsed_seconds'],native_acceptance_verified=accepted is not None)
            if closed:break
        report=dict(schema='HOSTED_MISSING_COUNT_SEARCH_CHAIN_V1',target=target,scope=scope(target),
            status='NATIVE_COUNT_ACCEPTED'if accepted is not None else'PARTIAL_CANDIDATE_CHECKPOINT_ONLY',
            requested_search_budget_seconds=search_seconds,allocated_search_seconds=search_seconds-remaining,
            attempts=attempts,native_acceptance_verified=accepted is not None,native_acceptance=accepted,
            checkpoint=str(checkpoint)if checkpoint is not None else None,
            fresh_parent_acquisitions_verified=False,complete_mathematical_dependency_graph_executed=False,
            all_index_conclusion_verified=False)
        write(output/'SEARCH_CHAIN_RESULT.json',report)
        event(output,'hosted_count_search_chain_finished',target=target,status=report['status'],
              slices=len(attempts),native_acceptance_verified=accepted is not None)
        print(json.dumps(report),flush=True)
    except BaseException as exc:
        write(output/'SEARCH_CHAIN_FAILURE.json',dict(status='INCOMPLETE_NOT_ACCEPTED',target=target,
            error=str(exc),attempts=attempts,checkpoint=str(checkpoint)if checkpoint is not None else None,
            native_acceptance_verified=False,all_index_conclusion_verified=False))
        event(output,'hosted_count_search_chain_failed',target=target,error=str(exc),native_acceptance_verified=False)
        raise


def execute(target,search_seconds,slice_seconds,hints_archive=None,hints_sha=None,use_published_hints=False):
    runner=runner_instance();pins=implementation_pins();verify_implementation(pins)
    run=runner.private_work();archives=BASE/'reproduction_inputs/count-source-archives';capsule=run/'prepared-capsule'
    report=dict(schema='HOSTED_MISSING_COUNT_RECONSTRUCTION_V1',target=target,scope=scope(target),
        started_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=pins,source_archives=list(ASSETS),
        observed_guarded_steps=[],native_acceptance_verified=False,fresh_parent_acquisitions_verified=False,
        complete_mathematical_dependency_graph_executed=False,all_index_conclusion_verified=False)
    write(run/'HOSTED_COUNT_START.json',report)
    event(run,'hosted_count_controller_started',target=target,source_epoch_scope=scope(target),
          native_acceptance_verified=False)
    commands=[('fetch',[sys.executable,'-B','-S',str(PUBLIC/'download_count_sources.py'),
                       '--directory',str(archives),'--download'],1800,256*MIB),
              ('prepare',preparation_command(target,archives,capsule),1800,256*MIB),
              ('search',[sys.executable,'-B','-S',str(Path(__file__).resolve()),'--internal-search',
                '--target',target,'--capsule',str(capsule),'--output',str(run/'search-chain'),
                '--search-seconds',str(search_seconds),'--slice-seconds',str(slice_seconds)],BRANCH_SECONDS,512*MIB)]
    if use_published_hints:
        hint_directory=BASE/'reproduction_inputs/hosted-count-hints'
        hints_archive=hint_directory/PUBLISHED_HINTS['name'];hints_sha=PUBLISHED_HINTS['sha256']
        commands.insert(1,('fetch-untrusted-hints',[sys.executable,'-B','-S',str(Path(__file__).resolve()),
            '--internal-hints-fetch','--hints-directory',str(hint_directory)],600,256*MIB))
    try:
        for label,command,cpu,memory in commands:
            if label=='search'and hints_archive is not None:
                hint=extract_hint(hints_archive,hints_sha,target,capsule,run/'INITIAL_UNTRUSTED_HINT.json')
                report['untrusted_initial_hint']=hint
                command+=['--initial-checkpoint',hint['checkpoint']]
                event(run,'hosted_count_untrusted_hint_prepared',**hint)
            verify_implementation(pins);runner.launch_gate();started=time.monotonic()
            event(run,'hosted_count_step_started',target=target,step=label,command=command,
                  whole_branch_memory_limit_bytes=memory,whole_branch_cpu_limit_seconds=cpu,
                  native_acceptance_verified=False)
            stdout=run_recorded(runner,command,run,label,cpu,memory)
            verify_implementation(pins);runner.parent_guard(work=run)
            report['observed_guarded_steps'].append(dict(label=label,command=command,cwd=str(run),
                observed_returncode=0,elapsed_seconds=time.monotonic()-started,
                stdout_sha256=digest(run/(label+'.stdout.txt')),
                whole_branch_cpu_limit_seconds=cpu,whole_branch_memory_limit_bytes=memory))
            if label=='prepare':report['prepared_source_epoch']=validate_source_epoch(target,capsule)
            if label=='search':
                result=json.loads(stdout.splitlines()[-1],object_pairs_hook=unique)
                need(result['schema']=='HOSTED_MISSING_COUNT_SEARCH_CHAIN_V1'and result['target']==target
                     and result['scope']==scope(target)and result['all_index_conclusion_verified']is False,
                     'Exact observed new count chain scope')
                report['search_result']=result
                report['native_acceptance_verified']=result['native_acceptance_verified']
            event(run,'hosted_count_step_finished',target=target,step=label,observed_returncode=0,
                  elapsed_seconds=time.monotonic()-started,native_acceptance_verified=report['native_acceptance_verified'])
        report.update(status='NATIVE_COUNT_ACCEPTED'if report['native_acceptance_verified']else'PARTIAL_CANDIDATE_CHECKPOINT_ONLY',
            execution_observed_by_this_controller=True,finished_utc=datetime.now(timezone.utc).isoformat(),
            retained_hypotheses=['Same original whole-parent INITIAL/resource/global predecessor acquisitions',
                'The retained contact/attainment/Fourier/count analytic framework',
                'New V14 targets additionally require their explicit attained-positive-contact5/16 premises'])
        write(run/'HOSTED_COUNT_RESULT.json',report)
        print(json.dumps(dict(event='hosted_missing_count_finished',target=target,status=report['status'],
            report=str(run/'HOSTED_COUNT_RESULT.json'),native_acceptance_verified=report['native_acceptance_verified'],
            all_index_conclusion_verified=False)),flush=True)
        return 0 if report['native_acceptance_verified']else 2
    except BaseException as exc:
        report.update(status='INCOMPLETE_NOT_ACCEPTED',error=str(exc),native_acceptance_verified=False,
            execution_observed_by_this_controller=False,finished_utc=datetime.now(timezone.utc).isoformat())
        write(run/'HOSTED_COUNT_FAILURE.json',report);raise


def collect_artifacts():
    """Inventory ALL work/checkpoints; upload work directly, without64MiB truncation."""
    source=BASE/'work';destination=BASE/'hosted_count_artifacts'
    need(not source.is_symlink()and not destination.is_symlink(),'Owned non-symlink artifact roots')
    destination.mkdir(exist_ok=True);files=[];total=0
    if source.exists():
        for folder,directories,names in os.walk(source,followlinks=False):
            directory=Path(folder)
            for name in directories:
                info=(directory/name).lstat()
                need(not stat.S_ISLNK(info.st_mode)and not(getattr(info,'st_file_attributes',0)&0x400),
                     'No symlink/reparse directory in public proof artifacts')
            for name in names:
                path=directory/name;info=path.lstat()
                need(stat.S_ISREG(info.st_mode)and not(getattr(info,'st_file_attributes',0)&0x400)
                     and path.resolve().is_relative_to(source.resolve()),'Only regular owned proof artifact files')
                total+=info.st_size;files.append(dict(path=path.relative_to(source).as_posix(),bytes=info.st_size))
                need(len(files)<=100000 and total<=4*1024**3,'Bounded complete proof artifact inventory')
    result=dict(scope='ALL_WORK_FILES_CHECKPOINTS_AND_LOGS_NOT_ACCEPTANCE',files=files,total_bytes=total,
        copy_or_size_filter_applied=False,source_archives_or_environment_uploaded=False,
        all_index_conclusion_verified=False)
    write(destination/('COUNT_ARTIFACT_INVENTORY_'+str(time.time_ns())+'.json'),result)
    print(json.dumps(dict(work_artifact_directory=str(source),inventory_directory=str(destination),
        files=len(files),bytes=total,native_acceptance_verified=False,all_index_conclusion_verified=False)),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',choices=tuple(TARGETS))
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--search-seconds',type=int,default=SEARCH_MAX)
    parser.add_argument('--slice-seconds',type=int,default=1800)
    parser.add_argument('--collect-artifacts',action='store_true')
    parser.add_argument('--hints-archive',type=Path,help='Optional exact published ZIP of UNTRUSTED search candidates')
    parser.add_argument('--hints-sha256',help='Required exact ZIP SHA with --hints-archive; not acceptance')
    parser.add_argument('--use-published-hints',action='store_true',help='Fetch the fixed small pinned UNTRUSTED hints asset')
    parser.add_argument('--internal-search',action='store_true',help=argparse.SUPPRESS)
    parser.add_argument('--capsule',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--output',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--initial-checkpoint',type=Path,help=argparse.SUPPRESS)
    parser.add_argument('--internal-hints-fetch',action='store_true',help=argparse.SUPPRESS)
    parser.add_argument('--hints-directory',type=Path,help=argparse.SUPPRESS)
    args=parser.parse_args()
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary Python -B without optimization')
    need(1<=args.search_seconds<=SEARCH_MAX and 1<=args.slice_seconds<=7200,'Bounded allocated search and unchanged slice API')
    need((args.hints_archive is None)==(args.hints_sha256 is None),'Hints require BOTH explicit archive and SHA')
    need(not(args.use_published_hints and args.hints_archive is not None),'One explicit hints source, not two')
    if args.collect_artifacts:collect_artifacts();return 0
    if args.internal_hints_fetch:
        need(args.hints_directory is not None,'Fixed guarded hint source destination')
        fetch_published_hints(args.hints_directory);return 0
    need(args.target is not None,'One enumerated target, never arbitrary native code')
    if args.internal_search:
        need(args.capsule is not None and args.output is not None,'Exact guarded internal source/output selectors')
        internal_search(args.target,args.capsule,args.output,args.search_seconds,args.slice_seconds,args.initial_checkpoint);return 0
    if args.run:return execute(args.target,args.search_seconds,args.slice_seconds,args.hints_archive,args.hints_sha256,
                               args.use_published_hints)
    print(json.dumps(dict(scope='HOSTED_COUNT_EXECUTION_PLAN_ONLY',target=args.target,source_epoch_scope=scope(args.target),
        design_sha256=TARGETS[args.target][2],search_seconds=args.search_seconds,slice_seconds=args.slice_seconds,
        source_archives=list(ASSETS),published_untrusted_hints=PUBLISHED_HINTS if args.use_published_hints else None,
        arithmetic_executed=False,native_acceptance_verified=False,
        all_index_conclusion_verified=False)),flush=True)
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        print('HOSTED_COUNT_RECONSTRUCTION_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True);raise SystemExit(1)
