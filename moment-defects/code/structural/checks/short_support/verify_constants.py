"""Exact algebra/arithmetic checks; not a formalization of the analytic proof."""
from fractions import Fraction as F
import sympy as S
if not __debug__:
    raise RuntimeError("Run without -O: assertions are proof obligations.")

a,x,u,y,p=S.symbols('a x u y p', positive=True)
b=1/a; s=a+b; gam=b-a
cg=gam*(gam**2+6)/s**3
wplus=x**3-cg*x**3-12*x**2/s**3+6*gam*x/s**3+4/s**3
wminus=u**3+cg*u**3-12*u**2/s**3-6*gam*u/s**3+4/s**3
coeff=S.symbols('c0:4')
H=sum(coeff[j]*x**j for j in range(4))
sol=S.solve([H.subs(x,-a)+a*a,S.diff(H,x).subs(x,-a)-2*a,H.subs(x,b)-b*b,S.diff(H,x).subs(x,b)-2*b],coeff)
H=S.factor(H.subs(sol))
assert S.simplify((x*x-H)/wplus-(-(-a**3+a+2*x)/(a*(a*a*x+2*a+3*x))))==0
assert S.simplify((-u*u-H.subs(x,-u))/wminus-(2*a**3*u+a*a-1)/((3*a*a+1)*u+2*a))==0
assert S.expand((a-1)*(4*a*a+a+1))==4*a**3-3*a*a-1
print('PASS signed-second-moment Hermite identities')

# Defect quotient extrema.
L=(3*p-(1+2*p)*y)/(1-y)**2
assert S.factor(S.diff(L,y)-(4*p-1-(1+2*p)*y)/(1-y)**3)==0
y0=(4*p-1)/(1+2*p)
assert S.simplify(L.subs(y,y0)-(1+2*p)**2/(4*(1-p)))==0
assert F(81,10)/F(24,25)==F(135,16)
assert F(121,480)<F(1,3) and F(135,464)<F(1,3)
assert F(25,3)<F(135,16)
assert 2/(F(4,5)*F(11,3))==F(15,22)
assert F(3,25)-F(15,22000)>F(119,1000)
assert F(1,5)+F(1,2000)<F(201,1000)
assert F(169,150)<F(16,15)**2
assert F(16,15)+F(1,1000)<F(107,100)
assert F(1,72)/F(6,25)**2==F(625,2592)<F(1,4)
print('PASS compact defect equivalence and moment constants')

# Elementary normal constants: pi via Machin alternating sums.
def atan_sum(z,m): return sum(((-1)**k*z**(2*k+1)/F(2*k+1) for k in range(m+1)),F(0))
pi_lo=16*atan_sum(F(1,5),9)-4*atan_sum(F(1,239),2)
pi_hi=16*atan_sum(F(1,5),8)-4*atan_sum(F(1,239),3)
assert F(3141,1000)<pi_lo<pi_hi<F(22,7)
assert F(199,500)**2*2*pi_hi<1
assert F(399,1000)**2*2*pi_lo>1
# 3.1622776 < sqrt10 < 3.1622777.
s10lo=F(31622776,10**7); s10hi=F(31622777,10**7)
assert s10lo*s10lo<10<s10hi*s10hi
assert (3+s10lo)**2 > F(409,1000)**2*72*pi_hi
assert (3+s10hi)**2 < F(41,100)**2*72*pi_lo
assert F(2,9)*F(22,7)**4<22
assert 22*F(21,20)**4<27
assert 1-F(11,500)-F(27,1000)>F(19,20)
assert F(121,875)+F(27,1000)<F(1,6)
assert F(10,57)<pi_lo/10
assert F(21,20)*F(-3,8)-F(1,20)==F(-71,160)
assert F(21,20)*F(3,2)+F(1,20)==F(13,8)
assert (F(13,8)*(F(13,8)-1))/(2-F(13,8))==F(65,24)
coercivity=F(73728,570375)*F(19,20)**4
assert coercivity>F(1,10)
print('PASS spectral strip constants; exact coercivity lower:',coercivity)

# Preliminary support bound without a bounded-support assumption.
assert (3+s10lo)**2 > F(4097,10000)**2*72*pi_hi
assert F(4097,10000)-F(3,100*10**6)>F(409,1000)
assert F(1661,5000)*(1+F(429,1000))<F(19,40)
assert F(1661,5000)*(F(107,100)+F(429,1000))<F(1,2)
assert F(3,100)*F(107,100)*(1+F(1,2*10**6))+F(41,100)*F(107,100*10**6)<F(33,1000)
r=S.symbols('r')
P0=S.Rational(1027,3000)*r**3-S.Rational(91,100)*r**2-S.Rational(19457,40000)*r-S.Rational(899,3000)
P0shift=S.Poly(S.expand(P0.subs(r,u+4)),u)
assert all(c>0 for c in P0shift.all_coeffs())
print('preliminary support shifted polynomial:',P0shift.as_expr())
# Gaussian comparison and shifted support polynomials.
N=10**6
rn2=F(N,N-1)
assert F(5,4)*rn2**2<F(13,10)
assert rn2/F(10000)<F(1,9000)
assert F(199,500)*F(8999,9000)*F(17999,18000)>F(397,1000)
assert rn2**3*F(399,1000)**2<F(2,5)**2
r=S.symbols('r')
err=S.Rational(13,10000)*(r**3/4+r**2/4+4*r/15+S.Rational(1,8))
Pp=S.Rational(1027,3000)*r**3-S.Rational(13161,20000)*r**2-S.Rational(4873,100000)*r-S.Rational(1,2*N)-err
Pm=S.Rational(2851,6000)*r**3-S.Rational(13161,20000)*r**2-S.Rational(53987,10**6)*r-S.Rational(1,2*N)-err
for name,pol,start in [('positive',Pp,S.Integer(2)),('negative',Pm,S.Rational(3,2))]:
    shifted=S.Poly(S.expand(pol.subs(r,u+start)),u)
    assert all(c>0 for c in shifted.all_coeffs())
    print(name,'shifted polynomial:',shifted.as_expr())
assert F(2,5)-F(3,4)>F(-3,8)
assert F(11,25)+1<F(3,2)
assert F(3,100)*(F(107,100)+F(67,10**6))<F(33,1000)
for name,pol,start in [('competitive-positive',Pp,S.Rational(21,10)),('competitive-negative',Pm,S.Rational(3,2))]:
    sh=S.Poly(S.expand(pol.subs(r,u+start)-S.Rational(33,1000)),u)
    assert all(c>0 for c in sh.all_coeffs())
    print(name,'shifted polynomial:',sh.as_expr())
assert F(11,25)+F(21,20)<F(3,2)
print('PASS explicit localized support bounds, including competitive maximizers')

# Doubled-bandwidth constants.
assert 1+4/pi_lo**2<F(6,5)**2
assert 1+F(1,5)+F(1,50)==F(61,50)
assert F(6,5)*F(50,61)==F(60,61)
assert F(199,500)/(4*F(13,25))>F(19,100)
assert F(19,100)/61==F(19,6100)
print('PASS doubled-bandwidth gap constants')

# Exact limiting support endpoints.
t=S.sqrt(10); ps=(4-t)/2; qs=1-ps
ss=1/S.sqrt(ps*qs); rs=(ps**2+qs**2)*ss
ce=(3+t)/6 # cancel phi(0)
Lm=3*ce*rs/(2*(ce+S.Rational(1,6)))
Up=3*ce*rs/(2*(ce-S.Rational(1,6)))
assert S.simplify(ps-Lm/ss-(S.Rational(9,2)-3*t/2))==0
assert S.simplify(ps+Up/ss-(S.Rational(9,2)-t))==0
assert S.simplify(3*ce*(1-2*ps)-S.Rational(1,2))==0
print('PASS exact limiting support identities')
print('ALL_EXACT_CHECKS_PASSED')
