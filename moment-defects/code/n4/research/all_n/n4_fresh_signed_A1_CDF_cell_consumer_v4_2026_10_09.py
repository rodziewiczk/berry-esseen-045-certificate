"""NEW V4 signed/ABS postconsumer with DIRECT fresh common-nu norm radii.

Input and scope are the SAME ORIGINAL DIRECT correct A1V2 table and the
SAME DIRECT original five-price Gamma table as frozen V3. No old CDF
evaluate function is called, no globals/table/frequency data are mutated,
and no CF/A1/Gamma producer is called. The NEW audited modulus helper is
DIRECTLY invoked inside this consumer on the ORIGINAL A1/RAW object.
Schema/status/hash/numeric JSON cannot establish those analytic bounds.

response_norm(default) adds the exact PHYSICAL affine model(0,Uq), where
Uq bounds |r_actual| on ALL273 y cells and BOTH actual contacts, with
the RAW nominal HG tail/mesh already ONCE, physical q^4*Delta_c/12 ONCE,
and whole cubic cap. It is not normalized by q^3 and not an H-summed
Gamma modulus. five_budget instead adds freshly proved PHYSICAL A,S
models from the exact common-nu norm dual. Use S:Fraction EXACTLY, not
its optional extra rounded S_upper_int. Signed slopes remain signed.
Every radius is frozen ONLY when nonnegative at BOTH cell endpoints;
negative radius signals are not clipped to a fake0 or used to mask eta.

Augment baseline frequencies ONLY for the refined SIGNED-R2 route.
g_actual modulus and kernel weights remain the original proven values.
Do NOT feed the augmented models to E29's complete-ABS routine: that
routine retains ONLY original cube/mass/unit models and count semantics.
The physical-H curvature also remains the ORIGINAL baseline version,
independently conservative. Actual reference moduli are never replaced
by delta/r norms or nominal reference moduli.

Midpoint model selection can favor a refined radius whose endpoint
maximum/cap choice is worse, despite enlarging the candidate family.
Therefore at EACH H/cell independently prove THREE full uniform routes:
 old baseline SIGNED Gamma+R2; refined-radius SIGNED Gamma+R2;
 baseline COMPLETE-ABS transfer.
Pair each with the SAME M_H, SAME signed Gamma where applicable, ONE
local-or-old quad_H and ONE whole-cell physical-H reserve before max-H.
Then select ONE COMPLETE uniform score, never coefficientwise min,
endpointwise route mixing, E[min], or ABS C,D labeled as Gamma/R2.
This preserves monotonicity relative to the complete frozen V3 method,
under the SAME original inputs/remainder switch, without claiming any
point-winner persists on the closed cell.

All16 closed eta cells/joins, all58/115/229 H, BOTH genuine reflections,
fresh T4097/10000<CE and actual-law tail2/5 remain. Every UNKNOWN interval
is retained, even when a norm dual gives conditional infeasibility signals.
Standing scope: standardized iid actual P in declared canonical BOX/eta,
|X|<=17/4, actualrho=rhoQ_actual+eta<46/25, retained CLOSED-CDF Prawitz/
original-P bridge. Local moments derive M4; no new atom/density/moment
axiom. This alone proves no entire-root/unrestricted C4. Stdlib60s/256MiB;
dormant tiny scalar tests only, no import-time jobs or write CLI. Every
older source and receipt stays unchanged. No performance/closure claim
before a separately authorized mathematical producer.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_signed_A1_CDF_cell_consumer_v3_2026_10_09 as previous
import n4_Q3_fresh_common_nu_modulus_radius_models_2026_10_09 as modulus_radius

core, local_quad = previous.core, previous.local_quad
SCALE, TARGET, require = previous.SCALE, previous.TARGET, previous.require
TIME_LIMIT, MEMORY_LIMIT, ETA_CELLS = previous.TIME_LIMIT, previous.MEMORY_LIMIT, previous.ETA_CELLS
fixed_eta_cells = previous.fixed_eta_cells
PREVIOUS_PIN = "82c98f8059f3ebe19168fe15f2b35123993a136e64d99d238bebd0fc63264b40"
RADIUS_PIN = "10e0392d347bf3aefeffedc5a861ee80d5dd5162b6e32b6697c2998100276456"
ROUTES = ("baseline_signed_A1_R2", "refined_radius_signed_A1_R2", "baseline_complete_ABS")


def source_drift_check():
    previous.source_drift_check()
    modulus_radius.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (modulus_radius, RADIUS_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen fresh-radius/complete-portfolio arithmetic integrity only")
    require(SCALE == modulus_radius.SCALE, "SAME physical fixed-point units")


def dependency_pins():
    pins = previous.dependency_pins()
    for path in (Path(__file__), Path(modulus_radius.__file__)):
        require(path.name not in pins, "Unique new modulus-radius source labels")
        pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def _checked_modulus_identity(fresh_radius, table, eta_cells, mode):
    """Scope only AFTER the DIRECT helper call, not a numerical importer."""
    box, nominal = table["box_geometry"], table["nominal_root_data"]
    require(type(fresh_radius["scale"]) is type(fresh_radius["N"]) is int
            and fresh_radius["scale"] == SCALE and fresh_radius["N"] == table["N"] == 256
            and tuple(fresh_radius["box_geometry"]["rectangle"]) == tuple(box["rectangle"]),
            "SAME entire actual box/N/scale for fresh radii")
    for key in ("a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket", "w_interval", "beta_abs_interval"):
        require(tuple(fresh_radius["box_geometry"][key]) == tuple(box[key]), "Actual box identity: " + key)
    for key in ("p0_hi", "u_hi", "rhoQ_lo", "rhoQ_hi"):
        require(type(fresh_radius["box_geometry"][key]) is F
                and fresh_radius["box_geometry"][key] == box[key], "Exact actual budget/rho identity: " + key)
    for key in ("w", "beta", "a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket"):
        require(fresh_radius["nominal_root_data"][key] == nominal[key], "Separate TRUE nominal identity: " + key)
    q_grid = tuple(item["q"] for item in table["frequency_data"])
    require(tuple(fresh_radius["q_grid"]) == q_grid and all(type(q) is F for q in fresh_radius["q_grid"])
            and tuple(fresh_radius["metadata"]["H_grid"]) == tuple(table["metadata"]["H_grid"]),
            "ALL physical q/H labels agree, no reflected or frequency prefix")
    if mode == "five_budget":
        require(tuple(tuple(cell) for cell in fresh_radius["eta_cells"]) == eta_cells
                and fresh_radius["metadata"]["price_order"] == core.PRICE_ORDER,
                "SAME closed eta cells and canonical normalized/physical price meanings")


def _augment_signed_frequencies(baseline, fresh_radius, table, mode):
    """Only delta-radius models change, NEVER actual g/weights/table data."""
    source = fresh_radius["frequency_data"] if mode == "response_norm" else fresh_radius["frequency_models"]
    require(len(source) == len(baseline) == len(table["frequency_data"]) == 256,
            "Every original frequency receives its OWN fresh radius models")
    refined = []
    box = table["box_geometry"]
    for j, (base, added) in enumerate(zip(baseline, source)):
        require(type(added["q"]) is F and type(added["q_index"]) is int
                and added["q"] == table["frequency_data"][j]["q"] and added["q_index"] == j,
                "SAME exact q and index, no cross-frequency radius")
        if mode == "response_norm":
            slope = added["actual_response_norm_upper_exact"]
            require(type(slope) is F and 0 <= slope <= added["q"] ** 3 / 6
                    and tuple(added["radius_model"]) == (F(0), slope, "zero_price_response_norm"),
                    "Fresh PHYSICAL Uq slope, no extra q-cubic scaling")
            extras = ((F(0), slope, "zero_price_response_norm"),)
        else:
            extras = []
            for model in added["five_budget_models"]:
                A, S, prices = model["A"], model["S"], tuple(model["prices"])
                require(type(A) is type(S) is F and A >= 0 and type(model["label"]) is str
                        and len(prices) == 5 and all(type(value) is F for value in prices)
                        and min(prices[:3]) >= 0,
                        "Exact PHYSICAL affine radius; signed S NOT its extra rounded integer alias")
                require(A == box["p0_hi"] * prices[0] + box["u_hi"] * (prices[1] + prices[2]),
                        "Recomputed PHYSICAL budget intercept from physical prices")
                extras.append((A, S, "fresh_modulus_" + model["label"]))
            require(extras, "At least zero-price complete common-nu norm model")
            extras = tuple(extras)
        models = tuple(dict.fromkeys(tuple(base["models"]) + extras))
        require(all(type(A) is type(B) is F and type(label) is str for A, B, label in models),
                "Exact PHYSICAL whole models, not a clipped or normalized radius")
        item = dict(base, models=models)
        require(item["modulus"] == base["modulus"] and item["weight_int"] == base["weight_int"]
                and all(model in models for model in base["models"]),
                "Original actual-reference modulus/kernel/baseline radius routes unchanged")
        refined.append(item)
    return refined


def _choose_three_complete_routes(baseline_signed, refined_signed, baseline_ABS):
    """Min ONE complete uniform row score; monotone without midpoint lore."""
    choices = tuple(zip(ROUTES, (baseline_signed, refined_signed, baseline_ABS)))
    route, chosen = min(choices, key=lambda pair: (pair[1]["normalized_score_upper"], pair[0]))
    require(chosen["whole_cell_strict_numeric_inequality"] == any(
            row["whole_cell_strict_numeric_inequality"] for _, row in choices),
            "ANY one COMPLETE WHOLE-cell route suffices")
    require(chosen["normalized_score_upper"] <= min(baseline_signed["normalized_score_upper"],
                                                     baseline_ABS["normalized_score_upper"]),
            "Never worse than BOTH complete original V3 routes")
    return route, dict(chosen)


def evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval, rectangle=None,
        N=256, H_step=F(1, 8), use_two_disk=True, modulus_radius_mode="response_norm",
        time_limit_seconds=TIME_LIMIT):
    """DIRECT original inputs -> DIRECT new radii -> three complete routes."""
    started = time.monotonic()
    rectangle = tuple(table["box_geometry"]["rectangle"] if rectangle is None else rectangle)
    core.cached.previous.checked_request(rectangle, eta_interval, N, H_step, ETA_CELLS, ETA_CELLS)
    require(type(use_two_disk) is bool and type(modulus_radius_mode) is str
            and modulus_radius_mode in ("response_norm", "five_budget")
            and type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Explicit fresh-radius mode/whole-R2 switch/cooperative60s timer")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Fresh-radius signed postconsumer elapsed budget")
        peak = core.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Fresh-radius signed postconsumer256MiB")

    eta_cells = fixed_eta_cells(eta_interval)
    box, grid = core._check_fresh_inputs(table, gamma_table, rectangle, N, H_step, eta_cells)
    baseline = core.H_leaf.transfer_frequencies(table["frequency_data"], box)
    if modulus_radius_mode == "response_norm":
        fresh_radius = modulus_radius.actual_response_norm_uppers(table, guard)
    else:
        fresh_radius = modulus_radius.compute_verified_modulus_radius_models(table, eta_cells, guard)
    _checked_modulus_identity(fresh_radius, table, eta_cells, modulus_radius_mode)
    refined = _augment_signed_frequencies(baseline, fresh_radius, table, modulus_radius_mode)
    gamma_rows = {(row["orientation"], row["H"]): row for row in gamma_table["rows"]}
    centre_rows = {(row["orientation"], row["H"]): row for row in table["rows"]}
    cells = []
    for L, U in eta_cells:
        guard()
        # Conservatively retain ORIGINAL physical-H fill/radius choices.
        curve = core.H_leaf.compact_cell_curvature(table["frequency_data"], box, L, U, H_step, N)
        H_reserve = F(curve["physical_H_reserve_upper_int"], SCALE)
        old_R2, old_choices = core._fresh_weighted_R2(baseline, L, U, use_two_disk, guard)
        new_R2, new_choices = core._fresh_weighted_R2(refined, L, U, use_two_disk, guard)
        # The augmented frequency/model family is NEVER supplied to E29.
        dummy_ABS = core.cached.previous.frozen_complete_ABS_cell(baseline, F(0), box["rhoQ_lo"], L, U)
        C, D = dummy_ABS["transfer_affine_upper"]
        moments = local_quad.whole_cell_moment_uppers(rectangle, (L, U))
        row_results, route_counts = [], {name: 0 for name in ROUTES}
        for H in grid:
            guard()
            quad_model = local_quad.physical_quad_at_H(moments, H, N)
            quad_H = quad_model["ONE_selected_physical_quad_upper_exact"]
            require(0 <= quad_H <= F(687, 8 * N * N), "ONE complete scalar local/old reserve intersection")
            for orientation in (1, -1):
                guard()
                key = orientation, H
                gamma_index, gamma_model = core._choose_gamma(gamma_rows[key]["models"], L, U)
                M_H = F(centre_rows[key]["raw_minus_target_rhoQ_upper_int"], SCALE)
                old_signed = core.ledger.per_H_signed_normalized_row(M_H, gamma_model, old_R2,
                    quad_H, H_reserve, box["rhoQ_lo"], L, U, TARGET, local_quad.RHO_CAP)
                new_signed = core.ledger.per_H_signed_normalized_row(M_H, gamma_model, new_R2,
                    quad_H, H_reserve, box["rhoQ_lo"], L, U, TARGET, local_quad.RHO_CAP)
                ABS = previous.complete_ABS_normalized_row(M_H, (C, D), quad_H,
                    H_reserve, box["rhoQ_lo"], L, U, TARGET, local_quad.RHO_CAP)
                route, chosen = _choose_three_complete_routes(old_signed, new_signed, ABS)
                chosen.update({"orientation": orientation, "H": H,
                    "normalized_reference_center_upper_exact": M_H,
                    "selected_WHOLE_cell_route": route,
                    "complete_baseline_signed_row_proof": old_signed,
                    "complete_refined_radius_signed_row_proof": new_signed,
                    "complete_baseline_ABS_row_proof": ABS,
                    "frozen_gamma_model_index": gamma_index,
                    "ONE_local_physical_quad_model": quad_model})
                route_counts[route] += 1
                row_results.append(chosen)
        require(len(row_results) == 2 * len(grid) and sum(route_counts.values()) == len(row_results),
                "Every H/reflection and ALL three COMPLETE routes checked")
        worst = max(row_results, key=lambda row: row["normalized_score_upper"])
        passed = all(row["whole_cell_strict_numeric_inequality"] for row in row_results)
        require(passed == (worst["normalized_score_upper"] < TARGET),
                "WHOLE-cell max only AFTER per-H full-route choice")
        cells.append({"lower": L, "upper": U, "passed": passed,
            "score_upper": worst["normalized_score_upper"], "worst_complete_H_row": worst,
            "H_reflection_rows_checked": len(row_results), "complete_route_counts": route_counts,
            "baseline_signed_weighted_R2_upper_polynomial": old_R2,
            "refined_radius_signed_weighted_R2_upper_polynomial": new_R2,
            "baseline_complete_ABS_transfer_affine_upper": (C, D),
            "baseline_complete_ABS_model_counts": dummy_ABS["selected_model_counts"],
            "baseline_complete_ABS_choices_digest_integrity_only": dummy_ABS["choices_digest_integrity_only"],
            "physical_H_curvature_uses_original_baseline_only": curve,
            "whole_cell_physical_moment_uppers": moments,
            "baseline_R2_choices_digest_integrity_only": hashlib.sha256(repr(old_choices).encode("ascii")).hexdigest(),
            "refined_radius_R2_choices_digest_integrity_only": hashlib.sha256(repr(new_choices).encode("ascii")).hexdigest(),
            "baseline_R2_methods_used": tuple(sorted({method for _, method in old_choices})),
            "refined_radius_R2_methods_used": tuple(sorted({method for _, method in new_choices}))})
    certificate, tail_lower = table["metadata"]["fresh_target_certificate"], table["metadata"]["positive_tail_Phi_lower_int"]
    require(certificate["target"] == TARGET and type(certificate["CE_lower_exact"]) is F
            and certificate["CE_lower_exact"] > TARGET and type(tail_lower) is int
            and 5 * tail_lower > 4 * SCALE, "Fresh target below CE/actual-law tails unchanged")
    tail, upper = F(2, 5), max([F(2, 5)] + [cell["score_upper"] for cell in cells])
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "ALL16 closed eta/H/reflections/tails strictly pass")
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "All fresh mathematical sources unchanged through V4 consumer")
    guard()
    return {"status": "EXACT_CONDITIONAL_FRESH_MODULUS_RADIUS_SIGNED_ABS_LOCAL_QUAD_BOX_ETA" if passed else "UNKNOWN",
        "scale": SCALE, "target": TARGET, "N": N, "H_step": H_step,
        "closed_rectangle": rectangle, "closed_eta_cover": tuple(eta_interval), "cells": cells,
        "modulus_radius_mode": modulus_radius_mode, "use_two_disk": use_two_disk,
        "DIRECT_fresh_modulus_radius_bounds": fresh_radius,
        "unresolved_eta_cell_indices": tuple(i for i, cell in enumerate(cells) if not cell["passed"]),
        "summary": {"score_upper_exact": upper, "failed_eta_cells": sum(not cell["passed"] for cell in cells),
            "ALL_H_nodes": len(grid), "ALL_H_reflection_rows_per_cell": 2 * len(grid), "fixed_closed_eta_cells": ETA_CELLS},
        "reserves_once": {"physical_quad": "PER_H_WHOLE_CLOSED_ETA_SCALAR_REPLACEMENT",
            "physical_H": "ORIGINAL_BASELINE_PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "actual_law_tail_score_upper": tail, "fresh_target_certificate": certificate,
        "physical_premises": "Standardized iid actual P in declared canonicalBOX/eta, |X|<=17/4,actualrho=rhoQ_actual+eta<46/25; CLOSED-CDF Prawitz/original-P bridge. Local identities derive M4; no extra atom/density/moment premise.",
        "freshness_premises": "SAME ORIGINAL DIRECTcorrect A1V2 and DIRECTexactGamma table, then DIRECT new common-nu modulus helper. PURE old arithmetic helpers only; no older evaluate call or numericJSON/flag/status/hash proof provenance.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_root_or_unrestricted_C4_proved": False,
            "ONE_COMPLETE_uniform_route_chosen_per_H_and_eta_cell": True,
            "monotone_relative_to_complete_frozen_V3_method": True,
            "V3_monotonicity_compares_the_SAME_remainder_switch": True,
            "refined_models_given_to_E29_ABS_or_physical_H_curvature": False,
            "Gamma_H_used_as_radius_or_actual_g_modulus_replaced": False,
            "negative_radius_clipped_or_eta_classes_masked": False,
            "polynomial_coefficients_or_endpoint_route_pieces_minimized": False,
            "old_CDF_evaluate_called_globals_patched_or_original_table_modified": False,
            "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": core.resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT,
            "DIRECT_new_modulus_helper_called": True, "CF_A1_Gamma_or_older_CDF_producer_called": False}}


def self_tests():
    """Dormant pure route/adaptation/sign checks, NO real radius/CDF producer."""
    source_drift_check()
    old = previous.self_tests()
    checks = old["exact_checks"]
    frequencies = [{"modulus": F(3, 5), "weight_int": SCALE // 7,
        "models": ((F(0), F(1), "cube"), (F(1, 3), F(0), "mass"), (F(8, 5), F(0), "unit"))}]
    augmented = [dict(frequencies[0], models=frequencies[0]["models"] +
        ((F(0), F(1, 2), "zero_price_response_norm"), (F(1, 50), F(-1, 10), "signed_norm")))]
    for two_disk in (False, True):
        old_R2, _ = core._fresh_weighted_R2(frequencies, F(0), F(1, 4), two_disk, lambda: None)
        new_R2, _ = core._fresh_weighted_R2(augmented, F(0), F(1, 4), two_disk, lambda: None)
        for M in (F(-1, 50), F(1, 50)):
            old_signed = core.ledger.per_H_signed_normalized_row(M, (F(0), F(-1, 20)), old_R2,
                F(0), F(0), F(1), F(0), F(1, 4))
            new_signed = core.ledger.per_H_signed_normalized_row(M, (F(0), F(-1, 20)), new_R2,
                F(0), F(0), F(1), F(0), F(1, 4))
            ABS = previous.complete_ABS_normalized_row(M, (F(0), F(1, 10)),
                F(0), F(0), F(1), F(0), F(1, 4))
            route, chosen = _choose_three_complete_routes(old_signed, new_signed, ABS)
            require(route in ROUTES and chosen["normalized_score_upper"] == min(
                    row["normalized_score_upper"] for row in (old_signed, new_signed, ABS)),
                    "THREE complete uniform scores, exact monotonicity without model persistence")
            checks += 1
    require(augmented[0]["modulus"] == frequencies[0]["modulus"]
            and augmented[0]["weight_int"] == frequencies[0]["weight_int"]
            and len(frequencies[0]["models"]) == 3,
            "Synthetic actual-g/weight and ORIGINAL baseline frequency object unchanged")
    checks += 1
    return {"exact_checks": checks, "CF_A1_Gamma_modulus_table_CDF_or_global_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
