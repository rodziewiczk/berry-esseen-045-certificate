"""Self-contained finite4 contamination/contact derivation for CLOSED CDFs.

This NEW standalone analytic source imports NO He--Cheng theorem, CF,
Gaussian certificate, root controller or numerical receipt. It derives
the CONTACT inequality used in the separate frozen5709 Gaussian/radius
note from the definition of C4 and elementary calculus. It leaves all
active sources/dependencies untouched. No attainment, C3 bound, root
closure or unrestrictedC4 result is newly asserted. Scalar checks below
are dormant until authorized and prove only exact algebraic identities.

DEFINITIONS AND PRECISE OWNER PREMISE
For every standardized real law P with EX0,EX^2=1 and finite
rho=E|X|^3, let F4_P(t)=P(X1+...+X4<=t). Let C4 be the supremum,
over ALL such laws and real t, of the normalized Kolmogorov ratio
 2*|F4_P(t)-Phi(t/2)|/rho.
Assume that some unrestricted maximizing pair (P,t) is attained in the
POSITIVE CLOSED orientation: for C=C4>0 and z=t/2,
 Delta=F4_P(t)-Phi(z)=C*rho/2>0.                       (OWNER)
This is an explicit premise, not a conclusion from source/status/flags.
The separately proved attainment/reflection reduction must supply it.
Set beta=E[X|X|]. FiniteM3 implies finite beta and all moments below.

NORMALIZE AN ACTUAL ONE-POINT CONTAMINATION
For ANY real y and0<=eps<1, put P_eps=(1-eps)P+eps*delta_y.
Use a raw Z_eps with this law and keep the raw four-sum threshold t
EXACTLY fixed; no derivative of an atomic CDF in its threshold is used.
Its mean and variance are exactly
 m_eps=eps*y,
 v_eps=1+eps*(y^2-1)-eps^2*y^2.
Since v0=1, variance stays positive for sufficiently small eps>=0.
Define the RAW CENTRAL third absolute moment
 rho_eps=E_{P_eps}|Z_eps-m_eps|^3,
and standardize Y_eps=(Z_eps-m_eps)/sqrt(v_eps). The four-sum event
is the original CLOSED event with threshold
 (t-4m_eps)/sqrt(v_eps), and its normal argument is
 z_eps=(t-4m_eps)/(2sqrt(v_eps)).
The standardized third absolute moment is rho_eps/v_eps^(3/2).
Therefore the normalized SIGNED ratio is exactly
 R_eps=2*v_eps^(3/2)/rho_eps
             *[F4_{P_eps}(t)-Phi(z_eps)] <= C.          (MAX)
Even if its discrepancy later changes sign, the signed ratio is bounded
by the absolute supremum defining C4. At0 it equals C. Thus its right
derivative exists and I(y):=R'_0(y)<=0 for EVERY real y.

ALL FINITE DERIVATIVES, INCLUDING ATOMS AND ZERO
Let G(s)=P(X1+X2+X3<=s) be the CLOSED predecessor CDF. Product expansion
of the actual mixture gives the exact degree4 polynomial in eps
 F4_{P_eps}(t)=sum_{k=0}^4 binom(4,k)(1-eps)^(4-k)eps^k
                       *F_{4-k,P}(t-k*y),
where F0_P(s)=1_{0<=s}. Hence F'_0=4[G(t-y)-F4_P(t)].
This polynomial identity is valid for arbitrary measures and all atoms;
the coordinates t-k*y are fixed for a fixed y. No density is assumed.

For the central third moment,
 rho_eps=(1-eps)*int|x-eps*y|^3 dP(x)+eps*|y-eps*y|^3.
For fixed y and0<=eps<=1, the difference quotients of the integral
are dominated by3|y|*(|x|+|y|)^2, integrable under finiteM2. The
values themselves are integrable under finiteM3. The derivative of
|x-eps*y|^3 at0 is-3y*x|x|, also at x0. Dominated convergence gives
 rho'_0=|y|^3-rho-3beta*y.
Furthermore m'_0=y, v'_0=y^2-1, and
 z'_0=-2y-(z/2)*(y^2-1).
The ordinary Gaussian derivative Phi'=phi then yields, from(MAX),
 rho*I(y)=8[G(t-y)-F4_P(t)]+4y*phi(z)+z*phi(z)*(y^2-1)
          +(3/2)*C*rho*(y^2-1)-C*(|y|^3-rho-3beta*y). (I)
The derivative of v_eps^(3/2) contributes(3/2)v'_0; omitting this
variance normalization would give the WRONG quadratic/constant terms.
The formula includes y0 and negative y. There is no M4 premise.

WHY CONTACT HOLDS ON THE WHOLE CLOSED SUPPORT
All terms in(I) are P-integrable: the CDF is bounded and the remaining
growth is at most cubic. Tonelli gives int G(t-y)dP(y)=F4_P(t).
Also EX0,EX^2=1,E|X|^3=rho. Integrating(I) therefore gives
 int I(y)dP(y)=0.
Together with I<=0 this implies I0 P-almost surely. This by itself
would NOT suffice for an accumulation point; the following topology
is essential. A CLOSED CDF G is uppersemicontinuous: if s_j->s,
then limsup G(s_j)<=G(s+h) for every h>0, and continuity from above
of (-infinity,s+h] as h decreases0 gives G(s+h)->G(s).
Consequently y->G(t-y) is uppersemicontinuous. The rest of(I) is
continuous, so I is uppersemicontinuous. Since I<=0 everywhere,
 {I=0}={I>=0} is CLOSED. It has full P-measure and therefore contains
the WHOLE CLOSED support of P. Equivalently, an excluded support
point would have an open neighborhood of positive P-mass outside
that closed full-measure set. Thus
                 I(y)=0 for EVERY y in supp(P).        (CONTACT0)
Zero atoms, other atoms, support ends and accumulation points all obey
the same statement; no original finite-support assumption has appeared.

PREDECESSOR SPLIT AND EXACT CONTACT INEQUALITY
Suppose C3 is an all-law upper constant for standardized iid triples:
 G(s)-Phi(s/sqrt(3)) <= C3*rho/sqrt(3), all real s.
The original law P is standardized, so this applies DIRECTLY to G.
Using(OWNER) and t2z, split the CDF part of(I) as
 8[G(t-y)-F4_P(t)]
 =8[G(t-y)-Phi((t-y)/sqrt(3))]
  +8[Phi((t-y)/sqrt(3))-Phi(z)]-4*C*rho.
Define exactly
 H4(z,y)=8[Phi((z-y/2)/sqrt(3/4))-Phi(z)]
                     +4yphi(z)+zphi(z)*(y^2-1),
and s=sqrt(4/3). Since8/sqrt(3)=4s, (I) yields
 rho*I(y) <= H4(z,y)+4rho*(C3-C)+4rho*(s-1)*C3
                  +C[-|y|^3+(3/2)rho*y^2+3beta*y-rho/2]. (CONTACT)
This is precisely the display used by the separate5709 finite Gaussian
and radius81/20 proof, now derived without importing a contact theorem.
No Gaussian(70) estimate is required here; a separate elementary finite
Gaussian bound can be inserted AFTER this exact derivation.

REFLECTION/ORIENTATION BOUNDARY AND WHAT REMAINS EXTERNAL
The proof assumes an attained POSITIVE CLOSED owner(OWNER). It does
not silently convert a negative closed discrepancy by1-F(t): if atoms
are present, F_{-S}(-t)=1-F_S(t-), not1-F_S(t). The all-law
orientation/attainment reduction must justify its chosen positive
closed maximizing pair separately, using left limits when reflecting.
Once(OWNER) holds, arbitrary signs of z/y/beta are already included.
No extra sign/probability/finite-atom assumption is hidden in(MAX).

This module proves the conditional contact identity and full-support
equality for an actually attained unrestricted C4 owner; it does NOT
prove that an owner exists, that C3<C4, the SV envelope, any support
radius, or completion of the live entire-root certificate. Those are
separate analytic/numerical stages. The scalar identities cannot replace
any measure-level premise with a trusted Boolean/JSON/source hash.
All active root dependencies and every older file remain unchanged.
"""

from __future__ import annotations

from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def finite_first_variation(y, rho, beta, C, delta_G, phi_z, z_phi_z):
    """Exact algebraic rho*I; supplied scalars are NOT an owner/CDF certificate."""
    require(all(type(value) is F for value in (y, rho, beta, C, delta_G, phi_z, z_phi_z))
            and rho > 0 and C > 0, "Exact scalar finite4 variation data")
    v_prime = y ** 2 - 1
    central_rho_prime = abs(y) ** 3 - rho - 3 * beta * y
    return 8 * delta_G + 4 * y * phi_z + z_phi_z * v_prime + F(3, 2) * C * rho * v_prime - C * central_rho_prime


def contact_majorant(y, rho, beta, C, C3, formal_s, H4):
    """Algebraic predecessor split; rational formal_s is ONLY a test symbol."""
    require(all(type(value) is F for value in (y, rho, beta, C, C3, formal_s, H4))
            and rho > 0 and C > 0, "Exact algebraic contact scalars")
    return H4 + 4 * rho * (C3 - C) + 4 * rho * (formal_s - 1) * C3 + C * (
        -abs(y) ** 3 + F(3, 2) * rho * y ** 2 + 3 * beta * y - rho / 2)


def scalar_identity_tests():
    """Dormant scalar algebra ONLY; no Phi/CDF/owner/contact/root producer."""
    checks = 0
    rho, beta, C, C3 = F(9, 5), F(2, 7), F(21, 50), F(2, 5)
    phi_z, z_phi_z, delta_G = F(3, 10), F(-2, 9), F(4, 13)
    for y in (F(-7, 3), F(-1), F(0), F(1, 5), F(5, 2)):
        # Direct differentiation of2*v^(3/2)/rho*Delta at v1 and
        # Delta=C*rho/2, using Gaussian darg EXACTLY, has this form.
        z_prime_phi = -2 * y * phi_z - z_phi_z * (y ** 2 - 1) / 2
        central_rho_prime = abs(y) ** 3 - rho - 3 * beta * y
        differentiated = 2 * (4 * delta_G - z_prime_phi) + C * (
            F(3, 2) * rho * (y ** 2 - 1) - central_rho_prime)
        require(finite_first_variation(y, rho, beta, C, delta_G, phi_z, z_phi_z)
                == differentiated, "All factors2/4/8 and variance normalization")
        checks += 1
        for formal_s in (F(1), F(7, 6), F(5, 4)):
            H4 = F(-5, 11)
            expanded = H4 + 4 * rho * formal_s * C3 - 4 * C * rho + F(3, 2) * C * rho * (
                y ** 2 - 1) - C * (abs(y) ** 3 - rho - 3 * beta * y)
            require(contact_majorant(y, rho, beta, C, C3, formal_s, H4) == expanded,
                    "Exact predecessor split, not a rational approximation tosqrt4/3")
            checks += 1
    # Formal integration of the displayed first variation with EX0,
    # EX^2=1,E|X|^3=rho and E[G-F4]=0 gives zero independently of beta.
    integrated = 8 * F(0) + 4 * phi_z * F(0) + z_phi_z * (F(1) - 1) + F(3, 2) * C * rho * (
        F(1) - 1) - C * (rho - rho - 3 * beta * F(0))
    require(integrated == 0, "Exact integralI0 under SAME one-law moments")
    checks += 1
    require(8 * F(1, 2) == 4 and F(3, 2) - 1 == F(1, 2),
            "OwnerDelta=C*rho/2 and constant-rho contact coefficient")
    checks += 1
    return {"status": "EXACT_SCALAR_IDENTITIES_FOR_SELF_CONTAINED_FINITE4_CONTACT",
        "exact_checks": checks, "Phi_or_CDF_contact_owner_or_root_producer_called": False,
        "rational_formal_s_is_a_sqrt4_3_proof_premise": False,
        "CONTACT0_requires_actual_attained_POSITIVE_CLOSED_unrestricted_owner": True,
        "C3_SV_attainment_support_radius_or_entire_root_proved_here": False,
        "unrestricted_C4_proved": False, "active_dependencies_or_old_files_modified": False}


if __name__ == "__main__":
    import json
    print(json.dumps(scalar_identity_tests(), sort_keys=True))
