"""Fresh normalized WHOLE-box finite Q3 centers; NO CDF/eta acceptance.

API fresh_normalized_center_table(rectangle, cache, guard) first DIRECTLY
calls the audited correctly-scaled cached.fresh_cached_center_table with
contact Taylor enabled. Thus its TRUE irrational nominal CF and nominal
raw center, whole-box raw center, and ACTUAL-reference modulus caps are
freshly computed mathematical bounds. The cache must itself come from a
DIRECT fresh audited quadrature builder. Types/pins/fields/status/JSON do
not substitute for either of these mathematical provenance premises.

For C_H(a,b)=1+2 Re sum kappa_H*g_Q(a,b)^4-2 Phi(H/2), this module
rebuilds SAME-root rational-above-nominal contact derivative bundles,
sums their signed gradient blocks across frequencies BEFORE taking an
upper, and uses the existing raw-center Hessian envelope to shift the
gradients to the TRUE nominal contact pair n. BOTH reflected C_H use
canonical a,b derivatives (not swapped because g was conjugated).
Neither a rational-bar CF nor a quadrature cache replaces C_H(n).
The legacy mis-scaled generic CF and high-level old CF rebuild APIs are
never called; only the audited correctly-scaled direct table and pure
fresh derivative/Hessian/signed-sum helpers are used.

Let T=4097/10000, rho_Q(a,b)=(a^2+b^2)/(a+b), and let z be the rational
upper endpoints of the TRUE nominal contact brackets. The normalized
supporting-plane helper proves on positive contacts

 rho_Q(x)>=rho_Q(z)+grad rho_Q(z).(n-z)+grad rho_Q(z).(x-n).

Its moment Hessian is PSD. Combining this lower plane with the freshly
proved signed Taylor upper for C_H gives a WHOLE-box bound on
 C_H(Q_actual)-T*rho_Q_actual.
The constant root shift -T*grad rho_Q(z).(n-z) retains its correct sign;
the linear gradient is grad C_H(n)-T*grad rho_Q(z). ONLY the existing
raw-center Hessian enters the quadratic remainder; NO absolute rho
Hessian cost is added. Actual/true-nominal/rational-upper references are
probabilities on the convex contact domain b>=a, ab>=1. Hessian bounds
are needed on their segments, not at every interval-box corner.

Independently the old fresh WHOLE-box raw upper C_upper and fresh
rho_Q_lower prove C_H(Q_actual)-T*rho_Q_actual<=C_upper-T*rho_Q_lower.
After separate outward ceilings, the scalar MIN of these TWO complete
WHOLE-box bounds is valid. It is not a coefficientwise minimum or a
pointwise geometric winner extrapolated to the box. The original raw
center/modulus/CF fields remain untouched. Each row gains only normalized
center fields and exact gradient diagnostics; worst normalized upper is
recorded separately from the old worst raw upper.

There is NO physical quadrature/H reserve, original-P transfer, eta-cell
decision, CDF comparison, tail coverage, root coverage or C4 theorem here.
A later consumer must add its proved COMPLETE transfer and ONE physical
reserve of each type, then subtract T*eta, since rho_P=rho_Q_actual+eta.
It must not subtract T*rho_Q_lower AGAIN from this normalized center.
Likewise it must not quietly relabel a normalized bound as a raw Q center.

SOURCE-only until explicitly authorized. Dormant tiny tests below invoke
ONLY scalar polynomial/supporting-plane arithmetic, no cache/CF/table
producer. No import-time computation, CLI producer, replay or file writes.
The caller supplies its own cooperative guard to every heavy loop. Frozen
dependency hashes are integrity checks only; all older files preserved.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path

import n4_Q3_fresh_cached_low_eta_box_leaf_2026_10_09 as cached
import n4_Q3_normalized_contact_center_supporting_plane_2026_10_09 as supporting_plane

quad, center = cached.quadrature, cached.center
SCALE, TARGET, require = cached.SCALE, cached.TARGET, cached.require
CACHED_PIN = "4bf4a90a3eae9ed88b8a9e02d27e02ef53d4bef7b836fe426bf3dcfa49c3bd9f"
QUAD_PIN = "6eca3207f22f510752a3939491fbfa1ba883db7e1a0dfad8608f3db4655b904e"
SUPPORTING_PLANE_PIN = "23d4ae257daabba3131e2644bfcd22bad752901d6ccbb66ae4ec0d1b11fbfb1b"


def source_drift_check():
    """Frozen dependency integrity; never a mathematical-bound premise."""
    require(SCALE == supporting_plane.SCALE and TARGET == supporting_plane.DEFAULT_TARGET,
            "Same exact fixed-point scale and normalized target")
    for module, pin in ((cached, CACHED_PIN), (quad, QUAD_PIN),
                        (supporting_plane, SUPPORTING_PLANE_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen source drift: " + Path(module.__file__).name)


def normalized_row_upper(row, nominal, box, a_bar, b_bar,
                         true_gradient_a_int, true_gradient_b_int, hessian):
    """Two complete bounds, under DIRECT fresh nominal/raw/gradient premises.

    Returns additional normalized fields; it never mutates raw/CF data.
    This is a pure mathematical-precondition consumer, not a JSON importer.
    """
    require(type(row) is dict and type(row.get("nominal_raw_Q_center_upper_int")) is int
            and type(row.get("raw_Q_center_upper_int")) is int,
            "TRUE nominal and WHOLE-box raw upper fixed-point integers")
    rho_lower = box.get("rhoQ_lo")
    require(type(rho_lower) is F and rho_lower >= 1,
            "Fresh WHOLE-box rho_Q lower, not a nominal moment substitution")
    result = supporting_plane.normalized_contact_taylor_upper_int(
        row["nominal_raw_Q_center_upper_int"], true_gradient_a_int, true_gradient_b_int,
        nominal["a_bracket"], nominal["b_bracket"], box["a_bracket"], box["b_bracket"],
        (a_bar, b_bar), hessian, target=TARGET, scale=SCALE)
    joint = result["raw_minus_target_rhoQ_upper_int"]
    separate = supporting_plane.ceil_scaled(
        F(row["raw_Q_center_upper_int"], SCALE) - TARGET * rho_lower, SCALE)
    selected = min(joint, separate)
    require(type(joint) is int and type(separate) is int and selected <= separate,
            "Scalar intersection of TWO complete normalized WHOLE-box uppers")
    return {"raw_minus_target_rhoQ_upper_int": selected,
        "raw_minus_target_rhoQ_supporting_plane_upper_int": joint,
        "raw_minus_target_rhoQ_separate_lower_upper_int": separate,
        "normalized_center_selected_bound": "SUPPORTING_PLANE" if joint < separate else "SEPARATE_RHO_LOWER",
        "true_nominal_raw_center_gradient_a_interval_int": tuple(true_gradient_a_int),
        "true_nominal_raw_center_gradient_b_interval_int": tuple(true_gradient_b_int)}


def fresh_normalized_center_table(rectangle, cache, guard):
    """Fresh full center table plus normalized fields; no CDF/eta decision.

    cache's mathematical bounds require the DIRECT fresh audited builder.
    guard is provided by the coordinating job, not an import-time monitor.
    """
    require(callable(guard), "Caller-supplied cooperative guard")
    guard()
    source_drift_check()
    quad.validate_preverified_fresh_cache(cache)
    table = cached.fresh_cached_center_table(rectangle, cache, True, guard)
    inputs = center.canonical_inputs(table, rectangle, cache.N, cache.H_grid)
    box, nominal, bridge, N, H_grid, ai, bi, a_bar, b_bar, da, db, ea, eb = inputs
    require(N == 256 and tuple(H_grid) == tuple(cache.H_grid),
            "Same complete physical N256/H grid and BOTH reflections")
    blocks = []
    for item in table["frequency_data"]:
        guard()
        bundle = quad.fresh_per_root_derivative_bundle(
            item["q"], a_bar, b_bar, item["kernel_rectangle"])
        require(bundle["q"] == item["q"] and bundle["a_bar"] == a_bar
                and bundle["b_bar"] == b_bar,
                "Fresh derivative bundle for THIS SAME nominal root only")
        blocks.append(bundle["signed_center_blocks"])
    hessian = center.center_hessian_majorants(table["frequency_data"], ai, bi)
    indexed = {(row["orientation"], row["H"]): row for row in table["rows"]}
    snapshots = {key: (row["nominal_raw_Q_center_upper_int"], row["raw_Q_center_upper_int"])
                 for key, row in indexed.items()}
    # There is no new nominal CF evaluation at rational z in this path.
    for H in H_grid:
        guard()
        gradients = quad.sum_signed_gradient_blocks_with_phases(blocks, cache.phases_at(H), guard)
        for orientation in (1, -1):
            row = indexed[(orientation, H)]
            ga, gb = center.expand_true_nominal_gradient(
                *gradients[orientation], ea, eb, hessian)
            row.update(normalized_row_upper(row, nominal, box, a_bar, b_bar, ga, gb, hessian))
            require((row["nominal_raw_Q_center_upper_int"], row["raw_Q_center_upper_int"])
                    == snapshots[(orientation, H)], "Original TRUE nominal/raw center fields UNCHANGED")
    worst = max(table["rows"], key=lambda row: row["raw_minus_target_rhoQ_upper_int"])
    rho_bar, rho_gradient, _ = supporting_plane.moment_value_gradient_hessian(a_bar, b_bar)
    table["metadata"]["normalized_contact_center"] = {
        "target": TARGET, "all_H_rows_both_orientations": len(table["rows"]),
        "worst_raw_minus_target_rhoQ_upper_int": worst["raw_minus_target_rhoQ_upper_int"],
        "worst_normalized_row_labels": (worst["orientation"], worst["H"]),
        "supporting_plane_selected_rows": sum(row["normalized_center_selected_bound"] == "SUPPORTING_PLANE"
                                              for row in table["rows"]),
        "rational_supporting_plane_contacts": (a_bar, b_bar),
        "rho_bar_exact": rho_bar, "rho_gradient_bar_exact": rho_gradient,
        "true_nominal_root_shift_bounds": (ea, eb),
        "actual_minus_true_nominal_contact_intervals": (da, db),
        "uniform_raw_center_Hessian_abs_bounds": hessian,
        "rho_Hessian_absolute_cost_added": F(0),
        "signed_frequency_sum_before_upper": True,
        "true_irrational_nominal_CF_and_raw_center_retained": True,
        "canonical_gradient_order_for_both_reflections": ("a", "b"),
        "old_actual_reference_modulus_and_raw_center_fields_unchanged": True,
        "physical_quadrature_H_reserves_or_eta_transfer_added": False,
        "CDF_eta_or_global_coverage_acceptance_computed": False}
    files = (Path(__file__), Path(cached.__file__), Path(quad.__file__),
        Path(supporting_plane.__file__), Path(cached.previous.__file__),
        Path(center.__file__), Path(cached.radial.__file__), Path(center.derivatives.__file__),
        Path(cached.geometry.__file__), Path(cached.previous.geometry_factory.__file__),
        Path(cached.geometry.reference_bridge.__file__), Path(cached.arithmetic.__file__),
        Path(cached.integer.__file__), Path(cached.previous.resources.__file__))
    table["metadata"]["normalized_contact_center_source_pins_integrity_only"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    source_drift_check()
    guard()
    return table


def self_tests():
    """Dormant scalar-only regressions; NEVER calls fresh center/cache builder."""
    checks = 0
    nominal = {"a_bracket": (SCALE, SCALE), "b_bracket": (SCALE, SCALE)}
    # C(a,b)=T*rho(a,b): raw-minus-target-moment is exactly zero.
    # Unit-contact nominal has rho=1, grad rho=(1/2,1/2).
    hessian = (TARGET / 2, TARGET / 2, TARGET / 2)
    center_int = supporting_plane.ceil_scaled(TARGET, SCALE)
    ga = gb = (supporting_plane.ceil_scaled(TARGET / 2, SCALE),) * 2
    row = {"nominal_raw_Q_center_upper_int": center_int, "raw_Q_center_upper_int": center_int}
    box = dict(nominal, rhoQ_lo=F(1))
    added = normalized_row_upper(row, nominal, box, F(1), F(1), ga, gb, hessian)
    require(F(added["raw_minus_target_rhoQ_upper_int"], SCALE) >= 0
            and added["raw_minus_target_rhoQ_upper_int"] <= 1,
            "Exact zero-width normalization, no double rho subtraction")
    require(row == {"nominal_raw_Q_center_upper_int": center_int,
                    "raw_Q_center_upper_int": center_int}, "Pure row helper leaves raw fields unchanged")
    checks += 2
    # C linear and rho convex: the normalized signed gradients cancel at
    # the nominal reference, unlike an independently minimized rho.
    box = {"a_bracket": (SCALE, 11 * SCALE // 10),
           "b_bracket": (SCALE, 11 * SCALE // 10), "rhoQ_lo": F(1)}
    row = {"nominal_raw_Q_center_upper_int": center_int,
           "raw_Q_center_upper_int": center_int + supporting_plane.ceil_scaled(TARGET / 10, SCALE)}
    added = normalized_row_upper(row, nominal, box, F(1), F(1), ga, gb, (F(0), F(0), F(0)))
    require(added["raw_minus_target_rhoQ_supporting_plane_upper_int"]
            < added["raw_minus_target_rhoQ_separate_lower_upper_int"],
            "Signed correlated normalization may beat separate rho lower")
    checks += 1
    # A safe negative raw upper stays signed after normalization/minimum.
    row = {"nominal_raw_Q_center_upper_int": -SCALE, "raw_Q_center_upper_int": -SCALE}
    box = dict(nominal, rhoQ_lo=F(1))
    added = normalized_row_upper(row, nominal, box, F(1), F(1), (0, 0), (0, 0), (F(0), F(0), F(0)))
    require(added["raw_minus_target_rhoQ_upper_int"] < -SCALE,
            "No clipping signed normalized upper to zero")
    checks += 1
    require(added["raw_minus_target_rhoQ_upper_int"]
            <= added["raw_minus_target_rhoQ_separate_lower_upper_int"],
            "Complete scalar intersection never weakens old normalized bound")
    checks += 1
    rejected = False
    try:
        normalized_row_upper({"nominal_raw_Q_center_upper_int": F(0), "raw_Q_center_upper_int": 0},
            nominal, box, F(1), F(1), (0, 0), (0, 0), (F(0), F(0), F(0)))
    except RuntimeError:
        rejected = True
    require(rejected, "Physical Fraction cannot masquerade as fixed-point raw integer")
    checks += 1
    return {"status": "TINY_NORMALIZED_CENTER_SCALAR_TESTS_ONLY", "exact_checks": checks,
            "fresh_cache_CF_center_table_or_CDF_producer_called": False,
            "unrestricted_C4_proved": False}
