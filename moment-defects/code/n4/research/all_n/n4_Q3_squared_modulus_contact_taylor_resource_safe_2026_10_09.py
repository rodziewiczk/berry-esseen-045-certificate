"""Exact contact-Taylor upper for |g_Q3(q)|^2 ONLY; no CDF producer.

The public compute_verified_box_modulus_squared_taylor consumes a FRESH
preverified in-memory BOX table, not saved JSON/status/hash data. Its
old g_actual_modulus_upper_int is a mathematical bound supplied by that
audited producer. Geometry and nominal characteristic rectangles are
independently rebuilt and matched. No A1/HG/cache/price/center producer
is called. Only g_actual_modulus_upper_int in the returned frequency_data
is changed. Old Eg/D3/D4/A1/caches and reference-center bounds remain
untouched and valid: tightening a consumer's |g_actual| upper does not
retroactively require redoing already valid looser A1 estimates.

For F_q(a,b)=|g(a,b)|^2,
 Fi=2Re(conj(g)*gi),
 Fij=2Re(conj(gi)*gj+conj(g)*gij).
The radial first derivatives retain their SIGNS at every frequency; no
|gi| triangle replaces them. On feasible probability contact segments,
 |Fij| <= 2*(Di*Dj+Eij), since |g|<=1.
The contact domain {a>0,b>=a,ab>=1} is convex. Thus the Hessian bounds
apply on the segments joining the true nominal, rational-above-nominal,
and actual Q3 references even though the w,beta image need not be convex.
Scalar Di/Eij are the audited HG/direct/matched minima from the center
helper. There is no claim that an infeasible contact-rectangle corner
itself is a probability.

Evaluate the signed radial gradients at rational a_bar=a_nom_hi/S,
b_bar=b_nom_hi/S. Expand them by Hessian*nominal-root-bracket width to
cover the TRUE irrational nominal gradients. The baseline is the TRUE
nominal CF rectangle's outward norm squared, NOT the bar-reference norm.
For the entire actual contact rectangle, signed linear increments plus
the absolute quadratic Taylor remainder enclose the actual squared
modulus. Intersect this complete upper with the old actualmod^2 and1,
then take an EXACT OUTWARD rational square root. Negative candidates are
rejected rather than clipped; all actual contact intervals contain the
nominal reference, so a valid whole-box Taylor upper is nonnegative.

Reflection conjugates both g and gi, leaving these real radial gradients
and modulus bounds unchanged. No eta/rho seed cap is imposed on the
nominal probability expansion point. All proof arithmetic Fraction/int;
timer/resources are diagnostic only. No physical quadrature/H reserves,
Gamma, norm-delta model, R2/CDF acceptance or unrestricted C4 assertion.
CLI runs only exact tiny algebra/unit/rounding tests, no N/H table or file
write. A coordinated consumer can call the API at N256/512 after a fresh
audited BOX backend, then use the new |g_actual| cap in its own R2 work.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import time

import n4_windows_resource_guard_2026_10_09 as resources

import n4_Q3_signed_contact_center_taylor_resource_safe_2026_10_09 as center

integer, arithmetic, SCALE = center.integer, center.arithmetic, center.SCALE
derivatives = center.derivatives
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
require, exact = center.require, center.exact


def nominal_squared_norm_upper(rectangle):
    """True probability CF rectangle; squared-modulus units, exact Fraction."""
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is int for value in rectangle)
            and rectangle[0] <= rectangle[1] and rectangle[2] <= rectangle[3],
            "Ordered integer nominal complex rectangle")
    real = max(abs(rectangle[0]), abs(rectangle[1]))
    imag = max(abs(rectangle[2]), abs(rectangle[3]))
    # Unit probability cap is a separate complete bound, not an assumption
    # that every point of the enclosing rectangle lies in the unit disk.
    return min(F(1), F(real * real + imag * imag, SCALE ** 2))


def radial_gradient_intervals(q, a_bar, b_bar):
    """Signed physical a/b gradients of |g|^2 at a rational probability Q."""
    values = derivatives.nominal_derivative_rectangles(q, a_bar, b_bar)
    g = arithmetic.unit_phase_intersection(values["g"])
    conjugate = integer.conjugate_rectangle(g)
    result = []
    for name in ("ga", "gb"):
        product = arithmetic.complex_multiply(conjugate, values[name])
        result.append((2 * product[0], 2 * product[1]))
    return tuple(result)


def modulus_squared_hessian_majorants(q, a_interval, b_interval):
    """Uniform |Faa|,|Fab|,|Fbb| on all feasible contact paths."""
    m = center.contact_derivative_majorants(q, a_interval, b_interval)
    return (2 * (m["ga"] ** 2 + m["gaa"]),
            2 * (m["ga"] * m["gb"] + m["gab"]),
            2 * (m["gb"] ** 2 + m["gbb"]))


def squared_modulus_taylor_upper(nominal_square_upper, gradient_a_int, gradient_b_int,
                                 delta_a_interval, delta_b_interval, hessian):
    """Whole-contact-box Taylor bound, with TRUE nominal F baseline."""
    nominal_square_upper = exact(nominal_square_upper)
    require(0 <= nominal_square_upper <= 1, "True nominal probability squared-modulus upper")
    da, db = center.interval(delta_a_interval), center.interval(delta_b_interval)
    require(da[0] <= 0 <= da[1] and db[0] <= 0 <= db[1], "Actual contact intervals contain true nominal")
    for gradient in (gradient_a_int, gradient_b_int):
        require(type(gradient) in (tuple, list) and len(gradient) == 2
                and all(type(value) is int for value in gradient) and gradient[0] <= gradient[1],
                "Ordered exact signed radial gradient")
    upper = derivatives.joint_taylor_upper(nominal_square_upper,
        tuple(F(value, SCALE) for value in gradient_a_int),
        tuple(F(value, SCALE) for value in gradient_b_int), da, db, hessian)
    require(upper >= 0, "Negative whole-box squared-modulus upper is an error, never clipped")
    return upper


def outward_modulus_from_squared_upper(taylor_square_upper, old_actual_modulus_upper_int):
    """Min of WHOLE square uppers then exact ceil(S*sqrt(.)); no floats."""
    taylor_square_upper = exact(taylor_square_upper)
    require(taylor_square_upper >= 0, "Nonnegative complete squared-modulus bound")
    require(type(old_actual_modulus_upper_int) is int and 0 <= old_actual_modulus_upper_int <= SCALE,
            "Old valid FRESH-table probability modulus upper integer")
    old_square = F(old_actual_modulus_upper_int ** 2, SCALE ** 2)
    selected_square = min(taylor_square_upper, old_square, F(1))
    numerator = selected_square.numerator * SCALE ** 2
    denominator = selected_square.denominator
    lower = isqrt(numerator // denominator)
    upper = lower + (lower * lower * denominator < numerator)
    require(lower * lower * denominator <= numerator
            and upper * upper * denominator >= numerator
            and 0 <= upper <= old_actual_modulus_upper_int <= SCALE,
            "Exact outward square root and never-weaker old modulus cap")
    return upper, selected_square


def compute_verified_box_modulus_squared_taylor(table, rectangle=None, N=None,
                                                 time_limit_seconds=TIME_LIMIT):
    """Fresh per-q radial Taylor API; input OLD modulus validity is a premise.

    This computes O(N) derivatives ONLY, not the box/A1/center table. It
    checks canonical labels, roots and exact midpoint CF rectangles. Old
    actualmod is NOT proven merely by labels: caller must have freshly
    called an audited producer. No arbitrary numeric-table importer or
    optimizer/status/hash substitute is supplied by this module.
    """
    started = time.monotonic()
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic cooperative budget <=60s")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Squared-modulus Taylor elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Squared-modulus Taylor working-set budget")
    # Exact geometry only; this routine does not execute a BOX producer.
    inputs = center.canonical_inputs(table, rectangle=rectangle, N=N)
    box, nominal, bridge, N, selected_H, ai, bi, a_bar, b_bar, da, db, ea, eb = inputs
    updated_frequencies, bounds = [], []
    for j, source in enumerate(table["frequency_data"]):
        guard()
        q = F(3 * (2 * j + 1), 2 * N)
        require(type(source["q"]) is F and source["q"] == q, "Exact physical q label")
        g0 = center.nominal_backend.generic_characteristic(q, nominal)
        require(tuple(source["g_nominal_rectangle"]) == g0,
                "TRUE nominal CF rectangle freshly rebuilt, not a bar-reference baseline")
        nominal_modulus = min(SCALE, integer.rectangle_modulus_upper(g0))
        require(type(source["g_nominal_modulus_upper_int"]) is int
                and source["g_nominal_modulus_upper_int"] == nominal_modulus,
                "Fresh nominal modulus integer matches exact rectangle")
        old_actual = source["g_actual_modulus_upper_int"]
        require(type(old_actual) is int and 0 <= old_actual <= SCALE,
                "Old actual modulus is a PREVERIFIED fresh-table bound")
        nominal_square = nominal_squared_norm_upper(g0)
        hessian = modulus_squared_hessian_majorants(q, ai, bi)
        bar_a, bar_b = radial_gradient_intervals(q, a_bar, b_bar)
        grad_a, grad_b = center.expand_true_nominal_gradient(bar_a, bar_b, ea, eb, hessian)
        taylor_square = squared_modulus_taylor_upper(nominal_square, grad_a, grad_b, da, db, hessian)
        actual_modulus, selected_square = outward_modulus_from_squared_upper(taylor_square, old_actual)
        # ONLY this proof field changes. In particular old A1/D3/D4/Eg
        # need not be recomputed, and are NOT rewritten here.
        updated_frequencies.append({**source, "g_actual_modulus_upper_int": actual_modulus})
        bounds.append({"q": q, "true_nominal_squared_modulus_upper": nominal_square,
            "rational_reference_radial_gradient_a_interval_int": bar_a,
            "rational_reference_radial_gradient_b_interval_int": bar_b,
            "true_nominal_radial_gradient_a_interval_int": grad_a,
            "true_nominal_radial_gradient_b_interval_int": grad_b,
            "uniform_squared_modulus_Hessian_abs_bounds": hessian,
            "whole_box_Taylor_squared_modulus_upper": taylor_square,
            "selected_squared_modulus_upper": selected_square,
            "old_actual_modulus_upper_int": old_actual,
            "new_actual_modulus_upper_int": actual_modulus,
            "modulus_improved": actual_modulus < old_actual})
    guard()
    require(len(updated_frequencies) == N and all(new[key] == old[key]
            for old, new in zip(table["frequency_data"], updated_frequencies)
            for key in old if key != "g_actual_modulus_upper_int"), "No old frequency proof field other than actual modulus changed")
    files = (Path(__file__), Path(center.__file__), Path(derivatives.__file__),
             Path(center.nominal_backend.__file__), Path(center.box_backend.__file__),
             Path(arithmetic.__file__), Path(integer.__file__), Path(resources.__file__))
    return {"status": "FRESH_INTEGER_OUTWARD_RADIAL_CONTACT_TAYLOR_BOX_MODULI_ONLY",
        "date": "2026-10-09", "scale": SCALE, "N": N,
        "box_geometry": box, "nominal_root_data": nominal,
        "frequency_data": updated_frequencies, "per_frequency_squared_modulus_bounds": bounds,
        "metadata": {"rational_reference_contacts": (a_bar, b_bar),
            "nominal_root_shift_upper": (ea, eb), "actual_minus_true_nominal_contact_intervals": (da, db),
            "radial_gradient": "2Re(conjg*gi), signed scalar intervals before contact increment upper",
            "radial_Hessian": "2*(DiDj+Eij), |g|<=1 ONLY on convex probability contact paths",
            "true_nominal_squared_modulus_baseline_rebuilt": True,
            "old_actual_modulus_validity_is_fresh_producer_math_precondition": True,
            "saved_JSON_status_hash_are_NOT_modulus_proofs": True,
            "modulus_improved_frequency_count": sum(row["modulus_improved"] for row in bounds),
            "exact_outward_square_root": "ceil(S*sqrt(min(Taylor_square,old_actualmod^2,1))) via integer isqrt and exact rational comparison",
            "only_existing_frequency_field_changed": "g_actual_modulus_upper_int",
            "A1_D3_D4_Eg_cache_center_Gamma_radius_modified": False,
            "reflection": "conjg/conjgi leave squared-modulus gradient and norm invariant; same result covers both beta orientations",
            "eta_or_rho_seed_cap_imposed_at_expansion_reference": False,
            "physical_or_H_reserves_added": False},
        "premises": "FRESH audited BOX table in memory, including its mathematically valid old actual-Q modulus caps; exact standardization and matching box Q3 geometry. Geometry/status/cache labels alone do not prove numeric inputs. Later conditional CDF/root work remains separate.",
        "conclusions": {"whole_box_reference_modulus_integer_outward_conditional_on_fresh_old_modulus": True,
            "delta_modulus_or_R2_acceptance_proved_here": False, "CDF_bound_proved": False,
            "unrestricted_C4_proved": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "standard_library_only": True}}


def self_tests():
    checks = 0
    for a, b in ((F(1), F(1)), (F(1, 2), F(2)), (F(3, 4), F(7, 4))):
        for q in (F(0), F(1, 8), F(1), F(3)):
            grads = radial_gradient_intervals(q, a, b)
            upper = integer.ceil_fraction_scaled(q ** 3 / 3)
            require(all(-upper <= lo <= hi <= upper for lo, hi in grads),
                    "Tiny radial gradient vs independent |F_i|<=2|g_i| HG bound")
            H = modulus_squared_hessian_majorants(q, (a, a), (b, b))
            require(min(H) >= 0, "Nonnegative complete analytic Hessian norms")
            values = derivatives.nominal_derivative_rectangles(q, a, b)
            nominal_square = nominal_squared_norm_upper(values["g"])
            taylor_square = squared_modulus_taylor_upper(nominal_square, *grads,
                (F(0), F(0)), (F(0), F(0)), H)
            require(taylor_square == nominal_square, "True baseline retained at zero contact displacement")
            if q == 0:
                require(grads == ((0, 0), (0, 0)) and H == (0, 0, 0) and nominal_square == 1,
                        "Exact q0 probability norm and zero radial derivatives")
            checks += 3
    # Independent rational square-root comparisons, including zero and
    # values whose square is not exactly representable at scale S.
    for taylor in (F(0), F(1, 9), F(1, 7), F(1), F(3)):
        for old in (0, SCALE // 3, SCALE // 2, SCALE):
            actual, selected = outward_modulus_from_squared_upper(taylor, old)
            require(F(actual, SCALE) ** 2 >= selected
                    and (actual == 0 or F(actual - 1, SCALE) ** 2 < selected)
                    and actual <= old, "Outward sqrt is exact minimal ceil and never weakens old bound")
            checks += 1
    require(nominal_squared_norm_upper((SCALE, SCALE, 1, 1)) == 1,
            "Unit cap is separate from rectangular norm geometry")
    checks += 1
    # Toy radial function F=(1+a+2b)^2 around a=b=0: signed gradients
    # 2 and4, exact Hessian (2,4,8), maximum at the positive endpoints.
    toy = squared_modulus_taylor_upper(F(1), (2 * SCALE, 2 * SCALE), (4 * SCALE, 4 * SCALE),
        (F(-1, 100), F(1, 100)), (F(-1, 200), F(1, 200)), (F(2), F(4), F(8)))
    require(toy == F(51, 50) ** 2, "Independent signed squared-modulus Taylor polynomial identity")
    checks += 1
    for call, expected in (
        (lambda: outward_modulus_from_squared_upper(F(-1), SCALE), "Nonnegative complete squared-modulus bound"),
        (lambda: outward_modulus_from_squared_upper(F(1), True), "Old valid FRESH-table probability modulus upper integer"),
        (lambda: squared_modulus_taylor_upper(F(1), (0, 0), (0, 0),
            (F(1), F(2)), (F(0), F(0)), (F(0), F(0), F(0))), "Actual contact intervals contain true nominal")):
        try:
            call()
        except RuntimeError as error:
            require(str(error) == expected, "Invalid exact interface input fails closed")
        else:
            raise RuntimeError("Invalid input accepted by squared-modulus helper")
        checks += 1
    return {"status": "SQUARED_MODULUS_SIGNED_CONTACT_TAYLOR_EXACT_TINY_TESTS_ONLY",
        "exact_checks": checks, "full_N_H_BOX_producer_called": False,
        "source_or_receipt_files_written_by_tests": False, "CDF_bound_proved": False,
        "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
