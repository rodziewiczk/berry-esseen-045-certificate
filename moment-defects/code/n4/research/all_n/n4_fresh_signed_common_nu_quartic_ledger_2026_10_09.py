"""Pure fresh-input signed common-nu quartic ledger; NOT a CDF gate.

No CF/kernel/response producer, JSON, old receipt, resource monitor or
status/hash-based proof is imported. ALL response, normalized centre,
modulus, radius, price-supremum and physical inputs are freshly established
MATHEMATICAL premises from the caller. This helper does not validate their
truth by inspecting fields. It supplies exact scalar algebra only.

Canonical measure and budgets (including atoms at zero)
------------------------------------------------------
For a standardized mean-zero law with finite third absolute moment, let
u=EX+=EX->0, v_s=E X_s^2, c_s=v_s/u (c_+=b,c_-=a). Set
W_s(y)=y*(y-c_s)^2 and eta=E W=rhoP-rhoQ. When eta>0, nu=W*dP/eta
is a probability on tagged y>0,y!=c_s. On this SAME measure,

 eta E k0 <= p0=1-u/a-u/b,       k0=1/(c_s^2*y),
 eta E_tag k2 <= u,             k2=1/(y-c_s)^2,
 E_tag k1=0,                   k1=1/(y-c_s).

Indeed eta E_tag k2=E_tag[y;off contacts]<=u and
eta E_tag k1=E_tag y*(y-c_s)=v_s-c_s*u=0. Cauchy gives absolute k1
integrability from k2. For k0, sum the off-zero identity
(y-c)^2/c^2=y^2/c^2-2y/c+1, obtaining
eta E k0=P(X!=0)-(u/a+u/b)=p0-P(X=0)<=p0. Actual zero atoms therefore
use budget, not a discarded sign class. Contact atoms contribute zero.
If eta=0, W=0 almost surely; sign means/second moments fix exactly Q3's
masses, so P=Q3 and every delta is0. No artificial nu is introduced there.

For each physical midpoint frequency, delta_q=phiP(q)-g_Q(q)=eta E r_q,
r_q=f_q[0,c,c,y], with the signed tag exponential. The corrected generic
A1 table MUST use the TRUE actual-reference CF or a proved whole-box
enclosure, the SAME q/kernel/H labels as its finite centre, and already
include HG tail/mesh/geometry margins ONCE. For an orientation+ row,
plus/minus contacts are b/a; a reflected orientation- row uses a/b with
its genuinely conjugated CF/response. No silent rational-bar CF baseline,
unswapped tag costs or second geometry margin is allowed.

For ONE fixed H and orientation define the signed COMMON curve
 A1_H(tag,y)=Re sum_q 4*kappa_H(q)*g_Q(q)^3*r_q(tag,y).
The coefficient4 is already in A1. Fixed prices lambda0,lambda+,lambda-
>=0 and theta+,theta- ANY real, and a proved WHOLE-domain signed upper
 S >= sup[A1-lambda0*k0-lambda_tag*k2-theta_tag*k1]
give eta E A1 <= Gamma(eta)=A+eta*S, where
 A=p0_hi*lambda0+u_hi*(lambda+ +lambda-).
The inequality prices are nonnegative; the equality prices remain signed.
S and Gamma can be NEGATIVE: neither clipping nor modulus/infeasibility
interpretation is valid. Each fixed model covers the WHOLE closed eta
cell/reference box, regardless of how its prices were found. Zero prices
give Gamma=eta*sup A1, including exact0 at eta0. A positive intercept
is valid but needlessly loose at eta0. At a singleton eta0 use exact0.

Fourth power and whole-cell remainder
------------------------------------
With psi=g+delta,
 psi^4-g^4=4*g^3*delta+delta^2*(psi^2+2*psi*g+3*g^2).
For proven ACTUAL-reference |g|<=a<=1, |psi|<=1 and a WHOLE-cell
nonnegative affine radius e=Aq+Bq*eta, freeze
p_hi=min(1,a+max(e(L),e(U))). Then the primary remainder is bounded by
 e^2*(p_hi^2+2*p_hi*a+3*a^2), a quadratic with leading coefficient>=0.
An independent disk cap follows from integral Taylor:
R2=12 delta^2 integral_0^1(1-t)(g+t*delta)^2 dt. The exact chord identity
|g+t delta|^2=(1-t)|g|^2+t|psi|^2-t(1-t)|delta|^2 yields
|R2|<=s*(4a^2+2-s), s=|delta|^2. Its maximum on[0,e_hi^2] is
U*(4a^2+2-U), U=min(e_hi^2,2a^2+1), a WHOLE-cell CONSTANT.
Choose either complete primary quadratic or complete disk constant;
NEVER minimize coefficients independently. Nonnegative weighted sums
retain their nonnegative quadratic coefficient, including signed Bq.

PER-H normalized target and factors
----------------------------------
A proved PER-H M_H >= C_H(Q_actual)-T*rhoQ_actual combines with the
SAME-H Gamma_H. Only AFTER deriving each full row polynomial may a later
consumer take the worst H/orientation score. Separately maximizing M_H
and Gamma_H loses crucial correlation and is not done here. The raw
physical transfer is 2*Gamma_H+2*sum|kappa|R2: A1 already contains4, so
the linear raw coefficient is8*kappa*g^3*delta, not16 or32.
Add ONE raw quadrature reserve and ONE WHOLE-cell physical H reserve;
then subtract T*eta ONCE. The resulting PER-ROW polynomial is
 P_H(eta)=M_H+reserves+2*Gamma_H+2*weighted_R2-T*eta.
Its leading coefficient is nonnegative, so strict endpoint negativity
equals strict degree2 Bernstein negativity on the ENTIRE closed cell.
For quantitative normalized scores, use BOTH denominator faces:
T+max(P(L)/cap,P(U)/cap,P(L)/(rhoQ_LO+L),P(U)/(rhoQ_LO+U)), clipped below0.
For P/(rhoQ_LO+eta), the derivative numerator N=P'*(rhoQ_LO+eta)-P
has N'=P''*(rhoQ_LO+eta)>=0: critical points can only be minima. The
cap branch is convex. Endpoint maxima therefore remain sound for signed
Gamma and either numerator sign. A lower denominator alone is unsafe
when P<0. The physical rho upper cap is a caller's standing premise.

A single Gamma_H bound does NOT bound |delta_q| and must not be turned
into a radius by taking abs(Gamma). Genuine directional sharpening uses
separately proved signed projections of the SAME delta_q at0,pi/2,pi,
3pi/2, via the SAME nu budgets. Their WHOLE-cell affine uppers give a
coordinate rectangle and hence a constant upper on |delta_q|^2. The
optional helper below makes this limited implication explicit; it does
not invent directional responses from an H-summed Gamma. Negative
directional uppers are retained; inconsistent opposite faces are not
silently clipped into a fake radius. Such rectangles can sharpen R2's
disk constant, but are not an extra moment-class/PSD axiom.

All-H/reflection labels, closed eta cover/joins, actual-law tails, target
below CE, physical Prawitz/midpoint support/rho inputs and first-critical
owner placement remain the later CDF consumer's duties. This source
alone proves no CDF/medium-eta/global C4 claim. Dormant exact tests only;
no execution on import and no producer/replay/file-write CLI.
"""

from __future__ import annotations

from fractions import Fraction as F

SCALE, DEFAULT_TARGET, DEFAULT_CAP = 10 ** 40, F(4097, 10000), F(46, 25)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    require(type(value) in (F, int), "Exact Fraction/int proof inputs only")
    return F(value)


def closed_interval(lower, upper):
    lower, upper = map(exact, (lower, upper))
    require(0 <= lower <= upper, "Whole nonnegative CLOSED eta cell")
    return lower, upper


def evaluate(polynomial, x):
    x = exact(x)
    result = F(0)
    for coefficient in reversed(tuple(map(exact, polynomial))):
        result = result * x + coefficient
    return result


def gamma_affine_from_proven_sup(p0_upper, u_upper, prices, signed_sup_upper):
    """Budget intercept only; caller proves response/cost WHOLE-domain sup."""
    p0, u, S = map(exact, (p0_upper, u_upper, signed_sup_upper))
    require(0 <= p0 <= 1 and u >= 0 and len(prices) == 5, "Valid proved budgets/five prices")
    lam0, lp, lm, tp, tm = map(exact, prices)
    require(min(lam0, lp, lm) >= 0, "Inequality prices nonnegative; equality prices signed")
    return p0 * lam0 + u * (lp + lm), S


def frozen_remainder(a, radius_model, lower, upper, method="auto"):
    """WHOLE primary quadratic or WHOLE disk constant, not coefficient minima."""
    a, A, B = map(exact, (a, *radius_model))
    lower, upper = closed_interval(lower, upper)
    require(0 <= a <= 1 and min(A + B * lower, A + B * upper) >= 0,
            "Proven ACTUAL-Q modulus and WHOLE-cell nonnegative radius")
    require(method in ("auto", "primary", "disk"), "Complete remainder choice")
    e_hi = max(A + B * lower, A + B * upper)
    p = min(F(1), a + e_hi)
    factor = p * p + 2 * p * a + 3 * a * a
    primary = (factor * A * A, 2 * factor * A * B, factor * B * B)
    U = min(e_hi * e_hi, 2 * a * a + 1)
    disk = (U * (4 * a * a + 2 - U), F(0), F(0))
    use_disk = method == "disk" or (method == "auto" and disk[0] < evaluate(primary, (lower + upper) / 2))
    selected = disk if use_disk else primary
    require(selected[2] >= 0, "Selected whole function has nonnegative leading coefficient")
    return selected, "disk_constant" if use_disk else "primary_quadratic"


def weighted_remainder_sum(frequencies, lower, upper):
    """Exact nonnegative-weight sum; each radius is frozen WHOLE cell."""
    lower, upper = closed_interval(lower, upper)
    require(1 <= len(frequencies) <= 512, "Finite declared physical frequency list")
    coefficients, choices = [F(0), F(0), F(0)], []
    for item in frequencies:
        weight = exact(item["weight"])
        require(weight >= 0, "Proven nonnegative kernel modulus upper")
        polynomial, choice = frozen_remainder(item["actual_modulus"], item["radius_model"],
            lower, upper, item.get("method", "auto"))
        for degree in range(3):
            coefficients[degree] += weight * polynomial[degree]
        choices.append(choice)
    require(coefficients[2] >= 0, "Sum remains convex, signed middle coefficient retained")
    return tuple(coefficients), tuple(choices)


def degree2_bernstein(polynomial, lower, upper):
    lower, upper = closed_interval(lower, upper)
    require(1 <= len(polynomial) <= 3, "Degree at most two")
    coefficients = tuple(map(exact, polynomial)) + (F(0),) * (3 - len(polynomial))
    c0, c1, c2 = coefficients
    require(c2 >= 0, "Convex row polynomial required for endpoint equivalence")
    left, right = evaluate(coefficients, lower), evaluate(coefficients, upper)
    middle = (left + right) / 2 - c2 * (upper - lower) ** 2 / 2
    return left, middle, right


def per_H_signed_normalized_row(normalized_center_upper, gamma_model, weighted_R2,
                                quad_reserve, H_reserve, rhoQ_lower, lower, upper,
                                target=DEFAULT_TARGET, rho_cap=DEFAULT_CAP):
    """ONE fixed H/reflection; combine its M_H and Gamma_H BEFORE max-H."""
    M, A, S, quad, H, rho, target, cap = map(exact, (
        normalized_center_upper, *gamma_model, quad_reserve, H_reserve,
        rhoQ_lower, target, rho_cap))
    lower, upper = closed_interval(lower, upper)
    require(quad >= 0 and H >= 0 and rho >= 1 and target > 0 and cap > 0,
            "ONE proved reserve each and physical denominator bounds")
    require(len(weighted_R2) == 3, "Proven complete weighted R2 quadratic")
    r0, r1, r2 = map(exact, weighted_R2)
    require(r2 >= 0, "Convex complete weighted remainder")
    candidates = [evaluate((r0, r1, r2), point) for point in (lower, upper)]
    if r2 > 0 and lower < -r1 / (2 * r2) < upper:
        candidates.append(evaluate((r0, r1, r2), -r1 / (2 * r2)))
    require(min(candidates) >= 0, "Complete remainder nonnegative on WHOLE cell")
    # This exact positivity check does NOT establish the independent
    # mathematical premise that R2 bounds the actual complex remainder.
    polynomial = (M + quad + H + 2 * A + 2 * r0,
                  2 * S + 2 * r1 - target, 2 * r2)
    bernstein = degree2_bernstein(polynomial, lower, upper)
    passed = all(value < 0 for value in bernstein)
    left, right = bernstein[0], bernstein[2]
    faces = (left / cap, right / cap, left / (rho + lower), right / (rho + upper))
    score = max(F(0), target + max(faces))
    require(passed == (left < 0 and right < 0) and passed == (score < target),
            "Convex row WHOLE-cell endpoints/Bernstein/sign-safe score agree")
    return {"normalized_target_polynomial": polynomial,
        "normalized_target_endpoint_uppers": (left, right),
        "degree2_Bernstein_coefficients": bernstein,
        "normalized_score_denominator_face_ratios": faces,
        "normalized_score_upper": score, "whole_cell_strict_numeric_inequality": passed,
        "signed_Gamma_model_retained": (A, S), "ONE_reserves": (quad, H),
        "CDF_or_all_H_proved_here": False}


def directional_axis_radius_square_upper(models, lower, upper):
    """From FOUR proved SAME-q projection uppers, NOT from an A1_H bound.

    Order: Re(delta), Im(delta), -Re(delta), -Im(delta). Each supplied
    affine model is a signed projection bound on the WHOLE box/eta cell.
    """
    lower, upper = closed_interval(lower, upper)
    require(len(models) == 4, "Four genuine signed coordinate projections")
    uppers = []
    for model in models:
        require(len(model) == 2, "Affine signed directional model")
        A, B = map(exact, model)
        uppers.append(max(A + B * lower, A + B * upper))
    real, imaginary = (-uppers[2], uppers[0]), (-uppers[3], uppers[1])
    require(real[0] <= real[1] and imaginary[0] <= imaginary[1],
            "Opposite directional faces consistent; no fake clipping of an empty rectangle")
    return {"real_interval": real, "imaginary_interval": imaginary,
        "whole_cell_delta_squared_norm_upper": max(map(abs, real)) ** 2
            + max(map(abs, imaginary)) ** 2,
        "H_summed_Gamma_was_NOT_used_as_radius": True}


def self_tests():
    """Dormant exact scalar/finite-measure algebra ONLY, no CF/CDF producer."""
    checks = 0
    # A standardized finite law at +/-1/2,+/-3/2, masses5/16,3/16.
    c, eta, u, p0 = F(8, 7), F(45, 224), F(7, 16), F(15, 64)
    nu = [(tag, F(1, 2), F(9, 28)) for tag in (1, -1)] + [
          (tag, F(3, 2), F(5, 28)) for tag in (1, -1)]
    require(sum(weight for _, _, weight in nu) == 1, "Exact SAME nu probability")
    require(eta * sum(weight / (c * c * y) for _, y, weight in nu) == p0,
            "Exact zero-mass budget, original P has no zero atom")
    checks += 2
    for tag in (1, -1):
        atoms = [(y, weight) for sign, y, weight in nu if sign == tag]
        require(sum(weight / (y - c) for y, weight in atoms) == 0
                and eta * sum(weight / (y - c) ** 2 for y, weight in atoms) == u,
                "Exact signed balance and first-moment budget per tag")
        checks += 1
    for prices in ((F(0),) * 5, (F(1, 100), F(1, 50), F(3, 100), F(-1, 25), F(1, 40))):
        lam0, lp, lm, tp, tm = prices
        S = max(-y ** 3 - lam0 / (c * c * y)
                - (lp if tag == 1 else lm) / (y - c) ** 2
                - (tp if tag == 1 else tm) / (y - c) for tag, y, _ in nu)
        A, S = gamma_affine_from_proven_sup(p0, u, prices, S)
        require(eta * sum(-weight * y ** 3 for _, y, weight in nu) <= A + eta * S,
                "Finite-support synthetic response dual, balances retain signed equality prices")
        checks += 1
    require(gamma_affine_from_proven_sup(p0, u, (F(0),) * 5, F(-1, 8))
            == (F(0), F(-1, 8)), "Negative signed Gamma not a modulus/infeasibility test")
    checks += 1
    for a, model in ((F(1, 3), (F(0), F(1))), (F(3, 5), (F(1), F(-1, 2)))):
        for method in ("primary", "disk", "auto"):
            polynomial, choice = frozen_remainder(a, model, F(0), F(1), method)
            for j in range(9):
                x = F(j, 8)
                e = model[0] + model[1] * x
                p = min(F(1), a + e)
                if choice == "primary_quadratic":
                    require(evaluate(polynomial, x) >= e * e * (p * p + 2 * p * a + 3 * a * a),
                            "Whole frozen primary quadratic")
                else:
                    s = e * e
                    require(evaluate(polynomial, x) >= s * (4 * a * a + 2 - s),
                            "Whole disk constant covers concave Taylor scalar")
                checks += 1
    def multiply(z, w):
        return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]
    def power(z, n):
        result = (F(1), F(0))
        for _ in range(n):
            result = multiply(result, z)
        return result
    for g in ((F(1, 3), F(0)), (F(3, 10), F(2, 5)), (F(0), F(0))):
        a = abs(g[0]) + abs(g[1])
        for psi in ((F(1), F(0)), (F(-1), F(0)), (F(3, 5), F(4, 5)), (F(1, 3), F(1, 3))):
            delta = (psi[0] - g[0], psi[1] - g[1])
            first = multiply(power(g, 3), delta)
            psi4, g4 = power(psi, 4), power(g, 4)
            remainder = (psi4[0] - g4[0] - 4 * first[0], psi4[1] - g4[1] - 4 * first[1])
            psi2, g2, pg = power(psi, 2), power(g, 2), multiply(psi, g)
            factor = (psi2[0] + 2 * pg[0] + 3 * g2[0], psi2[1] + 2 * pg[1] + 3 * g2[1])
            require(remainder == multiply(power(delta, 2), factor), "Exact complex quartic factorization")
            checks += 1
            e = abs(delta[0]) + abs(delta[1])
            for method in ("primary", "disk", "auto"):
                bound, _ = frozen_remainder(a, (e, F(0)), F(0), F(1), method)
                require(remainder[0] ** 2 + remainder[1] ** 2 <= evaluate(bound, F(1, 2)) ** 2,
                        "Exact rational complex remainder vs each complete norm upper")
                checks += 1
    R, _ = weighted_remainder_sum([
        {"actual_modulus": F(3, 5), "weight": F(2, 7), "radius_model": (F(1, 4), F(-1, 8))},
        {"actual_modulus": F(1, 10), "weight": F(1, 11), "radius_model": (F(0), F(3))}], F(0), F(1))
    row = per_H_signed_normalized_row(F(-1, 4), (F(1, 100), F(-1, 3)), R,
                                      F(1, 1000), F(1, 2000), F(1), F(0), F(1))
    for j in range(17):
        x = F(j, 16)
        P = evaluate(row["normalized_target_polynomial"], x)
        for denominator in (1 + x, DEFAULT_CAP):
            # For x beyond the physical lower<=cap capacity there is no
            # actual law, but each branch endpoint bound remains valid.
            require(DEFAULT_TARGET + P / denominator <= row["normalized_score_upper"],
                    "Convex and linear-fractional endpoint maxima with signed numerator")
            checks += 1
    rectangle = directional_axis_radius_square_upper(
        ((F(-1, 5), F(0)), (F(1, 10), F(0)), (F(3, 10), F(0)), (F(1, 10), F(0))), F(0), F(1))
    require(rectangle["real_interval"] == (F(-3, 10), F(-1, 5))
            and rectangle["whole_cell_delta_squared_norm_upper"] == F(1, 10),
            "Signed directional rectangle preserves negative projection upper")
    checks += 1
    return {"exact_checks": checks, "CF_response_CDF_or_global_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
