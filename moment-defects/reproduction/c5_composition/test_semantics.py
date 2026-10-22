"""Bounded rational/metadata tests. No interval/leaf/integration evaluator runs."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path
import unittest

from ..all_indices.c5_counts import BASE
from ..all_indices.c5_counts import digest
from ..all_indices.c5_high_one import source_at,read
from ..all_indices.c5_acquisition_plan import INITIAL_JOBS,RESOURCE_JOBS
from ..all_indices.c5_parent_evidence import ParentEvidence
from ..all_indices.c5_parent_facts import (BoundFact,GlobalOwncapFact,support_facts,high_facts,
                                          owncap_facts,entails_profile)
from ..all_indices.c5_high_one import VARIANTS as HIGH_VARIANTS,HIGH_ROOT
from ..all_indices.c5_owncaps_one import VARIANTS as OWN_VARIANTS,HIGH
from ..all_indices.c5_resources_arithmetic import summarize_job
from ..all_indices.c5_inputs import extended
from .core import (B2,B3,CASES,canonical_sha,closed_union,constants,declaration,domain,
                   exact,panel,same_resource_initial)
from .auxiliary import corner_domain,complement_domain
from .compose import whole_panels,physical_gap,finish_domains,join_count
from .loaders import CountArtifact,final_graph,source_functions,bind_count_header


class ExactCoreTests(unittest.TestCase):
    def test_no_bool_integer_alias(self):
        self.assertFalse(exact(True,1));self.assertFalse(exact({'a':[0]},{'a':[False]}))
        for bad in(True,False,-1,100,1.0):
            with self.assertRaises(ValueError):panel(bad)

    def test_targets_and_arrangement_close_all_faces(self):
        self.assertLess(F(4097,10000),constants())
        rectangles=[domain(c)for c in CASES if c.startswith('B3.')]
        corner=(['477/400','6/5'],['17/50',str(B3)])
        closed_union(rectangles+[corner],['237/200','6/5'],[-B3,B3])
        for changed in(rectangles,rectangles+[(corner[0],['341/1000',str(B3)])]):
            with self.assertRaises(ValueError):closed_union(changed,['237/200','6/5'],[-B3,B3])
        closed_union([domain('B2.S'+str(i))for i in range(4)],['23/20','237/200'],[-B2,B2])

    def test_all_reader_declarations_deny_execution_and_theorem(self):
        result=declaration(schema='synthetic')
        self.assertIs(result['source_bound_semantic_implications_verified'],True)
        for key in('execution_observed_by_this_reader','fresh_arithmetic',
                   'fresh_parent_fact_joins_verified','c5_theorem_freshly_verified','all_index_conclusion_verified'):
            self.assertIs(result[key],False)
        with self.assertRaises(ValueError):declaration(fresh_arithmetic=True)


class InitialIdentityTests(unittest.TestCase):
    def setUp(self):
        self.initial=dict(schema='C5_SOURCE_BOUND_JOINED_INITIAL_V1',
            source_bound_parent_implications_verified=True,execution_observed_by_this_reader=False,
            fresh_parent_fact_joins_verified=False,job_id='initial.B0',n=5,band='B0',sector=None,
            input_candidate_sha256='a'*64,profile=dict(invariants=dict(rho_lo='1',rho='11/10',beta_lo='-1/3',beta_hi='1/3')),
            rho_interval=['1','11/10'],beta_interval=['-1/3','1/3'],band_interval=None,beta_enclosing_interval=None,partition_kind=None,
            stages=9,final_invariants={'D':'1/10'},final_cover_sha256='b'*64,
            cells_per_stage=2592,validated_closed_p_indices=list(range(100)),final_active=3,final_gap_active=3)
        self.resource=dict(n=5,band='B0',sector=None,rho_interval=['1','11/10'],beta_interval=None,
            parent_initial=dict(job_id='initial.B0',
            candidate_sha256='a'*64,**{k:deepcopy(self.initial[k])for k in
                ('profile','band_interval','beta_enclosing_interval',
                 'partition_kind','stages','final_invariants','final_cover_sha256')}))

    def test_full_identity_passes_without_promoting_freshness(self):
        edge=same_resource_initial(self.resource,self.initial)
        self.assertEqual(edge['candidate_sha256'],'a'*64)

    def test_every_numerical_or_candidate_mismatch_is_rejected(self):
        changes=[lambda x:x['parent_initial'].update(candidate_sha256='c'*64),
            lambda x:x['parent_initial'].update(profile={'all':'other'}),
            lambda x:x.update(rho_interval=['1','6/5']),
            lambda x:x.update(beta_interval=['-1','1']),
            lambda x:x['parent_initial'].update(stages=4),
            lambda x:x['parent_initial'].update(final_cover_sha256='c'*64),
            lambda x:x.update(sector=False),lambda x:x.update(n=True)]
        for change in changes:
            damaged=deepcopy(self.resource);change(damaged)
            with self.assertRaises(ValueError):same_resource_initial(damaged,self.initial)
        for key in('execution_observed_by_this_reader','fresh_parent_fact_joins_verified'):
            damaged=deepcopy(self.initial);damaged[key]=True
            with self.assertRaises(ValueError):same_resource_initial(self.resource,damaged)


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.rows=[]
        for i in range(100):
            answer={'excluded':i!=50,'entire':{'D':'1/10','history':[]}}
            self.rows.append(dict(index=i,p=panel(i),result=answer,canonical_result_sha256=canonical_sha(answer)))
        self.resource=dict(initial_job='initial.B0',n=5,rho_interval=['1','11/10'],beta_interval=None,
            selected_probability_panels=list(range(100)),full_canonical_resource_rows=self.rows)

    def test_entire_closed_probability_cover(self):
        rows=whole_panels('B0',[self.resource],{50:object()})
        self.assertEqual(len(rows),100)

    def test_missing_duplicate_altered_or_unproved_panel_is_rejected(self):
        for mutation in(lambda z:z['full_canonical_resource_rows'].pop(),
                        lambda z:z['full_canonical_resource_rows'][0].update(index=False),
                        lambda z:z['full_canonical_resource_rows'][0].update(p=['0','1/200']),
                        lambda z:z['full_canonical_resource_rows'][0]['result']['entire'].update(D='0'),
                        lambda z:z.update(rho_interval=['1','6/5'])):
            value=deepcopy(self.resource);mutation(value)
            with self.assertRaises(ValueError):whole_panels('B0',[value],{50:object()})
        for counts in({}, {49:object()}, {50:object(),51:object()}):
            with self.assertRaises(ValueError):whole_panels('B0',[self.resource],counts)
        with self.assertRaises(ValueError):whole_panels('B0',[self.resource,self.resource],{50:object()})


class AuxiliaryTests(unittest.TestCase):
    def setUp(self):
        self.corner=dict(n=5,rho=['477/400','6/5'],beta=['17/50',str(B3)],target='4097/10000',
            compact=dict(roots=60,nodes=1994,leaves=1027,independent_upper='2/5',stored_upper='401/1000'),
            exteriors=dict(left_upper='33/100',right_upper='18/100',left_domain='z<=0',right_domain='z>=5'))
        endpoints=['6/5','5/4','13/10','3/2','8/5','7/4','7361/4000']
        self.complement=dict(n=5,rho_finite=['6/5','7361/4000'],target='4097/10000',strips=41,attempts=42,
            bands=[dict(name=str(i),rho=endpoints[i:i+2],radius='3',upper='2/5',strips=6 if i<5 else 11)
                   for i in range(6)],published_tail_upper_at_start='819/2000')
        facts=(BoundFact('support',5,F(6,5),F(7361,4000),F(5,2),None,'a'*64),)
        self.evidence=ParentEvidence(facts,GlobalOwncapFact(F(42,100),'b'*64),(),())

    def test_whole_corner_and_complement_support_tail(self):
        self.assertEqual(corner_domain(self.corner)['leaves'],1027)
        self.assertEqual(len(complement_domain(self.complement,self.evidence)['support_edges']),6)

    def test_corner_narrowing_or_missing_ray_rejected(self):
        for change in(lambda x:x.update(beta=['347/1000',str(B3)]),
                      lambda x:x['exteriors'].update(left_domain='z>=0'),
                      lambda x:x['compact'].update(leaves=True),
                      lambda x:x['compact'].update(independent_upper='1/2')):
            damaged=deepcopy(self.corner);change(damaged)
            with self.assertRaises(ValueError):corner_domain(damaged)

    def test_complement_gap_bad_tail_missing_support_rejected(self):
        for change in(lambda x:x['bands'][1]['rho'].__setitem__(0,'126/100'),
                      lambda x:x.update(published_tail_upper_at_start='0'),
                      lambda x:x['bands'].pop(),lambda x:x.update(attempts=41),
                      lambda x:x['bands'][0].update(radius='2')):
            damaged=deepcopy(self.complement);change(damaged)
            with self.assertRaises(ValueError):complement_domain(damaged,self.evidence)

    def case_summaries(self):
        cases=[];ordinal=0
        for number,name in enumerate(CASES):
            count=25 if number<11 else 20
            rows=[]
            for i in range(100):
                row=dict(index=i,p=panel(i),closure='count'if i<count else'resource')
                if i<count:
                    leaves=255 if ordinal<248 else 254;ordinal+=1
                    row['statistics']=dict(nodes=2*leaves-6,leaves=leaves,maximum_score='2/5')
                rows.append(row)
            retained=rows[:count];rho,beta=domain(name)
            cases.append(dict(case=name,rho=rho,beta=beta,panels=100,resource_exclusions=100-count,
                count_forests=count,count_roots=6*count,count_nodes=sum(r['statistics']['nodes']for r in retained),
                count_leaves=sum(r['statistics']['leaves']for r in retained),coverage=rows,maximum_count_score='2/5'))
        return cases

    def test_full_domain_composition_is_only_a_conditional_implication(self):
        corner=corner_domain(self.corner);complement=complement_domain(self.complement,self.evidence)
        result=finish_domains(self.case_summaries(),corner,complement)
        self.assertEqual((result['count_forests'],result['count_leaves']),(295,75178))
        self.assertIs(result['c5_theorem_freshly_verified'],False)

    def test_complete_composition_rejects_false_or_balanced_census_and_lost_seams(self):
        mutations=[lambda x:x.pop(),lambda x:x.reverse(),
            lambda x:x[0]['coverage'].pop(),lambda x:x[0].update(count_roots=149),
            lambda x:x[0]['coverage'][0].update(index=True),
            lambda x:x[0]['coverage'][0]['statistics'].update(leaves=-1,nodes=-8),
            lambda x:x[0].update(count_nodes=-1),
            lambda x:x[0]['coverage'][99].update(closure='count'),
            lambda x:x[0].update(maximum_count_score='0')]
        for mutation in mutations:
            value=self.case_summaries();mutation(value)
            with self.assertRaises((ValueError,KeyError)):
                finish_domains(value,corner_domain(self.corner),complement_domain(self.complement,self.evidence))


class AvailableSourceTests(unittest.TestCase):
    def test_actual_summarize_job_exports_join_without_optional_parent_scope_keys(self):
        cache=extended(BASE/'reproduction_inputs/c5-8428002462d4e650')
        if not cache.exists():self.skipTest('Optional byte-pinned source cache unavailable')
        for job in RESOURCE_JOBS:
            # Original bytes are SOURCE FIXTURES only, never an observed run.
            prepared=read(source_at(cache,job.prepared))
            candidate=read(source_at(cache,job.case_directory+'/INITIAL.json'))
            replay=read(source_at(cache,job.output_paths[0]))
            accepted=read(source_at(cache,job.output_paths[1]))
            report=summarize_job(cache,job,prepared,candidate,replay,accepted)
            profile=candidate['profile'];inv=profile['invariants'];cover=candidate['stages'][-1]['cover']
            initial=dict(schema='C5_SOURCE_BOUND_JOINED_INITIAL_V1',job_id=job.initial_parent,
                n=5,band=job.band,sector=job.sector,input_candidate_sha256=report['parent_initial']['candidate_sha256'],
                profile=profile,rho_interval=[inv['rho_lo'],inv['rho']],beta_interval=[inv['beta_lo'],inv['beta_hi']],
                band_interval=candidate.get('band_interval'),beta_enclosing_interval=candidate.get('beta_enclosing_interval'),
                partition_kind=candidate.get('partition_kind'),stages=len(candidate['stages']),
                final_invariants=candidate['final_invariants'],final_cover_sha256=canonical_sha(cover),
                cells_per_stage=2592,validated_closed_p_indices=list(range(100)),
                final_active=cover['active'],final_gap_active=cover['gap_active'],
                source_bound_parent_implications_verified=True,execution_observed_by_this_reader=False,
                fresh_parent_fact_joins_verified=False)
            # Older/newer summaries may retain these redundant resource-domain
            # fields. Neither is the INITIAL signed-domain source of truth.
            report['parent_initial'].pop('rho_interval',None)
            report['parent_initial'].pop('beta_interval',None)
            same_resource_initial(report,initial)
            damaged=deepcopy(initial);damaged['beta_interval']=['-1','1']
            with self.assertRaises(ValueError):same_resource_initial(report,damaged)

    def test_all_295_actual_forest_headers_have_no_self_hash_requirement(self):
        cache=extended(BASE/'reproduction_inputs/c5-8428002462d4e650')
        if not cache.exists():self.skipTest('Optional byte-pinned source cache unavailable')
        graph=final_graph(cache)
        paths=[name for name in graph if name.endswith('/COUNT_FOREST.json')
               and '/count5_prepare_'in name and '/n5/'in name]
        self.assertEqual(len(paths),295)
        for name in paths:
            path=source_at(cache,name);capsule=path.parent;original=name.removesuffix('/COUNT_FOREST.json')
            # Read a bounded actual header, not any stored leaf/evaluator. All
            # header fields precede roots in this frozen original schema.
            with path.open(encoding='utf-8')as stream:prefix=stream.read(65536)
            before,separator,_=prefix.partition('"roots":')
            self.assertTrue(separator)
            header=json.loads(before+'"roots":[]}')
            self.assertNotIn('forest_sha256',header)
            accepted=read(source_at(cache,original+'/COUNT_ACCEPTED.json'))
            manifest=read(source_at(cache,original+'/KERNEL_COPY_MANIFEST.json'))['files']
            bind_count_header(capsule,original,graph,accepted,header,manifest)
        bad=deepcopy(accepted);bad['forest_sha256']='0'*64
        with self.assertRaises(ValueError):bind_count_header(capsule,original,graph,bad,header,manifest)

    def test_original_selected_support_HIGH_owncaps_cover_all_fifteen_RESOURCE_profiles(self):
        cache=BASE/'reproduction_inputs/c5-8428002462d4e650'
        if not cache.exists():self.skipTest('Optional byte-pinned source cache unavailable')
        graph=final_graph(cache);facts=[]
        # Explicitly SOURCE FIXTURES for numerical implication only. These old
        # JSON/status values are NEVER loaded by the production evidence loader
        # as fresh execution, and this unit test returns no acquisition receipt.
        sources=[(HIGH_ROOT+v+'/REPLAY_CHECKED.json',support_facts)
                 for v in('support_v1','support_v2','support_A0_v1')]
        sources += [(HIGH_ROOT+v[0]+'/HIGH_CHECKED.json',high_facts)for v in HIGH_VARIANTS]
        sources += [(HIGH+v[0]+'/OWNCAPS_CHECKED.json',owncap_facts)for v in OWN_VARIANTS]
        for name,parser in sources:
            path=source_at(cache,name);self.assertEqual(digest(path),graph[name])
            facts.extend(parser(read(path),graph[name]))
        for resource in RESOURCE_JOBS:
            candidate=read(source_at(cache,resource.case_directory+'/INITIAL.json'))
            result=entails_profile(candidate['profile'],resource.high,resource.owncap,facts)
            self.assertEqual(len(result['edges']),3)

    def test_all_fifteen_resource_INITIAL_candidates_are_exact_same_source_INPUT(self):
        cache=BASE/'reproduction_inputs/c5-8428002462d4e650'
        if not cache.exists():self.skipTest('Optional byte-pinned source cache unavailable')
        graph=final_graph(cache)
        for resource in RESOURCE_JOBS:
            parent=next(p for p in INITIAL_JOBS if p.job_id==resource.initial_parent)
            lhs=resource.case_directory+'/INITIAL.json';rhs=parent.case_directory+'/INPUT.json'
            self.assertEqual(graph[lhs],graph[rhs])
            self.assertEqual(digest(source_at(cache,lhs)),digest(source_at(cache,rhs)))

    def test_original_interface_and_physical_gap_on_four_small_pinned_examples(self):
        cache=BASE/'reproduction_inputs/c5-8428002462d4e650'
        if not cache.exists():self.skipTest('Optional byte-pinned source cache unavailable')
        graph=final_graph(cache)
        for band in('B0','BN','B2','B3'):
            helper,binding=source_functions(cache,graph,band)
            paths=[name for name in graph if name.endswith('/contract.json')
                   and '/count5_prepare_'in name and '/n5/'+band+'/'in name]
            self.assertTrue(paths)
            obj=read(source_at(cache,paths[0]));cfg=obj['rows'][0]
            row=read(source_at(cache,obj['resource_path']))
            helper['interface'](row,cfg,band,obj['index'],5)
            physical_gap(helper,row,cfg,'/count5_prepare_v4/'in paths[0])
            self.assertEqual(len(binding['functions']),10)
            for change in(lambda x:x.update(Lambda='0'),lambda x:x.update(acquired_scale_upper='0'),
                          lambda x:x['quadratics'].pop()):
                damaged=deepcopy(cfg);change(damaged)
                with self.assertRaises((ValueError,ZeroDivisionError,IndexError)):
                    helper['interface'](row,damaged,band,obj['index'],5)
            damaged=deepcopy(cfg);damaged['geometry_gap_lower']='0'
            with self.assertRaises(ValueError):physical_gap(helper,row,damaged,'/count5_prepare_v4/'in paths[0])

    def test_count_join_compares_the_entire_resource_answer_not_only_D_or_status(self):
        cache=BASE/'reproduction_inputs/c5-8428002462d4e650'
        if not cache.exists():self.skipTest('Optional byte-pinned source cache unavailable')
        graph=final_graph(cache);helper,_=source_functions(cache,graph,'B0')
        path=next(name for name in graph if name.endswith('/contract.json')
                  and '/count5_prepare_'in name and '/n5/B0/'in name)
        obj=read(source_at(cache,path));source=read(source_at(cache,obj['resource_path']));i=obj['index']
        # An ORIGINAL SOURCE FIXTURE, not a fresh execution or proof. Only the
        # pure contract/resource mathematical implication is tested here.
        artifact=CountArtifact(path.removesuffix('/contract.json'),{},obj,{'maximum_score':'2/5'},{})
        row=dict(index=i,p=panel(i),result=source['result'])
        self.assertEqual(join_count(cache,graph,artifact,row,'B0',helper)['index'],i)
        for mutation in(lambda x:x['result']['initial'].update(D='0'),
                        lambda x:x['result']['result'].update(d0='0'),
                        lambda x:x['result']['history'].clear(),lambda x:x.update(index=True)):
            damaged=deepcopy(row);mutation(damaged)
            with self.assertRaises(ValueError):join_count(cache,graph,artifact,damaged,'B0',helper)


if __name__=='__main__':unittest.main()
