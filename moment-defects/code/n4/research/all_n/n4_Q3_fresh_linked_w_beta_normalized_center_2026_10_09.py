"""Fresh linked-(w,beta) normalized finite-center wrapper; NO CDF decision.

fresh_normalized_center_table(rectangle,cache,guard) makes exactly ONE
DIRECT call to the audited e5ef fresh normalized-contact builder. That
producer already supplies correctly-scaled TRUE nominal CF/raw centers,
WHOLE-box normalized contact bounds, ACTUAL-reference modulus caps, TRUE
signed C_a(n),C_b(n) intervals for every H/reflection, and its proven raw
contact Hessian envelope. The shared cache must come from the DIRECT fresh
audited quadrature builder. Types/hashes/status/JSON do not establish any
of those mathematical premises.

The existing per-row TRUE signed contact gradients and COMMON contact
Hessian are reused. There is NO second q/CF/gradient/table producer and
no rational-bar replacement of the TRUE nominal baseline. The pure ae6e
linked helper checks the exact rational w,beta midpoint and nominal root
squares/whole-contact envelopes, then gives a complete WHOLE-box upper
of C_H(Q_actual)-T*rhoQ_actual in LINKED parameter coordinates. It retains
signed C_w,C_beta, exact mixed-Cab cancellation and the lower supporting
plane of the jointly convex moment rho(w,beta). ONLY a raw-C Hessian
remainder is charged; no absolute rho-Hessian reserve is added.

The new linked upper is separately CEILED to fixed-point units. Its
scalar MIN with the existing individually valid WHOLE-box normalized
contact upper is another complete upper. This is NOT a coefficientwise
minimum, pointwise winner extrapolation, or independent raw/rho extrema.
Both genuine reflections use canonical a,b,w,beta coordinate derivatives;
they are not swapped merely because a CF was conjugated.

Every row keeps its TRUE nominal/raw center, CF/actual modulus data and
old contact-bound diagnostics, and gains the new linked upper/selection
fields. Its raw_minus_target_rhoQ_upper_int is the complete intersection.
All normalized worst-row metadata is refreshed. The raw center maximum
and normalized maximum are NEVER silently interchanged.

NO original-P transfer, eta-cell decision, physical quadrature/H reserve,
CDF/tail/root coverage, or unrestricted C4 theorem is produced. A later
consumer must add its proved complete raw transfer and ONE reserve of
each type, then subtract T*eta. It must not subtract T*rhoQ again from a
normalized center. Source pins are integrity only; older sources/receipts
remain untouched. The caller supplies a cooperative guard. Dormant tiny
tests below use ONLY scalar synthetic rational laws; no producer or file
write occurs on import or in those tests. No runtime until authorized.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import n4_Q3_fresh_normalized_contact_center_2026_10_09 as contact_center
import n4_Q3_normalized_w_beta_center_taylor_2026_10_09 as linked

SCALE, TARGET, require = contact_center.SCALE, contact_center.TARGET, contact_center.require
CONTACT_CENTER_PIN = "e5ef0b28bf0c91966ac878fdc0ad4130f4571b9a9149736e734004f6bcee7b30"
LINKED_PIN = "ae6e5c4480e53d5c5384a994ecae303dc93d11ea9a2de47d40244a3b29d9a7b9"


def source_drift_check():
    require(SCALE == linked.SCALE and TARGET == linked.DEFAULT_TARGET,
            "Same exact target and declared fixed-point scale")
    for module, pin in ((contact_center, CONTACT_CENTER_PIN), (linked, LINKED_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen source integrity only: " + Path(module.__file__).name)


def linked_row_upper(row, nominal, box, rectangle, contact_hessian):
    """Scalar consumer of DIRECT-FRESH complete row/gradient premises.

    No input schema or source/status flag proves the mathematical bounds.
    This returns new fields without mutating any previous raw/CF fields.
    """
    require(type(row) is dict and type(row.get("nominal_raw_Q_center_upper_int")) is int
            and type(row.get("raw_minus_target_rhoQ_upper_int")) is int,
            "Fresh TRUE nominal raw and old complete normalized fixed integers")
    ga, gb = (row.get("true_nominal_raw_center_gradient_a_interval_int"),
              row.get("true_nominal_raw_center_gradient_b_interval_int"))
    for interval in (ga, gb):
        require(type(interval) in (tuple, list) and len(interval) == 2
                and all(type(value) is int for value in interval) and interval[0] <= interval[1],
                "Fresh TRUE signed raw-contact gradients at the declared scale")
    result = linked.normalized_w_beta_center_taylor_upper_int(
        row["nominal_raw_Q_center_upper_int"], ga, gb, nominal["w"], nominal["beta"],
        nominal["a_bracket"], nominal["b_bracket"], nominal["rhoQ_bracket"],
        rectangle, box["a_bracket"], box["b_bracket"], contact_hessian,
        target=TARGET, scale=SCALE)
    new = result["raw_minus_target_rhoQ_upper_int"]
    old = row["raw_minus_target_rhoQ_upper_int"]
    require(type(new) is int, "Separate signed outward linked fixed-point upper")
    return {"raw_minus_target_rhoQ_old_contact_upper_int": old,
        "raw_minus_target_rhoQ_linked_w_beta_upper_int": new,
        "raw_minus_target_rhoQ_upper_int": min(old, new),
        "linked_w_beta_normalized_center_selected": new < old}


def fresh_normalized_center_table(rectangle, cache, guard):
    """ONE direct complete fresh builder, then cheap linked scalar row bounds."""
    require(callable(guard), "External cooperative guard")
    guard()
    source_drift_check()
    table = contact_center.fresh_normalized_center_table(rectangle, cache, guard)
    require(table["scale"] == SCALE and table["N"] == cache.N
            and tuple(table["metadata"]["H_grid"]) == tuple(cache.H_grid)
            and tuple(table["box_geometry"]["rectangle"]) == tuple(rectangle),
            "SAME fresh geometry and complete cached N/H grid")
    rows, nominal, box = table["rows"], table["nominal_root_data"], table["box_geometry"]
    expected = {(orientation, H) for H in cache.H_grid for orientation in (1, -1)}
    require(len(rows) == len(expected) and {(row["orientation"], row["H"]) for row in rows} == expected,
            "Every declared H and BOTH canonical genuine reflections")
    metadata = table["metadata"]["normalized_contact_center"]
    require(metadata["target"] == TARGET, "Existing normalized table uses SAME target")
    hessian = metadata["uniform_raw_center_Hessian_abs_bounds"]
    old_worst = max(rows, key=lambda row: row["raw_minus_target_rhoQ_upper_int"])
    old_worst_value = old_worst["raw_minus_target_rhoQ_upper_int"]
    old_worst_labels = old_worst["orientation"], old_worst["H"]
    raw_snapshots = {(row["orientation"], row["H"]):
        (row["nominal_raw_Q_center_upper_int"], row["raw_Q_center_upper_int"])
        for row in rows}
    for row in rows:
        guard()
        row.update(linked_row_upper(row, nominal, box, rectangle, hessian))
        require((row["nominal_raw_Q_center_upper_int"], row["raw_Q_center_upper_int"])
                == raw_snapshots[(row["orientation"], row["H"])],
                "Original TRUE nominal and WHOLE raw center fields UNCHANGED")
        require(row["raw_minus_target_rhoQ_upper_int"]
                <= row["raw_minus_target_rhoQ_old_contact_upper_int"],
                "Complete scalar intersection cannot weaken the old normalized bound")
    worst = max(rows, key=lambda row: row["raw_minus_target_rhoQ_upper_int"])
    selected = sum(row["linked_w_beta_normalized_center_selected"] for row in rows)
    metadata.update({
        "worst_raw_minus_target_rhoQ_upper_int": worst["raw_minus_target_rhoQ_upper_int"],
        "worst_normalized_row_labels": (worst["orientation"], worst["H"]),
        "base_contact_supporting_plane_selected_rows_diagnostic_only": metadata["supporting_plane_selected_rows"],
        "linked_w_beta_selected_rows": selected,
        "final_bound_is_complete_contact_linked_scalar_intersection": True})
    table["metadata"]["linked_w_beta_normalized_center"] = {
        "target": TARGET, "all_H_rows_both_orientations": len(rows),
        "old_contact_worst_normalized_upper_int": old_worst_value,
        "old_contact_worst_normalized_row_labels": old_worst_labels,
        "worst_raw_minus_target_rhoQ_upper_int": worst["raw_minus_target_rhoQ_upper_int"],
        "worst_normalized_row_labels": (worst["orientation"], worst["H"]),
        "linked_w_beta_selected_rows": selected,
        "largest_per_row_improvement_int": max(
            row["raw_minus_target_rhoQ_old_contact_upper_int"] - row["raw_minus_target_rhoQ_upper_int"]
            for row in rows),
        "TRUE_signed_contact_gradients_and_Hessian_reused": True,
        "second_CF_frequency_gradient_or_reference_table_producer_called": False,
        "true_nominal_raw_center_CF_and_actual_modulus_fields_unchanged": True,
        "complete_normalized_bounds_intersected_not_coefficients": True,
        "moment_convexity_has_no_absolute_rho_Hessian_cost": True,
        "physical_quad_H_reserves_eta_transfer_or_CDF_decision_added": False}
    table["metadata"]["linked_w_beta_normalized_center_source_pins_integrity_only"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), Path(contact_center.__file__), Path(linked.__file__))}
    source_drift_check()
    guard()
    return table


def self_tests():
    """Dormant SMALL pure row regressions; NEVER invokes a fresh table builder."""
    checks = 0
    rho_bracket = (5 * SCALE // 3, linked.ceil_scaled(F(5, 3), SCALE))
    nominal = {"w": F(1, 2), "beta": F(1, 3), "a_bracket": (SCALE, SCALE),
               "b_bracket": (2 * SCALE, 2 * SCALE), "rhoQ_bracket": rho_bracket}
    point = (F(1, 2), F(1, 2), F(1, 3), F(1, 3))
    box = {"a_bracket": nominal["a_bracket"], "b_bracket": nominal["b_bracket"]}
    exact = F(3) - TARGET * F(5, 3)
    old = linked.ceil_scaled(exact, SCALE)
    row = {"nominal_raw_Q_center_upper_int": 3 * SCALE,
           "raw_Q_center_upper_int": 3 * SCALE,
           "raw_minus_target_rhoQ_upper_int": old,
           "true_nominal_raw_center_gradient_a_interval_int": (2 * SCALE, 2 * SCALE),
           "true_nominal_raw_center_gradient_b_interval_int": (-3 * SCALE, -3 * SCALE)}
    snapshot = dict(row)
    added = linked_row_upper(row, nominal, box, point, (F(0), F(0), F(0)))
    require(added["raw_minus_target_rhoQ_upper_int"] == old,
            "Exact point center normalization; complete old upper intersects root-width enlargement")
    require(row == snapshot, "Pure helper preserves old raw/normalized/gradient fields")
    checks += 2
    rectangle = (F(49, 100), F(51, 100), F(97, 300), F(103, 300))
    box = {"a_bracket": (95 * SCALE // 100, 105 * SCALE // 100),
           "b_bracket": (195 * SCALE // 100, 205 * SCALE // 100)}
    row["raw_Q_center_upper_int"] = linked.ceil_scaled(F(13, 4), SCALE)
    row["raw_minus_target_rhoQ_upper_int"] = linked.ceil_scaled(F(13, 4) - TARGET, SCALE)
    added = linked_row_upper(row, nominal, box, rectangle, (F(0), F(0), F(0)))
    require(added["linked_w_beta_normalized_center_selected"]
            and added["raw_minus_target_rhoQ_upper_int"]
                < added["raw_minus_target_rhoQ_old_contact_upper_int"],
            "Linked signed increments can improve an independently valid whole-contact upper")
    checks += 1
    row["nominal_raw_Q_center_upper_int"] = -SCALE
    row["raw_minus_target_rhoQ_upper_int"] = linked.ceil_scaled(F(-1) - TARGET * F(5, 3), SCALE)
    added = linked_row_upper(row, nominal,
        {"a_bracket": nominal["a_bracket"], "b_bracket": nominal["b_bracket"]},
        point, (F(0), F(0), F(0)))
    require(added["raw_minus_target_rhoQ_upper_int"] < -SCALE,
            "Signed negative complete normalized upper is never clipped")
    checks += 1
    invalid = dict(row, raw_minus_target_rhoQ_upper_int=F(0))
    rejected = False
    try:
        linked_row_upper(invalid, nominal, box, rectangle, (F(0), F(0), F(0)))
    except RuntimeError:
        rejected = True
    require(rejected, "Physical Fraction cannot masquerade as a fixed-point normalized upper")
    checks += 1
    return {"status": "TINY_LINKED_NORMALIZED_CENTER_ROW_TESTS_ONLY", "exact_checks": checks,
            "fresh_CF_cache_gradient_or_center_table_producer_called": False,
            "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
