"""NEW optimized-radius V5 consumer; ORIGINAL V4 bound arithmetic.

The SAME ORIGINAL DIRECT fresh correct A1V2 table and SAME DIRECT
original Gamma table are required. PURE V4 input/adaptation/route helpers
are reused without calling V4.evaluate or patching its globals. The
production evaluator is its unchanged three-route arithmetic with ONLY
the full-radius compiler binding changed to NEW32a3/193 exact-LCM code.
Default mode is five_budget; response_norm remains an explicit option.

All selected physical A,S/prices, negative-model filters, radius/R2
mathematics and row/cell choices coincide with frozen10e/V4 on the SAME
fresh inputs and explicit mode. Only source-integrity closure differs.
This does NOT claim equality based on saved JSON; a later authorized
comparison must freshly build BOTH chains from the SAME original
A1/Gamma mathematical data. New29 scalar tests do not establish that
real comparison or an actual CDF outcome.

Most importantly, physical H curvature remains ORIGINAL baseline-only.
The new optional compact_refined_H_curvature helper is NOT called here.
No simultaneous H-reserve change, new quadrature, eta feasibility mask,
refined models in E29 ABS, actual g/kernel substitution or table mutation.
Three COMPLETE uniform row scores (baseline signed, refined signed,
baseline ABS) retain their exact per-H M/Gamma/local quad/H correlation.
All16 closed eta joins, H58/115/229 and true reflections/tails survive.

Standing physical/provenance premises are EXACTLY V4's: arbitrary
standardized iid actual P in BOX/eta, support17/4,actualrho<46/25,
retained CLOSED-CDF Prawitz/original-P bridge, DIRECT fresh analytic
input bounds. No original finite-atom/density/extra-M4 axiom, no full
root/C4 claim. Source pins are integrity only. Cooperative60s/256MiB,
no import-time jobs, old evaluate call, file writes or producer CLI.
Dormant tiny pure regressions only. Older frozen sources stay untouched.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_signed_A1_CDF_cell_consumer_v4_2026_10_09 as previous
import n4_Q3_fresh_common_nu_modulus_radius_models_v3_2026_10_09 as modulus_radius

core, local_quad = previous.core, previous.local_quad
SCALE, TARGET, require = previous.SCALE, previous.TARGET, previous.require
TIME_LIMIT, MEMORY_LIMIT, ETA_CELLS = previous.TIME_LIMIT, previous.MEMORY_LIMIT, previous.ETA_CELLS
fixed_eta_cells, ROUTES = previous.fixed_eta_cells, previous.ROUTES
PREVIOUS_PIN = "684568bb773216737fc0a9b158475e8d0e6ea11183d859ab22f56dae9dae138d"
RADIUS_PIN = "32a3b1b16e22801d27c45a2883fa215878b11ca7076f39382b2946fb0e0b7f0a"

# Reuse ONLY already-audited PURE functions on direct fresh output data.
_checked_modulus_identity = previous._checked_modulus_identity
_augment_signed_frequencies = previous._augment_signed_frequencies
_choose_three_complete_routes = previous._choose_three_complete_routes


def source_drift_check():
    previous.source_drift_check()
    modulus_radius.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (modulus_radius, RADIUS_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen original bound/optimized arithmetic integrity only")
    require(SCALE == modulus_radius.SCALE, "SAME physical radius/CF/kernel units")


def dependency_pins():
    pins = previous.dependency_pins()
    for path in (Path(__file__), Path(modulus_radius.__file__), Path(modulus_radius.previous.__file__)):
        pin = hashlib.sha256(path.read_bytes()).hexdigest()
        require(path.name not in pins or pins[path.name] == pin, "Consistent new optimized source closure")
        pins[path.name] = pin
    return pins


def evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval, rectangle=None,
        N=256, H_step=F(1, 8), use_two_disk=True, modulus_radius_mode="five_budget",
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
                ABS = previous.previous.complete_ABS_normalized_row(M_H, (C, D), quad_H,
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
    """Dormant V4 scalars and NEW corrected29 LCM checks; NO real producer."""
    source_drift_check()
    original = previous.self_tests()
    optimized = modulus_radius.self_tests()
    require(optimized["exact_checks"] == 29, "NEW explicit-scale regressions, not old193.self_tests")
    require(modulus_radius.actual_response_norm_uppers is previous.modulus_radius.actual_response_norm_uppers
            and modulus_radius.previous.previous is previous.modulus_radius,
            "Unchanged fast API and10e pure mathematical dependency, no monkeypatch")
    return {"exact_checks": original["exact_checks"] + optimized["exact_checks"] + 1,
        "CF_A1_Gamma_real_radius_CDF_or_global_producer_called": False,
        "old_V4_evaluate_or_old193_failing_selftest_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}

