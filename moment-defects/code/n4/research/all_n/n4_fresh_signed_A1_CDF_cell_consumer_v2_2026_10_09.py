"""NEW signed A1 postconsumer V2: ONLY per-H local physical quadrature.

Use the SAME DIRECT-FRESH correct A1V2 table and exact Gamma compiler on
the SAME16 CLOSED eta cells/geometry/q/H grid. Pure frozen-v1 scope,
radius/R2, Gamma-choice and typed arithmetic helpers are reused; its CDF
evaluate function is NEVER called, and no v1 globals are monkeypatched.
The only bound change is the fresh pure local-moment midpoint reserve.

For each WHOLE closed eta cell, recompute physical rho/skew/M4 upper
bounds from the canonical geometry and eta interval using exact cubic/
quartic W identities. No saved moments or extra M4 axiom. At EACH H,
use the freshly proved scalar minimum of the local raw midpoint reserve
and old687/(8N^2). Combine quad_H with THAT M_H+2Gamma_H+2R2-T eta BEFORE
maximizing H/reflections. The physical continuous-H reserve is separate
and still added ONCE. No partial-H route mixing or coefficient minima.

Every original CF/response/price/radius/normalized centre, whole-cell
primary/disk/two-disk remainder choice, signed coefficient and correct
denominator-face score is unchanged. All16 eta cells/joins, complete
H58/115/229 grid, BOTH genuine reflections, tails and T<CE remain.
No ABS portfolio is added in this version. Each UNKNOWN scope remains
explicit. The input bounds require DIRECT audited producers, not schema,
flags, hashes, statuses or numerical JSON. Original P need not be finite.

Standing physical conditions remain standardized iid actual P, declared
BOX/eta, |X|<=17/4,actualrho=rhoQ_actual+eta<46/25,CLOSED-CDF Prawitz and
retained original-P bridge. The local helper derives M4 from these
premises; it adds none. First-critical all-law placement stays external;
this source alone proves no full root/unrestricted C4. Stdlib60s/256MiB,
source-only until authorized, dormant tiny scalar tests only. No import-
time jobs or producer/replay/file-write CLI. All old files preserved.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_signed_A1_CDF_cell_consumer_2026_10_09 as previous
import n4_local_physical_moment_quadrature_2026_10_09 as local_quad

SCALE, TARGET, require = previous.SCALE, previous.TARGET, previous.require
TIME_LIMIT, MEMORY_LIMIT, ETA_CELLS = previous.TIME_LIMIT, previous.MEMORY_LIMIT, previous.ETA_CELLS
fixed_eta_cells = previous.fixed_eta_cells
PREVIOUS_PIN = "6ec11db2518d5dc7b07e06a6d44fc219c46acb4171b5dbc1b934e3c2df049f1f"
LOCAL_PIN = "8bdda6a54978a9b55a894e4d692887c40e32c8a546fe57a7c7cb9dabd77e803b"


def source_drift_check():
    previous.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (local_quad, LOCAL_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen local-quad arithmetic integrity only")
    require(SCALE == local_quad.SCALE and previous.ledger.DEFAULT_CAP == local_quad.RHO_CAP,
            "Matching physical units/cap")


def dependency_pins():
    pins = previous.dependency_pins()
    for path in (Path(__file__), Path(local_quad.__file__)):
        require(path.name not in pins, "Unique new local-quad source labels")
        pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval, rectangle=None,
        N=256, H_step=F(1, 8), use_two_disk=True, time_limit_seconds=TIME_LIMIT):
    """PURE-v1 input/helpers AFTER DIRECT producers; NOT v1 evaluate call."""
    started = time.monotonic()
    rectangle = tuple(table["box_geometry"]["rectangle"] if rectangle is None else rectangle)
    previous.cached.previous.checked_request(rectangle, eta_interval, N, H_step, ETA_CELLS, ETA_CELLS)
    require(type(use_two_disk) is bool and type(time_limit_seconds) in (int, float, F)
            and 0 < time_limit_seconds <= TIME_LIMIT, "Explicit remainder switch/cooperative local60s timer")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Local signed postconsumer elapsed budget")
        peak = previous.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Local signed postconsumer256MiB")

    eta_cells = fixed_eta_cells(eta_interval)
    box, grid = previous._check_fresh_inputs(table, gamma_table, rectangle, N, H_step, eta_cells)
    frequencies = previous.H_leaf.transfer_frequencies(table["frequency_data"], box)
    gamma_rows = {(row["orientation"], row["H"]): row for row in gamma_table["rows"]}
    centre_rows = {(row["orientation"], row["H"]): row for row in table["rows"]}
    cells = []
    for L, U in eta_cells:
        guard()
        curve = previous.H_leaf.compact_cell_curvature(table["frequency_data"], box, L, U, H_step, N)
        H_reserve = F(curve["physical_H_reserve_upper_int"], SCALE)
        R2, choices = previous._fresh_weighted_R2(frequencies, L, U, use_two_disk, guard)
        moments = local_quad.whole_cell_moment_uppers(rectangle, (L, U))
        row_results = []
        for H in grid:
            guard()
            quad_model = local_quad.physical_quad_at_H(moments, H, N)
            quad_H = quad_model["ONE_selected_physical_quad_upper_exact"]
            require(0 <= quad_H <= F(687, 8 * N * N), "ONE complete scalar local/old intersection")
            for orientation in (1, -1):
                guard()
                key = orientation, H
                gamma_index, gamma_model = previous._choose_gamma(gamma_rows[key]["models"], L, U)
                M_H = F(centre_rows[key]["raw_minus_target_rhoQ_upper_int"], SCALE)
                result = previous.ledger.per_H_signed_normalized_row(M_H, gamma_model, R2,
                    quad_H, H_reserve, box["rhoQ_lo"], L, U, TARGET, local_quad.RHO_CAP)
                result.update({"orientation": orientation, "H": H,
                    "normalized_reference_center_upper_exact": M_H,
                    "frozen_gamma_model_index": gamma_index,
                    "ONE_local_physical_quad_model": quad_model})
                row_results.append(result)
        require(len(row_results) == 2 * len(grid), "ALL local WHOLE-cell H/reflection rows checked")
        worst = max(row_results, key=lambda row: row["normalized_score_upper"])
        passed = all(row["whole_cell_strict_numeric_inequality"] for row in row_results)
        require(passed == (worst["normalized_score_upper"] < TARGET), "Max AFTER full per-H normalized ledger")
        cells.append({"lower": L, "upper": U, "passed": passed,
            "score_upper": worst["normalized_score_upper"], "worst_complete_H_row": worst,
            "H_reflection_rows_checked": len(row_results), "weighted_R2_upper_polynomial": R2,
            "physical_H_curvature": curve, "whole_cell_physical_moment_uppers": moments,
            "complete_R2_choices_digest_integrity_only": hashlib.sha256(repr(choices).encode("ascii")).hexdigest(),
            "remainder_methods_used": tuple(sorted({method for _, method in choices}))})
    certificate, tail_lower = (table["metadata"]["fresh_target_certificate"],
                               table["metadata"]["positive_tail_Phi_lower_int"])
    require(certificate["target"] == TARGET and type(certificate["CE_lower_exact"]) is F
            and certificate["CE_lower_exact"] > TARGET and type(tail_lower) is int
            and 5 * tail_lower > 4 * SCALE, "Fresh target below CE/actual-law tails unchanged")
    tail, upper = F(2, 5), max([F(2, 5)] + [cell["score_upper"] for cell in cells])
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "All16 eta/H/reflections/tails strictly pass")
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "All mathematical sources unchanged through local evaluator")
    guard()
    return {"status": "EXACT_CONDITIONAL_FRESH_SIGNED_A1_LOCAL_QUAD_BOX_ETA" if passed else "UNKNOWN",
        "scale": SCALE, "target": TARGET, "N": N, "H_step": H_step,
        "closed_rectangle": rectangle, "closed_eta_cover": tuple(eta_interval), "cells": cells,
        "unresolved_eta_cell_indices": tuple(i for i, cell in enumerate(cells) if not cell["passed"]),
        "summary": {"score_upper_exact": upper, "failed_eta_cells": sum(not cell["passed"] for cell in cells),
            "ALL_H_nodes": len(grid), "ALL_H_reflection_rows_per_cell": 2 * len(grid), "fixed_closed_eta_cells": ETA_CELLS},
        "reserves_once": {"physical_quad": "PER_H_WHOLE_CLOSED_ETA_SCALAR_REPLACEMENT",
            "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "actual_law_tail_score_upper": tail, "fresh_target_certificate": certificate,
        "physical_premises": "Standardized iid actual P in declaredBOX/eta, |X|<=17/4,actualrho=rhoQ_actual+eta<46/25; CLOSED-CDF Prawitz/original-P bridge. Contact moment identities derive localM4; no extra M4/atom-count/density premise.",
        "freshness_premises": "SAME DIRECTcorrect A1V2 table and DIRECTexactGamma compiler; PUREv1 only, v1evaluate NOTcalled; schema/status/hash/numericJSON is not proof provenance.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_root_or_unrestricted_C4_proved": False,
            "local_quad_paired_with_M_H_and_Gamma_H_before_max": True,
            "v1_evaluate_called_or_globals_monkeypatched": False,
            "ABS_portfolio_added": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": previous.resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "CF_A1_Gamma_or_v1_CDF_producer_called": False}}


def self_tests():
    """Dormant pure old scalar checks plus local-reserve pointwise dominance."""
    source_drift_check()
    old = previous.self_tests()
    checks = old["exact_checks"]
    for eta in (F(0), F(1, 10), F(1, 2)):
        moments = local_quad.whole_cell_moment_uppers((F(1), F(1), F(0), F(0)), (F(0), eta))
        for H in (F(-4), F(-1, 2), F(0), F(25, 8)):
            model = local_quad.physical_quad_at_H(moments, H)
            require(0 <= model["ONE_selected_physical_quad_upper_exact"] <= F(687, 8 * 256 * 256)
                    and model["H_interpolation_reserve_added"] is False,
                    "ONE localquad never weaker than old and does not add H reserve")
            checks += 1
    return {"exact_checks": checks, "CF_A1_Gamma_CDF_or_global_producer_called": False,
        "old_source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
