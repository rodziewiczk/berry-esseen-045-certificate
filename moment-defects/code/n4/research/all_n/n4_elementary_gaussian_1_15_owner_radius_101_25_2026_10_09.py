"""Elementary n4 Gaussian remainder 1/15 and critical-owner radius 101/25.

This NEW standalone analytic module does not alter any running certificate,
producer, dependency, receipt, or frozen radius premise. Its exact rational
checks are scalar checks, not a CDF or whole-root proof.

1. FINITE GAUSSIAN THEOREM.
Let phi(x)=phi0*exp(-x*x/2), Phi'=phi, and
 H4(z,y)=8[Phi((z-y/2)/sqrt(3/4))-Phi(z)]
          +4*y*phi(z)+z*phi(z)*(y*y-1).
For EVERY real z,y,
 |H4(z,y)| < phi0*|y|^3/6 + |y|/5 + 1/15.              (G)

Proof. Elementary Machin/alternating atan bounds give
 pi>16*(1/5-1/(3*5^3))-4/239=281476/89625>25/8;
the exponential series gives e>8/3. Consequently phi0<2/5 and
 sup_x |x|^3 phi(x)=3*sqrt(3)*phi0*exp(-3/2)<1/2,
since its square is <27*(4/25)/(8/3)^3=729/3200<1/4.
Also sup|phi''|=sup|(x*phi(x))'|=phi0: outside |x|<=1 the
maximum of (x*x-1)*exp(-x*x/2) is 2*exp(-3/2)<1.

Here is the sharper scale estimate, retaining cancellation inside the
Gaussian derivative. We claim sup_r |r*(3-r*r)*phi(r)|<3/5.
Put t=r*r. If 0<=t<=3, let S(t)=1+t+t*t/2+t*t*t/6. Exactly,
 (9/4)*S(t)-t*(3-t)^2
   =(-5*t^3+57*t^2-54*t+18)/8
   >=(42*t^2-54*t+18)/8
   =(3/4)*[7*(t-9/14)^2+3/28]>0.
Because exp(t)>=S(t), t*(3-t)^2*exp(-t)<9/4. Multiplication
by phi0^2<4/25 makes the squared Gaussian derivative <9/25.
For t>=3 its absolute value is <=|r|^3*phi(r)<1/2<3/5.
This proves the claim on the WHOLE real line, including t=0 and3.

Put w=z-y/2 and f_w(lambda)=Phi(w/sqrt(1-lambda)). For
0<=lambda<=1/4, r=w/sqrt(1-lambda), exact differentiation gives
 f'_w(0)=w*phi(w)/2,
 f''_w(lambda)=r*(3-r*r)*phi(r)/[4*(1-lambda)^2].
Thus |f''|<(3/5)/[4*(3/4)^2]=4/15, uniformly in w and lambda.
Taylor's integral remainder gives
 8[f_w(1/4)-f_w(0)]=w*phi(w)+E,  |E|<1/15.
The second-order translation expansion, with sup|Phi'''|=phi0, gives
 T=8[Phi(w)-Phi(z)]+4*y*phi(z)+z*phi(z)*y*y,
 |T|<=phi0*|y|^3/6.
The exact cancellation H4=T+[w*phi(w)-z*phi(z)]+E and
|w*phi(w)-z*phi(z)|<=phi0*|y|/2<=|y|/5 prove(G).
There is no normal-CDF numerical estimate, asymptotic substitution,
atom-count premise, or evaluation only at y=0 in this argument.

2. CANONICAL MOMENT BOUND, WITHOUT A SUPPORT ASSUMPTION.
For EX=0, EX^2=1 and rho=E|X|^3<46/25, put
 u=EX_+=EX_->0, beta=E[X|X|], v_+=(1+beta)/2,
 v_-=(1-beta)/2, w=4*u^2/(1-beta^2).
Both sign second moments are positive. Sign-tag Cauchy implies w<=1.
Sign-tag moment interpolation gives
 rho>=rhoQ=(v_+^2+v_-^2)/u,
 rhoQ^2=(1+beta^2)^2/[w*(1-beta^2)].
The function (1+b*b)^2/(1-b*b) increases with b*b on[0,1).
At b=321/500 it equals 124637947681/36739750000>(46/25)^2,
with strict cross-product difference 157406300625. Therefore
 |beta|<321/500.                                        (B)
Mass at zero is allowed; no bounded-support premise has been used.

3. WHOLE-SUPPORT CONSEQUENCE FOR AN ATTAINED CRITICAL OWNER.
Let C=C4>c=256/625, C3<C, and let(P,t=2*z) be an attained positive
CLOSED-CDF maximizing pair. The published iid Shevtsova envelope gives
 rho<(.3031*.646)/(c-.3031)=979013/532500<46/25.
The finite contamination derivative I is nonpositive everywhere and
vanishes on the WHOLE CLOSED support. Its direct measure-level
derivation is the companion finite4_contact_derivation_2026_10_09.py;
it does not require He--Cheng's eventual-exactness theorem. Using the
all-law predecessor bound, that identity implies
 rho*I(y)<=H4(z,y)+4*rho*(C3-C)+4*rho*(s-1)*C3
             +C[-|y|^3+(3/2)*rho*y*y+3*beta*y-rho/2],
 s=sqrt(4/3).
This analytic statement assumes attainment, the stated C3 bound and
Shevtsova's envelope; scalar tests do not prove those inputs.

Since 1/2<4*(s-1)<5/8, dropping the negative predecessor gap and
using(G),(B) gives, for r=|y|>=4,
 rho*I(y)<phi0*r^3/6+r/5+1/15+C*B_actual(y),
 B_actual(y)<B(r)=-r^3+(69/25)*r^2+(963/500)*r+23/100.
B(4)=-5953/500, B'(4)=-11997/500, B''(4)=-462/25, and B'''=-6.
Hence B<0 throughout r>=4. ONLY after this sign proof is it valid
to use C>c in the upper direction C*B_actual<c*B. With phi0<2/5,
 rho*I(y)<P(r),
 P(r)=-(643/1875)*r^3+(17664/15625)*r^2
                         +(77257/78125)*r+7541/46875.
At R=101/25, exactly,
 P(R)=-51557/9765625,
 P'(R)=-520966/78125,
 P''(R)=-94558/15625,
 P'''=-1286/625.
These are all negative, so P<0 on the entire ray r>=R. A closed
support point there would have I=0, a contradiction. Thus
 supp(P) subset (-101/25,101/25).                        (R)
This includes atoms, support end points and accumulation points.

Scope: (G) is unconditional elementary analysis. (R) is an owner
reduction under the named analytic inputs, NOT an all-law C4 bound,
not an exact value of C4, and not a completed root certificate. The
ongoing complete-root run still uses its frozen weaker radius17/4.
No live source or past receipt is imported or rewritten here.
"""

from fractions import Fraction as F

C0, RHO_CAP, BETA_CAP, RADIUS = F(256, 625), F(46, 25), F(321, 500), F(101, 25)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bracket_coefficients():
    return F(23, 100), F(963, 500), F(69, 25), F(-1)


def owner_coefficients():
    d, e, f, g = bracket_coefficients()
    return F(1, 15) + C0*d, F(1, 5) + C0*e, C0*f, F(1, 15) + C0*g


def polynomial_at(coefficients, x, derivative=0):
    require(type(x) is F and type(derivative) is int and 0 <= derivative <= 3,
            "Exact rational argument/derivative required")
    require(all(type(v) is F for v in coefficients), "Exact rational coefficients required")
    values = tuple(coefficients)
    for _ in range(derivative):
        values = tuple(i*v for i, v in enumerate(values) if i)
    result = F(0)
    for v in reversed(values):
        result = result*x + v
    return result


def scalar_regressions():
    """Only exact algebraic identities/signs; no CF/CDF/Gaussian producer."""
    checks = []

    def check(condition, label):
        require(condition, label)
        checks.append(label)

    pi_lo = 16*(F(1, 5)-F(1, 3*5**3))-F(4, 239)
    check(pi_lo == F(281476, 89625) and pi_lo > F(25, 8), "Elementary pi lower")
    check(27*F(4, 25)/F(8, 3)**3 == F(729, 3200) < F(1, 4),
          "Third-power normal maximum square")
    check(4 < F(8, 3)**3, "Density second derivative bound")
    # Increasing-power coefficients of (9/4)S-t(3-t)^2.
    difference = F(9, 4), -F(27, 4), F(57, 8), -F(5, 8)
    check(difference == (F(18, 8), -F(54, 8), F(57, 8), -F(5, 8)),
          "Exact cubic exponential majorant identity")
    quadratic = F(18, 8), -F(54, 8), F(42, 8)
    check(quadratic == (F(3, 4)*(7*F(9, 14)**2+F(3, 28)),
                        F(3, 4)*(-14*F(9, 14)), F(3, 4)*7),
          "Strict positive completed-square majorant")
    check(F(3, 28) > 0, "Positive quadratic remainder")
    check(F(4, 25)*F(9, 4) == F(9, 25), "Scale derivative square<9/25")
    check(F(3, 5)/(4*F(3, 4)**2) == F(4, 15), "Scale f'' bound4/15")
    check(8*F(1, 4)**2*F(4, 15)/2 == F(1, 15), "Scale remainder1/15")
    check(F(3031, 10000)*F(323, 500)/(C0-F(3031, 10000))
          == F(979013, 532500) < RHO_CAP, "SV strict owner moment cap")
    barrier = (1+BETA_CAP**2)**2/(1-BETA_CAP**2)
    check(barrier == F(124637947681, 36739750000) > RHO_CAP**2,
          "Canonical beta barrier without support")
    check(124637947681*625-36739750000*2116 == 157406300625 > 0,
          "Literal beta cross-product gap")
    check(F(9, 8)**2 < F(4, 3) < F(37, 32)**2, "Positive finite scale bracket")
    B, P = bracket_coefficients(), owner_coefficients()
    b_values = tuple(polynomial_at(B, F(4), j) for j in range(4))
    check(b_values == (-F(5953, 500), -F(11997, 500), -F(462, 25), F(-6)),
          "Negative B and three derivatives at4")
    check(P == (F(7541, 46875), F(77257, 78125), F(17664, 15625), -F(643, 1875)),
          "Exact new owner cubic coefficients")
    values = tuple(polynomial_at(P, RADIUS, j) for j in range(4))
    check(values == (-F(51557, 9765625), -F(520966, 78125),
                      -F(94558, 15625), -F(1286, 625))
          and all(v < 0 for v in values), "Entire-ray negative owner polynomial")
    check(4 < RADIUS < F(81, 20) < F(17, 4), "Strictly improved owner radius")
    check(F(1, 15) < F(5, 36) < F(1, 2), "Strictly improved Gaussian charge")
    return {"status": "EXACT_SCALARS_FOR_ELEMENTARY_GAUSSIAN_1_15_OWNER_RADIUS_101_25",
            "exact_comparisons": len(checks), "Gaussian_additive_constant": F(1, 15),
            "owner_radius": RADIUS, "owner_polynomial_and_derivatives_at_radius": values,
            "producer_or_root_called": False,
            "owner_reduction_REQUIRES_named_analytic_inputs": True,
            "entire_root_or_unrestricted_C4_proved": False,
            "live_dependencies_or_old_receipts_modified": False}


if __name__ == "__main__":
    import json
    print(json.dumps(scalar_regressions(), sort_keys=True, default=str))
