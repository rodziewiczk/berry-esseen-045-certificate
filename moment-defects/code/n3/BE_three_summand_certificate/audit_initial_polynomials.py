#!/usr/bin/env python3
"""Exact, implementation-diverse audit of every initial polynomial expansion.
The main checker constructs power coefficients and then Bernstein coefficients.
Here direct integer evaluations of the original 59 features at a full tensor
interpolation grid are compared with those Bernstein coefficients. Agreement
at all 6^3 nodes proves a polynomial identity on each sign orthant, not merely
a sampled positivity assertion. This audits expansions; verify.py checks
positivity and coverage. Python standard library only.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from math import comb, lcm
from pathlib import Path
import json,time
import verify as main_checker

ROOT=Path(__file__).resolve().parent
IDS=[a for a in combinations_with_replacement(range(7),3)
     if max(a)<5 or 1 in a or 2 in a]
PERMS=[list(set(permutations(a))) for a in IDS]
MON=list(product(range(6),repeat=3))
W=[[comb(5,k)*j**k*(5-j)**(5-k) for k in range(6)] for j in range(6)]

def collocation(b):
    arr=list(b)
    for axis in range(3):
        out=[0]*216
        for index,(i,j,k) in enumerate(MON):
            coords=[i,j,k]
            value=0
            for v in range(6):
                coords[axis]=v
                value+=W[MON[index][axis]][v]*arr[36*coords[0]+6*coords[1]+coords[2]]
            out[index]=value
        arr=out
    return arr

def integer_features(origin,j):
    h=5*origin+7*j
    # Every feature has the same denominator 5^5=3125.
    return (3125,h*625,(h*h-25)*125,h**3*25,abs(h)**3*25,h**4*5,h**5)

def run():
    start=time.monotonic();nodes=0;cells=0
    for path in sorted((ROOT/'certificate').glob('*.json')):
        data=json.loads(path.read_text());c=list(map(F,data['coefficients']))
        if len(c)!=59:raise ValueError('coefficient count')
        common=1
        for v in c:common=lcm(common,v.denominator)
        terms=[]
        for value,per in zip(c,PERMS):
            cv=6*common*value/len(per)
            if cv.denominator!=1:raise ValueError('integer coefficient conversion')
            if cv:terms.extend((int(cv),a) for a in per)
        for signs in [(-1,-1,-1),(-1,-1,1),(-1,1,1),(1,1,1)]:
            b,den=main_checker.transform_bern(main_checker.polynomial(c,signs),signs)
            evaluated=collocation(b)
            features=[[integer_features(-7 if signs[axis]<0 else 0,j) for j in range(6)] for axis in range(3)]
            for index,(i,j,k) in enumerate(MON):
                x,y,z=features[0][i],features[1][j],features[2][k]
                direct=sum(cv*x[a]*y[bb]*z[cc] for cv,(a,bb,cc) in terms)
                if evaluated[index]*(6*common)!=direct*den:
                    raise ValueError(f'polynomial identity failed: {path.name} {signs} {i,j,k}')
                nodes+=1
        cells+=1
    print(f'ACCEPTED_ALL_INITIAL_IDENTITIES cells={cells} orthants={4*cells} exact_grid_identities={nodes}')
    print('Degree-five tensor interpolation makes these exact polynomial identities.')
    print('This audit complements, and does not replace, verify.py.')
    print('Elapsed seconds (diagnostic):',round(time.monotonic()-start,3))

if __name__=='__main__':run()
