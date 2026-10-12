"""Same corrected whole-BOX Prawitz leaf, DIRECT-FRESH shared quadrature.

No box, H, reflection or eta face is removed. Kernels, phases and Gaussian
intervals are freshly built ONCE by the audited immutable quadrature
builder. CFs, roots, geometry errors, center gradients/Hessians and radius
transfers remain fresh for EACH box. Rational-BAR derivative values are
evaluated once per q/box for signed and radial gradients; they NEVER
replace the TRUE irrational nominal CF baseline.

All product/phase ordering and bounds are those of frozen corrected E29.
No legacy CF producer, saved numeric JSON or monkeypatch is used. Supplied
cache mathematical validity requires the coordinating producer's DIRECT
fresh builder call, not a schema/type/hash flag. Both physical reserves
are still added ONCE. Complete H58/115/229 grids, genuine reflections,
all fixed CLOSED eta cells and actual-law tails are retained.

Standing conditional premises remain standardized iid actual P,
canonical geometry/eta in the declared box/interval, |X|<=17/4,
actualrho<46/25, CLOSED-CDF Prawitz and the retained original-P bridge.
No finite-atom/M4 assumption is added; UNKNOWN is an upper-bound failure,
not a counterexample. This module does NOT prove the full root or C4.
60s/256MiB, stdlib, externally coordinated. CLI tiny scope tests ONLY.
Preserve every older source and receipt.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_generic_low_eta_center_only_exact_box_leaf_2026_10_09 as previous
import n4_fresh_Prawitz_quadrature_cache_2026_10_09 as quadrature

integer, arithmetic, SCALE = previous.integer, previous.arithmetic, previous.SCALE
center, radial, geometry = previous.center, previous.radial, previous.geometry
require, TARGET = previous.require, previous.TARGET
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
PREVIOUS_PIN = "e29ec0c0140f48a79495881cc4cc8ffc6ad519817034d5c6ddd78c4662eaaf71"


def fresh_cached_center_table(rectangle, cache, use_contact_taylor, guard):
    """All root-dependent quantities fresh; only quadrature is shared."""
    quadrature.validate_preverified_fresh_cache(cache)
    N, H_grid = cache.N, cache.H_grid
    box, nominal, bridge = geometry.canonical_geometry(rectangle)
    da, db = F(bridge["da"], SCALE), F(bridge["db"], SCALE)
    blocks, frequencies, triangle_scale2 = {1: [], -1: []}, [], 0
    for j, q in enumerate(cache.q_grid):
        guard()
        kernel, k = cache.kernel_rectangles[j], cache.kernel_modulus_uppers[j]
        g0 = previous.generic_characteristic_correctly_scaled(q, nominal)
        a0 = min(SCALE, integer.rectangle_modulus_upper(g0))
        Eg = integer.ceil_fraction_scaled(min(geometry.reference_bridge.reference_error(q, bridge),
                                               q ** 3 * (da + db) / 6))
        actual = min(SCALE, a0 + Eg)
        D4 = arithmetic.quartic_absolute_upper(Eg, a0)
        triangle_scale2 += 2 * k * D4
        frequencies.append({"q": q, "kernel_rectangle": kernel, "kernel_modulus_upper_int": k,
            "g_nominal_rectangle": g0, "g_nominal_modulus_upper_int": a0,
            "g_actual_modulus_upper_int": actual, "Eg_upper_int": Eg, "D4_upper_int": D4})
        for orientation, characteristic in ((1, g0), (-1, integer.conjugate_rectangle(g0))):
            square = arithmetic.complex_multiply(characteristic, characteristic)
            fourth = arithmetic.complex_multiply(square, square)
            blocks[orientation].append(arithmetic.complex_multiply(kernel, fourth))
    triangle = integer.ceil_div(triangle_scale2, SCALE)
    rows = []
    for H in H_grid:
        guard()
        sums = quadrature.sum_center_blocks_with_phases(blocks, cache.phases_at(H), guard)
        normal = cache.normal_at(H)
        for orientation in (1, -1):
            raw_nominal = SCALE + 2 * sums[orientation][1] - 2 * normal[0]
            rows.append({"orientation": orientation, "H": H,
                "nominal_raw_Q_center_upper_int": raw_nominal,
                "raw_Q_center_upper_int": raw_nominal + triangle})
    table = {"scale": SCALE, "N": N, "box_geometry": box, "nominal_root_data": nominal,
        "rows": rows, "frequency_data": frequencies, "metadata": {"H_grid": H_grid}}
    taylor = {"used": False}
    if use_contact_taylor:
        taylor = tighten_with_fresh_cached_taylor(table, rectangle, cache, guard)
    tail = cache.positive_tail_Phi_interval
    require(5 * tail[0] > 4 * SCALE and len(rows) == 2 * len(H_grid)
            and {(r["orientation"], r["H"]) for r in rows}
                == {(orientation, H) for H in H_grid for orientation in (1, -1)},
            "ALL H, actual-law tails and genuine reflections")
    table["metadata"].update({"no_common_A1_or_response_cache": True,
        "nominal_reference_rho_cap_imposed": False, "exponential_tail_in_fixedpoint_units": True,
        "raw_Q_geometry_margin_upper_int": triangle, "contact_Taylor": taylor,
        "positive_tail_Phi_lower_int": tail[0],
        "fresh_target_certificate": previous.fresh_target_certificate(cache.pi_bracket, cache.phi0_bracket),
        "fresh_quadrature_cache": cache.compact_metadata()})
    return table


def tighten_with_fresh_cached_taylor(table, rectangle, cache, guard):
    """Same-root derivatives ONCE; unchanged signed/radial Taylor bounds."""
    inputs = center.canonical_inputs(table, rectangle, cache.N, cache.H_grid)
    box, nominal, bridge, _, _, ai, bi, a_bar, b_bar, da, db, ea, eb = inputs
    bundles = []
    for item in table["frequency_data"]:
        guard()
        bundles.append(quadrature.fresh_per_root_derivative_bundle(
            item["q"], a_bar, b_bar, item["kernel_rectangle"]))
    gradient_blocks = [bundle["signed_center_blocks"] for bundle in bundles]
    hessian = center.center_hessian_majorants(table["frequency_data"], ai, bi)
    indexed = {(row["orientation"], row["H"]): row for row in table["rows"]}
    center_improvements = 0
    for H in cache.H_grid:
        guard()
        gradients = quadrature.sum_signed_gradient_blocks_with_phases(
            gradient_blocks, cache.phases_at(H), guard)
        for orientation in (1, -1):
            row = indexed[orientation, H]
            ga, gb = center.expand_true_nominal_gradient(*gradients[orientation], ea, eb, hessian)
            upper = center.whole_box_taylor_upper_int(
                row["nominal_raw_Q_center_upper_int"], ga, gb, da, db, hessian)
            center_improvements += upper < row["raw_Q_center_upper_int"]
            row["raw_Q_center_upper_int"] = min(upper, row["raw_Q_center_upper_int"])
    modulus_improvements = 0
    for item, bundle in zip(table["frequency_data"], bundles):
        guard()
        q = item["q"]
        require(bundle["q"] == q and bundle["a_bar"] == a_bar and bundle["b_bar"] == b_bar,
                "Fresh derivative data belong to THIS SAME root")
        nominal_square = radial.nominal_squared_norm_upper(item["g_nominal_rectangle"])
        Hess = radial.modulus_squared_hessian_majorants(q, ai, bi)
        ga, gb = center.expand_true_nominal_gradient(*bundle["radial_gradient_intervals"], ea, eb, Hess)
        square_upper = radial.squared_modulus_taylor_upper(nominal_square, ga, gb, da, db, Hess)
        old = item["g_actual_modulus_upper_int"]
        actual, _ = radial.outward_modulus_from_squared_upper(square_upper, old)
        require(item["g_nominal_modulus_upper_int"] <= actual <= old,
                "Actual norm tightening retains the TRUE nominal baseline")
        modulus_improvements += actual < old
        item["g_actual_modulus_upper_int"] = actual
    return {"used": True, "center_rows_improved": center_improvements,
        "moduli_improved": modulus_improvements, "raw_center_Hessian_abs_bounds": hessian,
        "probability_path": "b>=a,ab>=1 convex; |g|<=1 on actual/true-nominal/rational-upper-root paths",
        "baseline": "Correctly scaled TRUE nominal CF and raw-Q center from THIS fresh producer",
        "legacy_high_level_CF_rebuild_or_check_called": False}


def compute_verified_cached_low_eta_box_leaf(rectangle, eta_interval, cache=None, N=256,
        H_step=F(1, 8), use_contact_taylor=True, initial_eta_cells=16, max_eta_cells=16,
        time_limit_seconds=TIME_LIMIT):
    """Full fixed eta partition. Supplied cache MUST be directly freshly built."""
    started = time.monotonic()
    rectangle, eta_interval = previous.checked_request(
        rectangle, eta_interval, N, H_step, initial_eta_cells, max_eta_cells)
    require(initial_eta_cells == max_eta_cells, "Fixed eta partition, no runtime-dependent selection")
    require(type(use_contact_taylor) is bool and type(time_limit_seconds) in (int, float, F)
            and 0 < time_limit_seconds <= TIME_LIMIT, "Explicit Taylor switch and bounded timer")
    require(hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == PREVIOUS_PIN,
            "Frozen corrected source drift check, not a mathematical proof")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Cached leaf elapsed budget")
        peak = previous.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Cached leaf256MiB working set")
    cache_built_here = cache is None
    if cache is None:
        cache = quadrature.build_fresh_quadrature_cache(N, H_step,
            time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    quadrature.validate_preverified_fresh_cache(cache, N, H_step)
    table = fresh_cached_center_table(rectangle, cache, use_contact_taylor, guard)
    box, rho_lower = table["box_geometry"], table["box_geometry"]["rhoQ_lo"]
    require(rho_lower >= 1, "Whole-box reference normalization>=1")
    frequencies = []
    for item in table["frequency_data"]:
        a = F(item["g_actual_modulus_upper_int"], SCALE)
        frequencies.append({"modulus": a, "weight_int": item["kernel_modulus_upper_int"],
            "models": previous.affine_radius_models(item["q"], a, box)})
    worst = max(table["rows"], key=lambda row: row["raw_Q_center_upper_int"])
    quad, H_reserve = F(687, 8 * N * N), F(19, 32) * H_step ** 2
    raw_constant = F(worst["raw_Q_center_upper_int"], SCALE) + quad + H_reserve
    L, U = eta_interval
    intervals = [(L, U)] if L == U else [(L + (U - L) * F(j, initial_eta_cells),
        L + (U - L) * F(j + 1, initial_eta_cells)) for j in range(initial_eta_cells)]
    cells = []
    for l, u in intervals:
        guard()
        cells.append(previous.frozen_complete_ABS_cell(frequencies, raw_constant, rho_lower, l, u))
    require(intervals[0][0] == L and intervals[-1][1] == U
            and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])),
            "Entire CLOSED eta interval and all joins")
    tail = F(2, 5)
    upper = max(tail, max(cell["score_upper"] for cell in cells))
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "Every H/reflection/eta cell AND tails strictly pass")
    guard()
    files = (Path(__file__), Path(previous.__file__), Path(quadrature.__file__),
        Path(previous.resources.__file__), Path(center.__file__), Path(radial.__file__),
        Path(center.derivatives.__file__), Path(geometry.__file__), Path(previous.geometry_factory.__file__),
        Path(geometry.reference_bridge.__file__), Path(arithmetic.__file__), Path(integer.__file__),
        Path(previous.algebra.__file__), arithmetic.SUPPORT_NOTE, arithmetic.PHYSICAL_BRIDGE,
        previous.CONSTRAINT_NOTE)
    return {"status": "EXACT_CONDITIONAL_FRESH_CACHED_LOW_ETA_BOX_CDF_LEAF" if passed else "UNKNOWN",
        "date": "2026-10-09", "scale": SCALE, "N": N, "H_step": H_step, "target": TARGET,
        "closed_rectangle": rectangle, "closed_eta_cover": eta_interval, "box_geometry": box,
        "nominal_root_data": table["nominal_root_data"], "cells": cells,
        "reference_centers_both_orientations": table["rows"], "frequency_data": table["frequency_data"],
        "reference_metadata": table["metadata"], "worst_Q_center": worst,
        "reserves_once": {"physical_quad": quad, "physical_H": H_reserve},
        "tail": {"score_upper": tail, "Phi_25_16_lower_int": cache.positive_tail_Phi_interval[0]},
        "summary": {"score_upper_exact": upper, "strict_margin_exact": TARGET - upper,
            "initial_eta_cells": 1 if L == U else initial_eta_cells, "final_eta_cells": len(cells),
            "failed_eta_cells": sum(not cell["passed"] for cell in cells), "adaptive_scheduling_stopped": False,
            "ALL_H_rows": len(table["rows"]), "ALL_H_nodes": len(cache.H_grid)},
        "physical_premises": "Standardized iid actual P, canonical geometry/eta in CLOSED box/interval, |X|<=17/4,actualrho=rhoQ+eta<46/25. CLOSED-CDF Prawitz and retained original-P bridge; no finite-atom/separate M4 premise.",
        "proof_scope": "Same corrected TRUE center/whole-box correction/modulus/complete quartic ABS transfer/ONE physical reserve of each type/all H/reflections/CLOSED eta/tails; directly fresh geometry-independent quadrature only.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_global_root_covered": False, "unrestricted_C4_proved": False,
            "saved_numeric_JSON_or_float_proof_inputs": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": previous.resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "cache_built_in_this_leaf": cache_built_here,
            "fresh_cache_resources": cache.resource_metadata(), "standard_library_only": True}}


def self_tests():
    checked = previous.checked_request((F(1, 2), F(3, 4), F(0), F(1, 3)),
        (F(0), F(1, 4)), 256, F(1, 8), 16, 16)
    require(len(checked) == 2 and previous.complete_H_grid(F(1, 8))
            == quadrature.complete_H_grid(F(1, 8)), "Identical full H/eta request scope")
    require(hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == PREVIOUS_PIN,
            "Frozen corrected leaf remains unchanged")
    return {"status": "CACHED_LEAF_TINY_REQUEST_SCOPE_TESTS_ONLY", "exact_checks": 3,
        "full_cache_leaf_or_global_producer_called": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
