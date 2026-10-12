"""Fresh whole-box CDF leaf with continuous-frequency physical H curvature.

DIRECT fresh audited cached leaf supplies TRUE nominal CFs, whole-box
centres and ACTUAL reference moduli. Its old acceptance/score is ignored.
For EACH entire fixed CLOSED eta cell, the continuous-frequency lemma
replaces ONE old H reserve. The original physical quad reserve remains
ONE 687/(8*N^2); all H nodes, both genuine reflections and tails remain.
The complete fourth-power transfer is recomputed by the audited pure E29
arithmetic, not taken from a numerical JSON/status or coefficient minimum.

For B>=sup|J_P''|, first ceil B to scale S, then ceil
h^2*(B_up+1/4)/16 to S. Both roundings only enlarge the bound. This
reserve is CONSTANT on the WHOLE eta cell, irrespective of the transfer
model choices. It bounds interpolation of the PHYSICAL continuous J_P,
not the midpoint quadrature table. No second quad/frequency reserve.

The exact private consumer recomputes curvature, transfer, denominator,
degree1 Bernstein arithmetic, complete eta/H/reflection scope and tails
AFTER the DIRECT mathematical producer. Schemas, hashes and flags alone
never establish those producers' analytic premises. No import of receipts.

Conditional scope: standardized iid actual P, canonical coordinates in
the declared box, eta>=0, |X|<=17/4, actualrho<46/25, retained CLOSED-CDF
Prawitz/physical bridge. Owner placement and literature inputs remain
external; this module alone does NOT prove unrestricted C4. Stdlib only,
one externally coordinated sequential job, 60s/256MiB. CLI tiny tests only.
Preserve every older source/receipt; no import-time producer or file writes.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_fresh_cached_low_eta_box_leaf_2026_10_09 as cached
import n4_frequency_local_physical_H_curvature_2026_10_09 as curvature

SCALE, TARGET, require = cached.SCALE, cached.TARGET, cached.require
N, H_STEP, ETA_CELLS = 256, F(1, 8), 16
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
CACHED_PIN = "4bf4a90a3eae9ed88b8a9e02d27e02ef53d4bef7b836fe426bf3dcfa49c3bd9f"
CURVATURE_PIN = "6d0c5f1142016721f261bb63715788c21c62b6cd152a1f2538db38cf0e86aa5b"


def source_drift_check():
    for module, pin in ((cached, CACHED_PIN), (curvature, CURVATURE_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen source integrity only: " + Path(module.__file__).name)


def compact_cell_curvature(frequency_data, box, L, U, H_step, N):
    """Pure exact math under freshly proved modulus/geometry premises."""
    bound = curvature.from_preverified_box_frequency_data(
        frequency_data, box, (L, U), H_step, N=N, scale=SCALE)
    B = bound["J_second_derivative_uppers"]["complete_integral_intersection"]
    B_int = curvature.ceil_scaled(B, SCALE)
    H_int = curvature.ceil_scaled(H_step ** 2 * (F(B_int, SCALE) + F(1, 4)) / 16, SCALE)
    require(F(B_int, SCALE) >= B and F(H_int, SCALE) >= bound["physical_H_reserve"]
            and F(H_int, SCALE) <= F(25, 64) * H_step ** 2 + F(2, SCALE),
            "Two outward ceilings, never a smaller interpolating reserve")
    return {"J_second_derivative_upper_int": B_int,
            "physical_H_reserve_upper_int": H_int,
            "continuous_frequency_Lipschitz_fill": F(3, 2 * N),
            "continuous_kernel_cell_integral_intersection_sum":
                bound["kernel_weight_sums"]["complete_integral_intersection"]}


def transfer_frequencies(frequency_data, box):
    return [{"modulus": F(item["g_actual_modulus_upper_int"], SCALE),
             "weight_int": item["kernel_modulus_upper_int"],
             "models": cached.previous.affine_radius_models(
                 item["q"], F(item["g_actual_modulus_upper_int"], SCALE), box)}
            for item in frequency_data]


def compute_verified_low_eta_box_leaf(rectangle, eta_interval, cache=None,
        N=256, H_step=F(1, 8), initial_eta_cells=16, max_eta_cells=16,
        time_limit_seconds=TIME_LIMIT):
    started = time.monotonic()
    rectangle, eta_interval = cached.previous.checked_request(
        rectangle, eta_interval, N, H_step, initial_eta_cells, max_eta_cells)
    require(initial_eta_cells == max_eta_cells, "Fixed entire eta cover")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Bounded whole-leaf timer")
    source_drift_check()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "H-curvature leaf elapsed budget")
        peak = cached.previous.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "H-curvature leaf256MiB")

    # Only the DIRECT fresh mathematical producer supplies these premises.
    fresh = cached.compute_verified_cached_low_eta_box_leaf(rectangle, eta_interval, cache,
        N=N, H_step=H_step, use_contact_taylor=True,
        initial_eta_cells=initial_eta_cells, max_eta_cells=max_eta_cells,
        time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    box, rho = fresh["box_geometry"], fresh["box_geometry"]["rhoQ_lo"]
    frequencies = transfer_frequencies(fresh["frequency_data"], box)
    center = F(max(r["raw_Q_center_upper_int"]
                   for r in fresh["reference_centers_both_orientations"]), SCALE)
    quad = F(687, 8 * N * N)
    cells = []
    for old in fresh["cells"]:
        guard()
        L, U = old["lower"], old["upper"]
        curve = compact_cell_curvature(fresh["frequency_data"], box, L, U, H_step, N)
        raw = center + quad + F(curve["physical_H_reserve_upper_int"], SCALE)
        cell = cached.previous.frozen_complete_ABS_cell(frequencies, raw, rho, L, U)
        require(cell["transfer_affine_upper"] == old["transfer_affine_upper"],
                "Pure complete transfer independent of the replaced H reserve")
        cell["physical_H_curvature"] = curve
        cell["raw_constant_with_one_quad_and_one_H"] = raw
        cells.append(cell)
    tail = fresh["tail"]["score_upper"]
    upper = max([tail] + [c["score_upper"] for c in cells])
    passed = all(c["passed"] for c in cells) and tail < TARGET
    require(not passed or upper < TARGET, "ALL eta/H/reflections/tails strict")
    # Old raw-score/reserve/status fields are replaced, not added to the proof.
    fresh.update({"status": "EXACT_CONDITIONAL_H_CURVATURE_LOW_ETA_BOX" if passed else "UNKNOWN",
        "cells": cells, "reserves_once": {"physical_quad": quad,
            "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "proof_scope": "DIRECT corrected fresh TRUE Q centres/actual moduli; complete ABS transfer; ONE physical quad; ONE continuous-frequency H reserve per whole closed eta cell; all H/reflections/tails. Old H reserve NOT added.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_global_root_covered": False, "unrestricted_C4_proved": False,
            "saved_numeric_JSON_or_float_proof_inputs": False,
            "old_sources_or_receipts_modified": False}})
    fresh["summary"].update({"score_upper_exact": upper, "strict_margin_exact": TARGET - upper,
                            "failed_eta_cells": sum(not c["passed"] for c in cells)})
    fresh["source_pins_integrity_only"].update({p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__), Path(curvature.__file__))})
    fresh["resources"].update({"elapsed_seconds_diagnostic": time.monotonic() - started,
                               "peak_working_set_bytes": cached.previous.resources.peak_bytes()})
    source_drift_check()
    guard()
    return fresh


def _checked_fresh_leaf_math(fresh, request):
    """Exact consumer AFTER DIRECT fresh leaf; not a numerical JSON importer."""
    rectangle, cut, rho = request["closed_rectangle"], request["etaSV_exact"], request["rhoQ_lower_exact"]
    require(cut > 0 and fresh["scale"] == SCALE and fresh["N"] == N
            and fresh["target"] == TARGET and fresh["H_step"] == H_STEP
            and fresh["closed_rectangle"] == rectangle
            and fresh["closed_eta_cover"] == (F(0), cut), "Same COMPLETE request")
    box = fresh["box_geometry"]
    require(box["rhoQ_lo"] == rho and tuple(box["rectangle"]) == rectangle,
            "Whole-box actual normalization lower")
    grid = cached.previous.complete_H_grid(H_STEP)
    rows = fresh["reference_centers_both_orientations"]
    require(len(rows) == 2 * len(grid) and {(r["orientation"], r["H"]) for r in rows}
            == {(s, H) for s in (1, -1) for H in grid}
            and all(type(r["raw_Q_center_upper_int"]) is int for r in rows),
            "Every H and BOTH genuine orientations")
    quad = F(687, 8 * N * N)
    require(fresh["reserves_once"] == {"physical_quad": quad,
                "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"}, "ONE quad/ONE replaced H")
    tail = fresh["tail"]["score_upper"]
    require(tail == F(2, 5) and tail < TARGET
            and type(fresh["tail"]["Phi_25_16_lower_int"]) is int
            and 5 * fresh["tail"]["Phi_25_16_lower_int"] > 4 * SCALE, "Fresh actual-law tails")
    target_cert = fresh["reference_metadata"]["fresh_target_certificate"]
    require(target_cert["target"] == TARGET and type(target_cert["CE_lower_exact"]) is F
            and target_cert["CE_lower_exact"] > TARGET, "Fresh T below CE")
    frequencies = transfer_frequencies(fresh["frequency_data"], box)
    center = F(max(r["raw_Q_center_upper_int"] for r in rows), SCALE)
    require(len(fresh["cells"]) == ETA_CELLS, "Fixed16 complete eta partition")
    checked, unresolved = [], []
    for j, cell in enumerate(fresh["cells"]):
        L, U = cut * F(j, ETA_CELLS), cut * F(j + 1, ETA_CELLS)
        require((cell["lower"], cell["upper"]) == (L, U), "No missing eta interval/faces")
        curve = compact_cell_curvature(fresh["frequency_data"], box, L, U, H_STEP, N)
        raw = center + quad + F(curve["physical_H_reserve_upper_int"], SCALE)
        exact = cached.previous.frozen_complete_ABS_cell(frequencies, raw, rho, L, U)
        require(cell["physical_H_curvature"] == curve
                and cell["raw_constant_with_one_quad_and_one_H"] == raw
                and all(cell[key] == value for key, value in exact.items()),
                "Recomputed curvature/COMPLETE transfer/endpoints/Bernstein/denominator, not flags")
        record = {"eta_closed_interval": (L, U),
            "complete_transfer_affine_upper": exact["transfer_affine_upper"],
            "raw_endpoint_uppers": exact["raw_endpoint_uppers"],
            "target_Bernstein_coefficients": exact["target_Bernstein_coefficients"],
            "score_upper_exact": exact["score_upper"],
            "strict_numeric_bound_verified": exact["passed"],
            "physical_H_curvature": curve}
        checked.append(record)
        if not exact["passed"]:
            unresolved.append(record)
    upper = max([tail] + [r["score_upper_exact"] for r in checked])
    passed = not unresolved and upper < TARGET
    require(fresh["summary"]["score_upper_exact"] == upper, "Whole child rederived")
    return {"kind": "FRESH_LOW_ETA_WHOLE_BOX_CDF_BOUND" if passed else "UNKNOWN_NUMERIC_LOW_ETA_WHOLE_BOX",
        "low_eta_closed_scope": (F(0), cut), "low_eta_cells": checked,
        "unresolved_low_eta_cells": unresolved, "low_eta_upper_exact": upper,
        "conditional_whole_low_eta_CDF_bound_verified": passed,
        "both_orientations_H_nodes_checked": len(grid), "reference_center_rows_checked": len(rows),
        "physical_reserves_once": {"physical_quad": quad,
            "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "actual_law_tail_upper_exact": tail, "worst_fresh_reference_center": fresh["worst_Q_center"],
        "contact_Taylor_diagnostic": fresh["reference_metadata"]["contact_Taylor"],
        "reported_child_status_not_a_proof_premise": True}


def self_tests():
    source_drift_check()
    checks = curvature.self_tests()["exact_checks"]
    for B in (F(0), F(1, 3), F(6)):
        for h in (F(1, 8), F(1, 16), F(1, 32)):
            b = F(curvature.ceil_scaled(B, SCALE), SCALE)
            reserve = F(curvature.ceil_scaled(h ** 2 * (b + F(1, 4)) / 16, SCALE), SCALE)
            require(reserve >= h ** 2 * (B + F(1, 4)) / 16
                    and reserve < F(19, 32) * h ** 2, "Replacement outward and strictly sharper")
            checks += 2
    return {"status": "TINY_H_CURVATURE_LEAF_ARITHMETIC_ONLY", "exact_checks": checks,
            "fresh_cache_CF_leaf_or_root_producer_called": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
