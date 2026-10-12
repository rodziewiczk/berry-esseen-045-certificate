"""NEW postconsumer V3: per-H WHOLE-cell SIGNED or COMPLETE-ABS portfolio.

The SAME DIRECT-FRESH correct A1V2 table and exact Gamma table are required
as in frozen V2. No CF, A1, Gamma or older CDF producer is called here.
All older arithmetic and receipts stay unchanged. This new module reuses
only PURE V2/V1 input, curvature, radius/R2, Gamma and scalar helpers.

For one WHOLE closed eta cell, the audited E29 frozen_complete_ABS_cell
is called with raw_constant=0 ONLY to derive its complete transfer bound
 E_ABS(eta) <= C+D*eta, for sum |kappa|*|phi_P^4-g_Q^4|.
Its dummy acceptance, dummy target polynomial and dummy score are NEVER
used. The complete frozen-p telescope or complete endpoint cap is chosen
per q; outward coefficient rounding is already in E29. This ABS bound is
NOT an A1/Gamma bound and is NOT a second-order remainder bound.

At EACH H/reflection, using the very SAME normalized reference bound M_H,
ONE freshly proved local-or-old quad_H and ONE physical-H reserve, form
the two complete target polynomials:
 P_SIGNED = M_H+quad_H+H_reserve+2*Gamma_H+2*R2-T*eta;
 P_ABS    = M_H+quad_H+H_reserve+2*C+(2*D-T)*eta.
The raw factor2 appears ONCE in each full route. Never add both routes,
minimize their coefficients, or substitute C,D for a purported Gamma.
Each route is first independently checked on the ENTIRE closed cell.
Then choose ONE complete uniform score bound for this H/cell. Route
choice may vary between H/cells because both bound the SAME physical
Prawitz quantity, with the same original-P interpolation bridge. Max-H
is taken only after each complete per-H choice; a pointwise eta winner
need not persist, and no endpoint-min of different functions is used.

Both target polynomials have nonnegative quadratic leading coefficient
(zero for ABS). For P/(rhoQ_lo+eta), the derivative numerator satisfies
 N'=P''*(rhoQ_lo+eta)>=0, so there is no interior local maximum. The cap
denominator branch is convex. Hence the same sign-safe four endpoint /
denominator-face maximum is a uniform score for either numerator sign.
Strict negativity of the complete endpoint/Bernstein check is equivalent
to that entire-route score being below T. A complete per-H min of these
uniform scores is safe; coefficientwise or eta-endpointwise min is not.

ALL16 closed eta cells/joins, COMPLETE H58/115/229 grids, BOTH genuine
reflections and actual-law tails remain. UNKNOWN cells are retained.
Standing physical conditions: standardized iid actual P in declared BOX/
eta, |X|<=17/4, actualrho=rhoQ_actual+eta<46/25, retained CLOSED-CDF
Prawitz and original-P bridge. Local moments derive M4, not a new axiom.
DIRECT analytic provenance, not labels/status/hash/numeric JSON, proves
the input bounds. No entire-root/unrestricted C4 conclusion. Stdlib60s/
256MiB; dormant scalar tests only, no import-time jobs or write CLI.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_signed_A1_CDF_cell_consumer_v2_2026_10_09 as previous

core, local_quad = previous.previous, previous.local_quad
SCALE, TARGET, require = previous.SCALE, previous.TARGET, previous.require
TIME_LIMIT, MEMORY_LIMIT, ETA_CELLS = previous.TIME_LIMIT, previous.MEMORY_LIMIT, previous.ETA_CELLS
fixed_eta_cells = previous.fixed_eta_cells
PREVIOUS_PIN = "95172909e96a55d4f074c1ffc704d0c2ee8810ca51e520b1f141752885bb915c"


def source_drift_check():
    previous.source_drift_check()
    require(hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == PREVIOUS_PIN,
            "Frozen local-quad V2 arithmetic integrity only")


def dependency_pins():
    pins = previous.dependency_pins()
    # Include the upstream legacy PURE HG arithmetic used by the direct
    # fresh A1 producer; its quarantined CF/producer entry is never called.
    for path in (Path(__file__), Path(core.builder.previous.HG.__file__)):
        require(path.name not in pins, "Unique new portfolio/upstream PURE HG source labels")
        pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def complete_ABS_normalized_row(M_H, transfer, quad_H, H_reserve,
                                rhoQ_lo, L, U, target=TARGET, cap=local_quad.RHO_CAP):
    """Pure COMPLETE fourth-power ABS route, NOT a Gamma/R2 ledger call."""
    M, C, D, quad, curve, rho, target, cap = map(core.ledger.exact,
        (M_H, *transfer, quad_H, H_reserve, rhoQ_lo, target, cap))
    L, U = core.ledger.closed_interval(L, U)
    require(quad >= 0 and curve >= 0 and rho >= 1 and target > 0 and cap > 0
            and min(C + D * L, C + D * U) >= 0,
            "ONE proved reserve each and nonnegative WHOLE complete ABS transfer")
    # These exact checks do not establish that the supplied C,D actually
    # bound the complete complex transfer; that is E29's separate theorem.
    polynomial = (M + quad + curve + 2 * C, 2 * D - target, F(0))
    bernstein = core.ledger.degree2_bernstein(polynomial, L, U)
    left, right = bernstein[0], bernstein[2]
    faces = (left / cap, right / cap, left / (rho + L), right / (rho + U))
    score = max(F(0), target + max(faces))
    passed = all(value < 0 for value in bernstein)
    require(passed == (left < 0 and right < 0) and passed == (score < target),
            "Complete affine ABS endpoint/Bernstein/sign-safe uniform score agree")
    return {"normalized_target_polynomial": polynomial,
        "normalized_target_endpoint_uppers": (left, right),
        "degree2_Bernstein_coefficients": bernstein,
        "normalized_score_denominator_face_ratios": faces,
        "normalized_score_upper": score,
        "whole_cell_strict_numeric_inequality": passed,
        "complete_ABS_transfer_affine_upper": (C, D),
        "ONE_reserves": (quad, curve),
        "ABS_transfer_is_NOT_a_Gamma_or_R2_bound": True,
        "CDF_or_all_H_proved_here": False}


def _choose_complete_row_route(signed, ABS):
    """Choose ONE already WHOLE-cell proved score, never polynomial pieces."""
    route, chosen = min((("signed_A1_R2", signed), ("complete_ABS", ABS)),
                        key=lambda pair: (pair[1]["normalized_score_upper"], pair[0]))
    require(chosen["whole_cell_strict_numeric_inequality"] ==
            (signed["whole_cell_strict_numeric_inequality"] or ABS["whole_cell_strict_numeric_inequality"]),
            "Any ONE complete WHOLE-cell route suffices at this H/reflection")
    return route, dict(chosen)


def evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval, rectangle=None,
        N=256, H_step=F(1, 8), use_two_disk=True, time_limit_seconds=TIME_LIMIT):
    """Postconsumer only; BOTH tables need DIRECT mathematical provenance."""
    started = time.monotonic()
    rectangle = tuple(table["box_geometry"]["rectangle"] if rectangle is None else rectangle)
    core.cached.previous.checked_request(rectangle, eta_interval, N, H_step, ETA_CELLS, ETA_CELLS)
    require(type(use_two_disk) is bool and type(time_limit_seconds) in (int, float, F)
            and 0 < time_limit_seconds <= TIME_LIMIT,
            "Explicit complete-R2 switch/cooperative portfolio60s timer")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Signed/ABS postconsumer elapsed budget")
        peak = core.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Signed/ABS postconsumer256MiB")

    eta_cells = fixed_eta_cells(eta_interval)
    box, grid = core._check_fresh_inputs(table, gamma_table, rectangle, N, H_step, eta_cells)
    frequencies = core.H_leaf.transfer_frequencies(table["frequency_data"], box)
    gamma_rows = {(row["orientation"], row["H"]): row for row in gamma_table["rows"]}
    centre_rows = {(row["orientation"], row["H"]): row for row in table["rows"]}
    cells = []
    for L, U in eta_cells:
        guard()
        curve = core.H_leaf.compact_cell_curvature(table["frequency_data"], box, L, U, H_step, N)
        H_reserve = F(curve["physical_H_reserve_upper_int"], SCALE)
        R2, choices = core._fresh_weighted_R2(frequencies, L, U, use_two_disk, guard)
        # The raw_constant=0 acceptance/score has NO analytic meaning here.
        # Only the separately proved complete transfer C,D and diagnostics
        # are used, on the SAME actual moduli/radius/weights and whole cell.
        dummy_ABS = core.cached.previous.frozen_complete_ABS_cell(
            frequencies, F(0), box["rhoQ_lo"], L, U)
        C, D = dummy_ABS["transfer_affine_upper"]
        moments = local_quad.whole_cell_moment_uppers(rectangle, (L, U))
        row_results, route_counts = [], {"signed_A1_R2": 0, "complete_ABS": 0}
        for H in grid:
            guard()
            quad_model = local_quad.physical_quad_at_H(moments, H, N)
            quad_H = quad_model["ONE_selected_physical_quad_upper_exact"]
            require(0 <= quad_H <= F(687, 8 * N * N), "ONE complete scalar local/old quad intersection")
            for orientation in (1, -1):
                guard()
                key = orientation, H
                gamma_index, gamma_model = core._choose_gamma(gamma_rows[key]["models"], L, U)
                M_H = F(centre_rows[key]["raw_minus_target_rhoQ_upper_int"], SCALE)
                signed = core.ledger.per_H_signed_normalized_row(M_H, gamma_model, R2,
                    quad_H, H_reserve, box["rhoQ_lo"], L, U, TARGET, local_quad.RHO_CAP)
                ABS = complete_ABS_normalized_row(M_H, (C, D), quad_H,
                    H_reserve, box["rhoQ_lo"], L, U, TARGET, local_quad.RHO_CAP)
                route, chosen = _choose_complete_row_route(signed, ABS)
                chosen.update({"orientation": orientation, "H": H,
                    "normalized_reference_center_upper_exact": M_H,
                    "selected_WHOLE_cell_route": route,
                    "complete_signed_row_proof": signed,
                    "complete_ABS_row_proof": ABS,
                    "frozen_gamma_model_index": gamma_index,
                    "ONE_local_physical_quad_model": quad_model})
                route_counts[route] += 1
                row_results.append(chosen)
        require(len(row_results) == 2 * len(grid) and sum(route_counts.values()) == len(row_results),
                "Every COMPLETE row/route is checked, never partial-H proof mixing")
        worst = max(row_results, key=lambda row: row["normalized_score_upper"])
        passed = all(row["whole_cell_strict_numeric_inequality"] for row in row_results)
        require(passed == (worst["normalized_score_upper"] < TARGET),
                "Max only AFTER all per-H WHOLE-cell route choices")
        cells.append({"lower": L, "upper": U, "passed": passed,
            "score_upper": worst["normalized_score_upper"], "worst_complete_H_row": worst,
            "H_reflection_rows_checked": len(row_results), "complete_route_counts": route_counts,
            "signed_route_weighted_R2_upper_polynomial": R2,
            "complete_ABS_transfer_affine_upper": (C, D),
            "complete_ABS_model_counts": dummy_ABS["selected_model_counts"],
            "complete_ABS_choices_digest_integrity_only": dummy_ABS["choices_digest_integrity_only"],
            "physical_H_curvature": curve, "whole_cell_physical_moment_uppers": moments,
            "complete_signed_R2_choices_digest_integrity_only":
                hashlib.sha256(repr(choices).encode("ascii")).hexdigest(),
            "signed_remainder_methods_used": tuple(sorted({method for _, method in choices}))})
    certificate, tail_lower = (table["metadata"]["fresh_target_certificate"],
                               table["metadata"]["positive_tail_Phi_lower_int"])
    require(certificate["target"] == TARGET and type(certificate["CE_lower_exact"]) is F
            and certificate["CE_lower_exact"] > TARGET and type(tail_lower) is int
            and 5 * tail_lower > 4 * SCALE, "Fresh target below CE/actual-law tails unchanged")
    tail, upper = F(2, 5), max([F(2, 5)] + [cell["score_upper"] for cell in cells])
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "ALL16 eta/H/reflections/tails strictly pass")
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "All mathematical sources unchanged through portfolio evaluation")
    guard()
    return {"status": "EXACT_CONDITIONAL_FRESH_SIGNED_OR_COMPLETE_ABS_LOCAL_QUAD_BOX_ETA" if passed else "UNKNOWN",
        "scale": SCALE, "target": TARGET, "N": N, "H_step": H_step,
        "closed_rectangle": rectangle, "closed_eta_cover": tuple(eta_interval), "cells": cells,
        "unresolved_eta_cell_indices": tuple(i for i, cell in enumerate(cells) if not cell["passed"]),
        "summary": {"score_upper_exact": upper, "failed_eta_cells": sum(not cell["passed"] for cell in cells),
            "ALL_H_nodes": len(grid), "ALL_H_reflection_rows_per_cell": 2 * len(grid),
            "fixed_closed_eta_cells": ETA_CELLS},
        "reserves_once": {"physical_quad": "PER_H_WHOLE_CLOSED_ETA_SCALAR_REPLACEMENT",
            "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "actual_law_tail_score_upper": tail, "fresh_target_certificate": certificate,
        "physical_premises": "Standardized iid actual P in declaredBOX/eta, |X|<=17/4,actualrho=rhoQ_actual+eta<46/25; CLOSED-CDF Prawitz/original-P bridge. Contact moment identities derive localM4; no extra M4/atom-count/density premise.",
        "freshness_premises": "SAME DIRECTcorrect A1V2 table and DIRECTexactGamma compiler; V2/V1/E29 PURE helpers only, NONE of their evaluate/producer functions called; schema/status/hash/numericJSON is not analytic provenance.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_root_or_unrestricted_C4_proved": False,
            "ONE_complete_uniform_route_chosen_per_H_and_eta_cell": True,
            "M_H_Gamma_H_local_quad_combined_before_max": True,
            "ABS_transfer_labeled_as_Gamma_or_R2": False,
            "polynomial_coefficient_or_pointwise_eta_minimum_used": False,
            "older_evaluate_called_or_globals_monkeypatched": False,
            "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": core.resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "CF_A1_Gamma_or_older_CDF_producer_called": False}}


evaluate_fresh_signed_ABS_A1_CDF = evaluate_fresh_signed_A1_CDF


def self_tests():
    """Dormant pure V2 scalars plus BOTH-sign denominator/whole-route checks."""
    source_drift_check()
    old = previous.self_tests()
    checks = old["exact_checks"]
    for M in (F(-1, 50), F(1, 50)):
        for C, D in ((F(0), F(0)), (F(1, 20), F(-1, 20)), (F(0), F(1, 100))):
            result = complete_ABS_normalized_row(M, (C, D), F(1, 10000),
                F(1, 10000), F(1), F(0), F(1))
            endpoints = result["normalized_target_endpoint_uppers"]
            require(result["whole_cell_strict_numeric_inequality"] == (max(endpoints) < 0)
                    and result["degree2_Bernstein_coefficients"][1] == sum(endpoints) / 2,
                    "COMPLETE affine transfer has exact endpoint/Bernstein criterion")
            for j in range(9):
                eta = F(j, 8)
                value = core.ledger.evaluate(result["normalized_target_polynomial"], eta)
                for rho in (F(1) + eta, local_quad.RHO_CAP):
                    require(TARGET + value / rho <= result["normalized_score_upper"],
                            "Both numerator signs and denominator faces uniformly enclosed")
                    checks += 1
            checks += 1
    low = complete_ABS_normalized_row(F(-1, 50), (F(0), F(0)), F(0), F(0), F(1), F(0), F(1))
    high = complete_ABS_normalized_row(F(1, 50), (F(1, 50), F(0)), F(0), F(0), F(1), F(0), F(1))
    for signed, ABS in ((low, high), (high, low), (low, low), (high, high)):
        _, chosen = _choose_complete_row_route(signed, ABS)
        require(chosen["normalized_score_upper"] == min(signed["normalized_score_upper"], ABS["normalized_score_upper"]),
                "Minimum of two WHOLE-cell uniform scores, not pieces/coefficients")
        checks += 1
    return {"exact_checks": checks, "CF_A1_Gamma_CDF_or_global_producer_called": False,
        "old_source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
