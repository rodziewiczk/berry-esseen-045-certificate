"""Independent standard-library check of the numerical proof margins.
This checks rational arithmetic, not the analytic theorems.
"""
from fractions import Fraction as F
from math import comb
if not __debug__:
    raise RuntimeError('Run without -O: assertions are proof obligations.')

def shift(c, a):
    # Ascending coefficient order; exact expansion of p(a+u).
    return [sum((c[k]*comb(k,j)*a**(k-j) for k in range(j,len(c))),F(0))
            for j in range(len(c))]

def atan(z,m):
    return sum(((-1)**k*z**(2*k+1)/F(2*k+1) for k in range(m+1)),F(0))
lo=16*atan(F(1,5),9)-4*atan(F(1,239),2)
hi=16*atan(F(1,5),8)-4*atan(F(1,239),3)
assert lo>F(3141,1000) and hi<F(22,7)
assert 2*hi*F(199,500)**2<1<2*lo*F(399,1000)**2
assert F(2,9)*hi**4<22
assert 22*F(21,20)**4<27
assert F(73728,570375)*F(19,20)**4>F(1,10)
assert 1+4/lo**2<F(6,5)**2
assert F(6,5)/F(61,50)==F(60,61)
assert F(199,500)/F(52,25)>F(19,100)

E=[F(13,80000),F(13,37500),F(13,40000),F(13,40000)]
Pp=[F(-1,2000000),F(-4873,100000),F(-13161,20000),F(1027,3000)]
Pm=[F(-1,2000000),F(-53987,1000000),F(-13161,20000),F(2851,6000)]
Pp=[a-b for a,b in zip(Pp,E)];Pm=[a-b for a,b in zip(Pm,E)]
assert shift(Pp,F(2))==[F(12751,3000000),F(426457,300000),F(55747,40000),F(41041,120000)]
assert shift(Pm,F(3,2))==[F(316667,8000000),F(14108671,12000000),F(118273,80000),F(56981,120000)]
P0=[F(-899,3000),F(-19457,40000),F(-91,100),F(1027,3000)]
assert all(c>0 for c in shift(P0,F(4)))
Pp[0]-=F(33,1000); Pm[0]-=F(33,1000)
assert all(c>0 for c in shift(Pp,F(21,10)))
assert all(c>0 for c in shift(Pm,F(3,2)))
print('PASS: independent rational spectral and support margins')
