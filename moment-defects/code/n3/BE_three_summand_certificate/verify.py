#!/usr/bin/env python3
"""Exact checker for the three-summand null-control certificates.
Python standard library + a C++17 compiler and Boost.Multiprecision headers.
No floating-point arithmetic occurs in acceptance. Construction is separate.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement,permutations
from math import comb,lcm,isqrt,factorial
from pathlib import Path
import json,subprocess,tempfile,time,re,hashlib,sys
ROOT=Path(__file__).resolve().parent
D=5
IDS=[a for a in combinations_with_replacement(range(7),3) if max(a)<5 or any(i in (1,2) for i in a)]
PERMS=[sorted(set(permutations(a))) for a in IDS]
MON=list(product(range(6),repeat=3))

def require(ok,msg):
    if not ok: raise ValueError(msg)

def unique(items):
    d={}
    for k,v in items:
        require(k not in d,'duplicate JSON field');d[k]=v
    return d

def rational(s):
    require(type(s) is str,'rational must be a string');v=F(s)
    require(str(v)==s,'noncanonical rational');return v

def univ(j,s):
    if j==0:return [(0,1)]
    if j==1:return [(1,1)]
    if j==2:return [(0,-1),(2,1)]
    if j==3:return [(3,1)]
    if j==4:return [(3,s)]
    return [(j-1,1)]

def polynomial(coeff,sign):
    p={}
    for c,per in zip(coeff,PERMS):
        for a in per:
            for m in product(*(univ(j,s) for j,s in zip(a,sign))):
                ix=tuple(v[0] for v in m);z=c/len(per)
                for _,v in m:z*=v
                p[ix]=p.get(ix,F())+z
    return {k:v for k,v in p.items() if v}

def expectation(coeff):
    p={}
    for c,a in zip(coeff,IDS):
        if any(i not in (0,3,4) for i in a):continue
        k=(a.count(3),a.count(4));p[k]=p.get(k,F())+c
    return p

def transform_bern(p,sign):
    den=1
    for c in p.values():den=lcm(den,c.denominator)
    b={m:int(p.get(m,F())*den) for m in MON}
    for axis,s in enumerate(sign):
        lo=-7 if s<0 else 0;h=7
        T=[[sum(F(comb(k,a)*comb(i,a),comb(D,a))*lo**(k-a)*h**a for a in range(min(i,k)+1)) for k in range(6)] for i in range(6)]
        require(all((10*x).denominator==1 for row in T for x in row),'Bernstein denominator')
        Ti=[[int(10*x) for x in row] for row in T];bb={}
        for m in MON:
            val=0
            for k in range(6):
                mm=list(m);mm[axis]=k;val+=Ti[m[axis]][k]*b[tuple(mm)]
            bb[m]=val
        b=bb
    return [b[m] for m in MON],den*1000

def export(coeff,t,path):
    with path.open('w') as f:
        f.write(f'N3-BERNSTEIN-5-V1\n{t.numerator} {t.denominator}\n')
        for s in [(-1,-1,-1),(-1,-1,1),(-1,1,1),(1,1,1)]:
            b,den=transform_bern(polynomial(coeff,s),s)
            f.write(' '.join('-7' if x<0 else '0' for x in s)+'\n'+str(den)+'\n')
            f.write('\n'.join(map(str,b))+'\n')

def pi_bounds():
    def atan(x,m):return sum((F((-1)**k,2*k+1)*x**(2*k+1) for k in range(m+1)),F())
    return (16*atan(F(1,5),23)-4*atan(F(1,239),22),16*atan(F(1,5),22)-4*atan(F(1,239),23))

PL,PH=pi_bounds()
def normal3(t):
    """Enclose Phi(t/sqrt(3)) for rational |t| <= 4."""
    require(abs(t)<=4,'normal domain');scale=10**32
    sl=F(isqrt(6*PL.numerator*scale**2//PL.denominator),scale)
    sh=F(isqrt(6*PH.numerator*scale**2//PH.denominator)+1,scale)
    require(sl*sl<=6*PL<6*PH<=sh*sh,'normal square root enclosure')
    u=abs(t)
    def integral(m):return sum((F((-1)**k,6**k*factorial(k)*(2*k+1))*u**(2*k+1) for k in range(m+1)),F())
    a,b=integral(35),integral(34)
    require(0<=a<=b,'positive alternating integral enclosure')
    if t>=0:return F(1,2)+a/sh,F(1,2)+b/sl
    return F(1,2)-b/sl,F(1,2)-a/sh

def bern2(p,box):
    gl,gh,rl,rh=box
    def T(lo,hi):return [[sum(F(comb(k,a)*comb(i,a),comb(3,a))*lo**(k-a)*(hi-lo)**a for a in range(min(i,k)+1)) for k in range(4)] for i in range(4)]
    x,y=T(gl,gh),T(rl,rh)
    return [sum((v*x[i][a]*y[j][b] for (a,b),v in p.items()),F()) for i in range(4) for j in range(4)]

def check_moments(coeff,t):
    p={k:-v for k,v in expectation(coeff).items()}
    p[0,0]=p.get((0,0),F())+normal3(t)[0];p[0,1]=p.get((0,1),F())+F(59,250)
    stack=[((F(-15,8),F(15,8),F(1),F(15,8)),0)];count=0
    while stack:
        box,depth=stack.pop();count+=1;gl,gh,rl,rh=box
        require(depth<50 and count<100000,'unresolved moment positivity')
        gm=F() if gl<=0<=gh else min(gl*gl,gh*gh)
        # rho^2(s+4)-(s+2)^2 decreases in s>=0 when rho<=15/8<2.
        if rh*rh*(gm+4)-(gm+2)**2<0:continue
        if min(bern2(p,box))>=0:continue
        if gh-gl>=rh-rl:
            m=(gl+gh)/2;stack.extend([((gl,m,rl,rh),depth+1),((m,gh,rl,rh),depth+1)])
        else:
            m=(rl+rh)/2;stack.extend([((gl,gh,rl,m),depth+1),((gl,gh,m,rh),depth+1)])
    return count

def analytic_constants():
    a,b,rho0=F(1661,5000),F(429,1000),F(15,8);L=F(59,250)
    require((a*(1+b/rho0))**2<3*L**2,'structural complementary range')
    require(3*L**2<F(409,1000)**2,'tensor coefficient below rational Esseen lower bound')
    require(F(316227,100000)**2<10,'sqrt(10) lower')
    require(F(250663,100000)**2>2*PH,'sqrt(2*pi) upper')
    require((3+F(316227,100000))/(6*F(250663,100000))>F(4097,10000)>F(409,1000),'Esseen comparison')
    require(a*(1+b)<F(19,40) and a*(rho0+b)<F(77,100),'structural coefficient bounds')
    require(F(17,10)**2<3<F(7,4)**2,'sqrt(3) bounds')
    require(F(12,7)**2<3 and F(77,100)/F(12,7)<F(9,20),'D bound')
    require(F(19,40)/F(17,10)<F(2,7),'lambda upper')
    require(3*L**2>F(2,5)**2,'lambda lower')
    require(F(7,4)*F(2,5)+3*F(2,7)<F(8,5),'linear support coefficient')
    require((F(1,4)+3*F(9,20))/2==F(4,5),'quadratic support coefficient')
    # Shifted coefficients of 8r^3/35-4r^2/5-8r/5-1/8-3 at r=6+u.
    require(F(8,35)*216-F(4,5)*36-F(8,5)*6-F(1,8)-3==F(2197,280)>0,'support polynomial constant')
    require(3*F(8,35)*36-2*F(4,5)*6-F(8,5)==F(472,35)>0,'support polynomial linear')
    require(3*F(8,35)*6-F(4,5)==F(116,35)>0,'support polynomial quadratic')
    require(F(25,8)<PL and PL*F(8,3)>8,'normal density constants')
    require(F(12,61)<F(59,250),'negative tail')
    require(1-normal3(F(3,2))[0]<F(59,250),'positive tail')
    require(len(IDS)==59,'basis size')


def load_records(directory):
    paths=sorted(directory.iterdir());require(paths,'empty certificate')
    records=[]
    for path in paths:
        require(path.is_file() and not path.is_symlink() and path.suffix=='.json','unexpected certificate entry')
        raw=path.read_bytes();r=json.loads(raw,object_pairs_hook=unique)
        require(set(r)=={'format','t_lo','t_hi','coefficients'},'schema fields')
        require(r['format']=='be-three-summand-null-controls-v1','schema format')
        lo,hi=rational(r['t_lo']),rational(r['t_hi']);require(lo<hi,'empty threshold interval')
        require(type(r['coefficients']) is list and len(r['coefficients'])==59,'coefficient count')
        c=list(map(rational,r['coefficients']));records.append((lo,hi,c,path.name,hashlib.sha256(raw).hexdigest()))
    records.sort(key=lambda r:r[:2])
    require(records[0][0]==F(-7,2) and records[-1][1]==F(3,2),'global threshold scope')
    for a,b in zip(records,records[1:]):require(a[1]==b[0],'gap or overlap in threshold coverage')
    return records

def main():
    start=time.monotonic();analytic_constants();rs=load_records(ROOT/'certificate')
    nodes=leaves=moments=0
    with tempfile.TemporaryDirectory(prefix='be_n3_check_') as tmp:
        tmp=Path(tmp);binary=tmp/'check_cube'
        comp=subprocess.run(['g++','-O2','-std=c++17',str(ROOT/'check_cube.cpp'),'-o',str(binary)],capture_output=True,text=True)
        require(comp.returncode==0,'C++ compilation failed: '+comp.stderr)
        for i,(lo,hi,c,name,digest) in enumerate(rs):
            inp=tmp/'cell.bern';export(c,hi,inp)
            done=subprocess.run([str(binary),str(inp)],capture_output=True,text=True,timeout=180)
            require(done.returncode==0,done.stderr)
            match=re.fullmatch(r'ACCEPTED_EXACT_CUBES (\d+) (\d+) (\d+)\n',done.stdout)
            require(match is not None,'unexpected integer checker output')
            nn,ll,dd=map(int,match.groups());mm=check_moments(c,lo);nodes+=nn;leaves+=ll;moments+=mm
            print(f'CELL {i:03d} [{lo},{hi}] nodes={nn} leaves={ll} depth={dd} moment_boxes={mm} sha256={digest}',flush=True)
    print(f'ACCEPTED_FULL_N3 {len(rs)} {nodes} {leaves} {moments}',flush=True)
    print('Conclusion, conditional on the analytic reduction: C_3 <= 59*sqrt(3)/250 < C_E.')
    print('Elapsed seconds (diagnostic):',round(time.monotonic()-start,3))

if __name__=='__main__':
    try:main()
    except Exception as exc:print('REJECTED:',exc,file=sys.stderr);sys.exit(1)
