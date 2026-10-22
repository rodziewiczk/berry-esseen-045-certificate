"""Exact gap-free/complement domains and source-bound arithmetic artifacts."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path

from ..all_indices.c5_counts import BASE,FINAL_SHA,ARCHIVE_SHA,digest,need
from ..all_indices.c5_inputs import extended
from ..all_indices.c5_high_one import source_at
from ..all_indices.c5_parent_evidence import (ParentEvidence,checked_json,report_epoch,regular_owned,
                                            verify_graph,verify_capture)
from ..all_indices import c5_gapfree as gapfree
from ..all_indices import c5_complement_one as complement
from ..all_indices import c5_complement_worker as complement_worker
from .core import B3,TARGET,declaration,exact
from .loaders import final_graph


def corner_domain(value):
    need(type(value['n'])is int and value['n']==5 and value['rho']==['477/400','6/5']
         and value['beta']==['17/50',str(B3)]and value['target']==str(TARGET),
         'Exact whole-line corner, not a narrowed beta rectangle')
    compact=value['compact'];rays=value['exteriors']
    need(all(type(compact[k])is int for k in('roots','nodes','leaves'))
         and(compact['roots'],compact['nodes'],compact['leaves'])==(60,1994,1027)
         and 0<=F(compact['independent_upper'])<=F(compact['stored_upper'])<TARGET,
         'Entire independently evaluated compact forest and strict score')
    need(rays['left_domain']=='z<=0'and rays['right_domain']=='z>=5'
         and F(rays['left_upper'])<F(331,1000)<TARGET
         and F(rays['right_upper'])<F(187,1000)<TARGET,'Both complete exterior rays, not a finite threshold window')
    return dict(n=5,rho=value['rho'],beta=value['beta'],target=str(TARGET),
                roots=60,nodes=1994,leaves=1027,compact=compact,exteriors=rays)


def complement_domain(value,evidence):
    need(type(evidence)is ParentEvidence,'Typed complete source-bound support evidence')
    need(type(value['n'])is int and value['n']==5 and value['rho_finite']==['6/5','7361/4000']
         and value['target']==str(TARGET)and type(value['strips'])is int and value['strips']==41
         and type(value['attempts'])is int and value['attempts']==42,
         'All41 strips and42 attempts of the exact complement')
    cursor=F(6,5);strips=0;edges=[]
    for band in value['bands']:
        lo,hi=map(F,band['rho']);radius=F(band['radius'])
        need(lo==cursor<hi and F(band['upper'])<TARGET
             and type(band['strips'])is int and band['strips']>0,'Closed finite band seams and strict maxima')
        support=next((f for f in evidence.facts if f.kind=='support'and f.n==5
             and f.rho_lower<=lo<hi<=f.rho_upper and f.radius<=radius),None)
        need(support is not None,'Actual support implication on EVERY entire complementary band')
        edges.append(dict(kind='support',parent=support.receipt_sha256,band=band['name'],
                          rho=band['rho'],acquired_radius=str(support.radius),required_radius=str(radius)))
        cursor=hi;strips+=band['strips']
    tail=F(3031,10000)*(1+F(323,500)/cursor)
    need(len(value['bands'])==6 and cursor==F(7361,4000)and strips==41
         and tail==F(819,2000)==F(value['published_tail_upper_at_start'])<TARGET,
         'Complete finite complement and exact monotone Shevtsova tail seam')
    return dict(rho_finite=value['rho_finite'],bands=value['bands'],strips=41,attempts=42,
                support_edges=edges,published_tail=dict(rho_lower=str(cursor),upper=str(tail),
                    retained_published_premise='Shevtsova2013 iid .3031*(1+.646/rho)'))


def load_corner(cache,result_path,*,work_root=None):
    work_root=Path(work_root)if work_root is not None else BASE/'work'
    cache=extended(Path(cache));graph=final_graph(cache)
    regular_owned(work_root,result_path)
    capsule=Path(result_path).parent;epoch=capsule.parent
    need(Path(result_path).name=='FRESH_GAPFREE_RESULT.json'and capsule.name=='capsule'
         and epoch.parent.resolve()==work_root.resolve(),'New dedicated independent gap-free epoch')
    value=checked_json(epoch,result_path)
    need(value['status']=='PASS_FRESH_C5_GAPFREE_INDEPENDENT_WHOLE_LINE'
         and value['old_capture_metadata_used_as_a_mathematical_premise']is False
         and value['unrestricted_C5_or_all_indices_verified_by_this_stage']is False,
         'Only the NEW gap-free arithmetic artifact, not old READBACK/EXTERIOR acceptance')
    inputs=checked_json(epoch,capsule/'INPUTS.json')
    need(exact(value['inputs'],inputs)and inputs['schema']=='C5_GAPFREE_INDEPENDENT_REPLAY_INPUTS_V1'
         and inputs['original_archive_sha256']==ARCHIVE_SHA
         and inputs['original_final_index_sha256']==FINAL_SHA
         and inputs['original_source_paths']==gapfree.FILES,'Exact original three-source gap-free obligation')
    for name,original in gapfree.FILES.items():
        need(inputs['files'][name]==graph[original]==digest(regular_owned(epoch,capsule/name)),
             'Unchanged gap-free source/forest/exterior input')
    worker=regular_owned(epoch,capsule/'c5_gapfree_worker.py')
    need(digest(worker)==value['adapter_sha256']==digest(Path(gapfree.__file__).with_name(worker.name)),
         'Complete published independent1027-leaf/two-ray worker identity')
    need(type(value['negative_controls'])is list and len(value['negative_controls'])==16
         and len(set(value['negative_controls']))==16,'All16 original gap-free corruption controls')
    recorded=checked_json(epoch,epoch/'c5-gapfree-independent.stdout.txt')
    need(exact(recorded,value),'Entire recorded canonical independent gap-free result')
    return declaration(schema='C5_SOURCE_BOUND_GAPFREE_V1',**corner_domain(value),
        arithmetic_artifact=dict(path=str(result_path),sha256=digest(result_path)),
        recorded_native_stdout_sha256=digest(epoch/'c5-gapfree-independent.stdout.txt'),
        independent_worker_sha256=digest(worker))


def load_complement(cache,report_path,evidence,*,work_root=None):
    work_root=Path(work_root)if work_root is not None else BASE/'work'
    cache=extended(Path(cache));graph=final_graph(cache)
    epoch=report_epoch(report_path,'FRESH_COMPLEMENT_SUPERVISOR_RESULT.json',work_root)
    report=checked_json(epoch,report_path)
    need(report['scope']=='C5_COMPLEMENT_ARITHMETIC_ONLY_NOT_FULL_C5_COMPLEMENT_COMPONENT'
         and report['status']=='FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ACCEPTED'
         and report['fresh_arithmetic']is True
         and report['fresh_support_and_fourier_parent_joins_verified']is False
         and report['all_index_conclusion_verified']is False,'NEW conditional complement artifact')
    pins=complement.selected_sources(cache,graph)
    need(report['source_files_sha256']==pins,'Whole exact original complement arithmetic closure')
    verify_graph(epoch,pins)
    worker=regular_owned(epoch,epoch/'c5_complement_worker.py')
    need(digest(worker)==report['adapter_worker_sha256']==digest(Path(complement_worker.__file__)),
         'Published arithmetic-only complement worker')
    path=epoch/'FRESH_COMPLEMENT_ARITHMETIC_RESULT.json'
    need(Path(report['receipt']).resolve()==path.resolve(),'Exact new complement result destination')
    value=checked_json(epoch,path,report['sha256'])
    need(value['status']=='PASS_FRESH_C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_ONLY'
         and value['historical_captures_or_PASS_used_as_mathematical_premise']is False
         and value['two_complete_native_integrations']is True
         and value['fresh_support_and_fourier_parent_joins_verified']is False,'Both complete NEW integrations')
    inputs=checked_json(epoch,epoch/'COMPLEMENT_INPUTS.json',value['input_document_sha256'])
    need(inputs['schema']=='C5_COMPLEMENT_CONDITIONAL_ARITHMETIC_INPUTS_V1'
         and inputs['original_final_graph_sha256']==FINAL_SHA and inputs['source_files_sha256']==pins,
         'Full original complementary source bindings')
    directory=epoch/complement.COMPLEMENT;review=epoch/complement.REVIEW
    for action,output in(('construct','CONSTRUCTED.json'),('replay','REPLAY.json')):
        cap=epoch/('runs/cutoff5_20261020/high/complement_'+action+'01')
        verify_capture(epoch,cap,directory,['-B','protocol.py',action,'PLAN.json',output])
        complement_worker.captured_integration(epoch,directory,action)
        need(digest(directory/output)==value['constructed_sha256'if action=='construct'else'replay_sha256'],
             'Exact entire new complementary integration output')
    # This rechecks algebraic acceptor/readback comparisons and their controls,
    # NOT an integral, interval kernel, Gaussian leaf, or original integration.
    arithmetic=complement_worker.validate_two_results(directory/'accept.py',review/'check.py',directory)
    need(all(exact(value[k],v)for k,v in arithmetic.items()),'All independently checked complementary arithmetic facts')
    need(value['native_arithmetic_acceptor_sha256']==complement_worker.NATIVE_SHA
         and value['independent_arithmetic_readback_sha256']==complement_worker.READBACK_SHA,
         'Original arithmetic/readback sources, not a modified acceptance rule')
    return declaration(schema='C5_SOURCE_BOUND_COMPLEMENT_V1',n=5,target=str(TARGET),
        **complement_domain(value,evidence),
        arithmetic_artifact=dict(path=str(path),sha256=digest(path)),
        supervisor_report=dict(path=str(report_path),sha256=digest(report_path)),
        retained_extended_Fourier_premise='Same reviewed cotangent/stable-range extension and Prawitz/scalar formulas as parent evidence',
        extension_evidence=evidence.declaration())
