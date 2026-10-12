"""DIRECT fresh Cantelli/SV + linked-normalized Fourier ENTIRE-root join.

ALL260 CLOSED20x13 root requests are retained, including all shared w/beta
faces. Only exact rhoQ_min_square>=cap_square proves a whole class empty
under eta>=0 and STRICT actualrho<46/25. EVERY other class calls the
audited joint split DIRECTLY FRESH: sign-count Cantelli raw all-p/all-H
bounds, exact necessary-root p pruning, and ONE complete Cantelli or SV
high route. UNKNOWN backend status does not invalidate its proved raw
bounds. No saved frontier, price, previous score or easy-box mask is used.

For the selected joint cut c, a DIRECT fresh linked-normalized leaf covers
the ENTIRE CLOSED[0,c], FIXED16 eta cells, every central H/reflection and
actual-law tails. Its PURE postconsumer is called with explicit low_eta_cut
override; the original SV cut remains separately labeled. The compatibility
slot proves only the low interval arithmetic, not an above-cut SV claim.
The high route separately covers ALL actual eta>=c, including equality.
At c=0 it already covers eta0 and all eta>=0, so no low child is needed.
If a parent estimate fails, a FIXED depth1 refinement checks ALL FOUR
CLOSED midpoint geometry children with their OWN freshly derived rho/SV/
joint cut and entire-eta proofs. A parent closes only if all four close.
All child failures/shared faces and the original parent estimate remain
recorded; no recursive or runtime-truncated refinement is accepted.
Later geometry classes are still checked. No point classes, H prefixes, coefficientwise
route mix, reconstructed raw centre, or persistence of a point winner.

ONE DIRECT fresh immutable quadrature cache is shared; all geometry,
TRUE CF, signed gradients, actual moduli, linked moment normalization,
transfer and curvature remain fresh for each actual box. The original
physical midpoint reserve is added once; ONE per-cell continuous-frequency
H reserve replaces the old reserve. Negative normalized numerators use
BOTH valid denominator faces, not a falsely optimistic lower denominator.
The pilot's producer/three-class indices are NEVER called or modified.
Only its pure module aliases and integrity/source-closure helpers are used.

Conditional physical root: standardized iid actual P, canonical coordinates
in w[625/2116,1], |beta|[0,13/20], eta>=0, |X|<=17/4,
actualrho=rhoQ_actual+eta<46/25. CLOSED-CDF Prawitz/retained original-P
midpoint bridge and the published iid SV envelope are external analytic
inputs. No original-P atom-count/density/separate M4 assumption is added.
Fresh arithmetic proves T4097/10000<CE. If every nonempty full join closes,
the whole CONDITIONAL physical root has R4<=T<CE. Retained C3/attainment/
support-owner inputs remain necessary for all-law use; this program alone
NEVER proves unrestricted C4. An unfinished runtime yields no receipt.

SOURCE ONLY until explicitly authorized. Default tiny tests invoke only
pure260 root geometry/request and split arithmetic, no CDF/cache producer.
Explicit producer/replay: ONE sequential6000s/256MiB job, each heavy
producer<=60s; NEW exclusive<=24MiB full receipt or read-only EXACT ALL
nonresource comparison. Source snapshots are integrity, not mathematics.
Every older source/receipt is preserved; no globals are monkeypatched.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_fresh_Cantelli_linked_normalization_join_pilot_2026_10_09 as integration

split, leaf = integration.split, integration.leaf
root, resources, quadrature = split.root, leaf.resources, leaf.quadrature
require, SCALE, TARGET = split.require, split.SCALE, split.TARGET
ROOT, RHO_CAP = root.ROOT, root.RHO_CAP
N, H_STEP, ETA_CELLS = leaf.N, leaf.H_STEP, leaf.ETA_CELLS
TIME_LIMIT, CHILD_LIMIT, MAX_DEPTH = 6000, 60, 1
MEMORY_LIMIT, OUTPUT_LIMIT = 256 * 1024 * 1024, 24 * 1024 * 1024
INTEGRATION_PIN = "793302d170cfef3687d05e5da9af7ee148ab063725f5933db0299c6adf61f2b9"


def source_drift_check():
    """Pure integrity closure, not a cached numeric proof or pilot producer."""
    integration.source_drift_check()
    require(hashlib.sha256(Path(integration.__file__).read_bytes()).hexdigest() == INTEGRATION_PIN,
            "Frozen pilot helper source integrity only")
    require(SCALE == root.SCALE == leaf.SCALE and TARGET == root.TARGET == leaf.TARGET
            and RHO_CAP == leaf.RHO_CAP and N == 256 and H_STEP == F(1, 8) and ETA_CELLS == 16,
            "SAME exact whole physical root/target/N/H/closed-eta grids")


def dependency_pins():
    pins = integration.dependency_pins()
    path = Path(__file__)
    require(path.name not in pins, "Unique full-root source label")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def emit(event, started, limit, request, completed, **extra):
    """Runtime diagnostics only; an incomplete sequence is NOT a root proof."""
    now = time.monotonic()
    print(json.dumps({"runtime_diagnostic_not_prefix_proof": True, "event": event,
        "elapsed_seconds": now - started, "remaining_seconds": limit - (now - started),
        "completed_fresh_geometry_joins": completed,
        "grid_index": None if request is None else request["grid_index"],
        "peak_working_set_bytes": resources.peak_bytes(), **extra},
        sort_keys=True, allow_nan=False, default=root.json_ready), flush=True)


def fresh_rectangle_request(rectangle, grid_index=None, geometry_path=()):
    """Exact GENERIC subrectangle rho/SV request; no root-index lookup."""
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is F for value in rectangle), "Four exact generic endpoints")
    wl, wh, bl, bh = rectangle
    require(ROOT[0] <= wl <= wh <= ROOT[1] and ROOT[2] <= bl <= bh <= ROOT[3],
            "Whole closed subrectangle contained in root")
    rectangle = tuple(rectangle)
    square = root.root_algebra.rhoQ_min_square(rectangle)
    request = {"grid_index": grid_index, "geometry_path": tuple(geometry_path),
        "closed_rectangle": rectangle, "rhoQ_min_square_exact": square,
        "proved_root_empty": square >= RHO_CAP ** 2}
    if request["proved_root_empty"]:
        return request
    rho = max(F(1), F(leaf.cached.integer.sqrt_fraction_interval(square)[0], SCALE))
    cut = max(F(0), root.SV_RHO - rho)
    score = root.SV_C * (1 + root.SV_OFFSET / (rho + cut))
    require(score <= TARGET and cut < RHO_CAP - rho, "Fresh generic CLOSED SV/cap arithmetic")
    request.update({"rhoQ_lower_exact": rho, "etaSV_exact": cut,
        "SV_score_at_closed_cut_exact": score, "actual_eta_capacity_outer_open": RHO_CAP - rho})
    return request


def closed_four_children(rectangle):
    """FIXED exhaustive 2x2 CLOSED cover, all shared faces retained."""
    wl, wh, bl, bh = rectangle
    wm, bm = (wl + wh) / 2, (bl + bh) / 2
    children = ((wl, wm, bl, bm), (wl, wm, bm, bh),
                (wm, wh, bl, bm), (wm, wh, bm, bh))
    require(children[0][0] == wl and children[3][1] == wh
            and children[0][2] == bl and children[3][3] == bh
            and children[0][1] == children[2][0] == children[1][1] == children[3][0]
            and children[0][3] == children[1][2] == children[2][3] == children[3][2],
            "Whole outer and shared CLOSED midpoint faces")
    return children


def _remaining_child_budget(budget):
    value = budget() if callable(budget) else budget
    require(type(value) in (int, float, F) and value > 0, "Positive caller remaining diagnostic budget")
    return min(CHILD_LIMIT, value)


def compact_checked_low_result(checked):
    """AFTER DIRECT leaf+full pure consumer, retain all mathematical scopes.

    No acceptance is inferred from this compact shape. Drop only repeated
    centre/cache/source/Hessian diagnostics and duplicate failed-cell copies.
    Every16 closed interval, transfer, polynomial/endpoints, H curvature,
    exact score and failed-cell index remains. Fresh replay compares this
    fresh projection, not numeric input used to prove anything.
    """
    cells = []
    for cell in checked["low_eta_cells"]:
        cells.append({key: cell[key] for key in (
            "eta_closed_interval", "complete_transfer_affine_upper",
            "normalized_target_polynomial", "normalized_target_endpoint_uppers",
            "score_upper_exact", "strict_numeric_bound_verified", "physical_H_curvature")})
    worst = checked["worst_fresh_normalized_reference_center"]
    return {"kind": checked["kind"], "low_eta_closed_scope": checked["low_eta_closed_scope"],
        "low_eta_cells": cells,
        "unresolved_low_eta_cell_indices": tuple(i for i, cell in enumerate(cells)
            if not cell["strict_numeric_bound_verified"]),
        "low_eta_upper_exact": checked["low_eta_upper_exact"],
        "conditional_whole_low_eta_CDF_bound_verified": checked["conditional_whole_low_eta_CDF_bound_verified"],
        "both_orientations_H_nodes_checked": checked["both_orientations_H_nodes_checked"],
        "reference_center_rows_checked": checked["reference_center_rows_checked"],
        "physical_reserves_once": checked["physical_reserves_once"],
        "actual_law_tail_upper_exact": checked["actual_law_tail_upper_exact"],
        "normalized_reference_center_max_upper_exact": checked["normalized_reference_center_max_upper_exact"],
        "worst_normalized_row": {key: worst[key] for key in
            ("orientation", "H", "raw_minus_target_rhoQ_upper_int")},
        "actual_requested_low_eta_cut_exact": checked["actual_requested_low_eta_cut_exact"],
        "original_SV_eta_cut_exact": checked["original_SV_eta_cut_exact"],
        "low_eta_cut_is_explicit_override": checked["low_eta_cut_is_explicit_override"],
        "full_DIRECT_leaf_and_pure_consumer_before_compaction": True}


def _compute_fresh_rectangle_join(request, cache, guard, budget):
    guard()
    canonical = fresh_rectangle_request(request["closed_rectangle"], request.get("grid_index"),
                                        request.get("geometry_path", ()))
    for key, value in canonical.items():
        if key != "geometry_path":
            require(request.get(key) == value, "Fresh generic request arithmetic: " + key)
    if canonical["proved_root_empty"]:
        return (dict(request, kind="EXACT_ROOT_EMPTY_BY_STRICT_RHO_CAP",
            whole_geometry_all_actual_eta_closed=True, whole_geometry_score_upper_exact=F(0),
            conditional_whole_geometry_all_eta_CDF_bound_verified=True,
            fresh_complete_low_eta_result=None,
            reason="Exact generic rhoQ_min_square>=strict cap_square,eta>=0"), [])
    high = split.fresh_joint_cut_for_request(request, time_limit_seconds=_remaining_child_budget(budget))
    resource_records = [high["resources"]]
    high_math = {key: value for key, value in high.items() if key != "resources"}
    cut, high_upper = high["joint_eta_cut_exact"], high["joint_high_eta_score_at_closed_cut_exact"]
    require(type(cut) is F and cut >= 0 and type(high_upper) is F and high_upper <= TARGET,
            "Fresh complete CLOSED generic high route")
    guard()
    if cut == 0:
        checked, closed, upper, kind = None, True, high_upper, "ENTIRE_GEOMETRY_CLOSED_HIGH_ROUTE"
    else:
        fresh = leaf.compute_verified_low_eta_box_leaf(request["closed_rectangle"], (F(0), cut),
            cache=cache, N=N, H_step=H_STEP, initial_eta_cells=ETA_CELLS, max_eta_cells=ETA_CELLS,
            time_limit_seconds=_remaining_child_budget(budget))
        full_checked = leaf._checked_fresh_leaf_math(fresh, request, low_eta_cut=cut)
        resource_records.append(fresh["resources"])
        checked = compact_checked_low_result(full_checked)
        closed = full_checked["conditional_whole_low_eta_CDF_bound_verified"]
        upper = max(full_checked["low_eta_upper_exact"], high_upper)
        kind = "FRESH_COMPLETE_ETA_JOIN_CDF_BOUND" if closed else "UNKNOWN_LOW_ETA_INTERVALS_RETAINED"
        del fresh, full_checked
    require(not closed or upper <= TARGET, "BOTH complete generic routes give<=T<CE")
    guard()
    return (dict(request, kind=kind, original_SV_eta_cut_exact=request["etaSV_exact"],
        actual_joint_eta_cut_exact=cut, fresh_complete_high_eta_route=high_math,
        fresh_complete_low_eta_result=checked, whole_geometry_all_actual_eta_closed=closed,
        conditional_whole_geometry_all_eta_CDF_bound_verified=closed,
        whole_geometry_score_upper_exact=upper), resource_records)


def compute_fresh_parent_join(request, cache, guard, budget=60):
    """DIRECT parent then ALL4 CLOSED children iff UNKNOWN, depth EXACTLY1.

    Caller owns the overall clock/RAM guard; budget is scalar or callable
    remaining seconds and EACH producer is capped60. Numerical UNKNOWN
    never stops the four-child cover. Return (macro_record,resources).
    """
    require(callable(guard) and MAX_DEPTH == 1, "Caller guard and FIXED depth1")
    quadrature.validate_preverified_fresh_cache(cache, N, H_STEP)
    initial, resource_records = _compute_fresh_rectangle_join(request, cache, guard, budget)
    if initial["whole_geometry_all_actual_eta_closed"]:
        initial.update({"fixed_geometry_depth_used": 0,
            "fresh_high_producer_calls": 0 if request["proved_root_empty"] else 1,
            "fresh_low_producer_calls": int(initial["fresh_complete_low_eta_result"] is not None)})
        return initial, resource_records
    children = []
    parent_path = tuple(request.get("geometry_path", ()))
    for index, rectangle in enumerate(closed_four_children(request["closed_rectangle"])):
        guard()
        child_request = fresh_rectangle_request(rectangle, request.get("grid_index"), parent_path + (index,))
        child, new_resources = _compute_fresh_rectangle_join(child_request, cache, guard, budget)
        child["fixed_geometry_depth_used"] = 1
        children.append(child)
        resource_records.extend(new_resources)
    require(len(children) == 4 and tuple(child["closed_rectangle"] for child in children)
            == closed_four_children(request["closed_rectangle"]), "ALL FOUR closed children, even UNKNOWN")
    closed = all(child["whole_geometry_all_actual_eta_closed"] for child in children)
    macro = dict(initial)
    macro.update({"kind": "FRESH_COMPLETE_ETA_JOIN_CDF_BOUND" if closed else "UNKNOWN_LOW_ETA_INTERVALS_RETAINED",
        "initial_parent_whole_geometry_all_actual_eta_closed": False,
        "initial_parent_score_upper_exact": initial["whole_geometry_score_upper_exact"],
        "initial_parent_join_not_a_macro_acceptance_premise": True,
        "fixed_geometry_depth_used": 1, "fixed_depth1_closed_children": children,
        "whole_geometry_all_actual_eta_closed": closed,
        "conditional_whole_geometry_all_eta_CDF_bound_verified": closed,
        "whole_geometry_score_upper_exact": max(child["whole_geometry_score_upper_exact"] for child in children),
        "closure_route": "EXHAUSTIVE_FOUR_CLOSED_CHILDREN_ALL_ACTUAL_ETA",
        "fresh_high_producer_calls": 1 + sum(not child["proved_root_empty"] for child in children),
        "fresh_low_producer_calls": 1 + sum(child["fresh_complete_low_eta_result"] is not None for child in children)})
    require(not closed or macro["whole_geometry_score_upper_exact"] <= TARGET, "Whole parent from ALL4 complete children")
    guard()
    return macro, resource_records


def unresolved_low_cell_count(record):
    if "fixed_depth1_closed_children" in record:
        return sum(unresolved_low_cell_count(child) for child in record["fixed_depth1_closed_children"])
    if record["kind"] != "UNKNOWN_LOW_ETA_INTERVALS_RETAINED":
        return 0
    return len(record["fresh_complete_low_eta_result"]["unresolved_low_eta_cell_indices"])


def compute_verified_global_root(time_limit_seconds=TIME_LIMIT):
    """Every nonempty class DIRECT high proof + DIRECT entire low proof."""
    started = time.monotonic()
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Cooperative entire-root6000s timer")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "No incomplete whole-root receipt")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Entire joined root256MiB")

    def child_budget():
        budget = min(CHILD_LIMIT, time_limit_seconds - (time.monotonic() - started))
        require(budget > 0, "No omitted root request after runtime expiry")
        return budget

    guard()
    cache = quadrature.build_fresh_quadrature_cache(N, H_STEP,
        time_limit_seconds=child_budget())
    quadrature.validate_preverified_fresh_cache(cache, N, H_STEP)
    target_certificate = leaf.cached.previous.fresh_target_certificate(cache.pi_bracket, cache.phi0_bracket)
    require(target_certificate["target"] == TARGET and target_certificate["CE_lower_exact"] > TARGET,
            "DIRECT fresh target below CE, including zero-cut classes")
    w_faces, beta_faces, requests = root.fresh_root_requests()
    records, child_resources, completed, low_children, high_calls = [], [], 0, 0, 0
    active_request = None
    try:
        for request in requests:
            active_request = request
            guard()
            if request["proved_root_empty"]:
                records.append(dict(request, kind="EXACT_ROOT_EMPTY_BY_STRICT_RHO_CAP",
                    reason="Exact rhoQ_min_square>=cap_square,eta>=0,actualrho<cap; equality excluded by strict cap"))
                continue
            emit("PARENT_JOIN_BEFORE", started, time_limit_seconds, request, completed)
            record, new_resources = compute_fresh_parent_join(request, cache, guard, budget=child_budget)
            records.append(record)
            child_resources.extend(new_resources)
            low_children += record["fresh_low_producer_calls"]
            high_calls += record["fresh_high_producer_calls"]
            completed += 1
            emit("ENTIRE_CLASS_AFTER", started, time_limit_seconds, request, completed,
                 whole_geometry_all_actual_eta_closed=record["whole_geometry_all_actual_eta_closed"],
                 entire_low_eta_result_kind=record["kind"],
                 fixed_geometry_depth_used=record["fixed_geometry_depth_used"])
            guard()
    except Exception as error:
        emit("EXCEPTION_NO_PARTIAL_RECEIPT", started, time_limit_seconds, active_request, completed,
             exception_type=type(error).__name__, exception_message=str(error))
        raise
    require(len(records) == 260 and tuple(record["grid_index"] for record in records) == tuple(range(260)),
            "ALL260 closed geometry classes/shared faces, even UNKNOWN")
    allowed = {"EXACT_ROOT_EMPTY_BY_STRICT_RHO_CAP", "ENTIRE_GEOMETRY_CLOSED_HIGH_ROUTE",
               "FRESH_COMPLETE_ETA_JOIN_CDF_BOUND", "UNKNOWN_LOW_ETA_INTERVALS_RETAINED"}
    require(all(record["kind"] in allowed for record in records), "No implicitly accepted geometry")
    unknown = [record for record in records if record["kind"] == "UNKNOWN_LOW_ETA_INTERVALS_RETAINED"]
    passed = not unknown
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "All direct mathematical sources unchanged through full root")
    guard()
    return {"status": "EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_COMPLETE_ETA_JOIN" if passed
            else "UNKNOWN_WITH_ENTIRE_ROOT_AND_ALL_FAILED_LOW_ETA_CLASSES",
        "date": "2026-10-09", "scale": SCALE, "target": TARGET,
        "root_closed_rectangle": ROOT, "actual_rho_strict_cap": RHO_CAP,
        "fresh_target_certificate": target_certificate,
        "closed_w_faces": w_faces, "closed_beta_abs_faces": beta_faces,
        "SV_external_constants": {"C": root.SV_C, "offset": root.SV_OFFSET,
                                  "closed_rho_threshold": root.SV_RHO},
        "geometry_classes": records,
        "unresolved_geometry_indices": tuple(record["grid_index"] for record in unknown),
        "fresh_quad_cache_metadata": cache.compact_metadata(),
        "summary": {"geometry_classes_total": 260,
            "exact_rho_empty_geometry_classes": sum(record["kind"] == "EXACT_ROOT_EMPTY_BY_STRICT_RHO_CAP" for record in records),
            "fresh_nonempty_root_parent_joins": completed,
            "fresh_complete_high_geometry_children": high_calls,
            "fresh_complete_linked_low_eta_children": low_children,
            "fixed_geometry_max_depth": MAX_DEPTH,
            "parents_checked_by_all4_closed_children": sum("fixed_depth1_closed_children" in record for record in records),
            "geometry_classes_closed_by_complete_eta_join": sum(record["kind"] == "FRESH_COMPLETE_ETA_JOIN_CDF_BOUND" for record in records),
            "geometry_classes_closed_by_zero_cut_high_route": sum(record["kind"] == "ENTIRE_GEOMETRY_CLOSED_HIGH_ROUTE" for record in records),
            "unresolved_geometry_classes": len(unknown),
            "unresolved_closed_eta_classes": sum(unresolved_low_cell_count(record) for record in unknown)},
        "standing_mathematical_premises": {
            "physical_actual_law": "Standardized iid P, canonical coordinates in ROOT,eta>=0,|X|<=17/4,actualrho=rhoQ_actual+eta<46/25; no atom-count/density/separate M4 premise.",
            "fresh_high_route": "DIRECT audited conditional sign-count Cantelli backend eta0 bounds plus exact all-p accounting/root-square pruning; upward strict cut, or ONE complete published iid SV route. No saved frontier/status proof input.",
            "fresh_low_route": "DIRECT corrected TRUE-CF linked-normalized whole-box centre; complete ABS transfer; ONE original-P midpoint reserve and ONE per-cell continuous-frequency H replacement; all16 eta/H/reflections/tails; sign-safe score. Failed parent gets ALL4 fixed depth1 CLOSED children with OWN fresh rho/SV/joint cuts.",
            "analytic_inputs": "Retained CLOSED-CDF Prawitz/physical midpoint bridge and published iid .3031*(1+.646/rho) SV theorem; explicit external mathematics.",
            "first_critical_owner_placement": "Retained C3<CE,equality-level attainment and contact/support-owner structural inputs; not proved by this program."},
        "conclusions": {"all_260_closed_root_geometry_requests_accounted_for": True,
            "conditional_entire_physical_root_R4_le_T_below_CE": passed,
            "every_UNKNOWN_and_closed_eta_join_kept": True,
            "unrestricted_C4_proof_from_program_alone": False,
            "saved_numeric_receipts_or_float_proof_inputs": False,
            "pilot_producer_called_or_INDICES_modified": False,
            "old_sources_or_globals_monkeypatched": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "overall_time_limit_seconds": time_limit_seconds,
            "child_time_limit_seconds": CHILD_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "fresh_cache_resources": cache.resource_metadata(), "child_resources": child_resources,
            "children_sequential": True}}


def self_tests():
    """Pure old260 request/schema and split arithmetic ONLY; no producers."""
    source_drift_check()
    geometry_tests, split_tests = root.self_tests(), split.self_tests()
    extra = 0
    requests = root.fresh_root_requests()[2]
    for index in (0, 93, 149, 208, 247, 259):
        old = requests[index]
        generic = fresh_rectangle_request(old["closed_rectangle"], old["grid_index"])
        require(all(old[key] == value for key, value in generic.items() if key != "geometry_path"),
                "Generic fresh rectangle request matches exact root request, not lookup-based child math")
        extra += 1
        children = closed_four_children(old["closed_rectangle"])
        require(len(children) == 4 and MAX_DEPTH == 1, "Fixed ALL4 closed children at depth exactly1")
        extra += 1
        for child_index, rectangle in enumerate(children):
            child = fresh_rectangle_request(rectangle, index, (child_index,))
            require(child["closed_rectangle"] == rectangle and child["geometry_path"] == (child_index,),
                    "Each child has own exact request and explicit shared-face path")
            extra += 1
    return {"status": "FULL_JOIN_TINY_PURE_ROOT_AND_SPLIT_TESTS_ONLY",
        "exact_checks": geometry_tests["exact_checks"] + split_tests["exact_checks"] + extra,
        "all260_root_geometry_accounted_by_pure_tests": True,
        "cache_Cantelli_Fourier_leaf_pilot_or_global_producer_called": False,
        "synthetic_checks_prove_CDF_or_C4": False, "source_or_receipt_files_written": False}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--produce", action="store_true")
    modes.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if not (args.produce or args.replay_existing):
        print(json.dumps(self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem + "_W20_B13_N256_H1_8_ETA16_Np32_NH256_T4097_10000.json")
    require(args.replay_existing or not output.exists(), "Never overwrite any previous full-root receipt")
    require(not args.replay_existing or output.exists(), "Read-only fresh full-root replay requires receipt")
    result = compute_verified_global_root(time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"),
                     allow_nan=False, default=root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "ALL260 complete-root receipt<=24MiB")
    peak = resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and (peak is None or peak <= MEMORY_LIMIT),
            "Whole CLI including serialization within6000s/256MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only complete-root input")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        require(type(saved) is dict and type(fresh) is dict
                and {key: value for key, value in saved.items() if key != "resources"}
                    == {key: value for key, value in fresh.items() if key != "resources"},
                "Fresh ENTIRE root replay ALL nonresource fields EXACT MATCH")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "unresolved_geometry_indices": result["unresolved_geometry_indices"],
        "output_bytes": len(raw.encode("utf-8")), "resources": result["resources"]},
        sort_keys=True, default=root.json_ready))


if __name__ == "__main__":
    main()
