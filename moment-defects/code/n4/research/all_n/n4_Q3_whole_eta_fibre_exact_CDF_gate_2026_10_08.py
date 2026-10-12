"""Fresh exact WHOLE eta-fibre gate for ONE Q3 reference geometry.

Geometry w=9/10, |beta|=9/20, both orientations. This is not the whole
moment root and cannot close unrestricted C4. The actual-law standing
premises are an attained first-critical owner with |X|<17/4, rho<46/25,
and the structural/Prawitz/physical bridge inputs pinned below. No atom
bound is imposed on P. The eta cover is the enlarged closed interval
[0,46/25-rhoQ_LO]; the physical moment bound applies to actual laws only,
not to unrealizable numerical points on that outer interval.

Fresh affine dual radii are rebuilt in memory, never trusted from a JSON
table. Floating arithmetic in that module selects rational price indices
only. Generic Q3 probabilities here depend on the supplied beta, not on
the older beta=.3 point gate. All center/kernel/transfer/fibre acceptance
arithmetic is Fraction/integer outward. ABS transfer is independent of H,
so the upper reference center is maximized over both 229-point H grids
ONCE. A chosen affine radius is checked nonnegative on its entire eta cell.
Frozen-cap affine fourth-power majorants are then checked at both exact
endpoints. Refinement covers every closed cell, including eta=0.

ONE physical midpoint reserve 687/(8N^2) and H reserve19/32768 are added
to the raw center. The two physical tails are bounded by2/5. Strictly
negative target polynomials plus tails alone allow a conditional fibre
CDF assertion; any failed/gapped cell is UNKNOWN. No numerical optimizer
or receipt/status/source-pin trust can turn UNKNOWN into a proof.

60s cooperative process/256MiB, BLAS1, new exclusive receipt<=2MiB.
--replay-existing is read-only and repeats the fresh arithmetic.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import time

for _setting in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                 "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_setting] = "1"

STARTED = time.monotonic()
import n4_Q3_first_critical_integer_abs_Prawitz_gate_strict_v2_2026_10_08 as base
import n4_Q3_three_budget_exact_affine_radius_verifier_2026_10_08 as affine
import n4_eta_affine_transfer_bernstein_2026_10_08 as algebra

arith, S = base.arith, base.S
HERE = Path(__file__).resolve().parent
W, BETA, RHO_CAP = F(9, 10), F(9, 20), F(46, 25)
TARGET, R = F(256, 625), F(17, 4)
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 256 * 1024 * 1024, 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def guard():
    require(time.monotonic() - STARTED < TIME_LIMIT, "Whole eta gate time budget")
    peak = arith.peak_bytes()
    require(peak is None or peak <= MEMORY_LIMIT, "Whole eta gate memory budget")


def q3_rectangle(q, root):
    """Generic Q3, with exact masses w*(1+beta)/2 and w*(1-beta)/2."""
    require(type(q) is F and root["w"] == W and root["beta"] == BETA,
            "Generic exact geometry inputs")
    exp_tail = (q * R) ** 61 / math.factorial(61)
    negative = arith.weighted_rectangle(W * (1 + BETA) / 2,
        arith.conjugate_rectangle(arith.outward_exponential(q, root["a_bracket"], exp_tail)))
    positive = arith.weighted_rectangle(W * (1 - BETA) / 2,
        arith.outward_exponential(q, root["b_bracket"], exp_tail))
    zero = arith.fraction_interval(1 - W)
    return (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
            negative[2] + positive[2], negative[3] + positive[3])


def reference_center_and_frequency_blocks(verified, n, m):
    root = verified["root_data"]
    pi, phi0 = base.pi_and_phi0()
    blocks_positive, blocks_negative, frequencies = [], [], []
    for j, item in enumerate(verified["frequency_models"]):
        guard()
        q = item["q"]
        require(q == F(3 * (2 * j + 1), 2 * n), "Exact physical frequency grid")
        kernel = base.kernel_rectangle(F(2 * j + 1, 2 * n), n, m, pi)
        g = q3_rectangle(q, root)
        modulus = min(S, arith.rectangle_modulus_upper(g))
        weight = arith.rectangle_modulus_upper(kernel)
        g2 = base.complex_multiply(g, g)
        g4 = base.complex_multiply(g2, g2)
        conjugate = arith.conjugate_rectangle(g)
        negative2 = base.complex_multiply(conjugate, conjugate)
        negative4 = base.complex_multiply(negative2, negative2)
        blocks_positive.append(base.complex_multiply(kernel, g4))
        blocks_negative.append(base.complex_multiply(kernel, negative4))
        a = F(modulus, S)
        q3 = q ** 3
        models = []
        for k, model in enumerate(item["models"]):
            require(type(model["A"]) is F and type(model["S_upper_int"]) is int,
                    "Only fresh exact affine proof inputs")
            models.append((q3 * model["A"], q3 * F(model["S_upper_int"], S), "dual", k))
        # Each fallback is a valid radius on the whole feasible eta fibre.
        maximum_knot = F(max(root["a_bracket"][1], root["b_bracket"][1]), S)
        models.extend(((F(0), q3 / 6, "cube", -1),
                       (maximum_knot ** 2 * (1 - W) * q ** 2, F(0), "mass", -1),
                       (1 + a, F(0), "unit", -1)))
        frequencies.append({"q": q, "modulus": a, "weight": F(weight, S), "models": models})
    require(len(frequencies) == n, "Full frequency count")
    rows, normal_endpoint = [], None
    for h in base.H_GRID:
        guard()
        phase = base.exponential_exact_argument(-3 * h / (2 * n))
        ratio = base.exponential_exact_argument(-3 * h / n)
        positive = negative = 0
        for j in range(n):
            positive += base.complex_multiply(phase, blocks_positive[j])[1]
            negative += base.complex_multiply(phase, blocks_negative[j])[1]
            phase = base.unit_phase_intersection(base.complex_multiply(phase, ratio))
        normal = base.normal_cdf_interval(h / 2, phi0)
        if h == F(25, 8):
            normal_endpoint = normal
        for sign, center in ((1, positive), (-1, negative)):
            raw = S + 2 * center - 2 * normal[0]
            rows.append({"H_exact": str(h), "beta_orientation": sign, "raw_Q_upper_int": str(raw)})
    require(normal_endpoint is not None and 5 * normal_endpoint[0] > 4 * S,
            "Exact Gaussian positive-tail bound")
    maximum = max(int(row["raw_Q_upper_int"]) for row in rows)
    quad, hreserve = F(687, 8 * n * n), F(19, 32768)
    raw_constant = F(maximum, S) + quad + hreserve
    return frequencies, raw_constant, rows, {
        "max_raw_Q_upper_int": str(maximum),
        "ONE_original_P_midpoint_raw_exact": str(quad),
        "H_interpolation_raw_exact": str(hreserve),
        "raw_constant_upper_exact": str(raw_constant),
        "pi_bracket_ints": list(map(str, pi)), "phi0_bracket_ints": list(map(str, phi0)),
        "positive_tail_Phi_lower_int": str(normal_endpoint[0]),
    }


def choose_model(frequency, lower, upper):
    """Any valid model can be frozen; no optimizer continuity is assumed."""
    middle = (lower + upper) / 2
    allowed = [model for model in frequency["models"]
               if min(model[0] + model[1] * lower, model[0] + model[1] * upper) >= 0]
    require(allowed, "Cube fallback ensures a nonnegative whole-cell radius")
    return min(allowed, key=lambda model: model[0] + model[1] * middle)


def frozen_cell(frequencies, raw_constant, rho_q_lower, lower, upper):
    """Round both affine coefficients upward; eta>=0 makes this safe.

    Exact transfer functions are produced by the audited Fraction utility.
    Coefficient rounding reduces denominator growth in the frequency sum,
    and is not a pointwise numerical approximation. A signed slope is also
    ceiled, never clipped or rounded toward zero.
    """
    intercept_scale2 = slope_scale2 = 0
    choices, counts = [], {"dual": 0, "cube": 0, "mass": 0, "unit": 0, "endpoint": 0}
    for frequency in frequencies:
        A, B, kind, model_index = choose_model(frequency, lower, upper)
        a = frequency["modulus"]
        transfer = algebra.frozen_cap_linear_transfer(a, A, B, lower, upper)
        intercept, slope = transfer[0], transfer[1] if len(transfer) == 2 else F(0)
        p = min(F(1), a + max(A + B * lower, A + B * upper))
        endpoint = p ** 4 + a ** 4
        # A constant endpoint cap is usable on the whole cell only when it
        # is <= this affine majorant at BOTH endpoints.
        if endpoint <= min(intercept + slope * lower, intercept + slope * upper):
            intercept, slope = endpoint, F(0)
            counts["endpoint"] += 1
        weight_int = arith.ceil_fraction_scaled(frequency["weight"])
        require(weight_int >= 0, "Nonnegative kernel weight")
        # The unrounded E polynomial is nonnegative on the cell. The
        # rounded polynomial is pointwise larger there, hence also >=0,
        # so replacing the weight by an upper remains valid.
        intercept_scale2 += weight_int * arith.ceil_fraction_scaled(intercept)
        slope_scale2 += weight_int * arith.ceil_fraction_scaled(slope)
        choices.append((kind, model_index))
        counts[kind] += 1
    transfer_intercept = F(arith.ceil_div(intercept_scale2, S), S)
    transfer_slope = F(arith.ceil_div(slope_scale2, S), S)
    target = algebra.raw_target_for_transfers(raw_constant,
        [(F(1), (transfer_intercept, transfer_slope))], rho_q_lower, TARGET)
    passed, coefficients = algebra.bernstein_strict_negative(target, lower, upper, degree=1)
    raw_left = raw_constant + 2 * (transfer_intercept + transfer_slope * lower)
    raw_right = raw_constant + 2 * (transfer_intercept + transfer_slope * upper)
    scores = (raw_left / (rho_q_lower + lower), raw_right / (rho_q_lower + upper))
    # A ratio of affine functions with a positive denominator is monotone
    # or constant. Therefore the endpoint maximum covers the whole cell.
    # For a negative raw upper, replacing the true rhoQ by its LOWER
    # bracket does not upper-bound that negative quotient. Zero is a safe
    # score upper instead. Positive affine quotients have endpoint maxima.
    score_upper = max(F(0), *scores)
    choice_digest = hashlib.sha256(json.dumps(choices, separators=(",", ":")).encode("ascii")).hexdigest()
    return {"lower_exact": str(lower), "upper_exact": str(upper), "passed": passed,
            "target_Bernstein_coefficients_exact": list(map(str, coefficients)),
            "target_polynomial_exact": list(map(str, target)),
            "score_upper_int": str(arith.ceil_fraction_scaled(score_upper)),
            "selected_model_counts": counts, "selected_model_indices_sha256": choice_digest,
            "affine_radius_nonnegative_at_both_endpoints": True,
            "transfer_method": "frozen-cap affine majorant; optional whole-cell endpoint cap"}


def whole_fibre(frequencies, raw_constant, rho_q_lower, eta_max, initial_count, max_count):
    require(eta_max > 0 and 1 <= initial_count <= max_count <= 256, "Bounded complete fibre mesh")
    intervals = [(eta_max * F(j, initial_count), eta_max * F(j + 1, initial_count))
                 for j in range(initial_count)]
    rows = [frozen_cell(frequencies, raw_constant, rho_q_lower, L, U) for L, U in intervals]
    guard()
    while len(rows) < max_count:
        failures = [(int(row["score_upper_int"]), j) for j, row in enumerate(rows) if not row["passed"]]
        if not failures:
            break
        _, index = max(failures)
        L, U = intervals[index]
        middle = (L + U) / 2
        replacement = [(L, middle), (middle, U)]
        new_rows = [frozen_cell(frequencies, raw_constant, rho_q_lower, l, u) for l, u in replacement]
        intervals[index:index + 1] = replacement
        rows[index:index + 1] = new_rows
        guard()
    require(intervals[0][0] == 0 and intervals[-1][1] == eta_max, "Whole fibre endpoints")
    require(all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])), "No fibre gaps")
    passed = all(row["passed"] for row in rows)
    return rows, passed


def exact_model_digest(verified):
    value = [(str(item["q"]), [(str(model["A"]), str(model["S_upper_int"]), model["price_indices"])
             for model in item["models"]]) for item in verified["frequency_models"]]
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode("ascii")).hexdigest()


def exact_json_value(value):
    if type(value) is F:
        return str(value)
    raise TypeError("Unsupported receipt value: " + type(value).__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(64, 512), default=512)
    parser.add_argument("--kernel-M", type=int, choices=(16, 32), default=32)
    parser.add_argument("--initial-cells", type=int, choices=(64,), default=64)
    parser.add_argument("--max-cells", type=int, choices=(64, 128, 256), default=256)
    parser.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    n, m = args.N, args.kernel_M
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(n) + "_M" + str(m) + ".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a fibre receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay receipt exists")
    verified = affine.compute_verified_models(W, BETA, n, anchor_count=17, time_limit_seconds=45)
    guard()
    require(verified["status"] == "EXACT_AFFINE_DUAL_RADIUS_ENCLOSURES" and verified["scale"] == S,
            "Fresh affine arithmetic API")
    root = verified["root_data"]
    rho_q_lower = F(root["rhoQ_bracket"][0], S)
    eta_max = RHO_CAP - rho_q_lower
    require(rho_q_lower >= 1 and eta_max > 0, "Positive whole eta cover")
    frequencies, raw_constant, centers, center_details = reference_center_and_frequency_blocks(verified, n, m)
    rows, fibre_passed = whole_fibre(frequencies, raw_constant, rho_q_lower, eta_max,
                                    args.initial_cells, args.max_cells)
    tail_passed = F(2, 5) < TARGET
    passed = fibre_passed and tail_passed
    status = "EXACT_CONDITIONAL_WHOLE_ETA_FIBRE_CDF_BOUND" if passed else "UNKNOWN"
    entire_upper_int = max(arith.ceil_fraction_scaled(F(2, 5)), max(int(row["score_upper_int"]) for row in rows))
    inputs = (Path(__file__), Path(base.__file__), Path(arith.__file__), Path(affine.__file__),
              Path(algebra.__file__), base.SUPPORT_NOTE, base.PHYSICAL_BRIDGE)
    result = {
        "status": status, "date": "2026-10-08",
        "source_pins": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        "scale_exact": str(S), "N": n, "kernel_partial_fraction_M": m,
        "exact_geometry": {"w": str(W), "beta_orientations": [str(BETA), str(-BETA)],
                           "a_bracket_ints": list(map(str, root["a_bracket"])),
                           "b_bracket_ints": list(map(str, root["b_bracket"])),
                           "rhoQ_bracket_ints": list(map(str, root["rhoQ_bracket"])),
                           "rhoQ_lower_exact": str(rho_q_lower), "eta_cover_closed": ["0", str(eta_max)]},
        "definition": "Original standardized P. u=EX+=EX-,v+=EX+^2,v-=EX-^2,beta=v+-v-,w=u^2/(v+v-),eta=rho-rhoQ. No finite-atom reduction.",
        "external_proof_boundary": "C3<CE; equality-level attained positively oriented closed C4>=CE owner; published Shevtsova envelope, He--Cheng contact/Gaussian70, equality-level attainment, one-sided closed-CDF Prawitz, and pinned original-P quadrature/H bridge. These structural and analytic inputs are conditional premises, not consequences of source hashes.",
        "support_and_moment_premises": "Whole closed supp(P) subset(-17/4,17/4), rho<46/25. The enlarged numerical eta endpoint does NOT assert this physical moment bound for unrealizable parameter points; acceptance bounds all actual laws in this geometry satisfying the standing premises.",
        "fresh_radius_arithmetic": {"recomputed_in_memory": True, "numeric_JSON_tables_trusted": False,
                                    "affine_model_table_sha256": exact_model_digest(verified),
                                    "model_count": sum(len(item["models"]) for item in verified["frequency_models"]),
                                    "formula": "epsilon=q^3*(A+eta*Supper/scale), A exact Fraction, Supper signed outward integer. Models checked nonnegative on whole chosen eta cells; cube/mass/unit fallbacks always supplied.",
                                    "float_boundary": "Only rational price-index selection uses float; each chosen model freshly rebuilt by exact HG, tail, mesh and reciprocal penalties. No floating value is a proof premise.",
                                    "metadata": verified["verification_metadata"]},
        "reference_center": center_details, "reference_center_rows_both_orientations": centers,
        "reflection": "True conjugate of g is raised to the fourth power and integrated at the SAME H; no closed-CDF complement identity is assumed.",
        "whole_H": "All229 raw H nodes[-4,25/8] step1/32 for both beta signs; ONE physical original-P midpoint reserve and physical H interpolation cover frequency/H cells.",
        "eta_cell_cover": rows,
        "rounding_lemma": "Transfer affine coefficients each CEILED at scale. Since eta>=0 this increases the polynomial, including signed slopes. That polynomial is nonnegative on its cell, so kernel weight uppers preserve order. Product coefficients accumulated exactly at scale^2, then CEILED; target polynomial checked at both endpoints by degree1 Bernstein.",
        "tail_proof": "For actual original Z=S4/2 with mean0,var1: H<=-4 Cantelli gives F_Z<=1/5. For H>=25/8 exact Gaussian Phi(25/16)>4/5 and F_Z<=1. Each positive normalized tail<=2/(5rho)<=2/5<256/625. Reflection covers negative discrepancy via closed limits.",
        "summary": {"whole_eta_and_H_score_upper_int": str(entire_upper_int),
                    "whole_eta_and_H_score_upper_decimal": base.decimal_upper(entire_upper_int),
                    "target_exact": str(TARGET), "cell_count": len(rows),
                    "cells_not_strictly_below_target": sum(not row["passed"] for row in rows),
                    "closed_complete_eta_cover_verified": True,
                    "strict_margin_int": str(arith.floor_fraction_scaled(TARGET) - entire_upper_int)},
        "conclusions": {"integer_or_Fraction_outward_proof_arithmetic": True,
                        "floating_values_used_as_proof_premises": False,
                        "fresh_affine_radius_arithmetic_mandatory": True,
                        "conditional_whole_eta_fibre_CDF_bound": passed,
                        "both_beta_orientations_and_all_H_for_this_geometry": passed,
                        "full_w_beta_root_covered": False, "unrestricted_C4_proved": False,
                        "new_cutoff": False, "older_sources_or_receipts_modified": False},
        "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - STARTED,
                      "peak_working_set_bytes": arith.peak_bytes(), "time_limit_seconds": TIME_LIMIT,
                      "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
                      "cooperative_not_OS_limit": True},
    }
    guard()
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False, default=exact_json_value) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Fibre receipt output budget")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Replay receipt size")
        saved = json.loads(output.read_text(encoding="utf-8"))
        for field in ("status", "source_pins", "summary", "exact_geometry", "fresh_radius_arithmetic",
                      "reference_center", "reference_center_rows_both_orientations", "eta_cell_cover", "conclusions"):
            replay_value = json.loads(json.dumps(result[field], allow_nan=False, default=exact_json_value))
            require(saved[field] == replay_value, "Read-only exact fibre replay field: " + field)
        printed_status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        printed_status = status
    print(json.dumps({"status": printed_status, "result": str(output), "summary": result["summary"],
                      "resources": result["resources"], "output_bytes": len(raw.encode("utf-8"))}, sort_keys=True))


if __name__ == "__main__":
    main()
