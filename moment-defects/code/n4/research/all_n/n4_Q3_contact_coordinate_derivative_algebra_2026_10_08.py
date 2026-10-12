"""Tiny exact contact-coordinate derivative algebra; NOT a cover producer.

For standardized Q3 with contacts-a,b and possible zero mass:
 u=1/(a+b), w=1/(ab), beta=(b-a)/(a+b),
 pminus=1/[a(a+b)],pplus=1/[b(a+b)],pzero=1-1/(ab),
 rhoQ=(a^2+b^2)/(a+b).
The feasible magnitude domain ab>=1,b>=a,rhoQ<=r is a convex intersection
of an epigraph b>=1/a, a halfplane, and the disk
(a-r/2)^2+(b-r/2)^2<=r^2/2. Rational a,b centres remove square-root
geometry from reference weights and moment budgets. A nominal expansion
centre needs standardized probability/support ONLY, not an eta seed cap.

Let F_sigma(c)=(exp(i*sigma*q*c)-1-i*sigma*q*c+q^2*c^2/2)/c,
B=F_-(a)+F_+(b),s=a+b. Then g=1-q^2/2+B/s, preserving both fixed
moments explicitly. The functions below return outward complex rectangles
for g and its a/b first/second derivatives at a RATIONAL reference centre.
They also provide uniform exact analytic derivative majorants, with all
g derivatives O(q^3), useful for joint signed geometry gradients/Hessians.
Only reference Q3 is differentiated; original P/nu need not be a smooth
or finite-support family. No Gamma, radius, CDF or global-cover flag.

Inputs Fraction/int ONLY; no floats in proof arithmetic. CLI executes tiny
algebra/interval identity checks, no N/H/y table, optimizer or file writes.
"""

from __future__ import annotations

from fractions import Fraction as F
import json

import n4_Q3_first_critical_integer_abs_Prawitz_gate_strict_v2_2026_10_08 as arithmetic

integer, SCALE = arithmetic.arith, arithmetic.S


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    require(type(value) in (F, int), "Exact Fraction/int inputs only")
    return F(value)


def coordinates(a, b):
    a, b = map(exact, (a, b))
    require(0 < a <= b and a * b >= 1, "Standardized magnitude reference with nonnegative zero mass")
    s = a + b
    return {"a": a, "b": b, "u": 1 / s, "w": 1 / (a * b), "beta": (b - a) / s,
            "pminus": 1 / (a * s), "pplus": 1 / (b * s), "pzero": 1 - 1 / (a * b),
            "rhoQ": (a * a + b * b) / s}


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def scale(rectangle, factor):
    factor = exact(factor)
    rlo, rhi, ilo, ihi = rectangle
    if factor < 0:
        rlo, rhi, ilo, ihi = -rhi, -rlo, -ihi, -ilo
        factor = -factor
    n, d = factor.numerator, factor.denominator
    return rlo * n // d, integer.ceil_div(rhi * n, d), ilo * n // d, integer.ceil_div(ihi * n, d)


def constant(real=F(0), imaginary=F(0)):
    real, imaginary = map(exact, (real, imaginary))
    rl, rh = integer.fraction_interval(real)
    il, ih = integer.fraction_interval(imaginary)
    return rl, rh, il, ih


def multiply_i(rectangle, sign=1):
    require(type(sign) is int and sign in (1, -1), "Exact imaginary phase sign")
    result = (-rectangle[3], -rectangle[2], rectangle[0], rectangle[1])
    return result if sign == 1 else scale(result, -1)


def stable_F_derivatives(q, c, sign):
    """F,R derivatives via exact imaginary Taylor rectangles; no c=0 pole."""
    q, c = map(exact, (q, c))
    require(q >= 0 and c > 0 and type(sign) is int and sign in (1, -1), "Positive physical contact")
    exponential = arithmetic.exponential_exact_argument(sign * q * c)
    R = add(exponential, constant(-1 + q * q * c * c / 2, -sign * q * c))
    Rprime = scale(multiply_i(add(exponential, constant(-1, -sign * q * c)), sign), q)
    Rsecond = scale(add(exponential, constant(-1)), -q * q)
    F0 = scale(R, 1 / c)
    F1 = add(scale(Rprime, 1 / c), scale(R, -1 / (c * c)))
    F2 = add(add(scale(Rsecond, 1 / c), scale(Rprime, -2 / (c * c))), scale(R, 2 / (c ** 3)))
    return F0, F1, F2


def nominal_derivative_rectangles(q, a, b):
    """True g,ga,gb,gaa,gab,gbb at exact rational contact centre."""
    q, a, b = map(exact, (q, a, b))
    coordinates(a, b)
    require(0 <= q <= 3 and b <= F(17, 4), "Current proof frequency/contact domain")
    s = a + b
    Fa, Fap, Fapp = stable_F_derivatives(q, a, -1)
    Fb, Fbp, Fbpp = stable_F_derivatives(q, b, 1)
    B = add(Fa, Fb)
    g = add(constant(1 - q * q / 2), scale(B, 1 / s))
    ga = add(scale(Fap, 1 / s), scale(B, -1 / s ** 2))
    gb = add(scale(Fbp, 1 / s), scale(B, -1 / s ** 2))
    gaa = add(add(scale(Fapp, 1 / s), scale(Fap, -2 / s ** 2)), scale(B, 2 / s ** 3))
    gbb = add(add(scale(Fbpp, 1 / s), scale(Fbp, -2 / s ** 2)), scale(B, 2 / s ** 3))
    gab = add(scale(add(Fap, Fbp), -1 / s ** 2), scale(B, 2 / s ** 3))
    return {"g": g, "ga": ga, "gb": gb, "gaa": gaa, "gab": gab, "gbb": gbb}


def derivative_majorants(q, a_interval, b_interval):
    """Uniform norms on a positive contact rectangle, preserving O(q^3).

    F=c^2 K, K=(i*sigma*q)^3 int_D exp(i*sigma*q*c*lambda3)dλ.
    |K|<=q^3/6,|K'|<=q^4/24,|K''|<=q^5/60. Product derivatives
    give the F/F'/F'' bounds below. For actual paths Q3 is a probability;
    |g|<=1 is supplied separately, never assumed at infeasible ab<1 corners.
    """
    q = exact(q)
    al, ah = map(exact, a_interval)
    bl, bh = map(exact, b_interval)
    require(q >= 0 and 0 < al <= ah and 0 < bl <= bh, "Positive exact derivative domain")
    s = al + bl
    B = q ** 3 * (ah ** 2 + bh ** 2) / 6
    def F_bounds(c):
        return (q ** 3 * c ** 2 / 6,
                q ** 3 * c / 3 + q ** 4 * c ** 2 / 24,
                q ** 3 / 3 + q ** 4 * c / 6 + q ** 5 * c ** 2 / 60)
    _, pa, ppa = F_bounds(ah)
    _, pb, ppb = F_bounds(bh)
    return {"ga": pa / s + B / s ** 2, "gb": pb / s + B / s ** 2,
            "gaa": ppa / s + 2 * pa / s ** 2 + 2 * B / s ** 3,
            "gbb": ppb / s + 2 * pb / s ** 2 + 2 * B / s ** 3,
            "gab": (pa + pb) / s ** 2 + 2 * B / s ** 3}


def rho_derivatives(a, b):
    a, b = map(exact, (a, b))
    require(a > 0 and b > 0, "Positive rho geometry")
    s, Q = a + b, a * a + b * b
    return {"rho": Q / s, "ra": 2 * a / s - Q / s ** 2, "rb": 2 * b / s - Q / s ** 2,
            "raa": 4 * b * b / s ** 3, "rbb": 4 * a * a / s ** 3, "rab": -4 * a * b / s ** 3}


def joint_taylor_upper(nominal_upper, grad_a_interval, grad_b_interval,
                       delta_a_interval, delta_b_interval, Hessian_abs_bounds):
    """Whole-cell scalar upper from PREVERIFIED signed gradients/Hessian.

    Caller supplies signed gradient intervals (joint frequency sums already
    performed), and proven absolute Hessian bounds along every feasible
    segment from centre to target. No per-frequency triangle is inserted
    into the first-order term. This algebra utility verifies no premises.
    """
    nominal_upper = exact(nominal_upper)
    ga, gb, da, db = (tuple(map(exact, interval)) for interval in
                      (grad_a_interval, grad_b_interval, delta_a_interval, delta_b_interval))
    require(all(interval[0] <= interval[1] for interval in (ga, gb, da, db)), "Ordered exact intervals")
    haa, hab, hbb = map(exact, Hessian_abs_bounds)
    require(min(haa, hab, hbb) >= 0, "Proven nonnegative Hessian norms")
    linear = max(x * y for x in ga for y in da) + max(x * y for x in gb for y in db)
    wa, wb = max(map(abs, da)), max(map(abs, db))
    return nominal_upper + linear + (haa * wa ** 2 + 2 * hab * wa * wb + hbb * wb ** 2) / 2


def self_tests():
    checks = 0
    for a, b in ((F(1), F(1)), (F(1, 2), F(2)), (F(2, 3), F(3, 2)), (F(3, 4), F(7, 4))):
        geo = coordinates(a, b)
        pm, pp, pz = geo["pminus"], geo["pplus"], geo["pzero"]
        require(pm + pp + pz == 1 and -a * pm + b * pp == 0 and a * a * pm + b * b * pp == 1,
                "Exact Q3 normalization/mean/variance")
        require(a ** 3 * pm + b ** 3 * pp == geo["rhoQ"] and geo["w"] == 1 / (a * b), "Exact coordinate moments")
        r = rho_derivatives(a, b)
        require(r["raa"] * r["rbb"] == r["rab"] ** 2 and r["raa"] >= 0, "rho Hessian positive semidefinite rank1")
        checks += 3
        for q in (F(0), F(1, 8), F(1), F(3)):
            fresh = nominal_derivative_rectangles(q, a, b)
            negative = arithmetic.exponential_exact_argument(-q * a)
            positive = arithmetic.exponential_exact_argument(q * b)
            direct = add(add(scale(negative, pm), scale(positive, pp)), constant(pz))
            require(fresh["g"][0] <= direct[1] and direct[0] <= fresh["g"][1]
                    and fresh["g"][2] <= direct[3] and direct[2] <= fresh["g"][3], "Moment-preserving g equals direct reference")
            # Independent first-derivative formula from weights/exponents.
            s = a + b
            direct_ga = add(add(scale(negative, -(2 * a + b) / (a * a * s * s)),
                               scale(positive, -1 / (b * s * s))), constant(1 / (a * a * b)))
            direct_ga = add(direct_ga, scale(multiply_i(negative, -1), q * pm))
            require(fresh["ga"][0] <= direct_ga[1] and direct_ga[0] <= fresh["ga"][1]
                    and fresh["ga"][2] <= direct_ga[3] and direct_ga[2] <= fresh["ga"][3], "Independent exact ga algebra identity")
            if q == 0:
                require(all(rectangle == (0, 0, 0, 0) for key, rectangle in fresh.items() if key != "g"),
                        "Fixed moments give exact zero q0 geometry derivatives")
            checks += 2
    upper = joint_taylor_upper(F(1), (F(-2), F(-1)), (F(3), F(4)),
                              (F(-1, 10), F(1, 10)), (F(-1, 20), F(1, 20)), (F(2), F(1), F(3)))
    require(upper == F(1) + F(1, 5) + F(1, 5) + F(15, 800), "Joint signed gradient/Hessian algebra")
    checks += 1
    return {"status": "EXACT_CONTACT_COORDINATE_DERIVATIVE_ALGEBRA_TINY_CHECKS_ONLY", "exact_checks": checks,
            "N_H_y_table_or_optimizer_run": False, "CDF_or_global_cover_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
