#!/usr/bin/env python3
"""Rational certificate checker for a two-summand Berry--Esseen bound.

Generation uses SciPy as untrusted advice. Checking uses Fraction and integer
arithmetic only. Tensor positivity is checked in a Bernstein basis on triangles;
the moment-parameter bound is checked by Bernstein boxes and an exact moment test.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import argparse, json, sys, time

DEG=6
IDS=[(i,j) for i in range(5) for j in range(i,5)]
EXPS=[0,1,2,3,3]
TRI=[(i,j,DEG-i-j) for i in range(DEG+1) for j in range(DEG+1-i)]
ROOT=Path(__file__).resolve().parent

def require(ok, message):
    if not ok: raise ValueError(message)

def unique_object(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON field')
        result[key] = value
    return result

def padd(a,b):
    d=dict(a)
    for k,v in b.items(): d[k]=d.get(k,F(0))+v
    return {k:v for k,v in d.items() if v}
def pmul(a,b):
    d={}
    for (i,j),v in a.items():
        for (k,l),w in b.items(): d[i+k,j+l]=d.get((i+k,j+l),F(0))+v*w
    return {k:v for k,v in d.items() if v}
def pscale(a,s): return {k:v*s for k,v in a.items() if v*s}
def peval(p,x,y): return sum((c*x**i*y**j for (i,j),c in p.items()),F(0))
def compose(p, ax, ay):
    xp=[{(0,0):F(1)}];yp=[{(0,0):F(1)}]
    for i in range(max((i for i,j in p),default=0)): xp.append(pmul(xp[-1],ax))
    for j in range(max((j for i,j in p),default=0)): yp.append(pmul(yp[-1],ay))
    out={}
    for (i,j),c in p.items():out=padd(out,pscale(pmul(xp[i],yp[j]),c))
    return out

def tensor_poly(coeff,sx,sy):
    p={};mx=[1,1,1,1,sx];my=[1,1,1,1,sy]
    for c,(i,j) in zip(coeff,IDS):
        p=padd(p,{(EXPS[i],EXPS[j]):c*mx[i]*my[j]})
        if i!=j:p=padd(p,{(EXPS[j],EXPS[i]):c*mx[j]*my[i]})
    return p

def expectation_poly(coeff):
    mm=[{(0,0):F(1)},{},{(0,0):F(1)},{(1,0):F(1)},{(0,1):F(1)}]
    p={}
    for c,(i,j) in zip(coeff,IDS):p=padd(p,pscale(pmul(mm[i],mm[j]),c*(1 if i==j else 2)))
    return p

def clip(poly,sign,t):
    out=[]
    if not poly:return out
    for a,b in zip(poly,poly[1:]+poly[:1]):
        va=sign*(a[0]+a[1]-t);vb=sign*(b[0]+b[1]-t)
        ina=va<=0;inb=vb<=0
        if ina:out.append(a)
        if ina!=inb:
            r=va/(va-vb);out.append((a[0]+r*(b[0]-a[0]),a[1]+r*(b[1]-a[1])))
    clean=[]
    for v in out:
        if not clean or v!=clean[-1]:clean.append(v)
    if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
    return clean

def triangles(t):
    for sx in [-1,1]:
        for sy in [-1,1]:
            xl,xh=(F(-6),F(0)) if sx<0 else (F(0),F(6))
            yl,yh=(F(-6),F(0)) if sy<0 else (F(0),F(6))
            rect=[(xl,yl),(xh,yl),(xh,yh),(xl,yh)]
            for event,sg in [(1,1),(0,-1)]:
                pp=clip(rect,sg,t)
                for i in range(1,len(pp)-1):
                    vv=[pp[0],pp[i],pp[i+1]]
                    cross=(vv[1][0]-vv[0][0])*(vv[2][1]-vv[0][1])-(vv[1][1]-vv[0][1])*(vv[2][0]-vv[0][0])
                    if cross:yield sx,sy,event,vv

def tri_bern(p,vv):
    x0,y0=vv[0]
    c=compose(p,{(0,0):x0,(1,0):vv[1][0]-x0,(0,1):vv[2][0]-x0},
                {(0,0):y0,(1,0):vv[1][1]-y0,(0,1):vv[2][1]-y0})
    b={}
    for k,i,j in TRI:
        b[k,i,j]=sum((v*F(comb(i,a)*comb(j,bb),comb(DEG,a+bb)*comb(a+bb,a))
                         for (a,bb),v in c.items() if a<=i and bb<=j),F(0))
    return b

def tri_split(b,vv):
    edges=[(0,1,2),(0,2,1),(1,2,0)]
    a,bb,c=max(edges,key=lambda ij:(vv[ij[0]][0]-vv[ij[1]][0])**2+(vv[ij[0]][1]-vv[ij[1]][1])**2)
    perm=(a,bb,c)
    pb={}
    for inds in TRI:
        old=[0,0,0]
        for j in range(3):old[perm[j]]=inds[j]
        pb[inds]=b[tuple(old)]
    left={};right={}
    for i,j,k in TRI:
        left[i,j,k]=sum((F(comb(j,l),2**j)*pb[i+j-l,l,k] for l in range(j+1)),F(0))
        right[i,j,k]=sum((F(comb(i,l),2**i)*pb[l,i-l+j,k] for l in range(i+1)),F(0))
    mid=tuple((vv[a][i]+vv[bb][i])/2 for i in range(2))
    return (left,[vv[a],mid,vv[c]]),(right,[mid,vv[bb],vv[c]])

def check_xy(coeff,t,maxnodes=100000):
    count=0;leaves=0;deep=0
    for sx,sy,event,vv in triangles(t):
        pp=tensor_poly(coeff,sx,sy)
        pp=padd(pp,{(0,0):-F(event)})
        stack=[(tri_bern(pp,vv),vv,0)]
        while stack:
            b,v,depth=stack.pop();count+=1;deep=max(deep,depth)
            if min(b.values())>=0:leaves+=1;continue
            for j in range(3):
                ids=[0,0,0];ids[j]=DEG
                if b[tuple(ids)]<0:return False,(v[j][0],v[j][1],event),count,deep
            if depth>=35 or count>=maxnodes:raise RuntimeError('unresolved tensor positivity')
            ch1,ch2=tri_split(b,v)
            stack.append((*ch1,depth+1));stack.append((*ch2,depth+1))
    return True,None,count,deep

def phi_interval_raw(t):
    """Exact enclosure of Phi(t/sqrt(2)), for |t|<=5/2."""
    def atan(x,m):return sum((F((-1)**k,2*k+1)*x**(2*k+1) for k in range(m+1)),F(0))
    pl=16*atan(F(1,5),23)-4*atan(F(1,239),22)
    ph=16*atan(F(1,5),22)-4*atan(F(1,239),23)
    require(F(25,8)<pl<ph<F(22,7), 'Machin pi bounds')
    scale=10**30
    sl=F(isqrt(pl.numerator*scale*scale//pl.denominator),scale)
    sh=F(isqrt(ph.numerator*scale*scale//ph.denominator)+1,scale)
    require(sl*sl<=pl<ph<=sh*sh, 'square-root bracket')
    clo,chi=1/(2*sh),1/(2*sl)
    u=abs(t)
    def integ(m):return sum((F((-1)**k,4**k*factorial(k)*(2*k+1))*u**(2*k+1) for k in range(m+1)),F(0))
    il,ih=integ(25),integ(24)
    if t>=0:return F(1,2)+clo*il,F(1,2)+chi*ih
    return F(1,2)-chi*ih,F(1,2)-clo*il

def box_bern(p,box):
    gl,gh,rl,rh=box
    c=compose(p,{(0,0):gl,(1,0):gh-gl},{(0,0):rl,(0,1):rh-rl})
    return [sum((v*F(comb(i,a),comb(2,a))*F(comb(j,b),comb(2,b))
                   for (a,b),v in c.items() if a<=i and b<=j),F(0)) for i in range(3) for j in range(3)]

def feasible(g,r):return r*r*(g*g+4)-(g*g+2)**2>=0

def check_params(coeff,tlo,maxnodes=100000):
    plo,_=phi_interval_raw(tlo)
    p=padd({(0,0):plo,(0,1):F(2,7)},pscale(expectation_poly(coeff),F(-1)))
    stack=[((F(-2),F(2),F(1),F(2)),0)];count=0;deep=0
    while stack:
        box,dep=stack.pop();count+=1;deep=max(deep,dep)
        gl,gh,rl,rh=box
        gmin=F(0) if gl<=0<=gh else min(gl*gl,gh*gh)
        if rh*rh*(gmin+4)-(gmin+2)**2<0:continue
        if min(box_bern(p,box))>=0:continue
        for g in [gl,(gl+gh)/2,gh]:
            for r in [rl,(rl+rh)/2,rh]:
                if feasible(g,r) and peval(p,g,r)<0:return False,(g,r),count,deep
        if dep>=35 or count>=maxnodes:raise RuntimeError('unresolved moment-parameter positivity')
        if gh-gl>rh-rl:
            gm=(gl+gh)/2
            stack.extend([((gl,gm,rl,rh),dep+1),((gm,gh,rl,rh),dep+1)])
        else:
            rm=(rl+rh)/2
            stack.extend([((gl,gh,rl,rm),dep+1),((gl,gh,rm,rh),dep+1)])
    return True,None,count,deep

def initial_samples(t):
    import numpy as np
    ys=np.unique(np.r_[np.linspace(-6,6,31),np.linspace(-1.75,1.75,36),-1,0,1])
    xx,yy=np.meshgrid(ys,ys,indexing='ij');x=np.r_[xx.ravel(),ys];y=np.r_[yy.ravel(),float(t)-ys]
    keep=(y>=-6)&(y<=6);x,y=x[keep],y[keep]
    return [[float(u),float(v),float(u+v<=float(t)+1e-10)] for u,v in zip(x,y)]

def moment_samples():
    import numpy as np
    out=[]
    for rho in np.linspace(1,2,31):
        B=np.sqrt(max(0,(rho*rho+rho*np.sqrt(rho*rho+8))/2-2))
        for ga in np.linspace(-B,B,31):out.append((ga,rho))
    return out

def gen_one(index,output):
    import numpy as np
    from scipy.optimize import linprog
    tlo=F(-5,2)+F(index,20);thi=tlo+F(1,20)
    samples=initial_samples(thi);pars=moment_samples()
    normal_lo=float(phi_interval_raw(tlo)[0]);start=time.time()
    for iteration in range(100):
        xx=np.array(samples);x,y,rhs=xx.T
        ff=np.array([np.ones(x.shape),x,x*x,x**3,abs(x)**3]);gg=np.array([np.ones(y.shape),y,y*y,y**3,abs(y)**3])
        A=np.array([ff[i]*gg[j] if i==j else ff[i]*gg[j]+ff[j]*gg[i] for i,j in IDS]).T
        pp=np.array(pars);ga,rho=pp.T;mm=np.array([np.ones(ga.shape),np.zeros(ga.shape),np.ones(ga.shape),ga,rho])
        pm=np.array([mm[i]*mm[j]*(1 if i==j else 2) for i,j in IDS]).T
        AA=np.r_[np.c_[-A,np.zeros(len(A))],np.c_[pm,-rho]]
        bb=np.r_[-rhs,np.full(len(pars),normal_lo)]
        sol=linprog([0]*15+[1],A_ub=AA,b_ub=bb,bounds=[(None,None)]*15+[(0,None)],method='highs')
        if not sol.success:raise RuntimeError(sol.message)
        coeff=[F(round(float(c)*2**42),2**42) for c in sol.x[:15]]
        coeff[0]+=F(1,500) # strict tensor slack, charged in the scalar expectation check
        ok,wit,nxy,dep=check_xy(coeff,thi)
        if not ok:
            samples.append([float(v) for v in wit]);continue
        ok2,wit2,nparam,pdep=check_params(coeff,tlo)
        if not ok2:
            pars.append(tuple(float(v) for v in wit2))
            print('PARAM_FAIL',index,iteration,'lambda',sol.x[-1],'witness',wit2,flush=True)
            # Scalar failures despite an already small LP coefficient should disappear
            # after enrichment. A genuinely excessive optimal coefficient requires a narrower t-cell.
            if sol.x[-1]>.284:raise RuntimeError('coarse t-cell or insufficient tensor basis')
            continue
        record={'format':'be-two-summand-tensor-v1','index':index,'t_lo':str(tlo),'t_hi':str(thi),
                'coefficients':[str(c) for c in coeff]}
        output.mkdir(parents=True,exist_ok=True)
        (output/f'{index:03d}.json').write_text(json.dumps(record,indent=2)+'\n')
        print(f'CERTIFIED {index:02d}: [{tlo},{thi}], xy_nodes={nxy}, xy_depth={dep}, moment_nodes={nparam}, iterations={iteration+1}, seconds={time.time()-start:.2f}',flush=True)
        return
    raise RuntimeError('advice refinement did not converge')

def verify_one(path,index):
    d=json.loads(path.read_text(), object_pairs_hook=unique_object,
                 parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    require(set(d)=={'format','index','t_lo','t_hi','coefficients'}, 'schema mismatch')
    require(d['format']=='be-two-summand-tensor-v1', 'format mismatch')
    require(type(d['index']) is int and d['index']==index, 'index mismatch')
    tlo=F(-5,2)+F(index,20);thi=tlo+F(1,20)
    require(d['t_lo']==str(tlo) and d['t_hi']==str(thi), 'coverage mismatch')
    require(type(d['coefficients']) is list and len(d['coefficients'])==15, 'coefficient count')
    require(all(type(x) is str for x in d['coefficients']), 'coefficient types')
    cc=[F(v) for v in d['coefficients']]
    require(all(str(c)==s for c,s in zip(cc,d['coefficients'])), 'canonical rational')
    ok,w,n,d0=check_xy(cc,thi);require(ok, 'tensor positivity failure: '+str((index,w)))
    ok,w,np,d1=check_params(cc,tlo);require(ok, 'moment positivity failure: '+str((index,w)))
    return n,np

def verify_reductions():
    a,b=F(1661,5000),F(429,1000)
    require((a*(1+b/2))**2<F(8,49), 'large third moments')
    require(a*(1+b)<F(1,2) and a*(2+b)<1, 'contact constants')
    require(F(8,49)>F(4,25), 'target above 2/5')
    require(F(8,49)<F(81,200)**2, 'target below 0.405')
    require(F(79,25)**2<10 and 2*F(22,7)*F(997,2500)**2<1, 'Esseen brackets')
    require(F(997,2500)*(3+F(79,25))/6>F(409,1000), 'Esseen above 0.409')
    require(2*F(25,8)*F(2,5)**2>=1, 'upper normal density')
    require(2*F(25,8)*sum((F(1,factorial(k)) for k in range(5)),F(0))>16, 'x phi bound')
    require(F(10,7)**2>2 and F(5,7)**2>F(1,2), 'square root bounds')
    pol=[-F(1,8),-F(23,14),-F(67,56),F(2,7)]
    sh=[sum((pol[k]*comb(k,j)*6**(k-j) for k in range(j,4)),F(0))-(2 if j==0 else 0) for j in range(4)]
    require(sh==[F(373,56),F(104,7),F(221,56),F(2,7)], 'support polynomial')
    require(all(x>0 for x in sh), 'support polynomial positivity')
    require(F(8,33)<F(2,7), 'Cantelli tail')
    require(phi_interval_raw(F(1))[0]>F(5,7), 'normal tail')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['generate','check']);ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int,default=70)
    ap.add_argument('--directory',type=Path,default=ROOT/'certificate');args=ap.parse_args()
    require(0<=args.start<args.stop<=70, 'invalid index range')
    if args.mode=='generate':
        for i in range(args.start,args.stop):gen_one(i,args.directory)
    else:
        require(args.start==0 and args.stop==70, 'A global acceptance requires all 70 cells.')
        verify_reductions()
        require({p.name for p in args.directory.iterdir()}=={f'{i:03d}.json' for i in range(70)}, 'incomplete or extra shards')
        total=0;ptotal=0
        for i in range(70):
            n,np=verify_one(args.directory/f'{i:03d}.json',i);total+=n;ptotal+=np
            print('CHECKED',i,n,np,flush=True)
        print('ACCEPTED_ALL_70_TENSOR_CELLS',total,ptotal)
if __name__=='__main__':main()
