"""Exact normalized finite-Q3-centre Taylor lemma ONLY; no CDF producer.

This is a pure rational-arithmetic consumer of ALREADY FRESH mathematical
centre/gradient/Hessian enclosures. It does not build a CF, kernel, Gaussian
interval, nominal table, or quadrature cache. A status, source hash, JSON
receipt, or field named "verified" cannot establish any of its premises.
The legacy mis-scaled generic CF is not imported or called.

Let Q(a,b), a,b>0, be the standardized probability on {-a,0,b}, with
weights 1/[a(a+b)], 1-1/(ab), 1/[b(a+b)]. Its third absolute moment is
    rho(a,b) = (a*a+b*b)/(a+b).
Writing s=a+b, its exact gradient and Hessian are
    rho_a = (a*a+2*a*b-b*b)/s**2,
    rho_b = (b*b+2*a*b-a*a)/s**2,
    Hess rho = 4/s**3 * [[b*b,-a*b],[-a*b,a*a]].
The Hessian is positive semidefinite: v^T Hess v =
4*(b*v_a-a*v_b)**2/s**3. In fact, for ANY positive rational or real
contacts x=(a,b), z=(a_bar,b_bar), the supporting-plane residual is
    rho(x)-rho(z)-grad rho(z).(x-z)
      = 2*(b_bar*a-a_bar*b)**2 / [(a+b)*(a_bar+b_bar)**2] >= 0.
Thus the plane is a lower bound globally, not just at probability boxes.

For fixed H and reflection let C(x) be the finite raw Prawitz reference
centre 1+2 Re sum kappa_H*g_Q(x)**4-2 Phi(H/2). Let n be the TRUE nominal
contact pair, possibly irrational. The caller supplies a fresh upper C(n),
fresh intervals enclosing the TRUE signed C_a(n), C_b(n), and nonnegative
uniform |C_aa|,|C_ab|,|C_bb| bounds along each segment from n to an actual
probability reference in the box. One legitimate construction uses the
old signed-centre Hessian envelope and |g|<=1 on those probability paths.
The set a,b>0, ab>=1 is convex (b>=1/a); with beta-magnitude coordinates
b>=a it remains convex. It is NOT necessary that every interval-box corner
be a probability. The caller proves the actual and true nominal references
are probabilities and that the stated Hessian bounds cover the segments.

For T>=0 and any exact rational probability bar z, use
    rho(x)>=rho(z)+grad rho(z).(n-z)+grad rho(z).(x-n).
Taylor's inequality then bounds C(x)-T*rho(x) by
    C(n)-T*rho(z)-T*grad rho(z).(n-z)
      + [grad C(n)-T*grad rho(z)].(x-n) + R_C(x-n).
ONLY the old centre Hessian enters R_C. There is no extra absolute rho
Hessian cost: convexity already gives the correctly directed plane.
The TRUE nominal centre is retained; a CF at rational bar contacts must
NEVER silently replace C(n). Signed normalized gradients are retained.
The nominal-root intervals enclose n-z in the constant term and x-n in
the linear/quadratic terms. Independent interval enlargement loses only
root-width correlation and is outward; it makes no root equality claim.

If only fresh gradients at z are supplied, expand_true_nominal_gradient
encloses their difference from gradients at n using the SAME centre
Hessian envelope along z--n. This requires those additional probability
segments and no CF rebuild. Integer convenience functions express EVERY
input/output bound in the declared fixed-point scale without physical /
fixed-point remainder mixing.

The result is a uniform upper of C_H(Q_actual)-T*rhoQ_actual over the WHOLE
geometry box for the stated H/reflection. It is not max C minus an
independently minimized rho. A later CDF consumer can add a proved raw
transfer, ONE physical quadrature/H reserve, and subtract T*eta, since
rhoP=rhoQ_actual+eta. That consumer still proves all physical premises,
all H/reflections/tails, closed eta coverage and the target/CE comparison.
This helper proves none of those and no unrestricted C4. There is no
producer, replay, file-write, or runtime certificate CLI. The tiny exact
tests below are dormant until separately authorized and invoked.
"""

from __future__ import annotations

from fractions import Fraction as F

SCALE = 10 ** 40
DEFAULT_TARGET = F(4097, 10000)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    require(type(value) in (F, int), "Exact Fraction/int proof inputs only")
    return F(value)


def interval(values):
    require(type(values) in (tuple, list) and len(values) == 2,
            "Exact interval has two endpoints")
    lo, hi = map(exact, values)
    require(lo <= hi, "Ordered exact interval")
    return lo, hi


def product_upper(left, right):
    al, ah = interval(left)
    bl, bh = interval(right)
    return max(al * bl, al * bh, ah * bl, ah * bh)


def ceil_scaled(value, scale=SCALE):
    require(type(scale) is int and scale > 0, "Positive exact integer scale")
    value = exact(value) * scale
    return -((-value.numerator) // value.denominator)


def moment_value_gradient_hessian(a, b):
    """Exact rho, signed gradient, and PSD Hessian at positive contacts."""
    a, b = map(exact, (a, b))
    require(a > 0 and b > 0, "Positive physical contacts")
    s = a + b
    rho = (a * a + b * b) / s
    grad = ((a * a + 2 * a * b - b * b) / s ** 2,
            (b * b + 2 * a * b - a * a) / s ** 2)
    hessian = (4 * b * b / s ** 3, -4 * a * b / s ** 3,
               4 * a * a / s ** 3)
    return rho, grad, hessian


def supporting_plane_residual(a, b, a_bar, b_bar):
    """Exact nonnegative Bregman residual; useful also at nonprobability x."""
    a, b, a_bar, b_bar = map(exact, (a, b, a_bar, b_bar))
    require(min(a, b, a_bar, b_bar) > 0, "Positive supporting-plane domain")
    return 2 * (b_bar * a - a_bar * b) ** 2 / ((a + b) * (a_bar + b_bar) ** 2)


def hessian_abs_bounds(values):
    require(type(values) in (tuple, list) and len(values) == 3,
            "Centre Hessian absolute bounds are (aa,ab,bb)")
    values = tuple(map(exact, values))
    require(min(values) >= 0, "Nonnegative proven centre Hessian bounds")
    return values


def expand_true_nominal_gradient(bar_gradient_a, bar_gradient_b,
                                 nominal_a_interval, nominal_b_interval,
                                 bar_contacts, center_hessian):
    """Pure from-fresh-gradients root shift; no bar centre substitution.

    The supplied Hessian bounds MUST also hold on the nominal--bar segment.
    A bar probability above both true contacts is a usual valid choice.
    """
    ga, gb = interval(bar_gradient_a), interval(bar_gradient_b)
    na, nb = interval(nominal_a_interval), interval(nominal_b_interval)
    require(type(bar_contacts) in (tuple, list) and len(bar_contacts) == 2,
            "Two exact bar contacts")
    a_bar, b_bar = map(exact, bar_contacts)
    require(a_bar > 0 and b_bar >= a_bar and a_bar * b_bar >= 1,
            "Rational beta-magnitude bar reference is a probability")
    require(na[0] > 0 and nb[0] > 0, "Positive nominal contact brackets")
    haa, hab, hbb = hessian_abs_bounds(center_hessian)
    ea = max(abs(na[0] - a_bar), abs(na[1] - a_bar))
    eb = max(abs(nb[0] - b_bar), abs(nb[1] - b_bar))
    ra, rb = haa * ea + hab * eb, hab * ea + hbb * eb
    return (ga[0] - ra, ga[1] + ra), (gb[0] - rb, gb[1] + rb)


def normalized_contact_taylor_upper(
        true_nominal_center_upper, true_gradient_a_interval,
        true_gradient_b_interval, nominal_a_interval, nominal_b_interval,
        actual_a_interval, actual_b_interval, bar_contacts, center_hessian,
        target=DEFAULT_TARGET):
    """Uniform WHOLE-box upper C(actual)-T*rho(actual), exact Fraction.

    Bounds/gradients/Hessians are mathematical premises supplied freshly
    by the caller; checking types/geometry here does not verify their truth.
    Coordinates are canonical a,b for BOTH reflections, not swapped merely
    because the reference CF was conjugated. C must include its raw factor2.
    """
    c0, target = map(exact, (true_nominal_center_upper, target))
    require(target >= 0, "Nonnegative exact target")
    ga, gb = interval(true_gradient_a_interval), interval(true_gradient_b_interval)
    na, nb = interval(nominal_a_interval), interval(nominal_b_interval)
    aa, ab = interval(actual_a_interval), interval(actual_b_interval)
    require(min(na[0], nb[0], aa[0], ab[0]) > 0, "Positive contact intervals")
    require(aa[0] <= na[0] <= na[1] <= aa[1]
            and ab[0] <= nb[0] <= nb[1] <= ab[1],
            "Nominal root brackets contained in actual path envelopes")
    require(type(bar_contacts) in (tuple, list) and len(bar_contacts) == 2,
            "Two exact bar contacts")
    a_bar, b_bar = map(exact, bar_contacts)
    require(a_bar > 0 and b_bar >= a_bar and a_bar * b_bar >= 1,
            "Rational beta-magnitude bar reference is a probability")
    haa, hab, hbb = hessian_abs_bounds(center_hessian)
    rho_bar, rho_gradient, _ = moment_value_gradient_hessian(a_bar, b_bar)
    ra, rb = rho_gradient
    shift_a = (na[0] - a_bar, na[1] - a_bar)
    shift_b = (nb[0] - b_bar, nb[1] - b_bar)
    delta_a = (aa[0] - na[1], aa[1] - na[0])
    delta_b = (ab[0] - nb[1], ab[1] - nb[0])
    root_shift_upper = (product_upper((-target * ra, -target * ra), shift_a)
                        + product_upper((-target * rb, -target * rb), shift_b))
    normalized_ga = (ga[0] - target * ra, ga[1] - target * ra)
    normalized_gb = (gb[0] - target * rb, gb[1] - target * rb)
    signed_linear_upper = (product_upper(normalized_ga, delta_a)
                           + product_upper(normalized_gb, delta_b))
    da, db = max(map(abs, delta_a)), max(map(abs, delta_b))
    remainder = haa * da ** 2 / 2 + hab * da * db + hbb * db ** 2 / 2
    constant = c0 - target * rho_bar + root_shift_upper
    return {
        "target": target,
        "raw_minus_target_rhoQ_upper": constant + signed_linear_upper + remainder,
        "true_nominal_center_upper": c0,
        "rho_bar_exact": rho_bar,
        "rho_gradient_bar_exact": rho_gradient,
        "true_minus_bar_contact_intervals": (shift_a, shift_b),
        "actual_minus_true_nominal_contact_intervals": (delta_a, delta_b),
        "normalized_true_gradient_intervals": (normalized_ga, normalized_gb),
        "normalized_nominal_constant_upper": constant,
        "root_shift_constant_upper": root_shift_upper,
        "signed_linear_upper": signed_linear_upper,
        "raw_center_quadratic_remainder_upper": remainder,
        "center_Hessian_abs_bounds": (haa, hab, hbb),
        "rho_Hessian_absolute_cost_added": F(0),
        "true_nominal_baseline_retained": True,
        "physical_or_H_reserves_added": False,
        "CDF_bound_proved_here": False,
    }


def normalized_contact_taylor_upper_int(
        true_nominal_center_upper_int, true_gradient_a_interval_int,
        true_gradient_b_interval_int, nominal_a_bracket_int,
        nominal_b_bracket_int, actual_a_bracket_int, actual_b_bracket_int,
        bar_contacts, center_hessian, target=DEFAULT_TARGET, scale=SCALE):
    """Declared fixed-point convenience; no float or physical-unit ambiguity."""
    require(type(scale) is int and scale > 0, "Positive exact integer scale")
    require(type(true_nominal_center_upper_int) is int, "Raw centre upper fixed integer")
    inputs = (true_gradient_a_interval_int, true_gradient_b_interval_int,
              nominal_a_bracket_int, nominal_b_bracket_int,
              actual_a_bracket_int, actual_b_bracket_int)
    for values in inputs:
        require(type(values) in (tuple, list) and len(values) == 2
                and all(type(x) is int for x in values) and values[0] <= values[1],
                "Ordered two-integer gradient/root brackets at declared scale")
    converted = [tuple(F(value, scale) for value in values) for values in inputs]
    result = normalized_contact_taylor_upper(F(true_nominal_center_upper_int, scale),
        *converted, bar_contacts, center_hessian, target)
    result["scale"] = scale
    result["raw_minus_target_rhoQ_upper_int"] = ceil_scaled(
        result["raw_minus_target_rhoQ_upper"], scale)
    return result


def self_tests():
    """Dormant cheap exact algebra regressions, no CF/table/CDF producer."""
    checks = 0
    contacts = ((F(1), F(1)), (F(1, 2), F(2)),
                (F(3, 4), F(7, 4)), (F(2), F(3)))
    for a_bar, b_bar in contacts:
        rho_bar, grad, hess = moment_value_gradient_hessian(a_bar, b_bar)
        haa, hab, hbb = hess
        require(haa >= 0 and hbb >= 0 and haa * hbb - hab * hab == 0,
                "Exact PSD moment Hessian, not absolute-Hessian overhead")
        checks += 1
        for a, b in contacts + ((F(1, 10), F(1, 5)),):
            rho, _, _ = moment_value_gradient_hessian(a, b)
            residual = rho - rho_bar - grad[0] * (a - a_bar) - grad[1] * (b - b_bar)
            require(residual == supporting_plane_residual(a, b, a_bar, b_bar)
                    and residual >= 0, "Exact global plane residual identity")
            checks += 1
        for va, vb in ((F(1), F(0)), (F(-1), F(2)), (F(3, 7), F(-2, 5))):
            require(haa * va ** 2 + 2 * hab * va * vb + hbb * vb ** 2
                    == 4 * (b_bar * va - a_bar * vb) ** 2 / (a_bar + b_bar) ** 3,
                    "Exact PSD quadratic form identity")
            checks += 1
    require(moment_value_gradient_hessian(F(1, 2), F(2))[1][0] < 0,
            "Signed negative rho_a is retained")
    checks += 1
    target = F(4097, 10000)
    hessian = (F(4), F(2), F(3))
    def center(a, b):
        return 7 - 2 * a + 3 * b + 2 * a ** 2 + 2 * a * b + F(3, 2) * b ** 2
    def gradient(a, b):
        return -2 + 4 * a + 2 * b, 3 + 2 * a + 3 * b
    nominal_a, nominal_b = (F(99, 100), F(101, 100)), (F(199, 100), F(201, 100))
    actual_a, actual_b = (F(9, 10), F(11, 10)), (F(19, 10), F(21, 10))
    bar = (nominal_a[1], nominal_b[1])
    for na in nominal_a + (F(1),):
        for nb in nominal_b + (F(2),):
            ga, gb = gradient(na, nb)
            result = normalized_contact_taylor_upper(center(na, nb), (ga, ga), (gb, gb),
                nominal_a, nominal_b, actual_a, actual_b, bar, hessian, target)
            for a in actual_a + (F(1),):
                for b in actual_b + (F(2),):
                    rho, _, _ = moment_value_gradient_hessian(a, b)
                    require(center(a, b) - target * rho <= result["raw_minus_target_rhoQ_upper"],
                            "Whole-box signed normalized Taylor bound, uncertain true root")
                    checks += 1
    ga_bar, gb_bar = gradient(*bar)
    expanded = expand_true_nominal_gradient((ga_bar, ga_bar), (gb_bar, gb_bar),
        nominal_a, nominal_b, bar, hessian)
    for na in nominal_a:
        for nb in nominal_b:
            grad_true = gradient(na, nb)
            require(all(bounds[0] <= value <= bounds[1] for bounds, value in zip(expanded, grad_true)),
                    "Fresh bar gradient shifted to true nominal, no baseline replacement")
            checks += 1
    scale = 10000
    ga, gb = gradient(F(1), F(2))
    exact_result = normalized_contact_taylor_upper(center(F(1), F(2)), (ga, ga), (gb, gb),
        nominal_a, nominal_b, actual_a, actual_b, bar, hessian, target)
    inputs = [(ga, ga), (gb, gb), nominal_a, nominal_b, actual_a, actual_b]
    integers = [tuple(int(value * scale) for value in values) for values in inputs]
    integer_result = normalized_contact_taylor_upper_int(int(center(F(1), F(2)) * scale),
        *integers, bar, hessian, target, scale)
    require(integer_result["raw_minus_target_rhoQ_upper"] == exact_result["raw_minus_target_rhoQ_upper"]
            and F(integer_result["raw_minus_target_rhoQ_upper_int"], scale)
            >= exact_result["raw_minus_target_rhoQ_upper"], "Fixed-point units and outward signed ceil")
    checks += 1
    for value in (F(-17, 13), F(0), F(19, 11)):
        rounded = ceil_scaled(value, 17)
        require(F(rounded - 1, 17) < value <= F(rounded, 17), "Signed exact fixed-point ceiling")
        checks += 1
    try:
        moment_value_gradient_hessian(0.5, F(2))
    except ValueError as error:
        require(str(error) == "Exact Fraction/int proof inputs only", "Float proof input rejected")
        checks += 1
    else:
        raise ValueError("Float proof input was accepted")
    return {"exact_checks": checks, "CF_or_full_table_producer_called": False,
            "source_or_receipt_files_written": False, "CDF_bound_proved": False,
            "unrestricted_C4_proved": False}
