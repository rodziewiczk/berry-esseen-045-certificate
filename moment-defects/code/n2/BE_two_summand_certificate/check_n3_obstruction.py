#!/usr/bin/env python3
"""Exact check of a DEPENDENT 3-coordinate obstruction, not an iid counterexample."""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
from pathlib import Path
import json

def require(ok,msg):
    if not ok:raise ValueError(msg)

def check(path):
    d=json.loads(path.read_text())
    require(d['format']=='dependent-three-coordinate-tensor-obstruction-v1','format')
    rho,gamma,t=F(d['rho']),F(d['gamma']),F(d['threshold'])
    require((rho,gamma,t)==(F(6,5),F(3,8),F(-3,5)),'parameters')
    m=[F(1),F(0),F(1),gamma,rho]
    bs=list(combinations_with_replacement(range(5),3))
    totals=[F(0) for _ in bs];cdf=F(0);fourth_cross=F(0)
    for row in d['orbits']:
        v=tuple(F(s) for s in row['triple']);w=F(row['weight'])
        require(len(v)==3 and list(v)==sorted(v) and w>0,'positive ordered orbit')
        require(all(-9<=x<=9 for x in v),'support domain')
        orbit=sorted(set(permutations(v)))
        for y in orbit:
            f=[[F(1),x,x*x,x**3,abs(x)**3] for x in y]
            for j,(a,b,c) in enumerate(bs):totals[j]+=w* f[0][a]*f[1][b]*f[2][c]/len(orbit)
            fourth_cross+=w*y[0]**4*y[1]/len(orbit)
        if sum(v)<=t:cdf+=w
    for value,(i,j,k) in zip(totals,bs):require(value==m[i]*m[j]*m[k],'tensor moment mismatch')
    require(fourth_cross!=0,'must separately verify lack of independence')
    require(F(433,250)**2<3<F(1733,1000)**2,'sqrt3 brackets')
    require(2*F(22,7)*F(997,2500)**2<1,'lower phi0')
    zlo,zhi=F(433,1250),F(1733,5000)
    normal_hi=F(1,2)-F(997,2500)*(zlo-zhi**3/6)
    score_lo=F(433,250)/rho*(cdf-normal_hi)
    require(score_lo>F(41,100),'score must exceed 0.41')
    # pi > 3.1415 from Machin alternating bounds.
    atan=lambda x,k:sum((F((-1)**j,2*j+1)*x**(2*j+1) for j in range(k+1)),F(0))
    pil=16*atan(F(1,5),9)-4*atan(F(1,239),8)
    require(pil>F(6283,2000),'lower pi')
    require(2*pil*F(399,1000)**2>1,'upper phi0')
    require(F(3163,1000)**2>10,'upper sqrt10')
    require(F(399,1000)*(3+F(3163,1000))/6<F(41,100),'Esseen constant below 0.41')
    print('PASS: all 35 symmetric tensor moments factor exactly.')
    print('PASS: all orbit weights are positive and sum to one.')
    print('PASS: E[X1^4 X2] != 0, so the joint law is not independent.')
    print('PASS: normalized CDF score > 41/100 > C_E.')
    print('NOT an iid counterexample; it excludes a particular linear tensor relaxation.')
    print('Diagnostics only: orbit count =',len(d['orbits']),'; score lower =',float(score_lo),'; fourth cross =',float(fourth_cross))
if __name__=='__main__':check(Path(__file__).resolve().parent/'n3_dependent_obstruction.json')
