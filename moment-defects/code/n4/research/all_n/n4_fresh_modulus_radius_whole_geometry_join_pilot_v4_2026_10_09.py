"""NEW DIRECT fresh V4 whole-geometry/ALL-eta join, not full-root theorem.

Default domain is ENTIRE closed root200/child3. Other explicitly selected
whole root classes or their fixed closed children are also supported,
never sampled points. DIRECT high-FIRST Cantelli/SV, fresh quadrature,
correct A1V2, exact original Gamma, and fresh modulus-aware V4 prove
the SAME complete closed low/high eta cover. No saved numeric inputs,
eta-ceiling mask, dropped face or high backend64MiB override.

Optional in-memory cache or (exact_request, high_route) pairs have an explicit caller
mathematical premise: DIRECT fresh audited builders on SAME request and
grid. Their labels/status/hash/schema alone do NOT establish bounds.
This permits a later coordinated full-root two-phase computation to
finish ALL strict64MiB high backends before larger A1 arrays exist.
The pilot CLI always builds both directly itself, no import paths/JSON.

One externally coordinated sequential60s/128MiB stdlib job, exclusive
new <=8MiB projected receipt; read-only replay rebuilds all math and
compares ALL nonresource fields. ALL q256/H58/both reflections/eta16/
273tag limits/tails/source closure retained. Original P not finite-atom;
support/rho/Prawitz/first-critical inputs explicit. No entire-root/C4
claim from one class. Older sources/receipts untouched. Default tiny
scope tests only, no computation on import.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_fresh_signed_ABS_local_quad_whole_child_200_3_join_pilot_v3_2026_10_09 as previous
import n4_fresh_signed_A1_CDF_cell_consumer_v4_2026_10_09 as consumer

full, A1, scope, gamma_compiler = previous.full, previous.A1, previous.scope, previous.gamma_compiler
require, SCALE, TARGET = consumer.require, consumer.SCALE, consumer.TARGET
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 128 * 1024 * 1024, 8 * 1024 * 1024
PREVIOUS_PIN = "b3344e9fcc4c1689b797fa82e717f094d6197ef7fd0255559154a865103ce4e9"
CONSUMER_PIN = "684568bb773216737fc0a9b158475e8d0e6ea11183d859ab22f56dae9dae138d"


def source_drift_check():
    previous.source_drift_check()
    consumer.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (consumer, CONSUMER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen complete-domain modulus math integrity only")


def dependency_pins():
    pins = previous.dependency_pins()
    for name, pin in consumer.dependency_pins().items():
        require(name not in pins or pins[name] == pin, "Consistent entire math-source closure")
        pins[name] = pin
    path = Path(__file__)
    require(path.name not in pins, "Unique generic V4 join source")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def fresh_whole_request(index=200, child=3):
    require(type(index) is int and 0 <= index < 260 and type(child) is int and -1 <= child <= 3,
            "Exact whole-root class and optional fixed closed child; -1 means ENTIRE parent")
    parent = full.root.fresh_root_requests()[2][index]
    rectangle = parent["closed_rectangle"] if child == -1 else full.closed_four_children(
        parent["closed_rectangle"])[child]
    return full.fresh_rectangle_request(rectangle, index, () if child == -1 else (child,))


def compute_fresh_join(index=200, child=3, mode="response_norm", cache=None,
                       preverified_high=None, time_limit_seconds=TIME_LIMIT):
    """Complete DIRECT join; supplied high/cache require DIRECT caller proofs."""
    started = time.monotonic()
    require(type(mode) is str and mode in ("response_norm", "five_budget")
            and type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Explicit modulus mode/cooperative whole-join timer")
    source_drift_check()
    initial = dependency_pins()

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Whole fresh-radius geometry join timer")
        peak = full.resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Observed whole-join128MiB")

    guard()
    request = fresh_whole_request(index, child)
    require(not request["proved_root_empty"], "This pilot API declares NONEMPTY whole geometry only")
    if preverified_high is None:
        high = full.split.fresh_joint_cut_for_request(request,
            time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    else:
        require(type(preverified_high) in (tuple, list) and len(preverified_high) == 2
                and preverified_high[0] == request,
                "Explicit SAME exact request paired with DIRECT preverified high arithmetic")
        high = preverified_high[1]
    # A provided high object's mathematical truth comes ONLY from the
    # stated DIRECT builder premise. Recheck exact request identities.
    require(high["fresh_frontier_math"]["rhoQ_box_lower_exact"] == request["rhoQ_lower_exact"]
            and high["SV_eta_cut_exact_unchanged"] == request["etaSV_exact"],
            "SAME exact request normalization/SV labels for complete high route")
    guard()
    cut = high["joint_eta_cut_exact"]
    require(type(cut) is F and 0 < cut < request["actual_eta_capacity_outer_open"],
            "Declared pilot has positive complete low scope; eta0 cannot disappear")
    eta_interval = F(0), cut
    eta_cells = consumer.fixed_eta_cells(eta_interval)
    built_cache = cache is None
    if cache is None:
        cache = full.quadrature.build_fresh_quadrature_cache()
    full.quadrature.validate_preverified_fresh_cache(cache, 256, F(1, 8))
    table = A1.fresh_generic_common_A1_response_table(request["closed_rectangle"], cache, guard)
    gamma_table = gamma_compiler.compute_verified_gamma_models(table, eta_cells, guard)
    guard()
    low = consumer.evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval,
        rectangle=request["closed_rectangle"], N=256, H_step=F(1, 8), use_two_disk=True,
        modulus_radius_mode=mode, time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    guard()
    require(low["closed_rectangle"] == request["closed_rectangle"]
            and tuple(gamma_table["eta_cells"]) == eta_cells
            and tuple(table["box_geometry"]["rectangle"]) == request["closed_rectangle"],
            "SAME entire geometry/eta for A1/Gamma/refined-radius CDF")
    joined = previous.previous.exact_complete_join_summary(high, low, cut)
    closed = joined["conditional_entire_declared_child_all_actual_eta_closed"]
    # Relabel only scope metadata; that pure join covers any declared
    # geometry and does not infer an undeclared parent from one child.
    summary = {k: v for k, v in joined.items() if k not in (
        "conditional_entire_declared_child_all_actual_eta_closed",
        "whole_parent_200_or_full_root_or_unrestricted_C4_proved")}
    summary["conditional_entire_declared_geometry_all_actual_eta_closed"] = closed
    summary["entire_260_root_or_unrestricted_C4_proved"] = False
    raw_digest = scope.RAW_cache_digest(table["nom_mod_cache"], guard)
    projection = {key: table[key] for key in
                  ("scale", "N", "box_geometry", "nominal_root_data", "rows", "frequency_data", "metadata")}
    source_drift_check()
    final = dependency_pins()
    require(final == initial, "ALL mathematical sources unchanged through complete modulus join")
    guard()
    return {"status": "FRESH_ENTIRE_GEOMETRY_MODULUS_RADIUS_ALL_ETA_CLOSED" if closed
            else "UNKNOWN_WITH_ALL_COMPLETE_MODULUS_SIGNED_ABS_CELLS_AND_HIGH_ROUTE",
        "root_class": index, "fixed_geometry_path": request["geometry_path"],
        "declared_ENTIRE_parent_not_child": child == -1, "modulus_radius_mode": mode,
        "target": TARGET, "fresh_request": request, "summary": summary,
        "fresh_complete_high_eta_route": {k: v for k, v in high.items() if k != "resources"},
        "fresh_complete_low_eta_result": {k: v for k, v in low.items() if k != "resources"},
        "fresh_A1_table_projection": projection, "fresh_Gamma_table": gamma_table,
        "auxiliary_RAW_cache_sha256_integrity_only": raw_digest,
        "conclusions": {"conditional_entire_declared_geometry_all_actual_eta_closed": closed,
            "entire_260_root_or_unrestricted_C4_proved": False,
            "eta_ceiling_mask_added": False, "ABS_portfolio_and_fresh_modulus_radius_added": True,
            "saved_numeric_JSON_or_float_proof_inputs": False,
            "previous_producer_called_or_globals_changed": False,
            "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": full.resources.peak_bytes(),
            "time_limit_seconds": time_limit_seconds, "memory_limit_bytes": MEMORY_LIMIT,
            "one_sequential_producer": True, "fresh_cache_built_here": built_cache,
            "high_frontier_preverified_from_DIRECT_caller": preverified_high is not None,
            "high_route_resources": high.get("resources"), "low_consumer_resources": low["resources"]}}


def self_tests():
    """Exact geometry/scope only; no cache/CF/high/Gamma/CDF producer."""
    source_drift_check()
    parent = fresh_whole_request(200, -1)
    children = tuple(fresh_whole_request(200, child) for child in range(4))
    require(tuple(child["closed_rectangle"] for child in children)
                == full.closed_four_children(parent["closed_rectangle"]), "ALL4 closed children cover SAME parent")
    require(children[3]["closed_rectangle"] == scope.fresh_entire_request()["closed_rectangle"],
            "Default scope exactly preserved from independently replayed200/3")
    require(parent["geometry_path"] == () and all(c["geometry_path"] == (i,) for i, c in enumerate(children)),
            "ENTIRE parent and ENTIRE children have distinct explicit labels")
    return {"status": "TINY_FRESH_MODULUS_JOIN_WHOLE_GEOMETRY_SCOPE_ONLY", "exact_checks": 3,
        "CF_cache_A1_Gamma_CDF_high_route_or_root_producer_called": False}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--produce", action="store_true")
    modes.add_argument("--replay-existing", action="store_true")
    parser.add_argument("--index", type=int, default=200)
    parser.add_argument("--child", type=int, default=3)
    parser.add_argument("--mode", choices=("response_norm", "five_budget"), default="response_norm")
    args = parser.parse_args()
    if not (args.produce or args.replay_existing):
        print(json.dumps(self_tests(), sort_keys=True))
        return
    # Exact CLI scope validation precedes a filename or producer choice.
    fresh_whole_request(args.index, args.child)
    label = "parent" if args.child == -1 else "child" + str(args.child)
    output = Path(__file__).with_name(Path(__file__).stem + "_I" + str(args.index) + "_" + label + "_" + args.mode + ".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a scope-specific receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay needs existing result")
    result = compute_fresh_join(args.index, args.child, args.mode)
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False,
                     default=full.root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Complete projected geometry result<=8MiB")
    peak = full.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Entire serialization within60s/128MiB BEFORE receipt write")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only receipt")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        require({k: v for k, v in saved.items() if k != "resources"}
                == {k: v for k, v in fresh.items() if k != "resources"},
                "ALL projected nonresource fields match DIRECT whole-geometry replay")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    peak = full.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Complete CLI including replay within60s/128MiB")
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "scope": {"index": args.index, "child": args.child, "mode": args.mode},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": peak, "memory_limit_bytes": MEMORY_LIMIT}},
        sort_keys=True, default=full.root.json_ready))


if __name__ == "__main__":
    main()
