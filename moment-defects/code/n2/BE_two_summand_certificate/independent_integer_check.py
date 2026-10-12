#!/usr/bin/env python3
"""Independent rational checker. No imports from the construction/checker module.

Tensor positivity is recomputed from homogeneous integer coefficients at EVERY
triangle, not propagated by the other checker's Bernstein subdivision formula.
Requires Python standard library only. This checks a mathematical certificate,
not a formalization of the probabilistic extremizer reduction.
"""
from fractions import Fraction as Q
from math import factorial, comb, lcm
from pathlib import Path
import argparse, json

PAIR=[(i,j) for i in range(5) for j in range(i,5)]
POW=[0,1,2,3,3]

def require(condition,message):
    if not condition:raise ValueError(message)

def unique_object(items):
    out={}
    for k,v in items:
        require(k not in out,'duplicate JSON field');out[k]=v
    return out

def parse(path,index):
    d=json.loads(path.read_text(),object_pairs_hook=unique_object,
                 parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    require(set(d)=={'format','index','t_lo','t_hi','coefficients'},'schema mismatch')
    require(d['format']=='be-two-summand-tensor-v1','format mismatch')
    require(type(d['index']) is int and d['index']==index,'index mismatch')
    lo=Q(-5,2)+Q(index,20);hi=lo+Q(1,20)
    require(d['t_lo']==str(lo) and d['t_hi']==str(hi),'coverage mismatch')
    cc=d['coefficients'];require(type(cc) is list and len(cc)==15,'coefficient count')
    require(all(type(c) is str for c in cc),'coefficients must be rational strings')
    c=[Q(v) for v in cc];require(all(str(v)==s for v,s in zip(c,cc)),'noncanonical rational')
    return lo,hi,c

def exponent_tuples(k):
    return [(i,j,k-i-j) for i in range(k+1) for j in range(k+1-i)]

def linear_power(v,k):
    return {(i,j,l):comb(k,i)*comb(k-i,j)*v[0]**i*v[1]**j*v[2]**l
            for i,j,l in exponent_tuples(k)}

def multiply(a,b):
    out={}
    for ia,va in a.items():
        if not va:continue
        for ib,vb in b.items():
            if vb:
                e=tuple(ia[k]+ib[k] for k in range(3));out[e]=out.get(e,0)+va*vb
    return out

def polynomial(c,sx,sy,event):
    p={(0,0):-Q(event)}
    ax=[1,1,1,1,sx];ay=[1,1,1,1,sy]
    for v,(i,j) in zip(c,PAIR):
        e=(POW[i],POW[j]);p[e]=p.get(e,Q(0))+v*ax[i]*ay[j]
        if i!=j:
            e=(POW[j],POW[i]);p[e]=p.get(e,Q(0))+v*ax[j]*ay[i]
    return {e:v for e,v in p.items() if v}

def homogeneous_coefficients(p,vertices):
    dc=lcm(*(v.denominator for v in p.values()))
    dv=lcm(*(u.denominator for v in vertices for u in v))
    xv=[int(v[0]*dv) for v in vertices];yv=[int(v[1]*dv) for v in vertices]
    xp=[linear_power(xv,i) for i in range(4)];yp=[linear_power(yv,j) for j in range(4)]
    sp=[linear_power([1,1,1],k) for k in range(7)]
    out={e:0 for e in exponent_tuples(6)}
    for (i,j),v in p.items():
        h=multiply(multiply(xp[i],yp[j]),sp[6-i-j])
        factor=int(v*dc)*dv**(6-i-j)
        for e,a in h.items():out[e]+=factor*a
    return out

def cut(vertices,t,keep_low):
    result=[]
    for i in range(len(vertices)):
        a=vertices[i];b=vertices[(i+1)%len(vertices)]
        fa=a[0]+a[1]-t;fb=b[0]+b[1]-t
        ka=fa<=0 if keep_low else fa>=0
        kb=fb<=0 if keep_low else fb>=0
        if ka:result.append(a)
        if ka!=kb:
            rr=fa/(fa-fb);result.append(tuple(a[k]+rr*(b[k]-a[k]) for k in range(2)))
    out=[]
    for v in result:
        if not out or out[-1]!=v:out.append(v)
    if len(out)>1 and out[-1]==out[0]:out.pop()
    return out

def check_tensor(c,t):
    total=0;leaves=0
    for sx in [-1,1]:
        for sy in [-1,1]:
            xl,xh=(Q(-6),Q(0)) if sx==-1 else (Q(0),Q(6))
            yl,yh=(Q(-6),Q(0)) if sy==-1 else (Q(0),Q(6))
            rect=[(xl,yl),(xh,yl),(xh,yh),(xl,yh)]
            for event in [1,0]:
                vv=cut(rect,t,event==1);p=polynomial(c,sx,sy,event)
                for k in range(1,len(vv)-1):
                    v=[vv[0],vv[k],vv[k+1]]
                    area=(v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0])
                    if not area:continue
                    stack=[(v,0)]
                    while stack:
                        tri,depth=stack.pop();total+=1
                        h=homogeneous_coefficients(p,tri)
                        if min(h.values())>=0:leaves+=1;continue
                        for e in [(6,0,0),(0,6,0),(0,0,6)]:require(h[e]>=0,'negative value at a triangle vertex')
                        require(depth<35 and total<100000,'unresolved triangle')
                        a,b,rest=max([(0,1,2),(0,2,1),(1,2,0)],
                           key=lambda e:sum((tri[e[0]][j]-tri[e[1]][j])**2 for j in range(2)))
                        mid=tuple((tri[a][j]+tri[b][j])/2 for j in range(2))
                        stack.extend([([tri[a],mid,tri[rest]],depth+1),([mid,tri[b],tri[rest]],depth+1)])
    return total,leaves

def elementary_constants():
    def at(x,m):return sum((Q((-1)**k,2*k+1)*x**(2*k+1) for k in range(m+1)),Q(0))
    pi_lo=16*at(Q(1,5),21)-4*at(Q(1,239),20)
    pi_hi=16*at(Q(1,5),20)-4*at(Q(1,239),21)
    cl=Q(282094791773878,10**15);ch=Q(282094791773879,10**15)
    require(4*pi_hi*cl**2<1<4*pi_lo*ch**2,'Gaussian factor enclosure')
    require(2*pi_hi*Q(997,2500)**2<1,'lower normal density')
    require(Q(79,25)**2<10 and Q(997,2500)*(3+Q(79,25))/6>Q(409,1000),'lower Esseen constant')
    require(Q(8,49)<Q(81,200)**2<Q(409,1000)**2,'target strictly below Esseen')
    require(Q(8,49)>Q(2,5)**2,'target above 2/5')
    a,b=Q(1661,5000),Q(429,1000)
    require((a*(1+b/2))**2<Q(8,49),'large-moment reduction')
    require(a*(1+b)<Q(1,2) and a*(2+b)<1,'extremizer constants')
    require(2*pi_lo*Q(2,5)**2>1,'upper normal density')
    require(2*pi_lo*sum((Q(1,factorial(j)) for j in range(5)),Q(0))>16,'x phi bound')
    require(Q(10,7)**2>2 and Q(5,7)**2>Q(1,2),'square-root bounds')
    # Q(y) >= P(|y|), and P(6+u)-2 has positive coefficients.
    pp=[-Q(1,8),-Q(23,14),-Q(67,56),Q(2,7)]
    shifted=[sum((pp[k]*comb(k,j)*6**(k-j) for k in range(j,4)),Q(0))-(2 if j==0 else 0) for j in range(4)]
    require(all(s>0 for s in shifted),'six-unit support exclusion')
    require(Q(8,33)<Q(2,7),'lower-threshold Cantelli tail')
    return cl,ch

CL,CH=elementary_constants()

def normal_lower(t):
    u=abs(t)
    integral=lambda n:sum((Q((-1)**k,4**k*factorial(k)*(2*k+1))*u**(2*k+1) for k in range(n+1)),Q(0))
    return Q(1,2)+CL*integral(31) if t>=0 else Q(1,2)-CH*integral(30)

require(normal_lower(Q(1))>Q(5,7),'upper-threshold Gaussian tail')

def scalar_coefficients(c,lo):
    q={(0,0):normal_lower(lo),(0,1):Q(2,7)}
    ex=[(0,0),None,(0,0),(1,0),(0,1)]
    for v,(i,j) in zip(c,PAIR):
        if ex[i] is None or ex[j] is None:continue
        e=tuple(ex[i][k]+ex[j][k] for k in range(2))
        q[e]=q.get(e,Q(0))-v*(1 if i==j else 2)
    return [q.get(e,Q(0)) for e in [(0,0),(1,0),(0,1),(2,0),(1,1),(0,2)]]

def check_scalar(c,lo):
    A,B,C,D,E,F=scalar_coefficients(c,lo)
    stack=[(Q(-2),Q(2),Q(1),Q(2),0)];count=0
    while stack:
        gl,gh,rl,rh,depth=stack.pop();count+=1
        g2=Q(0) if gl<=0<=gh else min(gl*gl,gh*gh)
        if rh*rh*(g2+4)-(g2+2)**2<0:continue
        gw=gh-gl;rw=rh-rl
        const=A+B*gl+C*rl+D*gl*gl+E*gl*rl+F*rl*rl
        bx=(B+2*D*gl+E*rl)*gw;by=(C+E*gl+2*F*rl)*rw
        xx=D*gw*gw;xy=E*gw*rw;yy=F*rw*rw
        bounds=[const+bx*Q(i,2)+by*Q(j,2)+(xx if i==2 else 0)+(yy if j==2 else 0)+xy*Q(i*j,4)
                for i in range(3) for j in range(3)]
        if min(bounds)>=0:continue
        require(depth<35 and count<100000,'unresolved scalar bound')
        if gw>rw:
            gm=(gl+gh)/2;stack.extend([(gl,gm,rl,rh,depth+1),(gm,gh,rl,rh,depth+1)])
        else:
            rm=(rl+rh)/2;stack.extend([(gl,gh,rl,rm,depth+1),(gl,gh,rm,rh,depth+1)])
    return count

def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent/'certificate')
    p.add_argument('--start',type=int,default=0);p.add_argument('--stop',type=int,default=70);a=p.parse_args()
    require(0<=a.start<a.stop<=70,'invalid range')
    require({v.name for v in a.directory.iterdir()}=={f'{i:03d}.json' for i in range(70)},'incomplete or extra shards')
    nodes=leaves=moment=0
    for i in range(a.start,a.stop):
        lo,hi,c=parse(a.directory/f'{i:03d}.json',i)
        nn,ll=check_tensor(c,hi);mm=check_scalar(c,lo)
        nodes+=nn;leaves+=ll;moment+=mm
        print(f'INTEGER_CHECK {i:02d}: triangles={nn}, leaves={ll}, moment_boxes={mm}',flush=True)
    if a.start==0 and a.stop==70:
        print('ACCEPTED_ALL_70_BY_INDEPENDENT_INTEGER_CHECK',nodes,leaves,moment)
        print('Analytic reduction remains as stated in the accompanying mathematical note.')
    else:print('PARTIAL_INTEGER_CHECK_ONLY',a.start,a.stop,nodes,leaves,moment)
if __name__=='__main__':main()
