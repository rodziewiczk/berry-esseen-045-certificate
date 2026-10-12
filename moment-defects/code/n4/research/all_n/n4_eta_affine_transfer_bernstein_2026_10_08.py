"""Exact polynomial tools for WHOLE eta fibres, not a C4 certificate alone.

A proven affine nonnegative radius e=A+B*eta and a proven modulus upper
a in[0,1] give a quartic/linear/constant absolute fourth-power transfer.
The breakpoints are rational linear equations. Bernstein negativity can
then certify entire closed eta intervals; a conservative frozen-p cap
gives a cheaper affine majorant with exact endpoint/Bernstein checks.
This module does not supply the radius/moment/Prawitz inputs. Its tests
are exact algebra regressions, not a whole-root or CDF acceptance flag.
Only Fraction/int proof inputs; floats and bools are rejected. No imports
run jobs. Main creates a new small test receipt, never replaces one.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    require(type(value) in (F, int), "Only exact Fraction or int proof inputs")
    return F(value)


def polynomial(values):
    values = tuple(exact(value) for value in values)
    require(1 <= len(values) <= 5, "Polynomial degree at most four")
    while len(values) > 1 and values[-1] == 0:
        values = values[:-1]
    return values


def poly_add(left, right):
    left, right = polynomial(left), polynomial(right)
    return polynomial(tuple((left[j] if j < len(left) else F(0))
                            + (right[j] if j < len(right) else F(0))
                            for j in range(max(len(left), len(right)))))


def poly_scale(values, factor):
    factor = exact(factor)
    return polynomial(tuple(factor * value for value in polynomial(values)))


def poly_multiply(left, right):
    left, right = polynomial(left), polynomial(right)
    require(len(left) + len(right) - 2 <= 4, "Product degree at most four")
    result = [F(0)] * (len(left) + len(right) - 1)
    for j, a in enumerate(left):
        for k, b in enumerate(right):
            result[j + k] += a * b
    return polynomial(result)


def affine_power(intercept, slope, degree):
    intercept, slope = exact(intercept), exact(slope)
    require(type(degree) is int and 0 <= degree <= 4, "Exact degree zero to four")
    return polynomial(tuple(comb(degree, j) * intercept ** (degree - j) * slope ** j
                            for j in range(degree + 1)))


def evaluate(values, x):
    x = exact(x)
    result = F(0)
    for value in reversed(polynomial(values)):
        result = result * x + value
    return result


def bernstein_coefficients(values, lower, upper, degree=4):
    values, lower, upper = polynomial(values), exact(lower), exact(upper)
    require(lower <= upper, "Ordered closed interval")
    require(type(degree) is int and len(values) - 1 <= degree <= 4,
            "Bernstein degree covers the polynomial and is at most four")
    width = upper - lower
    shifted = [width ** j * sum((values[k] * comb(k, j) * lower ** (k - j)
                                for k in range(j, len(values))), F(0))
               for j in range(len(values))]
    return tuple(sum((shifted[j] * F(comb(i, j), comb(degree, j))
                      for j in range(min(i, len(shifted) - 1) + 1)), F(0))
                 for i in range(degree + 1))


def bernstein_strict_negative(values, lower, upper, degree=4):
    coefficients = bernstein_coefficients(values, lower, upper, degree)
    return all(value < 0 for value in coefficients), coefficients


def checked_radius(a, intercept, slope, lower, upper):
    a, intercept, slope, lower, upper = map(exact, (a, intercept, slope, lower, upper))
    require(0 <= a <= 1 and lower <= upper, "Valid modulus and interval")
    require(min(intercept + slope * lower, intercept + slope * upper) >= 0,
            "Affine radius must be nonnegative on the WHOLE interval")
    return a, intercept, slope, lower, upper


def frozen_cap_linear_transfer(a, intercept, slope, lower, upper):
    """A sound affine majorant; does NOT assert it is the tightest branch."""
    a, intercept, slope, lower, upper = checked_radius(a, intercept, slope, lower, upper)
    largest_radius = max(intercept + slope * lower, intercept + slope * upper)
    p = min(F(1), a + largest_radius)
    multiplier = p ** 3 + p ** 2 * a + p * a ** 2 + a ** 3
    return polynomial((intercept * multiplier, slope * multiplier))


def affine_transfer_segments(a, intercept, slope, lower, upper):
    """Exact transfer polynomial on each closed branch segment."""
    a, intercept, slope, lower, upper = checked_radius(a, intercept, slope, lower, upper)
    multiplier = 1 + a + a ** 2 + a ** 3
    first_threshold = 1 - a
    second_threshold = (1 + a ** 4) / multiplier
    require(second_threshold >= first_threshold, "Ordered cap transitions")
    cuts = {lower, upper}
    if slope:
        for threshold in (first_threshold, second_threshold):
            root = (threshold - intercept) / slope
            if lower < root < upper:
                cuts.add(root)
    ordered = sorted(cuts)
    intervals = list(zip(ordered, ordered[1:])) if lower < upper else [(lower, upper)]
    result = []
    for left, right in intervals:
        middle_radius = intercept + slope * (left + right) / 2
        if middle_radius <= first_threshold:
            kind = "quartic"
            values = poly_add(affine_power(a + intercept, slope, 4), (-a ** 4,))
        elif middle_radius <= second_threshold:
            kind = "linear"
            values = polynomial((intercept * multiplier, slope * multiplier))
        else:
            kind = "constant"
            values = polynomial((1 + a ** 4,))
        result.append({"lower": left, "upper": right, "kind": kind, "polynomial": values})
    require(len(result) >= 1, "Closed branch cover is nonempty")
    return result


def raw_target_for_transfers(raw_constant, terms, rho_q_lower, target):
    """raw_constant includes center/geometry and both physical reserves ONCE."""
    raw_constant, rho_q_lower, target = map(exact, (raw_constant, rho_q_lower, target))
    require(rho_q_lower > 0 and target > 0, "Positive normalization and target")
    result = polynomial((raw_constant - target * rho_q_lower, -target))
    for weight, transfer in terms:
        weight = exact(weight)
        require(weight >= 0, "Nonnegative kernel modulus weight")
        result = poly_add(result, poly_scale(transfer, 2 * weight))
    return result


def direct_transfer(a, radius):
    a, radius = exact(a), exact(radius)
    require(0 <= a <= 1 and radius >= 0, "Valid direct transfer inputs")
    p = min(F(1), a + radius)
    return min(radius * (p ** 3 + p ** 2 * a + p * a ** 2 + a ** 3), p ** 4 + a ** 4)


def exact_regressions():
    radius_cases = ((F(0), F(0), F(2), F(0), F(1)),
                    (F(1), F(0), F(1), F(0), F(1)),
                    (F(3, 5), F(0), F(1), F(0), F(1)),
                    (F(3, 5), F(1), F(-1), F(0), F(1)),
                    (F(1, 3), F(1, 10), F(0), F(0), F(1)),
                    (F(1, 2), F(1, 2), F(0), F(1, 3), F(1, 3)))
    checks = 0
    branch_counts = []
    for a, intercept, slope, lower, upper in radius_cases:
        pieces = affine_transfer_segments(a, intercept, slope, lower, upper)
        affine_upper = frozen_cap_linear_transfer(a, intercept, slope, lower, upper)
        require(pieces[0]["lower"] == lower and pieces[-1]["upper"] == upper, "Whole domain endpoints")
        for left, right in zip(pieces, pieces[1:]):
            require(left["upper"] == right["lower"], "No gap between closed branch cells")
            require(evaluate(left["polynomial"], left["upper"])
                    == evaluate(right["polynomial"], right["lower"]), "Branch face agreement")
        for piece in pieces:
            for j in range(9):
                eta = piece["lower"] + F(j, 8) * (piece["upper"] - piece["lower"])
                true = direct_transfer(a, intercept + slope * eta)
                require(evaluate(piece["polynomial"], eta) == true, "Exact transfer branch identity")
                require(evaluate(affine_upper, eta) >= true, "Frozen cap affine majorant")
                checks += 1
        branch_counts.append(len(pieces))
    for values in ((F(-1),), (F(-1), F(1, 2)), (F(-2), F(2), F(-1)),
                   (F(-3), F(2), F(5), F(-7), F(1))):
        for lower, upper in ((F(0), F(1)), (F(1, 3), F(7, 5)), (F(1, 2), F(1, 2))):
            coefficients = bernstein_coefficients(values, lower, upper)
            for j in range(9):
                t = F(j, 8)
                represented = sum((coefficients[i] * comb(4, i) * t ** i * (1 - t) ** (4 - i)
                                   for i in range(5)), F(0))
                require(represented == evaluate(values, lower + (upper - lower) * t),
                        "Exact Bernstein basis reconstruction")
                checks += 1
    passed, coefficients = bernstein_strict_negative((F(-1), F(1, 2)), F(0), F(1))
    require(passed and all(value < 0 for value in coefficients), "Strict whole-interval negativity")
    touching, _ = bernstein_strict_negative((F(-1), F(1)), F(0), F(1))
    require(not touching, "Touching target must not pass")
    invalid_radius_rejected = invalid_float_rejected = False
    try:
        affine_transfer_segments(F(1, 2), F(1, 10), F(-1), F(0), F(1))
    except ValueError:
        invalid_radius_rejected = True
    try:
        exact(.1)
    except ValueError:
        invalid_float_rejected = True
    require(invalid_radius_rejected and invalid_float_rejected, "Invalid proof inputs are rejected")
    target = raw_target_for_transfers(F(1, 10), [(F(1, 20), (F(0), F(1, 10)))], F(1), F(256, 625))
    require(evaluate(target, F(1, 3)) == F(1, 10) + F(1, 300) - F(256, 625) * F(4, 3),
            "Raw target includes sqrt4 factor and variable rho once")
    return {"exact_algebra_regression_checks": checks, "branch_counts": branch_counts,
            "touching_target_rejected": True, "negative_radius_rejected": True,
            "floating_proof_input_rejected": True, "raw_target_factor_two_checked": True}


def main():
    started = time.monotonic()
    output = Path(__file__).with_suffix(".json")
    require(not output.exists(), "Never overwrite an exact utility regression receipt")
    checks = exact_regressions()
    result = {"status": "EXACT_ETA_TRANSFER_AND_BERNSTEIN_UTILITIES_CHECKED",
              "date": "2026-10-08", "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "mathematical_scope": "Proven affine nonnegative epsilon, proven fixed a in[0,1], kernel/rho/center inputs must be supplied by the actual CDF gate. This utility alone does not verify those premises.",
              "proof_interface": "All strict-negative Bernstein coefficients bound the whole closed interval; failed or touching tests are UNKNOWN. Freeze any valid nonnegative affine radius per interval, not necessarily the pointwise optimizer.",
              "checks": checks,
              "conclusions": {"all_eta_for_an_actual_law_class_certified": False,
                              "CDF_bound_proved": False, "unrestricted_n4_closed": False},
              "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                            "standard_library_only": True, "degree_cap": 4}}
    raw = json.dumps(result, sort_keys=True, indent=2) + "\n"
    require(len(raw.encode("utf-8")) < 16 * 1024 and time.monotonic() - started < 10, "Tiny test budgets")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)
    print(json.dumps({"status": result["status"], "result": str(output), "checks": checks}, sort_keys=True))


if __name__ == "__main__":
    main()
