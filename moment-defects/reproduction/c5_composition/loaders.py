"""Read NEW arithmetic artifacts and pinned source bytes, never old PASS as proof.

These are post-hoc implications. A controller must separately observe its own
guarded executions; a file claiming freshness does not authenticate history.
No numerical kernel, native acceptor, or subprocess is executed here.
"""
from __future__ import annotations
import ast
from copy import deepcopy
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import zipfile

from ..all_indices.c5_counts import (BASE,FINAL,FINAL_SHA,ARCHIVE_BYTES,ARCHIVE_SHA,INDEX_SHA,
                                     catalog,digest,need,unique)
from ..all_indices.c5_high_one import read,source_at
from ..all_indices.c5_inputs import extended,safe_relative
from ..all_indices.c5_acquisition_plan import RESOURCE_JOBS,description,inspect_job
from ..all_indices.c5_resources_arithmetic import summarize_job
from ..all_indices import c5_resource_accept_port as port
from ..all_indices.c5_parent_evidence import (checked_json,report_epoch,regular_owned,verify_graph,ParentEvidence)
from ..all_indices.c5_parent_facts import entails_profile
from .core import canonical_sha,constants,declaration,exact,panel,same_resource_initial


def final_graph(cache):
    final=source_at(cache,FINAL)
    need(digest(final)==FINAL_SHA,'Original graph is an immutable SOURCE index only')
    graph=read(final)['files_sha256'];need(len(graph)==16576,'Complete original C5 source index')
    return graph


def load_resource(cache,report_path,initial,evidence,*,work_root=None):
    need(type(evidence)is ParentEvidence,'Checked typed parent evidence')
    # The RESOURCE supervisor deliberately returns extended-length Windows
    # paths. Use that SAME namespace for the containment root and selector;
    # never weaken containment or rewrite any old JSON/capture path.
    work_root=extended(Path(work_root)if work_root is not None else BASE/'work')
    report_path=extended(Path(report_path))
    cache=extended(Path(cache));graph=final_graph(cache)
    epoch=report_epoch(report_path,'RESOURCE_ARITHMETIC_RESULT.json',work_root)
    report=checked_json(epoch,report_path)
    need(report['scope']=='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY'
         and report['fresh_resource_arithmetic']is True and report['fresh_arithmetic']is False
         and report['fresh_parent_fact_joins_verified']is False
         and report['register_as_c5_resources']is False
         and report['all_index_conclusion_verified']is False
         and report['original_final_graph_sha256']==FINAL_SHA,'Only a NEW conditional resource arithmetic artifact')
    jobs=[j for j in RESOURCE_JOBS if j.job_id==report['job_id']]
    need(len(jobs)==1,'One exact original resource selection');job=jobs[0]
    pins=inspect_job(cache,graph,job,include_sources=True)['source_files_sha256']
    need(report['source_files_sha256']==pins,'Exact selected resource closure, no substituted sources')
    verify_graph(epoch,pins)
    request_path=regular_owned(epoch,epoch/'RESOURCE_REQUEST.json')
    request=checked_json(epoch,request_path);request_pin=digest(request_path)
    need(request['schema']=='FRESH_C5_RESOURCE_ARITHMETIC_REQUEST_V1'
         and exact(request['job'],description(job))and request['source_files_sha256']==pins
         and request['original_final_graph_sha256']==FINAL_SHA
         and request['fresh_parent_fact_joins_verified']is False,'Full source-bound current resource request')
    adapter=regular_owned(epoch,epoch/'c5_resource_accept_port.py')
    need(digest(adapter)==request['adapter_sha256']==report['metadata_source_port_adapter_sha256']
         ==digest(Path(port.__file__)),'Exact published metadata-only source port')
    port.preflight_capture(epoch,request,request_path,request_pin,adapter)
    capture=epoch/job.capture
    need(Path(report['real_replay_capture']).resolve()==capture.resolve()
         and report['real_replay_metadata_sha256']==digest(capture/'metadata.json')
         and report['actual_os_replay_command']==port.worker_command(adapter,request_path,request_pin,'replay')
         and report['actual_os_accept_command']==port.worker_command(adapter,request_path,request_pin,'accept'),
         'Exact report/capture/actual-command bindings, not native-semantic argv substituted for an OS command')
    for stage in('replay','accept'):
        path=epoch/('PORT_'+stage.upper()+'_REPORT.json')
        result=checked_json(epoch,path,report[stage+'_source_port_report_sha256'])
        raw=regular_owned(epoch,epoch/job.directory/(stage+'.py')).read_bytes()
        _,edits=port.transform(raw,job.family,stage)
        need(exact(result,report[stage+'_source_port_report'])and result['stage']==stage
             and result['original_source_sha256']==hashlib.sha256(raw).hexdigest()
             and result['adapter_sha256']==digest(adapter)and result['request_sha256']==request_pin
             and exact(result['exact_ast_transforms'],edits)
             and result['scope']=='NEW_METADATA_ONLY_SOURCE_PORT_NOT_UNCHANGED_NATIVE_WINDOWS_EXECUTION'
             and result['original_source_bytes_modified']is False and result['old_json_or_hashes_modified']is False
             and result['mathematical_expressions_and_all_native_negative_controls_unchanged']is True,
             'Exact metadata-only source transformation, not a weakened mathematical acceptor')
    replay=checked_json(epoch,epoch/job.output_paths[0],report['replay_sha256'])
    accepted=checked_json(epoch,epoch/job.output_paths[1],report['native_accept_sha256'])
    need(accepted['resource_replay_sha256']==digest(epoch/job.output_paths[0]),'Accepted entire current resource output')
    verify_graph(epoch,accepted['files_sha256'])
    prepared=checked_json(epoch,epoch/job.prepared)
    candidate=checked_json(epoch,epoch/job.case_directory/'INITIAL.json')
    recomputed=summarize_job(epoch,job,prepared,candidate,replay,accepted)
    need(all(k in report and exact(report[k],v)for k,v in recomputed.items()),
         'Every exported canonical resource answer/profile equals its native artifact')
    initial_edge=same_resource_initial(report,initial)
    profile=deepcopy(report['parent_initial']['profile'])
    profile['cap']=job.owncap
    # Resource caps may be stronger than INITIAL caps. They require their OWN
    # same-law whole-domain HIGH/support/owncap implication, not just the INITIAL edge.
    edges=entails_profile(profile,job.high,job.owncap,evidence.facts,evidence.global_owncap)
    return declaration(schema='C5_SOURCE_BOUND_JOINED_RESOURCE_V1',job_id=job.job_id,
        initial_job=job.initial_parent,n=5,band=job.band,sector=job.sector,
        rho_interval=report['rho_interval'],beta_interval=report['beta_interval'],
        selected_probability_panels=report['selected_probability_panels'],
        excluded=report['excluded'],retained=report['retained'],
        full_canonical_resource_rows=report['full_canonical_resource_rows'],
        initial_identity_edge=initial_edge,numerical_parent_edges=edges['edges'],
        resource_report=dict(path=str(report_path),sha256=digest(report_path)),
        native_replay=dict(path=report['replay_path'],sha256=report['replay_sha256']),
        native_accept=dict(path=report['native_accept_path'],sha256=report['native_accept_sha256']),
        recorded_capture_metadata_sha256=report['real_replay_metadata_sha256'],
        required_analytic_premises=initial['retained_analytic_premises'],
        metadata_port_scope=report['source_port_scope'])


def source_functions(cache,graph,band):
    """Use the original pinned interface/geometry FUNCTION ASTs, not their main.

    The extracted functions perform rational joins and tree geometry only.
    No evaluator/import/capture reader/old acceptance is executed.
    """
    folder=('audit/count5_readback_v1'if band in('B0','BN')else
            'audit/count5_sector_readback_v1'if band=='B2'else'high/B3_count_readback_v1')
    name='work/cutoff5_20261020/'+folder+'/common.py'
    path=source_at(cache,name);need(digest(path)==graph[name],'Frozen original mathematical interface helper')
    tree=ast.parse(path.read_bytes());names={'need','same','integer','rational','floorgrid','ceilgrid',
        'sqrtlo','polymin','interface','geometry'}
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in names]
    need({n.name for n in functions}==names and len(functions)==len(names),'Exactly the ten dependency-closed rational/geometry functions')
    constants_by_name={}
    for node in tree.body:
        if (isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)
            and node.targets[0].id in('BANDS','EMPTY')):
            constants_by_name[node.targets[0].id]=ast.literal_eval(node.value)
    need(set(constants_by_name)=={'BANDS','EMPTY'},'Original exact domain and leaf-classification constants')
    namespace=dict(F=F,deepcopy=deepcopy,Counter=Counter,isqrt=isqrt,CElo=constants(),**constants_by_name)
    b3_binding=None
    if band=='B3':
        check_name='work/cutoff5_20261020/high/B3_count_readback_v1/check.py'
        check_path=source_at(cache,check_name)
        need(digest(check_path)==graph[check_name],'Original source of the installed B3 constant')
        assignments=[]
        for node in ast.parse(check_path.read_bytes()).body:
            if(not isinstance(node,ast.Assign)or len(node.targets)!=1):continue
            target=node.targets[0]
            if(isinstance(target,ast.Subscript)and isinstance(target.value,ast.Attribute)
               and isinstance(target.value.value,ast.Name)and target.value.value.id=='c'
               and target.value.attr=='BANDS'and isinstance(target.slice,ast.Constant)
               and target.slice.value=='B3'):
                assignments.append(node)
        need(len(assignments)==1,'Exactly one original c.BANDS[B3] installation')
        installed=ast.literal_eval(assignments[0].value)
        need(installed==('237/200','6/5',None,None,None,None),
             'Unchanged literal B3 whole-band installation, not a new domain')
        namespace['BANDS']['B3']=installed
        b3_binding=dict(path=check_name,sha256=graph[check_name],
            installed_assignment_ast=ast.dump(assignments[0],include_attributes=False))
    selected=ast.Module(body=functions,type_ignores=[]);ast.fix_missing_locations(selected)
    exec(compile(selected,str(path),'exec'),namespace)
    selected_constants=dict(BANDS={k:list(v)for k,v in namespace['BANDS'].items()},
        EMPTY=sorted(namespace['EMPTY']),CElo=str(namespace['CElo']))
    core_source=Path(__file__).with_name('core.py')
    return namespace,dict(path=name,sha256=graph[name],functions=sorted(names),
        selected_ast_sha256=hashlib.sha256(ast.dump(selected,include_attributes=False).encode()).hexdigest(),
        selected_constants=selected_constants,selected_constants_sha256=canonical_sha(selected_constants),
        B3_installation_source=b3_binding,
        CElo_builder=dict(path=str(core_source),sha256=digest(core_source),function='constants',
            scope='Existing exact directed Machin80/40 and integer-square-root C_E lower enclosure; no acceptance change'),
        stdlib_dependencies=dict(F='fractions.Fraction',deepcopy='copy.deepcopy',
                                 Counter='collections.Counter',isqrt='math.isqrt'))


@dataclass(frozen=True)
class CountArtifact:
    original_capsule: str
    receipt: dict
    contract: dict
    forest_statistics: dict
    bindings: dict


def bind_count_header(capsule,original_capsule,graph,accepted,forest,manifest):
    """No self-hash is expected INSIDE a forest; its consumer binds its bytes."""
    for name,key in(('COUNT_FOREST.json','forest_sha256'),('contract.json','contract_sha256'),
                    ('count_protocol.py','checker_sha256')):
        pin=digest(capsule/name)
        need(graph.get(original_capsule+'/'+name)==pin==accepted[key],
             'Exact pinned/native-consumer count source binding: '+name)
        if name!='COUNT_FOREST.json':
            need(forest[key]==pin,'Exact contract/checker commitment inside forest header')
    need(exact(accepted['kernel_sha256'],manifest)and exact(forest['kernel_sha256'],manifest),
         'Entire unchanged native arithmetic kernel')


def load_counts(cache,archive,progress_path,*,work_root=None):
    """Full295 forest identities/geometries, NOT mathematical leaf reevaluation."""
    work_root=Path(work_root)if work_root is not None else BASE/'work'
    cache=extended(Path(cache));graph=final_graph(cache)
    archive=Path(archive)
    need(archive.is_file()and not archive.is_symlink()and archive.stat().st_size==ARCHIVE_BYTES
         and digest(archive)==ARCHIVE_SHA,'Exact original source archive for the selected295 inventory')
    with zipfile.ZipFile(archive)as zipped:rows,pinned_graph=catalog(zipped)
    need(pinned_graph==graph,'Same complete original selected source graph')
    epoch=report_epoch(progress_path,'C5_COUNTS_PROGRESS.jsonl',work_root)
    progress=regular_owned(epoch,progress_path)
    need(progress.stat().st_size<=4*1024**2,'Bounded complete count progress index')
    before=digest(progress)
    events=[json.loads(line,object_pairs_hook=unique)for line in progress.read_text(encoding='utf-8').splitlines()]
    need(digest(progress)==before and len(events)==295,'Complete immutable NEW count run index')
    result=checked_json(epoch,epoch/'C5_COUNTS_RESULT.json')
    need(result['scope']=='ALL_295_C5_COUNT_FORESTS_FRESHLY_REPLAYED'
         and result['source_archive_sha256']==ARCHIVE_SHA
         and result['source_index_sha256']==INDEX_SHA
         and result['resource_support_fourier_initial_and_gapfree_verified_by_this_stage']is False
         and result['all_index_conclusion_verified']is False,'New count-only batch artifact, not original final PASS')
    functions={};artifacts=[];seen=set();total_nodes=total_leaves=0
    for ordinal,(row,event)in enumerate(zip(rows,events)):
        need(type(event['ordinal'])is int and event['ordinal']==ordinal
             and event['original_capsule']==row['cwd']and row['cwd']not in seen,
             'Every original count selection exactly once in its canonical order')
        seen.add(row['cwd'])
        receipt_path=BASE.joinpath(*safe_relative(event['receipt']))
        # The count coordinator deliberately uses one separate private work
        # directory per mathematical worker, not the progress directory itself.
        regular_owned(work_root,receipt_path)
        need(receipt_path.name=='COUNT_ACCEPTED.json'and receipt_path.parent.name=='capsule'
             and receipt_path.parent.parent.parent.resolve()==work_root.resolve(),'Exact owned new count capsule')
        capsule=receipt_path.parent;work=capsule.parent
        accepted=checked_json(work,receipt_path,event['receipt_sha256'])
        contract=checked_json(work,capsule/'contract.json')
        forest=checked_json(work,capsule/'COUNT_FOREST.json')
        need(type(contract['n'])is int and contract['n']==5 and type(contract['index'])is int
             and contract['index']==row['index']and contract['resource_verified']is False
             and contract['cutoff_proved']is False and type(contract['rows'])is list
             and len(contract['rows'])==1,'Unchanged literal conditional count contract')
        for original,pin in graph.items():
            if original.startswith(row['cwd']+'/')and not original.endswith('/COUNT_ACCEPTED.json'):
                name=original[len(row['cwd'])+1:]
                need(Path(name).name==name and digest(regular_owned(work,capsule/name))==pin,
                     'Every original count source/forest byte preserved')
        manifest=checked_json(work,capsule/'KERNEL_COPY_MANIFEST.json')['files']
        verify_graph(capsule,manifest)
        band=contract['band'];index=contract['index']
        if band not in functions:functions[band]=source_functions(cache,graph,band)
        helper,binding=functions[band]
        stats=helper['geometry'](forest,contract['rows'][0],5)
        need(accepted['status']==f'PASS_FRESH_CONDITIONAL_ACTUAL5_GAMMA_SHARP_{band}_JOINT_PANEL{index}'
             and type(accepted['n'])is int and accepted['n']==5
             and type(accepted['index'])is int and accepted['index']==index
             and exact(accepted['statistics'],stats)
             and type(accepted['fresh_leaf_evaluations'])is int
             and accepted['fresh_leaf_evaluations']==stats['leaves']
             and len(accepted['negative_controls'])==len(set(accepted['negative_controls']))==24,
             'Whole count artifact and all native corruption controls, not an old success string alone')
        bind_count_header(capsule,row['cwd'],graph,accepted,forest,manifest)
        output=regular_owned(work,work/'c5-count-native.stdout.txt')
        need(output.stat().st_size<=16*1024**2,'Bounded recorded native output')
        need(exact(json.loads(output.read_text(encoding='utf-8'),object_pairs_hook=unique),accepted),
             'Complete recorded native canonical answer, not a truncated acceptance line')
        need(type(event['nodes'])is int and type(event['leaves'])is int
             and event['nodes']==stats['nodes']and event['leaves']==stats['leaves'],
             'Actual complete forest statistics match the selected progress row')
        total_nodes+=stats['nodes'];total_leaves+=stats['leaves']
        artifacts.append(CountArtifact(row['cwd'],accepted,contract,stats,
            dict(receipt=str(receipt_path),receipt_sha256=digest(receipt_path),
                 contract_sha256=digest(capsule/'contract.json'),forest_sha256=digest(capsule/'COUNT_FOREST.json'),
                 recorded_native_stdout_sha256=digest(output),interface_source=binding)))
    need((len(artifacts),total_nodes,total_leaves)==(295,148586,75178)
         and result['forests']==295 and result['original_count_roots']==1770
         and result['nodes']==total_nodes and result['leaves']==total_leaves,'Complete fixed295/1770 count census')
    return tuple(artifacts)
