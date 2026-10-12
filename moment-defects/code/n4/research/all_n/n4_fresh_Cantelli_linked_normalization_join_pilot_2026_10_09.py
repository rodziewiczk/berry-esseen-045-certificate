"""DIRECT fresh complete-eta joins on THREE whole previously hard classes.

Declared geometries are entire root classes149,208,247, not sampled
points or a global-root substitute. For each, fresh Cantelli/SV supplies
a COMPLETE high-eta route on [cut,infinity). DIRECT fresh linked-normalized
Prawitz supplies every fixed16 CLOSED low-eta cell on [0,cut]. Their
shared face belongs to BOTH; eta0 is never removed. UNKNOWN retains all
unclosed low cells. A zero high cut already covers eta0 without a low job.
Only when the fresh whole-low and whole-high proofs both hold is the
ENTIRE geometry/ALL actual eta class closed (under physical premises).

Mathematical scope: standardized iid actual P, canonical root geometry,
eta>=0, |X|<=17/4, actualrho=rhoQ+eta<46/25; retained closed-CDF Prawitz,
physical midpoint bridge and external SV. First-critical all-law use
still needs retained C3/attainment/contact inputs. NEVER global C4 here.
No saved numerical input, oldCF, coefficientwise mix or source edits.

ONE sequential180s/256MiB job, each producer<=60s; NEW exclusive<=2MiB
receipt/read-only replay all nonresource fields. Default scalar tests
ONLY. Preserve all earlier sources/receipts. This is a scope-declared
pilot before a COMPLETE260 controller, not a narrower success condition.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_fresh_Cantelli_SV_joint_low_eta_requests_2026_10_09 as split
import n4_Q3_linked_w_beta_H_curvature_low_eta_box_leaf_2026_10_09 as leaf

INDICES = (149, 208, 247)
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 180, 256 * 1024 * 1024, 2 * 1024 * 1024
require, SCALE, TARGET = split.require, split.SCALE, split.TARGET
SPLIT_PIN = "db439ba1c86e6f533cdd2f5c9ec0354f2e7585c4b98211a758821c49a970f51a"
LEAF_PIN = "0675c4bff82423f529e82e943274b0f47cd1cbcd9fbb578de7e15687a3d26b0c"


def source_drift_check():
    split.source_drift_check()
    leaf.source_drift_check()
    for module, pin in ((split, SPLIT_PIN), (leaf, LEAF_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen integration source integrity only")


def dependency_pins():
    pins = leaf.dependency_pins()
    modules = (split, split.root, split.frontier, split.frontier.previous,
        split.frontier.backend, split.frontier.backend.gaussian_helpers,
        split.frontier.backend.gaussian, split.frontier.backend.integer)
    for path in (Path(__file__), *(Path(module.__file__) for module in modules)):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(path.name not in pins or pins[path.name] == digest, "Unambiguous dependency closure")
        pins[path.name] = digest
    return pins


def compute_fresh_pilot():
    started = time.monotonic()
    source_drift_check()
    initial = dependency_pins()

    def guard():
        require(time.monotonic() - started < TIME_LIMIT, "Complete three-class pilot timer")
        peak = leaf.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "One pilot256MiB")

    cache = leaf.quadrature.build_fresh_quadrature_cache()
    requests = split.root.fresh_root_requests()[2]
    records, child_resources = [], []
    for index in INDICES:
        guard()
        request = requests[index]
        require(request["grid_index"] == index and not request["proved_root_empty"],
                "Entire declared root geometry, not a point/empty substitute")
        high = split.fresh_joint_cut_for_request(request,
            min(60, TIME_LIMIT - (time.monotonic() - started)))
        child_resources.append(high["resources"])
        high_math = {key: value for key, value in high.items() if key != "resources"}
        cut = high["joint_eta_cut_exact"]
        if cut == 0:
            checked = None
            low_closed, upper = True, high["joint_high_eta_score_at_closed_cut_exact"]
        else:
            fresh = leaf.compute_verified_low_eta_box_leaf(request["closed_rectangle"],
                (F(0), cut), cache=cache,
                time_limit_seconds=min(60, TIME_LIMIT - (time.monotonic() - started)))
            checked = leaf._checked_fresh_leaf_math(fresh, request, low_eta_cut=cut)
            child_resources.append(fresh["resources"])
            low_closed = checked["conditional_whole_low_eta_CDF_bound_verified"]
            upper = max(checked["low_eta_upper_exact"], high["joint_high_eta_score_at_closed_cut_exact"])
            del fresh
        require(not low_closed or upper <= TARGET, "BOTH complete routes give<=T<CE")
        records.append({"grid_index": index, "closed_rectangle": request["closed_rectangle"],
            "original_SV_eta_cut_exact": request["etaSV_exact"],
            "fresh_complete_high_eta_route": high_math,
            "fresh_complete_low_eta_result": checked,
            "whole_geometry_all_actual_eta_closed": low_closed,
            "whole_geometry_score_upper_exact": upper})
        print(json.dumps({"event": "ENTIRE_DECLARED_CLASS_FINISHED", "grid_index": index,
            "whole_geometry_all_actual_eta_closed": low_closed,
            "elapsed_seconds": time.monotonic() - started}, sort_keys=True), flush=True)
        guard()
    require(tuple(record["grid_index"] for record in records) == INDICES,
            "Every declared whole class retained even if UNKNOWN")
    source_drift_check()
    final = dependency_pins()
    require(final == initial, "All math sources unchanged through direct fresh computation")
    guard()
    return {"status": "FRESH_THREE_WHOLE_CLASSES_ALL_ETA_JOIN" if all(r["whole_geometry_all_actual_eta_closed"]
        for r in records) else "UNKNOWN_WITH_ALL_THREE_DECLARED_CLASSES_KEPT",
        "scale": SCALE, "target": TARGET, "declared_root_indices_only": INDICES,
        "geometry_classes": records,
        "summary": {"whole_geometry_classes_closed": sum(r["whole_geometry_all_actual_eta_closed"] for r in records),
            "whole_geometry_classes_unknown": sum(not r["whole_geometry_all_actual_eta_closed"] for r in records)},
        "conclusions": {"entire_260_root_or_unrestricted_C4_proved": False,
            "closed_join_faces_and_eta0_retained": True, "saved_numerical_proof_inputs": False},
        "source_pins_integrity_only": final,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": leaf.resources.peak_bytes(),
            "memory_limit_bytes": MEMORY_LIMIT, "time_limit_seconds": TIME_LIMIT,
            "children_sequential": True, "child_resources": child_resources}}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--produce", action="store_true")
    modes.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if not (args.produce or args.replay_existing):
        source_drift_check()
        print(json.dumps(split.self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_suffix(".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a prior receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay needs receipt")
    result = compute_fresh_pilot()
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"),
        allow_nan=False, default=split.root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Declared pilot receipt<=2MiB")
    peak = leaf.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT
            and (peak is None or peak <= MEMORY_LIMIT),
            "Whole CLI including serialization within180s/256MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only input")
        saved = json.loads(output.read_text(encoding="utf-8"))
        fresh = json.loads(raw)
        require({k: v for k, v in saved.items() if k != "resources"}
                == {k: v for k, v in fresh.items() if k != "resources"},
                "ALL nonresource fields EXACT fresh replay match")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "summary": result["summary"], "result": str(output),
        "resources": result["resources"]}, sort_keys=True, default=split.root.json_ready))


if __name__ == "__main__":
    main()
