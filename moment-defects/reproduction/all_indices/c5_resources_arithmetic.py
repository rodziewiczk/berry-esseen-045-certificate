"""Recompute15 C5 resource jobs, CONDITIONALLY on their pinned parent facts.

Not c5.resources: historical INITIAL/support/Fourier receipts are reference
inputs until the separate fresh-parent semantic join has been established.
Every native resource answer and all native controls are recomputed; neither
old success flags nor this arithmetic-only stage discharge those parent facts.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from .c5_high_one import read, source_at
    from .c5_inputs import extended
    from .c5_acquisition_plan import RESOURCE_JOBS, INITIAL_JOBS, inspect_job, description, validate_catalog
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from c5_high_one import read, source_at
    from c5_inputs import extended
    from c5_acquisition_plan import RESOURCE_JOBS, INITIAL_JOBS, inspect_job, description, validate_catalog

sys.dont_write_bytecode=True
REPLAY_STATUS={
    'resource5_selected_accept_v1':('COMPLETE_EXACT_SELECTED_RESOURCE5_REPLAY_PENDING_INPUT_JOINS',23,31),
    'resource5_gamma_accept_v1':('COMPLETE_EXACT_GAMMA_RESOURCE5_REPLAY_PENDING_INPUT_JOINS',13,20),
    'resource5_sector_accept_v1':('COMPLETE_EXACT_SELECTED_SECTOR5_REPLAY_PENDING_INPUT_JOINS',13,20),
    'resource5_B3_accept_v1':('COMPLETE_EXACT_B3_SECTOR5_RESOURCE_REPLAY_PENDING_INPUT_JOINS',13,22),
    'resource5_B3_T3lower_accept_v1':('COMPLETE_EXACT_B3_SECTOR5_RESOURCE_REPLAY_PENDING_INPUT_JOINS',13,22),
}


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def replay_rows(job, replay):
    """Normalize only the container; preserve each ENTIRE canonical answer."""
    need(type(replay.get('n'))is int and replay['n']==5 and replay.get('band')==job.band,
         'Fresh literal resource n/band')
    expected,replay_controls,_=REPLAY_STATUS[job.family]
    need(replay['status']==expected and len(replay['negative_controls'])==replay_controls
         and len(set(replay['negative_controls']))==replay_controls,'All native arithmetic controls')
    if job.family=='resource5_gamma_accept_v1':
        source=replay['rows'];need(type(source)is list and len(source)==len(job.indices),'All gamma rows')
        need([r['index']for r in source]==list(job.indices) and
             all(type(r['index'])is int for r in source),'Ordered literal gamma indices')
        values={str(r['index']):r['result']for r in source}
    else:
        values=replay['computed']
        need(type(values)is dict and list(values)==list(map(str,job.indices)),
             'Complete exact selected resource panel inventory')
    result=[]
    for i in job.indices:
        answer=values[str(i)]
        need(type(answer)is dict and type(answer.get('excluded'))is bool,'Literal native resource decision')
        result.append(dict(index=i,p=[str(F(i,100)),str(F(i+1,100))],result=answer,
                           canonical_result_sha256=canonical_sha(answer)))
    return result


def summarize_job(epoch, job, prepared, initial, replay, accepted):
    """Fresh arithmetic facts for a later exact parent/child semantic join."""
    rows=replay_rows(job,replay)
    _,_,controls=REPLAY_STATUS[job.family]
    if job.family=='resource5_sector_accept_v1'and job.arguments[-1]=='endpoint':controls+=1
    need(accepted['status']==job.expected_status and type(accepted['n'])is int and accepted['n']==5
         and accepted['band']==job.band and accepted['selected']==list(job.indices),
         'Complete original native acceptance at the exact selected scope')
    need(len(accepted['negative_controls'])==controls and
         len(set(accepted['negative_controls']))==controls,'All arithmetic and input-join controls actually ran')
    if job.sector is not None:
        need(type(accepted['sector'])is int and accepted['sector']==job.sector,'Actual accepted sector')
    for flag in ('cutoff_proved','c5_proved'):
        need(accepted.get(flag,False)is False and replay.get(flag,False)is False,'No promoted global proof flag')
    parent=next(item for item in INITIAL_JOBS if item.job_id==job.initial_parent)
    candidate=epoch/job.case_directory/'INITIAL.json'
    scoped=prepared.get('source_job',prepared)
    initial_pin=scoped.get('source_initial_sha256',prepared.get('initial_sha256'))
    need(initial_pin==digest(candidate),'Literal pinned INITIAL candidate used by resource arithmetic')
    need(type(initial['n'])is int and initial['n']==5 and initial['band']==job.band
         and initial['physical_defect_seed']is False and initial['failure']is None,
         'Original unseeded matching INITIAL reference')
    need(len(initial['stages'])==parent.stages,'Exact parent finite-stage count')
    cover=initial['stages'][-1]['cover']
    need(len(cover['panels'])==100 and cover['total']==2592 and cover['active']==cover['gap_active'],
         'Whole100-panel final gap-licensed INITIAL reference')
    profile=initial['profile']
    need(type(profile['n'])is int and profile['n']==5 and profile['cap']==parent.owncap
         and initial['assumed_HIGH']==parent.high,'Exact original parent numerical profile')
    if job.sector is not None:
        need(type(initial['sector'])is int and initial['sector']==job.sector,'Exact INITIAL sector identity')
    selected=[r['index']for r in rows]
    excluded=[r['index']for r in rows if r['result']['excluded']]
    retained=[r['index']for r in rows if not r['result']['excluded']]
    need(accepted['excluded']==excluded and accepted['retained']==retained,
         'Native resource decisions agree with every full recomputed answer')
    return dict(scope='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY',job_id=job.job_id,n=5,
        band=job.band,sector=job.sector,case=job.case,arguments=list(job.arguments),
        selected_probability_panels=selected,excluded=excluded,retained=retained,
        rho_interval=accepted['rho_interval'],beta_interval=accepted.get('beta_interval'),
        resource_radius=accepted.get('radius',scoped.get('radius',profile['radius'])),
        resource_owncap=job.owncap,resource_HIGH=job.high,
        source_prepared_sha256=digest(epoch/job.prepared),
        parent_initial=dict(job_id=job.initial_parent,candidate_path=str(candidate),candidate_sha256=initial_pin,
            profile=profile,rho_interval=accepted['rho_interval'],
            beta_interval=accepted.get('beta_interval',initial.get('beta_enclosing_interval')),
            band_interval=initial.get('band_interval'),
            beta_enclosing_interval=initial.get('beta_enclosing_interval'),
            partition_kind=initial.get('partition_kind'),stages=len(initial['stages']),
            final_invariants=initial['final_invariants'],final_cover_sha256=canonical_sha(cover),
            referenced_receipt=replay['initial_receipt'],referenced_receipt_sha256=replay['initial_receipt_sha256'],
            historical_receipt_is_fresh_parent_proof=False,fresh_parent_fact_join_verified=False),
        full_canonical_resource_rows=rows,arithmetic_negative_controls=replay['negative_controls'],
        native_acceptance_negative_controls=accepted['negative_controls'],
        replay_path=str(epoch/job.output_paths[0]),replay_sha256=digest(epoch/job.output_paths[0]),
        native_accept_path=str(epoch/job.output_paths[1]),native_accept_sha256=digest(epoch/job.output_paths[1]),
        original_native_internal_status=accepted['status'],
        source_port_scope='NEW_METADATA_ONLY_PORT_NOT_UNCHANGED_NATIVE_WINDOWS_ACCEPTANCE',
        source_row_references=prepared.get('source_rows'),
        required_fresh_fact_joins=list(job.required_fresh_fact_joins),
        fresh_resource_arithmetic=True,fresh_arithmetic=False,register_as_c5_resources=False,
        fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--job',choices=tuple(j.job_id for j in RESOURCE_JOBS))
    parser.add_argument('--inspect-only',action='store_true',help='Check immutable input closure only; no replay')
    args=parser.parse_args();need(__debug__ and not sys.flags.optimize,'Ordinary nonoptimized resource coordinator')
    validate_catalog();selected=[j for j in RESOURCE_JOBS if args.job is None or j.job_id==args.job]
    spec=importlib.util.spec_from_file_location('resource_coordinator_observer',BASE/'run_reproduction.py')
    r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
    def guard():
        need(r.own_peak()<=256*r.MIB and r.available_ram()>=1024*r.MIB,
             'Resource coordinator256MiB cap and1GiB host reserve')
    guard();cache=extended(args.cache);final=source_at(cache,FINAL)
    need(digest(final)==FINAL_SHA,'Pinned full original C5 source graph');graph=read(final)['files_sha256']
    need(len(graph)==16576,'Complete original C5 graph')
    checked={};inspected=[inspect_job(cache,graph,j,checked,guard)for j in selected]
    if args.inspect_only:
        print(json.dumps(dict(scope='RESOURCE_SOURCE_INSPECTION_ONLY',jobs=inspected,
            arithmetic_executed=False,all_index_conclusion_verified=False)),flush=True);return
    root=(BASE/'work').resolve()
    need(not(BASE/'work').is_symlink() and root.parent==BASE.resolve(),'Repository-owned regular work root')
    root.mkdir(exist_ok=True)
    run=root/('r5run-'+uuid.uuid4().hex[:10]);run.mkdir(exist_ok=False)
    supervisor=Path(__file__).with_name('c5_resources_one.py');supervisor_pin=digest(supervisor)
    completed=[]
    for job in selected:
        need(digest(supervisor)==supervisor_pin,'Frozen resource-supervisor source across the serial run')
        log=run/(job.job_id+'.log');child=None
        command=[sys.executable,'-B','-S',str(supervisor),'--cache',str(cache),'--job',job.job_id]
        try:
            with log.open('xb')as stream:
                child=subprocess.Popen(command,cwd=BASE,stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,
                    **({'creationflags':subprocess.CREATE_NO_WINDOW}if sys.platform=='win32'else{'start_new_session':True}))
                while child.poll()is None:
                    guard();need(stream.tell()<=16*r.MIB,'Bounded resource supervisor log');time.sleep(.25)
            need(child.returncode==0,'Full resource replay/accept stage completed: '+job.job_id)
        finally:
            if child is not None and child.poll()is None:child.terminate();child.wait(timeout=10)
        lines=log.read_text(encoding='utf-8').splitlines();event=json.loads(lines[-1])
        need(event['job_id']==job.job_id and event['scope']=='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY',
             'Exact arithmetic-only selected component completion')
        report_path=Path(event['report']);report=read(report_path)
        need(report['job_id']==job.job_id and report['fresh_resource_arithmetic']is True
             and report['fresh_parent_fact_joins_verified']is False and report['register_as_c5_resources']is False,
             'Never promote historical-reference replay to fresh parent acquisition')
        completed.append(dict(job_id=job.job_id,report=str(report_path),sha256=digest(report_path),
            panels=len(job.indices),parent_initial=job.initial_parent,
            parent_initial_candidate_sha256=report['parent_initial']['candidate_sha256']))
        print(json.dumps(dict(event='fresh_resource_arithmetic_completed',**completed[-1],
            fresh_parent_fact_joins_verified=False)),flush=True)
    full=len(completed)==15
    if full:need(sum(x['panels']for x in completed)==1200,'All1200 selected resource-panel obligations')
    result=dict(scope='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY',jobs=completed,
        selected_jobs=len(completed),complete_15_job_arithmetic=full,
        resource_probability_panel_obligations=sum(x['panels']for x in completed),
        original_final_graph_sha256=FINAL_SHA,supervisor_sha256=supervisor_pin,
        fresh_parent_fact_joins_verified=False,fresh_arithmetic=False,
        register_as_c5_resources=False,all_index_conclusion_verified=False)
    with (run/'RESOURCE_ARITHMETIC_RUN.json').open('x',encoding='utf-8')as stream:json.dump(result,stream,indent=2)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('C5_RESOURCE_ARITHMETIC_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True);raise SystemExit(1)
