#!/usr/bin/env python3
"""Optional exact symbolic cross-check; SymPy needed, not used by verify.py."""
import sympy as S
from itertools import combinations_with_replacement

y,e,rho,m,x,phi,F,D,lam,eps=S.symbols('y e rho m x phi F D lam eps',real=True)
rt=S.sqrt(3)
variance=1+eps*(y*y-1)-eps**2*y*y
mu=eps*y
xx=(rt*x-3*mu)/(rt*S.sqrt(variance))
assert S.simplify(S.diff(xx,eps).subs(eps,0)+rt*y+x*(y*y-1)/2)==0
# First raw central absolute moment derivative before variance normalization.
raw_derivative=S.Abs(y)**3-rho-3*y*m
rho_derivative=raw_derivative-S.Rational(3,2)*rho*(y*y-1)
assert S.simplify(rho_derivative-(S.Abs(y)**3-3*m*y+rho/2-3*rho*y*y/2))==0
G=S.symbols('G')
score_derivative=3*(G-F)-phi*(-rt*y-x*(y*y-1)/2)-lam*rho_derivative
Q=lam*S.Abs(y)**3-(x*phi+3*D)*y*y/2-(rt*phi+3*lam*m)*y+3*F+(x*phi+D)/2
assert S.simplify((3*G-score_derivative-Q).subs(D,lam*rho))==0
u=S.symbols('u')
p=S.Rational(8,35)*y**3-S.Rational(4,5)*y*y-S.Rational(8,5)*y-S.Rational(1,8)-3
shift=S.Poly(S.expand(p.subs(y,6+u)),u)
assert shift.all_coeffs()==[S.Rational(8,35),S.Rational(116,35),S.Rational(472,35),S.Rational(2197,280)]
ids=[a for a in combinations_with_replacement(range(7),3) if max(a)<5 or any(i in (1,2) for i in a)]
assert len(ids)==59
assert sum(max(a)>=5 for a in ids)==24
m4,m5,g,r=S.symbols('m4 m5 g r')
means=[1,0,0,g,r,m4,m5]
for a in ids:
 expr=S.sympify(S.prod(means[i] for i in a))
 assert not (expr.has(m4) or expr.has(m5))
 if any(i not in (0,3,4) for i in a):assert expr==0
 else:assert expr==g**a.count(3)*r**a.count(4)
# Bernstein half-space lemma: exact representation of affine coordinate
z=S.symbols('z')
B=[S.binomial(5,i)*z**i*(1-z)**(5-i) for i in range(6)]
assert S.expand(sum(B))==1
assert S.expand(sum(S.Rational(i,5)*B[i] for i in range(6)))==z
for j in range(6):
 left=sum(S.binomial(i,j)/S.Integer(2)**i*B[i] for i in range(j,6))
 right=sum(S.binomial(5-i,j-i)/S.Integer(2)**(5-i)*B[i] for i in range(j+1))
 assert S.expand(left-B[j].subs(z,z/2))==0
 assert S.expand(right-B[j].subs(z,(1+z)/2))==0
print('PASS: exact normalization, contact, support, 59-feature, affine and subdivision identities.')
print('These algebra checks do not replace the analytic proof or the full certificate checker.')
