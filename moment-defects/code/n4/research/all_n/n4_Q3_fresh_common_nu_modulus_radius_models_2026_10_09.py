"""Fresh per-q COMMON-nu modulus radii from DIRECT correct A1V2 RAW cache.

compute_verified_modulus_radius_models(table,eta_cells,guard) consumes
the fresh IN-MEMORY output of the corrected A1V2 producer. The caller
must have DIRECTLY established that producer's true CF/geometry and RAW
nominal response-cell bounds. Schema, flags, source hashes, statuses or
numeric JSON do not prove them. No CF/A1/Gamma/CDF producer is called
here, no old globals/receipts are changed, and nothing runs on import.

Fast API actual_response_norm_uppers(table,guard) computes ONLY the
zero-price whole-response norm, without any pole tables/finite-price
search. It returns a PHYSICAL per-q slope Uq such that
 |delta_q|<=eta*Uq,
Uq=min(q^3/6,max_ALL273_AND_BOTH_TAGS actual_cell_norm_upper).
This is an independent complete affine radius (0,Uq), directly useful
in an R2 consumer. It performs no q^3 normalization, H maximization,
CDF acceptance or mutation of the original frequency/cache data.

Measure-level bound, including zero/contact atoms
------------------------------------------------
For standardized P in the declared box with |X|<=17/4 and eta>0,
nu=W*dP/eta is ONE probability measure on tagged nonzero off-contact
magnitudes. The SAME canonical identities give
 eta E k0<=p0, eta E_tag k2<=u, E_tag k1=0,
where k0=1/(c^2*y),k2=1/(y-c)^2,k1=1/(y-c), plus=b,minus=a.
For each positive q, delta_q=phiP(q)-g_Qactual(q)=eta E r_q.
Therefore |delta_q|<=eta E |r_q|, not abs(an H-summed Gamma).

The supplied cache arrays are RAW SCALE*|r_nom| upper bounds on ALL273
CLOSED y cells, already containing their HG tail and half-cell mesh
ONCE. They are not divided by q^3 and are never modified here. Hermite-
Genocchi gives |r_actual|<=q^3/6 and |partial_c r|<=q^4/12. With the
physical contact displacement Delta between TRUE nominal and whole box,
each actual response cell is bounded by
 min(q^3/6, RAW_nom/SCALE + q^4*Delta/12).
Outward integer movement rounding occurs ONCE, then the response bound
is divided by the positive EXACT q^3 and rounded UP to SCALE. There is
NO second HG tail/mesh, no r_c-cache claim, and no extra q^3 divisor.

For normalized response b_q=|r_actual|/q^3, a fixed canonical tuple
(tau,zeta_plus,zeta_minus,theta_plus,theta_minus), FIRST3 nonnegative,
LAST2 signed, and a complete signed supremum
 S>=sup[b_q-tau*k0-zeta_tag*k2-theta_tag*k1]
give |delta_q|<=q^3*(A+eta*S), A=p0_hi*tau+u_hi*(zeta_plus+zeta_minus).
Pure retained full-cell offsets from f5 use the ACTUAL contact envelope:
k0 LOWER floor, nonnegative tau-cost LOWER floor, and SIGNED concave
two-ray pole maximum UPWARD ceil. For EACH fixed theta take MAX ALL
cells first, THEN MIN theta. Both tags share ONE global tau budget.
All7x7 tag-price combinations are complete bounds; no coefficient min.
At an exact eta-cell midpoint freeze a WHOLE tuple, not pointwise prices.
All emitted models remain valid on the entire feasible eta fibre.

Output A,S are PHYSICAL Fraction radius coefficients: A=q^3*A_normal,
S=q^3*S_normal. Physical prices are q^3 times their normalized prices;
their budget recomputes EXACTLY to physical A. S_upper_int is an OPTIONAL
extra upward rounding of physical S, not the coefficient used by the
exact (A,S,label) transfer models. Normalized fields are labeled separately.
There is no guessed scaling or saved optimizer bound.

Independent cube/mass/unit affine routes are also kept, not replaced:
 eta*q^3/6, M_hi^2*p0_hi*q^2, 1+a_actual(q).
For the mass route, writing the quadratic Hermite interpolant as the
linear Taylor polynomial at c plus beta*(y-c)^2 gives |beta|<=q^2/2
and |exp(iqy)-H(y)|<=q^2*(y-c)^2. Hence |r|<=q^2/y<=M^2*q^2*k0.
The unit route uses the FRESH ACTUAL-reference modulus, never nominal.
At eta0 P=Q3 and delta=0 directly without defining nu; all A>=0 models
remain valid, and the independent cube route is exactly0.

Why one norm orientation is enough
---------------------------------
Conjugation of a signed exponential preserves the response norm. Thus
the physical c=a and c=b norm cells cover both actual signs. Reflection
swaps those two physical sign tags and their price pairs; the budget A,
global maximum S and resulting radius are unchanged. We compile plus=b,
minus=a ONCE with this explicit relabeling argument, NOT by pretending
the unreflected signed A1_H curve equals its reflected version.

Signed slopes and infeasibility
------------------------------
Normalized and physical S are NEVER clipped. A radius upper negative
at an eta value proves conditional impossibility there, since a norm
is nonnegative. It is not a fake zero radius. For use in R2 a model is
frozen only when BOTH closed-cell endpoint values are nonnegative.
The independent cube always supplies such a fallback. A negative value
at ONE endpoint alone does NOT prove the WHOLE cell empty. Only a single
valid affine upper with MAX(endpoint values)<0 excludes that entire
closed cell; equality0 is kept. These necessary scalar signals neither
mask any global controller class nor accept a CDF/root theorem here.

Exact N256/q/ROOT labels, all273 RAW cells, true nominal/actual contact
brackets and declared adjacent closed eta cells are checked. Contact
offsets are built once and responses streamed one q at a time; no H*y*q
or q*price*y tensor is allocated. Caller owns the cooperative time/
256MiB guard. Pure Fraction/int arithmetic, dormant tiny algebra tests
only, no CLI, runtime producer, file writes or unrestricted C4 claim.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from math import lcm
from pathlib import Path

import n4_Q3_fresh_generic_A1_five_price_cell_suprema_2026_10_09 as price

SCALE, require, integer = price.SCALE, price.require, price.integer
RADIUS, Y_STEP, Y_NODES = price.RADIUS, price.Y_STEP, price.Y_NODES
PRICE_ORDER = price.PRICE_ORDER
PRICE_PIN = "f5dc893e0674255cc68981bdb61a2b0ce5586b8a2afbea14f7634cd85c0a5ad4"


def source_drift_check():
    price.source_drift_check()
    require(hashlib.sha256(Path(price.__file__).read_bytes()).hexdigest() == PRICE_PIN,
            "Frozen PURE complete-price arithmetic integrity, not numeric proof provenance")


def checked_RAW_cache(table, nominal, q_grid):
    """Scope only under DIRECT producer mathematical cache-bound premise."""
    cache = table["nom_mod_cache"]
    require(type(cache) is dict and type(cache["scale"]) is int and cache["scale"] == SCALE
            and type(cache["N"]) is int and cache["N"] == table["N"]
            and type(cache["R"]) is F and cache["R"] == RADIUS
            and type(cache["y_step"]) is F and cache["y_step"] == Y_STEP
            and type(cache["HG_degree"]) is int and cache["HG_degree"] == 60,
            "Same exact RAW response grid/domain/HG units")
    require(cache["includes_HG_tail_and_y_mesh"] is True
            and cache["cell_arrays_raw_r_not_normalized"] is True
            and cache["cell_arrays_are_RAW_r_modulus_not_q_cubic_normalized"] is True,
            "Correct DIRECT A1V2 RAW norms already include HG tail/mesh ONCE")
    require(cache["nominal_root_data"] == nominal and tuple(cache["q_grid"]) == q_grid
            and all(type(q) is F for q in cache["q_grid"]), "TRUE nominal and ALL physical q identities")
    for name in ("a", "b"):
        array = cache[name + "_cell_modulus_upper_int"]
        require(type(array) in (tuple, list) and len(array) == Y_NODES
                and all(type(row) in (tuple, list) and len(row) == table["N"]
                        and all(type(value) is int and value >= 0 for value in row) for row in array),
                "ALL273xN nonnegative RAW nominal response-cell norm integers")
    return cache


def contact_displacements(box, nominal):
    result = {}
    for name in ("a", "b"):
        al, ah = box[name + "_bracket"]
        nl, nh = nominal[name + "_bracket"]
        require(all(type(x) is int for x in (al, ah, nl, nh))
                and 0 < al <= nl <= nh <= ah <= RADIUS * SCALE,
                "WHOLE actual and TRUE nominal physical contact containment")
        result[name] = F(max(nh - al, ah - nl), SCALE)
    return result


def actual_response_RAW_column(raw_array, q_index, q, displacement):
    """RAW cache+ONE contact movement, global cubic intersection ONCE."""
    require(type(q) is F and q > 0 and type(displacement) is F and displacement >= 0
            and type(q_index) is int and q_index >= 0, "Exact positive frequency/physical displacement")
    q3 = q ** 3
    cube = integer.ceil_fraction_scaled(q3 / 6)
    movement = integer.ceil_fraction_scaled(q ** 4 * displacement / 12)
    values = []
    for row in raw_array:
        raw = row[q_index]
        require(type(raw) is int and raw >= 0, "Preverified RAW response bound")
        cap = min(cube, raw + movement)
        values.append(cap)
    require(len(values) == Y_NODES and all(type(value) is int and value >= 0 for value in values),
            "Complete RAW actual upper column, never signed A1_H or an extra mesh")
    return tuple(values), {"ONE_contact_motion_upper_int": movement,
                           "global_RAW_cube_upper_int": cube}


def normalized_actual_response_column(raw_array, q_index, q, displacement):
    """ONLY after RAW/S movement: positive EXACT q^3 normalization upward."""
    raw_values, diagnostic = actual_response_RAW_column(raw_array, q_index, q, displacement)
    q3 = q ** 3
    return tuple(integer.ceil_div(value * q3.denominator, q3.numerator)
                 for value in raw_values), diagnostic


def actual_response_norm_uppers(table, guard):
    """FAST zero-price PHYSICAL norm slopes; no finite-price/pole/CF producer."""
    require(callable(guard), "Caller-owned cooperative time/256MiB guard")
    guard()
    source_drift_check()
    box, nominal, q_grid, H_grid, _ = price.checked_preverified_A1_scope(table, ((F(0), F(0)),))
    cache = checked_RAW_cache(table, nominal, q_grid)
    displacements = contact_displacements(box, nominal)
    frequencies = []
    for q_index, q in enumerate(q_grid):
        guard()
        columns, diagnostics = {}, {}
        for name in ("a", "b"):
            columns[name], diagnostics[name] = actual_response_RAW_column(
                cache[name + "_cell_modulus_upper_int"], q_index, q, displacements[name])
        maximum_a, maximum_b = max(columns["a"]), max(columns["b"])
        maximum = max(maximum_a, maximum_b)
        # BOTH alternatives are independently complete whole-cell bounds.
        # Exact cube intersection avoids a harmless extra SCALE rounding.
        bound = min(q ** 3 / 6, F(maximum, SCALE))
        require(0 <= bound <= q ** 3 / 6, "Whole-response physical slope never worse than cube")
        frequencies.append({"q": q, "q_index": q_index,
            "actual_response_norm_upper_exact": bound,
            "actual_response_norm_upper_int": integer.ceil_fraction_scaled(bound),
            "radius_model": (F(0), bound, "zero_price_response_norm"),
            "model": {"kind": "ZERO_PRICE_COMMON_NU_RESPONSE_NORM", "label": "zero_price_response_norm",
                "A": F(0), "S": bound, "S_upper_int": integer.ceil_fraction_scaled(bound)},
            "actual_a_contact_RAW_cell_maximum_upper_int": maximum_a,
            "actual_b_contact_RAW_cell_maximum_upper_int": maximum_b,
            "contact_motion_and_cube_rounding": diagnostics})
    source_drift_check()
    guard()
    files = (Path(__file__), Path(price.__file__), Path(price.A1_builder.__file__), Path(price.base.__file__))
    return {"scale": SCALE, "N": table["N"], "box_geometry": box, "nominal_root_data": nominal,
        "q_grid": q_grid, "frequency_data": tuple(frequencies),
        "metadata": {"H_grid": H_grid, "physical_contact_displacement_upper": displacements,
            "ALL273_y_cells_and_BOTH_physical_contacts_checked": True,
            "raw_arrays_unchanged_and_HG_tail_y_mesh_not_repeated": True,
            "q_cubic_normalization_or_price_offset_tables_computed": False,
            "both_reflections_covered_by_signed_response_conjugation_and_tag_swap": True,
            "eta0_delta_is_exactly_zero_without_nu": True,
            "CDF_or_eta_acceptance_computed": False,
            "CF_A1_Gamma_radius_compiler_or_CDF_producer_called": False,
            "DIRECT_fresh_RAW_cache_truth_is_caller_mathematical_premise": True,
            "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                         for path in files}}}


def radius_value(model, eta):
    require(type(model["A"]) is F and type(model["S"]) is F
            and type(eta) is F and eta >= 0, "PHYSICAL exact affine radius inputs")
    return model["A"] + model["S"] * eta


def physical_model(candidate, q, index):
    """Exact PHYSICAL conversion, retaining signed S and explicit prices."""
    q3 = q ** 3
    A, S = q3 * candidate["A"], q3 * F(candidate["S_upper_int"], SCALE)
    physical_prices = tuple(q3 * value for value in candidate["prices"])
    return {"kind": "COMMON_NU_FIVE_BUDGET", "label": "five_budget_" + str(index),
        "A": A, "S": S, "S_upper_int": integer.ceil_fraction_scaled(S),
        "prices": physical_prices, "normalized_prices": candidate["prices"],
        "normalized_A": candidate["A"], "normalized_S_upper_int": candidate["S_upper_int"],
        "positive_normalized_sup_upper_int": candidate["positive_sup_upper_int"],
        "negative_normalized_sup_upper_int": candidate["negative_sup_upper_int"],
        "positive_active_cell": candidate["positive_active_cell"],
        "negative_active_cell": candidate["negative_active_cell"],
        "selected_eta_cell_indices": tuple(candidate["selected_eta_cell_indices"]),
        "unrestricted_midpoint_eta_cell_indices": tuple(candidate["unrestricted_midpoint_eta_cell_indices"])}


def independent_models(q, actual_modulus, box):
    require(type(q) is F and q > 0 and type(actual_modulus) is F and 0 <= actual_modulus <= 1,
            "Positive physical frequency and preverified ACTUAL-Q modulus")
    M, p0 = F(max(box["a_bracket"][1], box["b_bracket"][1]), SCALE), box["p0_hi"]
    require(M > 0 and type(p0) is F and 0 <= p0 <= 1, "Complete mass-budget geometry")
    triples = ((F(0), q ** 3 / 6, "cube"), (M * M * p0 * q * q, F(0), "mass"),
               (1 + actual_modulus, F(0), "unit"))
    return tuple({"kind": "INDEPENDENT_" + name.upper(), "label": name,
                  "A": A, "S": S, "S_upper_int": integer.ceil_fraction_scaled(S)}
                 for A, S, name in triples)


def nonnegative_models_for_closed_cell(frequency, lower, upper):
    """R2-ready WHOLE models only; no clipping or validity from a winner."""
    require(type(lower) is F and type(upper) is F and 0 <= lower <= upper,
            "Exact nonnegative CLOSED eta cell")
    eligible = tuple(model for model in frequency["models"]
                     if min(radius_value(model, lower), radius_value(model, upper)) >= 0)
    require(eligible, "Independent cube is always a valid WHOLE-cell fallback")
    return eligible


def as_transfer_models(frequency):
    """PHYSICAL (A,S,label) models; caller still filters BOTH endpoints."""
    return tuple((model["A"], model["S"], model["label"]) for model in frequency["models"])


def compute_verified_modulus_radius_models(table, eta_cells, guard):
    """DIRECT fresh mathematical A1V2 cache input; no producer or receipt import."""
    require(callable(guard), "Caller owns cooperative time/256MiB budget")
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
                    candidates.append({"A": intercepts[it, ip, im], "S_upper_int": max(sp, sm),
                        "prices": price.checked_prices((tau, zp, zm, tp, tm)),
                        "positive_sup_upper_int": sp, "negative_sup_upper_int": sm,
                        "positive_active_cell": activep, "negative_active_cell": activem})
        require(len(candidates) == len(price.TAUS) * len(price.ZETAS) ** 2,
                "Complete tag-price combinations share ONE normalized inverse-size price")
        zero = next(candidate for candidate in candidates if candidate["prices"] == (F(0),) * 5)
        require(zero["A"] == 0 and zero["S_upper_int"] >= 0,
                "Zero-priced positive response is valid at eta0 and all nonnegative eta")
        selected = {zero["prices"]: dict(zero, selected_eta_cell_indices=[],
                                          unrestricted_midpoint_eta_cell_indices=[])}
        for cell_index, (L, U) in enumerate(eta_cells):
            guard()
            midpoint = (L + U) / 2
            winner = candidates[price.exact_midpoint_choice(candidates, midpoint, denominator)]
            endpoint_values = (winner["A"] + F(winner["S_upper_int"], SCALE) * L,
                               winner["A"] + F(winner["S_upper_int"], SCALE) * U)
            if min(endpoint_values) < 0:
                negative_signals.append({"q_index": q_index, "eta_cell_index": cell_index,
                    "normalized_endpoint_uppers": endpoint_values, "normalized_prices": winner["prices"],
                    "whole_closed_cell_proved_empty_by_THIS_model": max(endpoint_values) < 0,
                    "zero_radius_substituted": False})
            eligible = [candidate for candidate in candidates
                        if min(candidate["A"] + F(candidate["S_upper_int"], SCALE) * L,
                               candidate["A"] + F(candidate["S_upper_int"], SCALE) * U) >= 0]
            require(eligible, "Zero-price model remains a nonnegative whole-cell norm fallback")
            safe = eligible[price.exact_midpoint_choice(eligible, midpoint, denominator)]
            for candidate, key in ((winner, "unrestricted_midpoint_eta_cell_indices"),
                                   (safe, "selected_eta_cell_indices")):
                model = selected.setdefault(candidate["prices"], dict(candidate,
                    selected_eta_cell_indices=[], unrestricted_midpoint_eta_cell_indices=[]))
                require(model["A"] == candidate["A"] and model["S_upper_int"] == candidate["S_upper_int"],
                        "Dedup FULL tuple only, no mixed A/S/prices")
                model[key].append(cell_index)
        models = []
        for index, prices in enumerate(sorted(selected)):
            candidate = selected[prices]
            model = physical_model(candidate, q, index)
            require(model["A"] == box["p0_hi"] * model["prices"][0]
                    + box["u_hi"] * (model["prices"][1] + model["prices"][2]),
                    "Exact PHYSICAL budget intercept matches q^3-scaled physical prices")
            models.append(model)
        actual_modulus_int = table["frequency_data"][q_index]["g_actual_modulus_upper_int"]
        require(type(actual_modulus_int) is int and 0 <= actual_modulus_int <= SCALE,
                "Fresh actual-reference modulus, never nominal substituted")
        independents = independent_models(q, F(actual_modulus_int, SCALE), box)
        frequency = {"q": q, "q_index": q_index, "models": tuple(models) + independents,
            "five_budget_models": tuple(models), "independent_models": independents,
            "contact_motion_and_cube_rounding": column_metadata}
        for cell_index, (L, U) in enumerate(eta_cells):
            require(nonnegative_models_for_closed_cell(frequency, L, U),
                    "Every declared cell has separate nonnegative R2-ready whole models")
        frequencies.append(frequency)
    source_drift_check()
    guard()
    files = (Path(__file__), Path(price.__file__), Path(price.A1_builder.__file__),
        Path(price.base.__file__), Path(price.point.__file__), Path(integer.__file__),
        Path(price.cached.geometry.__file__), Path(price.cached.previous.geometry_factory.__file__))
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


def self_tests():
    """Dormant tiny units/price/sign regressions ONLY; no real table/compiler."""
    checks = 0
    q = F(3, 512)
    raw = [[integer.ceil_fraction_scaled(q ** 3 / 30)] for _ in range(Y_NODES)]
    original = tuple(tuple(row) for row in raw)
    normalized, diagnostic = normalized_actual_response_column(raw, 0, q, F(1, 100))
    require(tuple(tuple(row) for row in raw) == original and diagnostic["ONE_contact_motion_upper_int"] >= 0,
            "RAW cache never modified or silently normalized in place")
    checks += 1
    exact = min(q ** 3 / 6, F(raw[0][0], SCALE) + q ** 4 * F(1, 100) / 12) / q ** 3
    require(F(normalized[0], SCALE) >= exact and len(normalized) == Y_NODES,
            "Correct RAW/S+movement, ONLY then positive q^3 division")
    checks += 1
    response = [0, 0]
    fake_choices = ((F(-1), (0, 10)), (F(1), (10, 0)))
    require(price.best_complete_equality_supremum(response, fake_choices)[0] == 10,
            "MINtheta AFTER MAXallcells, never per-node equality prices")
    checks += 1
    candidate = {"A": F(1, 5), "S_upper_int": -SCALE // 2,
        "prices": (F(1), F(0), F(0), F(-1), F(1)),
        "positive_sup_upper_int": -SCALE // 2, "negative_sup_upper_int": -SCALE,
        "positive_active_cell": 1, "negative_active_cell": 2,
        "selected_eta_cell_indices": [], "unrestricted_midpoint_eta_cell_indices": [0]}
    model = physical_model(candidate, q, 0)
    require(model["A"] == q ** 3 / 5 and model["S"] == -q ** 3 / 2
            and model["prices"][0] == q ** 3 and model["normalized_prices"] == candidate["prices"]
            and F(model["S_upper_int"], SCALE) >= model["S"],
            "Exact PHYSICAL q^3 conversion, signed slope and separately outward integer alias")
    checks += 1
    frequency = {"models": (model, {"A": F(0), "S": q ** 3 / 6, "label": "cube"})}
    eligible = nonnegative_models_for_closed_cell(frequency, F(0), F(1))
    require(len(eligible) == 1 and eligible[0]["label"] == "cube"
            and radius_value(model, F(1)) < 0 and model["S"] < 0,
            "Negative endpoint model not fake-clipped; independent cube whole-cell fallback")
    checks += 1
    require(as_transfer_models(frequency)[0][0:2] == (q ** 3 / 5, -q ** 3 / 2),
            "Transfer adapter retains exact signed PHYSICAL coefficients")
    checks += 1
    whole_negative = {"A": F(1, 10), "S": F(-1)}
    require(max(radius_value(whole_negative, F(1, 5)), radius_value(whole_negative, F(2, 5))) < 0,
            "Strict whole-cell negative radius evidence, equality not excluded")
    checks += 1
    zero_face = {"A": F(1, 5), "S": F(-1)}
    require(max(radius_value(zero_face, F(1, 5)), radius_value(zero_face, F(2, 5))) == 0,
            "Zero ceiling face is retained, not an empty WHOLE closed cell")
    checks += 1
    return {"status": "TINY_COMMON_NU_MODULUS_RADIUS_UNITS_ALGEBRA_ONLY", "exact_checks": checks,
        "CF_cache_A1_Gamma_radius_table_CDF_or_global_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
