"""Integrated all-law n4 reduction, CONDITIONAL on a COMPLETE physical ROOT.

This NEW standalone analytic source changes NO active dependency, run,
receipt, frozen source or accepted theorem. No producer/root job is run.
Its dormant Fraction checks establish only finite scalar identities.
The full conditional proof is below; it does not assume imported
He--Cheng contact Lemma4.3, Gaussian(70), eventual exactness, a finite
atom count, or an independent original fourth-moment hypothesis.

DEFINITIONS, ACCEPTED INPUTS, AND THE ACTUAL REMAINING REQUIREMENT
For a standardized real law P, EX0,EX^2=1 and rho(P)=E|X|^3<infinity,
let F_{n,P}(t)=P(X1+...+Xn<=t), a CLOSED CDF, and
 R_n(P)=sqrt(n)*sup_t |F_{n,P}(t)-Phi(t/sqrt(n))|/rho(P),
 C_n=sup_P R_n(P), C_E=(3+sqrt(10))*phi0/6,
 phi0=1/sqrt(2pi), T=4097/10000, c=256/625.
The copies are iid. The three accepted external analytic ingredients are:
 (A) ALL-LAW C3<=K3=59sqrt(3)/250, not merely a binary/three-atom result;
 (SV) R_n(P)<=3031/10000*(1+(323/500)/rho(P)), in particular n4;
 (PW) the retained one-sided CLOSED-CDF Prawitz majorant and its
      original-physical-law quadrature/interpolation bridge, if used to
      establish the full physical-root inequality specified next.
Input(A) is recorded in research/accepted_external_results_20260909.md;
the supplied n3 analytic proof/data/checkers are separate from this file.
No scalar test or n4 receipt re-proves the n3 certificate. Input(SV) is
the published iid Shevtsova envelope. Input(PW) belongs to the actual
root proof, not the purely analytic contradiction after that proof.

For a finite real U>=0, COMPLETE_ROOT(U) denotes the MATHEMATICAL statement:
 EVERY standardized iid actual P with support in[-17/4,17/4],
 rho(P)<46/25, canonical eta>=0, w in[625/2116,1], and
 |beta| in[0,13/20], satisfying actualrho=rhoQ_actual+eta,
 obeys R4(P)<=U, at ALL thresholds and BOTH signed discrepancies.
In(|beta|,orientation) coordinates it must cover both actual reflected
laws, zero atoms, eta0,w1, all shared geometry/eta faces and all tails.
This is precisely the remaining whole-root certificate requirement.
It is NOT an extra trusted Boolean/Prop/status/hash/JSON gate. A numerical
claim must complete every root class and be faithfully recomputed in a
fresh independent replay of the actual mathematical acceptance path.
An UNKNOWN label alone, truncated prefix, historic success mask or sampled
bound does not supply COMPLETE_ROOT. Conversely a failed T-label does not
invalidate a separately established complete uniform U. This file supplies
neither that bound nor its acceptance from any status record.

THEOREM. Under(A),(SV) and an actually established COMPLETE_ROOT(U),
                 C4<=max(c,U).                          (GENERAL)
In particular U<=T implies C4<=T<C_E.                   (RESULT)
Even a complete VALID U>T but U<C_E implies C4<C_E, since c<T<C_E;
a failed T-test alone is not proof that such a uniform U is invalid.
Using(PW) to prove COMPLETE_ROOT(U) is an explicit analytic input. Equality
C4=T (or C4=max(c,U)) is not excluded. Other indices and C*=C_E remain
separate; there is no claim of all-index completion.

1. COMPACT EXACT COMPARISON K3<c<T<C_E, INDEPENDENT OF ROOT NUMERICS
For q0 in(0,1), put A(q0,m)=sum_{k=0}^m (-1)^k*q0^(2k+1)/(2k+1).
The alternating integral expansion of atan gives upper for even m,
lower for odd m. Machin's identity is exact:
 pi=16atan(1/5)-4atan(1/239).
There is no hidden numerical branch: atan(1/5)<pi/8 because
tan(pi/8)=sqrt(2)-1>1/5 (sqrt(2)>6/5). Thus
0<4atan(1/5)-atan(1/239)<pi/2. Tangent doubling gives5/12 then120/119;
tangent subtraction of1/239 gives1, so this angle equals pi/4.
Consequently
 pi<16A(1/5,4)-4A(1/239,1)<3927/1250.
The last comparison is a finite rational inequality. With p=19947/50000,
 1-2*(3927/1250)*p^2=14209057/1562500000000>0,
so phi0>p. Also
 10-(15811/5000)^2=12279/25000000>0,
so sqrt(10)>15811/5000. All factors are positive, hence
 C_E>(3+15811/5000)*p/6=204862339/500000000>T,
 the exact strict gap being12339/500000000.
Finally
 c^2-K3^2=1069/1562500>0, and T-c=1/10000>0.
These exact comparisons use no CF/CDF/root producer or old receipt.

2. ATTAINMENT ABOVE c, WITH ATOMS AND POSSIBLE M3 MASS LOSS
Suppose contrary to(GENERAL) that C4>max(c,U), hence C4>c. The bound(SV), rho>=1,
makes C4 finite. The all-law absolute supremum equals the supremum of
positive CLOSED signed discrepancies across all standardized laws.
Indeed a negative closed gap Phi(t/2)-F4_P(t) is the limit of positive
closed gaps for -P at raw thresholds-t-eps as eps decreases0:
 F4_{-P}(-t-eps)=1-F4_P((t+eps)-)->1-F4_P(t).
Continuity of Phi and right continuity of the CLOSED CDF justify the
limit. Do NOT replace a reflected closed CDF by1-F4_P(t) at a fixed
atomic threshold; its exact identity there uses F4_P(t-).

Choose positive signed pairs(P_j,t_j) with ratios r_j->C4 and discard
a prefix so r_j>c. Each law is standardized. From(SV),
 1<=rho_j<M=(3031/10000)*(323/500)/(c-3031/10000)
           =979013/532500<46/25.
Tightness follows from EX_j^2=1. Uniform square integrability follows
from E[X_j^2;|X_j|>A]<=M/A. A weakly convergent subsequence therefore
preserves EX0 and EX^2=1. Select further rho_j->b in[1,M]. Lower
semicontinuity gives rho(P)<=b, finite; it does NOT assume M3 convergence.

The raw thresholds are bounded. The positive discrepancy is
r_j*rho_j/2>c/2. For t_j<0 it is <=F4_Pj(t_j)<=4/t_j^2 by Chebyshev.
For t_j>0 it is <=1-Phi(t_j/2)<=4/t_j^2 by the normal second-moment
tail bound. Thus |t_j|^2<8/c when t_j!=0; pass to t_j->t.
Weak convergence of product laws and the continuous sum map give
convolution weak convergence. For every d>0, eventually t_j<=t+d;
the fixed CLOSED-set Portmanteau inequality and continuity from above
as d decreases0 give
 F4_P(t)>=limsup_j F4_Pj(t_j).
Phi is continuous, so F4_P(t)-Phi(t/2)>=C4*b/2>0. By definition,
 C4>=R4(P)>=2[F4_P(t)-Phi(t/2)]/rho(P)
               >=C4*b/rho(P)>=C4.
Equality holds everywhere, forcing rho(P)=b and an actual attained
POSITIVE CLOSED unrestricted maximizing pair(P,t) with R4(P)=C4.
Reapplying(SV) to this actual ratio C4>c gives rho(P)<M<46/25,
strictly, even though the compactness limit alone only gave b<=M.
This is the complete attainment-above-c argument from the project
quantitative transfer, independent of any Esseen-level HC theorem.

3. OWN FINITE4 CONTACT, NOT AN IMPORTED CONTACT THEOREM
Write C=C4,z=t/2,beta=E[X|X|], and G=F3_P. For ANY real y use the
actual contamination P_eps=(1-eps)P+eps delta_y, holding raw t fixed.
Its mean m_eps=eps y and variance
 v_eps=1+eps(y^2-1)-eps^2y^2 stay valid for small eps>=0.
Let centralrho_eps=E_{P_eps}|X-m_eps|^3. Standardizing this ACTUAL
law and threshold yields the signed ratio
 R_eps=2v_eps^(3/2)/centralrho_eps
             *[F4_Peps(t)-Phi((t-4m_eps)/(2sqrt(v_eps)))]<=C.
This inequality uses the UNRESTRICTED global C4 supremum. A maximizer
only inside physical ROOT would NOT justify arbitrary contaminations,
which may leave that class. Here attainment supplied the global owner.

The fixed raw CDF is a degree4 mixture polynomial, atoms included,
so its derivative is4[G(t-y)-F4_P(t)]. Dominated differentiation of
|x-eps y|^3 uses the integrable M2 majorant3|y|(|x|+|y|)^2, and yields
 centralrho'_0=|y|^3-rho-3beta y.
Also v'_0=y^2-1 and z'_0=-2y-z(y^2-1)/2. Therefore I(y)=R'_0(y)<=0,
and exactly
 rho I(y)=8[G(t-y)-F4_P(t)]+4yphi(z)+zphi(z)(y^2-1)
             +(3/2)C rho(y^2-1)-C(|y|^3-rho-3beta y).
Tonelli and the SAME moments give int I(y)dP(y)=0, hence I0 P-a.s.
The CLOSED CDF is uppersemicontinuous: G(s_j) has limsup<=G(s+d)
for every d>0, and G(s+d)->G(s). Thus I is uppersemicontinuous;
since I<=0, {I=0}={I>=0} is closed and has full P measure. It contains
the WHOLE CLOSED support, including ends and accumulation points.

Use(A) DIRECTLY on this original standardized P's predecessor. With
s=sqrt(4/3), 8/sqrt(3)=4s and F4_P(t)=Phi(z)+C rho/2, this gives
 rho I(y)<=H4(z,y)+4rho(K3-C)+4rho(s-1)K3
                 +C[-|y|^3+(3/2)rho y^2+3beta y-rho/2],
 H4=8[Phi((z-y/2)/sqrt(3/4))-Phi(z)]
                         +4yphi(z)+zphi(z)(y^2-1).
K3 is a valid ALL-LAW upper constant, not asserted to be the optimal
C3 value. Since K3<c<C, its predecessor gap is strictly negative.
This is the self-contained finite4 contact derivation in companion
finite4_contact_derivation_2026_10_09.py (frozen e9acee7c...).

4. OWN FINITE GAUSSIAN ANALYSIS AND BOUNDED OWNER, NO Gaussian(70)
Elementary Machin bounds give pi>281476/89625>25/8, so phi0<2/5;
the exponential series gives e>8/3. Thus sup|x|^3phi(x)<1/2 and
sup|phi''|=sup|(xphi)'|=phi0. A sharper elementary bound is
 sup_r |r(3-r^2)phi(r)|<3/5.
To check it, put q=r^2. For0<=q<=3,
 (9/4)(1+q+q^2/2+q^3/6)-q(3-q)^2
 =(-5q^3+57q^2-54q+18)/8
 >=(42q^2-54q+18)/8=(3/4)[7(q-9/14)^2+3/28]>0.
Since exp(q) dominates that positive series and phi0^2<4/25, the
squared derivative is <9/25. For q>=3 use |r|^3phi(r)<1/2.
For w=z-y/2 and f(lambda)=Phi(w/sqrt(1-lambda)),
 f'(0)=wphi(w)/2, f''=r(3-r^2)phi(r)/(4(1-lambda)^2).
On lambda[0,1/4], |f''|<4/15, so
 8[f(1/4)-f(0)]=wphi(w)+E, |E|<1/15.
Second-order translation of Phi has remainder<=phi0|y|^3/6 after
multiplication by8. The exact H4 decomposition adds wphi(w)-zphi(z),
whose magnitude is <=phi0|y|/2<=|y|/5. Hence, ALL real z,y,
 |H4(z,y)|<phi0|y|^3/6+|y|/5+1/15.

Here are the canonical moment facts, before any support premise.
Let u=EX+=EX->0, v+=(1+beta)/2>0,v-=(1-beta)/2>0,
 w=4u^2/(1-beta^2). Sign-tag Cauchy gives0<w<=1. Define a=v-/u,
b=v+/u and the genuine Q3 masses u/a at-a,u/b at b,1-w at0.
Q has mean0 and variance1. Weighted square moment defects give
 eta=rho-rhoQ>=0, rhoQ=(v+^2+v-^2)/u,
 rhoQ^2=(1+beta^2)^2/[w(1-beta^2)].
At |beta|=321/500 the lower bound at w1 is
124637947681/36739750000>(46/25)^2 (cross-gap157406300625).
Monotonicity in beta^2 and rhoQ<=rho<46/25 imply |beta|<321/500.

Since1/2<4(s-1)<5/8, drop the strictly negative predecessor gap,
replace K3 by C in the positive scale term, and put r=|y|>=4:
 rho I(y)<phi0r^3/6+r/5+1/15+C B_actual(y),
 B_actual(y)<B(r)=-r^3+(69/25)r^2+(963/500)r+23/100.
B,B',B'',B''' at4 are -5953/500,-11997/500,-462/25,-6.
Thus B<0 on that ray. ONLY then use C>c with the negative bracket:
 rho I(y)<P(r)=-(643/1875)r^3+(17664/15625)r^2
                                      +(77257/78125)r+7541/46875.
At R=101/25, P and its first three derivatives are exactly
 -51557/9765625, -520966/78125, -94558/15625, -1286/625.
They are negative, and P'' decreases thereafter, so P<0 for r>=R.
But I0 at EVERY closed support point. Consequently
 supp(P) subset(-101/25,101/25) subset(-17/4,17/4).
This is the companion own Gaussian1/15/radius theorem (frozen db960b92...),
not an invocation of HC contact/70. Zero mass and infinite bounded
support are allowed; required M4 for physical quadrature is now DERIVED
from bounded support, not assumed for the original all-law problem.

5. EXACT PLACEMENT IN THE DECLARED CLOSED ROOT AND CONTRADICTION
The same genuine Q3 moments give rho=rhoQ+eta with eta>=0. Since
rhoQ^2=(1+beta^2)^2/[w(1-beta^2)]>=1/w and rho<46/25,
 w>625/2116, and |beta|<321/500<13/20. Also0<w<=1.
The global owner is therefore in the actual COMPLETE_ROOT class;
eta0,w1,zero atoms and all shared faces must not be dropped. Negative
beta is represented with the physical orientation, not by changing
the owner/CDF to a naive complement. Covering the positive CLOSED
discrepancy for both P and -P covers negative CLOSED gaps as well:
 Phi(t/2)-F4_P(t)<=Phi(t/2)-F4_P(t-)
                  =F4_{-P}(-t)-Phi(-t/2).
This is why BOTH genuine orientations and ALL tails are required.

COMPLETE_ROOT(U) now gives R4(P)<=U, contradicting R4(P)=C4>max(c,U).
Thus C4<=max(c,U). If U<=T, then max(c,U)<=T; Step1 gives T<C_E
independently of any root numerical target flag. If instead a VALID
complete U is greater than T but less than C_E, max(c,U)<C_E still
excludes the fourth-index conjecture violation. Such U must come from
the whole mathematically valid acceptance bounds, not from assuming
that UNKNOWN/partial H/eta records are automatically valid certificates.
No equality C4=T exclusion or all-index conclusion has been proved.

PROOF/TRUST BOUNDARY
The own contact/Gaussian proofs remove HC Lemma4.3 and(70) as n4
assumptions. They do not remove(A), published(SV), or(PW) when used
inside the physical root acceptance chain. The old bridge note has
historical C4>=CE/HC headers, but its actual quadrature formulas require
only the REAL support17/4 and rho cap supplied above. No live dependency
needs editing while its producer runs. The COMPLETE_ROOT premise must
be the authentic full continuous original-P theorem, not a Q3/binary
reference theorem, fixed geometry theorem, finite-atom reduction, partial
cover or Boolean gate. C3's separate original certificate remains an
accepted theorem input; it is not re-executed by the scalar checks here.
Until that full n4 certificate finishes and is independently replayed,
this module is a CONDITIONAL reduction only, not a completed C4 result.
"""

from __future__ import annotations

from fractions import Fraction as F

C0, TARGET, RHO_CAP = F(256, 625), F(4097, 10000), F(46, 25)
SV_C, SV_OFFSET = F(3031, 10000), F(323, 500)
ROOT = F(625, 2116), F(1), F(0), F(13, 20)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def atan_alternating(q, m):
    """Exact finite scalar only: even m upper, odd m lower for0<q<1."""
    require(type(q) is F and 0 < q < 1 and type(m) is int and m >= 0,
            "Exact rational alternating atan data")
    return sum((F((-1) ** k, 2 * k + 1) * q ** (2 * k + 1) for k in range(m + 1)), F(0))


def compact_exact_target_certificate():
    """Finite Machin/root inequalities, no CF/Phi/root numerical producer."""
    pi_upper = 16 * atan_alternating(F(1, 5), 4) - 4 * atan_alternating(F(1, 239), 1)
    pi_cap, phi_lower, sqrt10_lower = F(3927, 1250), F(19947, 50000), F(15811, 5000)
    phi_square_margin = 1 - 2 * pi_cap * phi_lower ** 2
    sqrt_margin = 10 - sqrt10_lower ** 2
    ce_lower = (3 + sqrt10_lower) * phi_lower / 6
    require(pi_upper < pi_cap and phi_square_margin == F(14209057, 1562500000000) > 0,
            "Strict elementary pi/phi0 lower certificate")
    require(sqrt_margin == F(12279, 25000000) > 0, "Strict elementary sqrt10 lower")
    require(ce_lower == F(204862339, 500000000) and ce_lower - TARGET == F(12339, 500000000) > 0,
            "Exact target below Esseen constant, independent of any root status")
    return {"target": TARGET, "finite_Machin_pi_upper": pi_upper, "rational_pi_upper_cap": pi_cap,
        "strict_phi0_lower": phi_lower, "phi_lower_square_margin": phi_square_margin,
        "strict_sqrt10_lower": sqrt10_lower, "sqrt10_lower_square_margin": sqrt_margin,
        "strict_CE_lower": ce_lower, "strict_CE_lower_minus_target": ce_lower - TARGET,
        "CF_Phi_or_ROOT_producer_used": False}


def conditional_all_law_ceiling_from_uniform_root_bound(U):
    """Arithmetic ONLY under ACTUALLY proved COMPLETE_ROOT(U), NOT acceptance.

    This function cannot establish the analytic premise from a Fraction,
    record, flag or source hash. It only evaluates the theorem's formula.
    """
    require(type(U) is F and U >= 0, "Exact nonnegative scalar U, no CDF truth inferred")
    return max(C0, U)


def scalar_regressions():
    """Dormant exact constants ONLY; never imports/accepts COMPLETE_ROOT."""
    certificate = compact_exact_target_certificate()
    checks = 4
    require(C0 ** 2 - F(59 * 59 * 3, 250 * 250) == F(1069, 1562500) > 0
            and TARGET - C0 == F(1, 10000) > 0, "Accepted ALL-LAW K3<c<T")
    checks += 1
    moment_cap = SV_C * SV_OFFSET / (C0 - SV_C)
    require(moment_cap == F(979013, 532500) < RHO_CAP, "Attainment/SV cap above c, not only CE")
    checks += 1
    require(1 / RHO_CAP ** 2 == ROOT[0], "Exact low-rho whole-root w boundary")
    checks += 1
    beta = F(321, 500)
    require((1 + beta ** 2) ** 2 / (1 - beta ** 2) == F(124637947681, 36739750000) > RHO_CAP ** 2
            and beta < ROOT[3], "Actual beta bound strictly inside declaredroot")
    checks += 1
    require(F(9, 8) ** 2 < F(4, 3) < F(37, 32) ** 2, "Positive scale charge less than1/8")
    checks += 1
    # Exact coefficient/sign checks; scalar tests do not prove contact.
    coefficients = F(7541, 46875), F(77257, 78125), F(17664, 15625), -F(643, 1875)
    r = F(101, 25)
    d, e, f, g = coefficients
    values = d + e * r + f * r ** 2 + g * r ** 3, e + 2 * f * r + 3 * g * r ** 2, 2 * f + 6 * g * r, 6 * g
    require(values == (-F(51557, 9765625), -F(520966, 78125), -F(94558, 15625), -F(1286, 625))
            and all(value < 0 for value in values), "Whole-ray owner support polynomial signs")
    checks += 1
    require(F(4) < r < F(17, 4), "Own stronger radius supplies frozenphysicalroot support")
    checks += 1
    require(conditional_all_law_ceiling_from_uniform_root_bound(F(2, 5)) == C0
            and conditional_all_law_ceiling_from_uniform_root_bound(TARGET) == TARGET
            and conditional_all_law_ceiling_from_uniform_root_bound(TARGET + F(1, 100000)) == TARGET + F(1, 100000),
            "GENERALmax(c,U), not automatic acceptance of anUNKNOWN target record")
    checks += 1
    return {"status": "EXACT_SCALARS_FOR_CONDITIONAL_COMPLETE_ROOT_ALL_LAW_REDUCTION",
        "exact_comparisons": checks, "compact_exact_target_certificate": certificate,
        "conditional_analytic_conclusion": "C4<=max(256/625,U) IF ACTUAL COMPLETEphysicalROOT(U) is established under accepted all-lawC3,SV and the applicable Prawitz bridge; U<=4097/10000 yields C4<=4097/10000<CE.",
        "COMPLETE_ROOT_is_an_actual_remaining_math_requirement_not_a_Boolean_input": True,
        "root_CDF_owner_contact_or_certificate_producer_called": False,
        "COMPLETE_ROOT_or_unrestricted_C4_proved_by_scalar_tests": False,
        "HC_contact_or_Gaussian70_imported_as_analytic_input": False,
        "active_dependencies_old_sources_or_receipts_modified": False}


if __name__ == "__main__":
    import json
    print(json.dumps(scalar_regressions(), sort_keys=True, default=str))
