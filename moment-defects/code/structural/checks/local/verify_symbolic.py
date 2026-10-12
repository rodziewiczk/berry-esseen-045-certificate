"""Optional exact symbolic checks. Not an analytic-proof verifier."""
import sympy as s
x,t,p,h,eps,n,mass,denphi = s.symbols('x t p h eps n mass denphi')
B0=s.integrate((1+x)*(1-t+x),(x,t-1,0))+s.integrate((1-x)*(1-t+x),(x,0,t))+s.integrate((1-x)*(1+t-x),(x,t,1))
B1=s.integrate((1-x)*(1-t+x),(x,t-1,1))
assert s.simplify(B0-(s.Rational(2,3)-t*t+t**3/2))==0
assert s.simplify(B1-(2-t)**3/6)==0
assert s.diff(B0,t).subs(t,1)==-s.Rational(1,2)
assert s.diff(B1,t).subs(t,1)==-s.Rational(1,2)
assert s.diff(B1,t).subs(t,2)==0
assert s.simplify((1-(1-denphi/(s.sqrt(n)*mass)))*s.sqrt(n)*mass-denphi)==0

nodes=[-h,h,1-h,1+h]
w=[(1-h)*(1+h-p)/(2*(1+2*h)),(1+h)*(1-p-h)/(2*(1-2*h)),
   (p-h)*(1+h)/(2*(1-2*h)),(1-h)*(p+h)/(2*(1+2*h))]
assert s.factor(sum(w)-1)==0
for j in (1,2,3):
    assert s.factor(sum(wi*yi**j for wi,yi in zip(w,nodes))-p)==0

# Compact defect quotient extrema used in the proof.
y=s.symbols('y',real=True)
q=1-p;r=s.sqrt(p*q)
L=2*q/(p*r)*(3*p-(1+2*p)*y)/(1-y)**2
R=2*p/(q*r)*((3-2*p)*y-p)/y**2
crit=(4*p-1)/(1+2*p)
assert s.simplify(L.subs(y,crit)-(1+2*p)**2/(2*p*r))==0
assert s.simplify(R.subs(y,p)-4/r)==0
assert s.simplify(1/L.subs(y,-s.Rational(3,8))-121*p*r/(16*q*(30*p+3)))==0
assert s.simplify(1/R.subs(y,s.Rational(3,2))-9*q*r/(4*p*(9-8*p)))==0
print('PASS: convolution transform, calibration identity, moment family, compact quotients')
print('SCOPE: symbolic identities only, not the uniform asymptotic arguments.')
