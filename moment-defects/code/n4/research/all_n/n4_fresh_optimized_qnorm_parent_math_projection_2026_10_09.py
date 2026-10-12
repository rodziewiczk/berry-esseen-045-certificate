"""PURE smaller projection AFTER a complete DIRECT optimized parent proof.

project_complete_parent_result(result) returns a NEW dictionary with the
SAME top-level keys and values/scopes. For every parent/child low result,
it preserves ALL16 closed eta cells, failed indices, H/reflection counts,
target/tails/reserves/scores and the selected worst COMPLETE row proof.
It drops ONLY these three DUPLICATE alternative row-proof dictionaries:
 complete_baseline_signed_row_proof,
 complete_refined_radius_signed_row_proof,
 complete_baseline_ABS_row_proof.
They occur only inside each cell's worst_complete_H_row. No polynomial,
endpoint, Bernstein coefficient, denominator face, signed Gamma/ABS,
ONE quad/H reserve, local-quad model or selected route is changed.
Cell-level baseline/refined R2 polynomials and ABS transfer also remain.

The selected row already contains its FULL chosen uniform polynomial,
endpoint/Bernstein/score/reserve/linear-transfer proof, and the full
audited consumer checked ALL H/reflections before retaining this worst
row. Its three complete alternatives were only duplicated diagnostics.
They are never numerical premises of this projection or a later replay.
ALL5 exact requests/high pairs, initial UNKNOWN parent, all4 attempted
children, own cuts, strict-empty/cut0 cases and every shared face stay.
Directparent closure OR the exhaustive4-child cover is unchanged.

MATHEMATICAL prerequisite for a proof workflow: the caller just DIRECTLY
ran frozen6ad's complete parent coordinator, including its audited A1/
Gamma/V5/high analytic stages. This module does not establish their truth
from fields, flags, source hashes, statuses or parsed numeric receipts.
Its shape checks and synthetic tests do NOT accept a CDF/root theorem.
Structural JSON diagnostics may use the same projection to measure size,
but are NEVER a mathematical proof/comparison input. Every proof replay
must re-run the FULL DIRECT parent computation BEFORE this projection.

No inplace edits: top result, parent/child records, low results, cells
and changed worst-row dictionaries are new objects. Unchanged values
are shared read-only. No numeric bound is recomputed, rounded, clipped,
minimized or relabeled. No CF/cache/Cantelli/Gamma/radius/CDF producer
is imported or called. No file writes/CLI/import-time tests. Fraction/
dict definitions only; source pins are integrity, not mathematics.
Preserve every older source/receipt. No entire-root/unrestricted C4 claim.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

PARENT_NAME = "n4_fresh_optimized_qnorm_parent_four_child_coordinator_2026_10_09.py"
PARENT_PIN = "6ad87c2f8dc3bca497b6ba8d81afc0932bc059175299c09410ee83d934556cdd"
ALTERNATIVE_PROOF_KEYS = (
    "complete_baseline_signed_row_proof",
    "complete_refined_radius_signed_row_proof",
    "complete_baseline_ABS_row_proof",
)
SELECTED_PROOF_KEYS = (
    "normalized_target_polynomial", "normalized_target_endpoint_uppers",
    "degree2_Bernstein_coefficients", "normalized_score_denominator_face_ratios",
    "normalized_score_upper", "whole_cell_strict_numeric_inequality", "ONE_reserves",
    "orientation", "H", "normalized_reference_center_upper_exact", "selected_WHOLE_cell_route",
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def source_drift_check():
    path = Path(__file__).with_name(PARENT_NAME)
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PARENT_PIN,
            "Frozen complete-parent source integrity only, not bound provenance")


def dependency_pins():
    files = (Path(__file__), Path(__file__).with_name(PARENT_NAME))
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def _project_selected_row(row):
    require(type(row) is dict and all(key in row for key in SELECTED_PROOF_KEYS),
            "Selected FULL complete row proof must remain, not only its score")
    require(all(key in row and type(row[key]) is dict for key in ALTERNATIVE_PROOF_KEYS),
            "ONLY the three expected duplicate alternatives are omitted")
    require("signed_Gamma_model_retained" in row or "complete_ABS_transfer_affine_upper" in row,
            "Keep the chosen actual signed Gamma OR complete ABS linear bound")
    return {key: value for key, value in row.items() if key not in ALTERNATIVE_PROOF_KEYS}


def _project_complete_low_result(low):
    if low is None:
        return None
    require(type(low) is dict and type(low["cells"]) in (tuple, list) and len(low["cells"]) == 16,
            "Every complete low result has ALL16 original closed eta cells")
    old_cells = low["cells"]
    interval = tuple(low["closed_eta_cover"])
    require((old_cells[0]["lower"], old_cells[-1]["upper"]) == interval
            and all(left["upper"] == right["lower"] for left, right in zip(old_cells, old_cells[1:])),
            "Exact original outer and shared eta faces preserved")
    require(tuple(i for i, cell in enumerate(old_cells) if not cell["passed"])
            == tuple(low["unresolved_eta_cell_indices"]), "ALL failed eta-cell indices retained")
    cells = []
    for original in old_cells:
        require(original["H_reflection_rows_checked"] == low["summary"]["ALL_H_reflection_rows_per_cell"],
                "Original complete all-H/BOTH-reflection check count retained")
        cell = dict(original)
        cell["worst_complete_H_row"] = _project_selected_row(original["worst_complete_H_row"])
        cells.append(cell)
    projected = dict(low)
    projected["cells"] = tuple(cells) if type(low["cells"]) is tuple else cells
    return projected


def _project_join_record(record):
    require(type(record) is dict and "request" in record and "fresh_complete_low_eta_result" in record,
            "Complete original geometry join, including empty/cut0/UNKNOWN")
    projected = dict(record)
    projected["fresh_complete_low_eta_result"] = _project_complete_low_result(record["fresh_complete_low_eta_result"])
    return projected


def project_complete_parent_result(result):
    """Pure structural projection AFTER DIRECT complete math, NEVER acceptance."""
    require(type(result) is dict and type(result["all_five_exact_requests"]) in (tuple, list)
            and len(result["all_five_exact_requests"]) == 5
            and type(result["all_five_DIRECT_high_pairs"]) in (tuple, list)
            and len(result["all_five_DIRECT_high_pairs"]) == 5,
            "Keep ALL5 exact parent/child requests and their OWN DIRECT high pairs")
    requests = result["all_five_exact_requests"]
    require(result["whole_parent_request"] == requests[0]
            and all(len(pair) == 2 and pair[0] == request
                    for request, pair in zip(requests, result["all_five_DIRECT_high_pairs"])),
            "Same entire declared parent/ALL4 child scopes, no high-pair swap")
    initial = result["initial_parent_complete_join"]
    children = result["all_four_complete_child_joins_if_parent_UNKNOWN"]
    require(initial["request"] == requests[0] and type(children) in (tuple, list)
            and len(children) in (0, 4), "Keep original direct parent and all attempted children")
    require(initial["whole_geometry_all_actual_eta_closed"] or len(children) == 4,
            "An UNKNOWN parent must retain EVERY four completed child joins")
    if children:
        require(tuple(child["request"] for child in children) == tuple(requests[1:]),
                "All CLOSED midpoint child scopes stay in exact original order")
    projected = dict(result)
    projected["initial_parent_complete_join"] = _project_join_record(initial)
    new_children = tuple(_project_join_record(child) for child in children)
    projected["all_four_complete_child_joins_if_parent_UNKNOWN"] = (
        new_children if type(children) is tuple else list(new_children))
    require(set(projected) == set(result) and projected["summary"] == result["summary"]
            and projected["conclusions"] == result["conclusions"],
            "Top keys/closure/score/failure claims unchanged, not new mathematics")
    return projected


def self_tests():
    """Dormant synthetic shape/nonmutation ONLY, no physical/CDF producer."""
    from copy import deepcopy
    from fractions import Fraction as F
    source_drift_check()
    requests = tuple({"grid_index": 200, "geometry_path": path}
                     for path in ((), (0,), (1,), (2,), (3,)))
    row = {key: (F(-1), F(1)) for key in SELECTED_PROOF_KEYS}
    row.update({"selected_WHOLE_cell_route": "refined_radius_signed_A1_R2",
        "signed_Gamma_model_retained": (F(1, 7), F(-1, 11)), "orientation": 1, "H": F(-1, 2),
        "whole_cell_strict_numeric_inequality": False, "normalized_score_upper": F(1, 2),
        "ONE_reserves": (F(1, 10000), F(1, 5000))})
    for key in ALTERNATIVE_PROOF_KEYS:
        row[key] = {"synthetic_duplicate_payload_NOT_math": tuple(range(32))}
    cells = [{"lower": F(j, 16), "upper": F(j + 1, 16), "passed": False,
              "H_reflection_rows_checked": 116, "worst_complete_H_row": deepcopy(row)} for j in range(16)]
    low = {"closed_eta_cover": (F(0), F(1)), "cells": cells, "unresolved_eta_cell_indices": tuple(range(16)),
           "summary": {"ALL_H_reflection_rows_per_cell": 116}, "tail": F(2, 5)}
    initial = {"request": requests[0], "whole_geometry_all_actual_eta_closed": False,
               "fresh_complete_low_eta_result": deepcopy(low)}
    children = tuple({"request": request, "whole_geometry_all_actual_eta_closed": False,
                      "fresh_complete_low_eta_result": deepcopy(low)} for request in requests[1:])
    result = {"root_index": 200, "whole_parent_request": requests[0], "all_five_exact_requests": requests,
        "all_five_DIRECT_high_pairs": tuple((request, None) for request in requests),
        "initial_parent_complete_join": initial, "all_four_complete_child_joins_if_parent_UNKNOWN": children,
        "summary": {"whole_parent_all_actual_eta_closed": False}, "conclusions": {"unrestricted_C4_proved": False}}
    snapshot = deepcopy(result)
    projected = project_complete_parent_result(result)
    require(result == snapshot and projected is not result, "No inplace source mutation")
    checks = 1
    for old, new in zip((initial,) + children,
                        (projected["initial_parent_complete_join"],) + projected["all_four_complete_child_joins_if_parent_UNKNOWN"]):
        old_low, new_low = old["fresh_complete_low_eta_result"], new["fresh_complete_low_eta_result"]
        require(len(new_low["cells"]) == 16 and new_low["unresolved_eta_cell_indices"] == tuple(range(16))
                and new_low["closed_eta_cover"] == old_low["closed_eta_cover"], "All UNKNOWN cells/scopes retained")
        for old_cell, new_cell in zip(old_low["cells"], new_low["cells"]):
            old_row, new_row = old_cell["worst_complete_H_row"], new_cell["worst_complete_H_row"]
            require(set(new_row) == set(old_row) - set(ALTERNATIVE_PROOF_KEYS)
                    and all(new_row[key] == old_row[key] for key in new_row), "ONLY3duplicates dropped, fullselectedproof same")
        checks += 1
    require(projected["all_five_exact_requests"] == requests
            and projected["all_five_DIRECT_high_pairs"] == result["all_five_DIRECT_high_pairs"]
            and projected["summary"] == result["summary"], "ALL5 high/scopes and parent failure unchanged")
    checks += 1
    direct = dict(result, initial_parent_complete_join=dict(initial, whole_geometry_all_actual_eta_closed=True,
                  fresh_complete_low_eta_result=None), all_four_complete_child_joins_if_parent_UNKNOWN=())
    require(project_complete_parent_result(direct)["initial_parent_complete_join"]["fresh_complete_low_eta_result"] is None,
            "Empty/cut0/direct-parent no-low shape retained, no phantom children")
    checks += 1
    return {"status": "TINY_STRUCTURAL_PARENT_PROJECTION_ONLY", "exact_checks": checks,
        "synthetic_flags_or_JSON_prove_CDF": False, "CF_cache_Cantelli_Gamma_radius_CDF_or_parent_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
