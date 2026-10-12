"""Exact signed common-A1 CDF postconsumer from DIRECT-FRESH inputs only.

The coordinating job must DIRECTLY call the audited correct generic A1
builderV2 and the audited rational five-price Gamma compiler on that SAME
table and these SAME16 closed eta cells. This function accepts their fresh
in-memory mathematical outputs, never paths/JSON/receipts, and builds no
CF/A1/Gamma table itself. Fields, identities, pins or status flags cannot
prove the analytic input bounds. These freshness/validity premises are
explicit; there is no numeric certificate importer or producer CLI here.

Each row supplies a WHOLE-box M_H >= raw_Q(H)-T*rhoQ_actual, and Gamma_H
models A+eta*S from the SAME common positive nu and canonical budgets.
Prices have canonical order(lambda0,lambda+,lambda-,theta+,theta-): only
the first three are nonnegative. Cost A is recomputed exactly from fullbox
p0_hi,u_hi. S/Gamma stay signed. Any one model selected at the exact cell
midpoint is valid on the WHOLE eta cell; point optimality is not claimed.
Different H/cells may choose different valid models. Combine M_H and
Gamma_H for THAT row before max over H, preserving their correlation.

Modulus radii are INDEPENDENT proved cube/mass/unit affine models for
delta_q=P-Q_ACTUAL from the existing audited helper. Never abs(Gamma_H).
Freeze one nonnegative radius on the whole cell. For each q choose either
a complete frozen-primary R2 quadratic, a complete old-disk constant, or
the complete new two-disk constant at(a_actual,e_hi). Choosing by exact
midpoint only affects tightness, not validity; coefficients are NOT
minimized separately. Sum nonnegative kernel weights, then outward-CEIL
each coefficient to SCALE. Since eta>=0, this raises the entire polynomial;
the quadratic leading term remains nonnegative, even for signed slopes.

A1 already contains4*kappa*g^3*r. Raw transfer therefore is2*Gamma_H
+2*weighted_R2, NOT another4. Per-H target polynomial is
 M_H+ONE687/(8N^2)+ONEphysical_H+2*Gamma_H+2*weighted_R2-T*eta.
The current physical H reserve is fresh per ENTIRE eta cell and replaces
the old reserve. Original midpoint reserve stays ONCE; no local-quad
improvement is assumed here. The pure17b convex degree2/endpoints/Bernstein
criterion and BOTH denominator-face score are applied to EVERY declared
H/reflection row. Negative Gamma is neither clipped nor infeasibility.
Only after these complete row checks is a whole-cell maximum taken.

ALL16 closed cells, joins, COMPLETE H58/115/229 grid and BOTH genuine
reflections are retained. Every failed eta cell stores a whole-cell upper
and its worst row; all rows were checked, not just a selected H. Actual-law
tail2/5 plus fresh T4097/10000<CE are mandatory. Numerical eta points may
be unrealizable; bounds concern every ACTUAL law under the premises.

Conditional scope: standardized iid actual P in declared canonical box/
eta interval, |X|<=17/4, actualrho=rhoQ_actual+eta<46/25, retained CLOSED-CDF
Prawitz and original-P physical midpoint bridge. No original finite-atom,
density or separate M4 assumption. First-critical owner/literature inputs
remain external. This source proves no entire-root/unrestricted C4 claim.
Stdlib cooperative60s/256MiB. Dormant scalar tests only, no jobs on import,
no producer/replay/file-write CLI. Every older source stays untouched.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_Q3_fresh_generic_common_A1_response_table_v2_2026_10_09 as builder
import n4_Q3_fresh_generic_A1_five_price_cell_suprema_2026_10_09 as gamma_compiler
import n4_fresh_signed_common_nu_quartic_ledger_2026_10_09 as ledger
import n4_two_disk_fourth_power_remainder_2026_10_09 as lens
import n4_Q3_H_curvature_low_eta_box_leaf_2026_10_09 as H_leaf

cached, resources = H_leaf.cached, H_leaf.cached.previous.resources
SCALE, TARGET, require = H_leaf.SCALE, H_leaf.TARGET, H_leaf.require
TIME_LIMIT, MEMORY_LIMIT, ETA_CELLS = 60, 256 * 1024 * 1024, 16
PRICE_ORDER = ("lambda0", "lambda_plus", "lambda_minus", "theta_plus", "theta_minus")
BUILDER_PIN = "0a5cf384dd991e8c9f30bc653dc3b180fe0fa8b23d14808890e64b1d7b173a7f"
LEDGER_PIN = "17b4c2b7b90ef39a4d524f0ea388f035f2bcfe85e12127b802eade6632fab987"
LENS_PIN = "8a0fd09fadab0f90edef5cd4bdbcbdd89a1b24e3b48c2f97b07898b3c9d8d8cd"
H_LEAF_PIN = "3ee382c9b6de905da3d53034e65ae854ea13c9d877c60a59e98c8bc5de057c68"
GAMMA_PIN = "f5dc893e0674255cc68981bdb61a2b0ce5586b8a2afbea14f7634cd85c0a5ad4"


def source_drift_check():
    builder.source_drift_check()
    for module, pin in ((builder, BUILDER_PIN), (ledger, LEDGER_PIN),
                        (lens, LENS_PIN), (H_leaf, H_LEAF_PIN), (gamma_compiler, GAMMA_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen input arithmetic integrity only: " + Path(module.__file__).name)
    require(SCALE == ledger.SCALE == lens.SCALE and TARGET == ledger.DEFAULT_TARGET,
            "Same exact physical arithmetic units/target")


def dependency_pins():
    files = (Path(__file__), Path(builder.__file__), Path(builder.previous.__file__),
        Path(gamma_compiler.__file__), Path(gamma_compiler.point.__file__),
        Path(ledger.__file__), Path(lens.__file__), Path(H_leaf.__file__), Path(H_leaf.curvature.__file__),
        Path(builder.previous.linked_center.__file__), Path(builder.previous.linked_center.linked.__file__),
        Path(builder.previous.linked_center.contact_center.__file__),
        Path(builder.previous.linked_center.contact_center.supporting_plane.__file__),
        Path(cached.__file__), Path(cached.quadrature.__file__), Path(cached.previous.__file__),
        Path(cached.center.__file__), Path(cached.radial.__file__), Path(cached.center.derivatives.__file__),
        Path(cached.geometry.__file__), Path(cached.previous.geometry_factory.__file__),
        Path(cached.geometry.reference_bridge.__file__), Path(cached.arithmetic.__file__),
        Path(cached.integer.__file__), Path(cached.previous.algebra.__file__), Path(resources.__file__),
        cached.arithmetic.SUPPORT_NOTE, cached.arithmetic.PHYSICAL_BRIDGE, cached.previous.CONSTRAINT_NOTE)
    require(len({path.name for path in files}) == len(files), "Unambiguous complete math-source closure")
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def fixed_eta_cells(eta_interval):
    require(type(eta_interval) in (tuple, list) and len(eta_interval) == 2
            and all(type(value) is F for value in eta_interval)
            and 0 <= eta_interval[0] <= eta_interval[1], "Exact CLOSED physical eta interval")
    L, U = eta_interval
    return tuple((L + (U - L) * F(j, ETA_CELLS), L + (U - L) * F(j + 1, ETA_CELLS))
                 for j in range(ETA_CELLS))


def _ceil_scaled(value):
    value = ledger.exact(value) * SCALE
    return -((-value.numerator) // value.denominator)


def _check_fresh_inputs(table, gamma, rectangle, N, H_step, eta_cells):
    """Strict identities under DIRECT-FRESH mathematical input premises."""
    require(type(table) is dict and type(gamma) is dict and N == 256 and type(N) is int,
            "DIRECT fresh dicts/approved physical N256")
    grid = cached.previous.complete_H_grid(H_step)
    cached.center.canonical_inputs(table, rectangle, N, grid)
    require(type(table["scale"]) is type(gamma["scale"]) is int
            and type(table["N"]) is type(gamma["N"]) is int
            and table["scale"] == gamma["scale"] == SCALE and table["N"] == gamma["N"] == N,
            "Matching fresh A1/Gamma scale/N")
    box, nominal = table["box_geometry"], table["nominal_root_data"]
    require(all(type(H) is F for H in table["metadata"]["H_grid"])
            and all(type(H) is F for H in gamma["metadata"]["H_grid"])
            and tuple(table["metadata"]["H_grid"]) == tuple(gamma["metadata"]["H_grid"]) == grid
            and tuple(gamma["metadata"]["price_order"]) == PRICE_ORDER
            and all(len(pair) == 2 and all(type(value) is F for value in pair) for pair in gamma["eta_cells"])
            and tuple(tuple(pair) for pair in gamma["eta_cells"]) == eta_cells,
            "Same ALL H/closed eta cells and canonical price meanings")
    require(tuple(gamma["box_geometry"]["rectangle"]) == tuple(rectangle), "Same ACTUAL geometry box")
    for key in ("a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket", "w_interval", "beta_abs_interval"):
        expected_type = int if key.endswith("bracket") else F
        require(all(type(value) is expected_type for value in gamma["box_geometry"][key])
                and tuple(gamma["box_geometry"][key]) == tuple(box[key]), "Actual root interval identity: " + key)
    for key in ("p0_hi", "u_hi", "rhoQ_lo", "rhoQ_hi"):
        require(type(box[key]) is type(gamma["box_geometry"][key]) is F
                and gamma["box_geometry"][key] == box[key], "Fullbox budget/rho identity: " + key)
    for key in ("w", "beta", "a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket"):
        value = gamma["nominal_root_data"][key]
        require((all(type(endpoint) is int for endpoint in value) if key.endswith("bracket")
                 else type(value) is F) and value == nominal[key],
                "TRUE nominal labels separate from actual box: " + key)
    require(max(box["a_bracket"][1], box["b_bracket"][1]) <= F(17, 4) * SCALE,
            "Whole owner/contact response domain")
    frequencies = table["frequency_data"]
    q_grid = tuple(F(3 * (2 * j + 1), 2 * N) for j in range(N))
    require(len(frequencies) == N and all(type(q) is F for q in gamma["q_grid"])
            and tuple(gamma["q_grid"]) == q_grid
            and all(type(item["q"]) is F and item["q"] == q for item, q in zip(frequencies, q_grid)),
            "ALL physical q identity")
    for item in frequencies:
        require(type(item["kernel_modulus_upper_int"]) is int and item["kernel_modulus_upper_int"] >= 0
                and type(item["g_actual_modulus_upper_int"]) is int
                and 0 <= item["g_actual_modulus_upper_int"] <= SCALE,
                "Outward nonnegative kernel/ACTUAL modulus integers at declared scale")
    metadata = table["metadata"]
    require(metadata["A1_includes_nominal_HG_tail_y_mesh_once"] is True
            and metadata["A1_includes_box_geometry_margin"] is True,
            "A1 corrections ALREADY included; flags are not mathematical provenance")
    expected = {(orientation, H) for H in grid for orientation in (1, -1)}
    table_rows, gamma_rows = table["rows"], gamma["rows"]
    require(len(table_rows) == len(gamma_rows) == len(expected)
            and {(row["orientation"], row["H"]) for row in table_rows} == expected
            and {(row["orientation"], row["H"]) for row in gamma_rows} == expected,
            "Every H and BOTH orientations, without duplicate/prefix")
    for row in table_rows:
        require(type(row["orientation"]) is int and type(row["H"]) is F
                and type(row["raw_minus_target_rhoQ_upper_int"]) is int
                and all(len(row[key]) == 273 and all(type(value) is int for value in row[key])
                    for key in ("positive_cell_upper_int", "negative_cell_upper_int")),
                "Signed whole-box M_H and complete actual A1 response cells")
    for row in gamma_rows:
        require(type(row["orientation"]) is int and type(row["H"]) is F
                and row["models"], "Exact row labels/at least zero-price whole-fibre Gamma model")
        seen = set()
        for model in row["models"]:
            prices = tuple(model["prices"])
            require(len(prices) == 5 and all(type(value) is F for value in prices)
                    and min(prices[:3]) >= 0 and prices not in seen,
                    "Distinct FULL exact prices, inequality prices nonnegative/equality prices signed")
            seen.add(prices)
            require(type(model["A"]) is F and type(model["S_upper_int"]) is int,
                    "Exact signed complete Gamma affine model")
            A, _ = ledger.gamma_affine_from_proven_sup(box["p0_hi"], box["u_hi"], prices,
                                                      F(model["S_upper_int"], SCALE))
            require(model["A"] == A, "Recomputed exact fullbox budget cost; no tuple-order ambiguity")
        require((F(0),) * 5 in seen, "Zero-price model valid also at eta0")
    return box, grid


def _choose_gamma(models, lower, upper):
    midpoint = (lower + upper) / 2
    index, model = min(enumerate(models), key=lambda pair:
        (pair[1]["A"] + F(pair[1]["S_upper_int"], SCALE) * midpoint, tuple(pair[1]["prices"])))
    return index, (model["A"], F(model["S_upper_int"], SCALE))


def _fresh_weighted_R2(frequencies, lower, upper, use_two_disk, guard):
    """One WHOLE radius and ONE WHOLE remainder function per q/cell."""
    coefficients, choices = [F(0), F(0), F(0)], []
    midpoint = (lower + upper) / 2
    for item in frequencies:
        guard()
        allowed = [model for model in item["models"]
                   if min(model[0] + model[1] * lower, model[0] + model[1] * upper) >= 0]
        require(allowed, "Cube supplies a nonnegative whole-cell radius")
        A, B, name = min(allowed, key=lambda model: model[0] + model[1] * midpoint)
        a = item["modulus"]
        primary, _ = ledger.frozen_remainder(a, (A, B), lower, upper, "primary")
        disk, _ = ledger.frozen_remainder(a, (A, B), lower, upper, "disk")
        candidates = [(primary, "primary_quadratic"), (disk, "old_disk_constant")]
        if use_two_disk:
            e_hi = max(A + B * lower, A + B * upper)
            upper_R2 = lens.two_disk_remainder_upper(a, e_hi, SCALE)["remainder_upper"]
            candidates.append(((upper_R2, F(0), F(0)), "two_disk_constant"))
        selected, method = min(candidates, key=lambda candidate: ledger.evaluate(candidate[0], midpoint))
        weight = F(item["weight_int"], SCALE)
        require(weight >= 0, "Fresh nonnegative outward kernel modulus")
        for degree in range(3):
            coefficients[degree] += weight * selected[degree]
        choices.append((name, method))
    # Upward coefficient rounding raises the WHOLE polynomial on eta>=0,
    # including a negative middle coefficient; no absolute clipping.
    rounded = tuple(F(_ceil_scaled(value), SCALE) for value in coefficients)
    require(rounded[2] >= 0, "Outward complete weighted R2 retains convex leading term")
    return rounded, tuple(choices)


def evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval, rectangle=None,
        N=256, H_step=F(1, 8), use_two_disk=True, time_limit_seconds=TIME_LIMIT):
    """Postconsumer ONLY, both tables must be DIRECT fresh mathematical outputs."""
    started = time.monotonic()
    rectangle = tuple(table["box_geometry"]["rectangle"] if rectangle is None else rectangle)
    cached.previous.checked_request(rectangle, eta_interval, N, H_step, ETA_CELLS, ETA_CELLS)
    require(type(use_two_disk) is bool and type(time_limit_seconds) in (int, float, F)
            and 0 < time_limit_seconds <= TIME_LIMIT, "Explicit complete-R2 switch/cooperative60s timer")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Signed postconsumer elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Signed postconsumer256MiB")

    eta_cells = fixed_eta_cells(eta_interval)
    box, grid = _check_fresh_inputs(table, gamma_table, rectangle, N, H_step, eta_cells)
    norm_frequencies = H_leaf.transfer_frequencies(table["frequency_data"], box)
    indexed_gamma = {(row["orientation"], row["H"]): row for row in gamma_table["rows"]}
    indexed_center = {(row["orientation"], row["H"]): row for row in table["rows"]}
    quad, cells = F(687, 8 * N * N), []
    for L, U in eta_cells:
        guard()
        curve = H_leaf.compact_cell_curvature(table["frequency_data"], box, L, U, H_step, N)
        H_reserve = F(curve["physical_H_reserve_upper_int"], SCALE)
        R2, choices = _fresh_weighted_R2(norm_frequencies, L, U, use_two_disk, guard)
        row_results = []
        for H in grid:
            for orientation in (1, -1):
                guard()
                key = orientation, H
                gamma_index, gamma_model = _choose_gamma(indexed_gamma[key]["models"], L, U)
                M_H = F(indexed_center[key]["raw_minus_target_rhoQ_upper_int"], SCALE)
                result = ledger.per_H_signed_normalized_row(M_H, gamma_model, R2,
                    quad, H_reserve, box["rhoQ_lo"], L, U, TARGET, ledger.DEFAULT_CAP)
                result.update({"orientation": orientation, "H": H,
                    "normalized_reference_center_upper_exact": M_H,
                    "frozen_gamma_model_index": gamma_index})
                row_results.append(result)
        require(len(row_results) == 2 * len(grid), "Every WHOLE eta-cell row checked")
        worst = max(row_results, key=lambda row: row["normalized_score_upper"])
        passed = all(row["whole_cell_strict_numeric_inequality"] for row in row_results)
        require(passed == (worst["normalized_score_upper"] < TARGET), "Max AFTER complete correlated row checks")
        cells.append({"lower": L, "upper": U, "passed": passed,
            "score_upper": worst["normalized_score_upper"], "worst_complete_H_row": worst,
            "H_reflection_rows_checked": len(row_results), "weighted_R2_upper_polynomial": R2,
            "physical_H_curvature": curve,
            "complete_R2_choices_digest_integrity_only": hashlib.sha256(repr(choices).encode("ascii")).hexdigest(),
            "remainder_methods_used": tuple(sorted({method for _, method in choices}))})
    certificate = table["metadata"]["fresh_target_certificate"]
    tail_lower = table["metadata"]["positive_tail_Phi_lower_int"]
    require(certificate["target"] == TARGET and type(certificate["CE_lower_exact"]) is F
            and certificate["CE_lower_exact"] > TARGET and type(tail_lower) is int
            and 5 * tail_lower > 4 * SCALE, "Fresh T<CE and actual-law tails")
    tail, upper = F(2, 5), max([F(2, 5)] + [cell["score_upper"] for cell in cells])
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "Entire CLOSED eta/all H/reflections/tails")
    guard()
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "All fresh mathematical dependencies unchanged through evaluation")
    guard()
    return {"status": "EXACT_CONDITIONAL_FRESH_SIGNED_A1_WHOLE_BOX_ETA" if passed else "UNKNOWN",
        "scale": SCALE, "target": TARGET, "N": N, "H_step": H_step,
        "closed_rectangle": rectangle, "closed_eta_cover": tuple(eta_interval),
        "cells": cells, "unresolved_eta_cell_indices": tuple(i for i, cell in enumerate(cells) if not cell["passed"]),
        "summary": {"score_upper_exact": upper, "failed_eta_cells": sum(not cell["passed"] for cell in cells),
            "ALL_H_nodes": len(grid), "ALL_H_reflection_rows_per_cell": 2 * len(grid), "fixed_closed_eta_cells": ETA_CELLS},
        "reserves_once": {"physical_quad": quad, "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "actual_law_tail_score_upper": tail, "fresh_target_certificate": certificate,
        "physical_premises": "Standardized iid actual P in declared canonical BOX/eta, |X|<=17/4,actualrho=rhoQ_actual+eta<46/25; retained CLOSED-CDF Prawitz and original-P midpoint bridge. No original atom-count/density/separate M4 premise.",
        "freshness_premises": "SAME table DIRECT corrected A1V2 producer and DIRECT exact Gamma compiler; label/schema/pin/status checks are not mathematical provenance. All radius models separately proved on WHOLE box/eta cell.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_root_or_unrestricted_C4_proved": False, "Gamma_used_as_modulus_radius": False,
            "raw_center_reconstructed_or_M_and_Gamma_separately_maximized": False,
            "saved_numeric_JSON_or_float_proof_inputs": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "A1_Gamma_or_CF_producer_called": False}}


def self_tests():
    """Dormant PURE scalar tests only; no A1/Gamma/CF/CDF evaluator called."""
    source_drift_check()
    checks = 0
    intervals = fixed_eta_cells((F(1, 10), F(3, 10)))
    require(len(intervals) == 16 and intervals[0][0] == F(1, 10)
            and intervals[-1][1] == F(3, 10)
            and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])), "Every CLOSED cell/join retained")
    checks += 1
    frequencies = [{"modulus": F(3, 5), "weight_int": SCALE // 7,
        "models": ((F(0), F(1), "cube"), (F(1, 3), F(0), "mass"), (F(8, 5), F(0), "unit"))}]
    for two_disk in (False, True):
        R2, _ = _fresh_weighted_R2(frequencies, F(0), F(1, 4), two_disk, lambda: None)
        for j in range(9):
            eta = F(j, 32)
            require(ledger.evaluate(R2, eta) >= 0 and R2[2] >= 0, "Whole nonnegative outward R2/convex leading term")
            checks += 1
    models = [{"A": F(0), "S_upper_int": SCALE // 10, "prices": (F(0),) * 5},
              {"A": F(1, 50), "S_upper_int": -SCALE // 25,
               "prices": (F(1, 10), F(0), F(0), F(-1, 10), F(0))}]
    _, selected = _choose_gamma(models, F(1, 2), F(1))
    require(selected[1] < 0 and selected[0] + selected[1] < 0,
            "Frozen WHOLE-cell signed Gamma retained; not clipped or a radius")
    checks += 1
    return {"exact_checks": checks, "cache_CF_A1_Gamma_CDF_or_global_producer_called": False,
            "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
