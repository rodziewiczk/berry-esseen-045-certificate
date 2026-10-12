"""Strict v2: exact conditional ABS Prawitz gate for ONE fixed Q3 moment class.

External proof boundary: C3<CE; equality-level attained positive closed
C4>=CE owner; Shevtsova/He--Cheng structural support lemma; one-sided
closed-CDF Prawitz majorant; audited original-P physical quadrature and H
interpolation bridge. Pins retain those sources as mathematical inputs,
not axioms newly proved by this program. Owner |X|<17/4, rho<46/25.

Moment class ONLY: w=97/100, beta=+/-3/10,
eta=1633550843/10796617633, with the actual-law Q3 definitions. No finite
support/atom reduction of P is used. No w=.9 or full moment-root cover.

All proof arithmetic is exact integer/Fraction outward at scale10^40.
The radius table is source-pinned and parameter-checked, but those hashes
are integrity checks only. Fresh arithmetic recompute/replay of its w97
chart is mandatory. The gate consumes the freshly computed radii. An
in-memory forged-zero radius table retaining the original receipt status
and source pins is rejected by the same exact comparison. Kernel cot partial fractions
use exact tails [1/(M+1),(2M+1)/(2M(M+1))]. Pi is Machin alternating atan.
Q3 exponentials and phases use degree60 imaginary Taylor remainders.
Phi uses the exact degree60 integrated Gaussian Taylor remainder.
Phase0=exp(-i3H/(2N)), ratio=exp(-i3H/N); arithmetic recurrence covers
all q_j instead of recomputing every phase exponential.

Gate includes both reflections at all229 H in[-4,25/8], raw physical
reserve687/(8N^2), raw H interpolation19/32768, and closed-CDF tails.
PASS is allowed only if every exact outward score is strictly<256/625.
Otherwise status UNKNOWN. This never proves unrestricted C4 or all-n.

Resources:45s,256MiB,one BLAS thread (no BLAS/NumPy imported),128KiB JSON.
No optimizer/build or older gate runs. New receipts are exclusive; the
read-only --replay-existing option checks an existing receipt in memory.
"""

from __future__ import annotations

import argparse
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
import n4_Q3_first_critical_integer_response_radius_verifier_2026_10_08 as arith

S = arith.SCALE
HERE = Path(__file__).resolve().parent
SUPPORT_NOTE = HERE / "first_critical_support_17_4_2026_10_01.md"
PHYSICAL_BRIDGE = HERE / "n4_first_critical_physical_quadrature_bridge_2026_10_08.md"
W = Fraction(97, 100)
ETA = Fraction(1633550843, 10796617633)
BETA = Fraction(3, 10)
TARGET = Fraction(256, 625)
H_GRID = tuple(Fraction(-4) + Fraction(j, 32) for j in range(229))
TIME_LIMIT = 45
MEMORY_LIMIT = 256 * 1024 * 1024
OUTPUT_LIMIT = 128 * 1024
EXP_DEGREE = 60
GAUSSIAN_DEGREE = 60


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def guard():
    require(time.monotonic() - STARTED < TIME_LIMIT, "ABS gate time budget")
    peak = arith.peak_bytes()
    require(peak is None or peak <= MEMORY_LIMIT, "ABS gate working-set budget")


def complex_multiply(left, right):
    a, b, c, d = left
    e, f, g, h = right
    real_first = (a * e, a * f, b * e, b * f)
    real_second = (c * g, c * h, d * g, d * h)
    imag_first = (a * g, a * h, b * g, b * h)
    imag_second = (c * e, c * f, d * e, d * f)
    return ((min(real_first) - max(real_second)) // S,
            arith.ceil_div(max(real_first) - min(real_second), S),
            (min(imag_first) + min(imag_second)) // S,
            arith.ceil_div(max(imag_first) + max(imag_second), S))


def unit_phase_intersection(rectangle):
    result = (max(-S, rectangle[0]), min(S, rectangle[1]),
              max(-S, rectangle[2]), min(S, rectangle[3]))
    require(result[0] <= result[1] and result[2] <= result[3], "Nonempty unit phase enclosure")
    return result


def exponential_exact_argument(argument):
    magnitude = abs(argument)
    interval = arith.fraction_interval(magnitude)
    coefficient = (S, S)
    re_lo = re_hi = S
    im_lo = im_hi = 0
    for degree in range(1, EXP_DEGREE + 1):
        coefficient = (coefficient[0] * interval[0] // (S * degree),
                       arith.ceil_div(coefficient[1] * interval[1], S * degree))
        phase = degree % 4
        if phase == 0:
            re_lo += coefficient[0]; re_hi += coefficient[1]
        elif phase == 1:
            im_lo += coefficient[0]; im_hi += coefficient[1]
        elif phase == 2:
            re_lo -= coefficient[1]; re_hi -= coefficient[0]
        else:
            im_lo -= coefficient[1]; im_hi -= coefficient[0]
    remainder = arith.ceil_fraction_scaled(magnitude ** 61 / math.factorial(61))
    result = (re_lo - remainder, re_hi + remainder, im_lo - remainder, im_hi + remainder)
    if argument < 0:
        result = arith.conjugate_rectangle(result)
    return unit_phase_intersection(result)


def atan_inverse_bracket(denominator, terms):
    partial = sum((Fraction((-1) ** j, (2 * j + 1) * denominator ** (2 * j + 1))
                   for j in range(terms)), Fraction(0))
    next_term = Fraction(1, (2 * terms + 1) * denominator ** (2 * terms + 1))
    return ((partial, partial + next_term) if terms % 2 == 0
            else (partial - next_term, partial))


def pi_and_phi0():
    a_lo, a_hi = atan_inverse_bracket(5, 64)
    b_lo, b_hi = atan_inverse_bracket(239, 16)
    pi_exact_lo, pi_exact_hi = 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo
    pi = (arith.floor_fraction_scaled(pi_exact_lo), arith.ceil_fraction_scaled(pi_exact_hi))
    root_lo = arith.sqrt_fraction_interval(Fraction(2 * pi[0], S))[0]
    root_hi = arith.sqrt_fraction_interval(Fraction(2 * pi[1], S))[1]
    phi0 = (S * S // root_hi, arith.ceil_div(S * S, root_lo))
    require(phi0[0] * 8 >= 3 * S, "Gaussian normalization lower bound")
    return pi, phi0


def normal_cdf_interval(x, phi0):
    y = abs(x)
    require(y <= 2, "Approved Gaussian Taylor domain")
    partial = sum((Fraction((-1) ** degree) * y ** (2 * degree + 1)
                   / (2 ** degree * math.factorial(degree) * (2 * degree + 1))
                   for degree in range(GAUSSIAN_DEGREE + 1)), Fraction(0))
    order = GAUSSIAN_DEGREE + 1
    remainder = y ** (2 * order + 1) / (2 ** order * math.factorial(order) * (2 * order + 1))
    integral = (max(0, arith.floor_fraction_scaled(partial - remainder)),
                arith.ceil_fraction_scaled(partial + remainder))
    require(0 <= integral[0] <= integral[1], "Gaussian integral order")
    product = (phi0[0] * integral[0] // S, arith.ceil_div(phi0[1] * integral[1], S))
    return ((S // 2 + product[0], S // 2 + product[1]) if x >= 0
            else (S // 2 - product[1], S // 2 - product[0]))


def kernel_rectangle(u, n, m, pi):
    finite = sum((Fraction(1, 1) / (j * j - u * u) for j in range(1, m + 1)), Fraction(0))
    tail_lo = Fraction(1, m + 1)
    tail_hi = Fraction(2 * m + 1, 2 * m * (m + 1))
    coefficient = 2 * u * (1 - u)
    numerator_lo = 1 / u - coefficient * (finite + tail_hi)
    numerator_hi = 1 / u - coefficient * (finite + tail_lo)
    pi_lo, pi_hi = Fraction(pi[0], S), Fraction(pi[1], S)
    candidates = (numerator_lo / pi_lo, numerator_lo / pi_hi,
                  numerator_hi / pi_lo, numerator_hi / pi_hi)
    r_lo, r_hi = min(candidates), max(candidates)
    real = arith.fraction_interval((1 - u) / n)
    imag = (arith.floor_fraction_scaled(r_lo / n), arith.ceil_fraction_scaled(r_hi / n))
    return real[0], real[1], imag[0], imag[1]


def q3_characteristic_rectangle(q, a, b, exp_remainder):
    negative = arith.weighted_rectangle(W * Fraction(13, 20),
        arith.conjugate_rectangle(arith.outward_exponential(q, a, exp_remainder)))
    positive = arith.weighted_rectangle(W * Fraction(7, 20), arith.outward_exponential(q, b, exp_remainder))
    zero = arith.fraction_interval(1 - W)
    return (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
            negative[2] + positive[2], negative[3] + positive[3])


def quartic_absolute_upper(epsilon, modulus):
    p = min(S, modulus + epsilon)
    telescope = arith.ceil_div(epsilon * (p ** 3 + p * p * modulus
                                         + p * modulus * modulus + modulus ** 3), S ** 3)
    endpoint = arith.ceil_div(p ** 4 + modulus ** 4, S ** 3)
    return min(telescope, endpoint)


def score_upper(raw_upper, rho_interval):
    denominator = rho_interval[0] if raw_upper >= 0 else rho_interval[1]
    return arith.ceil_div(raw_upper * S, denominator)


def decimal_upper(integer):
    sign = "-" if integer < 0 else ""
    value = abs(integer)
    return sign + str(value // S) + "." + str(value % S).zfill(40)


def require_fresh_radius_equal(saved_case, recomputed_case):
    """Numeric receipt data are not a mathematical premise."""
    require(saved_case == recomputed_case, "Fresh exact helper replay must match all chart fields")


def validated_radius(n, mode):
    require(mode == "recompute-replay", "Strict v2 permits only fresh arithmetic recompute/replay")
    receipt = HERE / (Path(arith.__file__).stem + "_N" + str(n) + ".json")
    require(receipt.stat().st_size <= OUTPUT_LIMIT, "Radius receipt size bound")
    saved = json.loads(receipt.read_text(encoding="utf-8"))
    source_hash = hashlib.sha256(Path(arith.__file__).read_bytes()).hexdigest()
    require(saved["status"] == "INTEGER_OUTWARD_HELPER_BOUNDS", "Outward helper status")
    require(saved["source_pins"][Path(arith.__file__).name] == source_hash, "Radius source pin")
    require(saved["source_pins"][SUPPORT_NOTE.name] == hashlib.sha256(SUPPORT_NOTE.read_bytes()).hexdigest(),
            "Radius structural source pin")
    require(saved["integer_arithmetic"]["scale_exact"] == str(S), "Radius scale")
    require(saved["frequency_grid_exact"]["N"] == n, "Radius frequency count")
    require(saved["magnitude_grid_exact"]["R"] == "17/4" and saved["magnitude_grid_exact"]["step"] == "1/64",
            "Radius owner domain and mesh")
    require(saved["HG_exponential_truncation_degree"] == 60, "Radius truncation")
    case = next(item for item in saved["cases"] if item["w_exact"] == str(W))
    require(case["eta_exact"] == str(ETA) and case["beta_magnitudes_covered_exact"] == ["3/10", "-3/10"],
            "Exact moment class and reflection")
    data = arith.frequency_data(n)
    recomputed = arith.verify_chart(W, ETA, data)
    require_fresh_radius_equal(case, recomputed)
    # Lightweight tamper regression: all integrity metadata have already
    # passed above. Change only the selected numeric radius table in memory.
    # The same actual verification comparison must reject it.
    forged = dict(case)
    forged["radius_upper_fixedpoint_integers"] = ["0"] * n
    tamper_rejected = False
    try:
        require_fresh_radius_equal(forged, recomputed)
    except RuntimeError:
        tamper_rejected = True
    require(tamper_rejected, "Forged zero radii with unchanged integrity metadata must be rejected")
    tamper_record = {
        "forged_zero_radius_table_rejected": True,
        "receipt_status_and_source_pins_unchanged": True,
        "same_arithmetic_comparison_as_proof_path": True,
        "in_memory_only_no_file_modified": True,
    }
    # Mathematical input comes from fresh arithmetic, never a trusted
    # numerical table/status/hash in the saved JSON.
    return receipt, recomputed, data, tamper_record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(64, 512), default=512)
    parser.add_argument("--kernel-M", type=int, choices=(16, 32), default=32)
    parser.add_argument("--radius-mode", choices=("recompute-replay",), default="recompute-replay")
    parser.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    n, m = args.N, args.kernel_M
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(n) + "_M" + str(m) + ".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a gate receipt")
    require(not args.replay_existing or output.exists(), "Replay receipt exists")
    radius_path, radius_case, data, tamper_record = validated_radius(n, args.radius_mode)
    guard()
    a = tuple(map(int, radius_case["a_bracket_fixedpoint_integers"]))
    b = tuple(map(int, radius_case["b_bracket_fixedpoint_integers"]))
    epsilon = list(map(int, radius_case["radius_upper_fixedpoint_integers"]))
    require(len(epsilon) == n, "Radius table length")
    rho_q = arith.sqrt_fraction_interval(Fraction(11881, 9100) / W)
    eta_interval = arith.fraction_interval(ETA)
    rho = (rho_q[0] + eta_interval[0], rho_q[1] + eta_interval[1])
    require(rho[0] >= S and rho[1] * 25 < 46 * S, "Physical moment regime")
    pi, phi0 = pi_and_phi0()
    blocks_positive, blocks_negative = [], []
    transfer_sum_scale2 = 0
    for j, item in enumerate(data):
        guard()
        q = item["q"]
        u = Fraction(2 * j + 1, 2 * n)
        kernel = kernel_rectangle(u, n, m, pi)
        g = q3_characteristic_rectangle(q, a, b, item["exp_tail"])
        modulus = min(S, arith.rectangle_modulus_upper(g))
        delta4 = quartic_absolute_upper(epsilon[j], modulus)
        weight = arith.rectangle_modulus_upper(kernel)
        transfer_sum_scale2 += weight * delta4
        g2 = complex_multiply(g, g)
        g4 = complex_multiply(g2, g2)
        conjugate_g = arith.conjugate_rectangle(g)
        negative_g2 = complex_multiply(conjugate_g, conjugate_g)
        negative_g4 = complex_multiply(negative_g2, negative_g2)
        blocks_positive.append(complex_multiply(kernel, g4))
        blocks_negative.append(complex_multiply(kernel, negative_g4))
    transfer_upper = arith.ceil_div(transfer_sum_scale2, S)
    quad_raw = arith.ceil_fraction_scaled(Fraction(687, 8 * n * n))
    h_raw = arith.ceil_fraction_scaled(Fraction(19, 32768))
    rows_positive, rows_negative = [], []
    normal_endpoint = None
    for h in H_GRID:
        guard()
        phase = exponential_exact_argument(-Fraction(3) * h / (2 * n))
        ratio = exponential_exact_argument(-Fraction(3) * h / n)
        positive_upper = negative_upper = 0
        for j in range(n):
            positive_upper += complex_multiply(phase, blocks_positive[j])[1]
            negative_upper += complex_multiply(phase, blocks_negative[j])[1]
            phase = unit_phase_intersection(complex_multiply(phase, ratio))
        normal = normal_cdf_interval(h / 2, phi0)
        if h == Fraction(25, 8):
            normal_endpoint = normal
        for coefficient_upper, rows in ((positive_upper, rows_positive), (negative_upper, rows_negative)):
            raw = S + 2 * coefficient_upper - 2 * normal[0] + 2 * transfer_upper + quad_raw + h_raw
            bound = score_upper(raw, rho)
            rows.append({"H_exact": str(h), "raw_upper_int": str(raw),
                         "score_upper_int": str(bound), "negative_raw_uses_rho_hi": raw < 0})
    require(normal_endpoint is not None and 5 * normal_endpoint[0] > 4 * S,
            "Exact positive-tail Gaussian lower bound Phi(25/16)>4/5")
    # For H<=-4 use Cantelli F_Z(H/2)<=1/5; for H>=25/8 use
    # F_Z<=1 and the just-certified Phi boundary. Both give2/(5rho).
    tail_upper = arith.ceil_div(2 * S * S, 5 * rho[0])
    all_rows = rows_positive + rows_negative
    worst = max(int(row["score_upper_int"]) for row in all_rows)
    entire_upper = max(worst, tail_upper)
    target_scaled = arith.floor_fraction_scaled(TARGET)
    require(arith.ceil_fraction_scaled(TARGET) == target_scaled, "Exact target representation")
    passed = entire_upper < target_scaled
    status = "EXACT_CONDITIONAL_MOMENT_CLASS_CDF_BOUND" if passed else "UNKNOWN"
    inputs = (Path(__file__), Path(arith.__file__), radius_path, SUPPORT_NOTE, PHYSICAL_BRIDGE)
    require(all(path.exists() for path in inputs), "Pinned mathematical inputs exist")
    result = {
        "status": status, "date": "2026-10-08",
        "source_pins": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
        "exact_moment_class": {"w": str(W), "beta": [str(BETA), str(-BETA)], "eta": str(ETA),
                               "definitions": "u=EX+=EX-,v+=EX+^2,v-=EX-^2; beta=v+-v-,w=u^2/(v+v-),eta=rho-(v+^2+v-^2)/u. Standardized original P, no atom bound.",
                               "rho_interval_fixedpoint_integers": list(map(str, rho))},
        "explicit_external_proof_boundary": "C3<CE and an attained positively oriented closed C4>=CE owner, equality included. He--Cheng contact/Gaussian, Shevtsova iid envelope, equality-level attainment, one-sided closed-CDF Prawitz, and the pinned original-P quadrature/H bridge supply the conditional structural/analytic inputs.",
        "support_used_conditionally": "Whole closed supp(P) subset(-17/4,17/4); nu domain enlarged to closed endpoints. rho<46/25.",
        "scale_exact": str(S), "N": n, "kernel_partial_fraction_M": m,
        "kernel_exact_model": "R(u)=1/pi*[1/u-2u(1-u)*sum_(k>=1)1/(k^2-u^2)]; tail in[1/(M+1),(2M+1)/(2M(M+1))]. Divide signed numerator interval by positive pi interval using all endpoint quotients.",
        "pi_enclosure_fixedpoint_integers": list(map(str, pi)),
        "pi_model": "16atan(1/5)-4atan(1/239);64 and16 alternating terms with explicit next-term remainder.",
        "phi0_enclosure_fixedpoint_integers": list(map(str, phi0)),
        "Gaussian_model": "Phi(x)=1/2+phi0*integral_0^x exp(-t^2/2)dt, |x|<=2. Degree60 integrated Taylor, remainder<=|x|^123/[2^61*61!*123].",
        "phase_model": "phase0=exp(-i3H/(2N)),ratio=exp(-i3H/N); outward recurrence over all q_j. Degree60 pure-imaginary Taylor remainder; unit-coordinate intersection is valid.",
        "reflection_model": "Recompute kernel*g_conjugate^4 at the SAME H and phase, not a closed-J complement.",
        "radius_verification_mode": args.radius_mode,
        "radius_fresh_recompute_replay_passed": True,
        "radius_tamper_regression": tamper_record,
        "radius_proof_API": "Strict v2: receipt-only numerical trust mode does not exist; fresh arithmetic is mandatory even through direct API calls. Saved status/hashes are integrity checks, not radius premises.",
        "absolute_transfer_J_upper_fixedpoint_integer": str(transfer_upper),
        "absolute_transfer_formula": "Sum |kappa|*min(epsilon*(p^3+p^2*a+p*a^2+a^3),p^4+a^4), a=outward|g| capped1,p=min1,a+epsilon. Positive products summed atscale^2 before upper rounding.",
        "physical_reserves_raw_fixedpoint_integers": {"ONE_original_P_midpoint_687_over_8N2": str(quad_raw),
                                                     "H_interpolation_19_over_32768": str(h_raw)},
        "tail_proof": "H<=-4: Cantelli for original Z with mean0,var1 gives F_Z<=1/5. H>=25/8: certified Phi(25/16)>4/5 and F_Z<=1. Both positive normalized tails<=2/(5rho). Reflection handles the negative discrepancy with closed-CDF limits.",
        "positive_tail_Phi_lower_fixedpoint_integer": str(normal_endpoint[0]),
        "tail_score_upper_fixedpoint_integer": str(tail_upper),
        "whole_H_interval": "[-4,25/8], all229 rawHnodes at1/32; physical interpolation reserve handles intervals, not a nonsmooth numerical minimum.",
        "positive_beta_rows": rows_positive, "negative_beta_rows": rows_negative,
        "summary": {"all_H_score_upper_fixedpoint_integer": str(entire_upper),
                    "all_H_score_upper_decimal": decimal_upper(entire_upper),
                    "target_exact": str(TARGET), "strict_margin_fixedpoint_integer": str(target_scaled - entire_upper),
                    "central_nodes_count_both_orientations": len(all_rows),
                    "central_nodes_not_strictly_below_target": sum(int(row["score_upper_int"]) >= target_scaled for row in all_rows),
                    "negative_raw_node_count": sum(row["negative_raw_uses_rho_hi"] for row in all_rows)},
        "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - STARTED,
                      "peak_working_set_bytes": arith.peak_bytes(), "time_limit_seconds": TIME_LIMIT,
                      "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
                      "NumPy_or_BLAS_imported": False, "cooperative_not_OS_limit": True},
        "conclusions": {"proof_arithmetic_integer_or_Fraction_outward": True,
                        "floating_values_used_as_proof_premises": False,
                        "fresh_arithmetic_radius_replay_mandatory": True,
                        "forged_zero_radius_receipt_rejected": True,
                        "specified_conditional_moment_class_CDF_bound": passed,
                        "whole_H_and_both_reflections_covered_for_this_class": passed,
                        "unrestricted_C4_proved": False, "full_moment_root_covered": False,
                        "new_cutoff": False, "older_receipts_modified": False},
    }
    guard()
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Receipt output budget")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Existing receipt size")
        saved = json.loads(output.read_text(encoding="utf-8"))
        for field in ("status", "source_pins", "summary", "positive_beta_rows", "negative_beta_rows",
                      "absolute_transfer_J_upper_fixedpoint_integer", "tail_score_upper_fixedpoint_integer",
                      "radius_tamper_regression", "radius_proof_API"):
            require(saved[field] == result[field], "Exact gate replay field: " + field)
        printed_status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        printed_status = status
    print(json.dumps({"status": printed_status, "result": str(output),
                      "output_bytes": len(raw.encode("utf-8")), "summary": result["summary"],
                      "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()


