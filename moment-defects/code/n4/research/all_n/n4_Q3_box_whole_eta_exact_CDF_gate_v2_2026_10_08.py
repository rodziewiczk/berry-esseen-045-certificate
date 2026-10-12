"""V2: exact CLOSED (w,|beta|) BOX x WHOLE eta-fibre CDF gate.

Reusable run_verification(rectangle,N=512,M=32) accepts four Fraction
endpoints (w_lo,w_hi,beta_lo,beta_hi), covers both beta signs and every
actual-law eta>=0 with rho<46/25. Its enlarged closed eta interval is
[0,46/25-rhoQ_LO_box]. The first-critical owner support |X|<17/4 and
Prawitz/physical bridge are external conditional premises. No assertion
that every relaxation point is an actual law or a first-critical owner.

Box affine radius models are freshly rebuilt in memory. Actual Q3 geometry
is enclosed by exact monotone endpoint formulae, not corner sampling.
Reference centers use the nominal geometry, with raw correction
2 sum |kappa| D4(Eg,a_nominal), with a sharp fourth-power telescope. Eg
is the minimum of direct, mass-cancelled O(q), and matched-moment O(q^3)
reference perturbation bounds. Both reference laws have total mass1,
mean0 and variance1. Their Taylor terms cancel exactly. Actual
reference moduli are min(1,|g_nominal|upper+Eg). Nominal center is maximized
over all229 H nodes and both orientations once. The entire eta fibre is
covered by exact affine transfer endpoint checks, then physical frequency
and H reserves and original-P tails. Nothing imports a point epsilon or
an older normalized score as a box proof bound.

Only rational price index SELECTION uses floats; every proof bound is
integer/Fraction outward. No JSON data or hash is a radius premise.
Exported API does not write files; CLI writes only its new exclusive
receipt. --replay-existing repeats fresh arithmetic without writing.
60s cooperative job/256MiB/BLAS1/new receipt<=2MiB; existing fibre/box
sources and receipts remain untouched. Any uncovered cell is UNKNOWN.
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

import n4_Q3_whole_eta_fibre_exact_CDF_gate_2026_10_08 as fibre
import n4_Q3_three_budget_exact_box_affine_radius_verifier_v2_2026_10_08 as box_affine

base, arith, S = fibre.base, fibre.arith, fibre.S
HERE = Path(__file__).resolve().parent
TARGET, RHO_CAP, R = F(256, 625), F(46, 25), F(17, 4)
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 256 * 1024 * 1024, 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fresh_guard(started):
    require(time.monotonic() - started < TIME_LIMIT, "Box whole-eta time budget")
    peak = arith.peak_bytes()
    require(peak is None or peak <= MEMORY_LIMIT, "Box whole-eta memory budget")


def sqrt_interval(lo, hi):
    require(type(lo) is F and type(hi) is F and 0 < lo <= hi, "Positive exact root interval")
    return arith.sqrt_fraction_interval(lo)[0], arith.sqrt_fraction_interval(hi)[1]


def geometry(rectangle):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is F for value in rectangle), "Four exact Fraction box endpoints")
    wl, wh, bl, bh = rectangle
    require(0 < wl <= wh <= 1 and 0 <= bl <= bh < 1, "Nondegenerate closed magnitude box")
    w0, b0 = (wl + wh) / 2, (bl + bh) / 2
    a2 = ((1 - bh) / (wh * (1 + bh)), (1 - bl) / (wl * (1 + bl)))
    b2 = ((1 + bl) / (wh * (1 - bl)), (1 + bh) / (wl * (1 - bh)))
    a, b = sqrt_interval(*a2), sqrt_interval(*b2)
    a0 = arith.sqrt_fraction_interval((1 - b0) / (w0 * (1 + b0)))
    b0root = arith.sqrt_fraction_interval((1 + b0) / (w0 * (1 - b0)))
    da = max(a[1] - a0[0], a0[1] - a[0])
    db = max(b[1] - b0root[0], b0root[1] - b[0])
    require(da >= 0 and db >= 0 and max(a[1], b[1]) <= R * S,
            "Whole reference-knot box inside conditional owner support")
    pm = (wl * (1 + bl) / 2, wh * (1 + bh) / 2)
    pp = (wl * (1 - bh) / 2, wh * (1 - bl) / 2)
    pz = (1 - wh, 1 - wl)
    pm0, pp0, pz0 = w0 * (1 + b0) / 2, w0 * (1 - b0) / 2, 1 - w0
    dm, dp, dz = (max(pm[1] - pm0, pm0 - pm[0]),
                  max(pp[1] - pp0, pp0 - pp[0]),
                  max(pz[1] - pz0, pz0 - pz[0]))
    rho2 = ((1 + bl * bl) ** 2 / (wh * (1 - bl * bl)),
            (1 + bh * bh) ** 2 / (wl * (1 - bh * bh)))
    rho = sqrt_interval(*rho2)
    return {"rectangle": tuple(rectangle), "w0": w0, "beta0": b0, "a2": a2, "b2": b2,
            "a": a, "b": b, "a0": a0, "b0": b0root, "da": da, "db": db,
            "pminus": pm, "pplus": pp, "pzero": pz, "mass_deviations": (dm, dp, dz),
            "rho2": rho2, "rho": rho}


def nominal_rectangle(q, box):
    exp_tail = (q * R) ** 61 / math.factorial(61)
    w, beta = box["w0"], box["beta0"]
    negative = arith.weighted_rectangle(w * (1 + beta) / 2,
        arith.conjugate_rectangle(arith.outward_exponential(q, box["a0"], exp_tail)))
    positive = arith.weighted_rectangle(w * (1 - beta) / 2,
        arith.outward_exponential(q, box["b0"], exp_tail))
    zero = arith.fraction_interval(1 - w)
    return (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
            negative[2] + positive[2], negative[3] + positive[3])


def reference_error(q, box):
    """Three independent rigorous bounds; no subtraction of upper bounds.

    Let R2(x)=exp(i*q*x)-1-i*q*x+q^2*x^2/2. Both references have
    total mass1, mean0 and second moment1, so their R2 sums differ by
    exactly their characteristic-function difference. Taylor's integral
    remainder gives |R2(x)|<=q^3*|x|^3/6 and
    |R2'(x)|=|i*q*(exp(i*q*x)-1-i*q*x)|<=q^3*x^2/2.
    Atom motion remains on its same sign halfline, hence its absolute
    magnitude along the segment is <=the actual knot box upper.
    The mass-cancelled bound instead uses exp(i*q*x)-1, bounded by
    min(2,q*|x|). Zero atoms disappear in both cancellations.
    """
    require(type(q) is F and q >= 0, "Nonnegative exact frequency")
    dm, dp, dz = box["mass_deviations"]
    da, db = F(box["da"], S), F(box["db"], S)
    a0, b0 = F(box["a0"][1], S), F(box["b0"][1], S)
    amax, bmax = F(box["a"][1], S), F(box["b"][1], S)
    pm, pp = box["pminus"][1], box["pplus"][1]
    motion = pm * q * da + pp * q * db
    direct = dm + dp + dz + motion
    mass_cancelled = dm * min(F(2), q * a0) + dp * min(F(2), q * b0) + motion
    moments_cancelled = q ** 3 * ((dm * a0 ** 3 + dp * b0 ** 3) / 6
                                 + (pm * amax ** 2 * da + pp * bmax ** 2 * db) / 2)
    return min(direct, mass_cancelled, moments_cancelled)


def center_and_blocks(verified, box, n, m, guard):
    pi, phi0 = base.pi_and_phi0()
    positive_blocks, negative_blocks, frequencies = [], [], []
    center_scale2 = 0
    eg_ints = []
    for j, item in enumerate(verified["frequency_models"]):
        guard()
        q = item["q"]
        require(q == F(3 * (2 * j + 1), 2 * n), "Fresh physical frequency nodes")
        kernel = base.kernel_rectangle(F(2 * j + 1, 2 * n), n, m, pi)
        weight_int = arith.rectangle_modulus_upper(kernel)
        g = nominal_rectangle(q, box)
        nominal_modulus = min(S, arith.rectangle_modulus_upper(g))
        eg_int = arith.ceil_fraction_scaled(reference_error(q, box))
        eg_ints.append(eg_int)
        center_scale2 += weight_int * base.quartic_absolute_upper(eg_int, nominal_modulus)
        actual_modulus = F(min(S, nominal_modulus + eg_int), S)
        square = base.complex_multiply(g, g)
        fourth = base.complex_multiply(square, square)
        reflected = arith.conjugate_rectangle(g)
        reflected_square = base.complex_multiply(reflected, reflected)
        reflected_fourth = base.complex_multiply(reflected_square, reflected_square)
        positive_blocks.append(base.complex_multiply(kernel, fourth))
        negative_blocks.append(base.complex_multiply(kernel, reflected_fourth))
        models = []
        for index, model in enumerate(item["models"]):
            require(type(model["A"]) is F and type(model["S_upper_int"]) is int,
                    "Fresh exact BOX affine inputs")
            models.append((q ** 3 * model["A"], q ** 3 * F(model["S_upper_int"], S), "dual", index))
        M_hi = F(max(box["a"][1], box["b"][1]), S)
        models.extend(((F(0), q ** 3 / 6, "cube", -1),
                       (M_hi ** 2 * box["pzero"][1] * q ** 2, F(0), "mass", -1),
                       (1 + actual_modulus, F(0), "unit", -1)))
        frequencies.append({"q": q, "modulus": actual_modulus,
                            "weight": F(weight_int, S), "models": models})
    require(len(frequencies) == n, "All frequency blocks")
    center_variation_int = arith.ceil_div(2 * center_scale2, S)
    rows, normal_endpoint = [], None
    for h in base.H_GRID:
        guard()
        phase = base.exponential_exact_argument(-3 * h / (2 * n))
        ratio = base.exponential_exact_argument(-3 * h / n)
        positive = negative = 0
        for j in range(n):
            positive += base.complex_multiply(phase, positive_blocks[j])[1]
            negative += base.complex_multiply(phase, negative_blocks[j])[1]
            phase = base.unit_phase_intersection(base.complex_multiply(phase, ratio))
        normal = base.normal_cdf_interval(h / 2, phi0)
        if h == F(25, 8):
            normal_endpoint = normal
        for sign, center in ((1, positive), (-1, negative)):
            rows.append({"H_exact": str(h), "beta_orientation": sign,
                         "nominal_raw_Q_upper_int": str(S + 2 * center - 2 * normal[0])})
    require(normal_endpoint is not None and 5 * normal_endpoint[0] > 4 * S,
            "Exact Gaussian tail lower bound")
    maximum = max(int(row["nominal_raw_Q_upper_int"]) for row in rows)
    quad, hreserve = F(687, 8 * n * n), F(19, 32768)
    raw_constant = F(maximum + center_variation_int, S) + quad + hreserve
    return frequencies, raw_constant, rows, {
        "max_nominal_raw_Q_upper_int": str(maximum),
        "reference_center_RAW_variation_upper_int": str(center_variation_int),
        "largest_Eg_upper_int": str(max(eg_ints)),
        "ONE_original_P_midpoint_raw_exact": str(quad), "H_interpolation_raw_exact": str(hreserve),
        "raw_constant_upper_exact": str(raw_constant),
        "pi_bracket_ints": list(map(str, pi)), "phi0_bracket_ints": list(map(str, phi0)),
        "positive_tail_Phi_lower_int": str(normal_endpoint[0]),
    }


def whole_fibre(frequencies, raw_constant, rho_lower, eta_max, guard, max_count=256):
    intervals = [(eta_max * F(j, 64), eta_max * F(j + 1, 64)) for j in range(64)]
    rows = []
    for L, U in intervals:
        guard()
        rows.append(fibre.frozen_cell(frequencies, raw_constant, rho_lower, L, U))
    while len(rows) < max_count:
        failures = [(int(row["score_upper_int"]), j) for j, row in enumerate(rows) if not row["passed"]]
        if not failures:
            break
        _, index = max(failures)
        L, U = intervals[index]
        midpoint = (L + U) / 2
        replacements = [(L, midpoint), (midpoint, U)]
        new_rows = []
        for l, u in replacements:
            guard()
            new_rows.append(fibre.frozen_cell(frequencies, raw_constant, rho_lower, l, u))
        intervals[index:index + 1] = replacements
        rows[index:index + 1] = new_rows
    require(intervals[0][0] == 0 and intervals[-1][1] == eta_max
            and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])),
            "Complete closed eta cover without gaps")
    return rows, all(row["passed"] for row in rows)


def run_verification(rectangle, N=512, M=32, max_cells=256):
    """Pure fresh verification API; no receipt inputs and no file writes."""
    started = time.monotonic()
    guard = lambda: fresh_guard(started)
    require(type(N) is int and N in (64, 512) and type(M) is int and M in (16, 32), "Bounded exact grid")
    require(type(max_cells) is int and max_cells in (64, 128, 256), "Bounded fibre refinement")
    box = geometry(rectangle)
    verified = box_affine.compute_verified_box_models(*rectangle, N, anchor_count=17,
                                                     time_limit_seconds=45)
    guard()
    require(verified["status"] == "EXACT_BOX_AFFINE_DUAL_RADIUS_ENCLOSURES"
            and verified["scale"] == S, "Fresh BOX affine verification API")
    root = verified["root_data"]
    # Geometric monotonicity is independently recomputed here. Agreement
    # checks catch API/coordinate mismatches rather than trusting metadata.
    require(tuple(root["a_bracket"]) == box["a"] and tuple(root["b_bracket"]) == box["b"]
            and tuple(root["rhoQ_bracket"]) == box["rho"], "Independent full-box root enclosure agreement")
    rho_lower = F(box["rho"][0], S)
    eta_max = RHO_CAP - rho_lower
    require(rho_lower >= 1 and eta_max > 0, "Positive whole actual eta cover")
    frequencies, raw_constant, centers, center_details = center_and_blocks(verified, box, N, M, guard)
    rows, cells_passed = whole_fibre(frequencies, raw_constant, rho_lower, eta_max, guard, max_cells)
    passed = cells_passed and F(2, 5) < TARGET
    upper = max(arith.ceil_fraction_scaled(F(2, 5)), max(int(row["score_upper_int"]) for row in rows))
    inputs = (Path(__file__), Path(fibre.__file__), Path(base.__file__), Path(arith.__file__),
              Path(box_affine.__file__), Path(box_affine.box.__file__),
              Path(fibre.affine.__file__), Path(fibre.algebra.__file__),
              base.SUPPORT_NOTE, base.PHYSICAL_BRIDGE)
    guard()
    return {
        "status": "EXACT_CONDITIONAL_BOX_WHOLE_ETA_CDF_BOUND" if passed else "UNKNOWN",
        "date": "2026-10-08", "scale_exact": str(S), "N": N, "kernel_partial_fraction_M": M,
        "eta_initial_cell_count": 64, "eta_refinement_cell_cap": max_cells,
        "source_pins": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        "closed_parameter_box": {"w": list(map(str, rectangle[:2])), "abs_beta": list(map(str, rectangle[2:])),
                                 "both_beta_orientations": True, "whole_eta_cover": ["0", str(eta_max)],
                                 "nominal_w": str(box["w0"]), "nominal_abs_beta": str(box["beta0"])},
        "continuous_box_geometry": {key: box[key] for key in ("a2", "b2", "a", "b", "a0", "b0", "da", "db",
                                                                 "pminus", "pplus", "pzero", "mass_deviations", "rho2", "rho")},
        "geometry_proof": "a^2 decreases in w,beta; b^2 decreases in w and increases in beta; rhoQ^2 decreases in w and increases in abs(beta). Endpoint ranges with exact outward roots cover the WHOLE closed box, not only its corners.",
        "actual_law_definitions": "Standardized P, u=EX+=EX-,v+=EX+^2,v-=EX-^2; w=u^2/(v+v-), beta=v+-v-, eta=rho-rhoQ. No finite-atom reduction.",
        "external_conditional_boundary": "C3<CE; equality-level attained positive closed C4>=CE owner; Shevtsova/He--Cheng/attainment support17/4 and rho<46/25; one-sided closed-CDF Prawitz; pinned original-P physical quadrature/H bridge. These are mathematical input premises, not results of checking a source hash.",
        "physical_scope": "The numerical eta cover is enlarged using rhoQ_LO_box. Only actual laws satisfying rho<46/25 acquire the physical reserve; no claim that every relaxation corner or outer eta face is realizable.",
        "fresh_radius_verification": {"recomputed_in_memory": True, "numeric_JSON_tables_trusted": False,
                                      "model_table_sha256": fibre.exact_model_digest(verified),
                                      "model_count": sum(len(item["models"]) for item in verified["frequency_models"]),
                                      "metadata": verified["verification_metadata"],
                                      "formula": "q^3*(A+eta*Supper/scale), A exact full-box price-budget upper; Supper signed full-box HG/pole/cost upper. Nonnegative radius endpoints checked on every entire eta cell.",
                                      "float_boundary": "Midpoint float search selects rational price indices only; fresh exact box verification proves every used model independently."},
        "reference_variation": "Eg=min(direct, mass-cancelled O(q), matched mass/mean/variance O(q^3)). Eg1=dm*min(2,q*a0_hi)+dp*min(2,q*b0_hi)+pminus_hi*q*Delta_a+pplus_hi*q*Delta_b. Eg3=q^3*((dm*a0_hi^3+dp*b0_hi^3)/6+(pminus_hi*amax^2*Delta_a+pplus_hi*bmax^2*Delta_b)/2). Actual |g|<=min1(|g_nominal|upper+Eg). RAW2sum|kappa|D4(Eg,a_nominal) uses the exact fourth-power telescope with p=min1(a_nominal+Eg), optional endpoint cap; never raw8*Eg unless that happens to be sharper.",
        "reference_center": center_details, "reference_center_rows_both_orientations": centers,
        "reflection": "True characteristic conjugation at the same H and phase, not a closed-CDF complement.",
        "eta_cell_cover": rows,
        "acceptance_proof": "Each chosen affine epsilon nonnegative at both cell endpoints. Audited frozen-cap E affine majorant, optional whole-cell endpoint cap. Both affine coefficients ceiled outward and weight uppers applied to nonnegative cell polynomials. Raw target maxHcenter+geometry+quad+H+2sumweightE-(256/625)*(rhoQ_LO_box+eta) is strictly negative at both endpoints of EVERY closed cell.",
        "whole_H_and_tails": "All229 H nodes[-4,25/8]step1/32, both signs; physical H reserve19/32768 and ONE original-P midpoint687/(8N^2). H<=-4 Cantelli; H>=25/8 exact Phi(25/16)>4/5. Positive closed tails<=2/(5rho)<=2/5, reflection via closed limits.",
        "summary": {"whole_box_eta_and_H_score_upper_int": str(upper),
                    "whole_box_eta_and_H_score_upper_decimal": base.decimal_upper(upper),
                    "target_exact": str(TARGET), "strict_margin_int": str(arith.floor_fraction_scaled(TARGET) - upper),
                    "cell_count": len(rows), "cells_not_strictly_below_target": sum(not row["passed"] for row in rows),
                    "complete_closed_eta_cover_verified": True},
        "conclusions": {"conditional_continuous_box_times_whole_eta_CDF_bound": passed,
                        "both_reflections_all_H_and_tails": passed,
                        "proof_bounds_integer_or_Fraction_outward": True,
                        "floating_proof_premises": False, "cached_point_bounds_used_as_box_bounds": False,
                        "fresh_whole_box_affine_verification_mandatory": True,
                        "full_w_beta_root_covered": False, "unrestricted_C4_proved": False,
                        "old_sources_or_receipts_modified": False},
        "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                      "peak_working_set_bytes": arith.peak_bytes(), "time_limit_seconds": TIME_LIMIT,
                      "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
                      "cooperative_not_OS_limit": True},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", choices=("1/1000", "1/10000"), default="1/1000")
    parser.add_argument("--N", type=int, choices=(64, 512), default=512)
    parser.add_argument("--kernel-M", type=int, choices=(16, 32), default=32)
    parser.add_argument("--max-cells", type=int, choices=(64, 128, 256), default=256)
    parser.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    width = F(args.width)
    rectangle = (F(9, 10) - width, F(9, 10) + width, F(9, 20) - width, F(9, 20) + width)
    output = Path(__file__).with_name(Path(__file__).stem + "_width1_" + str(width.denominator)
                                    + "_N" + str(args.N) + "_M" + str(args.kernel_M) + ".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a box-fibre receipt")
    require(not args.replay_existing or output.exists(), "Read-only box-fibre replay receipt exists")
    result = run_verification(rectangle, args.N, args.kernel_M, args.max_cells)
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False, default=fibre.exact_json_value) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Box-fibre output budget")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Read-only receipt size")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for field in fresh:
            if field != "resources":
                require(saved[field] == fresh[field], "Read-only box-fibre replay field: " + field)
        printed_status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        printed_status = result["status"]
    print(json.dumps({"status": printed_status, "result": str(output), "output_bytes": len(raw.encode("utf-8")),
                      "summary": result["summary"], "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
