#!/usr/bin/env python3
"""Optional exact symbolic audit; needs SymPy. Not used by the rational checkers."""
from fractions import Fraction as F
import sympy as S

def require(ok,label):
    if not ok:raise ValueError(label)

def zero(expr,label):
    require(S.factor(expr)==0,label);print('PASS:',label)

a,R,y=S.symbols('a R y',positive=True)
b=1/a;s=a+b;g=b-a
cg=g*(g*g+6)/s**3
wp=y**3-cg*y**3-12*y*y/s**3+6*g*y/s**3+4/s**3
wn=y**3+cg*y**3-12*y*y/s**3-6*g*y/s**3+4/s**3
zero(wp-2*a*a/s**3*(y-b)**2*(2+(a+3*b)*y),'positive defect factorization')
zero(wn-2*b*b/s**3*(y-a)**2*(2+(3*a+b)*y),'negative defect factorization')
zero((y*y-g*y-1)**2-(y+a)**2*(y-b)**2,'fourth-moment residual factorization')
Jp=s**3*(R+a)**2/(2*a*a*(2+(a+3*b)*R))
Jm=s**3*(R+b)**2/(2*b*b*(2+(3*a+b)*R))
gap=s**3*(b-a)*R*((s*s+2)*R*R+4*s*R+2)/(2*(2+(a+3*b)*R)*(2+(3*a+b)*R))
zero(Jp-Jm-gap,'positive-ray response dominates negative ray')
num=-6*R**2+R*a*(a**4+5*a*a-8)+3*a*a*(a*a-1)
den=a**5*(R*a*a+3*R+2*a)**2
zero(S.diff(Jp,a)-(R+a)*(a*a+1)**2*num/den,'monotonicity of bounded-support coefficient')
M5=S.simplify(Jp.subs({R:5,a:S.sqrt(S.Rational(2,3))}))
zero(M5-S.Rational(514375,72024)-S.Rational(4125,6002)*S.sqrt(6),'exact endpoint coefficient at R=5, p=2/5')
require(F(49,20)**2>6,'sqrt6 upper')
require(F(514375,72024)+F(4125,6002)*F(49,20)<9,'M5 < 9')
print('PASS: bounded-support quartic Fourier coefficient <= 3/8')
# Contamination derivative at n=2.
e,x,rho,m,ph,lam,FF,HH,a3=S.symbols('e x rho m ph lam F H a3',real=True)
var=1+e*(y*y-1)-e*e*y*y
xp=S.diff((x-S.sqrt(2)*e*y)/S.sqrt(var),e).subs(e,0)
raw=rho+e*(a3-rho-3*m*y)
rhop=S.diff(raw*var**S.Rational(-3,2),e).subs(e,0)
QQ=lam*a3-(x*ph+3*lam*rho)*y*y/2-(S.sqrt(2)*ph+3*lam*m)*y+2*FF+(x*ph+lam*rho)/2
zero(2*(HH-FF)-ph*xp-lam*rhop-(2*HH-QQ),'n=2 contact inequality normalization')
print('PASS: exact algebra only; probability arguments require mathematical review.')
