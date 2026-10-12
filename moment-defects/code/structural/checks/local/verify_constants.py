"""Exact rational checks for Calibrated_local_domination.tex.

Scope: constants, polynomial coefficients, and budget arithmetic ONLY.
This is not a formal verification of the analytic proof.
"""
from fractions import Fraction as F


def atan_sum(x, m):
    return sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(m+1)),F(0))

pi_lo=16*atan_sum(F(1,5),9)-4*atan_sum(F(1,239),2)
pi_hi=16*atan_sum(F(1,5),8)-4*atan_sum(F(1,239),3)
assert F(3)<pi_lo<pi_hi<F(22,7)
assert 2*pi_hi*F(199,500)**2<1
assert pi_hi**2<F(10)
assert 2*pi_hi**4/F(9)<22

# Real response loss at frequency one, including rotated phases.
r0=F(512,1215)
theta0=F(1,1000)
assert F(32,9)*F(16,135)==r0
assert r0-44*pi_hi*theta0>F(1,4)
assert F(199,24000)*F(31,32)>F(1,128)

# Pointwise kernel bounds. T4' is bounded in modulus by 2/3.
assert F(1,24)+F(1,12)/pi_lo<F(1,2)
assert F(1,3)+F(1,24)+F(1,12)/pi_lo<1
# Exact corrected kernel values, origin / first return / endpoint.
origin=F(1,2)-F(1,12)*F(1,2)
return_value=F(1,12)*F(1,4)
assert origin==F(11,24)
assert return_value==F(1,48)
assert F(11,24)-F(7,16)==F(1,48)

# Uniform response derivative bounds on [0,2].
z=4*pi_hi
rprime=(2*pi_hi)*(F(3,2)*z**4+4*z**3)/72
rsecond=(2*pi_hi)**2*(F(9,4)*z**4+12*z**3+12*z**2)/72
assert rprime<6000
assert rsecond<60000

# Nonlinear integral remainder <= 1,500,000 (nd)^2.
alpha=F(24,25)
assert pi_hi/alpha<4
zero_tail=F(8712)/(alpha**4*128)
other_peaks=3*352**2*4
assert other_peaks+zero_tail<1500000
small=F(1,10**9)
assert F(8800,3)*small<1
assert F(1,128)-1500000*small>F(1,256)

# Uniform negative curvature in the calibrated binomial score.
cos_lower=1-2*pi_hi**2*theta0**2
curvature_lower=F(1,12)*2*pi_lo**2*2*F(199,500)*F(31,32)*cos_lower
assert curvature_lower>1

# Explicit outer entry on the fixed short-support neighborhood.
dstar=F(1,10**7)
h=F(1,100)
x=F(48,25)*h*h
assert 1-x+x*x/2+352*dstar<1-F(1,10000)
assert 1-2*F(11,25)*pi_hi**2*h*h-352*dstar>F(1,2)
curvature_b=4*pi_lo**2*F(6,25)*(1-2*pi_hi**2*h*h)
assert curvature_b>8
err=2*60000*dstar+28*6000*dstar+240*352*dstar
assert err<1
assert F(199,500)/(12*F(13,25))>F(3,50)
assert F(3,50)-F(1,400)==F(23,400)

print('PASS: exact constants for finite-row calibration and local domination')
print('majorant: M - H/12 + eps V, |eps| <= 1/4')
print('return kernel real part = 1/48; rotated response < -1/4')
print('nonlinear remainder <= 1500000 (nd)^2')
print('local windows: |z| <= 1/4, |theta| <= 1/1000, nd <= 1e-9')
print('strict local penalties: theta^2/(4 rho) + nd/(256 rho)')
print('fixed short-support neighborhood: d <= 1e-7')
print('SCOPE: exact finite arithmetic, not verification of analytic estimates or a numerical N.')
