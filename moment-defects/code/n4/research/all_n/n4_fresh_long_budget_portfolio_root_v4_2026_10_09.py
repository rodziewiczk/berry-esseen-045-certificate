"""NEW robust local600s/root43200s clone with IDENTICAL priced mathematics.

This is a mechanical NEW clone of frozen146394/V3, preserving frozen
V3/V2/5729. The ONLY production changes are the NEW V7/adapterV2 resource
binding, complete optimized TOTAL/postconsumer600s and A1/Gamma phases
180s. Global43200s, outer256MiB and HIGH64MiB remain unchanged. HIGH,
cache and cheap0675 STILL have their original60s clamps.
The I254 producer elapsed about896s; its independent replay then hit a
local TOTAL180s guard without MATCH. These are runtime DIAGNOSTICS, not
mathematical rejection, accepted I254 evidence or a timing guarantee.
No geometry, cutoff, frequency, eta, price, CDF or reserve formula changes.
V3/V2 themselves are minimal NEW clones of frozen5729. Its whole-geometry choices,
priced response mathematics, projections, all260 closed parents and ALL4
closed child covers are unchanged. Every exact parent+four child HIGH
proof is DIRECTLY fresh FIRST under the retained64MiB/60s limits, before
ONE N256/H1/8 cache and any A1 arrays. Cache and cheap0675 also retain60s.
ONLY the optimized complete low join now uses NEW robust-budget adapter:
A1<=180s, Gamma<=180s, V7 postconsumer within remaining TOTAL600s.
The outer deadline is now43200s; its256MiB memory limit is unchanged.
No frozen source, arithmetic,
previous receipt or global binding is modified or monkeypatched.

Complete alternatives stay cheap parent OR optimized parent OR ALL4
complete children, each using its OWN rho/cut and complete CLOSED eta
interval. Cheap UNKNOWN cells only schedule WHOLE optimized proofs; they
never mask eta/H. Exact strict-rho square emptiness includes equality.
A CLOSED high cut0 includes eta0 and skips low. Every attempted UNKNOWN,
all16 eta cells, BOTH reflections, all H/tails and ONE physical reserve
of each kind remain. No finite-atom/density/additionalM4 premise is added.
Correctly-scaled TRUE CF, all exact prices and whole-row score formulas
are untouched; optimized budget is NEVER silently reclamped to old60 or180.

CHECKPOINTS ARE OUTPUTS, NOT MATHEMATICAL INPUTS OR RESUME AUTHORITY.
Only the --produce CLI branch creates a fresh UUID run directory BELOW this
source folder. AFTER each ENTIRE parent has completed its DIRECT
mathematical producer/consumer and the current full source closure still
matches, an exclusive parent *.incomplete.json is streamed. Only after a
complete write, source check and outer resource guard is it renamed to
the corresponding absent *.json within that same validated directory.
No existing checkpoint or final receipt is overwritten. A later failure
leaves completed parent evidence, NOT an entire-root/prefix proof; an
incomplete file is never relabeled as complete or read as numerical truth.

Each checkpoint's canonical math is exactly that live complete parent
record plus the current source-integrity pins. The UUID, run directory,
file names and elapsed diagnostics occur ONLY under resources. The final
ALL260 result still derives from all260 live DIRECT records, never from
parsed checkpoints or saved statuses. No resume/import/checkpoint-reading
path exists. Read-only replay NEVER creates a directory or writes any
checkpoint: it freshly rebuilds ALL1300 HIGH proofs, cache and ALL260
portfolio records, then compares EVERY final nonresource canonical byte.
The final filename is NEW/exclusive; every older file stays unchanged.

Physical mathematical scope remains arbitrary standardized iid actual P
in closedROOT, eta>=0, |X|<=17/4, actualrho=rhoQ_actual+eta<46/25; the
retained CLOSED-CDF Prawitz/original-P bridge and published iid SV input
are explicit. Fresh arithmetic proves T4097/10000<CE. Entire-root or
all-law conclusions require the authentic complete mathematical bound
and the separate accepted C3/attainment/contact/support reduction, not a
checkpoint/status/hash/JSON gate. Numeric UNKNOWN still retains a valid
complete uniform majorant; runtime/scope/resource failures raise and
yield NO complete-root receipt. No all-index/C*=CE claim is made.

Source-only until authorized. Dormant tiny tests use pure budget routing,
path/name checks and StringIO serialization only; no cache/CDF producer,
real checkpoint directory or file write is executed by those tests.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import time
from uuid import uuid4

import n4_fresh_optimized_qnorm_parent_four_child_coordinator_2026_10_09 as parent
import n4_fresh_optimized_qnorm_parent_math_projection_2026_10_09 as projection
import n4_fresh_long_budget_qnorm_geometry_join_adapter_v2_2026_10_09 as long_join

full, cheap, root = parent.full, parent.full.leaf, parent.root
resources, quadrature, require = parent.resources, parent.quadrature, parent.require
SCALE, TARGET, ROOT, RHO_CAP = parent.SCALE, parent.TARGET, full.ROOT, full.RHO_CAP
N, H_STEP, ETA_CELLS = parent.N, parent.H_STEP, parent.ETA_CELLS
TIME_LIMIT, CHILD_LIMIT, OPTIMIZED_LIMIT, MAX_DEPTH = 43200, 60, 600, 1
MEMORY_LIMIT, HIGH_MEMORY_LIMIT = 256 * 1024 * 1024, 64 * 1024 * 1024
OUTPUT_LIMIT, RESOURCE_HEADER_LIMIT = 48 * 1024 * 1024, 4 * 1024 * 1024
PARENT_PIN = "6ad87c2f8dc3bca497b6ba8d81afc0932bc059175299c09410ee83d934556cdd"
PROJECTION_PIN = "40f907b67ea7dcc95c7a76034ab92d3ee99aa33ed81b3c1318d5ce4d377a988b"
FULL_PIN = "e16285e11f10c144d5278accab1bf8468260543e0243c1ab6ffd53caeded6dbd"
CHEAP_PIN = "0675c4bff82423f529e82e943274b0f47cd1cbcd9fbb578de7e15687a3d26b0c"
LONG_JOIN_PIN = "199dcca762fe2855a3a07775c20408f8c84ae7f547d13e244ecebf8dbb3799ea"
FROZEN_MASTER_NAME = "n4_fresh_optimized_qnorm_portfolio_entire_root_2026_10_09.py"
FROZEN_MASTER_PIN = "5729cf8ce3ba9f8bbaabc1f2e10ef05648d55ab389235dfcaca850e74ca5745b"
V2_ORIGIN_NAME = "n4_fresh_long_budget_portfolio_root_v2_2026_10_09.py"
V2_ORIGIN_PIN = "d5368f04472c5252298c68c8fbe7fcb60c525df280ffd2a17366ea47f0db513f"
V3_ORIGIN_NAME = "n4_fresh_long_budget_portfolio_root_v3_2026_10_09.py"
V3_ORIGIN_PIN = "146394adf2ed43f0244df3f2ea36629cb5647db0996f868d091a0ceef59f477a"
CHECKPOINT_ROOT_NAME = Path(__file__).stem + "_checkpoints"


def source_drift_check():
    parent.source_drift_check()
    projection.source_drift_check()
    cheap.source_drift_check()
    long_join.source_drift_check()
    require(hashlib.sha256(Path(__file__).with_name(FROZEN_MASTER_NAME).read_bytes()).hexdigest() == FROZEN_MASTER_PIN,
            "Frozen5729 clone origin integrity only, never old producer")
    require(hashlib.sha256(Path(__file__).with_name(V2_ORIGIN_NAME).read_bytes()).hexdigest() == V2_ORIGIN_PIN,
            "Frozen d536/V2 mechanical origin integrity only, never its producer")
    require(hashlib.sha256(Path(__file__).with_name(V3_ORIGIN_NAME).read_bytes()).hexdigest() == V3_ORIGIN_PIN,
            "Frozen146394/V3 mechanical origin integrity only, never its producer")
    for module, pin in ((parent, PARENT_PIN), (projection, PROJECTION_PIN),
                        (full, FULL_PIN), (cheap, CHEAP_PIN), (long_join, LONG_JOIN_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen math-source integrity only: " + Path(module.__file__).name)
    require(SCALE == full.SCALE == cheap.SCALE and TARGET == full.TARGET == cheap.TARGET
            and N == 256 and H_STEP == F(1, 8) and ETA_CELLS == 16
            and long_join.SCALE == SCALE and long_join.TARGET == TARGET
            and long_join.N == N and long_join.H_STEP == H_STEP
            and long_join.ETA_CELLS == ETA_CELLS and long_join.TIME_LIMIT == OPTIMIZED_LIMIT
            and long_join.PHASE_LIMIT == 180 and long_join.MEMORY_LIMIT == MEMORY_LIMIT,
            "SAME priced math/grids; only optimized600, outer256 and HIGH64 unchanged")


def dependency_pins():
    pins = {}
    for closure in (parent.dependency_pins(), projection.dependency_pins(), cheap.dependency_pins(), long_join.dependency_pins()):
        for name, pin in closure.items():
            require(name not in pins or pins[name] == pin, "Consistent full source/math closure")
            pins[name] = pin
    frozen = Path(__file__).with_name(FROZEN_MASTER_NAME)
    require(frozen.name not in pins or pins[frozen.name] == FROZEN_MASTER_PIN, "Consistent frozen clone-origin pin")
    pins[frozen.name] = FROZEN_MASTER_PIN
    origin = Path(__file__).with_name(V2_ORIGIN_NAME)
    require(origin.name not in pins or pins[origin.name] == V2_ORIGIN_PIN, "Consistent frozenV2 origin pin")
    pins[origin.name] = V2_ORIGIN_PIN
    recent = Path(__file__).with_name(V3_ORIGIN_NAME)
    require(recent.name not in pins or pins[recent.name] == V3_ORIGIN_PIN, "Consistent frozenV3 origin pin")
    pins[recent.name] = V3_ORIGIN_PIN
    path = Path(__file__)
    require(path.name not in pins, "Unique NEW entire-root long-budget source")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def _remaining(budget):
    """Retained SHORT60 routing ONLY for HIGH/cache/cheap."""
    return parent._remaining_budget(budget)


def _optimized_remaining(budget):
    """NEW optimized600 clamp; never old6ad/full min60 or oldadapter180."""
    return long_join.remaining_pair_budget(budget)


def _compact_cheap_after_full_math(checked):
    """e162 PURE compact AFTER DIRECT0675 plus its full consumer, not acceptance."""
    result = full.compact_checked_low_result(checked)
    require(len(result["low_eta_cells"]) == ETA_CELLS, "ALL16 cheap closed cells")
    cells = []
    for compact, original in zip(result["low_eta_cells"], checked["low_eta_cells"]):
        cell = dict(compact)
        cell["normalized_target_Bernstein_coefficients"] = original["normalized_target_Bernstein_coefficients"]
        cell["normalized_score_denominator_face_ratios"] = original["normalized_score_denominator_face_ratios"]
        cells.append(cell)
    result["low_eta_cells"] = tuple(cells)
    return result


def _cheap_join_from_pair(pair, cache, guard, budget):
    """Complete own-cut cheap low/high join; no stale high or JSON importer."""
    request, high = pair
    guard()
    parent._checked_high_pair(request, high)
    if request["proved_root_empty"]:
        return {"request": request, "kind": "EXACT_EMPTY_BY_STRICT_RHO_CAP_INCLUDING_EQUALITY",
            "whole_geometry_all_actual_eta_closed": True, "whole_geometry_score_upper_exact": F(0),
            "own_joint_eta_cut_exact": None, "fresh_complete_low_eta_result": None}, None
    cut = high["joint_eta_cut_exact"]
    if cut == 0:
        return {"request": request, "kind": "ALL_ACTUAL_ETA_CLOSED_HIGH_ROUTE_INCLUDING_ETA0",
            "whole_geometry_all_actual_eta_closed": True,
            "whole_geometry_score_upper_exact": high["joint_high_eta_score_at_closed_cut_exact"],
            "own_joint_eta_cut_exact": cut, "fresh_complete_low_eta_result": None}, None
    started, limit = time.monotonic(), _remaining(budget)

    def low_guard():
        require(time.monotonic() - started < limit, "COMPLETE cheap producer+full consumer<=60s")
        guard()

    def low_remaining():
        value = min(_remaining(budget), limit - (time.monotonic() - started))
        require(value > 0, "No truncated cheap low proof after local expiry")
        return value

    fresh = cheap.compute_verified_low_eta_box_leaf(request["closed_rectangle"], (F(0), cut),
        cache=cache, N=N, H_step=H_STEP, initial_eta_cells=ETA_CELLS, max_eta_cells=ETA_CELLS,
        time_limit_seconds=low_remaining())
    low_guard()
    checked = cheap._checked_fresh_leaf_math(fresh, request, low_eta_cut=cut)
    require(checked["low_eta_closed_scope"] == (F(0), cut)
            and checked["actual_requested_low_eta_cut_exact"] == cut
            and checked["original_SV_eta_cut_exact"] == request["etaSV_exact"]
            and len(checked["low_eta_cells"]) == ETA_CELLS,
            "OWN complete CLOSED low face; original SV is separately retained")
    closed = checked["conditional_whole_low_eta_CDF_bound_verified"]
    upper = max(checked["low_eta_upper_exact"], high["joint_high_eta_score_at_closed_cut_exact"])
    require(type(closed) is bool and type(upper) is F and (not closed or upper <= TARGET),
            "BOTH independent complete low/high routes uniformly bound the geometry")
    record = {"request": request, "kind": "COMPLETE_CHEAP_OWN_LOW_HIGH_JOIN" if closed
            else "UNKNOWN_CHEAP_LOW_CELLS_RETAINED", "whole_geometry_all_actual_eta_closed": closed,
        "whole_geometry_score_upper_exact": upper, "own_joint_eta_cut_exact": cut,
        "complete_low_high_join_summary": {"closed_low_eta_interval": (F(0), cut),
            "complete_high_eta_includes_closed_cut_and_all_actual_larger_eta": True,
            "conditional_entire_declared_geometry_all_actual_eta_closed": closed,
            "original_SV_eta_cut_exact": request["etaSV_exact"],
            "low_cut_override_is_not_an_above_cut_SV_theorem": True,
            "entire_260_root_or_unrestricted_C4_proved_by_this_join": False},
        "fresh_complete_low_eta_result": _compact_cheap_after_full_math(checked)}
    resource = {"route": "cheap0675", "grid_index": request["grid_index"],
        "geometry_path": request["geometry_path"], "complete_low_elapsed_seconds_diagnostic": time.monotonic() - started,
        "local_time_limit_seconds": limit, "producer_resources": fresh["resources"]}
    low_guard()
    del fresh, checked
    guard()
    return record, resource


def _optimized_join_from_pair(pair, cache, guard, budget):
    """DIRECT NEW600 adapter, SAME priced math/outer256 and complete scope."""
    record, resource = long_join.complete_geometry_join_from_pair(pair, cache, guard, budget)
    projected = dict(record)
    # Same complete DIRECT math/shape as40f; V7 differs ONLY by resource budget.
    projected["fresh_complete_low_eta_result"] = projection._project_complete_low_result(
        record["fresh_complete_low_eta_result"])
    guard()
    if resource is not None:
        resource = dict(resource, route="optimized_V7", grid_index=pair[0]["grid_index"],
                        geometry_path=pair[0]["geometry_path"])
    return projected, resource


def _checked_complete_geometry(record, request):
    """Structural consistency AFTER DIRECT audited join, NEVER proof from flags."""
    require(type(record) is dict and record["request"] == request
            and type(record["whole_geometry_all_actual_eta_closed"]) is bool
            and type(record["whole_geometry_score_upper_exact"]) is F,
            "SAME complete geometry and exact uniform score")
    require(not record["whole_geometry_all_actual_eta_closed"]
            or record["whole_geometry_score_upper_exact"] <= TARGET, "Complete accepted bound<=T")
    if request["proved_root_empty"]:
        require(record["whole_geometry_all_actual_eta_closed"]
                and record["whole_geometry_score_upper_exact"] == 0,
                "Exact empty class score0, not missing evidence")
    return record


def _select_complete_child(cheap_record, optimized_record, request):
    _checked_complete_geometry(cheap_record, request)
    if optimized_record is not None:
        _checked_complete_geometry(optimized_record, request)
    if cheap_record["whole_geometry_all_actual_eta_closed"]:
        selected, route = cheap_record, "COMPLETE_CHEAP_CHILD"
    elif optimized_record is not None and optimized_record["whole_geometry_all_actual_eta_closed"]:
        selected, route = optimized_record, "COMPLETE_OPTIMIZED_CHILD"
    else:
        # For UNKNOWN diagnostics only: each is still a valid WHOLE majorant.
        selected, route = cheap_record, "UNKNOWN_COMPLETE_CHEAP_CHILD"
        if optimized_record is not None and optimized_record["whole_geometry_score_upper_exact"] < selected["whole_geometry_score_upper_exact"]:
            selected, route = optimized_record, "UNKNOWN_COMPLETE_OPTIMIZED_CHILD"
    return {"request": request, "selected_WHOLE_geometry_route": route,
        "whole_geometry_all_actual_eta_closed": selected["whole_geometry_all_actual_eta_closed"],
        "whole_geometry_score_upper_exact": selected["whole_geometry_score_upper_exact"]}


def _portfolio_summary(requests, cheap_parent, cheap_children, optimized_parent, optimized_children):
    """Pure complete-geometry OR / ALL4 logic under DIRECT mathematical premises."""
    require(len(requests) == 5 and len(cheap_children) in (0, 4)
            and type(optimized_children) is dict, "Fixed parent+ALL4 closed cover shape")
    _checked_complete_geometry(cheap_parent, requests[0])
    if optimized_parent is not None:
        _checked_complete_geometry(optimized_parent, requests[0])
    require(all(type(i) is int and 0 <= i < 4 for i in optimized_children), "Only exact child0..3")
    if cheap_parent["whole_geometry_all_actual_eta_closed"]:
        require(not cheap_children and optimized_parent is None and not optimized_children,
                "Complete cheap parent alone, no unnecessary partial cover")
        selected_children = ()
        route, upper, closed = "DIRECT_COMPLETE_CHEAP_PARENT", cheap_parent["whole_geometry_score_upper_exact"], True
    else:
        require(len(cheap_children) == 4, "UNKNOWN cheap parent requires EVERY four cheap child")
        for index, child in enumerate(cheap_children):
            _checked_complete_geometry(child, requests[index + 1])
        cheap_cover = all(child["whole_geometry_all_actual_eta_closed"] for child in cheap_children)
        if cheap_cover:
            require(optimized_parent is None and not optimized_children, "Entire cheap cover before optimization")
        else:
            require(optimized_parent is not None, "Whole V7 parent is tried before selective child scheduling")
            if not optimized_parent["whole_geometry_all_actual_eta_closed"]:
                expected = {i for i, child in enumerate(cheap_children) if not child["whole_geometry_all_actual_eta_closed"]}
                require(set(optimized_children) == expected, "EVERY cheap-failed child V7, even earlier failure")
            else:
                require(not optimized_children, "Complete V7 parent alone is a legitimate alternative")
        selected_children = tuple(_select_complete_child(child, optimized_children.get(i), requests[i + 1])
                                  for i, child in enumerate(cheap_children))
        child_cover = all(child["whole_geometry_all_actual_eta_closed"] for child in selected_children)
        if cheap_cover:
            route, upper, closed = "ALL_FOUR_COMPLETE_CHEAP_CLOSED_CHILDREN", max(
                child["whole_geometry_score_upper_exact"] for child in selected_children), True
        elif optimized_parent["whole_geometry_all_actual_eta_closed"]:
            route, upper, closed = "DIRECT_COMPLETE_OPTIMIZED_PARENT", optimized_parent["whole_geometry_score_upper_exact"], True
        else:
            route = "ALL_FOUR_COMPLETE_CHILD_PORTFOLIOS" if child_cover else "UNKNOWN_ALL_FOUR_CHILD_PORTFOLIOS_RETAINED"
            upper, closed = max(child["whole_geometry_score_upper_exact"] for child in selected_children), child_cover
    require(type(closed) is bool and type(upper) is F and (not closed or upper <= TARGET),
            "WHOLE parent: direct complete alternative OR exhaustive complete4-child MAX")
    return {"whole_parent_all_actual_eta_closed": closed, "whole_parent_score_upper_exact": upper,
        "selected_complete_closure_route": route, "selected_complete_child_bounds": selected_children,
        "unresolved_child_indices": tuple(i for i, child in enumerate(selected_children)
            if not child["whole_geometry_all_actual_eta_closed"]),
        "cheap_child_joins_attempted": len(cheap_children), "optimized_child_joins_attempted": len(optimized_children),
        "optimized_parent_join_attempted": optimized_parent is not None,
        "cheap_cell_failures_used_only_to_schedule_WHOLE_optimized_geometry": True}


def compute_fresh_parent_portfolio(index, prepared_high, cache, guard, budget=OPTIMIZED_LIMIT):
    """Caller just DIRECTLY prepared all1300 HIGH first and ONE fresh cache."""
    requests = parent.fresh_parent_and_child_requests(index)
    pairs = parent._checked_direct_pairs(requests, prepared_high)
    quadrature.validate_preverified_fresh_cache(cache, N, H_STEP)
    cheap_parent, resource = _cheap_join_from_pair(pairs[0], cache, guard, budget)
    resource_records = [] if resource is None else [resource]
    cheap_children, optimized_parent, optimized_children = [], None, {}
    if not cheap_parent["whole_geometry_all_actual_eta_closed"]:
        for pair in pairs[1:]:
            child, resource = _cheap_join_from_pair(pair, cache, guard, budget)
            cheap_children.append(child)
            if resource is not None:
                resource_records.append(resource)
        if not all(child["whole_geometry_all_actual_eta_closed"] for child in cheap_children):
            optimized_parent, resource = _optimized_join_from_pair(pairs[0], cache, guard, budget)
            if resource is not None:
                resource_records.append(resource)
            if not optimized_parent["whole_geometry_all_actual_eta_closed"]:
                for child_index, child in enumerate(cheap_children):
                    if not child["whole_geometry_all_actual_eta_closed"]:
                        optimized, resource = _optimized_join_from_pair(pairs[child_index + 1], cache, guard, budget)
                        optimized_children[child_index] = optimized
                        if resource is not None:
                            resource_records.append(resource)
    summary = _portfolio_summary(requests, cheap_parent, cheap_children, optimized_parent, optimized_children)
    guard()
    return {"root_index": index, "whole_parent_request": requests[0],
        "all_five_exact_requests": requests, "all_five_DIRECT_high_pairs": pairs,
        "cheap_parent_complete_join": cheap_parent,
        "all_four_cheap_child_joins_if_cheap_parent_UNKNOWN": tuple(cheap_children),
        "optimized_parent_complete_join_if_cheap_cover_UNKNOWN": optimized_parent,
        "optimized_complete_joins_for_ALL_cheap_failed_children_if_needed": optimized_children,
        "summary": summary,
        "conclusions": {"conditional_entire_declared_parent_all_actual_eta_closed": summary["whole_parent_all_actual_eta_closed"],
            "unrestricted_C4_or_entire_root_from_single_parent": False,
            "point_eta_H_mask_or_coefficientwise_route_min_used": False}}, tuple(resource_records)


def compute_verified_global_root(time_limit_seconds=TIME_LIMIT, checkpoint_directory=None):
    started = time.monotonic()
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Cooperative whole43200s sequential budget")
    source_drift_check()
    initial_pins = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "No runtime-truncated entire-root receipt")
        peak = resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Observed complete-root256MiB")

    def remaining():
        return min(CHILD_LIMIT, time_limit_seconds - (time.monotonic() - started))

    def optimized_remaining():
        return min(OPTIMIZED_LIMIT, time_limit_seconds - (time.monotonic() - started))

    guard()
    if checkpoint_directory is not None:
        checkpoint_directory = _checked_checkpoint_directory(checkpoint_directory)
        require(not any(checkpoint_directory.iterdir()), "Fresh EMPTY exclusive run directory, never resume")
    checkpoint_files = []
    w_faces, beta_faces, original_requests = root.fresh_root_requests()
    require(len(original_requests) == 260 and tuple(r["grid_index"] for r in original_requests) == tuple(range(260)),
            "ALL260 original closed root rectangles, not a historic failure schedule")
    prepared, high_resources, records, low_resources = [], [], [], []
    active_request = None
    try:
        for index in range(260):
            active_request = parent.fresh_parent_and_child_requests(index)[0]
            original = original_requests[index]
            require(active_request["closed_rectangle"] == original["closed_rectangle"]
                    and index == 13 * original["w_index"] + original["beta_index"]
                    and all(original.get(key) == value for key, value in active_request.items() if key != "geometry_path"),
                    "Canonical parent matches ENTIRE original root class")
            pairs, new_resources = parent.prepare_fresh_parent_high(index, guard, remaining)
            prepared.append(pairs)
            high_resources.extend(new_resources)
            full.emit("ALL_HIGH_FIRST_PARENT_AFTER", started, time_limit_seconds, active_request, index + 1,
                      exact_high_request_slots_accounted=5 * (index + 1))
        require(len(prepared) == 260 and all(len(pairs) == 5 for pairs in prepared),
                "ALL1300 HIGH own-scope proofs completed before ANY cache/A1")
        cache = quadrature.build_fresh_quadrature_cache(N, H_STEP, time_limit_seconds=_remaining(remaining))
        quadrature.validate_preverified_fresh_cache(cache, N, H_STEP)
        certificate = cheap.cached.previous.fresh_target_certificate(cache.pi_bracket, cache.phi0_bracket)
        require(certificate["target"] == TARGET and certificate["CE_lower_exact"] > TARGET, "DIRECT fresh T<CE")
        guard()
        for index, pairs in enumerate(prepared):
            active_request = pairs[0][0]
            full.emit("WHOLE_PARENT_PORTFOLIO_BEFORE", started, time_limit_seconds, active_request, len(records))
            record, new_resources = compute_fresh_parent_portfolio(index, pairs, cache, guard, optimized_remaining)
            records.append(record)
            low_resources.extend(new_resources)
            if checkpoint_directory is not None:
                source_drift_check()
                require(dependency_pins() == initial_pins, "Whole source closure unchanged BEFORE complete checkpoint")
                checkpoint_files.append(_write_parent_checkpoint(checkpoint_directory, record, initial_pins, guard))
            full.emit("WHOLE_PARENT_PORTFOLIO_AFTER", started, time_limit_seconds, active_request, len(records),
                      whole_geometry_all_actual_eta_closed=record["summary"]["whole_parent_all_actual_eta_closed"],
                      selected_complete_route=record["summary"]["selected_complete_closure_route"])
            guard()
    except Exception as error:
        full.emit("EXCEPTION_NO_PARTIAL_RECEIPT", started, time_limit_seconds, active_request, len(records),
                  exception_type=type(error).__name__, exception_message=str(error))
        raise
    require(len(records) == 260 and tuple(record["root_index"] for record in records) == tuple(range(260)),
            "EVERY closed parent/root face is accounted, even UNKNOWN")
    unresolved = tuple(record["root_index"] for record in records if not record["summary"]["whole_parent_all_actual_eta_closed"])
    passed = not unresolved
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "Complete source closure unchanged through ALL fresh root arithmetic")
    guard()
    upper = max(record["summary"]["whole_parent_score_upper_exact"] for record in records)
    require(not passed or upper <= TARGET, "ENTIRE conditional root uniformly<=T<CE")
    return {"status": "EXACT_CONDITIONAL_ENTIRE_PHYSICAL_ROOT_PORTFOLIO" if passed
            else "UNKNOWN_WITH_ENTIRE_ROOT_AND_ALL_PORTFOLIO_GAPS_RETAINED",
        "date": "2026-10-09", "scale": SCALE, "target": TARGET,
        "root_closed_rectangle": ROOT, "actual_rho_strict_cap": RHO_CAP,
        "closed_w_faces": w_faces, "closed_beta_abs_faces": beta_faces,
        "fresh_target_certificate": certificate, "geometry_classes": tuple(records),
        "unresolved_geometry_indices": unresolved, "fresh_quad_cache_metadata": cache.compact_metadata(),
        "SV_external_constants": {"C": root.SV_C, "offset": root.SV_OFFSET, "closed_rho_threshold": root.SV_RHO},
        "summary": {"geometry_classes_total": 260, "exact_rho_empty_parent_classes": sum(
            record["whole_parent_request"]["proved_root_empty"] for record in records),
            "closed_geometry_classes": 260 - len(unresolved), "unresolved_geometry_classes": len(unresolved),
            "entire_conditional_root_score_upper_exact": upper, "ALL_high_request_slots_accounted": 1300,
            "DIRECT_high_producer_calls": len(high_resources), "DIRECT_complete_low_producer_calls": len(low_resources),
            "complete_cheap_low_producer_calls": sum(r["route"] == "cheap0675" for r in low_resources),
            "complete_optimized_low_producer_calls": sum(r["route"] == "optimized_V7" for r in low_resources),
            "fixed_geometry_max_depth": MAX_DEPTH,
            "closure_route_counts": {route: sum(record["summary"]["selected_complete_closure_route"] == route for record in records)
                for route in sorted({record["summary"]["selected_complete_closure_route"] for record in records})}},
        "standing_mathematical_premises": {
            "physical_actual_law": "Arbitrary standardized iid P in closedROOT,eta>=0,|X|<=17/4,actualrho=rhoQ_actual+eta<46/25; no finite-atom/density/separateM4 premise.",
            "high_route": "DIRECT all1300 SAME-request conditional sign-count Cantelli/SV proofs BEFORE cache/A1; fullp/root pruning, own CLOSED joint cuts. No saved scores/masks/status truth.",
            "low_portfolio": "DIRECT correctly-scaled TRUECF cheap linked whole-box leaf/full pure validator OR DIRECT NEW600 A1/Gamma/V7 complete SAME qnorm low; ALL16eta/ALLH2/tails/ONE original quad and ONE H replacement. Parentcomplete OR ALL4 closed-child complete alternatives.",
            "analytic_inputs": "Retained CLOSED-CDF Prawitz/original-P physical midpoint bridge and published iid .3031*(1+.646/rho) SV envelope.",
            "first_critical_all_law_placement": "Retained C3/attainment/contact/support-owner hypotheses are external. This program alone does not prove unrestrictedC4; no fresh literature axioms added."},
        "conclusions": {"all_260_closed_root_geometry_requests_accounted_for": True,
            "conditional_entire_physical_root_R4_le_T_below_CE": passed,
            "every_UNKNOWN_and_ALL_attempted_closed_eta_scopes_kept": True,
            "unrestricted_C4_proof_from_program_alone": False,
            "saved_numeric_receipts_float_inputs_or_historic_closed_mask_used": False,
            "legacy_bad_CF_pilot_or_old_entire_root_producers_called": False,
            "globals_monkeypatched_or_frozen_files_modified": False,
            "optional_refined_H_eta_ceiling_or_CF_reuse_upgrade_added": False,
            "checkpoint_files_or_saved_statuses_used_as_mathematical_inputs": False,
            "completed_checkpoints_alone_prove_entire_root": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "overall_time_limit_seconds": time_limit_seconds,
            "cheap_low_time_limit_seconds": CHILD_LIMIT, "optimized_complete_low_time_limit_seconds": OPTIMIZED_LIMIT,
            "A1_and_Gamma_phase_time_limit_seconds": long_join.PHASE_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "strict_HIGH_phase_memory_limit_bytes": HIGH_MEMORY_LIMIT,
            "fresh_cache_resources": cache.resource_metadata(), "high_resources": tuple(high_resources),
            "low_resources": tuple(low_resources), "all_stages_sequential": True,
            "checkpoint_run_directory": None if checkpoint_directory is None else str(checkpoint_directory),
            "complete_parent_checkpoint_files": tuple(checkpoint_files),
            "checkpoint_files_read_as_numeric_inputs_or_used_to_resume": False}}



def _checkpoint_directory_path(source_directory, run_id):
    """PURE path plan: UUID child strictly below this exact source directory."""
    require(isinstance(source_directory, Path) and type(run_id) is str
            and re.fullmatch(r"[0-9a-f]{32}", run_id) is not None,
            "Exact resolved source directory and fresh UUID hex only")
    source_directory = source_directory.resolve()
    checkpoint_root = source_directory / CHECKPOINT_ROOT_NAME
    directory = checkpoint_root / run_id
    require(checkpoint_root.resolve().parent == source_directory
            and directory.resolve().parent == checkpoint_root.resolve(),
            "Checkpoint targets remain strictly BELOW the named source directory")
    require(not checkpoint_root.is_symlink() and not directory.is_symlink(),
            "No symlink checkpoint root/run target")
    return directory


def _checked_checkpoint_directory(directory):
    """Production run directory scope; no checkpoint JSON is read or accepted."""
    require(isinstance(directory, Path), "Checkpoint directory is an explicit Path")
    source_directory = Path(__file__).resolve().parent
    canonical = _checkpoint_directory_path(source_directory, directory.name)
    require(directory.resolve() == canonical.resolve()
            and canonical.is_dir() and not canonical.is_symlink(),
            "Existing exact UUID directory BELOW this source folder only")
    return canonical


def create_checkpoint_run_directory(guard):
    """PRODUCE only: create NEW exclusive UUID run directory, no overwrite."""
    require(callable(guard), "Outer whole-CLI resource guard")
    guard()
    directory = _checkpoint_directory_path(Path(__file__).resolve().parent, uuid4().hex)
    checkpoint_root = directory.parent
    checkpoint_root.mkdir(exist_ok=True)
    require(checkpoint_root.is_dir() and not checkpoint_root.is_symlink()
            and checkpoint_root.resolve().parent == Path(__file__).resolve().parent,
            "Resolved checkpoint root remains within source folder")
    directory.mkdir(exist_ok=False)
    directory = _checked_checkpoint_directory(directory)
    require(not any(directory.iterdir()), "NEW exclusive UUID directory starts empty")
    guard()
    return directory


def _checkpoint_directory_for_mode(read_only_replay, creator):
    """Replay NEVER calls any creator/writer; no saved checkpoint input path."""
    require(type(read_only_replay) is bool and callable(creator), "Explicit mode and callable producer creator")
    return None if read_only_replay else creator()


def _checkpoint_file_names(index):
    """PURE exact scope-specific names; included raw class index0..259."""
    require(type(index) is int and 0 <= index < 260, "Exact entire-root parent index")
    stem = "parent_" + str(index).zfill(3) + "_N256_H1_8_ETA16_five_budget"
    return stem + ".incomplete.json", stem + ".json"


def _checkpoint_paths(directory, index):
    directory = _checked_checkpoint_directory(directory)
    incomplete_name, final_name = _checkpoint_file_names(index)
    incomplete, final = directory / incomplete_name, directory / final_name
    require(incomplete.resolve().parent == directory.resolve()
            and final.resolve().parent == directory.resolve()
            and not incomplete.is_symlink() and not final.is_symlink(),
            "Both exact checkpoint file targets stay inside the same UUID run")
    require(not incomplete.exists() and not final.exists(), "No checkpoint overwrite or resume")
    return incomplete, final


def _checkpoint_math_payload(record, pins):
    """AFTER DIRECT complete parent ONLY; structural checks do not prove CDF."""
    require(type(record) is dict and type(pins) is dict, "Live complete result/source closure")
    index = record["root_index"]
    requests = parent.fresh_parent_and_child_requests(index)
    require(record["whole_parent_request"] == requests[0]
            and tuple(record["all_five_exact_requests"]) == requests,
            "Exact whole parent/ALL4 closed children match the live result")
    parent._checked_direct_pairs(requests, record["all_five_DIRECT_high_pairs"])
    summary = _portfolio_summary(requests, record["cheap_parent_complete_join"],
        record["all_four_cheap_child_joins_if_cheap_parent_UNKNOWN"],
        record["optimized_parent_complete_join_if_cheap_cover_UNKNOWN"],
        record["optimized_complete_joins_for_ALL_cheap_failed_children_if_needed"])
    require(summary == record["summary"], "Complete live whole-geometry OR/ALL4 arithmetic unchanged")
    require(Path(__file__).name in pins and pins[Path(__file__).name]
            == hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "Current complete-source integrity snapshot")
    return {"complete_parent_result": record, "source_pins_integrity_only": dict(pins)}


def _write_parent_checkpoint(directory, record, pins, guard):
    """Write/rename ONLY complete live math; NEVER parse a checkpoint as input."""
    require(callable(guard), "Caller outer256/time guard")
    guard()
    incomplete, final = _checkpoint_paths(directory, record["root_index"])
    payload = _checkpoint_math_payload(record, pins)
    source_drift_check()
    require(dependency_pins() == pins, "Current source closure equals live run snapshot")
    checkpoint = dict(payload, resources={"checkpoint_path_diagnostic": str(final),
        "entire_root_or_prefix_proof": False, "saved_numeric_math_used_as_input": False})
    size = _receipt_size(checkpoint, guard)
    # Exclusive new file. A failure leaves .incomplete.json, never a root proof.
    with incomplete.open("x", encoding="utf-8", newline="\n") as stream:
        _write_receipt(stream, checkpoint, guard)
        stream.flush()
    guard()
    source_drift_check()
    require(dependency_pins() == pins, "Source closure unchanged AFTER complete checkpoint write")
    require(incomplete.is_file() and not incomplete.is_symlink()
            and not final.exists() and not final.is_symlink(), "Exact completed source file/absent publish target")
    require(incomplete.resolve().parent == directory.resolve()
            and final.resolve().parent == directory.resolve(), "Revalidated rename stays inside UUID directory")
    guard()
    # Windows Path.rename does not replace an existing target; the private
    # fresh UUID directory plus absent-target check supplies the same scope.
    incomplete.rename(final)
    guard()
    return {"root_index": record["root_index"], "checkpoint_path": str(final),
        "complete_checkpoint_bytes_diagnostic": size,
        "checkpoint_is_not_entire_root_or_accepted_prefix": True}


def _encoder():
    return json.JSONEncoder(sort_keys=True, separators=(",", ":"), allow_nan=False, default=root.json_ready)


def _canonical_math_chunks(result):
    """ALL nonresource fields, deterministic ASCII JSON; no numeric input read."""
    require(type(result) is dict and "resources" in result and len(result) > 1, "Complete result with top-only resources")
    values = {key: value for key, value in result.items() if key != "resources"}
    chunks = iter(_encoder().iterencode(values))
    require(next(chunks) == "{", "Canonical math dictionary framing")
    yield from chunks  # omit ONLY its first '{'; final '}' closes full receipt


def _receipt_chunks(result):
    yield '{"resources":'
    yield from _encoder().iterencode(result["resources"])
    yield ","
    yield from _canonical_math_chunks(result)
    yield "\n"


def _receipt_size(result, guard):
    total, unchecked = 0, 0
    for chunk in _receipt_chunks(result):
        size = len(chunk.encode("utf-8"))
        total += size
        unchecked += size
        require(total <= OUTPUT_LIMIT, "Complete whole-root streamed receipt<=48MiB")
        if unchecked >= 65536:
            guard()
            unchecked = 0
    guard()
    return total


def _write_receipt(stream, result, guard):
    unchecked = 0
    for chunk in _receipt_chunks(result):
        stream.write(chunk)
        unchecked += len(chunk)
        if unchecked >= 65536:
            guard()
            unchecked = 0
    guard()


def _read_resource_header(stream):
    """Read only bounded diagnostic JSON; math remains unread as numerical data."""
    prefix = '{"resources":'
    require(stream.read(len(prefix)) == prefix, "NEW canonical resource-first receipt framing")
    require(stream.read(1) == "{", "Resource header is one JSON object")
    parts, depth, in_string, escaped = ["{"], 1, False, False
    while depth:
        char = stream.read(1)
        require(char != "", "Complete diagnostic header, not truncated receipt")
        parts.append(char)
        require(len(parts) <= RESOURCE_HEADER_LIMIT, "Small ignored diagnostic header<=4MiB")
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "{[":
            depth += 1
        elif char in "}]":
            depth -= 1
    diagnostic = json.loads("".join(parts))
    require(type(diagnostic) is dict and stream.read(1) == ",", "Valid diagnostics followed by ALL math")
    return diagnostic


def _compare_canonical_math(stream, result, guard):
    """Fresh full arithmetic BEFORE exact comparison of ALL nonresource bytes."""
    _read_resource_header(stream)
    unchecked = 0
    for chunk in _canonical_math_chunks(result):
        require(stream.read(len(chunk)) == chunk, "ALL nonresource fresh mathematical fields EXACT MATCH")
        unchecked += len(chunk)
        if unchecked >= 65536:
            guard()
            unchecked = 0
    require(stream.read(1) == "\n" and stream.read(1) == "", "No omitted/extra receipt fields or suffix")
    guard()


def self_tests():
    """Dormant tiny PURE scope/whole-route/streaming checks, NO math producers."""
    from io import StringIO
    source_drift_check()
    checks = 0
    w_faces, beta_faces, original = root.fresh_root_requests()
    require(len(w_faces) == 21 and len(beta_faces) == 14 and len(original) == 260, "ENTIRE20x13 geometry")
    checks += 1
    for index in (0, 93, 149, 200, 247, 259):
        requests = parent.fresh_parent_and_child_requests(index)
        require(requests[0]["closed_rectangle"] == original[index]["closed_rectangle"]
                and index == 13 * original[index]["w_index"] + original[index]["beta_index"]
                and all(original[index].get(key) == value for key, value in requests[0].items() if key != "geometry_path")
                and tuple(r["closed_rectangle"] for r in requests[1:]) == full.closed_four_children(requests[0]["closed_rectangle"]),
                "ALL4closed children and original parent")
        checks += 1
    # Synthetic complete-route flags below test Boolean algebra ONLY; they
    # are deliberately NOT passed to any CF/Cantelli/A1/Gamma/CDF producer.
    requests = tuple({"synthetic": i, "proved_root_empty": False} for i in range(5))

    def record(i, closed, score=None):
        return {"request": requests[i], "whole_geometry_all_actual_eta_closed": closed,
                "whole_geometry_score_upper_exact": (TARGET - F(1, 100) if closed else TARGET + F(1, 100))
                    if score is None else score}

    good_parent, bad_parent = record(0, True), record(0, False)
    good_children = tuple(record(i + 1, True) for i in range(4))
    some_bad = tuple(record(i + 1, i != 2) for i in range(4))
    all_bad = tuple(record(i + 1, False) for i in range(4))
    require(_portfolio_summary(requests, good_parent, (), None, {})["whole_parent_all_actual_eta_closed"], "WHOLE cheap parent")
    require(_portfolio_summary(requests, bad_parent, good_children, None, {})["whole_parent_all_actual_eta_closed"], "ALL4 cheap cover")
    require(_portfolio_summary(requests, bad_parent, some_bad, good_parent, {})["whole_parent_all_actual_eta_closed"], "WHOLE V7parent alternative")
    require(_portfolio_summary(requests, bad_parent, some_bad, bad_parent, {2: record(3, True)})["whole_parent_all_actual_eta_closed"], "Different COMPLETE routes perchild")
    require(not _portfolio_summary(requests, bad_parent, all_bad, bad_parent,
            {i: record(i + 1, i != 3) for i in range(4)})["whole_parent_all_actual_eta_closed"], "One UNKNOWNchild keepsWHOLEparent UNKNOWN")
    checks += 5
    rejected = False
    try:
        _portfolio_summary(requests, bad_parent, all_bad, bad_parent, {0: record(1, True)})
    except RuntimeError:
        rejected = True
    require(rejected, "No early stop/omitted V7 cheapfailedchildren")
    checks += 1
    synthetic = {"status": "SYNTHETIC_NOT_A_PROOF", "fraction": F(-3, 7),
        "math_nested": (True, False, {"unicode": "zażółć", "escaped": '"}{\\'}),
        "resources": {"elapsed": 1.25, "nested": [{"braces": "}{[]", "quote": '\\"'}]}}
    encoded = "".join(_receipt_chunks(synthetic))
    require(json.loads(encoded) == json.loads(json.dumps(synthetic, default=root.json_ready)), "Streaming valid JSON, SAME all fields")
    _compare_canonical_math(StringIO(encoded), synthetic, lambda: None)
    altered_resources = dict(synthetic, resources={"different_runtime": 999})
    _compare_canonical_math(StringIO("".join(_receipt_chunks(altered_resources))), synthetic, lambda: None)
    require(_receipt_size(synthetic, lambda: None) == len(encoded.encode("utf-8")), "Exact streamed size")
    checks += 4
    for corrupted in (encoded.replace("SYNTHETIC_NOT_A_PROOF", "TAMPERED"), encoded + "{}", encoded[:-2]):
        rejected = False
        try:
            _compare_canonical_math(StringIO(corrupted), synthetic, lambda: None)
        except RuntimeError:
            rejected = True
        require(rejected, "Any math change/truncation/extra suffix rejected")
        checks += 1
    # New checks remain PURE: no directory creator, file writer or producer.
    require(_remaining(F(720)) == 60 and _optimized_remaining(F(720)) == 600
            and _remaining(lambda: F(240)) == 60 and _optimized_remaining(lambda: F(240)) == 240
            and long_join.PHASE_LIMIT == 180,
            "Separate HIGH/cache/cheap60 versus optimized600/phases180, scalar and callable")
    checks += 1
    directory = _checkpoint_directory_path(Path(__file__).resolve().parent, "a" * 32)
    require(directory.parent.parent == Path(__file__).resolve().parent
            and directory.name == "a" * 32, "Checkpoint directory STRICTLY below source")
    checks += 1
    for bad_run_id in ("../escape", "a" * 31, "A" * 32):
        rejected = False
        try:
            _checkpoint_directory_path(Path(__file__).resolve().parent, bad_run_id)
        except RuntimeError:
            rejected = True
        require(rejected, "No path escape/noncanonical UUID names")
        checks += 1
    require(_checkpoint_file_names(0) == ("parent_000_N256_H1_8_ETA16_five_budget.incomplete.json",
            "parent_000_N256_H1_8_ETA16_five_budget.json")
            and _checkpoint_file_names(259)[1].startswith("parent_259_"), "Exact all-parent checkpoint names")
    checks += 1
    called = []
    def synthetic_creator():
        called.append(True)
        return directory
    require(_checkpoint_directory_for_mode(True, synthetic_creator) is None and not called,
            "READONLY replay NEVER invokes directory creator")
    require(_checkpoint_directory_for_mode(False, synthetic_creator) == directory and called == [True],
            "Only explicit produce requests checkpoint creation")
    checks += 2
    checkpoint_synthetic = {"complete_parent_result": {"root_index": 0,
        "WHOLE_synthetic_not_CDF": True, "fraction": F(-2, 9)},
        "source_pins_integrity_only": {"synthetic_only": "a" * 64},
        "resources": {"UUID_path_diagnostic_only": str(directory)}}
    checkpoint_encoded = "".join(_receipt_chunks(checkpoint_synthetic))
    _compare_canonical_math(StringIO(checkpoint_encoded), checkpoint_synthetic, lambda: None)
    require("UUID_path_diagnostic_only" not in "".join(_canonical_math_chunks(checkpoint_synthetic)),
            "Checkpoint path/UUID is RESOURCES ONLY, all live math remains canonical")
    checks += 1
    return {"status": "TINY_PURE_LONG_BUDGET_PORTFOLIO_CHECKPOINT_AND_STREAM_TESTS_ONLY", "exact_checks": checks,
        "CF_cache_Cantelli_A1_Gamma_radius_CDF_or_global_producer_called": False,
        "synthetic_flags_prove_CDF_or_C4": False, "source_or_receipt_files_written": False,
        "checkpoint_directories_or_real_files_created_by_tiny_tests": False}


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
    output = Path(__file__).with_name(Path(__file__).stem + "_ALL260_W20_B13_N256_H1_8_ETA16_five_budget.json")
    require(args.replay_existing or not output.exists(), "Never overwrite ANY frozen complete-root receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay requires complete result")

    def cli_guard():
        peak = resources.peak_bytes()
        require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
                "Entire CLI including streaming/replay43200s256MiB")

    checkpoint_directory = _checkpoint_directory_for_mode(args.replay_existing,
        lambda: create_checkpoint_run_directory(cli_guard))
    result = compute_verified_global_root(TIME_LIMIT - (time.monotonic() - started),
        checkpoint_directory=checkpoint_directory)
    size = _receipt_size(result, cli_guard)
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded complete-root read-only input")
        with output.open("r", encoding="utf-8", newline="") as stream:
            _compare_canonical_math(stream, result, cli_guard)
        status = "READ_ONLY_REPLAY_ALL_NONRESOURCE_FIELDS_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            _write_receipt(stream, result, cli_guard)
        status = result["status"]
    cli_guard()
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "unresolved_geometry_indices": result["unresolved_geometry_indices"],
        "fresh_output_bytes_diagnostic": size,
        "resources": {"actual_CLI_elapsed_seconds": time.monotonic() - started,
            "actual_CLI_peak_working_set_bytes": resources.peak_bytes(),
            "time_limit_seconds": TIME_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "fresh_computation_elapsed_seconds": result["resources"]["elapsed_seconds_diagnostic"],
            "checkpoint_run_directory": result["resources"]["checkpoint_run_directory"],
            "read_only_replay_wrote_any_checkpoint": False}},
        sort_keys=True, allow_nan=False, default=root.json_ready))


if __name__ == "__main__":
    main()
