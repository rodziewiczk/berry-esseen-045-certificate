"""NEW exact-LCM radius compiler optimization and refined H-curvature API.

The frozen10e helper and every earlier source remain unchanged. All
response-cache/physical-contact/norm/price math is EXACTLY its theorem.
Only candidate eligibility, endpoint signs and midpoint selection are
changed to equivalent integer comparisons. No table globals are patched.
The fast actual_response_norm_uppers API is an unchanged alias of10e;
it still computes no finite-price/pole grid, CF/A1/Gamma/CDF producer.

For the SAME exact LCM D of SCALE and normalized intercept denominators,
write Ai=D*A and Si=(D/SCALE)*S_upper_int, both integers. Then
 A+eta*S_upper_int/SCALE = (Ai*eta.denominator+eta.numerator*Si)
                         /(D*eta.denominator).
The denominator is strictly positive. WHOLE-cell eligibility therefore
uses the two integer numerator signs, not two new Fraction expressions
for every candidate/cell. The midpoint objective uses the SAME integer
numerator and SAME candidate order/strict tie comparison as frozen f5.
Convert endpoint numerators to Fraction ONLY when storing a negative
conditional signal. Physical A,S/prices, signed values, exact row/q
labels and every selected price tuple remain unchanged. Negative one-
face signals are not whole-cell emptiness; MAX(two upper values)<0 is
the strict complete empty test. Equality and independent fallbacks stay.

The old loop has256*16*539 eligibility checks, each with two Fraction
endpoint expressions. This source removes that repeated Fraction work;
it does NOT claim runtime or acceptance before an authorized fresh run.
No mathematical or numeric old receipt is used as an input. Inputs
must be the DIRECT fresh correct A1V2 object, including its unchanged
RAW nominal cache with HG tail/y mesh ONCE. Complete signed price-pole
suprema are freshly rebuilt using f5 PURE helpers. No old bad CF entry.

Optional PURE compact_refined_H_curvature takes that SAME original
table and DIRECT freshly proved norm-radius output. It augments only an
independent curvature-frequency list: TRUE actual-reference moduli and
exact q are unchanged. The audited6d whole_cell_radius_upper selects
MIN of COMPLETE endpoint MAXES among whole-cell nonnegative affine
models. Adding models therefore can only lower that radius. Actual-P
continuous CF fill remains3/(2N); kernel integral bounds are unchanged.
Hence B=36 sum(cell kernel weights*pbar^4) cannot increase. Use the SAME
two outward ceilings: B_int=CEIL(S*B), H_int=CEIL(S*h^2*(B_int/S+1/4)/16).
They remain complete and monotone. This REPLACES one physical H reserve;
it adds neither a second H reserve nor a new frequency quadrature term.
Never supply added radius labels to E29's old ABS-count routine.

No CDF/eta/controller acceptance occurs here. Negative slopes are not
clipped, no original finite-atom/density/M4 axiom is added, and no full
root/C4 conclusion is asserted. Caller owns its cooperative guard.
Pure Fraction/int definitions, dormant tiny algebra tests only, no CLI,
file writes, import-time jobs or runtime producer calls. Source hashes
are integrity only, not analytic provenance. Frozen legacy pins preserved.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from math import lcm
from pathlib import Path

import n4_Q3_fresh_common_nu_modulus_radius_models_2026_10_09 as previous
import n4_frequency_local_physical_H_curvature_2026_10_09 as curvature

price, integer = previous.price, previous.integer
SCALE, require = previous.SCALE, previous.require
RADIUS, Y_STEP, Y_NODES, PRICE_ORDER = previous.RADIUS, previous.Y_STEP, previous.Y_NODES, previous.PRICE_ORDER
PREVIOUS_PIN = "10e0392d347bf3aefeffedc5a861ee80d5dd5162b6e32b6697c2998100276456"
CURVATURE_PIN = "6d0c5f1142016721f261bb63715788c21c62b6cd152a1f2538db38cf0e86aa5b"

# Aliases are PURE definitions, not wrappers that invoke old producers.
actual_response_norm_uppers = previous.actual_response_norm_uppers
actual_response_RAW_column = previous.actual_response_RAW_column
normalized_actual_response_column = previous.normalized_actual_response_column
checked_RAW_cache = previous.checked_RAW_cache
contact_displacements = previous.contact_displacements
physical_model = previous.physical_model
independent_models = previous.independent_models
radius_value = previous.radius_value
nonnegative_models_for_closed_cell = previous.nonnegative_models_for_closed_cell
as_transfer_models = previous.as_transfer_models


def source_drift_check():
    previous.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (curvature, CURVATURE_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen PURE arithmetic integrity, not numeric bound truth")
    require(SCALE == curvature.SCALE, "Same physical fixed-point units")


def exact_LCM_coefficients(A, S_upper_int, denominator):
    require(type(A) is F and A >= 0 and type(S_upper_int) is int
            and type(denominator) is int and denominator > 0
            and denominator % SCALE == 0 and denominator % A.denominator == 0,
            "Exact normalized coefficients at the SAME positive common LCM")
    return A.numerator * (denominator // A.denominator), S_upper_int * (denominator // SCALE)


def LCM_endpoint_numerator(A_int, S_factor, eta):
    require(type(A_int) is type(S_factor) is int and type(eta) is F and eta >= 0,
            "Exact integer affine coefficients/nonnegative eta")
    return A_int * eta.denominator + eta.numerator * S_factor


def exact_LCM_midpoint_choice(candidates, midpoint):
    require(candidates and type(midpoint) is F and midpoint >= 0,
            "Ordered complete exact candidates and eta midpoint")
    best = None
    for index, candidate in enumerate(candidates):
        value = LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], midpoint)
        if best is None or value < best[0]:
            best = value, index
    return best[1]


def compute_verified_modulus_radius_models(table, eta_cells, guard):
    """FRESH10e mathematical bounds with EXACT equivalent integer selection."""
    require(callable(guard), "Caller-owned cooperative time/256MiB budget")
    guard()
    source_drift_check()
    box, nominal, q_grid, H_grid, eta_cells = price.checked_preverified_A1_scope(table, eta_cells)
    cache = checked_RAW_cache(table, nominal, q_grid)
    displacements = contact_displacements(box, nominal)
    offsets, offset_metadata = {}, {}
    for name in ("a", "b"):
        offsets[name], offset_metadata[name] = price.whole_contact_price_offsets(box[name + "_bracket"], guard)
    intercepts, denominator = {}, SCALE
    for it, tau in enumerate(price.TAUS):
        for ip, zp in enumerate(price.ZETAS):
            for im, zm in enumerate(price.ZETAS):
                A = box["p0_hi"] * tau + box["u_hi"] * (zp + zm)
                intercepts[it, ip, im] = A
                denominator = lcm(denominator, A.denominator)
    A_ints = {key: A.numerator * (denominator // A.denominator) for key, A in intercepts.items()}
    S_multiplier = denominator // SCALE
    frequencies, negative_signals = [], []
    for q_index, q in enumerate(q_grid):
        guard()
        columns, column_metadata = {}, {}
        for name in ("a", "b"):
            columns[name], column_metadata[name] = normalized_actual_response_column(
                cache[name + "_cell_modulus_upper_int"], q_index, q, displacements[name])
        plus = price.tag_supremum_grid(columns["b"], offsets["b"], guard)
        minus = price.tag_supremum_grid(columns["a"], offsets["a"], guard)
        candidates = []
        for it, tau in enumerate(price.TAUS):
            for ip, zp in enumerate(price.ZETAS):
                sp, tp, activep = plus[it][ip]
                for im, zm in enumerate(price.ZETAS):
                    sm, tm, activem = minus[it][im]
                    S = max(sp, sm)
                    candidates.append({"A": intercepts[it, ip, im], "S_upper_int": S,
                        "prices": price.checked_prices((tau, zp, zm, tp, tm)),
                        "positive_sup_upper_int": sp, "negative_sup_upper_int": sm,
                        "positive_active_cell": activep, "negative_active_cell": activem,
                        "_A_LCM_int": A_ints[it, ip, im], "_S_LCM_factor": S * S_multiplier})
        require(len(candidates) == len(price.TAUS) * len(price.ZETAS) ** 2,
                "Every complete price combination, original10e candidate order unchanged")
        zero = next(candidate for candidate in candidates if candidate["prices"] == (F(0),) * 5)
        require(zero["A"] == 0 and zero["S_upper_int"] >= 0,
                "Zero-price nonnegative response remains valid at eta0/all eta")
        selected = {zero["prices"]: dict(zero, selected_eta_cell_indices=[],
                                          unrestricted_midpoint_eta_cell_indices=[])}
        for cell_index, (L, U) in enumerate(eta_cells):
            guard()
            midpoint = (L + U) / 2
            winner = candidates[exact_LCM_midpoint_choice(candidates, midpoint)]
            endpoint_numerators = tuple(LCM_endpoint_numerator(
                winner["_A_LCM_int"], winner["_S_LCM_factor"], eta) for eta in (L, U))
            if min(endpoint_numerators) < 0:
                endpoint_values = tuple(F(value, denominator * eta.denominator)
                                        for value, eta in zip(endpoint_numerators, (L, U)))
                negative_signals.append({"q_index": q_index, "eta_cell_index": cell_index,
                    "normalized_endpoint_uppers": endpoint_values, "normalized_prices": winner["prices"],
                    "whole_closed_cell_proved_empty_by_THIS_model": max(endpoint_numerators) < 0,
                    "zero_radius_substituted": False})
            eligible = [candidate for candidate in candidates if min(
                LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], L),
                LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], U)) >= 0]
            require(eligible, "Zero-price remains nonnegative on both WHOLE-cell faces")
            safe = eligible[exact_LCM_midpoint_choice(eligible, midpoint)]
            for candidate, key in ((winner, "unrestricted_midpoint_eta_cell_indices"),
                                   (safe, "selected_eta_cell_indices")):
                model = selected.setdefault(candidate["prices"], dict(candidate,
                    selected_eta_cell_indices=[], unrestricted_midpoint_eta_cell_indices=[]))
                require(model["A"] == candidate["A"] and model["S_upper_int"] == candidate["S_upper_int"],
                        "FULL tuple only, identical signed coefficient semantics")
                model[key].append(cell_index)
        models = []
        for index, prices in enumerate(sorted(selected)):
            model = physical_model(selected[prices], q, index)
            require(model["A"] == box["p0_hi"] * model["prices"][0]
                    + box["u_hi"] * (model["prices"][1] + model["prices"][2]),
                    "Unchanged exact PHYSICAL q^3 budget/price scaling")
            models.append(model)
        actual_modulus_int = table["frequency_data"][q_index]["g_actual_modulus_upper_int"]
        require(type(actual_modulus_int) is int and 0 <= actual_modulus_int <= SCALE,
                "Unchanged TRUE actual-reference modulus")
        independents = independent_models(q, F(actual_modulus_int, SCALE), box)
        frequency = {"q": q, "q_index": q_index, "models": tuple(models) + independents,
            "five_budget_models": tuple(models), "independent_models": independents,
            "contact_motion_and_cube_rounding": column_metadata}
        for L, U in eta_cells:
            require(nonnegative_models_for_closed_cell(frequency, L, U), "Independent R2 fallbacks remain")
        frequencies.append(frequency)
    source_drift_check()
    guard()
    files = (Path(__file__), Path(previous.__file__), Path(curvature.__file__), Path(price.__file__),
        Path(price.A1_builder.__file__), Path(price.base.__file__), Path(price.point.__file__),
        Path(integer.__file__), Path(price.cached.geometry.__file__),
        Path(price.cached.previous.geometry_factory.__file__))
    # All numerical/model metadata fields have the SAME10e meanings/values.
    # Only source-integrity closure differs because this is a NEW source.
    return {"scale": SCALE, "N": table["N"], "box_geometry": box, "nominal_root_data": nominal,
        "q_grid": q_grid, "eta_cells": eta_cells, "frequency_models": frequencies,
        "conditional_negative_radius_signals": tuple(negative_signals),
        "metadata": {"H_grid": H_grid, "price_order": PRICE_ORDER,
            "physical_A_S_prices_scaled_by_positive_exact_q_cubic": True,
            "S_upper_int_is_extra_upward_physical_rounding_S_fraction_is_exact_model": True,
            "normalized_price_grids": (price.TAUS, price.ZETAS, price.THETAS),
            "physical_contact_displacement_upper": displacements,
            "actual_contact_price_metadata": offset_metadata,
            "exact_normalized_objective_LCM_denominator": denominator,
            "RAW_cache_modified_or_HG_tail_y_mesh_repeated": False,
            "r_c_contact_derivative_cache_claimed": False,
            "theta_MIN_after_COMPLETE_MAX_and_global_inverse_size_budget": True,
            "signed_S_clipped_or_negative_upper_replaced_by_zero": False,
            "one_norm_orientation_covers_both_reflections_by_contact_price_swap": True,
            "selected_eta_indices_are_diagnostics_ALL_models_valid_whole_feasible_fibre": True,
            "independent_cube_mass_unit_routes_retained": True,
            "H_summed_Gamma_used_as_modulus_radius": False,
            "CF_A1_Gamma_CDF_or_controller_producer_called": False,
            "conditional_CDF_or_full_root_C4_proved": False,
            "DIRECT_fresh_cache_response_truth_is_external_mathematical_premise": True,
            "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                         for path in files}}}


def same_radius_math_except_new_source_pins(old, new):
    """Exact comparison helper ONLY; no numeric receipt/proof importer."""
    left, right = dict(old), dict(new)
    left["metadata"] = {k: v for k, v in old["metadata"].items() if k != "source_pins_integrity_only"}
    right["metadata"] = {k: v for k, v in new["metadata"].items() if k != "source_pins_integrity_only"}
    return left == right


def compact_refined_H_curvature(table, fresh_radius, eta_interval, H_step,
                               mode="response_norm", guard=None):
    """PURE fresh-bound prerequisite; complete endpoint MAX/MIN, not E29."""
    require(callable(guard), "Externally owned cooperative guard")
    guard()
    source_drift_check()
    require(type(mode) is str and mode in ("response_norm", "five_budget")
            and type(H_step) is F and H_step > 0,
            "Declared physical radius mode/H spacing")
    box, nominal, q_grid, H_grid, _ = price.checked_preverified_A1_scope(table, (tuple(eta_interval),))
    require(tuple(H_grid) == price.cached.quadrature.complete_H_grid(H_step), "SAME complete H scope")
    require(type(fresh_radius["scale"]) is type(fresh_radius["N"]) is int
            and fresh_radius["scale"] == SCALE and fresh_radius["N"] == table["N"] == 256
            and fresh_radius["box_geometry"] == box and fresh_radius["nominal_root_data"] == nominal
            and tuple(fresh_radius["q_grid"]) == q_grid
            and tuple(fresh_radius["metadata"]["H_grid"]) == H_grid,
            "SAME DIRECT fresh actual geometry/nominal/q/H radius bounds")
    source = fresh_radius["frequency_data"] if mode == "response_norm" else fresh_radius["frequency_models"]
    require(len(source) == len(table["frequency_data"]) == 256, "ALL exact q radii, not a prefix")
    if mode == "five_budget":
        require(fresh_radius["metadata"]["price_order"] == PRICE_ORDER
                and fresh_radius["metadata"]["physical_A_S_prices_scaled_by_positive_exact_q_cubic"] is True,
                "DIRECT physical, not normalized, five-price model meanings")
    frequencies = []
    for j, (original, added) in enumerate(zip(table["frequency_data"], source)):
        guard()
        require(type(added["q_index"]) is int and added["q_index"] == j
                and type(added["q"]) is F and added["q"] == q_grid[j], "SAME q-specific proven models")
        a_int = original["g_actual_modulus_upper_int"]
        require(type(a_int) is int and 0 <= a_int <= SCALE, "UNCHANGED actual-Q modulus at SCALE")
        models = tuple((model["A"], model["S"], model["label"]) for model in
                       independent_models(q_grid[j], F(a_int, SCALE), box))
        if mode == "response_norm":
            slope = added["actual_response_norm_upper_exact"]
            require(type(slope) is F and 0 <= slope <= q_grid[j] ** 3 / 6,
                    "Fresh PHYSICAL response slope, no extra normalization")
            extras = ((F(0), slope, "zero_price_response_norm"),)
        else:
            for model in added["five_budget_models"]:
                prices = tuple(model["prices"])
                require(len(prices) == 5 and all(type(value) is F for value in prices)
                        and min(prices[:3]) >= 0
                        and model["A"] == box["p0_hi"] * prices[0]
                            + box["u_hi"] * (prices[1] + prices[2]),
                        "Recomputed PHYSICAL price-budget cost, no guessed q^3 conversion")
            extras = tuple((model["A"], model["S"], "fresh_modulus_" + model["label"])
                           for model in added["five_budget_models"])
            require(extras and all(type(A) is type(S) is F and A >= 0 and type(label) is str
                                   for A, S, label in extras), "Exact signed PHYSICAL whole radius models")
        frequencies.append({"q": q_grid[j], "modulus_upper_int": a_int,
                            "models": tuple(dict.fromkeys(models + extras))})
    bound = curvature.physical_H_curvature_bound(frequencies, tuple(eta_interval), H_step, N=256, scale=SCALE)
    B = bound["J_second_derivative_uppers"]["complete_integral_intersection"]
    B_int = curvature.ceil_scaled(B, SCALE)
    H_int = curvature.ceil_scaled(H_step ** 2 * (F(B_int, SCALE) + F(1, 4)) / 16, SCALE)
    require(F(B_int, SCALE) >= B and F(H_int, SCALE) >= bound["physical_H_reserve"]
            and F(H_int, SCALE) <= F(25, 64) * H_step ** 2 + F(2, SCALE),
            "SAME two outward B/H ceilings on a complete continuous kernel integral")
    source_drift_check()
    guard()
    return {"J_second_derivative_upper_int": B_int, "physical_H_reserve_upper_int": H_int,
        "continuous_frequency_Lipschitz_fill": F(3, 512),
        "continuous_kernel_cell_integral_intersection_sum":
            bound["kernel_weight_sums"]["complete_integral_intersection"],
        "refined_complete_radius_models_used": True, "modulus_radius_mode": mode,
        "physical_H_reserve_is_ONE_REPLACEMENT_not_extra_reserve": True,
        "frequency_quadrature_or_E29_ABS_models_changed": False,
        "CDF_eta_or_controller_acceptance_computed": False}


def self_tests():
    """DORMANT exact LCM equivalence and monotone curvature scalars ONLY."""
    checks = 0
    candidates = [{"A": F(1, 3), "S_upper_int": -SCALE},
                  {"A": F(1, 7), "S_upper_int": SCALE // 2},
                  {"A": F(0), "S_upper_int": SCALE // 10},
                  {"A": F(1, 3), "S_upper_int": -SCALE}]
    D = lcm(SCALE, 3, 7)
    for candidate in candidates:
        Ai, Si = exact_LCM_coefficients(candidate["A"], candidate["S_upper_int"], D)
        candidate.update({"_A_LCM_int": Ai, "_S_LCM_factor": Si})
    for eta in (F(0), F(1, 10), F(1, 3), F(2, 3), F(1)):
        require(exact_LCM_midpoint_choice(candidates, eta)
                == price.exact_midpoint_choice(candidates, eta, D), "Identical ordered midpoint ties/values")
        checks += 1
        for candidate in candidates:
            numerator = LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], eta)
            physical = candidate["A"] + F(candidate["S_upper_int"], SCALE) * eta
            require(F(numerator, D * eta.denominator) == physical
                    and (numerator < 0) == (physical < 0) and (numerator >= 0) == (physical >= 0),
                    "EXACT Fraction endpoint equality and signs including0 and negativeS")
            checks += 1
    L, U = F(1, 10), F(4, 5)
    old_eligible = [candidate for candidate in candidates if min(
        candidate["A"] + F(candidate["S_upper_int"], SCALE) * L,
        candidate["A"] + F(candidate["S_upper_int"], SCALE) * U) >= 0]
    new_eligible = [candidate for candidate in candidates if min(
        LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], L),
        LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], U)) >= 0]
    require(old_eligible == new_eligible, "Identical candidate identities/order, no relaxed endpoint")
    checks += 1
    for old_upper, refined_upper in ((F(1), F(1)), (F(1), F(1, 2)), (F(1, 3), F(1, 4))):
        a, fill = F(1, 5), F(3, 512)
        old_p, new_p = min(F(1), a + old_upper + fill), min(F(1), a + refined_upper + fill)
        old_B, new_B = 6 * old_p ** 4, 6 * new_p ** 4
        old_Bi, new_Bi = curvature.ceil_scaled(old_B), curvature.ceil_scaled(new_B)
        old_Hi = curvature.ceil_scaled(F(1, 64) * (F(old_Bi, SCALE) + F(1, 4)) / 16)
        new_Hi = curvature.ceil_scaled(F(1, 64) * (F(new_Bi, SCALE) + F(1, 4)) / 16)
        require(new_p <= old_p and new_Bi <= old_Bi and new_Hi <= old_Hi,
                "Complete radius MAX/MIN fill and BOTH outward ceilings are monotone")
        checks += 1
    return {"status": "TINY_LCM_RADIUS_EQUIVALENCE_AND_CURVATURE_ALGEBRA_ONLY", "exact_checks": checks,
        "CF_cache_A1_Gamma_real_radius_compiler_CDF_or_global_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
