"""Generate an exact dependent-law obstruction to the 5-feature tensor relaxation.
Uses SciPy and SymPy as untrusted construction tools. The resulting JSON can be
checked with Fraction alone; it is NOT an iid counterexample.
"""
import itertools as it
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
import sympy as S
root=Path(__file__).resolve().parent
BAS=list(it.combinations_with_replacement(range(5),3));PERM=[sorted(set(it.permutations(k))) for k in BAS]
grid=sorted(set([F(-9)+F(3,2)*j for j in range(13)]+[F(17*j,100) for j in range(-10,11)]+[F(-1),F(0),F(1)]))
t=F(-3,5);rho=F(6,5);ga=F(3,8)
pts=list(it.combinations_with_replacement(grid,3))
for x,y in it.combinations_with_replacement(grid,2):
 z=t-x-y
 if -9<=z<=9:pts.append(tuple(sorted([x,y,z])))
pts=sorted(set(pts));arr=np.array([[float(u) for u in v] for v in pts]);x,y,z=arr.T
ff=[np.array([np.ones(q.shape),q,q*q,q**3,abs(q)**3]) for q in [x,y,z]]
A=np.array([sum(ff[0][i]*ff[1][j]*ff[2][k] for i,j,k in perms)/len(perms) for perms in PERM]).T
mm=[F(1),F(0),F(1),ga,rho];mom=[mm[i]*mm[j]*mm[k] for i,j,k in BAS]
rhs=np.array([float(sum(p)<=t) for p in pts])
sol=linprog([float(v) for v in mom],A_ub=-A,b_ub=-rhs,bounds=[(None,None)]*len(BAS),method='highs')
if not sol.success:raise RuntimeError(sol.message)
w=-sol.ineqlin.marginals;active=np.flatnonzero(w>1e-9)
print('active orbit count',len(active),'mass',sum(w[active]),'cdf',sol.fun,flush=True)

def feat(q):return [F(1),q,q*q,q**3,abs(q)**3]
def row(v):
 f=[feat(x) for x in v]
 return [sum((f[0][i]*f[1][j]*f[2][k] for i,j,k in perms),F(0))/len(perms) for perms in PERM]
rat=lambda x:S.Rational(x.numerator,x.denominator)
M=S.Matrix([[rat(v) for v in row(pts[j])] for j in active]).T
bb=S.Matrix([rat(v) for v in mom])
print('exact solve',M.shape,flush=True)
ww=M.inv()*bb if M.rows==M.cols else M.gauss_jordan_solve(bb)[0]
if any(v<=0 for v in ww):raise RuntimeError('nonpositive exact weight')
if M*ww!=bb:raise RuntimeError('exact moments mismatch')
weights=[F(int(v.p),int(v.q)) for v in ww]
cdf=sum((ww for j,ww in zip(active,weights) if sum(pts[j])<=t),F(0))
# phi_0 > 997/2500; sqrt(3) between 433/250 and 1733/1000.
zlo=F(433,1250);zhi=F(1733,5000)
normal_hi=F(1,2)-F(997,2500)*(zlo-zhi**3/6)
score_lo=F(433,250)/rho*(cdf-normal_hi)
if not score_lo>F(41,100):raise RuntimeError('no strict obstruction')
record={'format':'dependent-three-coordinate-tensor-obstruction-v1','rho':str(rho),'gamma':str(ga),'threshold':str(t),
        'orbits':[{'triple':[str(x) for x in pts[j]],'weight':str(ww)} for j,ww in zip(active,weights)]}
(root/'n3_dependent_obstruction.json').write_text(json.dumps(record,indent=2)+'\n')
print('EXACT_DEPENDENT_RELAXATION_OBSTRUCTION',len(weights),'score lower approx',float(score_lo),flush=True)
