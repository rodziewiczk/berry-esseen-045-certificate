"""DIRECT fresh linked-(w,beta) normalized BOX x closed-eta CDF leaf.

The NEW linked centre builder is called DIRECTLY once for this box. It
starts with the fresh correctly-scaled TRUE CF/centre/modulus table, then
adds a linked w,beta Taylor upper of raw-Q centre minus T*rhoQ_actual.
Both TRUE signed gradients and the old contact Hessian come from that
same fresh table, not from JSON/status/hash or a rational-bar CF baseline.
The scalar minimum with the already valid contact-normalized centre is
a minimum of complete WHOLE-box bounds. Original raw/CF/modulus fields
remain unchanged. No older source is edited or globally monkeypatched.

After this DIRECT new mathematical producer, only PURE audited849 helpers
check scope and derive complete ABS transfer, continuous-frequency H
replacement and normalized eta arithmetic. The 849 producer is NEVER
called, since that would build the older contact-only table. Its dummy
ABS acceptance is never used. The true polynomial is
 M+ONEquad+ONEH+2C+(2D-T)*eta, with M=max all normalized H/reflection rows.
FIXED16 CLOSED eta cells, both genuine reflections, every central H node,
joins and actual-law tails remain. Both denominator faces are checked,
including the physical rho upper face for a negative numerator. No raw
centre is reconstructed from a normalized bound or separately minimized
moment. The postconsumer delegates only the849 PURE validator AFTER the
new DIRECT producer, under its explicit fresh mathematical precondition.

Standing scope remains standardized iid actual P, geometry and eta in the
declared closed intervals, |X|<=17/4, actualrho=rhoQ_actual+eta<46/25,
CLOSED-CDF Prawitz and retained original-P midpoint bridge. No atom-count,
density or separate M4 assumption. First-critical all-law placement and
literature inputs remain external. UNKNOWN preserves every failed closed
eta interval, not a counterexample. No unrestricted C4 claim.

Stdlib; externally coordinated single60s/256MiB job. Source-only until
explicit authorization. Default CLI delegates dormant pure108 scalar
tests (no cache/CF/centre producer); no producer/replay/file-write CLI.
Source snapshots are integrity checks, not mathematical numeric inputs.
All older source/receipt files remain untouched.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_fresh_linked_w_beta_normalized_center_2026_10_09 as linked_center
import n4_Q3_normalized_H_curvature_low_eta_box_leaf_2026_10_09 as previous
import n4_Q3_normalized_w_beta_center_taylor_2026_10_09 as linked_math

cached = previous.cached
quadrature, resources = previous.quadrature, previous.resources
SCALE, TARGET, require = previous.SCALE, previous.TARGET, previous.require
N, H_STEP, ETA_CELLS = previous.N, previous.H_STEP, previous.ETA_CELLS
RHO_CAP = previous.RHO_CAP
TIME_LIMIT, MEMORY_LIMIT = previous.TIME_LIMIT, previous.MEMORY_LIMIT
PREVIOUS_PIN = "8495404c28ed7f0f75b63f8f16914d5bf75f7dbf7553e767581b03202b09c091"
LINKED_MATH_PIN = "ae6e5c4480e53d5c5384a994ecae303dc93d11ea9a2de47d40244a3b29d9a7b9"
LINKED_CENTER_PIN = "3f50db40de37b5220ee1ce011f62f4f9e5d3429af61be5c871c604c8d952c523"


def source_drift_check():
    """Frozen dependency integrity, not analytic provenance from hashes."""
    previous.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (linked_math, LINKED_MATH_PIN),
                        (linked_center, LINKED_CENTER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen linked leaf dependency: " + Path(module.__file__).name)
    require(SCALE == linked_math.SCALE and TARGET == linked_math.DEFAULT_TARGET,
            "Same exact normalized target/units")


def dependency_pins():
    pins = previous.dependency_pins()
    for path in (Path(__file__), Path(linked_center.__file__), Path(linked_math.__file__)):
        require(path.name not in pins, "Unique linked-source labels")
        pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def compute_verified_low_eta_box_leaf(rectangle, eta_interval, cache=None,
        N=256, H_step=F(1, 8), initial_eta_cells=16, max_eta_cells=16,
        time_limit_seconds=TIME_LIMIT):
    """DIRECT new linked builder, SAME pure WHOLE-eta normalized arithmetic."""
    started = time.monotonic()
    rectangle, eta_interval = cached.previous.checked_request(
        rectangle, eta_interval, N, H_step, initial_eta_cells, max_eta_cells)
    require(initial_eta_cells == max_eta_cells == ETA_CELLS, "FIXED16 entire linked eta cover")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Cooperative linked leaf60s budget")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Linked normalized leaf elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Linked normalized leaf256MiB")

    built_here = cache is None
    if cache is None:
        cache = quadrature.build_fresh_quadrature_cache(N, H_step,
            time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    quadrature.validate_preverified_fresh_cache(cache, N, H_step)
    # NEVER previous.compute_verified_low_eta_box_leaf: it would rebuild e5 only.
    table = linked_center.fresh_normalized_center_table(rectangle, cache, guard)
    previous.checked_fresh_center_scope(table, rectangle, cache)
    box, rho = table["box_geometry"], table["box_geometry"]["rhoQ_lo"]
    frequencies = previous.H_leaf.transfer_frequencies(table["frequency_data"], box)
    worst = max(table["rows"], key=lambda row: row["raw_minus_target_rhoQ_upper_int"])
    M = F(worst["raw_minus_target_rhoQ_upper_int"], SCALE)
    quad = F(687, 8 * N * N)
    L, U = eta_interval
    intervals = [(L + (U - L) * F(j, ETA_CELLS),
                  L + (U - L) * F(j + 1, ETA_CELLS)) for j in range(ETA_CELLS)]
    cells = []
    for l, u in intervals:
        guard()
        curve = previous.H_leaf.compact_cell_curvature(table["frequency_data"], box, l, u, H_step, N)
        cells.append(previous.fresh_normalized_ABS_cell(frequencies, M, quad, curve, rho, l, u))
    require(intervals[0][0] == L and intervals[-1][1] == U
            and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])),
            "Entire linked CLOSED eta interval and every shared face")
    certificate = cached.previous.fresh_target_certificate(cache.pi_bracket, cache.phi0_bracket)
    tail = F(2, 5)
    require(5 * cache.positive_tail_Phi_interval[0] > 4 * SCALE,
            "Fresh actual-law tails")
    upper = max([tail] + [cell["score_upper"] for cell in cells])
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "All linked eta/H/reflections/tails strictly pass")
    source_drift_check()
    pins = dependency_pins()
    require(pins == initial_pins, "All fresh linked mathematical sources unchanged")
    guard()
    metadata = dict(table["metadata"])
    metadata.update({"fresh_target_certificate": certificate,
        "normalized_reference_center_max_upper_exact": M,
        "normalized_center_target": TARGET,
        "fresh_quadrature_cache": cache.compact_metadata(),
        "direct_linked_center_builder_used": True,
        "old849_contact_only_eta_producer_called": False,
        "raw_center_reconstructed_from_normalized_bound": False})
    return {"status": "EXACT_CONDITIONAL_LINKED_W_BETA_H_CURVATURE_LOW_ETA_BOX" if passed else "UNKNOWN",
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
        "physical_premises": "Standardized iid actual P, declared CLOSED geometry/eta, |X|<=17/4,actualrho=rhoQ_actual+eta<46/25; CLOSED-CDF Prawitz/retained original-P midpoint bridge; no atom-count/density/separate M4 premise.",
        "proof_scope": "DIRECT correctly-scaled TRUE CF centre with linked-wβ and contact normalized WHOLE-box scalar bounds; actual moduli; COMPLETE ABS transfer; ONE quad/ONE continuous-frequency H replacement; FIXED16 closed eta/BOTH orientations/ALL H/tails. Correct negative-numerator denominator faces. No old849 producer or fabricated raw centre.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_global_root_covered": False, "unrestricted_C4_proved": False,
            "saved_numeric_JSON_or_float_proof_inputs": False,
            "old_sources_or_receipts_modified": False,
            "old849_contact_only_eta_producer_called": False,
            "dummy_ABS_acceptance_or_old_raw_score_used": False,
            "raw_center_reconstructed_from_normalized_bound": False},
        "source_pins_integrity_only": pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "cache_built_in_this_leaf": built_here,
            "fresh_cache_resources": cache.resource_metadata(), "standard_library_only": True}}


def _checked_fresh_leaf_math(fresh, request, low_eta_cut=None):
    """PURE849 postconsumer AFTER DIRECT new linked producer, NEVER JSON.

    The source/record shape cannot prove a linked centre inequality. The
    coordinating controller must have just called this new mathematical
    producer. Under that premise, the849 pure consumer exactly rederives
    normalized C,D/curve/denominator/Bernstein/all16/H/reflections/tails.

    An explicit low_eta_cut changes ONLY a LOCAL compatibility copy of
    the legacy etaSV_exact slot: in the849 pure consumer that slot means
    the expected upper face of [0,cut]. It does NOT prove the override
    comes from SV, Cantelli, or any above-cut theorem. The original request
    and its SV cut are preserved and separately recorded. A coordinating
    joint-route controller must prove its COMPLETE high route independently.
    At cut0 that high closed route already includes eta0, so the controller
    skips the low child/checker; the legacy positive-cut validator is not
    silently repurposed to accept a different interval.
    """
    original_sv_cut = request["etaSV_exact"]
    require(type(original_sv_cut) is F and original_sv_cut >= 0,
            "Exact original SV cut remains separately labeled")
    selected_cut = original_sv_cut if low_eta_cut is None else low_eta_cut
    require(type(selected_cut) is F and selected_cut >= 0,
            "Explicit generic low-eta upper face is an exact nonnegative Fraction")
    require(selected_cut > 0,
            "Zero complete-high-route cut covers eta0; skip low child/checker")
    compatibility_request = dict(request)
    compatibility_request["etaSV_exact"] = selected_cut
    result = previous._checked_fresh_leaf_math(fresh, compatibility_request)
    result.update({"actual_requested_low_eta_cut_exact": selected_cut,
        "original_SV_eta_cut_exact": original_sv_cut,
        "low_eta_cut_is_explicit_override": low_eta_cut is not None,
        "legacy_etaSV_slot_used_only_as_generic_interval_face": True,
        "complete_above_override_cut_route_proved_here": False,
        "original_request_or_SV_cut_mutated": False})
    return result


def self_tests():
    """Dormant delegated exact scalar tests only; no fresh math producers."""
    source_drift_check()
    result = previous.self_tests()
    return {"status": "LINKED_W_BETA_ETA_LEAF_TINY_PURE_SCALAR_TESTS_ONLY",
        "exact_checks": result["exact_checks"],
        "direct_linked_cache_CF_center_leaf_or_global_producer_called": False,
        "old849_producer_or_globals_monkeypatched": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
