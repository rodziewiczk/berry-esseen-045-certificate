"""Linked-(w,beta) normalized Q3 centre Taylor lemma ONLY; no CDF producer.

All C(n), signed C_a(n),C_b(n), and contact Hessian enclosures are FRESH
mathematical premises. This pure Fraction consumer builds no CF, kernel,
Gaussian, quadrature cache, or reference table. Types, statuses, source
hashes, and numeric receipts do not establish any analytic input premise.
The TRUE, possibly irrational nominal centre is NEVER replaced by a CF
at rational contact endpoints. No physical or threshold reserve is added.

Canonical coordinates and root-width checks
------------------------------------------
For 0<w<=1 and 0<=beta<1 set D=1-beta^2 and

 a=sqrt((1-beta)/(w*(1+beta))),
 b=sqrt((1+beta)/(w*(1-beta))),
 rho=(1+beta^2)/sqrt(w*D).

Q(-a,0,b) is a standardized probability and ab=1/w>=1. The caller
supplies a closed rational w,beta rectangle, its EXACT rational midpoint,
positive nominal a,b,rho root brackets and whole-box a,b envelopes. Their
squares are checked against the exact nominal squares and monotone box
endpoint squares. This proves those scalar root enclosures arithmetically;
it does NOT prove the supplied centre/gradient/Hessian enclosures. Every
w,beta segment lies in this rectangular probability domain. Straight
contact segments needed below also remain probabilities because the set
{a,b>0,ab>=1,b>=a} is convex. The contact Hessian premise MUST cover those
nominal-to-actual segments as well as the actual w,beta image. It need not
assert that all corners of an enclosing contact rectangle are laws.

Jointly convex moment, with NO rho-Hessian absolute cost
-----------------------------------------------------
Writing rho=w^(-1/2)*f(beta),

 f=(1+beta^2)/sqrt(D),
 f'=beta*(3-beta^2)/D^(3/2), f''=3*(1+beta^2)/D^(5/2),

gives rho_w=-rho/(2w), rho_beta=k*rho, where
k=beta*(3-beta^2)/((1+beta^2)*D). The Hessian divided by rho is

 [[3/(4w^2), -k/(2w)],[-k/(2w),3/D^2]].

Its determinant is
 [9+9beta^2+15beta^4-beta^6]/[4w^2*(1+beta^2)^2*D^2]>0.
The numerator is 9+9z+z^2*(15-z)>0 for z=beta^2<1. Hence rho is
jointly convex on w>0, |beta|<1. At the TRUE nominal midpoint n,

 rho(x)>=rho(n)+rho_w(n)*(w-w0)+rho_beta(n)*(beta-beta0).

For T>=0 this is a correctly directed lower supporting plane. We enclose
TRUE rho(n) and TRUE nominal moment derivatives using the checked root
bracket, then subtract that plane. No absolute rho-Hessian remainder is
introduced. Separate rho and raw-centre extrema are not taken.

Linked signed centre gradients and uniform C-Hessian
--------------------------------------------------
For the finite raw reference centre C(a,b), including its factor2,

 C_w=-(a*C_a+b*C_b)/(2w), C_beta=(-a*C_a+b*C_b)/D.

These are enclosed with TRUE nominal a,b and TRUE signed contact gradients.
Let (Haa,Hab,Hbb) bound the absolute contact Hessian on all required paths.
The whole-box contact gradient bounds follow from the TRUE nominal
gradient intervals plus Haa*Delta_a+Hab*Delta_b and its b counterpart.
The exact contact derivatives are

 a_w=-a/(2w), b_w=-b/(2w), a_beta=-a/D, b_beta=b/D,
 a_ww=3a/(4w^2), b_ww=3b/(4w^2),
 a_wbeta=a/(2wD), b_wbeta=-b/(2wD),
 a_betabeta=a*(1-2beta)/D^2, b_betabeta=b*(1+2beta)/D^2.

In C_wbeta the Cab term cancels EXACTLY because
a_w*b_beta+b_w*a_beta=0. Uniform positive Jacobian/second-derivative
envelopes produce only a C-Hessian cost. A full absolute C-Hessian bound
(Hww,Hwb,Hbbeta) then gives the WHOLE-rectangle Taylor remainder

 Hww*dw_max^2/2+Hwb*dw_max*dbeta_max+Hbbeta*dbeta_max^2/2.

The linear terms use the linked rational increments w-w0,beta-beta0 and
SIGNED intervals C_w(n)-T*rho_w(n), C_beta(n)-T*rho_beta(n). Combining
their interval upper with C(n)_upper-T*rho(n)_lower and the centre
remainder bounds C(actual)-T*rho(actual) for every point in the box.
Both genuine reflections use the SAME a,b,w,beta coordinates; their
fresh centre gradients may differ and are supplied separately.

A later CDF consumer must still establish whole eta/H/reflection scope,
original-P transfer, ONE physical quadrature and H reserve, tails, target
comparison, and retained owner/literature premises. This helper proves
none of those, introduces no axioms, and proves no unrestricted C4.
No imports of older CF producers, files, JSON, timers, or runtime resource
monitor. Dormant exact algebra tests below are NOT executed on import.
"""

from __future__ import annotations

from fractions import Fraction as F

SCALE = 10 ** 40
DEFAULT_TARGET = F(4097, 10000)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    require(type(value) in (F, int), "Fraction/int exact inputs only; no floats/bools")
    return F(value)


def interval(values):
    require(type(values) in (tuple, list) and len(values) == 2,
            "Exact two-endpoint interval")
    lo, hi = map(exact, values)
    require(lo <= hi, "Ordered exact interval")
    return lo, hi


def multiply_intervals(left, right):
    al, ah = interval(left)
    bl, bh = interval(right)
    products = (al * bl, al * bh, ah * bl, ah * bh)
    return min(products), max(products)


def add_intervals(left, right):
    al, ah = interval(left)
    bl, bh = interval(right)
    return al + bl, ah + bh


def subtract_intervals(left, right):
    al, ah = interval(left)
    bl, bh = interval(right)
    return al - bh, ah - bl


def scalar_interval(value, bounds):
    value = exact(value)
    return multiply_intervals((value, value), bounds)


def absolute_interval_upper(bounds):
    return max(map(abs, interval(bounds)))


def ceil_scaled(value, scale=SCALE):
    require(type(scale) is int and scale > 0, "Positive exact integer scale")
    value = exact(value) * scale
    return -((-value.numerator) // value.denominator)


def checked_rectangle(rectangle):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4,
            "Closed rational w,beta-magnitude rectangle")
    wl, wh, bl, bh = map(exact, rectangle)
    require(0 < wl <= wh <= 1 and 0 <= bl <= bh < 1,
            "Whole rectangular standardized-probability domain")
    return wl, wh, bl, bh


def nominal_squares(w, beta):
    w, beta = map(exact, (w, beta))
    require(w > 0 and -1 < beta < 1, "Positive w and |beta|<1")
    D = 1 - beta ** 2
    return ((1 - beta) / (w * (1 + beta)),
            (1 + beta) / (w * (1 - beta)),
            (1 + beta ** 2) ** 2 / (w * D))


def check_positive_root_bracket(bounds, square, label):
    lo, hi = interval(bounds)
    require(lo > 0 and lo ** 2 <= square <= hi ** 2,
            "Exact positive TRUE " + label + " root bracket")
    return lo, hi


def checked_contact_data(rectangle, nominal_w, nominal_beta,
                         nominal_a_interval, nominal_b_interval,
                         nominal_rho_interval, actual_a_interval,
                         actual_b_interval):
    wl, wh, bl, bh = checked_rectangle(rectangle)
    w0, beta0 = map(exact, (nominal_w, nominal_beta))
    require(w0 == (wl + wh) / 2 and beta0 == (bl + bh) / 2,
            "TRUE reference uses the EXACT rational parameter midpoint")
    a2, b2, rho2 = nominal_squares(w0, beta0)
    na = check_positive_root_bracket(nominal_a_interval, a2, "nominal a")
    nb = check_positive_root_bracket(nominal_b_interval, b2, "nominal b")
    nr = check_positive_root_bracket(nominal_rho_interval, rho2, "nominal rho")
    aa, ab = interval(actual_a_interval), interval(actual_b_interval)
    require(aa[0] > 0 and ab[0] > 0,
            "Positive whole-contact envelopes")
    amin2, amax2 = (1 - bh) / (wh * (1 + bh)), (1 - bl) / (wl * (1 + bl))
    bmin2, bmax2 = (1 + bl) / (wh * (1 - bl)), (1 + bh) / (wl * (1 - bh))
    require(aa[0] ** 2 <= amin2 and amax2 <= aa[1] ** 2
            and ab[0] ** 2 <= bmin2 and bmax2 <= ab[1] ** 2,
            "Whole-box contact roots enclosed by exact endpoint squares")
    require(aa[0] <= na[0] <= na[1] <= aa[1]
            and ab[0] <= nb[0] <= nb[1] <= ab[1],
            "TRUE nominal root brackets contained in whole-contact envelopes")
    return (wl, wh, bl, bh), w0, beta0, na, nb, nr, aa, ab


def moment_derivative_shape(w, beta):
    """Exact gradient/Hessian divided by TRUE positive rho; PSD globally."""
    w, beta = map(exact, (w, beta))
    require(w > 0 and -1 < beta < 1, "Global convex-moment domain")
    D = 1 - beta ** 2
    k = beta * (3 - beta ** 2) / ((1 + beta ** 2) * D)
    numerator = 9 + 9 * beta ** 2 + 15 * beta ** 4 - beta ** 6
    determinant = numerator / (4 * w ** 2 * (1 + beta ** 2) ** 2 * D ** 2)
    hessian = (F(3, 4) / w ** 2, -k / (2 * w), 3 / D ** 2)
    require(numerator >= 9 and hessian[0] > 0 and hessian[2] > 0
            and hessian[0] * hessian[2] - hessian[1] ** 2 == determinant,
            "Exact positive definite rho-Hessian shape and determinant identity")
    return {"gradient_over_rho": (-1 / (2 * w), k),
            "Hessian_over_rho": hessian,
            "Hessian_determinant_over_rho_squared": determinant,
            "positive_determinant_numerator": numerator}


def contact_differentials(w, beta, a, b):
    """Exact physical contact Jacobian and second derivatives at a point."""
    w, beta, a, b = map(exact, (w, beta, a, b))
    a2, b2, _ = nominal_squares(w, beta)
    require(a > 0 and b > 0 and a ** 2 == a2 and b ** 2 == b2,
            "Exact rational point contacts match w,beta")
    D = 1 - beta ** 2
    return {"a_w": -a / (2 * w), "b_w": -b / (2 * w),
        "a_beta": -a / D, "b_beta": b / D,
        "a_ww": 3 * a / (4 * w ** 2), "b_ww": 3 * b / (4 * w ** 2),
        "a_wbeta": a / (2 * w * D), "b_wbeta": -b / (2 * w * D),
        "a_betabeta": a * (1 - 2 * beta) / D ** 2,
        "b_betabeta": b * (1 + 2 * beta) / D ** 2}


def chain_point_derivatives(contact_gradient, contact_hessian, differential):
    """Signed exact chain-rule identity; used only as pure algebra here."""
    ga, gb = map(exact, contact_gradient)
    haa, hab, hbb = map(exact, contact_hessian)
    d = differential
    cross = d["a_w"] * d["b_beta"] + d["b_w"] * d["a_beta"]
    require(cross == 0, "Mixed Cab term cancels EXACTLY")
    gradient = (ga * d["a_w"] + gb * d["b_w"],
                ga * d["a_beta"] + gb * d["b_beta"])
    hessian = (
        haa * d["a_w"] ** 2 + 2 * hab * d["a_w"] * d["b_w"]
        + hbb * d["b_w"] ** 2 + ga * d["a_ww"] + gb * d["b_ww"],
        haa * d["a_w"] * d["a_beta"] + hbb * d["b_w"] * d["b_beta"]
        + ga * d["a_wbeta"] + gb * d["b_wbeta"],
        haa * d["a_beta"] ** 2 + 2 * hab * d["a_beta"] * d["b_beta"]
        + hbb * d["b_beta"] ** 2 + ga * d["a_betabeta"] + gb * d["b_betabeta"])
    return gradient, hessian


def linked_center_hessian_bounds(rectangle, nominal_a_interval, nominal_b_interval,
                                  actual_a_interval, actual_b_interval,
                                  true_gradient_a_interval, true_gradient_b_interval,
                                  center_contact_hessian):
    """Whole-box C-Hessian, with contact-gradient drift and exact cross cancellation.

    The supplied contact Hessian bounds are ANALYTIC PREMISES on the image
    and the probability contact segments from the TRUE nominal reference.
    """
    wl, wh, bl, bh = checked_rectangle(rectangle)
    na, nb = interval(nominal_a_interval), interval(nominal_b_interval)
    aa, ab = interval(actual_a_interval), interval(actual_b_interval)
    ga, gb = interval(true_gradient_a_interval), interval(true_gradient_b_interval)
    require(type(center_contact_hessian) in (tuple, list) and len(center_contact_hessian) == 3,
            "Contact absolute Hessian triple aa,ab,bb")
    haa, hab, hbb = map(exact, center_contact_hessian)
    require(min(haa, hab, hbb) >= 0 and min(aa[0], ab[0], na[0], nb[0]) > 0,
            "Nonnegative analytic contact Hessian and positive envelopes")
    da = max(abs(aa[0] - na[1]), abs(aa[1] - na[0]))
    db = max(abs(ab[0] - nb[1]), abs(ab[1] - nb[0]))
    Ga = absolute_interval_upper(ga) + haa * da + hab * db
    Gb = absolute_interval_upper(gb) + hab * da + hbb * db
    A, B, Dlo = aa[1], ab[1], 1 - bh ** 2
    aw, bw = A / (2 * wl), B / (2 * wl)
    at, bt = A / Dlo, B / Dlo
    aww, bww = 3 * A / (4 * wl ** 2), 3 * B / (4 * wl ** 2)
    awt, bwt = A / (2 * wl * Dlo), B / (2 * wl * Dlo)
    att = A * max(abs(1 - 2 * bl), abs(1 - 2 * bh)) / Dlo ** 2
    btt = B * (1 + 2 * bh) / Dlo ** 2
    Hww = haa * aw ** 2 + 2 * hab * aw * bw + hbb * bw ** 2 + Ga * aww + Gb * bww
    Hwt = haa * aw * at + hbb * bw * bt + Ga * awt + Gb * bwt
    Htt = haa * at ** 2 + 2 * hab * at * bt + hbb * bt ** 2 + Ga * att + Gb * btt
    return {"center_w_beta_Hessian_abs_bounds": (Hww, Hwt, Htt),
        "whole_contact_gradient_absolute_uppers": (Ga, Gb),
        "nominal_to_actual_contact_drift_uppers": (da, db),
        "contact_Hessian_abs_bounds": (haa, hab, hbb),
        "mixed_Cab_coefficient_exact": F(0),
        "contact_Jacobian_abs_bounds": (aw, bw, at, bt),
        "contact_second_derivative_abs_bounds": (aww, bww, awt, bwt, att, btt)}


def normalized_w_beta_center_taylor_upper(
        true_nominal_center_upper, true_gradient_a_interval, true_gradient_b_interval,
        nominal_w, nominal_beta, nominal_a_interval, nominal_b_interval,
        nominal_rho_interval, rectangle, actual_a_interval, actual_b_interval,
        center_contact_hessian, target=DEFAULT_TARGET):
    """Uniform C(actual)-T*rhoQ(actual), preserving LINKED w,beta increments."""
    c0, target = map(exact, (true_nominal_center_upper, target))
    require(target >= 0, "Nonnegative exact target")
    rect, w0, beta0, na, nb, nr, aa, ab = checked_contact_data(
        rectangle, nominal_w, nominal_beta, nominal_a_interval, nominal_b_interval,
        nominal_rho_interval, actual_a_interval, actual_b_interval)
    ga, gb = interval(true_gradient_a_interval), interval(true_gradient_b_interval)
    a_ga, b_gb = multiply_intervals(na, ga), multiply_intervals(nb, gb)
    Cw = scalar_interval(-1 / (2 * w0), add_intervals(a_ga, b_gb))
    Cbeta = scalar_interval(1 / (1 - beta0 ** 2),
                           add_intervals(scalar_interval(-1, a_ga), b_gb))
    shape = moment_derivative_shape(w0, beta0)
    rho_w = scalar_interval(shape["gradient_over_rho"][0], nr)
    rho_beta = scalar_interval(shape["gradient_over_rho"][1], nr)
    normalized_w = subtract_intervals(Cw, scalar_interval(target, rho_w))
    normalized_beta = subtract_intervals(Cbeta, scalar_interval(target, rho_beta))
    wl, wh, bl, bh = rect
    dw, dt = (wl - w0, wh - w0), (bl - beta0, bh - beta0)
    linear = (multiply_intervals(normalized_w, dw)[1]
              + multiply_intervals(normalized_beta, dt)[1])
    bound = linked_center_hessian_bounds(rect, na, nb, aa, ab, ga, gb, center_contact_hessian)
    Hww, Hwt, Htt = bound["center_w_beta_Hessian_abs_bounds"]
    W, Tbeta = absolute_interval_upper(dw), absolute_interval_upper(dt)
    remainder = Hww * W ** 2 / 2 + Hwt * W * Tbeta + Htt * Tbeta ** 2 / 2
    constant = c0 - target * nr[0]
    return {"target": target, "closed_rectangle": rect,
        "nominal_w_beta_exact": (w0, beta0),
        "raw_minus_target_rhoQ_upper": constant + linear + remainder,
        "true_nominal_center_upper": c0, "true_nominal_rho_interval": nr,
        "true_nominal_contact_intervals": (na, nb),
        "true_nominal_linked_center_gradient_intervals": (Cw, Cbeta),
        "true_nominal_moment_gradient_intervals": (rho_w, rho_beta),
        "normalized_true_linked_gradient_intervals": (normalized_w, normalized_beta),
        "actual_minus_nominal_w_beta_intervals": (dw, dt),
        "normalized_nominal_constant_upper": constant,
        "signed_linked_linear_upper": linear,
        "raw_center_linked_quadratic_remainder_upper": remainder,
        "center_chain_rule_bound": bound,
        "rho_Hessian_absolute_cost_added": F(0),
        "true_nominal_baseline_retained": True,
        "physical_or_H_reserves_added": False, "CDF_bound_proved_here": False}


def normalized_w_beta_center_taylor_upper_int(
        true_nominal_center_upper_int, true_gradient_a_interval_int,
        true_gradient_b_interval_int, nominal_w, nominal_beta,
        nominal_a_bracket_int, nominal_b_bracket_int, nominal_rho_bracket_int,
        rectangle, actual_a_bracket_int, actual_b_bracket_int,
        center_contact_hessian, target=DEFAULT_TARGET, scale=SCALE):
    """Explicit fixed-point convenience; Hessian contacts remain physical Fractions."""
    require(type(scale) is int and scale > 0 and type(true_nominal_center_upper_int) is int,
            "Exact positive scale and signed raw-centre fixed integer")
    inputs = (true_gradient_a_interval_int, true_gradient_b_interval_int,
              nominal_a_bracket_int, nominal_b_bracket_int, nominal_rho_bracket_int,
              actual_a_bracket_int, actual_b_bracket_int)
    for pair in inputs:
        require(type(pair) in (tuple, list) and len(pair) == 2
                and all(type(v) is int for v in pair) and pair[0] <= pair[1],
                "Ordered two-int bracket in DECLARED fixed-point scale")
    ga, gb, na, nb, nr, aa, ab = [tuple(F(v, scale) for v in pair) for pair in inputs]
    result = normalized_w_beta_center_taylor_upper(F(true_nominal_center_upper_int, scale),
        ga, gb, nominal_w, nominal_beta, na, nb, nr, rectangle, aa, ab,
        center_contact_hessian, target)
    result["scale"] = scale
    result["raw_minus_target_rhoQ_upper_int"] = ceil_scaled(
        result["raw_minus_target_rhoQ_upper"], scale)
    return result


def self_tests():
    """DORMANT exact scalar regressions ONLY; no CF/certificate producer."""
    checks = 0
    for w in (F(1, 5), F(1, 2), F(1)):
        for beta in (F(-3, 4), F(-1, 3), F(0), F(1, 3), F(3, 4)):
            shape = moment_derivative_shape(w, beta)
            hww, hwt, htt = shape["Hessian_over_rho"]
            D = 1 - beta ** 2
            rho2 = (1 + beta ** 2) ** 2 / (w * D)
            expected = (9 + 9 * beta ** 2 + 15 * beta ** 4 - beta ** 6) / (4 * w ** 3 * D ** 3)
            require((hww * htt - hwt ** 2) * rho2 == expected and expected > 0,
                    "Exact rho-Hessian determinant identity, including negative beta")
            checks += 1
    for a, b in ((F(1), F(1)), (F(1, 2), F(2)), (F(1), F(2)), (F(3, 4), F(7, 4))):
        w, beta = 1 / (a * b), (b - a) / (a + b)
        d = contact_differentials(w, beta, a, b)
        require(d["a_w"] * d["b_beta"] + d["b_w"] * d["a_beta"] == 0,
                "Exact mixed-contact cross cancellation")
        checks += 1
        for name, gradient, hessian in (
                ("ab", (b, a), (F(0), F(1), F(0))),
                ("a2", (2 * a, F(0)), (F(2), F(0), F(0))),
                ("b2", (F(0), 2 * b), (F(0), F(0), F(2)))):
            actual_gradient, actual_hessian = chain_point_derivatives(gradient, hessian, d)
            if name == "ab":
                expected_gradient, expected_hessian = (-1 / w ** 2, F(0)), (2 / w ** 3, F(0), F(0))
            elif name == "a2":
                expected_gradient = (-a ** 2 / w, -2 / (w * (1 + beta) ** 2))
                expected_hessian = (2 * a ** 2 / w ** 2,
                    2 / (w ** 2 * (1 + beta) ** 2), 4 / (w * (1 + beta) ** 3))
            else:
                expected_gradient = (-b ** 2 / w, 2 / (w * (1 - beta) ** 2))
                expected_hessian = (2 * b ** 2 / w ** 2,
                    -2 / (w ** 2 * (1 - beta) ** 2), 4 / (w * (1 - beta) ** 3))
            require(actual_gradient == expected_gradient and actual_hessian == expected_hessian,
                    "Independent rational composition polynomial " + name)
            checks += 1
    rect = (F(2, 5), F(3, 5), F(1, 4), F(5, 12))
    w0, beta0 = F(1, 2), F(1, 3)
    na, nb, nr = (F(1), F(1)), (F(2), F(2)), (F(5, 3), F(5, 3))
    aa, ab = (F(4, 5), F(3, 2)), (F(3, 2), F(5, 2))
    H = (F(4), F(2), F(3))
    def center(a, b):
        return 7 - 2 * a + 3 * b + 2 * a ** 2 + 2 * a * b + F(3, 2) * b ** 2
    def gradient(a, b):
        return -2 + 4 * a + 2 * b, 3 + 2 * a + 3 * b
    ga, gb = gradient(F(1), F(2))
    result = normalized_w_beta_center_taylor_upper(center(F(1), F(2)), (ga, ga), (gb, gb),
        w0, beta0, na, nb, nr, rect, aa, ab, H)
    for a in (F(9, 10), F(1), F(11, 10)):
        for b in (F(9, 5), F(2), F(11, 5)):
            w, beta = 1 / (a * b), (b - a) / (a + b)
            if not (rect[0] <= w <= rect[1] and rect[2] <= beta <= rect[3]):
                continue
            rho = (a ** 2 + b ** 2) / (a + b)
            require(center(a, b) - DEFAULT_TARGET * rho <= result["raw_minus_target_rhoQ_upper"],
                    "Linked WHOLE-box normalized Taylor at rational probability law")
            d = contact_differentials(w, beta, a, b)
            _, chain = chain_point_derivatives(gradient(a, b), H, d)
            envelope = result["center_chain_rule_bound"]["center_w_beta_Hessian_abs_bounds"]
            require(all(abs(v) <= cap for v, cap in zip(chain, envelope)),
                    "Uniform chain Hessian envelope includes signed mixed derivative")
            checks += 2
    uncertain = normalized_w_beta_center_taylor_upper(center(F(1), F(2)), (ga, ga), (gb, gb),
        w0, beta0, (F(99, 100), F(101, 100)), (F(199, 100), F(201, 100)),
        (F(166, 100), F(168, 100)), rect, aa, ab, H)
    require(uncertain["normalized_nominal_constant_upper"] >= result["normalized_nominal_constant_upper"]
            and uncertain["raw_minus_target_rhoQ_upper"] >= center(F(1), F(2)) - DEFAULT_TARGET * F(5, 3),
            "TRUE irrational-root-width analogue: no nominal-root equality substitution")
    checks += 1
    scale = 3000
    pairs = ((ga, ga), (gb, gb), na, nb, nr, aa, ab)
    integer_pairs = [tuple(int(v * scale) for v in pair) for pair in pairs]
    gi_a, gi_b, ni_a, ni_b, ni_r, ai_a, ai_b = integer_pairs
    integer_result = normalized_w_beta_center_taylor_upper_int(int(center(F(1), F(2)) * scale),
        gi_a, gi_b, w0, beta0, ni_a, ni_b, ni_r, rect, ai_a, ai_b, H, scale=scale)
    require(integer_result["raw_minus_target_rhoQ_upper"] == result["raw_minus_target_rhoQ_upper"]
            and F(integer_result["raw_minus_target_rhoQ_upper_int"], scale)
            >= result["raw_minus_target_rhoQ_upper"], "Fixed-point conversion and signed upward rounding")
    checks += 1
    for value in (F(-17, 13), F(0), F(19, 11)):
        rounded = ceil_scaled(value, 17)
        require(F(rounded - 1, 17) < value <= F(rounded, 17), "Signed exact ceil")
        checks += 1
    invalid_cases = (
        lambda: moment_derivative_shape(F(1, 2), 0.5),
        lambda: exact(True),
        lambda: checked_contact_data(rect, w0, beta0, (F(101, 100), F(102, 100)), nb, nr, aa, ab),
        lambda: checked_contact_data(rect, w0, beta0, na, nb, (F(8, 5), F(33, 20)), aa, ab),
        lambda: checked_contact_data(rect, F(51, 100), beta0, na, nb, nr, aa, ab),
        lambda: checked_contact_data(rect, w0, beta0, na, nb, nr, (F(1), F(6, 5)), ab))
    for call in invalid_cases:
        rejected = False
        try:
            call()
        except ValueError:
            rejected = True
        require(rejected, "Invalid midpoint/root/whole-envelope/float/bool premise rejected")
        checks += 1
    return {"exact_checks": checks, "CF_reference_quadrature_or_CDF_producer_called": False,
        "files_JSON_or_runtime_proof_inputs": False, "rho_Hessian_absolute_cost_added": False,
        "CDF_bound_proved": False, "unrestricted_C4_proved": False}
