"""Exact RESOURCE -> COUNTS -> closed C5-domain implications.

This module NEVER declares a fresh theorem from post-hoc files. In addition
to these checks, a future end-to-end controller must observe its own guarded
subprocesses and retain the stated analytic/published hypotheses.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

from ..all_indices.c5_counts import BASE,FINAL,digest,need
from ..all_indices.c5_high_one import source_at,read
from ..all_indices.c5_inputs import extended
from ..all_indices.c5_acquisition_plan import INITIAL_JOBS,RESOURCE_JOBS
from ..all_indices.c5_initial_join import load_initial_join
from ..all_indices.c5_parent_evidence import load_parent_evidence,checked_json
from .core import (B2,B3,CASES,COUNT_TARGET,TARGET,canonical_sha,closed_union,
                   constants,declaration,domain,exact,panel)
from .loaders import CountArtifact,final_graph,load_resource,load_counts,source_functions
from .auxiliary import load_corner,load_complement


def physical_gap(helper,row,cfg,endpoint_product):
    """Original exact gamma/physical gap derivation in all three readbacks."""
    raw=row['result']['raw_row'];r=row['result']['result']
    need(list(map(F,cfg['acquired_gamma']))==[helper['floorgrid'](raw['gamma_lo'],10**6),
         helper['ceilgrid'](raw['gamma_hi'],10**6)],'Entire signed acquired gamma interval')
    sl=F(3162277660,10**9)
    rl,D,gh,mu=map(F,[r['rho_lo'],r['D'],raw['gamma_hi'],raw['mean_hi']])
    price=max((sl-1)*rl,sl*rl-gh)-D
    if endpoint_product:
        price=max(price,6*F(row['result']['initial']['mean_lo'])*F(raw['A'])*F(raw['B']))
    need(sl*sl<10 and price>0 and mu>0,'Positive same-law physical gap price')
    gap=max(F(raw['A'])+F(raw['B']),helper['sqrtlo'](
        max(F(0),2*rl-2*D/(sl-1),2*price/(3*mu)),10**12))
    pl,pu=map(F,cfg['p'])
    inward=helper['ceilgrid'](1-gap*helper['sqrtlo'](min(pl*(1-pl),pu*(1-pu)),10**12),10**6)
    need(F(cfg['geometry_gap_lower'])==gap and F(cfg['acquired_inward_upper'])==inward,
         'Independently derived physical inward domain, no silent radial strengthening')


def join_count(cache,graph,count,resource_row,case,helper):
    need(type(count)is CountArtifact,'Count must come from the full source-bound loader')
    obj=count.contract;cfg=obj['rows'][0];index=obj['index'];band=case.split('.')[0]
    need(type(index)is int and type(resource_row['index'])is int and resource_row['index']==index
         and obj['band']==band and exact(resource_row['p'],panel(index)),
         'Same exact selected count/resource closed p panel')
    source=obj['resource_path']
    need(graph.get(source)==obj['resource_sha256'],'Original source-row commitment belongs to the pinned graph')
    original=source_at(cache,source)
    need(digest(original)==obj['resource_sha256'],'Original resource-row source bytes, not an old acceptance')
    row=read(original)
    need(type(row['index'])is int and row['index']==index and row['status']=='RESOURCE_ROW_DIAGNOSTIC'
         and exact(row['result'],resource_row['result'])and row['result']['excluded']is False,
         'ENTIRE acquired canonical resource answer equals the newly read arithmetic artifact')
    helper['interface'](row,cfg,band,index,5)
    physical_gap(helper,row,cfg,'/count5_prepare_v4/'in count.original_capsule)
    rho,_=domain(case);r=row['result']['result']
    if band in('B0','BN'):
        need(F(r['rho_hi'])<=F(cfg['rho_upper'])<=F(rho[1]),'Full acquired rho upper scope')
    else:
        need(F(rho[0])==F(r['rho_lo'])==F(cfg['rho_lower'])
             and F(r['rho_hi'])<=F(cfg['rho_upper'])<=F(rho[1]),'Whole exact signed-beta sector rho scope')
    need(count.forest_statistics['maximum_score']is not None
         and 0<=F(count.forest_statistics['maximum_score'])<COUNT_TARGET,
         'Strict original count target on every retained panel')
    return dict(index=index,p=panel(index),closure='count',
                count_source=count.original_capsule,resource_source=source,
                resource_answer_sha256=canonical_sha(resource_row['result']),
                statistics=count.forest_statistics,bindings=count.bindings)


def whole_panels(case,resources,counts):
    """Pure1200-panel inventory; identities/geometry are checked separately."""
    expected_parent='initial.'+case
    selected={}
    for resource in resources:
        need(resource['initial_job']==expected_parent and resource['n']==5
             and type(resource['n'])is int,'Same exact INITIAL case for every selected resource variant')
        rho,beta=domain(case)
        need(resource['rho_interval']==rho and exact(resource['beta_interval'],beta),
             'Exact full acquired rho/signed-beta rectangle')
        rows=resource['full_canonical_resource_rows']
        need(type(rows)is list and exact([r['index']for r in rows],resource['selected_probability_panels']),
             'Ordered entire selected resource rows')
        for row in rows:
            index=row['index'];need(type(index)is int and index not in selected
                 and row['p']==panel(index)and type(row['result']['excluded'])is bool
                 and row['canonical_result_sha256']==canonical_sha(row['result']),
                 'Disjoint exact resource variant partition and complete canonical answer')
            selected[index]=row
    need(sorted(selected)==list(range(100)),'All100 closed p panels without duplication or omissions')
    expected=[i for i in range(100)if not selected[i]['result']['excluded']]
    need(type(counts)is dict and sorted(counts)==expected
         and all(type(i)is int for i in counts),'ALL AND ONLY retained panels have independent count closures')
    return selected


def finish_domains(cases,corner,complement):
    need(type(cases)is list and [c['case']for c in cases]==list(CASES),'All twelve exact case closures once')
    for case in cases:
        need(all(type(case[k])is int and case[k]>=0 for k in
             ('panels','resource_exclusions','count_forests','count_roots','count_nodes','count_leaves')),
             'Literal nonnegative complete case census')
        rows=case['coverage'];retained=[]
        need(type(rows)is list and len(rows)==100,'Entire100-panel case coverage')
        for i,row in enumerate(rows):
            need(type(row['index'])is int and row['index']==i and row['p']==panel(i)
                 and row['closure']in('resource','count'),'Each exact closed seam and proved closure kind')
            if row['closure']=='count':
                stats=row['statistics']
                need(type(stats['nodes'])is int and type(stats['leaves'])is int
                     and stats['leaves']>=6 and stats['nodes']==2*stats['leaves']-6
                     and stats['nodes']<=50000 and 0<=F(stats['maximum_score'])<COUNT_TARGET,
                     'Complete positive six-root forest and strict exact score')
                retained.append(row)
        need(case['count_forests']==len(retained)and case['resource_exclusions']==100-len(retained)
             and case['count_roots']==6*len(retained)
             and case['count_nodes']==sum(r['statistics']['nodes']for r in retained)
             and case['count_leaves']==sum(r['statistics']['leaves']for r in retained)
             and F(case['maximum_count_score'])==max((F(r['statistics']['maximum_score'])for r in retained),default=F(0)),
             'Exact case sums/maxima derived from every actual closure, no balanced-negative census')
    need(sum(c['resource_exclusions']for c in cases)==905
         and sum(c['count_forests']for c in cases)==295
         and sum(c['count_roots']for c in cases)==1770
         and sum(c['count_nodes']for c in cases)==148586
         and sum(c['count_leaves']for c in cases)==75178,'Complete fixed end-to-end finite census')
    for case in cases:
        need(case['rho']==domain(case['case'])[0]and exact(case['beta'],domain(case['case'])[1])
             and case['panels']==100,'All exact literal full moment domains')
    need(corner['rho']==['477/400','6/5']and corner['beta']==['17/50',str(B3)],'Whole missing positive-beta corner')
    checks=closed_union([domain('B2.S'+str(i))for i in range(4)],
                        ['23/20','237/200'],[-B2,B2])
    checks+=closed_union([domain(c)for c in CASES if c.startswith('B3.')]
                         +[(corner['rho'],corner['beta'])],['237/200','6/5'],[-B3,B3])
    need(complement['rho_finite']==['6/5','7361/4000']
         and complement['published_tail']==dict(rho_lower='7361/4000',upper='819/2000',
             retained_published_premise='Shevtsova2013 iid .3031*(1+.646/rho)'),
         'Whole final moment seam through infinity')
    return declaration(schema='C5_SOURCE_BOUND_DOMAIN_COMPOSITION_V1',
        scope='IF_THE_BOUND_ARITHMETIC_WAS_EXECUTED_AND_ANALYTIC_PREMISES_HOLD_THEN_C5_LE_CE',
        n=5,regions=cases,probability_panel_instances=1200,resource_exclusions=905,
        count_forests=295,count_roots=1770,count_nodes=148586,count_leaves=75178,
        ce_lower=str(constants()),arrangement_checks=checks,corner=corner,complement=complement,
        retained_analytic_premises=[
            'Global all-law C4<=CE; unrestricted fixed-index attainment and positive closed-contact/support reduction.',
            'The source-bound continuous INITIAL/resource moment, signed-support and shared-budget implications.',
            'The reviewed count-probability/filter inequalities and source-specific outward/endpoint-product ports.',
            'Prawitz smoothing and the reviewed Shevtsova moment/scalar and extended Fourier inputs.',
            'Every cited arithmetic artifact must arise from the owning controller\'s observed guarded execution.'])


def compose(cache,archive,initial_paths,resource_paths,counts_progress,corner_path,complement_path,evidence,
            *,work_root=None):
    """Recheck all source-bound mathematical implications; NO fresh theorem flag."""
    cache=extended(Path(cache));graph=final_graph(cache)
    need(set(initial_paths)=={j.job_id for j in INITIAL_JOBS}
         and set(resource_paths)=={j.job_id for j in RESOURCE_JOBS},'All12 INITIAL and15 RESOURCE artifacts explicitly supplied')
    initials={key:load_initial_join(cache,path,evidence,work_root=work_root)for key,path in initial_paths.items()}
    resources={}
    for job in RESOURCE_JOBS:
        value=load_resource(cache,resource_paths[job.job_id],initials[job.initial_parent],evidence,work_root=work_root)
        need(value['job_id']==job.job_id,'The supplied RESOURCE path has exactly its declared selector')
        resources[job.job_id]=value
    counts=load_counts(cache,archive,counts_progress,work_root=work_root)
    by_resource={}
    for count in counts:
        key=(count.contract['resource_path'],count.contract['index'])
        need(key not in by_resource,'No duplicated original count-resource source selector')
        by_resource[key]=count
    # Match each source row to the unique complete fresh resource answer; the
    # identity check below compares all raw budgets, history and signed moments.
    used=set();case_results=[]
    for case in CASES:
        chosen=[resources[j.job_id]for j in RESOURCE_JOBS if j.initial_parent=='initial.'+case]
        available={}
        for count in counts:
            source=count.contract['resource_path'];pin=count.contract['resource_sha256']
            need(graph.get(source)==pin,'Selected resource-row input belongs to the immutable source graph')
            original=source_at(cache,source)
            row=checked_json(cache,original,pin)
            matches=[r for resource in chosen for r in resource['full_canonical_resource_rows']
                     if r['index']==count.contract['index']and exact(r['result'],row['result'])]
            if matches:
                index=count.contract['index'];need(index not in available,'Exactly one selected count per case/panel')
                available[index]=count
        rows=whole_panels(case,chosen,available)
        band=case.split('.')[0];helper,interface_binding=source_functions(cache,graph,band)
        closures=[]
        for index in range(100):
            if rows[index]['result']['excluded']:
                closures.append(dict(index=index,p=panel(index),closure='resource',
                                     resource_answer_sha256=canonical_sha(rows[index]['result'])))
            else:
                count=available[index];need(count.original_capsule not in used,'No count proof reused for another source law')
                used.add(count.original_capsule)
                closures.append(join_count(cache,graph,count,rows[index],case,helper))
        retained=[r for r in closures if r['closure']=='count'];rho,beta=domain(case)
        case_results.append(dict(case=case,rho=rho,beta=beta,panels=100,
            resource_exclusions=100-len(retained),count_forests=len(retained),count_roots=6*len(retained),
            count_nodes=sum(r['statistics']['nodes']for r in retained),
            count_leaves=sum(r['statistics']['leaves']for r in retained),
            maximum_count_score=str(max((F(r['statistics']['maximum_score'])for r in retained),default=F(0))),
            coverage=closures,interface_source=interface_binding,
            resource_artifact_bindings=[r['resource_report']for r in chosen]))
    need(len(used)==295,'No selected count omitted, repeated, or used on an unrelated resource domain')
    corner=load_corner(cache,corner_path,work_root=work_root)
    complement=load_complement(cache,complement_path,evidence,work_root=work_root)
    result=finish_domains(case_results,corner,complement)
    index_name='work/cutoff5_20261020/root/final_composition_v2/ANALYTIC_SOURCES.json'
    index=source_at(cache,index_name);need(digest(index)==graph[index_name],'Original explicit continuous-source boundary')
    documents=read(index);need(documents['schema']=='C5_CONTINUOUS_PROOF_SOURCE_INDEX_V1'
                             and len(documents['files'])>=20,'Complete original named continuous source list')
    proof_pins={name:graph[name]for name in documents['files']}
    need(all(digest(source_at(cache,name))==pin for name,pin in proof_pins.items()),'Every stated analytic source still bound')
    result.update(continuous_proof_source_sha256=proof_pins,
                  original_final_used_as='SOURCE_HASH_INDEX_ONLY_NOT_PRIOR_EXECUTION_OR_THEOREM',
                  parent_evidence=evidence.declaration(),
                  initial_artifacts=[value['initial_arithmetic_report']for value in initials.values()])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--inputs',type=Path,required=True,help='Explicit12/15 paths plus observed-run artifact selectors')
    args=parser.parse_args();need(__debug__ and not __import__('sys').flags.optimize,'No optimized checking')
    need(args.inputs.is_file()and not args.inputs.is_symlink()and args.inputs.stat().st_size<=1024**2,
         'Bounded explicit artifact selector, not arbitrary unbounded JSON')
    inputs=read(args.inputs)
    evidence=load_parent_evidence(args.cache,inputs['support'],inputs['high'],inputs['owncaps'])
    result=compose(args.cache,args.archive,inputs['initials'],inputs['resources'],inputs['counts_progress'],
                   inputs['corner'],inputs['complement'],evidence)
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
