"""Small exact domain checks; no numerical oracle or subprocess is invoked."""
from __future__ import annotations
from fractions import Fraction as F
import hashlib
import json
from math import isqrt

from ..all_indices.c5_counts import need

TARGET=F(4097,10000)
COUNT_TARGET=F('76824784444199314310731654405729617052063596250011448874609/187500000000000000000000000000000000000000000000000000000000')
B2=F(84729828287999,250000000000000)
B3=F(35139006743001,10**14)
CASES=('B0','BN','B2.S0','B2.S1','B2.S2','B2.S3',
       'B3.S0','B3.S2','B3.T0','B3.T1','B3.T2','B3.T3lower')


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def exact(a,b):
    if type(a)is not type(b):return False
    if type(a)is dict:return a.keys()==b.keys()and all(exact(a[k],b[k])for k in a)
    if type(a)is list:return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
    return a==b


def rational(value):
    need(type(value)is str,'Rational text, not a float/bool')
    result=F(value);need(str(result)==value,'Canonical rational representation')
    return result


def panel(index):
    need(type(index)is int and 0<=index<100,'Literal probability-panel identity')
    return [str(F(index,100)),str(F(index+1,100))]


def domain(case):
    need(case in CASES,'One of the twelve exact original cases')
    if case=='B0':return ['1','11/10'],None
    if case=='BN':return ['11/10','23/20'],None
    band,name=case.split('.')
    i=int(name[1])
    if band=='B2':
        rho=[F(23,20),F(467,400)]if i<2 else[F(467,400),F(237,200)]
        beta=[-B2,F(1,5)]if i%2==0 else[F(1,5),B2]
    else:
        rho=[F(237,200),F(477,400)]if i<2 else[F(477,400),F(6,5)]
        beta=([-B3,F(1,5)]if name[0]=='S'else
              [F(3,10),F(17,50)]if name=='T3lower'else
              [F(1,5),F(3,10)]if i%2==0 else[F(3,10),B3])
    return list(map(str,rho)),list(map(str,beta))


def closed_union(rectangles,rho,beta):
    """All arrangement vertices AND open faces/cells, hence every closed seam."""
    rho,beta=list(map(F,rho)),list(map(F,beta))
    rectangles=[(list(map(F,r)),list(map(F,b)))for r,b in rectangles]
    need(rho[0]<rho[1]and beta[0]<beta[1]and rectangles,'Nonempty exact enclosing rectangle')
    need(all(rho[0]<=r[0]<r[1]<=rho[1]and beta[0]<=b[0]<b[1]<=beta[1]
             for r,b in rectangles),'Only contained nondegenerate closed rectangles')
    xs=sorted(set(rho+[x for r,_ in rectangles for x in r]))
    ys=sorted(set(beta+[x for _,b in rectangles for x in b]))
    probes_x=xs+[(a+b)/2 for a,b in zip(xs,xs[1:])]
    probes_y=ys+[(a+b)/2 for a,b in zip(ys,ys[1:])]
    need(all(any(r[0]<=x<=r[1]and b[0]<=y<=b[1]for r,b in rectangles)
             for x in probes_x for y in probes_y),'No missing face, endpoint or open moment cell')
    return len(probes_x)*len(probes_y)


def sqrt_lower(x,grid=10**60):
    x=F(x);need(x>=0,'Nonnegative square-root input')
    lo=F(isqrt(x.numerator*grid*grid//x.denominator),grid)
    need(lo*lo<=x<(lo+F(1,grid))**2,'Directed rational square root')
    return lo


def constants():
    def atan(q,n):
        need(n%2==0,'Even alternating prefix')
        lo=sum((F((-1)**k,(2*k+1)*q**(2*k+1))for k in range(n)),F(0))
        return lo,lo+F(1,(2*n+1)*q**(2*n+1))
    a,b=atan(5,80);c,d=atan(239,40)
    pilo,pihi=16*a-4*d,16*b-4*c
    need(3<pilo<pihi<4,'Machin enclosure')
    ce=(3+sqrt_lower(10))*sqrt_lower(1/(2*pihi))/6
    need(TARGET<COUNT_TARGET<ce,'Both frozen strict targets are below C_E')
    for rho,beta in((F(237,200),B2),(F(6,5),B3)):
        need(0<beta<1 and(1+beta*beta)**2>=rho*rho*(1-beta*beta),
             'Whole-band universal signed-beta enclosure')
    return ce


def declaration(**values):
    """No caller-provided Boolean may upgrade this reader into a fresh run."""
    need(not(set(values)&{'source_bound_semantic_implications_verified','execution_observed_by_this_reader',
        'fresh_arithmetic','fresh_parent_fact_joins_verified','c5_theorem_freshly_verified',
        'all_index_conclusion_verified'}),'No caller-supplied proof/freshness upgrade')
    return dict(values,source_bound_semantic_implications_verified=True,
                execution_observed_by_this_reader=False,fresh_arithmetic=False,
                fresh_parent_fact_joins_verified=False,c5_theorem_freshly_verified=False,
                all_index_conclusion_verified=False)


def same_resource_initial(resource,initial):
    need(initial['schema']=='C5_SOURCE_BOUND_JOINED_INITIAL_V1'
         and initial['source_bound_parent_implications_verified']is True
         and initial['execution_observed_by_this_reader']is False
         and initial['fresh_parent_fact_joins_verified']is False,'Posthoc INITIAL implication, not forged execution')
    parent=resource['parent_initial']
    need(parent['job_id']==initial['job_id']and resource['n']==initial['n']==5
         and type(resource['n'])is type(initial['n'])is int
         and resource['band']==initial['band']and exact(resource['sector'],initial['sector']),
         'Same literal n/band/sector and INITIAL job')
    comparisons={'candidate_sha256':'input_candidate_sha256','profile':'profile',
        'band_interval':'band_interval',
        'beta_enclosing_interval':'beta_enclosing_interval','partition_kind':'partition_kind',
        'stages':'stages','final_invariants':'final_invariants','final_cover_sha256':'final_cover_sha256'}
    for child_key,parent_key in comparisons.items():
        need(exact(parent[child_key],initial[parent_key]),'Complete resource/INITIAL identity: '+child_key)
    inv=parent['profile']['invariants']
    rho=[inv['rho_lo'],inv['rho']];beta=[inv['beta_lo'],inv['beta_hi']]
    need(all(type(v)is str for v in rho+beta)
         and 1<=F(rho[0])<=F(rho[1])and -1<=F(beta[0])<=F(beta[1])<=1
         and exact(rho,initial['rho_interval'])and exact(beta,initial['beta_interval'])
         and exact(resource['rho_interval'],rho),'Exact rho/beta derived from the identical FULL parent profile')
    if resource['sector']is None:
        need(resource['band']in('B0','BN')and resource['beta_interval']is None,
             'Full B0/BN resource band; INITIAL retains its actual universal beta enclosure')
    else:
        need(exact(resource['beta_interval'],beta),'Same exact resource/INITIAL signed-beta sector')
    need(initial['cells_per_stage']==2592 and type(initial['cells_per_stage'])is int
         and exact(initial['validated_closed_p_indices'],list(range(100)))
         and type(initial['final_active'])is int
         and initial['final_active']==initial['final_gap_active'],'Whole INITIAL domain and every active gap license')
    return dict(initial_job=initial['job_id'],candidate_sha256=initial['input_candidate_sha256'],
                final_cover_sha256=initial['final_cover_sha256'])
