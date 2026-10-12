"""Fresh EXACT affine three-budget radius models on CLOSED rational boxes.

No pointwise parameter substitution: every Hermite response rectangle,
inverse-size cost and reciprocal-pole penalty is evaluated on the entire
contact-root interval induced by the supplied w,beta-magnitude rectangle.
Only rational price indices are selected at the exact nominal midpoint.

Public API compute_verified_box_models(w_lo,w_hi,beta_lo,beta_hi,N,
anchor_count=17) returns the same q/Fraction A/signed integer S model format
as the audited point verifier. e_q(eta)=q^3*(A+eta*S/SCALE) is valid on the
whole feasible eta fibre AND parameter box. The consumer supplies the Q3
centre perturbation, actual |g| cap, denominator enclosure and CDF reserves.
It must retain only nonnegative radius candidates on a cell, or separately
prove conditional-model emptiness; at eta0 delta=0 directly.

No CDF or global parameter cover, no trusted JSON replay. Conditional owner
support R17/4 and physical moment/rho premises are explicit inputs. Old
verifier/engine/receipts/globals are never edited. Cooperative60s/256MiB,
BLAS1, one fresh N512 job per box, exclusive new receipt<=2MiB.
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

import n4_Q3_three_budget_exact_affine_radius_verifier_2026_10_08 as point

SCALE, RADIUS, STEP = point.SCALE, point.RADIUS, point.STEP
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60.0, 256 * 1024 * 1024, 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sqrt_interval_between(low, high):
    require(0 < low <= high, "Positive ordered exact square endpoints")
    return (point.integer.sqrt_fraction_interval(low)[0],
            point.integer.sqrt_fraction_interval(high)[1])


def nominal_root_data(w, beta):
    """Price-selection reference, including boxes straddling the root face."""
    a2 = (1 - beta) / (w * (1 + beta))
    b2 = (1 + beta) / (w * (1 - beta))
    u2 = w * (1 - beta * beta) / 4
    rho2 = (1 + beta * beta) ** 2 / (w * (1 - beta * beta))
    a, b, u, rho = map(point.integer.sqrt_fraction_interval, (a2, b2, u2, rho2))
    # A nominal point outside the root face is not a blocker for a box
    # intersecting it: zero-only seed anchors are still allowed prices.
    return {"w": w, "beta": beta, "p0": 1 - w, "a_square": a2, "b_square": b2,
            "u_square": u2, "rhoQ_square": rho2, "a_bracket": a, "b_bracket": b,
            "u_bracket": u, "rhoQ_bracket": rho,
            "eta_max_upper": max(F(0), point.ROOT_CAP - F(rho[0], SCALE))}


def box_root_data(w_lo, w_hi, beta_lo, beta_hi):
    endpoints = (w_lo, w_hi, beta_lo, beta_hi)
    require(all(isinstance(value, F) for value in endpoints), "Exact Fraction rectangle endpoints")
    require(0 < w_lo <= w_hi <= 1 and 0 <= beta_lo <= beta_hi < 1, "Closed valid w and beta-magnitude box")
    # a^2 decreases in both w,beta; b^2 decreases in w/increases in beta.
    a2 = ((1 - beta_hi) / (w_hi * (1 + beta_hi)),
          (1 - beta_lo) / (w_lo * (1 + beta_lo)))
    b2 = ((1 + beta_lo) / (w_hi * (1 - beta_lo)),
          (1 + beta_hi) / (w_lo * (1 - beta_hi)))
    # u^2 increases in w/decreases in beta>=0. rhoQ^2 does the opposite.
    u2 = (w_lo * (1 - beta_hi ** 2) / 4, w_hi * (1 - beta_lo ** 2) / 4)
    rho2 = ((1 + beta_lo ** 2) ** 2 / (w_hi * (1 - beta_lo ** 2)),
            (1 + beta_hi ** 2) ** 2 / (w_lo * (1 - beta_hi ** 2)))
    a, b, u, rho = [sqrt_interval_between(*interval) for interval in (a2, b2, u2, rho2)]
    require(max(a[1], b[1]) <= RADIUS * SCALE, "Entire closed contact-root intervals inside owner R17/4")
    p0_lo, p0_hi = 1 - w_hi, 1 - w_lo
    nominal = nominal_root_data((w_lo + w_hi) / 2, (beta_lo + beta_hi) / 2)
    require(all(box[0] <= nominal[name + "_bracket"][0] <= nominal[name + "_bracket"][1] <= box[1]
                for name, box in (("a", a), ("b", b), ("u", u), ("rhoQ", rho))),
            "Nominal root brackets enclosed in the closed box")
    return {"w_interval": (w_lo, w_hi), "beta_abs_interval": (beta_lo, beta_hi),
            "a_square_interval": a2, "b_square_interval": b2, "u_square_interval": u2,
            "rhoQ_square_interval": rho2, "a_bracket": a, "b_bracket": b,
            "u_bracket": u, "rhoQ_bracket": rho, "p0_lo": p0_lo, "p0_hi": p0_hi,
            "u_hi": F(u[1], SCALE), "rhoQ_lo": F(rho[0], SCALE), "rhoQ_hi": F(rho[1], SCALE),
            "eta_max_root_outer": point.ROOT_CAP - F(rho[0], SCALE),
            "eta_max_physical_outer": F(46, 25) - F(rho[0], SCALE),
            "nominal_root_data": nominal,
            "nominal_probabilities": {"negative": nominal["w"] * (1 + nominal["beta"]) / 2,
                                      "zero": nominal["p0"], "positive": nominal["w"] * (1 - nominal["beta"]) / 2},
            "probability_intervals": {"negative": (w_lo * (1 + beta_lo) / 2, w_hi * (1 + beta_hi) / 2),
                                      "zero": (p0_lo, p0_hi),
                                      "positive": (w_lo * (1 - beta_hi) / 2, w_hi * (1 - beta_lo) / 2)}}


def compute_verified_box_models(w_lo, w_hi, beta_lo, beta_hi, N, anchor_count=17,
                                time_limit_seconds=TIME_LIMIT):
    """Fresh replay on a rational rectangle; no numeric receipt is trusted."""
    started = time.monotonic()
    require(N in (64, 512) and anchor_count in (17, 33), "Fixed small exact frequency/seed grid")
    require(0 < time_limit_seconds <= TIME_LIMIT, "Cooperative time limit<=60s")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Exact box affine elapsed budget")
        peak = point.integer.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Exact box affine working-set budget")
    root = box_root_data(w_lo, w_hi, beta_lo, beta_hi)
    nominal = root["nominal_root_data"]
    # Search prices are selected only at the exact rational nominal point.
    # No numerical suprema from search are retained or used in verification.
    nominal_tables = {name: point.cell_tables(nominal[name + "_bracket"], guard) for name in ("a", "b")}
    selected, search_metadata = point.float_search_seeds(nominal, N, anchor_count, nominal_tables, guard)
    del nominal_tables
    # These are separate, FRESH tables enclosing the ENTIRE parameter box.
    box_tables = {name: point.cell_tables(root[name + "_bracket"], guard) for name in ("a", "b")}
    data = point.frequency_data(N, guard)
    plus_wanted = [sorted(set((it, ip) for it, ip, im in row)) for row in selected]
    minus_wanted = [sorted(set((it, im) for it, ip, im in row)) for row in selected]
    plus, plus_metadata = point.verify_tag(root["b_bracket"], box_tables["b"], data, plus_wanted, guard)
    minus, minus_metadata = point.verify_tag(root["a_bracket"], box_tables["a"], data, minus_wanted, guard)
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
    source_paths = (Path(__file__), Path(point.__file__), Path(point.integer.__file__), point.integer.SUPPORT_NOTE)
    return {"status": "EXACT_BOX_AFFINE_DUAL_RADIUS_ENCLOSURES", "scale": SCALE, "N": N,
            "root_data": root, "nominal_root_data": nominal,
            "nominal_probabilities": root["nominal_probabilities"], "frequency_models": frequency_models,
            "prices": {"tau": point.TAUS, "pairs": point.PAIRS}, "search_metadata": search_metadata,
            "verification_metadata": {"positive_tag": plus_metadata, "negative_tag": minus_metadata,
                                      "HG_degree": point.DEGREE, "R": RADIUS, "y_step": STEP,
                                      "HG_tail": "q^3/6*(qR)^61/61!", "raw_mesh": "q^4*h/48",
                                      "HG_c_interval": "Whole outward contact-root interval of the CLOSED w,beta box; no nominal c substitution",
                                      "cost": "floor_SCALE[1/(c_box_hi^2*y_cell_hi)]",
                                      "pole": "exact Fraction concave maximum over reciprocal image of[cellLo-c_box_hi,cellHi-c_box_lo], with two rays on crossing0; signed CEIL",
                                      "intercept": "A_box=p0_hi*tau+u_hi*(zeta_plus+zeta_minus), an exact rational upper",
                                      "model": "|delta(q)|<=q^3*(A_box+eta*S_box_upper_int/SCALE), uniform on full parameter box and every feasible eta>=0",
                                      "nominal_float_values_retained_as_proof_bounds": False,
                                      "fresh_replay": True, "source_pin_is_integrity_not_proof": True},
            "premises_and_consumer_obligations": {
                "radius_domain": "Standardized P with Q3 sign-moment parameters in the CLOSED rectangle, common nu=W*dP/eta and supplied whole owner support |X|<=17/4. No finite-support requirement for P.",
                "three_budgets": "eta E k0<=p0_actual; eta E_tag k2<=u_actual; E_tag k1=0; nu probability off zero/contact nodes. Fixed-point response and pole bounds cover every actual c in its box interval.",
                "eta_scope": "Radius models hold for all feasible eta>=0. Anchor/root caps select prices ONLY; outer eta endpoints do not themselves establish actual rho membership or feasibility.",
                "reflection": "Negative beta magnitude is handled by reflecting P,Q3 and conjugating characteristic functions; the SAME norm bound holds, with sign-tag prices exchanged.",
                "nonnegative_candidate": "The CDF consumer must verify chosen A+eta*S/SCALE>=0 on a whole eta cell, use another positive cap, or separately prove exact conditional-model emptiness. Never clamp a negative radius to0. At eta0 delta=0/P=Q3 directly.",
                "separate_geometry": "This module does NOT certify phiQ centre, closed-box Eg perturbation, original-P physical quadrature, H interpolation, Gaussian CDF, denominator bounds or tails.",
                "physical_owner": "The root uses separately supplied C3<CE/attainment/owner-contact/support inputs. If the consumer uses physical raw125/N^2 reserve, it must retain actual rho<46/25 together with |X|<=17/4; the outer rectangular eta endpoint alone is not this premise.",
                "integrity": "Source pins and saved JSON are audit trails only; fresh compute_verified_box_models replay is required for a certificate consumer."},
            "source_pins": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
            "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                          "peak_working_set_bytes": point.integer.peak_bytes(), "time_limit_seconds": time_limit_seconds,
                          "memory_limit_bytes": MEMORY_LIMIT, "one_BLAS_thread": True},
            "conclusions": {"exact_radius_models_valid_on_closed_box": True,
                            "floating_bounds_used_as_proof_premises": False, "CDF_bound_proved": False,
                            "all_eta_CDF_certified": False, "global_parameter_cover": False,
                            "old_verifier_engine_globals_or_receipts_modified": False}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(64, 512), default=512)
    parser.add_argument("--anchors", type=int, choices=(17, 33), default=17)
    parser.add_argument("--half-width", choices=("1/10000", "1/1000"), default="1/10000")
    args = parser.parse_args()
    half_width = F(args.half_width)
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(args.N) + "_halfwidth_" + args.half_width.replace("/", "_") + ".json")
    require(not output.exists(), "Never overwrite a box affine receipt")
    result = compute_verified_box_models(F(9, 10) - half_width, F(9, 10) + half_width,
                                        F(9, 20) - half_width, F(9, 20) + half_width,
                                        args.N, args.anchors)
    raw = json.dumps(point.json_ready(result), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "New box receipt<=2MiB")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)
    counts = [len(item["models"]) for item in result["frequency_models"]]
    print(json.dumps({"status": result["status"], "result": str(output), "N": args.N,
                      "half_width_exact": str(half_width), "output_bytes": len(raw.encode("utf-8")),
                      "model_count": sum(counts), "models_per_frequency_min_max": [min(counts), max(counts)],
                      "closed_rectangle": point.json_ready((result["root_data"]["w_interval"], result["root_data"]["beta_abs_interval"])),
                      "verification_metadata": point.json_ready(result["verification_metadata"]),
                      "search_metadata": result["search_metadata"], "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
