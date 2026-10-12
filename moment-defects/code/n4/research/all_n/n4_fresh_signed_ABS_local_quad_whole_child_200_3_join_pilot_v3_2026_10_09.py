"""NEW whole-child200/3 pilot, COMPLETE signed/ABS portfolio consumerV3.

Same DIRECT high-FIRST/quad/A1/Gamma pipeline and entire closed child
as the frozen3df pilot. The ONLY changed mathematical stage is audited
V3: at each H/cell it independently proves signed and COMPLETE ABS
uniform bounds and chooses ONE whole bound before max-H. No coefficient
or eta-endpoint minima. No eta-feasibility mask/new radius is used yet.

Every q/H/orientation/closed eta face, actual-law tail, physical reserve
and first-critical input remains. All UNKNOWN cells remain in the result.
The pure3df complete-low/high join is reused, never its producer or globals.
No saved numerical proof input; exclusive <=6MiB new projected result,
read-only fresh rebuild/all nonresource compare;60s/128MiB stdlib. The
high backend's stricter64MiB runs FIRST and is not overridden. No whole
parent/root/unrestricted C4 conclusion from this one declared child.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_fresh_signed_A1_local_quad_whole_child_200_3_join_pilot_2026_10_09 as previous
import n4_fresh_signed_A1_CDF_cell_consumer_v3_2026_10_09 as consumer

full, A1, scope, gamma_compiler = previous.full, previous.A1, previous.scope, previous.gamma_compiler
require, SCALE, TARGET = consumer.require, consumer.SCALE, consumer.TARGET
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 128 * 1024 * 1024, 6 * 1024 * 1024
PREVIOUS_PIN = "3df038e7278b9e30b0141776ab6befaee985f087eec3d43d051b8a0fec5888ea"
CONSUMER_PIN = "82c98f8059f3ebe19168fe15f2b35123993a136e64d99d238bebd0fc63264b40"


def source_drift_check():
    previous.source_drift_check()
    consumer.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (consumer, CONSUMER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen complete-route math integrity, not a proof by hash")


def dependency_pins():
    pins = previous.dependency_pins()
    for name, pin in consumer.dependency_pins().items():
        require(name not in pins or pins[name] == pin, "Consistent same-name source identities")
        pins[name] = pin
    path = Path(__file__)
    require(path.name not in pins, "Unique new portfolio pilot source")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def compute_fresh_pilot():
    started = time.monotonic()
    source_drift_check()
    initial = dependency_pins()

    def guard():
        require(time.monotonic() - started < TIME_LIMIT, "Entire portfolio child pilot60s")
        peak = full.resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Observed portfolio child128MiB")

    guard()
    request = scope.fresh_entire_request()
    high = full.split.fresh_joint_cut_for_request(request,
        time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    guard()
    cut = high["joint_eta_cut_exact"]
    require(type(cut) is F and 0 < cut < request["actual_eta_capacity_outer_open"],
            "Whole hard child's positive complete low-eta scope")
    eta_interval = F(0), cut
    eta_cells = consumer.fixed_eta_cells(eta_interval)
    cache = full.quadrature.build_fresh_quadrature_cache()
    table = A1.fresh_generic_common_A1_response_table(request["closed_rectangle"], cache, guard)
    gamma_table = gamma_compiler.compute_verified_gamma_models(table, eta_cells, guard)
    guard()
    low = consumer.evaluate_fresh_signed_A1_CDF(table, gamma_table, eta_interval,
        rectangle=request["closed_rectangle"], N=256, H_step=F(1, 8), use_two_disk=True,
        time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    guard()
    require(low["closed_rectangle"] == request["closed_rectangle"]
            and tuple(gamma_table["eta_cells"]) == eta_cells
            and tuple(table["box_geometry"]["rectangle"]) == request["closed_rectangle"],
            "DIRECT A1/Gamma/portfolio all cover SAME entire child and eta")
    summary = previous.exact_complete_join_summary(high, low, cut)
    raw_digest = scope.RAW_cache_digest(table["nom_mod_cache"], guard)
    projection = {key: table[key] for key in
                  ("scale", "N", "box_geometry", "nominal_root_data", "rows", "frequency_data", "metadata")}
    source_drift_check()
    final = dependency_pins()
    require(final == initial, "All mathematical sources unchanged through full portfolio pilot")
    guard()
    closed = summary["conditional_entire_declared_child_all_actual_eta_closed"]
    return {"status": "FRESH_ENTIRE_CHILD_SIGNED_OR_ABS_ALL_ETA_CLOSED" if closed
            else "UNKNOWN_WITH_COMPLETE_SIGNED_AND_ABS_LOW_CELLS_AND_HIGH_ROUTE",
        "root_class": scope.INDEX, "fixed_geometry_path": (scope.CHILD,),
        "target": TARGET, "fresh_request": request, "summary": summary,
        "fresh_complete_high_eta_route": {k: v for k, v in high.items() if k != "resources"},
        "fresh_complete_low_eta_result": {k: v for k, v in low.items() if k != "resources"},
        "fresh_A1_table_projection": projection, "fresh_Gamma_table": gamma_table,
        "auxiliary_RAW_cache_sha256_integrity_only": raw_digest,
        "conclusions": {"conditional_entire_declared_child_all_actual_eta_closed": closed,
            "whole_parent_or_entire_260_root_or_unrestricted_C4_proved": False,
            "ABS_portfolio_added": True, "eta_ceiling_mask_or_new_radius_added": False,
            "saved_numeric_JSON_or_float_proof_inputs": False,
            "previous_producer_called_or_globals_changed": False,
            "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": full.resources.peak_bytes(),
            "time_limit_seconds": TIME_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "one_sequential_producer": True, "standard_library_only": True,
            "high_route_resources": high["resources"], "low_consumer_resources": low["resources"]}}


def self_tests():
    """Scope and source identity only; no cache/CF/Gamma/CDF producers."""
    source_drift_check()
    old = previous.self_tests()
    require(old["exact_checks"] == 3, "Unchanged closed-child/source scope tests")
    pins = dependency_pins()
    require(pins[Path(consumer.__file__).name] == CONSUMER_PIN, "New WHOLE-route portfolio source")
    return {"status": "TINY_COMPLETE_PORTFOLIO_JOIN_SCOPE_ONLY", "exact_checks": 4,
        "CF_cache_A1_Gamma_CDF_high_route_or_root_producer_called": False}


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
    output = Path(__file__).with_suffix(".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay needs existing receipt")
    result = compute_fresh_pilot()
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False,
                     default=full.root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Projected COMPLETE child result<=6MiB")
    peak = full.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Whole serialization bounded BEFORE receipt write")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only result")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        require({k: v for k, v in saved.items() if k != "resources"}
                == {k: v for k, v in fresh.items() if k != "resources"},
                "ALL projected nonresource fields match DIRECT complete-route replay")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    peak = full.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Full CLI including replay within60s/128MiB")
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": peak, "memory_limit_bytes": MEMORY_LIMIT}},
        sort_keys=True, default=full.root.json_ready))


if __name__ == "__main__":
    main()
