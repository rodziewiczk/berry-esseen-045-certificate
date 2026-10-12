"""Fresh exact box radius V2: intersect interval-HG and knot-Lipschitz bounds.

Preserves V1 sources/receipts. At every node/q, freshly compute both the
whole-box c-interval HG rectangle and the exact nominal-c HG rectangle.
The physical-knot difference is at most
Delta=max(cnom_hi-cbox_lo,cbox_hi-cnom_lo)/SCALE.
HG gives |partial_c r_q|<=q^4/12 because the two repeated c knots have
simplex weight integral1/12. Therefore a second uniform response upper is
nominal_rectangle_norm_up+HG_tail_up+q^4*Delta/12+q^4*h/48.
Take its minimum with full-c HG upper. BOTH upper bounds are exact.

All inverse-size costs and signed pole maxima STILL use the entire closed
box c intervals. Float search selects rational indices at the exact nominal
point only; no float numerical bound crosses into the verification.
Same public compute_verified_box_models API as V1. No CDF/global cover.
Cooperative60s/256MiB, BLAS1, fresh replay, exclusive receipt<=2MiB.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import time

for _thread_setting in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                        "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_thread_setting] = "1"

import n4_Q3_three_budget_exact_box_affine_radius_verifier_2026_10_08 as box

point = box.point
SCALE, RADIUS, STEP = box.SCALE, box.RADIUS, box.STEP
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60.0, box.MEMORY_LIMIT, box.OUTPUT_LIMIT


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalized_powers(c):
    normalized = (c[0] * 4 // 17, point.ceil_div(c[1] * 4, 17))
    powers = [(SCALE, SCALE)]
    for order in range(1, point.DEGREE + 1):
        powers.append(point.integer.positive_multiply(powers[-1], normalized))
    return powers


def verify_sharpened_tag(c_box, c_nominal, table, data, wanted, guard):
    require(c_box[0] <= c_nominal[0] <= c_nominal[1] <= c_box[1], "Nominal true knot within entire box")
    delta_int = max(c_nominal[1] - c_box[0], c_box[1] - c_nominal[0])
    delta = F(delta_int, SCALE)
    require(delta >= 0, "Nonnegative physical knot variation upper")
    box_powers, nominal_powers = normalized_powers(c_box), normalized_powers(c_nominal)
    costs, penalties, contact_counts = table
    all_keys = sorted(set(key for keys in wanted for key in keys))
    offsets = {key: [penalties[node][key[1]] - costs[node] * point.TAUS[key[0]].numerator // point.TAUS[key[0]].denominator
                     for node in range(273)] for key in all_keys}
    margins = [point.ceil_scaled(item["q"] ** 4 * delta / 12) for item in data]
    maxima = [{key: None for key in keys} for keys in wanted]
    checks = sharpened = maximum_gain = 0
    for node in range(273):
        guard()
        homogeneous_box = point.integer.homogeneous_at_node(box_powers, node)
        homogeneous_nominal = point.integer.homogeneous_at_node(nominal_powers, node)
        for j, item in enumerate(data):
            rectangle_box = point.integer.response_rectangle(item["coefficients"], homogeneous_box)
            rectangle_nominal = point.integer.response_rectangle(item["coefficients"], homogeneous_nominal)
            norm_box = point.integer.rectangle_modulus_upper(rectangle_box)
            norm_nominal_plus_knot = point.integer.rectangle_modulus_upper(rectangle_nominal) + margins[j]
            # The same valid HG remainder and y half-cell mesh are added ONCE
            # after taking the min of two independent polynomial-based uppers.
            gain = max(0, norm_box - norm_nominal_plus_knot)
            sharpened += gain > 0
            maximum_gain = max(maximum_gain, gain)
            response = min(norm_box, norm_nominal_plus_knot) + item["HG_tail"] + item["mesh"]
            q = item["q"]
            normalized_upper = point.ceil_div(response * q.denominator ** 3, q.numerator ** 3)
            for key in wanted[j]:
                value = normalized_upper + offsets[key][node]
                if maxima[j][key] is None or value > maxima[j][key]:
                    maxima[j][key] = value
            checks += 1
    require(all(value is not None for row in maxima for value in row.values()), "Every selected box tag candidate freshly checked at every node/q")
    return maxima, {"node_frequency_response_count": checks, "unique_tag_price_pairs": len(all_keys),
                    "contact_cell_counts": contact_counts, "HG_interval_c_enclosure_used": True,
                    "fresh_nominal_HG_enclosure_used": True, "physical_delta_c_upper": delta,
                    "HG_knot_derivative_bound": "|partial_c r_q|<=q^4/12 from two HG c knots",
                    "node_frequency_bounds_sharpened": sharpened,
                    "largest_raw_response_upper_gain_fixedpoint_integer": maximum_gain}


def compute_verified_box_models(w_lo, w_hi, beta_lo, beta_hi, N, anchor_count=17,
                                time_limit_seconds=TIME_LIMIT):
    """Fresh V2 replay; never consume a saved table as a proof premise."""
    started = time.monotonic()
    require(N in (64, 512) and anchor_count in (17, 33), "Fixed exact frequency and search grids")
    require(0 < time_limit_seconds <= TIME_LIMIT, "Cooperative time limit<=60s")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Exact V2 box radius elapsed budget")
        peak = point.integer.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Exact V2 box radius working-set budget")
    root = box.box_root_data(w_lo, w_hi, beta_lo, beta_hi)
    nominal = root["nominal_root_data"]
    nominal_tables = {name: point.cell_tables(nominal[name + "_bracket"], guard) for name in ("a", "b")}
    selected, search_metadata = point.float_search_seeds(nominal, N, anchor_count, nominal_tables, guard)
    del nominal_tables
    box_tables = {name: point.cell_tables(root[name + "_bracket"], guard) for name in ("a", "b")}
    data = point.frequency_data(N, guard)
    plus_wanted = [sorted(set((it, ip) for it, ip, im in row)) for row in selected]
    minus_wanted = [sorted(set((it, im) for it, ip, im in row)) for row in selected]
    plus, plus_metadata = verify_sharpened_tag(root["b_bracket"], nominal["b_bracket"], box_tables["b"], data, plus_wanted, guard)
    minus, minus_metadata = verify_sharpened_tag(root["a_bracket"], nominal["a_bracket"], box_tables["a"], data, minus_wanted, guard)
    frequency_models = []
    for j, tuples in enumerate(selected):
        models = []
        for it, ip, im in tuples:
            tau = point.TAUS[it]
            zp, xp = point.PAIRS[ip]
            zm, xm = point.PAIRS[im]
            require(tau >= 0 and zp >= 0 and zm >= 0, "Nonnegative inequality prices")
            A = root["p0_hi"] * tau + root["u_hi"] * (zp + zm)
            S = max(plus[j][(it, ip)], minus[j][(it, im)])
            models.append({"A": A, "A_upper_int": point.ceil_scaled(A), "S_upper_int": S,
                           "price_indices": (it, ip, im)})
        frequency_models.append({"q": data[j]["q"], "models": models})
    guard()
    source_paths = (Path(__file__), Path(box.__file__), Path(point.__file__),
                    Path(point.integer.__file__), point.integer.SUPPORT_NOTE)
    return {"status": "EXACT_BOX_AFFINE_DUAL_RADIUS_ENCLOSURES", "variant": "V2_HG_KNOT_LIPSCHITZ_INTERSECTION",
            "scale": SCALE, "N": N, "root_data": root, "nominal_root_data": nominal,
            "nominal_probabilities": root["nominal_probabilities"], "frequency_models": frequency_models,
            "prices": {"tau": point.TAUS, "pairs": point.PAIRS}, "search_metadata": search_metadata,
            "verification_metadata": {"positive_tag": plus_metadata, "negative_tag": minus_metadata,
                                      "HG_degree": point.DEGREE, "R": RADIUS, "y_step": STEP,
                                      "HG_tail": "q^3/6*(qR)^61/61!", "raw_mesh": "q^4*h/48",
                                      "delta_c": "max(cnom_hi-cbox_lo,cbox_hi-cnom_lo)/SCALE; physical not R-normalized",
                                      "response_intersection": "min(full_c_HG_rectangle_modulus_up,nominal_HG_rectangle_modulus_up+ceil_SCALE(q^4*Delta_c/12))+HG_tail_up+mesh_up",
                                      "HG_derivative_proof": "r_q=(iq)^3*integral_D exp(iq[theta1*c+theta2*c+theta3*y])dtheta. Differentiate the TWO c knots: |partial_c r_q|<=q^4*integral_D(theta1+theta2)=q^4/12.",
                                      "cost": "Unchanged fullbox floor_SCALE[1/(c_box_hi^2*y_cell_hi)]",
                                      "pole": "Unchanged fullbox exact Fraction signed concave sup on one interval/ray or TWO reciprocal rays, then CEIL_SCALE",
                                      "intercept": "A_box=p0_hi*tau+u_hi*(zeta_plus+zeta_minus)",
                                      "model": "|delta(q)|<=q^3*(A_box+eta*S_box_upper_int/SCALE), whole box/every feasible eta>=0",
                                      "nominal_float_values_retained_as_proof_bounds": False,
                                      "fresh_replay": True, "source_pin_is_integrity_not_proof": True},
            "premises_and_consumer_obligations": {
                "radius_domain": "Standardized P with Q3 moment parameters in the closed rational box, SAME nu=W*dP/eta, whole supplied owner support |X|<=17/4; no finite-support requirement.",
                "budgets": "eta E k0<=p0_actual, eta E_tag k2<=u_actual, E_tag k1=0, nu probability off zero/contact nodes. All costs/poles remain uniformly fullbox even though the response is sharpened around a nominal knot.",
                "nonnegative_candidate": "Use only radius candidates nonnegative over each eta cell, or independently prove exact emptiness. Do not clip a negative candidate to0. At eta0 delta=0/P=Q3 directly.",
                "reflection": "Both beta signs use reflection/conjugation and exchanged sign-tag prices, giving the same norm bound.",
                "physical_owner": "C3<CE/attainment/contact/support inputs supplied separately. If physical125/N^2 is used later, standing actual rho<46/25 is required; an outer eta endpoint alone does not prove it.",
                "separate_geometry": "No Q3 centre/Eg perturbation, actual characteristic modulus, Gaussian CDF, denominator, physical quadrature, H interpolation, tail or CDF acceptance certified here.",
                "integrity": "Saved JSON and source hashes audit integrity only; consumer must invoke fresh replay."},
            "source_pins": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
            "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                          "peak_working_set_bytes": point.integer.peak_bytes(), "time_limit_seconds": time_limit_seconds,
                          "memory_limit_bytes": MEMORY_LIMIT, "one_BLAS_thread": True},
            "conclusions": {"exact_radius_models_valid_on_closed_box": True,
                            "floating_bounds_used_as_proof_premises": False, "CDF_bound_proved": False,
                            "all_eta_CDF_certified": False, "global_parameter_cover": False,
                            "old_source_verifier_engine_or_receipts_modified": False}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(64, 512), default=512)
    parser.add_argument("--anchors", type=int, choices=(17, 33), default=17)
    parser.add_argument("--half-width", choices=("1/10000", "1/1000"), default="1/1000")
    args = parser.parse_args()
    half_width = F(args.half_width)
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(args.N) + "_halfwidth_" + args.half_width.replace("/", "_") + ".json")
    require(not output.exists(), "Never overwrite a V2 box affine receipt")
    result = compute_verified_box_models(F(9, 10) - half_width, F(9, 10) + half_width,
                                        F(9, 20) - half_width, F(9, 20) + half_width, args.N, args.anchors)
    raw = json.dumps(point.json_ready(result), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "New V2 box receipt<=2MiB")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)
    counts = [len(item["models"]) for item in result["frequency_models"]]
    print(json.dumps({"status": result["status"], "variant": result["variant"], "result": str(output),
                      "N": args.N, "half_width_exact": str(half_width), "output_bytes": len(raw.encode("utf-8")),
                      "model_count": sum(counts), "models_per_frequency_min_max": [min(counts), max(counts)],
                      "verification_metadata": point.json_ready(result["verification_metadata"]),
                      "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
