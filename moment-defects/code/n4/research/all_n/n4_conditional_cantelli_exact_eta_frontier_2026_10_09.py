"""Fresh exact ETA FRONTIER over the ENTIRE necessary n4 moment root.

This is NOT a proof of unrestricted C4.  The closed root is
 w in [625/2116,1], |beta| in [0,13/20], eta >= 0,
 actual rho = rhoQ(w,beta)+eta < 46/25,
 rhoQ^2 = (1+beta^2)^2/[w(1-beta^2)].
Twenty equal CLOSED w intervals and thirteen CLOSED beta intervals of
width 1/20 cover the entire rectangle, including all shared faces.
Only rhoQ_min^2 >= (46/25)^2 proves a whole geometry cell empty, because
the physical rho cap is STRICT.  No sample, optimizer status, saved
numeric receipt or geometric corner feasibility is a proof premise.

Every other rectangle calls the audited exact all-p/all-H Cantelli
backend FRESH at eta_lower=0, even if its status is UNKNOWN.  Its raw
CDF bounds remain valid: for every actual p cell i,
 R4 <= raw_i/(rhoQ_i_LO+eta), including both signed beta orientations.
The separate global tail has raw <= 2/5.  Thus
 cC = max(0, max_i(raw_i/T-rhoQ_i_LO), (2/5)/T-rhoQ_box_LO)
is an exact sufficient non-strict eta cut.  Rounding UP to the rational
1e-4 grid and then adding 1e-4 yields a STRICT whole-box bound < T at
every eta >= the recorded Cantelli cut.  The local p/rho dependence is
retained; raw_i and rhoQ_i_LO are not replaced by independent maxima.

The optional second COMPLETE route uses the supplied published iid
Shevtsova all-H envelope .3031*(1+.646/rho).  Its exact cut is obtained
from rhoSV=.3031*.646/(T-.3031), without an artificial reserve: the
CLOSED boundary gives <=T, sufficient because fresh arithmetic proves
T<CE.  Thus the complete joint frontier guarantees <=T<CE; Cantelli
alone gives <T.  A zero SV cut does not manufacture a low-eta gap.
The MINIMUM of the two COMPLETE whole-box eta cuts is valid; no p/H
contribution or polynomial coefficient is mixed between routes.
This external envelope is an explicit mathematical premise, not a
Boolean/JSON/source-integrity premise.

T=4097/10000 is proved below CE=(3+sqrt(10))*phi(0)/6 using a FRESH
Machin pi/phi(0) enclosure and a fresh exact sqrt(10) enclosure.  This
is not a comparison to the older conservative target 256/625.

Below the recorded frontier (and under the physical rho cap) each
nonempty rectangle remains explicitly UNCLOSED.  A cut >= the outward
eta capacity means no useful high-eta region from that route, NOT that
the moment class is empty.  No support or fourth moment is needed by
Cantelli; the restriction to the necessary root is an external scope.

Default CLI: tiny exact tests ONLY. Explicit --produce performs the
whole 260-rectangle fresh scan, each child <=60s, overall <=300s and
64MiB, then writes one NEW exclusive <=1MiB receipt.  There is no prefix
PASS: incomplete runtime raises before any receipt.  --replay-existing
recomputes the entire root read-only and compares all nonresource data.
No producer is called by self-tests. Preserve all older sources/receipts.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_conditional_sign_count_cantelli_exact_box_2026_10_09 as backend
import n4_windows_resource_guard_2026_10_09 as resources

SCALE = backend.SCALE
TARGET = F(4097, 10000)
ROOT = (F(625, 2116), F(1), F(0), F(13, 20))
RHO_CAP = F(46, 25)
SV_C, SV_OFFSET = F(3031, 10000), F(323, 500)
RESERVE, CUT_GRID = F(1, 10000), F(1, 10000)
NW, NBETA, DEFAULT_NP, DEFAULT_NH = 20, 13, 32, 256
TIME_LIMIT, CHILD_LIMIT = 300, 60
MEMORY_LIMIT, OUTPUT_LIMIT = 64 * 1024 * 1024, 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def root_grid():
    """Exact fixed CLOSED cover; repeated faces are intentional."""
    wl, wh, bl, bh = ROOT
    w_faces = tuple(wl + (wh - wl) * F(i, NW) for i in range(NW + 1))
    beta_faces = tuple(F(i, 20) for i in range(NBETA + 1))
    require(w_faces[0] == wl and w_faces[-1] == wh
            and beta_faces[0] == bl and beta_faces[-1] == bh,
            "Exact whole-root outer faces")
    cells = tuple({"grid_index": wi * NBETA + bi, "w_index": wi, "beta_index": bi,
                   "closed_rectangle": (w_faces[wi], w_faces[wi + 1], beta_faces[bi], beta_faces[bi + 1])}
                  for wi in range(NW) for bi in range(NBETA))
    require(len(cells) == 260, "Entire fixed 20x13 CLOSED geometry cover")
    return w_faces, beta_faces, cells


def rhoQ_min_square(rectangle):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is F for value in rectangle), "Four exact geometry endpoints")
    wl, wh, bl, bh = rectangle
    require(0 < wl <= wh <= 1 and 0 <= bl <= bh < 1, "Closed necessary moment rectangle")
    return (1 + bl ** 2) ** 2 / (wh * (1 - bl ** 2))


def strict_cap_empty(rectangle):
    """Equality is empty ONLY because actual rho < cap and eta >= 0."""
    return rhoQ_min_square(rectangle) >= RHO_CAP ** 2


def upward_strict_cut(non_strict_cut):
    require(type(non_strict_cut) is F, "Exact rational non-strict eta cut")
    nonnegative = max(F(0), non_strict_cut)
    multiple = backend.integer.ceil_div(nonnegative.numerator * CUT_GRID.denominator,
                                        nonnegative.denominator * CUT_GRID.numerator)
    result = multiple * CUT_GRID + RESERVE
    require(result >= nonnegative + RESERVE and result > nonnegative,
            "Upward rational grid plus positive strict reserve")
    return result


def fresh_target_certificate():
    pi, phi0 = backend.gaussian.pi_and_phi0()
    sqrt10 = backend.integer.sqrt_fraction_interval(F(10))
    ce_lower = F((3 * SCALE + sqrt10[0]) * phi0[0], 6 * SCALE ** 2)
    require(TARGET < ce_lower, "Fresh Machin/sqrt10 proves 4097/10000 < CE")
    require(SV_C < TARGET and SV_OFFSET > 0, "Positive exact Shevtsova threshold")
    return {"target": TARGET, "CE_formula": "(3+sqrt(10))*phi(0)/6",
            "fresh_pi_bracket": pi, "fresh_phi0_bracket": phi0,
            "fresh_sqrt10_bracket": sqrt10, "CE_lower_exact": ce_lower,
            "target_strictly_below_CE": True,
            "SV_rho_threshold_exact": SV_C * SV_OFFSET / (TARGET - SV_C)}


def _checked_fresh_rows(fresh, rectangle, Np, NH):
    """Private arithmetic consumer, under the fresh audited-backend premise.

    These checks catch integration errors; labels/status/hash do not establish
    mathematical validity. The public producer obtains this object solely by
    a direct fresh audited-backend call, never by reading numeric JSON.
    """
    require(fresh["closed_rectangle"] == rectangle and fresh["eta_lower"] == F(0)
            and fresh["scale"] == SCALE and fresh["Np"] == Np and fresh["NH"] == NH
            and fresh["closed_H_domain"] == (backend.H_LO, backend.H_HI),
            "Same fresh exact eta0 rectangle/grid/scale/H scope")
    rows, empties = fresh["p_cells"], fresh["proved_empty_p_cells"]
    require(len(rows) + len(empties) == 2 * Np
            and fresh["metadata"]["H_cells_checked"] == len(rows) * NH,
            "Complete BOTH signed-beta actual-p/H covers, no prefix")
    labels = [(row["orientation"], row["p_index"]) for row in rows + empties]
    require(set(labels) == {(orientation, i) for orientation in (1, -1) for i in range(Np)}
            and len(labels) == len(set(labels)), "Each exact signed p cell accounted for ONCE")
    require(type(fresh["global_actual_rho_lower"]) is F and fresh["global_actual_rho_lower"] > 0,
            "Fresh positive eta0 global rhoQ lower")
    for row in rows:
        require(type(row["raw_upper_int"]) is int and row["raw_upper_int"] >= 0
                and type(row["actual_rho_lower"]) is F and row["actual_rho_lower"] > 0
                and row["H_closed_cells_checked"] == NH,
                "Exact nonnegative raw whole-H bound and local eta0 rhoQ lower")
    return rows, empties


def _frontier_from_fresh_backend(fresh, rectangle, Np, NH):
    """Complete route cuts; input must be FRESH mathematically valid backend."""
    rows, empties = _checked_fresh_rows(fresh, rectangle, Np, NH)
    global_rho = fresh["global_actual_rho_lower"]
    tail_raw = F(2, 5)
    raw_cut, worst = max(F(0), tail_raw / TARGET - global_rho), None
    worst_kind = "tail" if raw_cut > 0 else "zero_floor"
    for row in rows:
        candidate = F(row["raw_upper_int"], SCALE) / TARGET - row["actual_rho_lower"]
        if candidate > raw_cut:
            raw_cut, worst, worst_kind = candidate, row, "actual_p_H_cell"
    cantelli_cut = upward_strict_cut(raw_cut)
    cantelli_score = max([tail_raw / (global_rho + cantelli_cut)]
                         + [F(row["raw_upper_int"], SCALE) / (row["actual_rho_lower"] + cantelli_cut)
                            for row in rows])
    require(cantelli_score < TARGET, "Entire fresh Cantelli route passes at upward reserved cut")
    sv_rho = SV_C * SV_OFFSET / (TARGET - SV_C)
    sv_raw_cut = max(F(0), sv_rho - global_rho)
    sv_cut = sv_raw_cut
    sv_score = SV_C * (1 + SV_OFFSET / (global_rho + sv_cut))
    require(sv_score <= TARGET, "Entire external all-H SV route <=T at its exact CLOSED cut")
    if cantelli_cut <= sv_cut:
        joint_cut, selected_route, joint_score = cantelli_cut, "Cantelli", cantelli_score
    else:
        joint_cut, selected_route, joint_score = sv_cut, "Shevtsova_external", sv_score
    require(joint_score <= TARGET and joint_cut >= 0,
            "ONE complete whole-box route, not mixed contributions")
    eta_cap_outer = RHO_CAP - global_rho
    require(eta_cap_outer > 0, "Nonempty strict-cap geometry has positive outward eta capacity")
    worst_record = None if worst is None else {
        key: worst[key] for key in ("orientation", "p_index", "lower", "upper", "raw_upper_int",
            "actual_rho_lower", "worst_H_index", "worst_H_closed_cell",
            "necessary_outer_w_interval", "necessary_outer_signed_beta_interval")}
    return {"rhoQ_box_lower_exact": global_rho, "eta_capacity_outer_open": eta_cap_outer,
            "Cantelli_non_strict_cut_exact": raw_cut, "Cantelli_eta_cut_exact": cantelli_cut,
            "Cantelli_score_at_cut_exact": cantelli_score,
            "Cantelli_worst_cut_kind": worst_kind, "Cantelli_worst_p_H": worst_record,
            "Cantelli_high_eta_region_potentially_nonempty": cantelli_cut < eta_cap_outer,
            "SV_non_strict_cut_exact": sv_raw_cut, "SV_eta_cut_exact": sv_cut,
            "SV_score_at_cut_exact": sv_score,
            "joint_eta_cut_exact": joint_cut, "joint_complete_route": selected_route,
            "joint_score_at_cut_exact": joint_score,
            "joint_high_eta_region_potentially_nonempty": joint_cut < eta_cap_outer,
            "remaining_eta_outer_upper_exact": min(joint_cut, eta_cap_outer),
            "remaining_region": ("UNCLOSED: actual 0<=eta<joint_eta_cut and rhoQ(actualgeometry)+eta<46/25. A cut above capacity is NOT an emptiness proof."
                                 if joint_cut > 0 else "NONE: external SV already gives <=T<CE for ALL actual eta>=0 in this geometry box."),
            "fresh_p_H_cells_checked": len(rows) * NH, "fresh_p_cells_bounded": len(rows),
            "fresh_p_cells_proved_empty": len(empties),
            "backend_status_not_a_proof_premise": True}


def compute_verified_eta_frontier(Np=DEFAULT_NP, NH=DEFAULT_NH, time_limit_seconds=TIME_LIMIT):
    """Fresh ENTIRE-root geometry frontier; low-eta/global C4 remains open."""
    started = time.monotonic()
    require(type(Np) is int and type(NH) is int, "Exact integer child grids")
    backend.checked_request(ROOT, F(0), Np, NH, CHILD_LIMIT)
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Overall timer only, <=300 seconds")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Whole-root frontier elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Whole-root frontier64MiB working set")
    target_certificate = fresh_target_certificate()
    w_faces, beta_faces, cells = root_grid()
    output_rows, child_count, child_H_count = [], 0, 0
    for cell in cells:
        guard()
        rectangle = cell["closed_rectangle"]
        square = rhoQ_min_square(rectangle)
        if square >= RHO_CAP ** 2:
            output_rows.append(dict(cell, status="PROVED_EMPTY_BY_STRICT_RHO_CAP",
                rhoQ_min_square_exact=square,
                reason="rhoQ(actualgeometry)>=rhoQ_min>=46/25 but actualrho=rhoQ+eta<46/25 and eta>=0",
                fresh_CDF_backend_called=False))
            continue
        remaining = time_limit_seconds - (time.monotonic() - started)
        require(remaining > 0, "No prefix certificate when the global budget is exhausted")
        fresh = backend.compute_verified_conditional_cantelli_box(rectangle, F(0), Np=Np, NH=NH,
                    time_limit_seconds=min(CHILD_LIMIT, remaining))
        frontier = _frontier_from_fresh_backend(fresh, rectangle, Np, NH)
        output_rows.append(dict(cell, status="FRESH_EXACT_HIGH_ETA_FRONTIER_LOW_ETA_UNCLOSED",
                               rhoQ_min_square_exact=square, **frontier))
        child_count += 1
        child_H_count += frontier["fresh_p_H_cells_checked"]
        del fresh
        guard()
    require(len(output_rows) == 260 and tuple(row["grid_index"] for row in output_rows) == tuple(range(260)),
            "Entire root CLOSED cover, no omitted geometry prefix/face")
    nonempty = [row for row in output_rows if row["status"] != "PROVED_EMPTY_BY_STRICT_RHO_CAP"]
    require(len(nonempty) == child_count, "Every nonempty geometry has exactly one fresh child")
    guard()
    source_files = (Path(__file__), Path(backend.__file__), Path(backend.gaussian_helpers.__file__),
                    Path(backend.gaussian.__file__), Path(backend.integer.__file__), Path(resources.__file__))
    return {"status": "ENTIRE_NECESSARY_ROOT_FRESH_EXACT_ETA_FRONTIER_NOT_C4",
        "date": "2026-10-09", "scale": SCALE, "target": TARGET, "root_closed_rectangle": ROOT,
        "actual_rho_strict_cap": RHO_CAP, "w_closed_faces": w_faces, "beta_abs_closed_faces": beta_faces,
        "Np": Np, "NH": NH, "eta_cut_grid": CUT_GRID, "positive_strict_reserve": RESERVE,
        "fresh_target_certificate": target_certificate, "geometry_cells": output_rows,
        "summary": {"geometry_cells_entire_root": 260, "proved_empty_geometry_cells": 260 - child_count,
            "fresh_nonempty_geometry_children": child_count, "fresh_p_H_cells_checked": child_H_count,
            "Cantelli_useful_high_eta_boxes": sum(row["Cantelli_high_eta_region_potentially_nonempty"] for row in nonempty),
            "joint_useful_high_eta_boxes": sum(row["joint_high_eta_region_potentially_nonempty"] for row in nonempty),
            "geometry_boxes_with_explicit_unclosed_low_eta_region": sum(row["joint_eta_cut_exact"] > 0 for row in nonempty)},
        "premises": {"root_scope": "Arbitrary standardized iid P, canonical w/beta/eta, w and |beta| in ROOT, eta>=0 and actualrho=rhoQ+eta<46/25. This necessary-root reduction is supplied external scope, not proved by this controller.",
            "fresh_backend_mathematical_validity": "Audited exact conditional sign-count Cantelli backend invoked directly fresh; raw all-p/all-H bounds remain valid even UNKNOWN. Labels/status/source hashes do not substitute for that mathematics.",
            "Shevtsova_external_mathematical_input": "Published iid all-H envelope R_n<=3031/10000*(1+(323/500)/rho), supplied external theorem. No Fourier/H reserves appended.",
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


def _synthetic_fresh_result():
    """Synthetic PRIVATE consumer input ONLY; never a law/CDF certificate."""
    Np, NH, rows = 16, 64, []
    rectangle = (F(9, 10), F(19, 20), F(7, 20), F(9, 20))
    for orientation in (1, -1):
        for i in range(Np):
            rows.append({"orientation": orientation, "p_index": i, "lower": F(1, 3), "upper": F(2, 5),
                "raw_upper_int": SCALE // 2 if i == 0 else 4 * SCALE // 5,
                "actual_rho_lower": F(1) if i == 0 else F(9, 5),
                "H_closed_cells_checked": NH, "worst_H_index": 0,
                "worst_H_closed_cell": (F(-2), F(-1)),
                "necessary_outer_w_interval": rectangle[:2],
                "necessary_outer_signed_beta_interval": rectangle[2:]})
    return {"closed_rectangle": rectangle, "eta_lower": F(0), "scale": SCALE, "Np": Np, "NH": NH,
        "closed_H_domain": (backend.H_LO, backend.H_HI), "p_cells": rows, "proved_empty_p_cells": [],
        "metadata": {"H_cells_checked": len(rows) * NH}, "global_actual_rho_lower": F(1),
        "status": "UNKNOWN", "conclusions": {"all_CDF_passed": False}}


def tiny_regressions():
    """Exact geometry/cut consumer tests ONLY, zero actual backend producers."""
    checks = 0
    ws, bs, cells = root_grid()
    require(len(ws) == 21 and len(bs) == 14 and len(cells) == 260, "Complete root grid")
    checks += 1
    for wi in range(NW):
        for bi in range(NBETA):
            rectangle = cells[wi * NBETA + bi]["closed_rectangle"]
            require(rectangle == (ws[wi], ws[wi + 1], bs[bi], bs[bi + 1]), "No missing CLOSED grid cell")
            if wi < NW - 1:
                require(rectangle[1] == cells[(wi + 1) * NBETA + bi]["closed_rectangle"][0], "Shared w face retained")
            if bi < NBETA - 1:
                require(rectangle[3] == cells[wi * NBETA + bi + 1]["closed_rectangle"][2], "Shared beta face retained")
            checks += 1
    require(strict_cap_empty((ROOT[0], ROOT[0], F(0), F(0)))
            and not strict_cap_empty((ROOT[0], ROOT[0] + F(1, 1000), F(0), F(0))),
            "Strict physical cap: equality empty, adjacent nonempty cell retained")
    checks += 2
    empty_count = sum(strict_cap_empty(cell["closed_rectangle"]) for cell in cells)
    require(0 < empty_count < 260, "Root grid has both exact empty and nonempty geometry")
    checks += 1
    for raw in (F(-1), F(0), F(1, 3), F(12345, 10000), F(1234501, 1000000)):
        cut = upward_strict_cut(raw)
        require(cut >= max(F(0), raw) + RESERVE and (cut / CUT_GRID).denominator == 1,
                "Exact upward cut plus positive reserve")
        checks += 1
    fake = _synthetic_fresh_result()
    frontier = _frontier_from_fresh_backend(fake, fake["closed_rectangle"], fake["Np"], fake["NH"])
    require(frontier["Cantelli_non_strict_cut_exact"] == F(1, 2) / TARGET - 1
            and frontier["Cantelli_worst_p_H"]["p_index"] == 0,
            "Retain SAME p-cell raw/rho correlation, not largest independent raw")
    checks += 1
    require(frontier["Cantelli_score_at_cut_exact"] < TARGET
            and frontier["SV_score_at_cut_exact"] == TARGET
            and frontier["joint_eta_cut_exact"] == min(frontier["Cantelli_eta_cut_exact"], frontier["SV_eta_cut_exact"]),
            "Complete route cuts and strict whole-cell min")
    checks += 3
    zero_sv = _synthetic_fresh_result()
    zero_sv["global_actual_rho_lower"] = SV_C * SV_OFFSET / (TARGET - SV_C)
    for row in zero_sv["p_cells"]:
        row["actual_rho_lower"] = zero_sv["global_actual_rho_lower"]
    zero_frontier = _frontier_from_fresh_backend(zero_sv, zero_sv["closed_rectangle"], zero_sv["Np"], zero_sv["NH"])
    require(zero_frontier["SV_eta_cut_exact"] == 0 and zero_frontier["SV_score_at_cut_exact"] == TARGET
            and zero_frontier["joint_eta_cut_exact"] == 0
            and zero_frontier["remaining_region"].startswith("NONE"),
            "Exact CLOSED SV equality covers eta0 without manufacturing a low-eta gap")
    checks += 4
    fake["status"] = "invented_PASS_label"
    require(_frontier_from_fresh_backend(fake, fake["closed_rectangle"], fake["Np"], fake["NH"]) == frontier,
            "Ignore backend status/Boolean labels as proof premises")
    checks += 1
    for row in fake["p_cells"]:
        row["raw_upper_int"] = 2 * SCALE
    larger = _frontier_from_fresh_backend(fake, fake["closed_rectangle"], fake["Np"], fake["NH"])
    require(not larger["Cantelli_high_eta_region_potentially_nonempty"]
            and larger["remaining_region"].startswith("UNCLOSED"),
            "Cut above eta capacity is NOT a whole-class emptiness proof")
    checks += 1
    broken = _synthetic_fresh_result()
    broken["p_cells"].pop()
    try:
        _frontier_from_fresh_backend(broken, broken["closed_rectangle"], broken["Np"], broken["NH"])
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("Incomplete p/H prefix accepted")
    try:
        rhoQ_min_square((0.3, F(1), F(0), F(1, 20)))
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("Floating geometry proof input accepted")
    target = fresh_target_certificate()
    require(target["CE_lower_exact"] > TARGET
            and target["SV_rho_threshold_exact"] == SV_C * SV_OFFSET / (TARGET - SV_C),
            "Fresh CE target certificate and exact external SV threshold")
    checks += 2
    return {"status": "EXACT_ETA_FRONTIER_GEOMETRY_AND_CONSUMER_TESTS_ONLY", "exact_checks": checks,
            "whole_root_geometry_cells": 260, "exact_strict_cap_empty_geometry_cells": empty_count,
            "actual_backend_or_full_root_producers_called": 0,
            "synthetic_consumer_tables_are_CDF_proofs": False,
            "entire_root_or_C4_proved_by_tests": False, "old_sources_or_receipts_modified": False}


def json_ready(value):
    if type(value) is F:
        return str(value)
    raise TypeError("Unsupported exact frontier receipt value: " + type(value).__name__)


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
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=json_ready) + "\n"
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
        sort_keys=True, default=json_ready))


if __name__ == "__main__":
    main()
