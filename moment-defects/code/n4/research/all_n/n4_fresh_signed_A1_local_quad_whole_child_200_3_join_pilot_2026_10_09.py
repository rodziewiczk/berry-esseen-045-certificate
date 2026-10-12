"""NEW DIRECT-FRESH signed-A1/local-quad WHOLE closed child200/3 eta join.

First compute the complete fresh Cantelli/SV high-eta route and its
exact CLOSED cut from the generic whole-child request. The retained
backend's stricter64MiB guard is not overridden: it runs FIRST before
the large A1 table. Then DIRECT fresh quadrature, correct A1V2, exact
five-price Gamma on SAME16 closed [0,cut] cells, and local-quad signed
CDF consumerV2 compute the full low-eta bound. No numeric receipt is
imported as a mathematical premise. The original actual law need not
be finite-atom; support/rho/Prawitz/first-critical inputs are explicit.

Every q256/H58/BOTH reflection/273tag/eta face stays. Whole child is
closed only by the COMPLETE low result AND complete high result, not
a prefix/point/isolated response. All UNKNOWN cells are retained. No
eta-ceiling mask or ABS portfolio is applied here. No full260 root or
unrestricted C4 conclusion is asserted by this one-child pilot.

The exclusive new projected receipt keeps ALL A1/centre/frequency and
Gamma model data, full low result, full high arithmetic and source
closure. Only the large auxiliary RAW response cache is represented by
an integrity digest (never a numerical proof input). Read-only replay
directly rebuilds everything and compares ALL projected nonresource
fields. Floating clocks and memory counters are diagnostics only.
One externally coordinated sequential60s/128MiB stdlib job; <=6MiB
receipt. Default CLI tiny scope/interface tests ONLY. Old files stay.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_fresh_signed_A1_whole_child_200_3_pilot_2026_10_09 as scope
import n4_Q3_fresh_generic_A1_five_price_cell_suprema_2026_10_09 as gamma_compiler
import n4_fresh_signed_A1_CDF_cell_consumer_v2_2026_10_09 as consumer

full, A1 = scope.full, scope.A1
require, SCALE, TARGET = consumer.require, consumer.SCALE, consumer.TARGET
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 128 * 1024 * 1024, 6 * 1024 * 1024
SCOPE_PIN = "35b1a73113a6b9c62e6a8aa568be7517d887a3706b2f9afdac1649166834f470"
GAMMA_PIN = "f5dc893e0674255cc68981bdb61a2b0ce5586b8a2afbea14f7634cd85c0a5ad4"
CONSUMER_PIN = "95172909e96a55d4f074c1ffc704d0c2ee8810ca51e520b1f141752885bb915c"


def source_drift_check():
    scope.source_drift_check()
    gamma_compiler.source_drift_check()
    consumer.source_drift_check()
    for module, pin in ((scope, SCOPE_PIN), (gamma_compiler, GAMMA_PIN), (consumer, CONSUMER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen whole-domain mathematical sources, not truth from hashes")
    require(SCALE == full.SCALE == gamma_compiler.SCALE
            and TARGET == full.TARGET == gamma_compiler.TARGET,
            "SAME physical arithmetic units/target")


def dependency_pins():
    pins = scope.dependency_pins()
    for name, pin in consumer.dependency_pins().items():
        require(name not in pins or pins[name] == pin, "No contradictory same-name source identity")
        pins[name] = pin
    path = Path(__file__)
    require(path.name not in pins, "Unique new producer source")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def exact_complete_join_summary(high, low, cut):
    """Pure joining under the two DIRECT proved COMPLETE-route premises."""
    require(type(cut) is F and cut > 0 and high["joint_eta_cut_exact"] == cut
            and high["closed_low_eta_interval_still_to_prove"] == (F(0), cut)
            and low["closed_eta_cover"] == (F(0), cut), "Exact CLOSED shared eta face")
    high_upper, low_upper = high["joint_high_eta_score_at_closed_cut_exact"], low["summary"]["score_upper_exact"]
    require(type(high_upper) is type(low_upper) is F and high_upper <= TARGET
            and low["summary"]["fixed_closed_eta_cells"] == 16,
            "Complete fresh high route and fixed entire low-eta cover")
    L, U = low["closed_eta_cover"]
    cells = low["cells"]
    require(len(cells) == 16 and cells[0]["lower"] == L and cells[-1]["upper"] == U
            and all(left["upper"] == right["lower"] for left, right in zip(cells, cells[1:])),
            "ALL16 closed intervals and every shared face")
    passed = all(cell["passed"] for cell in cells)
    require(type(passed) is bool
            and low["conclusions"]["conditional_CDF_on_entire_declared_BOX_and_eta"] == passed
            and passed == (low_upper < TARGET), "Fresh COMPLETE low result agrees, not prefix acceptance")
    upper = max(high_upper, low_upper)
    require(not passed or upper <= TARGET, "Both whole-eta routes give<=T<CE")
    return {"conditional_entire_declared_child_all_actual_eta_closed": passed,
        "whole_geometry_score_upper_exact": upper,
        "low_eta_score_upper_exact": low_upper, "high_eta_score_upper_exact": high_upper,
        "closed_join_eta_exact": cut,
        "unresolved_low_eta_cell_indices": low["unresolved_eta_cell_indices"],
        "all_H_reflection_rows_per_low_eta_cell": low["summary"]["ALL_H_reflection_rows_per_cell"],
        "whole_parent_200_or_full_root_or_unrestricted_C4_proved": False}


def compute_fresh_pilot():
    started = time.monotonic()
    source_drift_check()
    initial = dependency_pins()

    def guard():
        require(time.monotonic() - started < TIME_LIMIT, "Whole signed child pilot60s")
        peak = full.resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Observed whole-child128MiB")

    guard()
    request = scope.fresh_entire_request()
    # The backend's stricter64MiB monitoring remains unchanged. No A1
    # arrays or saved high arithmetic exist before this DIRECT call.
    high = full.split.fresh_joint_cut_for_request(request,
        time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    guard()
    cut = high["joint_eta_cut_exact"]
    require(type(cut) is F and 0 < cut < request["actual_eta_capacity_outer_open"],
            "This declared hard child has a complete positive low scope, not an omitted eta0")
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
            "SAME entire child for fresh A1/Gamma/CDF, not four points")
    summary = exact_complete_join_summary(high, low, cut)
    raw_digest = scope.RAW_cache_digest(table["nom_mod_cache"], guard)
    projection = {key: table[key] for key in
                  ("scale", "N", "box_geometry", "nominal_root_data", "rows", "frequency_data", "metadata")}
    # ONLY nondeterministic resource records are separated. Every kept
    # mathematical field is directly recomputed in read-only replay.
    high_math = {key: value for key, value in high.items() if key != "resources"}
    low_math = {key: value for key, value in low.items() if key != "resources"}
    source_drift_check()
    final = dependency_pins()
    require(final == initial, "ALL mathematical dependencies unchanged through complete pilot")
    guard()
    closed = summary["conditional_entire_declared_child_all_actual_eta_closed"]
    return {"status": "FRESH_ENTIRE_CHILD_SIGNED_A1_LOCAL_QUAD_ALL_ETA_CLOSED" if closed
            else "UNKNOWN_WITH_ALL_LOW_ETA_CELLS_AND_COMPLETE_HIGH_ROUTE_RETAINED",
        "root_class": scope.INDEX, "fixed_geometry_path": (scope.CHILD,),
        "target": TARGET, "fresh_request": request, "summary": summary,
        "fresh_complete_high_eta_route": high_math, "fresh_complete_low_eta_result": low_math,
        "fresh_A1_table_projection": projection, "fresh_Gamma_table": gamma_table,
        "auxiliary_RAW_cache_sha256_integrity_only": raw_digest,
        "conclusions": {"conditional_entire_declared_child_all_actual_eta_closed": closed,
            "whole_parent_or_entire_260_root_or_unrestricted_C4_proved": False,
            "eta_ceiling_mask_or_ABS_portfolio_added": False,
            "saved_numeric_JSON_or_float_proof_inputs": False,
            "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": final,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": full.resources.peak_bytes(),
            "time_limit_seconds": TIME_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "one_sequential_producer": True, "standard_library_only": True,
            "high_route_resources": high["resources"], "low_consumer_resources": low["resources"]}}


def self_tests():
    """Tiny scope and fixed closed-cover ONLY, no real producer invoked."""
    source_drift_check()
    request = scope.fresh_entire_request()
    cut = F(1, 5)  # Synthetic test interval, not a claimed physical frontier.
    cells = consumer.fixed_eta_cells((F(0), cut))
    require(request["geometry_path"] == (3,) and not request["proved_root_empty"],
            "Whole child request, no point labels")
    require(len(cells) == 16 and cells[0][0] == 0 and cells[-1][1] == cut
            and all(left[1] == right[0] for left, right in zip(cells, cells[1:])),
            "All synthetic CLOSED faces including eta0/cut retained")
    require(dependency_pins()[Path(A1.previous.HG.__file__).name]
                == hashlib.sha256(Path(A1.previous.HG.__file__).read_bytes()).hexdigest(),
            "Legacy PURE HG source included in full integrity closure")
    return {"status": "TINY_WHOLE_CHILD_SIGNED_JOIN_SCOPE_ONLY", "exact_checks": 3,
        "CF_cache_A1_Gamma_CDF_high_route_or_root_producer_called": False,
        "source_or_receipt_files_written": False}


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
    require(args.replay_existing or not output.exists(), "Never overwrite any previous receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay requires existing receipt")
    result = compute_fresh_pilot()
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False,
                     default=full.root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Complete projected child result<=6MiB")
    peak = full.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Whole serialization bounded before any receipt write")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only receipt")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        require({k: v for k, v in saved.items() if k != "resources"}
                == {k: v for k, v in fresh.items() if k != "resources"},
                "ALL projected nonresource fields exactly match direct fresh replay")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    peak = full.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and peak is not None and peak <= MEMORY_LIMIT,
            "Whole CLI including serialization/replay within60s/128MiB")
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": peak, "memory_limit_bytes": MEMORY_LIMIT}},
        sort_keys=True, default=full.root.json_ready))


if __name__ == "__main__":
    main()
