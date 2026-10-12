"""Generic WHOLE-parent optimized qnorm join; default root index200.

For the exact declared root parent and ALL FOUR CLOSED midpoint children,
compute every nonempty high Cantelli/SV route FIRST, before any cache/A1
arrays. The retained backend64MiB guard is not overridden; this wrapper
also checks observed peak<=64MiB before/after every high call. Empty
classes require exact rhoQ_min_square>=cap^2, valid INCLUDING equality
because actualrho<cap and eta>=0. Each nonempty high proof owns its exact
request/rho/SV/joint cut, with CLOSED all-eta-above-cut scope. At cut0 it
already covers eta0 and every actual eta>=0, so low is skipped.

After ALL5 high records, build ONE DIRECT fresh immutable quadrature
cache. First compute the ENTIRE parent low V5 proof on its OWN [0,cut],
fixed16 closed eta cells/allH/both reflections/tails. If the parent is
complete, this is a legitimate direct closure alternative. If UNKNOWN,
check EVERY four child, using its OWN already-fresh high proof/cut and
complete V5 low proof unless empty/cut0. Never stop after a failed child.
The parent closes iff its direct join closes OR ALL FOUR child joins
close. Shared faces stay in both children. Child-cover score is MAX of
all complete child scores, with empty children0. Parent UNKNOWN data and
all failed child intervals remain. No point/partial-H/eta masking.

PUBLIC batch APIs (no serialized mathematical inputs)
-----------------------------------------------------
fresh_parent_and_child_requests(index=200) returns exact tuple5.
prepare_fresh_high_requests(requests,guard,budget=60) returns
 (tuple5((exact_request,high_math_orNone)), tuple resource records).
prepare_fresh_parent_high(index,guard,budget=60) is a convenience call.
compute_fresh_parent_join(index=200,cache=None,preverified_high=None,
 guard=None,budget=60,time_limit_seconds=240) returns the complete record.
Optional cache and exact5 high pairs have explicit caller mathematical
prerequisites: DIRECT fresh audited builders on SAME requests/grid. Type,
schema/status/hash/JSON cannot prove them. A later full batch must finish
ALL high preparation BEFORE ANY A1 arrays; then supply those proof pairs
and ONE shared fresh cache. No old producer/global monkeypatch is used.

Compaction occurs ONLY after the full DIRECT V5 consumer has checked all
16 cells/allH/reflections/tails. It retains every eta scope, polynomial,
failed index, worst THREE complete route proofs, reserve and score. Large
A1/RAW/radius diagnostics are not numerical premises in a later replay;
replay rebuilds the entire direct arithmetic before this same projection.
No saved numerical receipts participate as mathematical inputs.

Conditional scope is the existing physical root: arbitrary standardized
iid actual P in declared w/beta rectangle, support17/4,eta>=0,actualrho
<46/25; retained CLOSED-CDF Prawitz/original-P bridge and external SV.
First-critical C3/attainment/support placement remains external. This
ONE parent never proves entire-root/unrestricted C4. Fresh T<CE checked.
Original H reserve retained, no optional refined H/eta ceiling added.

Single sequential<=240s/128MiB, each producer<=60s; strict high64MiB.
No incomplete-prefix receipt on exceptions/time expiry. New exclusive
scope-specific<=12MiB receipt or read-only ALL nonresource comparison.
Default tiny tests are PURE geometry/scope only, no CDF/cache producer.
Every older source/receipt remains unchanged; source pins integrity only.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_fresh_modulus_radius_whole_geometry_join_pilot_v4_2026_10_09 as geometry
import n4_fresh_signed_A1_CDF_cell_consumer_v5_2026_10_09 as consumer

full, A1, gamma_compiler = geometry.full, geometry.A1, geometry.gamma_compiler
resources, quadrature, root = full.resources, full.quadrature, full.root
require, SCALE, TARGET = consumer.require, consumer.SCALE, consumer.TARGET
INDEX, N, H_STEP, ETA_CELLS = 200, 256, F(1, 8), 16
TIME_LIMIT, CHILD_LIMIT = 240, 60
MEMORY_LIMIT, HIGH_MEMORY_LIMIT, OUTPUT_LIMIT = 128 * 1024 * 1024, 64 * 1024 * 1024, 12 * 1024 * 1024
GEOMETRY_PIN = "961b912466f793c72d6093e7183c57655f2bf92eb33aa925e17e1380aa537bb8"
CONSUMER_PIN = "66baf7865c7f70f27284358a0c6479a290ec4df2fd0605662fb636a512e082b2"


def source_drift_check():
    geometry.source_drift_check()
    consumer.source_drift_check()
    for module, pin in ((geometry, GEOMETRY_PIN), (consumer, CONSUMER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen DIRECT math-source integrity only")
    require(SCALE == full.SCALE and TARGET == full.TARGET, "SAME physical root/target units")


def dependency_pins():
    pins = geometry.dependency_pins()
    for name, pin in consumer.dependency_pins().items():
        require(name not in pins or pins[name] == pin, "Consistent complete math-source closure")
        pins[name] = pin
    path = Path(__file__)
    require(path.name not in pins, "Unique new parent coordinator")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def fresh_parent_and_child_requests(index=INDEX):
    require(type(index) is int and 0 <= index < 260, "Exact single root-parent index0..259")
    requests = tuple(geometry.fresh_whole_request(index, child) for child in (-1, 0, 1, 2, 3))
    require(tuple(request["geometry_path"] for request in requests) == ((), (0,), (1,), (2,), (3,))
            and tuple(request["closed_rectangle"] for request in requests[1:])
                == full.closed_four_children(requests[0]["closed_rectangle"]), "EXHAUSTIVE four CLOSED children")
    return requests


def _remaining_budget(budget):
    return full._remaining_child_budget(budget)


def _checked_high_pair(request, high):
    """Scope arithmetic AFTER DIRECT proof; not a status/JSON importer."""
    canonical = full.fresh_rectangle_request(request["closed_rectangle"], request["grid_index"],
                                             request["geometry_path"])
    require(request == canonical, "Exact request rederived, not stale geometry labels")
    if request["proved_root_empty"]:
        require(high is None, "Exact empty class must not be relabeled as a numerical high proof")
        return None
    require(type(high) is dict, "Every NONEMPTY class requires its OWN DIRECT complete high proof")
    cut, score = high["joint_eta_cut_exact"], high["joint_high_eta_score_at_closed_cut_exact"]
    require(type(cut) is type(score) is F and 0 <= cut < request["actual_eta_capacity_outer_open"]
            and 0 <= score <= TARGET and high["closed_low_eta_interval_still_to_prove"] == (F(0), cut)
            and high["SV_eta_cut_exact_unchanged"] == request["etaSV_exact"]
            and high["fresh_frontier_math"]["rhoQ_box_lower_exact"] == request["rhoQ_lower_exact"],
            "OWN CLOSED joint cut/rho/SV/complete high bound, including cut0/eta0")
    return high


def prepare_fresh_high_requests(requests, guard, budget=CHILD_LIMIT):
    """ALL exact parent+4 HIGH FIRST; actual backend64MiB never overridden."""
    require(callable(guard) and type(requests) in (tuple, list) and len(requests) == 5,
            "Caller guard and all5 exact ordered requests")
    require(tuple(requests) == fresh_parent_and_child_requests(requests[0]["grid_index"]),
            "Parent and ALL4 complete closed children, no prefix/selected class")
    source_drift_check()
    pairs, resource_records = [], []
    for request in requests:
        guard()
        peak = resources.peak_bytes()
        require(peak is not None and peak <= HIGH_MEMORY_LIMIT, "ALL high preparation BEFORE A1/strict64MiB")
        if request["proved_root_empty"]:
            high = None
        else:
            fresh = full.split.fresh_joint_cut_for_request(request, time_limit_seconds=_remaining_budget(budget))
            resource_records.append(fresh["resources"])
            high = {key: value for key, value in fresh.items() if key != "resources"}
        _checked_high_pair(request, high)
        pairs.append((request, high))
        guard()
        peak = resources.peak_bytes()
        require(peak is not None and peak <= HIGH_MEMORY_LIMIT, "High backend original64MiB still respected")
    require(len(pairs) == 5, "ALL5 high requests completed, no early result")
    source_drift_check()
    return tuple(pairs), tuple(resource_records)


def prepare_fresh_parent_high(index, guard, budget=CHILD_LIMIT):
    return prepare_fresh_high_requests(fresh_parent_and_child_requests(index), guard, budget)


def _checked_direct_pairs(requests, pairs):
    require(type(pairs) in (tuple, list) and len(pairs) == 5, "Exactly5 DIRECT same-request high pairs")
    for request, pair in zip(requests, pairs):
        require(type(pair) in (tuple, list) and len(pair) == 2 and pair[0] == request,
                "Exact parent/child request ORDER and own high arithmetic")
        _checked_high_pair(request, pair[1])
    return tuple(tuple(pair) for pair in pairs)


def compact_complete_low_result(low):
    """AFTER DIRECT full V5 checks only; every closed cell/proof kept."""
    cells = low["cells"]
    interval = low["closed_eta_cover"]
    require(len(cells) == ETA_CELLS and tuple((cell["lower"], cell["upper"]) for cell in cells)
            == consumer.fixed_eta_cells(interval), "ALL16 closed eta intervals including both faces")
    require(tuple(i for i, cell in enumerate(cells) if not cell["passed"])
            == tuple(low["unresolved_eta_cell_indices"]), "Every UNKNOWN cell remains")
    require(low["summary"]["ALL_H_reflection_rows_per_cell"] == 116
            and all(cell["H_reflection_rows_checked"] == 116 for cell in cells), "ALL58 H and BOTH true reflections")
    keys = ("status", "scale", "target", "N", "H_step", "closed_rectangle", "closed_eta_cover", "cells",
            "modulus_radius_mode", "use_two_disk", "unresolved_eta_cell_indices", "summary", "reserves_once",
            "actual_law_tail_score_upper", "fresh_target_certificate", "physical_premises", "freshness_premises", "conclusions")
    return {key: low[key] for key in keys}


def _complete_join_from_pair(pair, cache, guard, budget):
    request, high = pair
    guard()
    _checked_high_pair(request, high)
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
    low_started = time.monotonic()
    low_limit = _remaining_budget(budget)

    def low_guard():
        require(time.monotonic() - low_started < low_limit, "COMPLETE A1+Gamma+V5 low route<=60s")
        guard()

    def low_remaining():
        value = min(_remaining_budget(budget), low_limit - (time.monotonic() - low_started))
        require(value > 0, "No partial low route after its local budget expires")
        return value

    eta_interval = F(0), cut
    table = A1.fresh_generic_common_A1_response_table(request["closed_rectangle"], cache, low_guard)
    eta_cells = consumer.fixed_eta_cells(eta_interval)
    gamma = gamma_compiler.compute_verified_gamma_models(table, eta_cells, low_guard)
    low_guard()
    low = consumer.evaluate_fresh_signed_A1_CDF(table, gamma, eta_interval,
        rectangle=request["closed_rectangle"], N=N, H_step=H_STEP, use_two_disk=True,
        modulus_radius_mode="five_budget", time_limit_seconds=low_remaining())
    require(low["closed_rectangle"] == request["closed_rectangle"] and low["closed_eta_cover"] == eta_interval,
            "SAME entire request and OWN complete low eta interval")
    joined = geometry.previous.previous.exact_complete_join_summary(high, low, cut)
    closed = joined["conditional_entire_declared_child_all_actual_eta_closed"]
    summary = {key: value for key, value in joined.items() if key not in (
        "conditional_entire_declared_child_all_actual_eta_closed",
        "whole_parent_200_or_full_root_or_unrestricted_C4_proved")}
    summary["conditional_entire_declared_geometry_all_actual_eta_closed"] = closed
    summary["entire_260_root_or_unrestricted_C4_proved"] = False
    record = {"request": request, "kind": "COMPLETE_OWN_LOW_HIGH_JOIN" if closed else "UNKNOWN_LOW_CELLS_RETAINED",
        "whole_geometry_all_actual_eta_closed": closed,
        "whole_geometry_score_upper_exact": joined["whole_geometry_score_upper_exact"],
        "own_joint_eta_cut_exact": cut, "complete_low_high_join_summary": summary,
        "fresh_complete_low_eta_result": compact_complete_low_result(low)}
    resource = {"complete_A1_Gamma_V5_low_elapsed_seconds_diagnostic": time.monotonic() - low_started,
                "time_limit_seconds": low_limit, "V5_postconsumer": low["resources"]}
    low_guard()
    del table, gamma, low
    guard()
    return record, resource


def compute_fresh_parent_join(index=INDEX, cache=None, preverified_high=None, guard=None,
                              budget=CHILD_LIMIT, time_limit_seconds=TIME_LIMIT):
    """One WHOLE parent; optional cache/high MUST be DIRECT fresh math outputs."""
    started = time.monotonic()
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT
            and (guard is None or callable(guard)), "Cooperative parent240s and optional external guard")
    source_drift_check()
    initial_pins = dependency_pins()

    def parent_guard():
        require(time.monotonic() - started < time_limit_seconds, "No truncated parent/child receipt")
        peak = resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Observed parent128MiB")
        if guard is not None:
            guard()

    def remaining():
        return min(_remaining_budget(budget), time_limit_seconds - (time.monotonic() - started))

    parent_guard()
    requests = fresh_parent_and_child_requests(index)
    high_supplied = preverified_high is not None
    if not high_supplied:
        pairs, high_resources = prepare_fresh_high_requests(requests, parent_guard, remaining)
    else:
        # This branch requires the explicit caller DIRECT all-HIGH-first
        # mathematical prerequisite, not schema/serialized proof truth.
        pairs, high_resources = _checked_direct_pairs(requests, preverified_high), ()
    cache_built = cache is None
    if cache is None:
        cache = quadrature.build_fresh_quadrature_cache(N, H_STEP, time_limit_seconds=_remaining_budget(remaining))
    quadrature.validate_preverified_fresh_cache(cache, N, H_STEP)
    certificate = consumer.core.cached.previous.fresh_target_certificate(cache.pi_bracket, cache.phi0_bracket)
    require(certificate["target"] == TARGET and certificate["CE_lower_exact"] > TARGET, "DIRECT fresh T<CE")
    parent, first_resource = _complete_join_from_pair(pairs[0], cache, parent_guard, remaining)
    low_resources = [] if first_resource is None else [first_resource]
    children = []
    if not parent["whole_geometry_all_actual_eta_closed"]:
        for pair in pairs[1:]:
            child, resource = _complete_join_from_pair(pair, cache, parent_guard, remaining)
            children.append(child)
            if resource is not None:
                low_resources.append(resource)
        require(len(children) == 4 and tuple(child["request"] for child in children) == requests[1:],
                "ALL FOUR complete CLOSED children, even if earlier child UNKNOWN")
    direct = parent["whole_geometry_all_actual_eta_closed"]
    by_children = bool(children) and all(child["whole_geometry_all_actual_eta_closed"] for child in children)
    closed = direct or by_children
    upper = parent["whole_geometry_score_upper_exact"] if direct else max(
        child["whole_geometry_score_upper_exact"] for child in children)
    require(type(closed) is bool and (not closed or upper <= TARGET), "WHOLE parent iff DIRECT or ALL4 closed")
    source_drift_check()
    final_pins = dependency_pins()
    require(final_pins == initial_pins, "ALL source dependencies unchanged through complete parent")
    parent_guard()
    return {"status": "EXACT_CONDITIONAL_WHOLE_PARENT_COMPLETE_ETA_COVER" if closed
            else "UNKNOWN_WITH_PARENT_AND_ALL_FOUR_CLOSED_CHILDREN_RETAINED",
        "root_index": index, "target": TARGET, "whole_parent_request": requests[0],
        "fresh_target_certificate": certificate, "all_five_exact_requests": requests,
        "all_five_DIRECT_high_pairs": pairs, "initial_parent_complete_join": parent,
        "all_four_complete_child_joins_if_parent_UNKNOWN": tuple(children),
        "summary": {"whole_parent_all_actual_eta_closed": closed, "whole_parent_score_upper_exact": upper,
            "closed_by_DIRECT_parent": direct, "closed_by_ALL_four_children": by_children,
            "all_five_high_requests_accounted": 5, "four_child_joins_attempted": len(children),
            "unresolved_child_indices": tuple(i for i, child in enumerate(children)
                if not child["whole_geometry_all_actual_eta_closed"]),
            "low_V5_producer_calls_here": len(low_resources),
            "high_producer_calls_here": 0 if high_supplied else sum(not r["proved_root_empty"] for r in requests)},
        "fresh_cache_metadata": cache.compact_metadata(),
        "standing_mathematical_premises": "DIRECT all5 own-request high proofs BEFORE any A1; DIRECT ONEfreshcache and correct A1/Gamma/V5 complete low proofs. Standardized iid actual P in declaredROOTbox,eta>=0,|X|<=17/4,actualrho<46/25; retained Prawitz/original-P bridge, external SV and first-critical placement for all-law use. No original finite-atom/density/extraM4 axiom; schema/status/hash/JSON is not analytic provenance.",
        "conclusions": {"conditional_entire_declared_parent_all_actual_eta_closed": closed,
            "entire_260_root_or_unrestricted_C4_proved": False,
            "ALL_four_children_checked_if_parent_UNKNOWN": True,
            "closed_shared_faces_own_cuts_and_eta0_kept": True,
            "eta_ceiling_or_optional_refined_H_added": False,
            "old_producers_called_globals_patched_or_old_receipts_modified": False},
        "source_pins_integrity_only": final_pins,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "strict_HIGH_phase_memory_limit_bytes": HIGH_MEMORY_LIMIT,
            "child_time_limit_seconds": CHILD_LIMIT, "high_resources": high_resources, "low_resources": low_resources,
            "DIRECT_high_pairs_supplied_by_caller": high_supplied, "fresh_cache_built_here": cache_built}}


def self_tests():
    """Dormant PURE root/scope/high-cut shape checks; no CDF/cache producer."""
    source_drift_check()
    requests = fresh_parent_and_child_requests()
    require(len(requests) == 5 and requests[0]["geometry_path"] == ()
            and tuple(r["geometry_path"] for r in requests[1:]) == ((0,), (1,), (2,), (3,)), "Exact ordered parent+4 paths")
    require(tuple(r["closed_rectangle"] for r in requests[1:]) == full.closed_four_children(requests[0]["closed_rectangle"]),
            "Complete closed four-child geometry cover")
    wl = full.ROOT[0]
    empty = full.fresh_rectangle_request((wl, wl, F(0), F(0)), 0, ())
    require(empty["rhoQ_min_square_exact"] == full.RHO_CAP ** 2 and empty["proved_root_empty"]
            and _checked_high_pair(empty, None) is None, "STRICTcap excludes equality, no invented high proof")
    rejected = False
    try:
        _checked_high_pair(requests[0], None)
    except RuntimeError:
        rejected = True
    require(rejected, "NONEMPTY requires OWN DIRECT high, no omitted eta interval")
    cut, _, score = full.split.select_complete_cut(F(1, 10), TARGET - F(1, 100), F(0), TARGET)
    require(cut == 0 and score <= TARGET, "Closedcut0 high coverseta0 and needs no low")
    return {"status": "TINY_GENERIC_PARENT_HIGH_FIRST_GEOMETRY_ONLY", "exact_checks": 5,
        "CF_cache_Cantelli_A1_Gamma_radius_CDF_or_parent_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--produce", action="store_true")
    modes.add_argument("--replay-existing", action="store_true")
    parser.add_argument("--index", type=int, default=INDEX)
    args = parser.parse_args()
    fresh_parent_and_child_requests(args.index)
    if not (args.produce or args.replay_existing):
        print(json.dumps(self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem + "_I" + str(args.index) + "_N256_H1_8_ETA16_five_budget.json")
    require(args.replay_existing or not output.exists(), "Never overwrite a scope-specific receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay requires complete result")
    result = compute_fresh_parent_join(args.index, time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Complete compact parent result<=12MiB")
    peak = resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Complete serialization within240s/128MiB BEFORE receipt write")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only complete receipt")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        require({k: v for k, v in saved.items() if k != "resources"}
                == {k: v for k, v in fresh.items() if k != "resources"}, "ALL nonresource fields match DIRECT full replay")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    peak = resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT, "EntireCLIincludingreplaybounded")
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "resources": result["resources"]}, sort_keys=True, default=root.json_ready))


if __name__ == "__main__":
    main()
