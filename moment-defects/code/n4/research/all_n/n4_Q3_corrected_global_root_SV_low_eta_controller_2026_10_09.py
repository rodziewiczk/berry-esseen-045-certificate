"""Fresh COMPLETE necessary-root SV + corrected low-eta BOX controller.

NOT a local snapshot: the EXACT closed 20x13 cover of
 w in[625/2116,1], |beta| in[0,13/20], eta>=0,
 actualrho=rhoQ(w,beta)+eta<46/25
is retained in full, including every shared geometry/eta face. Only
rhoQ_min_square>=cap_square proves a whole geometry class empty (the
physical cap is STRICT). There are no sample masks or trusted JSON
frontiers/price tables/legacy Fourier receipts.

This initial version does NOT execute the ~275s Cantelli frontier scan.
For every nonempty WHOLE geometry box, a fresh exact rhoQ lower gives
 etaSV=max(0,979013/533000-rhoQ_LO).
The supplied published iid Shevtsova envelope .3031*(1+.646/rho)
proves R4<=T=4097/10000 for ALL actual eta>=etaSV, including equality.
Fresh Machin phi0/sqrt10 proves T<CE. This is an explicit external
literature theorem, not a new arithmetic axiom/status/hash premise.

For eta in the ENTIRE CLOSED interval[0,etaSV], directly invoke the
audited correctly-scaled Fourier leaf freshly: N256, complete H1/8
grid (58 nodes, BOTH reflections), fixed16 CLOSED eta cells, pure
contact-Taylor tightening. No adaptive scheduling changes math scope.
The shared etaSV boundary belongs to both routes. If etaSV=0, the
CLOSED SV route alone already covers every eta>=0; no eta0 is dropped.
Each leaf may return UNKNOWN; ALL its failed CLOSED eta classes are
preserved, and every other geometry box is still checked. There is no
easy-box-only replacement or coefficient/partial-H route mixing.

Private validators check numerical arithmetic/complete scopes only
AFTER the direct fresh audited-leaf call. Their validity depends on
that mathematical producer, not on labels/status/Boolean flags. We
derive acceptance again from exact raw endpoints/degree1 Bernstein
coefficients, denominator, ONE687/(8N^2), ONE19h^2/32 and tails.
The frozen OLD incorrectly-scaled generic CF is never on a proof path.
The exact Q3 CDF theorem is NOT substituted for a Prawitz center.

Standing conditional physical premises: standardized iid actual P,
canonical coordinates in the declared root, |X|<=17/4, rhoP<46/25,
closed-CDF Prawitz and the retained physical quadrature/H bridge. A
first-critical fourth owner is placed here only by the retained C3,
attainment/He--Cheng/Shevtsova structural inputs. No finite-atom or
separate M4 assumption on original P is introduced. Program alone is
not an unrestricted C4 proof; all-law use needs those explicit inputs.

Default CLI pure synthetic tests ONLY. Explicit --produce or read-only
--replay-existing: one coordinated sequential whole-root job, <=600s
overall, each child<=60s,256MiB, NEW exclusive<=8MiB receipt. A runtime
or assertion interruption raises BEFORE a partial receipt. A numerical
UNKNOWN receipt accounts for ALL260 classes and every failed eta face.
No old source/receipt edits, no automatic restart/replay/producer.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_conditional_cantelli_exact_eta_frontier_2026_10_09 as root_algebra
import n4_Q3_generic_low_eta_center_only_exact_box_leaf_2026_10_09 as leaf

SCALE, TARGET, ROOT, RHO_CAP = leaf.SCALE, leaf.TARGET, root_algebra.ROOT, root_algebra.RHO_CAP
SV_C, SV_OFFSET = root_algebra.SV_C, root_algebra.SV_OFFSET
SV_RHO = F(979013, 533000)
N, H_STEP, ETA_CELLS = 256, F(1, 8), 16
TIME_LIMIT, CHILD_LIMIT = 600, 60
MEMORY_LIMIT, OUTPUT_LIMIT = 256 * 1024 * 1024, 8 * 1024 * 1024
LEAF_PIN = "e29ec0c0140f48a79495881cc4cc8ffc6ad519817034d5c6ddd78c4662eaaf71"
require = leaf.require


def fresh_root_requests():
    """Every closed root rectangle; exact SV split, not numeric receipts."""
    require(SCALE == root_algebra.SCALE and TARGET == root_algebra.TARGET
            and SV_RHO == SV_C * SV_OFFSET / (TARGET - SV_C), "Exact new target/SV arithmetic")
    w_faces, beta_faces, cells = root_algebra.root_grid()
    result = []
    for cell in cells:
        rectangle = cell["closed_rectangle"]
        square = root_algebra.rhoQ_min_square(rectangle)
        if square >= RHO_CAP ** 2:
            result.append(dict(cell, rhoQ_min_square_exact=square, proved_root_empty=True))
            continue
        rho_lower = max(F(1), F(leaf.integer.sqrt_fraction_interval(square)[0], SCALE))
        eta_sv = max(F(0), SV_RHO - rho_lower)
        sv_score = SV_C * (1 + SV_OFFSET / (rho_lower + eta_sv))
        require(sv_score <= TARGET and eta_sv < RHO_CAP - rho_lower,
                "Exact CLOSED all-H SV split lies below outward physical capacity")
        result.append(dict(cell, rhoQ_min_square_exact=square, proved_root_empty=False,
            rhoQ_lower_exact=rho_lower, etaSV_exact=eta_sv, SV_score_at_closed_cut_exact=sv_score,
            actual_eta_capacity_outer_open=RHO_CAP - rho_lower))
    require(len(result) == 260 and tuple(r["grid_index"] for r in result) == tuple(range(260)),
            "Entire root closed geometry, no prefix or mask")
    return w_faces, beta_faces, tuple(result)


def _checked_fresh_leaf_math(fresh, request):
    """Private exact consumer under the FRESH audited-leaf math premise.

    This is deliberately not a numeric-JSON importer. Status/flags/source
    hashes are not CDF proofs. The public controller calls the leaf directly.
    """
    rectangle, cut, rho = request["closed_rectangle"], request["etaSV_exact"], request["rhoQ_lower_exact"]
    require(cut > 0, "A zero SV cut needs no low-eta child")
    H_grid = leaf.complete_H_grid(H_STEP)
    require(fresh["scale"] == SCALE and fresh["N"] == N and fresh["target"] == TARGET
            and fresh["H_step"] == H_STEP and fresh["closed_rectangle"] == rectangle
            and fresh["closed_eta_cover"] == (F(0), cut), "SAME full rectangle/closed eta/N/H/target")
    require(fresh["box_geometry"]["rhoQ_lo"] == rho
            and tuple(fresh["box_geometry"]["rectangle"]) == rectangle,
            "Fresh matching box denominator, not point substitution")
    rows = fresh["reference_centers_both_orientations"]
    require(len(rows) == 2 * len(H_grid) and {(r["orientation"], r["H"]) for r in rows}
            == {(orientation, H) for orientation in (1, -1) for H in H_grid},
            "ALL58 physical thresholds and BOTH genuine reflections")
    require(all(type(r["raw_Q_center_upper_int"]) is int for r in rows), "Exact fresh whole-box center bounds")
    quad, threshold = F(687, 8 * N * N), F(19, 32) * H_STEP ** 2
    require(fresh["reserves_once"] == {"physical_quad": quad, "physical_H": threshold},
            "ONE physical quadrature/H reserve, including coarse spacing")
    tail = fresh["tail"]["score_upper"]
    require(tail == F(2, 5) and tail < TARGET
            and type(fresh["tail"]["Phi_25_16_lower_int"]) is int
            and 5 * fresh["tail"]["Phi_25_16_lower_int"] > 4 * SCALE,
            "Fresh Gaussian actual-law tails, not a Boolean flag")
    certificate = fresh["reference_metadata"]["fresh_target_certificate"]
    require(certificate["target"] == TARGET and type(certificate["CE_lower_exact"]) is F
            and certificate["CE_lower_exact"] > TARGET, "Fresh target below CE")
    raw_constant = F(max(r["raw_Q_center_upper_int"] for r in rows), SCALE) + quad + threshold
    cells = fresh["cells"]
    require(len(cells) == ETA_CELLS, "Fixed16 complete closed eta cells")
    checked, unresolved = [], []
    for index, cell in enumerate(cells):
        L, U = cut * F(index, ETA_CELLS), cut * F(index + 1, ETA_CELLS)
        require(cell["lower"] == L and cell["upper"] == U, "No eta gaps/shrunk faces/runtime scheduling")
        C, D = cell["transfer_affine_upper"]
        require(type(C) is F and type(D) is F and min(C + D * L, C + D * U) >= 0,
                "Fresh whole-cell nonnegative COMPLETE transfer affine")
        raw_endpoints = raw_constant + 2 * (C + D * L), raw_constant + 2 * (C + D * U)
        polynomial = leaf.algebra.raw_target_for_transfers(raw_constant, [(F(1), (C, D))], rho, TARGET)
        coefficients = leaf.algebra.bernstein_coefficients(polynomial, L, U, degree=1)
        passed = all(v < 0 for v in coefficients)
        score = max(F(0), raw_endpoints[0] / (rho + L), raw_endpoints[1] / (rho + U))
        require(cell["raw_endpoint_uppers"] == raw_endpoints
                and cell["target_polynomial"] == polynomial
                and cell["target_Bernstein_coefficients"] == coefficients
                and cell["score_upper"] == score,
                "Exact raw factor2/denominator/degree1 arithmetic, not status trust")
        record = {"eta_closed_interval": (L, U), "complete_transfer_affine_upper": (C, D),
            "raw_endpoint_uppers": raw_endpoints, "target_Bernstein_coefficients": coefficients,
            "score_upper_exact": score, "strict_numeric_bound_verified": passed}
        checked.append(record)
        if not passed:
            unresolved.append(record)
    upper = max([tail] + [r["score_upper_exact"] for r in checked])
    passed = not unresolved and upper < TARGET
    require(fresh["summary"]["score_upper_exact"] == upper,
            "Whole-child all-H/all-eta score recomputed exactly")
    return {"kind": "FRESH_LOW_ETA_WHOLE_BOX_CDF_BOUND" if passed else "UNKNOWN_NUMERIC_LOW_ETA_WHOLE_BOX",
        "low_eta_closed_scope": (F(0), cut), "low_eta_cells": checked,
        "unresolved_low_eta_cells": unresolved, "low_eta_upper_exact": upper,
        "conditional_whole_low_eta_CDF_bound_verified": passed,
        "both_orientations_H_nodes_checked": len(H_grid), "reference_center_rows_checked": len(rows),
        "physical_reserves_once": {"physical_quad": quad, "physical_H": threshold},
        "actual_law_tail_upper_exact": tail,
        "worst_fresh_reference_center": fresh["worst_Q_center"],
        "contact_Taylor_diagnostic": fresh["reference_metadata"]["contact_Taylor"],
        "reported_child_status_not_a_proof_premise": True}


def compute_verified_global_root_cover(time_limit_seconds=TIME_LIMIT):
    """Fresh ALL260 root requests; every failed closed class remains explicit."""
    started = time.monotonic()
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Cooperative whole-root budget<=600s, diagnostic only")
    require(hashlib.sha256(Path(leaf.__file__).read_bytes()).hexdigest() == LEAF_PIN,
            "Frozen correctly-scaled source drift check, NOT mathematical validity")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "No runtime-prefix global root certificate")
        peak = leaf.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Global root controller256MiB working set")
    target_certificate = leaf.fresh_target_certificate()
    w_faces, beta_faces, requests = fresh_root_requests()
    results, child_calls = [], 0
    for request in requests:
        guard()
        if request["proved_root_empty"]:
            results.append(dict(request, kind="EXACT_ROOT_EMPTY_BY_STRICT_RHO_CAP",
                reason="rhoQ_min_square>=cap_square, eta>=0, actualrho<cap; equality excluded by STRICT physical cap"))
            continue
        if request["etaSV_exact"] == 0:
            results.append(dict(request, kind="ENTIRE_GEOMETRY_CLOSED_SV_ROUTE",
                conditional_whole_geometry_CDF_bound_verified=True,
                reason="rhoQ_LO>=rhoSV: CLOSED SV theorem already covers eta0 and every eta>=0; no omitted boundary"))
            continue
        remaining = time_limit_seconds - (time.monotonic() - started)
        require(remaining > 0, "Do not run/accept an omitted global-prefix request")
        fresh = leaf.compute_verified_low_eta_box_leaf(request["closed_rectangle"], (F(0), request["etaSV_exact"]),
            N=N, H_step=H_STEP, use_contact_taylor=True, initial_eta_cells=ETA_CELLS,
            max_eta_cells=ETA_CELLS, time_limit_seconds=min(CHILD_LIMIT, remaining))
        checked = _checked_fresh_leaf_math(fresh, request)
        results.append(dict(request, **checked))
        child_calls += 1
        del fresh
        guard()
    require(len(results) == 260 and tuple(r["grid_index"] for r in results) == tuple(range(260)),
            "ALL closed geometry classes and shared faces, even UNKNOWN")
    unresolved = [r for r in results if r["kind"] == "UNKNOWN_NUMERIC_LOW_ETA_WHOLE_BOX"]
    passed = not unresolved
    guard()
    source_files = (Path(__file__), Path(leaf.__file__), Path(root_algebra.__file__),
        Path(leaf.resources.__file__), Path(leaf.center.__file__), Path(leaf.radial.__file__),
        Path(leaf.center.derivatives.__file__), Path(leaf.geometry.__file__), Path(leaf.geometry_factory.__file__),
        Path(leaf.geometry.reference_bridge.__file__), Path(leaf.arithmetic.__file__),
        Path(leaf.integer.__file__), Path(leaf.algebra.__file__), leaf.arithmetic.SUPPORT_NOTE,
        leaf.arithmetic.PHYSICAL_BRIDGE, leaf.CONSTRAINT_NOTE)
    return {"status": "EXACT_CONDITIONAL_ENTIRE_N4_PHYSICAL_ROOT_CDF_COVER" if passed
                       else "UNKNOWN_WITH_ENTIRE_ROOT_AND_ALL_FAILED_LOW_ETA_CLASSES",
        "date": "2026-10-09", "scale": SCALE, "target": TARGET, "root_closed_rectangle": ROOT,
        "actual_rho_strict_cap": RHO_CAP, "fresh_target_certificate": target_certificate,
        "SV_external_constants": {"C": SV_C, "offset": SV_OFFSET, "closed_rho_threshold": SV_RHO},
        "closed_w_faces": w_faces, "closed_beta_abs_faces": beta_faces,
        "geometry_classes": results,
        "unresolved_geometry_indices": tuple(r["grid_index"] for r in unresolved),
        "summary": {"geometry_classes_total": 260,
            "exact_rho_empty_geometry_classes": sum(r["kind"] == "EXACT_ROOT_EMPTY_BY_STRICT_RHO_CAP" for r in results),
            "fresh_corrected_low_eta_children": child_calls,
            "low_eta_geometry_classes_with_complete_strict_bound": sum(r["kind"] == "FRESH_LOW_ETA_WHOLE_BOX_CDF_BOUND" for r in results),
            "SV_entire_geometry_classes_without_a_low_eta_gap": sum(r["kind"] == "ENTIRE_GEOMETRY_CLOSED_SV_ROUTE" for r in results),
            "unresolved_geometry_classes": len(unresolved),
            "unresolved_closed_eta_classes": sum(len(r["unresolved_low_eta_cells"]) for r in unresolved)},
        "standing_mathematical_premises": {"physical_actual_law": "Standardized iid P, canonical geometry/eta in ROOT,eta>=0,|X|<=17/4,actualrho=rhoQ+eta<46/25; original P need not be finite or smooth.",
            "Prawitz_and_physical_bridge": "Retained one-sided CLOSED-CDF Prawitz and original-P quadrature/H bridge; M4 is derived from support/rho, not supplied as a new axiom.",
            "Shevtsova_external_envelope": "Published iid R_n<=3031/10000*(1+(323/500)/rho), supplied external literature theorem. All eta>=etaSV covered with <=T<CE, no interpolation reserve for this route.",
            "first_critical_owner_placement": "Retained C3<CE, equality-level attainment and He--Cheng/Shevtsova structural support input place a hypothetical fourth critical owner in this class. These are external analytic inputs, not proved by this program.",
            "fresh_leaf_mathematical_validity": "Correctly-scaled audited direct leaf APIs, not labels/status/hash/numeric JSON. No quarantined legacy Fourier CDF receipt accepted."},
        "conclusions": {"all_260_closed_root_geometry_requests_accounted_for": True,
            "conditional_entire_physical_root_R4_le_T_below_CE": passed,
            "unresolved_classes_kept_in_entire_scope": True,
            "unrestricted_C4_proof_from_program_alone": False,
            "saved_numeric_receipts_or_float_proof_inputs": False,
            "Cantelli_frontier_or_GLOBAL_Q3_producer_called": False,
            "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": leaf.resources.peak_bytes(), "overall_time_limit_seconds": time_limit_seconds,
            "child_time_limit_seconds": CHILD_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "fresh_children_sequential": True}}


def _synthetic_fresh_leaf(request):
    """Private tiny arithmetic/schema input, NEVER a physical CDF proof."""
    cut, rho = request["etaSV_exact"], request["rhoQ_lower_exact"]
    grid = leaf.complete_H_grid(H_STEP)
    rows = [{"orientation": orientation, "H": H, "raw_Q_center_upper_int": SCALE // 5}
            for H in grid for orientation in (1, -1)]
    quad, threshold = F(687, 8 * N * N), F(19, 32) * H_STEP ** 2
    raw_constant = F(1, 5) + quad + threshold
    cells = []
    for j in range(ETA_CELLS):
        L, U = cut * F(j, ETA_CELLS), cut * F(j + 1, ETA_CELLS)
        polynomial = leaf.algebra.raw_target_for_transfers(raw_constant, [(F(1), (F(0), F(0)))], rho, TARGET)
        coefficients = leaf.algebra.bernstein_coefficients(polynomial, L, U, degree=1)
        cells.append({"lower": L, "upper": U, "transfer_affine_upper": (F(0), F(0)),
            "raw_endpoint_uppers": (raw_constant, raw_constant), "target_polynomial": polynomial,
            "target_Bernstein_coefficients": coefficients,
            "score_upper": max(F(0), raw_constant / (rho + L), raw_constant / (rho + U)), "passed": False})
    return {"scale": SCALE, "N": N, "target": TARGET, "H_step": H_STEP,
        "closed_rectangle": request["closed_rectangle"], "closed_eta_cover": (F(0), cut),
        "box_geometry": {"rectangle": request["closed_rectangle"], "rhoQ_lo": rho},
        "reference_centers_both_orientations": rows, "reserves_once": {"physical_quad": quad, "physical_H": threshold},
        "tail": {"score_upper": F(2, 5), "Phi_25_16_lower_int": 4 * SCALE // 5 + 1},
        "reference_metadata": {"fresh_target_certificate": leaf.fresh_target_certificate(), "contact_Taylor": {"used": False}},
        "cells": cells, "summary": {"score_upper_exact": max(F(2, 5), max(c["score_upper"] for c in cells))},
        "worst_Q_center": rows[0], "status": "SYNTHETIC_UNKNOWN_NOT_A_LAW_PROOF"}


def self_tests():
    """Pure roots/cuts/schema arithmetic only; NO N/H/geometry producer."""
    checks = 0
    ws, bs, requests = fresh_root_requests()
    require(len(ws) == 21 and len(bs) == 14 and len(requests) == 260
            and sum(r["proved_root_empty"] for r in requests) == 54, "Whole exact root cover and strict empties")
    checks += 4
    for r in requests:
        if not r["proved_root_empty"]:
            require(r["SV_score_at_closed_cut_exact"] <= TARGET and r["etaSV_exact"] >= 0,
                    "Every nonempty closed SV high-eta route")
            checks += 1
    request = requests[93]
    require(not request["proved_root_empty"] and request["etaSV_exact"] > 0, "Full largest former Cantelli box exists")
    checks += 1
    fake = _synthetic_fresh_leaf(request)
    checked = _checked_fresh_leaf_math(fake, request)
    require(checked["conditional_whole_low_eta_CDF_bound_verified"]
            and len(checked["low_eta_cells"]) == 16 and not checked["unresolved_low_eta_cells"],
            "Private arithmetic consumer derives complete strict bounds, ignores false status/flags")
    checks += 3
    fake["status"] = "INVENTED_PASS_LABEL"
    require(_checked_fresh_leaf_math(fake, request) == checked, "Status is never a proof premise")
    checks += 1
    for mutation in ("H_prefix", "eta_gap", "reserve_double"):
        broken = _synthetic_fresh_leaf(request)
        if mutation == "H_prefix":
            broken["reference_centers_both_orientations"].pop()
        elif mutation == "eta_gap":
            broken["cells"][1]["lower"] += F(1, 10000)
        else:
            broken["reserves_once"]["physical_quad"] *= 2
        try:
            _checked_fresh_leaf_math(broken, request)
        except RuntimeError:
            checks += 1
        else:
            raise RuntimeError("Incomplete/shrunk/double-reserve synthetic class accepted: " + mutation)
    require(leaf.fresh_target_certificate()["CE_lower_exact"] > TARGET, "Fresh target below CE")
    checks += 1
    return {"status": "GLOBAL_SV_CORRECTED_LEAF_CONTROLLER_TINY_TESTS_ONLY", "exact_checks": checks,
        "whole_root_geometry_requests": 260, "actual_leaf_or_other_producer_calls": 0,
        "synthetic_consumer_tables_are_CDF_proofs": False, "unrestricted_C4_proved_by_tests": False,
        "old_sources_or_receipts_modified": False}


def json_ready(value):
    if type(value) is F:
        return str(value)
    raise TypeError("Unsupported exact global root receipt value: " + type(value).__name__)


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--produce", action="store_true")
    mode.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if not (args.produce or args.replay_existing):
        print(json.dumps(self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem + "_W20_B13_N256_H1_8_ETA16_T4097_10000.json")
    require(args.replay_existing or not output.exists(), "Never overwrite any global root receipt")
    require(not args.replay_existing or output.exists(), "Fresh read-only complete root replay requires receipt")
    result = compute_verified_global_root_cover(time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Complete ALL260 root receipt<=8MiB")
    peak = leaf.resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and (peak is None or peak <= MEMORY_LIMIT),
            "Entire root CLI, including serialization, within600s/256MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only global root receipt")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for key in fresh:
            if key != "resources":
                require(saved[key] == fresh[key], "Fresh complete global root replay: " + key)
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "summary": result["summary"],
        "unresolved_geometry_indices": result["unresolved_geometry_indices"],
        "output_bytes": len(raw.encode("utf-8")), "resources": result["resources"]}, sort_keys=True, default=json_ready))


if __name__ == "__main__":
    main()
