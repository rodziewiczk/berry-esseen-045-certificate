"""Integer outward helper/radius bounds under an EXPLICIT owner-support premise.

This is not an n4 CDF certificate or a whole-frequency quadrature verifier.
Analytical model: C3<CE, an attained positive closed C4>=CE owner, and the
audited whole-support conclusion supp(P) subset(-17/4,17/4). Its SAME
defect measure nu=W P/eta has y<=17/4 and eta*E[1/(c^2*y)]<=p0. All proof
parameters below are exact Fractions or integers, never floating values.
Floating time/working-set counters are operational guards only.

HG model: r_q(y)=sum_(n=0)^60 i^(n+3)*coeff_n*hhat_n + remainder,
hhat_0=1, hhat_n=(y/R)hhat_(n-1)+(n+1)*(c/R)^n,
coeff_0=q^3/6, coeff_n=coeff_(n-1)*(qR)/(n+3).
The pure-imaginary exponential Taylor integral remainder, integrated over
the HG simplex of volume1/6, is <=q^3/6*(qR)^61/61!. No exp(qR) factor is
needed: the Taylor path is real and exp(i*s) has modulus1. The two c knots
and one y knot lie in[0,R]. Negative tags conjugate the same real-coefficient
series, so their modulus bounds agree exactly.

Every interval uses SCALE=10^40 with lower floor / upper ceiling. Positive
term products are accumulated at SCALE^2 BEFORE coordinate rounding;
isqrt with an exact square comparison rounds the rectangle norm upward.
Root brackets for a,b come from isqrt of rational squares. An independent
degree60 outward exponential also encloses phi_Q for the old 1+|phi_Q| cap.

Magnitude nodes y=j/64,j=0..272; q=3(2j+1)/(2N),N=64 or512 only.
At each nearest-node half-cell add q^4/(64*48), subtract a LOWER penalty
lambda/[c_hi^2*(y+h/2)], and maximize over the bounded grid; NO tail cap.
lambda=q^3*tau, with11 exact rational tau. The resulting radius is the
minimum of the outward dual candidates and existing outward old caps.
A negative candidate is recorded as a conditional-model infeasibility
signal; this prototype retains the old radius, and does not declare n4
closed. No signed Prawitz response, physical quadrature, or CDF runs.

Cooperative resources:30s,256MiB,<=128KiB JSON, one BLAS thread requested
(BLAS/NumPy are not imported), streaming integer arrays. Source and each
N-specific receipt are new files; existing receipts are never overwritten.
"""

from __future__ import annotations

import argparse
import ctypes
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import time

for _thread_setting in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                        "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_thread_setting] = "1"

STARTED = time.monotonic()
SCALE = 10 ** 40
R = Fraction(17, 4)
STEP = Fraction(1, 64)
DEGREE = 60
TIME_LIMIT = 30
MEMORY_LIMIT = 256 * 1024 * 1024
OUTPUT_LIMIT = 128 * 1024
HERE = Path(__file__).resolve().parent
SUPPORT_NOTE = HERE / "first_critical_support_17_4_2026_10_01.md"
TAU = tuple(map(Fraction, ("0", "1/1000", "1/400", "1/200", "1/100", "1/50",
                           "1/25", "2/25", "4/25", "8/25", "16/25")))
CHARTS = ((Fraction(97, 100), Fraction(1633550843, 10796617633)),
          (Fraction(9, 10), Fraction(113089567, 365551652)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil_div(numerator, denominator):
    require(denominator > 0, "Positive rounding denominator")
    return -((-numerator) // denominator)


def floor_fraction_scaled(value):
    return value.numerator * SCALE // value.denominator


def ceil_fraction_scaled(value):
    return ceil_div(value.numerator * SCALE, value.denominator)


def fraction_interval(value):
    return floor_fraction_scaled(value), ceil_fraction_scaled(value)


def sqrt_fraction_interval(value):
    require(value > 0, "Positive root radicand")
    lower = math.isqrt(value.numerator * SCALE * SCALE // value.denominator)
    upper = lower if lower * lower * value.denominator == value.numerator * SCALE * SCALE else lower + 1
    require(lower * lower * value.denominator <= value.numerator * SCALE * SCALE,
            "Root lower square check")
    require(upper * upper * value.denominator >= value.numerator * SCALE * SCALE,
            "Root upper square check")
    return lower, upper


def positive_multiply(left, right):
    require(0 <= left[0] <= left[1] and 0 <= right[0] <= right[1], "Nonnegative interval product")
    return left[0] * right[0] // SCALE, ceil_div(left[1] * right[1], SCALE)


def rectangle_modulus_upper(rectangle):
    re_lower, re_upper, im_lower, im_upper = rectangle
    require(re_lower <= re_upper and im_lower <= im_upper, "Ordered complex rectangle")
    real_abs = max(abs(re_lower), abs(re_upper))
    imag_abs = max(abs(im_lower), abs(im_upper))
    square = real_abs * real_abs + imag_abs * imag_abs
    result = math.isqrt(square)
    return result if result * result == square else result + 1


def conjugate_rectangle(rectangle):
    return rectangle[0], rectangle[1], -rectangle[3], -rectangle[2]


def response_rectangle(coefficients, homogeneous):
    """All products below are exact integers at SCALE^2; round only once."""
    re_lo = re_hi = im_lo = im_hi = 0
    for n, (coefficient, h) in enumerate(zip(coefficients, homogeneous)):
        lower = coefficient[0] * h[0]
        upper = coefficient[1] * h[1]
        phase = (n + 3) % 4
        if phase == 0:
            re_lo += lower
            re_hi += upper
        elif phase == 1:
            im_lo += lower
            im_hi += upper
        elif phase == 2:
            re_lo -= upper
            re_hi -= lower
        else:
            im_lo -= upper
            im_hi -= lower
    return re_lo // SCALE, ceil_div(re_hi, SCALE), im_lo // SCALE, ceil_div(im_hi, SCALE)


def homogeneous_at_node(c_powers, node):
    y = fraction_interval(Fraction(node, 272))
    values = [(SCALE, SCALE)]
    for n in range(1, DEGREE + 1):
        multiplied = positive_multiply(y, values[-1])
        values.append((multiplied[0] + (n + 1) * c_powers[n][0],
                       multiplied[1] + (n + 1) * c_powers[n][1]))
    return values


def outward_exponential(q, c_interval, exp_remainder):
    argument = (c_interval[0] * q.numerator // q.denominator,
                ceil_div(c_interval[1] * q.numerator, q.denominator))
    coefficient = (SCALE, SCALE)
    re_lo = re_hi = SCALE
    im_lo = im_hi = 0
    for n in range(1, DEGREE + 1):
        coefficient = (coefficient[0] * argument[0] // (SCALE * n),
                       ceil_div(coefficient[1] * argument[1], SCALE * n))
        phase = n % 4
        if phase == 0:
            re_lo += coefficient[0]
            re_hi += coefficient[1]
        elif phase == 1:
            im_lo += coefficient[0]
            im_hi += coefficient[1]
        elif phase == 2:
            re_lo -= coefficient[1]
            re_hi -= coefficient[0]
        else:
            im_lo -= coefficient[1]
            im_hi -= coefficient[0]
    return (re_lo - exp_remainder, re_hi + exp_remainder,
            im_lo - exp_remainder, im_hi + exp_remainder)


def weighted_rectangle(value, rectangle):
    require(value >= 0, "Nonnegative Q3 weight")
    return tuple((component * value.numerator // value.denominator
                  if index % 2 == 0 else ceil_div(component * value.numerator, value.denominator))
                 for index, component in enumerate(rectangle))


def phi_q_modulus_upper(q, a, b, w, exp_remainder):
    negative = weighted_rectangle(w * Fraction(13, 20),
                                  conjugate_rectangle(outward_exponential(q, a, exp_remainder)))
    positive = weighted_rectangle(w * Fraction(7, 20), outward_exponential(q, b, exp_remainder))
    zero = fraction_interval(1 - w)
    rectangle = (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
                 negative[2] + positive[2], negative[3] + positive[3])
    # Q3 is an exact probability law, so its characteristic modulus<=1.
    return min(SCALE, rectangle_modulus_upper(rectangle))


def peak_bytes():
    if os.name != "nt":
        return None
    class Counters(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in (
                "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), ctypes.c_ulong]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    return int(counters.PeakWorkingSetSize) if psapi.GetProcessMemoryInfo(
        kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb) else None


def guard():
    require(time.monotonic() - STARTED < TIME_LIMIT, "Integer helper time budget")
    peak = peak_bytes()
    require(peak is None or peak <= MEMORY_LIMIT, "Integer helper working-set budget")


def frequency_data(n):
    data = []
    factorial_61 = math.factorial(61)
    for j in range(n):
        guard()
        q = Fraction(3 * (2 * j + 1), 2 * n)
        qr = fraction_interval(q * R)
        require(qr[0] == qr[1], "qR is exactly representable at this scale")
        coefficients = [fraction_interval(q ** 3 / 6)]
        for order in range(1, DEGREE + 1):
            previous = coefficients[-1]
            coefficients.append((previous[0] * qr[0] // (SCALE * (order + 3)),
                                 ceil_div(previous[1] * qr[1], SCALE * (order + 3))))
        exp_tail = (q * R) ** 61 / factorial_61
        data.append({"q": q, "coefficients": coefficients,
                     "exp_tail": ceil_fraction_scaled(exp_tail),
                     "HG_tail": ceil_fraction_scaled(q ** 3 * exp_tail / 6),
                     "mesh": ceil_fraction_scaled(q ** 4 * STEP / 48),
                     "lambdas": [q ** 3 * tau for tau in TAU]})
    return data


def verify_chart(w, eta, data):
    guard()
    p0 = 1 - w
    a_square, b_square = Fraction(7, 13) / w, Fraction(13, 7) / w
    a, b = sqrt_fraction_interval(a_square), sqrt_fraction_interval(b_square)
    require(a[1] < R * SCALE and b[1] < R * SCALE, "All true knots lie in[0,R]")
    maxima = [[None] * len(TAU) for _ in data]
    response_count = 0
    for label, c in (("negative_magnitude", a), ("positive_magnitude", b)):
        normalized = (c[0] * 4 // 17, ceil_div(c[1] * 4, 17))
        c_powers = [(SCALE, SCALE)]
        for order in range(1, DEGREE + 1):
            c_powers.append(positive_multiply(c_powers[-1], normalized))
        for node in range(273):
            guard()
            homogeneous = homogeneous_at_node(c_powers, node)
            # cost*S <= S^3*128/[c_hi^2*(2j+1)], and this is a LOWER
            # bound for 1/[c_true^2*y] throughout the nearest half-cell.
            cost_lower = SCALE ** 3 * 128 // (c[1] * c[1] * (2 * node + 1))
            for j, item in enumerate(data):
                rectangle = response_rectangle(item["coefficients"], homogeneous)
                conjugated = conjugate_rectangle(rectangle)
                require(max(abs(rectangle[2]), abs(rectangle[3]))
                        == max(abs(conjugated[2]), abs(conjugated[3])), "Exact sign conjugation check")
                response_upper = rectangle_modulus_upper(rectangle) + item["HG_tail"] + item["mesh"]
                for index, lam in enumerate(item["lambdas"]):
                    penalty_lower = cost_lower * lam.numerator // lam.denominator
                    upper = response_upper - penalty_lower
                    previous = maxima[j][index]
                    if previous is None or upper > previous:
                        maxima[j][index] = upper
                response_count += 1
    radii, old_radii, chosen_indices = [], [], []
    negative_signals = []
    for j, item in enumerate(data):
        guard()
        candidates = [ceil_fraction_scaled(lam * p0)
                      + ceil_div(eta.numerator * maxima[j][index], eta.denominator)
                      for index, lam in enumerate(item["lambdas"])]
        chosen = min(range(len(TAU)), key=lambda index: candidates[index])
        dual_upper = candidates[chosen]
        q = item["q"]
        g_upper = phi_q_modulus_upper(q, a, b, w, item["exp_tail"])
        old = min(SCALE + g_upper, ceil_fraction_scaled(eta * q ** 3 / 6),
                  ceil_fraction_scaled(Fraction(b[1], SCALE) ** 2 * p0 * q ** 2))
        if dual_upper < 0:
            negative_signals.append({"j": j, "negative_dual_upper_fixedpoint_integer": str(dual_upper)})
            radius = old
        else:
            radius = min(old, dual_upper)
        require(0 <= radius <= old, "Nonnegative radius not enlarged")
        radii.append(str(radius))
        old_radii.append(str(old))
        chosen_indices.append(chosen)
    return {
        "w_exact": str(w), "beta_magnitudes_covered_exact": ["3/10", "-3/10"],
        "eta_exact": str(eta), "p0_exact": str(p0),
        "a_square_exact": str(a_square), "b_square_exact": str(b_square),
        "a_bracket_fixedpoint_integers": list(map(str, a)),
        "b_bracket_fixedpoint_integers": list(map(str, b)),
        "radius_upper_fixedpoint_integers": radii,
        "old_radius_upper_fixedpoint_integers": old_radii,
        "chosen_tau_index": chosen_indices,
        "improved_frequency_count": sum(int(new) < int(old) for new, old in zip(radii, old_radii)),
        "response_node_frequency_count": response_count,
        "exact_sign_conjugation_checks": response_count,
        "negative_exact_candidate_infeasibility_signals": negative_signals,
        "negative_signal_policy": "Record conditional-model signal and retain old radius; no n4/CDF inference",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(64, 512), default=64)
    n = parser.parse_args().N
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(n) + ".json")
    require(not output.exists(), "Never overwrite an integer helper receipt")
    require(SUPPORT_NOTE.exists(), "Conditional structural boundary must be pinned")
    data = frequency_data(n)
    cases = [verify_chart(w, eta, data) for w, eta in CHARTS]
    guard()
    result = {
        "status": "INTEGER_OUTWARD_HELPER_BOUNDS",
        "date": "2026-10-08", "source_pins": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in (Path(__file__), SUPPORT_NOTE)},
        "scope": "Conditional owner-support Hermite response/modulus and per-frequency delta-radius upper bounds ONLY. No signed Prawitz budget, original-P frequency quadrature, continuumH or CDF acceptance is certified.",
        "explicit_conditional_boundary": "C3<CE; attained positively oriented closed maximizing pair with C4>=CE including equality; standardized P. Audited support note gives WHOLE CLOSED supp(P) subset(-17/4,17/4). Enlarge nu domain to closed endpoints. External Shevtsova/He--Cheng and equality-level project inputs are not proved by this program.",
        "analytical_model": "delta(q)=eta*integral r_q dnu; nu probability, y<=17/4, eta*integral1/(c^2*y)dnu<=p0. The dual constraints are necessary, not full owner/actual-law feasibility.",
        "integer_arithmetic": {"scale_exact": str(SCALE), "lower_rounding": "floor", "upper_rounding": "ceiling",
                               "complex_product_accumulation_scale": "SCALE^2, exact integer sums before rounding",
                               "modulus_rounding": "isqrt plus exact square check; then add absolute HG tail"},
        "frequency_grid_exact": {"N": n, "q_j": "3*(2*j+1)/(2*N)", "j_min": 0, "j_max": n - 1},
        "magnitude_grid_exact": {"R": "17/4", "step": "1/64", "y_j": "j/64", "j_min": 0, "j_max": 272},
        "HG_exponential_truncation_degree": DEGREE,
        "HG_remainder_exact_formula": "q^3/6*(q*R)^61/61!; pure-imaginary Taylor integral remainder and HG simplex volume1/6",
        "largest_HG_remainder_upper_fixedpoint_integer": str(max(item["HG_tail"] for item in data)),
        "normalized_complete_homogeneous_recurrence": "hhat0=1; hhat_n=(y/R)*hhat_(n-1)+(n+1)*(c/R)^n",
        "coefficient_recurrence_exact": "coeff0=q^3/6; coeff_n=coeff_(n-1)*(qR)/(n+3); phase i^(n+3), conjugate for negative tag",
        "dual_radius_formula": "lambda=q^3*tau. At each node use response_modulus_upper+q^4*h/48-lambda*cost_lower. Max over both c tags and bounded cells, no tail. Radius dual=lambda*p0+eta*max. Select any minimum candidate as an upper bound.",
        "cost_lower_exact_scaled_formula": "floor(SCALE^3*128/[c_hi_int^2*(2*y_index+1)])",
        "old_caps": "min(1+outward_abs_phi_Q,eta*q^3/6,b_hi^2*p0*q^2); reflection same modulus. phi_Q exponential degree60 with its own pure-imaginary remainder<= (qR)^61/61!.",
        "tau_exact_list": list(map(str, TAU)), "cases": cases,
        "summary": {"N": n, "chart_count": len(cases),
                    "improved_frequency_counts": [case["improved_frequency_count"] for case in cases],
                    "total_response_node_frequency_count": sum(case["response_node_frequency_count"] for case in cases),
                    "negative_exact_candidate_signal_count": sum(len(case["negative_exact_candidate_infeasibility_signals"]) for case in cases)},
        "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - STARTED,
                      "peak_working_set_bytes": peak_bytes(), "time_limit_seconds": TIME_LIMIT,
                      "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
                      "cooperative_not_OS_limit": True, "NumPy_or_BLAS_imported": False},
        "conclusions": {"integer_outward_helper_evaluation_completed": True,
                        "floating_values_used_as_proof_premises": False,
                        "all_real_frequency_intervals_certified": False,
                        "signed_common_curve_certified": False,
                        "physical_frequency_quadrature_certified": False,
                        "CDF_bound_proved": False, "unrestricted_n4_closed": False,
                        "new_cutoff": False, "old_receipts_modified": False},
    }
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Output budget")
    guard()
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)
    print(json.dumps({"status": result["status"], "result": str(output),
                      "output_bytes": len(raw.encode("utf-8")), "summary": result["summary"],
                      "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
