"""ENTIRE-root fresh ETA FRONTIER, with exact root-empty actual-p pruning.

Preserves the frozen first frontier source; imports only its pure exact
geometry/target/cut consumers, never its producer or numeric receipts.
The fixed root, 260 CLOSED geometry cells, T=4097/10000<CE, exact SV
closed threshold, and explicit unclosed low-eta regions are unchanged.

One genuine ROOT-ONLY improvement: after an actual fresh eta0 backend
has accounted for EVERY signed-beta actual-p cell, take each row's
NECESSARY outer w/beta rectangle. Its exact minimum
 rhoQ^2=(1+minabsbeta^2)^2/[w_effHI*(1-minabsbeta^2)]
can be >= (46/25)^2. Such a WHOLE actual-p class is impossible under
the STRICT root condition actualrho=rhoQ+eta<46/25 and eta>=0, for ALL
eta. Equality is also impossible. We omit ONLY these exact proved
root-empty p classes from the eta-cut maximum, never merely large raw
bounds or rounded rhoLO comparisons. Both orientations and all indices
remain explicitly accounted for. Backend's own proved-empty p classes
are separate. The global tail uses the UNCHANGED global rhoQ lower.

Pruned arithmetic views below are conditional on this root proof; they
are NOT unrestricted-law backend results. Reusing the first source's
private arithmetic consumer does not infer validity from status/flags.
Public production invokes the audited backend DIRECTLY FRESH, verifies
its full cover first, proves each omitted class by exact squares, and
only then computes cuts from the retained genuine raw/rho pairs.
Compact witnesses record (orientation,p-index,min-square,wUP,betaLO,
betaHI); p faces are determined exactly by geometry/grid. Integrity
hashes are NOT substituted for the empty-class proofs.

No full C4 claim: every below-frontier region stays explicit. Default
CLI tiny tests ONLY. Whole260 --produce / read-only --replay-existing,
sequential <=60s children, overall300s/64MiB, exclusive <=1MiB receipt.
No runtime prefix PASS and no old source/receipt edits.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_conditional_cantelli_exact_eta_frontier_2026_10_09 as previous

backend, resources = previous.backend, previous.resources
SCALE, TARGET, ROOT, RHO_CAP = previous.SCALE, previous.TARGET, previous.ROOT, previous.RHO_CAP
TIME_LIMIT, CHILD_LIMIT = previous.TIME_LIMIT, previous.CHILD_LIMIT
MEMORY_LIMIT, OUTPUT_LIMIT = previous.MEMORY_LIMIT, previous.OUTPUT_LIMIT
DEFAULT_NP, DEFAULT_NH = previous.DEFAULT_NP, previous.DEFAULT_NH
require = previous.require
ROOT_EMPTY_WITNESS_FORMAT = ("orientation", "p_index", "rhoQ_min_square_exact",
                             "necessary_w_upper", "necessary_signed_beta_lower", "necessary_signed_beta_upper")


def row_root_rhoQ_min_square(row):
    """Exact necessary local rectangle minimum, including NEGATIVE beta."""
    w = row["necessary_outer_w_interval"]
    beta = row["necessary_outer_signed_beta_interval"]
    require(type(w) in (tuple, list) and len(w) == 2 and all(type(v) is F for v in w)
            and type(beta) in (tuple, list) and len(beta) == 2 and all(type(v) is F for v in beta),
            "Exact NECESSARY local w/signed-beta endpoints")
    wl, wh = w
    blo, bhi = beta
    require(0 < wl <= wh <= 1 and -1 < blo <= bhi < 1, "Ordered necessary local moment rectangle")
    beta2 = backend.minmax_beta_square(blo, bhi)[0]
    return (1 + beta2) ** 2 / (wh * (1 - beta2))


def _root_frontier_from_fresh_backend(fresh, rectangle, Np, NH):
    """Fresh raw proof + EXACT root emptiness, then pure cut arithmetic.

    Mathematical preconditions: fresh audited backend validity AND actual
    rho<46/25 with eta>=0. This private consumer is not a JSON importer.
    """
    all_rows, backend_empty = previous._checked_fresh_rows(fresh, rectangle, Np, NH)
    retained, pruned, witnesses = [], [], []
    for row in all_rows:
        square = row_root_rhoQ_min_square(row)
        if square >= RHO_CAP ** 2:
            pruned.append(row)
            witnesses.append((row["orientation"], row["p_index"], square,
                row["necessary_outer_w_interval"][1], *row["necessary_outer_signed_beta_interval"]))
        else:
            retained.append(row)
    require(len(retained) + len(pruned) + len(backend_empty) == 2 * Np,
            "Every BOTH-orientation p class retained or explicitly proved empty")
    # This is a ROOT-restricted arithmetic view, not a fabricated new
    # unrestricted backend theorem. All raw bounds remain untouched.
    root_view = dict(fresh)
    root_view["p_cells"] = retained
    root_view["proved_empty_p_cells"] = list(backend_empty) + pruned
    root_view["metadata"] = dict(fresh["metadata"], H_cells_checked=len(retained) * NH)
    frontier = previous._frontier_from_fresh_backend(root_view, rectangle, Np, NH)
    frontier["fresh_p_H_cells_checked"] = fresh["metadata"]["H_cells_checked"]
    frontier.update({"root_applicable_p_H_cells_used_for_cut": len(retained) * NH,
        "p_cells_proved_empty_by_unrestricted_backend": len(backend_empty),
        "p_cells_proved_root_empty_by_exact_strict_cap": len(pruned),
        "root_empty_p_class_witnesses": witnesses,
        "all_signed_p_classes_accounted_for": len(retained) + len(pruned) + len(backend_empty),
        "root_pruning_scope": "ONLY actualrho=rhoQ+eta<46/25 and eta>=0. Each omitted actual-p class has necessary local rhoQ_min_square>=cap_square, equality included.",
        "global_tail_rho_lower_unchanged": True})
    require(frontier["all_signed_p_classes_accounted_for"] == 2 * Np,
            "No hard or shared-face actual-p cell omitted without proof")
    return frontier


def compute_verified_eta_frontier(Np=DEFAULT_NP, NH=DEFAULT_NH, time_limit_seconds=TIME_LIMIT):
    """Fresh entire-root geometry frontier; low-eta/global C4 remains open."""
    started = time.monotonic()
    require(type(Np) is int and type(NH) is int, "Exact integer child grids")
    backend.checked_request(ROOT, F(0), Np, NH, CHILD_LIMIT)
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Overall timer only, <=300 seconds")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Whole-root frontier elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Whole-root frontier64MiB working set")
    target_certificate = previous.fresh_target_certificate()
    w_faces, beta_faces, cells = previous.root_grid()
    output_rows, child_count, child_H_count, retained_H_count = [], 0, 0, 0
    for cell in cells:
        guard()
        rectangle = cell["closed_rectangle"]
        square = previous.rhoQ_min_square(rectangle)
        if square >= RHO_CAP ** 2:
            output_rows.append(dict(cell, status="PROVED_EMPTY_BY_STRICT_RHO_CAP",
                rhoQ_min_square_exact=square,
                reason="rhoQ(actualgeometry)>=rhoQ_min>=46/25 but actualrho=rhoQ+eta<46/25 and eta>=0",
                fresh_CDF_backend_called=False))
            continue
        remaining = time_limit_seconds - (time.monotonic() - started)
        require(remaining > 0, "No prefix certificate when global budget exhausted")
        fresh = backend.compute_verified_conditional_cantelli_box(rectangle, F(0), Np=Np, NH=NH,
                    time_limit_seconds=min(CHILD_LIMIT, remaining))
        frontier = _root_frontier_from_fresh_backend(fresh, rectangle, Np, NH)
        output_rows.append(dict(cell, status="FRESH_EXACT_ROOT_HIGH_ETA_FRONTIER_LOW_ETA_UNCLOSED",
                               rhoQ_min_square_exact=square, **frontier))
        child_count += 1
        child_H_count += frontier["fresh_p_H_cells_checked"]
        retained_H_count += frontier["root_applicable_p_H_cells_used_for_cut"]
        del fresh
        guard()
    require(len(output_rows) == 260 and tuple(row["grid_index"] for row in output_rows) == tuple(range(260)),
            "Entire root CLOSED cover, no omitted geometry prefix/face")
    nonempty = [row for row in output_rows if row["status"] != "PROVED_EMPTY_BY_STRICT_RHO_CAP"]
    require(len(nonempty) == child_count, "Every nonempty geometry has exactly one fresh child")
    guard()
    source_files = (Path(__file__), Path(previous.__file__), Path(backend.__file__),
        Path(backend.gaussian_helpers.__file__), Path(backend.gaussian.__file__),
        Path(backend.integer.__file__), Path(resources.__file__))
    return {"status": "ENTIRE_NECESSARY_ROOT_FRESH_EXACT_ETA_FRONTIER_NOT_C4",
        "date": "2026-10-09", "scale": SCALE, "target": TARGET, "root_closed_rectangle": ROOT,
        "actual_rho_strict_cap": RHO_CAP, "w_closed_faces": w_faces, "beta_abs_closed_faces": beta_faces,
        "Np": Np, "NH": NH, "eta_cut_grid": previous.CUT_GRID, "Cantelli_positive_strict_reserve": previous.RESERVE,
        "SV_closed_cut_no_artificial_reserve": True,
        "fresh_target_certificate": target_certificate, "geometry_cells": output_rows,
        "root_empty_p_class_witness_format": ROOT_EMPTY_WITNESS_FORMAT,
        "summary": {"geometry_cells_entire_root": 260, "proved_empty_geometry_cells": 260 - child_count,
            "fresh_nonempty_geometry_children": child_count, "fresh_p_H_cells_checked": child_H_count,
            "root_applicable_p_H_cells_used_for_cuts": retained_H_count,
            "p_classes_proved_root_empty_by_exact_squares": sum(row["p_cells_proved_root_empty_by_exact_strict_cap"] for row in nonempty),
            "Cantelli_useful_high_eta_boxes": sum(row["Cantelli_high_eta_region_potentially_nonempty"] for row in nonempty),
            "joint_useful_high_eta_boxes": sum(row["joint_high_eta_region_potentially_nonempty"] for row in nonempty),
            "geometry_boxes_with_explicit_unclosed_low_eta_region": sum(row["joint_eta_cut_exact"] > 0 for row in nonempty)},
        "premises": {"root_scope": "Arbitrary standardized iid P, canonical w/beta/eta, w and |beta| in ROOT, eta>=0 and actualrho=rhoQ+eta<46/25. Necessary-root reduction is supplied external scope, not proved by this controller.",
            "fresh_backend_mathematical_validity": "Audited exact sign-count Cantelli backend invoked directly fresh; raw all-p/all-H bounds valid even UNKNOWN. Status/labels/source hashes are not mathematics.",
            "root_p_class_pruning": "Fresh backend complete cover checked FIRST. Only necessary local exact rhoQ_min_square>=cap_square proves root class empty for ALL eta, never rounded rhoLO/raw-score pruning.",
            "Shevtsova_external_mathematical_input": "Published iid all-H envelope R_n<=3031/10000*(1+(323/500)/rho), supplied external theorem; no Fourier/H reserves appended.",
            "no_saved_numeric_bounds_or_float_proof_inputs": True},
        "conclusions": {"entire_necessary_geometry_root_accounted_for": True,
            "above_each_joint_eta_frontier_uniform_R4_le_target_strictly_below_CE": True,
            "regions_below_each_frontier_explicitly_unclosed": True,
            "entire_root_or_unrestricted_C4_proved": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_files},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "overall_time_limit_seconds": time_limit_seconds,
            "child_time_limit_seconds": CHILD_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "children_run_sequentially": True, "saved_child_numeric_tables_loaded": False}}


def tiny_regressions():
    """All old pure tests plus exact root-only p pruning; no real producers."""
    old = previous.tiny_regressions()
    checks = old["exact_checks"]
    fake = previous._synthetic_fresh_result()
    unpruned = previous._frontier_from_fresh_backend(fake, fake["closed_rectangle"], fake["Np"], fake["NH"])
    unchanged = _root_frontier_from_fresh_backend(fake, fake["closed_rectangle"], fake["Np"], fake["NH"])
    require(unchanged["p_cells_proved_root_empty_by_exact_strict_cap"] == 0
            and unchanged["Cantelli_eta_cut_exact"] == unpruned["Cantelli_eta_cut_exact"],
            "No arbitrary hard raw/p class omitted when exact root condition fails")
    checks += 2
    rows = fake["p_cells"]
    rows[0]["necessary_outer_w_interval"] = (ROOT[0], ROOT[0])
    rows[0]["necessary_outer_signed_beta_interval"] = (F(0), F(0))
    rows[1]["necessary_outer_w_interval"] = (ROOT[0], ROOT[0])
    rows[1]["necessary_outer_signed_beta_interval"] = (F(-13, 20), F(-3, 5))
    rows[2]["necessary_outer_w_interval"] = (ROOT[0], ROOT[0] + F(1, 1000))
    rows[2]["necessary_outer_signed_beta_interval"] = (F(0), F(0))
    require(row_root_rhoQ_min_square(rows[0]) == RHO_CAP ** 2
            and row_root_rhoQ_min_square(rows[1]) > RHO_CAP ** 2
            and row_root_rhoQ_min_square(rows[2]) < RHO_CAP ** 2,
            "EXACT squared equality root-empty; negative signed-beta min; adjacent cell retained")
    checks += 3
    pruned = _root_frontier_from_fresh_backend(fake, fake["closed_rectangle"], fake["Np"], fake["NH"])
    require(pruned["p_cells_proved_root_empty_by_exact_strict_cap"] == 2
            and pruned["all_signed_p_classes_accounted_for"] == 2 * fake["Np"]
            and pruned["root_applicable_p_H_cells_used_for_cut"] == (2 * fake["Np"] - 2) * fake["NH"]
            and pruned["fresh_p_H_cells_checked"] == 2 * fake["Np"] * fake["NH"],
            "Full accounting separates fresh evaluated classes from root-applicable classes")
    checks += 4
    require(pruned["global_tail_rho_lower_unchanged"] and pruned["rhoQ_box_lower_exact"] == fake["global_actual_rho_lower"]
            and len(pruned["root_empty_p_class_witnesses"]) == 2
            and all(witness[2] >= RHO_CAP ** 2 and len(witness) == 6 for witness in pruned["root_empty_p_class_witnesses"]),
            "Global tail denominator unchanged; compact exact square witnesses, not hash/status proofs")
    checks += 4
    signed = dict(rows[2], necessary_outer_signed_beta_interval=(F(-1, 5), F(1, 10)))
    require(row_root_rhoQ_min_square(signed) == 1 / signed["necessary_outer_w_interval"][1],
            "Signed-beta interval crossingzero uses minabs0")
    checks += 1
    broken = previous._synthetic_fresh_result()
    broken["p_cells"].pop()
    try:
        _root_frontier_from_fresh_backend(broken, broken["closed_rectangle"], broken["Np"], broken["NH"])
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("Root pruning accepted an incomplete original backend cover")
    return {"status": "EXACT_ROOT_ETA_FRONTIER_AND_P_CLASS_PRUNING_TESTS_ONLY", "exact_checks": checks,
            "whole_root_geometry_cells": 260,
            "exact_strict_cap_empty_geometry_cells": old["exact_strict_cap_empty_geometry_cells"],
            "actual_backend_or_full_root_producers_called": 0,
            "synthetic_consumer_tables_are_CDF_proofs": False,
            "entire_root_or_C4_proved_by_tests": False, "old_sources_or_receipts_modified": False}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--produce", action="store_true")
    mode.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if args.self_test or not (args.produce or args.replay_existing):
        print(json.dumps(tiny_regressions(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem + "_whole_root_W20_B13_Np32_NH256_T4097_10000.json")
    require(args.replay_existing or not output.exists(), "Never overwrite a whole-root frontier receipt")
    require(not args.replay_existing or output.exists(), "Read-only fresh full-root replay receipt exists")
    result = compute_verified_eta_frontier(time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=previous.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Compact whole-root frontier receipt<=1MiB")
    peak = resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and (peak is None or peak <= MEMORY_LIMIT),
            "Entire full-root CLI within300s/64MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only frontier receipt input")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for key in fresh:
            if key != "resources":
                require(saved[key] == fresh[key], "Fresh exact full-root frontier replay: " + key)
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "target": TARGET,
        "root_closed_rectangle": ROOT, "summary": result["summary"],
        "output_bytes": len(raw.encode("utf-8")), "resources": result["resources"]},
        sort_keys=True, default=previous.json_ready))


if __name__ == "__main__":
    main()
