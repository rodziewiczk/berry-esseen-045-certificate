"""Fresh normalized-reference BOX x closed-eta CDF leaf, NOT full C4.

DIRECT fresh normalized centre builder supplies correctly-scaled TRUE
nominal CFs, actual-reference modulus bounds, and for every H/reflection
a WHOLE-box bound M_H >= C_H(Q_actual)-T*rhoQ_actual. Its supporting plane
retains signed centre/moment correlation. It does NOT replace the true
nominal baseline by a rational-bar CF. No numerical JSON/status/hash is a
mathematical input; a coordinating producer supplies any shared cache by
the DIRECT fresh audited quadrature builder, not by receipt deserialization.

On each of the FIXED16 entire CLOSED eta cells, the audited pure complete
ABS fourth-power arithmetic supplies C+D*eta >= sum|kappa|E_q(eta).
It is called with dummy raw constant zero ONLY to derive that complete
transfer. Its dummy acceptance, scores and target polynomial are ignored.
The separately fresh actual-P continuous-frequency H-curvature bound
replaces the old H reserve; ONE physical 687/(8*N^2) remains unchanged.
If M=max over ALL H nodes and BOTH genuine reflections of M_H, then
    P(eta) = M+quad+H_reserve+2*C+(2*D-T)*eta
is a uniform upper of the physical central raw discrepancy minus
T*rhoP, since rhoP=rhoQ_actual+eta. Degree1 Bernstein coefficients, or
equivalently both endpoint values, strictly negative prove the WHOLE
closed cell, including shared faces. There is no reconstructed independent
raw centre, coefficientwise minimum, partial-H route mix or point winner
persistence premise.

For a quantitative score, division by a LOWER rho is WRONG when P<0.
The standing physical premise gives rhoP in [rhoQ_LO+eta,rho_cap), with
rho_cap=46/25. Thus P/rhoP <= max(P/(rhoQ_LO+eta),P/rho_cap), regardless
of its sign. Each affine or linear-fractional branch has an endpoint
maximum on the whole cell. The score is therefore
    max(0, T+max(P(L)/cap,P(U)/cap,
                 P(L)/(rhoQ_LO+L),P(U)/(rhoQ_LO+U))).
Strict Bernstein negativity is the acceptance criterion; the score
agrees with that criterion but never silently uses only the lower face.
Outer eta points need not be realizable. The bound concerns every ACTUAL
law satisfying the physical premises, not fabricated laws at those points.

The private postconsumer rederives all16 cells, complete transfers,
curvature/reserves, normalized polynomials, both denominator faces,
ALL H/reflections, tails and target comparison AFTER the DIRECT fresh
mathematical producer. It is not a JSON certificate importer. All UNKNOWN
cells retain their closed scopes and normalized names. The actual-law
tail score2/5 and fresh T<CE remain mandatory.

Standing conditional scope: standardized iid P, its canonical coordinates
in the declared closed box/eta interval, |X|<=17/4, rhoP<46/25, one-sided
CLOSED-CDF Prawitz and retained original-P physical midpoint bridge.
No finite-support/density/separate M4 assumption on P is added. Retained
first-critical owner placement/literature inputs remain external. This
module proves no unrestricted C4. Stdlib, externally coordinated single
sequential60s/256MiB job. No producer/replay/file-write CLI. Default CLI
runs ONLY dormant tiny exact scalar tests when separately authorized.
Older sources and receipts are never edited or used as numerical truth.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_fresh_normalized_contact_center_2026_10_09 as normalized_center
import n4_Q3_H_curvature_low_eta_box_leaf_2026_10_09 as H_leaf
import n4_Q3_normalized_contact_center_supporting_plane_2026_10_09 as supporting

cached = H_leaf.cached
quadrature, resources = cached.quadrature, cached.previous.resources
SCALE, TARGET, require = cached.SCALE, cached.TARGET, cached.require
N, H_STEP, ETA_CELLS = 256, F(1, 8), 16
RHO_CAP = F(46, 25)
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
CACHED_PIN = "4bf4a90a3eae9ed88b8a9e02d27e02ef53d4bef7b836fe426bf3dcfa49c3bd9f"
H_LEAF_PIN = "3ee382c9b6de905da3d53034e65ae854ea13c9d877c60a59e98c8bc5de057c68"
SUPPORTING_PIN = "23d4ae257daabba3131e2644bfcd22bad752901d6ccbb66ae4ec0d1b11fbfb1b"
NORMALIZED_CENTER_PIN = "e5ef0b28bf0c91966ac878fdc0ad4130f4571b9a9149736e734004f6bcee7b30"


def source_drift_check():
    """Integrity checks only; no hash establishes a mathematical bound."""
    for module, pin in ((cached, CACHED_PIN), (H_leaf, H_LEAF_PIN),
                        (supporting, SUPPORTING_PIN),
                        (normalized_center, NORMALIZED_CENTER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen source integrity only: " + Path(module.__file__).name)
    require(TARGET == supporting.DEFAULT_TARGET and SCALE == supporting.SCALE,
            "Exact supporting-plane target/scale agreement")


def dependency_pins():
    """Actual source closure for drift diagnostics, never a numeric proof."""
    files = (Path(__file__), Path(normalized_center.__file__), Path(H_leaf.__file__),
        Path(H_leaf.curvature.__file__), Path(supporting.__file__), Path(cached.__file__),
        Path(quadrature.__file__), Path(cached.previous.__file__), Path(resources.__file__),
        Path(cached.center.__file__), Path(cached.radial.__file__),
        Path(cached.center.derivatives.__file__), Path(cached.geometry.__file__),
        Path(cached.previous.geometry_factory.__file__),
        Path(cached.geometry.reference_bridge.__file__), Path(cached.arithmetic.__file__),
        Path(cached.integer.__file__), Path(cached.previous.algebra.__file__),
        cached.arithmetic.SUPPORT_NOTE, cached.arithmetic.PHYSICAL_BRIDGE,
        cached.previous.CONSTRAINT_NOTE)
    require(len({path.name for path in files}) == len(files), "Unique source-pin labels")
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def checked_fresh_center_scope(table, rectangle, cache):
    """Scope checks AFTER the DIRECT normalized mathematical producer."""
    require(type(table) is dict and table["scale"] == SCALE and table["N"] == cache.N,
            "Exact directly fresh centre scale/N")
    cached.center.canonical_inputs(table, rectangle, cache.N, cache.H_grid)
    require(tuple(table["metadata"]["H_grid"]) == cache.H_grid,
            "Entire shared complete H grid")
    rows, frequencies = table["rows"], table["frequency_data"]
    require(len(rows) == 2 * len(cache.H_grid)
            and {(r["orientation"], r["H"]) for r in rows}
                == {(orientation, H) for H in cache.H_grid for orientation in (1, -1)}
            and all(type(r["raw_minus_target_rhoQ_upper_int"]) is int for r in rows),
            "ALL central H/reflections and exact WHOLE-box normalized bounds")
    require(len(frequencies) == cache.N, "Complete fresh physical frequencies")
    for j, item in enumerate(frequencies):
        require(item["q"] == cache.q_grid[j]
                and tuple(item["kernel_rectangle"]) == cache.kernel_rectangles[j]
                and item["kernel_modulus_upper_int"] == cache.kernel_modulus_uppers[j]
                and type(item["g_actual_modulus_upper_int"]) is int
                and 0 <= item["g_actual_modulus_upper_int"] <= SCALE,
                "Same fresh q/kernel and ACTUAL reference modulus, not nominal substitution")
    require(type(table["box_geometry"]["rhoQ_lo"]) is F
            and table["box_geometry"]["rhoQ_lo"] >= 1,
            "Exact whole-box lower normalization")


def normalized_score_upper(polynomial, rho_lower, L, U,
                           target=TARGET, rho_cap=RHO_CAP):
    """WHOLE-cell upper using BOTH denominator faces, valid for either sign."""
    require(all(type(value) is F for value in (rho_lower, L, U, target, rho_cap))
            and rho_lower >= 1 and 0 <= L <= U and target > 0 and rho_cap > 0,
            "Exact normalized closed interval/physical denominator bounds")
    polynomial = cached.previous.algebra.polynomial(polynomial)
    require(len(polynomial) <= 2, "Affine normalized target polynomial")
    pL, pU = (cached.previous.algebra.evaluate(polynomial, point) for point in (L, U))
    faces = (pL / rho_cap, pU / rho_cap,
             pL / (rho_lower + L), pU / (rho_lower + U))
    return max(F(0), target + max(faces)), (pL, pU), faces


def normalized_cell_from_transfer(C, D, normalized_center_upper, quad,
                                  curve, rho_lower, L, U):
    """Pure exact degree1 criterion; no independent raw centre reconstructed."""
    require(all(type(value) is F for value in
                (C, D, normalized_center_upper, quad, rho_lower, L, U))
            and min(C + D * L, C + D * U) >= 0,
            "Proven nonnegative COMPLETE affine transfer on WHOLE cell")
    H_int = curve["physical_H_reserve_upper_int"]
    require(type(H_int) is int and H_int >= 0 and quad >= 0,
            "ONE outward physical reserve of each kind")
    constant = normalized_center_upper + quad + F(H_int, SCALE)
    polynomial = cached.previous.algebra.polynomial((constant + 2 * C, 2 * D - TARGET))
    passed, coefficients = cached.previous.algebra.bernstein_strict_negative(polynomial, L, U, degree=1)
    score, endpoints, faces = normalized_score_upper(polynomial, rho_lower, L, U)
    require(passed == all(value < 0 for value in endpoints)
            and passed == (score < TARGET),
            "Strict WHOLE-cell degree1 Bernstein/endpoints/BOTH-denominator score agree")
    return {"lower": L, "upper": U, "passed": passed, "score_upper": score,
        "transfer_affine_upper": (C, D),
        "normalized_reference_center_max_upper_exact": normalized_center_upper,
        "normalized_constant_with_one_quad_and_one_H": constant,
        "normalized_target_polynomial": polynomial,
        "normalized_target_endpoint_uppers": endpoints,
        "normalized_target_Bernstein_coefficients": coefficients,
        "normalized_score_denominator_face_ratios": faces,
        "physical_H_curvature": curve}


def fresh_normalized_ABS_cell(frequencies, normalized_center_upper, quad,
                              curve, rho_lower, L, U):
    """Fresh complete transfer only; IGNORE all dummy acceptance/score fields."""
    dummy = cached.previous.frozen_complete_ABS_cell(frequencies, F(0), rho_lower, L, U)
    C, D = dummy["transfer_affine_upper"]
    cell = normalized_cell_from_transfer(C, D, normalized_center_upper,
                                         quad, curve, rho_lower, L, U)
    cell["selected_model_counts"] = dummy["selected_model_counts"]
    cell["choices_digest_integrity_only"] = dummy["choices_digest_integrity_only"]
    return cell


def compute_verified_low_eta_box_leaf(rectangle, eta_interval, cache=None,
        N=256, H_step=F(1, 8), initial_eta_cells=16, max_eta_cells=16,
        time_limit_seconds=TIME_LIMIT):
    """DIRECT fresh builder/cache, FIXED16 complete closed eta cells."""
    started = time.monotonic()
    rectangle, eta_interval = cached.previous.checked_request(
        rectangle, eta_interval, N, H_step, initial_eta_cells, max_eta_cells)
    require(initial_eta_cells == max_eta_cells == ETA_CELLS, "FIXED16 entire eta cover")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Cooperative whole-leaf60s budget")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Normalized leaf elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Normalized leaf256MiB working set")

    built_here = cache is None
    if cache is None:
        cache = quadrature.build_fresh_quadrature_cache(N, H_step,
            time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    quadrature.validate_preverified_fresh_cache(cache, N, H_step)
    table = normalized_center.fresh_normalized_center_table(rectangle, cache, guard)
    checked_fresh_center_scope(table, rectangle, cache)
    box, rho = table["box_geometry"], table["box_geometry"]["rhoQ_lo"]
    frequencies = H_leaf.transfer_frequencies(table["frequency_data"], box)
    worst = max(table["rows"], key=lambda row: row["raw_minus_target_rhoQ_upper_int"])
    M = F(worst["raw_minus_target_rhoQ_upper_int"], SCALE)
    quad = F(687, 8 * N * N)
    L, U = eta_interval
    intervals = [(L + (U - L) * F(j, ETA_CELLS),
                  L + (U - L) * F(j + 1, ETA_CELLS)) for j in range(ETA_CELLS)]
    cells = []
    for l, u in intervals:
        guard()
        curve = H_leaf.compact_cell_curvature(table["frequency_data"], box, l, u, H_step, N)
        cells.append(fresh_normalized_ABS_cell(frequencies, M, quad, curve, rho, l, u))
    require(intervals[0][0] == L and intervals[-1][1] == U
            and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])),
            "Entire CLOSED eta interval and EVERY join")
    target_cert = cached.previous.fresh_target_certificate(cache.pi_bracket, cache.phi0_bracket)
    tail = F(2, 5)
    require(5 * cache.positive_tail_Phi_interval[0] > 4 * SCALE,
            "Fresh actual-law Gaussian tail witness")
    upper = max([tail] + [cell["score_upper"] for cell in cells])
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "All eta/H/reflections/tails strictly pass")
    source_drift_check()
    pins = dependency_pins()
    require(pins == initial_pins, "Fresh mathematical sources unchanged through leaf")
    guard()
    metadata = dict(table["metadata"])
    metadata.update({"fresh_target_certificate": target_cert,
        "normalized_reference_center_max_upper_exact": M,
        "normalized_center_target": TARGET,
        "fresh_quadrature_cache": cache.compact_metadata(),
        "raw_center_reconstructed_from_normalized_bound": False})
    return {"status": "EXACT_CONDITIONAL_NORMALIZED_H_CURVATURE_LOW_ETA_BOX" if passed else "UNKNOWN",
        "date": "2026-10-09", "scale": SCALE, "N": N, "H_step": H_step, "target": TARGET,
        "closed_rectangle": rectangle, "closed_eta_cover": eta_interval,
        "box_geometry": box, "nominal_root_data": table["nominal_root_data"],
        "cells": cells, "reference_centers_both_orientations": table["rows"],
        "frequency_data": table["frequency_data"], "reference_metadata": metadata,
        "worst_normalized_Q_center": worst,
        "reserves_once": {"physical_quad": quad, "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "tail": {"score_upper": tail, "Phi_25_16_lower_int": cache.positive_tail_Phi_interval[0]},
        "summary": {"score_upper_exact": upper, "strict_margin_exact": TARGET - upper,
            "initial_eta_cells": ETA_CELLS, "final_eta_cells": len(cells),
            "failed_eta_cells": sum(not cell["passed"] for cell in cells),
            "adaptive_scheduling_stopped": False,
            "ALL_H_rows": len(table["rows"]), "ALL_H_nodes": len(cache.H_grid)},
        "physical_premises": "Standardized iid actual P; canonical geometry/eta in declared CLOSED box/interval; |X|<=17/4,actualrho=rhoQ_actual+eta<46/25. CLOSED-CDF Prawitz/retained original-P midpoint bridge; no finite-atom/density/separate M4 premise.",
        "proof_scope": "DIRECT corrected TRUE centres and normalized supporting-plane whole-box bounds; actual-Q moduli; COMPLETE ABS transfer; ONE quad/ONE continuous-frequency H replacement per closed eta cell; BOTH orientations/ALL H/eta joins/actual-law tails. Strict degree1 normalized target criterion; quantitative score checks both denominator faces.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_global_root_covered": False, "unrestricted_C4_proved": False,
            "saved_numeric_JSON_or_float_proof_inputs": False,
            "old_sources_or_receipts_modified": False,
            "dummy_ABS_acceptance_or_old_raw_score_used": False,
            "raw_center_reconstructed_from_normalized_bound": False},
        "source_pins_integrity_only": pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "cache_built_in_this_leaf": built_here,
            "fresh_cache_resources": cache.resource_metadata(), "standard_library_only": True}}


def _checked_fresh_leaf_math(fresh, request):
    """Exact complete postconsumer AFTER DIRECT fresh normalized leaf only."""
    rectangle, cut, rho = request["closed_rectangle"], request["etaSV_exact"], request["rhoQ_lower_exact"]
    require(cut > 0 and fresh["scale"] == SCALE and fresh["N"] == N
            and fresh["target"] == TARGET and fresh["H_step"] == H_STEP
            and fresh["closed_rectangle"] == rectangle
            and fresh["closed_eta_cover"] == (F(0), cut), "SAME entire normalized request")
    box = fresh["box_geometry"]
    require(box["rhoQ_lo"] == rho and tuple(box["rectangle"]) == rectangle,
            "Exact actual geometry/lower moment for denominator faces")
    grid = cached.previous.complete_H_grid(H_STEP)
    rows = fresh["reference_centers_both_orientations"]
    require(len(rows) == 2 * len(grid) and {(r["orientation"], r["H"]) for r in rows}
            == {(orientation, H) for H in grid for orientation in (1, -1)}
            and all(type(r["raw_minus_target_rhoQ_upper_int"]) is int for r in rows),
            "Every H and BOTH normalized reflection bounds")
    quad = F(687, 8 * N * N)
    require(fresh["reserves_once"] == {"physical_quad": quad,
                "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"}, "ONE quad/ONE replaced H")
    tail = fresh["tail"]["score_upper"]
    require(tail == F(2, 5) and tail < TARGET
            and type(fresh["tail"]["Phi_25_16_lower_int"]) is int
            and 5 * fresh["tail"]["Phi_25_16_lower_int"] > 4 * SCALE,
            "Fresh actual-law tails, not an acceptance flag")
    certificate = fresh["reference_metadata"]["fresh_target_certificate"]
    require(certificate["target"] == TARGET and type(certificate["CE_lower_exact"]) is F
            and certificate["CE_lower_exact"] > TARGET, "Fresh target below CE")
    frequencies = H_leaf.transfer_frequencies(fresh["frequency_data"], box)
    M = F(max(r["raw_minus_target_rhoQ_upper_int"] for r in rows), SCALE)
    require(fresh["reference_metadata"]["normalized_reference_center_max_upper_exact"] == M
            and fresh["reference_metadata"]["normalized_center_target"] == TARGET,
            "Recomputed full normalized centre maximum/target")
    require(len(fresh["cells"]) == ETA_CELLS, "FIXED16 entire closed eta cover")
    checked, unresolved = [], []
    for j, cell in enumerate(fresh["cells"]):
        L, U = cut * F(j, ETA_CELLS), cut * F(j + 1, ETA_CELLS)
        require((cell["lower"], cell["upper"]) == (L, U), "No missing normalized eta scope/joins")
        curve = H_leaf.compact_cell_curvature(fresh["frequency_data"], box, L, U, H_STEP, N)
        exact_cell = fresh_normalized_ABS_cell(frequencies, M, quad, curve, rho, L, U)
        require(all(cell[key] == value for key, value in exact_cell.items()),
                "Recomputed complete transfer/curvature/normalized polynomial/Bernstein/score, no flags")
        record = {"eta_closed_interval": (L, U),
            "complete_transfer_affine_upper": exact_cell["transfer_affine_upper"],
            "normalized_target_polynomial": exact_cell["normalized_target_polynomial"],
            "normalized_target_endpoint_uppers": exact_cell["normalized_target_endpoint_uppers"],
            "normalized_target_Bernstein_coefficients": exact_cell["normalized_target_Bernstein_coefficients"],
            "normalized_score_denominator_face_ratios": exact_cell["normalized_score_denominator_face_ratios"],
            "score_upper_exact": exact_cell["score_upper"],
            "strict_numeric_bound_verified": exact_cell["passed"],
            "physical_H_curvature": curve}
        checked.append(record)
        if not exact_cell["passed"]:
            unresolved.append(record)
    upper = max([tail] + [record["score_upper_exact"] for record in checked])
    passed = not unresolved and upper < TARGET
    require(fresh["summary"]["score_upper_exact"] == upper, "Whole normalized child rederived")
    return {"kind": "FRESH_LOW_ETA_WHOLE_BOX_CDF_BOUND" if passed else "UNKNOWN_NUMERIC_LOW_ETA_WHOLE_BOX",
        "low_eta_closed_scope": (F(0), cut), "low_eta_cells": checked,
        "unresolved_low_eta_cells": unresolved, "low_eta_upper_exact": upper,
        "conditional_whole_low_eta_CDF_bound_verified": passed,
        "both_orientations_H_nodes_checked": len(grid), "reference_center_rows_checked": len(rows),
        "physical_reserves_once": {"physical_quad": quad,
            "physical_H": "PER_CLOSED_ETA_CELL_REPLACEMENT"},
        "actual_law_tail_upper_exact": tail,
        "worst_fresh_normalized_reference_center": fresh["worst_normalized_Q_center"],
        "normalized_reference_center_max_upper_exact": M,
        "normalized_center_metadata": fresh["reference_metadata"],
        "reported_child_status_not_a_proof_premise": True,
        "naive_lower_denominator_for_negative_numerator_used": False}


def self_tests():
    """Dormant scalar sign/denominator/ceiling tests; no cache/CF producer."""
    source_drift_check()
    checks = 0
    lower, upper, rho = F(0), F(1, 2), F(1)
    for polynomial in ((F(-1, 100),), (F(1, 100),),
                       (F(-1, 100), F(1, 25)), (F(1, 100), F(-1, 25)),
                       (F(-1, 100), F(-1, 25)), (F(0), F(0))):
        score, endpoints, _ = normalized_score_upper(polynomial, rho, lower, upper)
        passed, coefficients = cached.previous.algebra.bernstein_strict_negative(polynomial, lower, upper, degree=1)
        require(passed == all(value < 0 for value in endpoints)
                and passed == (score < TARGET) and coefficients == endpoints,
                "Whole affine strict criterion and quantitative score agree")
        checks += 1
        for j in range(5):
            eta = lower + (upper - lower) * F(j, 4)
            p = cached.previous.algebra.evaluate(polynomial, eta)
            for denominator in (rho + eta, (rho + eta + RHO_CAP) / 2, RHO_CAP):
                require(TARGET + p / denominator <= score,
                        "Both denominator faces cover negative/positive numerator throughout cell")
                checks += 1
    score, _, _ = normalized_score_upper((F(-1, 100),), F(1), F(0), F(0))
    require(score == TARGET - F(1, 100) / RHO_CAP
            and score > TARGET - F(1, 100), "Negative numerator requires upper denominator face")
    checks += 1
    for B in (F(0), F(1, 3), F(6)):
        for h in (F(1, 8), F(1, 16), F(1, 32)):
            B_int = H_leaf.curvature.ceil_scaled(B, SCALE)
            H_int = H_leaf.curvature.ceil_scaled(h ** 2 * (F(B_int, SCALE) + F(1, 4)) / 16, SCALE)
            require(F(H_int, SCALE) >= h ** 2 * (B + F(1, 4)) / 16
                    and F(H_int, SCALE) <= F(25, 64) * h ** 2 + F(2, SCALE),
                    "ONE H replacement, two outward ceilings and global curvature guard")
            checks += 1
    curve = {"physical_H_reserve_upper_int": 1}
    result = normalized_cell_from_transfer(F(1, 1000), F(1, 2000), F(-1, 100), F(0),
                                           curve, F(1), F(0), F(1, 2))
    require(result["normalized_target_polynomial"]
            == (F(-1, 100) + F(1, SCALE) + F(1, 500), F(1, 1000) - TARGET),
            "Transfer factor2 and −T eta appear once, no fictitious raw centre")
    checks += 1
    try:
        normalized_score_upper((F(-1, 100),), 1.0, F(0), F(1, 2))
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("Floating denominator proof input accepted")
    return {"status": "NORMALIZED_H_CURVATURE_LEAF_TINY_SCALAR_TESTS_ONLY",
        "exact_checks": checks, "cache_CF_center_leaf_or_global_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
