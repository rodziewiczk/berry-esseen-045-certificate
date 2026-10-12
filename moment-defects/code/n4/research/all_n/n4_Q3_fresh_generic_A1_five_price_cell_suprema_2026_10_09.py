"""Exact finite-price Gamma compiler from a DIRECT-FRESH generic A1 table.

compute_verified_gamma_models(table,eta_cells,guard) consumes the fresh
correct generic A1 V2 API object IN MEMORY, never parsed numeric JSON.
The caller must have DIRECTLY invoked that audited producer, including
its correctly-scaled TRUE CF, actual-Q geometry correction, signed q
sum and closed-y-cell HG tail/mesh. Schema/flags/hash/status cannot prove
that mathematical prerequisite. We add NONE of its margins again.
No CF/A1/old price-search/radius/CDF producer is called by this compiler.

Five budgets, one shared positive measure
----------------------------------------
For eta>0 let nu=W*P/eta on tagged magnitudes y in[0,17/4], c=b or a.
Its off-contact support has y>0,y!=c. Set
 k0=1/(c^2*y), k1=1/(y-c), k2=1/(y-c)^2.
The canonical moment identities give nu probability,
 eta E k0<=p0, eta E_tag k2<=u, E_tag k1=0 for BOTH signs.
Take one COMPLETE physical-price tuple in canonical OLD order
 (lambda0,lambda_plus,lambda_minus,theta_plus,theta_minus),
with first3 nonnegative, last2 freely signed. If on EVERY tagged point

 A1_H -lambda0*k0-lambda_tag*k2-theta_tag*k1 <= S,

then eta E_nu A1_H <= A+eta*S, where
 A=p0_hi*lambda0+u_hi*(lambda_plus+lambda_minus).
The WHOLE-box upper budgets are valid because inequality prices are
nonnegative. Equality prices cost zero. Signed S and Gamma are NEVER
clipped or required nonnegative. At eta0 the original linear transfer
is zero directly, without defining nu; A>=0 keeps every model valid.
The later raw CDF ledger must multiply this Gamma by2.

Exact full-cell supremum
-----------------------
For each closed nearest-node y cell [L,H] and actual c in[clo,chi],
 k0>=1/(chi^2*H). Floor this lower bound to SCALE. For each rational
lambda0, floor its product with that lower integer BEFORE subtracting.
For z=1/(y-c), use the full reciprocal interval/ray OR TWO rays of
[L-chi,H-clo]\{0}; no nominal c substitution or one-sided pole clipping.
The pure retained reciprocal_domains/penalty_maximum compute the exact
concave maximum of -lambda_tag*z^2-theta_tag*z on those domains. CEIL
that SIGNED supremum to SCALE. Add this complete penalty upper to the
already signed A1 cell upper, subtract the inequality-cost lower, and
take the maximum over ALL273 cells. Contacts/zero are absent from nu,
but continuous A1 limits and the neighboring cells are all included.

Finite prices and frozen selection
----------------------------------
The declared exact grid has11 lambda0 prices,7 tag prices and7 equality
prices. A zero tag price uses only zero equality price: otherwise the
full domain around its contact has an infinite favorable linear ray.
For EACH fixed lambda0/tag price/equality price first take a WHOLE-cell
supremum over ALL y cells, THEN minimize over equality prices. Never
choose different equality prices per y point: that would lose E k1=0.
Because equality prices do not affect A and both tags are independent,
minimizing each complete tag supremum minimizes their maximum for fixed
lambda0/lambda_plus/lambda_minus. Combine all7x7 tag-price pairs using
the SAME lambda0 (the inverse-size budget is global, not per-tag).

At each exact eta-cell midpoint, select ONE complete five-price model
from this finite grid. Comparisons are exact integer operations at an
LCM denominator, not floating seeds or rounded objective comparisons.
Deduplicate ONLY full price tuples; always include the all-zero model.
Every emitted model is valid on the ENTIRE feasible eta fiber/WHOLE box,
not just its midpoint or selected cells. selected_eta_cell_indices is
diagnostic ONLY. A consumer may freeze any whole model on its eta cell;
it must never minimize polynomial coefficients or assert point-winner
persistence. All H and BOTH true reflections remain. Reflections SWAP
the actual positive/negative contact envelopes, not the canonical a/b
names or the physical-price tuple order.

Output schema agreed with the signed quartic consumer: scale,N,
box_geometry,nominal_root_data,q_grid,eta_cells,rows[{orientation,H,
models[{A:Fraction,S_upper_int:signedint,prices:tuple5Fractions,
selected_eta_cell_indices}]}], metadata.H_grid and metadata.price_order.
A is EXACT rational budget arithmetic; S is an outward signed integer.
The compiler adds no original-P remainder, radius model, physical reserve,
eta/CDF acceptance, root coverage or C4 theorem. Original P is not assumed
finitely supported. Caller owns cooperative time/256MiB guard; source
only until authorized. Dormant tiny algebra tests call no producer or
write any file. Preserve every older source/receipt/global.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from math import lcm
from pathlib import Path

import n4_Q3_fresh_generic_common_A1_response_table_v2_2026_10_09 as A1_builder

base = A1_builder.previous
cached, point, integer = base.cached, base.HG.point, base.integer
SCALE, TARGET, require = base.SCALE, base.TARGET, base.require
RADIUS, Y_STEP, Y_NODES = base.RADIUS, base.Y_STEP, base.Y_NODES
BUILDER_PIN = "0a5cf384dd991e8c9f30bc653dc3b180fe0fa8b23d14808890e64b1d7b173a7f"
PRICE_ORDER = ("lambda0", "lambda_plus", "lambda_minus", "theta_plus", "theta_minus")
TAUS = tuple(map(F, ("0", "1/1000", "1/400", "1/200", "1/100", "1/50",
                    "1/25", "2/25", "4/25", "8/25", "16/25")))
ZETAS = tuple(map(F, ("0", "1/2000", "1/1000", "1/400", "1/200", "1/100", "1/50")))
THETAS = tuple(map(F, ("-1/50", "-1/100", "-1/200", "0", "1/200", "1/100", "1/50")))


def source_drift_check():
    A1_builder.source_drift_check()
    require(hashlib.sha256(Path(A1_builder.__file__).read_bytes()).hexdigest() == BUILDER_PIN,
            "Correct builder source integrity only, not a Gamma proof premise")
    require(SCALE == point.SCALE and RADIUS == point.RADIUS and Y_STEP == point.STEP,
            "Identical PURE reciprocal/cost domain and fixed-point units")


def checked_prices(prices):
    require(type(prices) in (tuple, list) and len(prices) == 5
            and all(type(price) is F for price in prices) and min(prices[:3]) >= 0,
            "Canonical five exact prices: FIRST3 inequality, LAST2 signed equality")
    return tuple(prices)


def checked_preverified_A1_scope(table, eta_cells):
    """Scope/geometry guards ONLY; A1 bound truth requires DIRECT producer."""
    require(type(table) is dict and type(table.get("scale")) is int and table["scale"] == SCALE
            and type(table.get("N")) is int and table["N"] == 256, "Exact fresh N256 A1 scale")
    box, nominal = table["box_geometry"], table["nominal_root_data"]
    rectangle = tuple(box["rectangle"])
    canonical, true_nominal, _ = cached.geometry.canonical_geometry(rectangle)
    for key in ("a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket", "w_interval", "beta_abs_interval"):
        require(tuple(box[key]) == tuple(canonical[key]), "SAME canonical actual box: " + key)
    for key in ("p0_hi", "u_hi", "rhoQ_lo", "rhoQ_hi"):
        require(type(box[key]) is F and box[key] == canonical[key], "Exact WHOLE-box budget: " + key)
    for key in ("w", "beta", "a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket"):
        require(nominal[key] == true_nominal[key], "TRUE nominal not relabeled as box: " + key)
    metadata = table["metadata"]
    require(type(metadata["R"]) is F and metadata["R"] == RADIUS
            and type(metadata["y_step"]) is F and metadata["y_step"] == Y_STEP
            and type(metadata["y_nodes"]) is int and metadata["y_nodes"] == Y_NODES
            and type(metadata["HG_degree"]) is int and metadata["HG_degree"] == 60
            and metadata["A1_includes_nominal_HG_tail_y_mesh_once"] is True
            and metadata["A1_includes_box_geometry_margin"] is True,
            "Preproved WHOLE closed A1 cells; margins included ONCE")
    H_grid = tuple(metadata["H_grid"])
    require(len(H_grid) in (58, 115, 229) and all(type(H) is F for H in H_grid),
            "Complete declared physical H grid, no partial-H table")
    step = H_grid[1] - H_grid[0]
    require(H_grid == cached.quadrature.complete_H_grid(step), "Every central H endpoint/shared face")
    expected = {(orientation, H) for H in H_grid for orientation in (1, -1)}
    rows = table["rows"]
    require(len(rows) == len(expected) and {(row["orientation"], row["H"]) for row in rows} == expected,
            "Every H and BOTH physical signed-tag reflections")
    for row in rows:
        require(type(row["orientation"]) is int and type(row["H"]) is F,
                "Exact H/orientation, no Boolean orientation labels")
        for name in ("positive_cell_upper_int", "negative_cell_upper_int"):
            require(type(row[name]) in (tuple, list) and len(row[name]) == Y_NODES
                    and all(type(value) is int for value in row[name]), "All273 SIGNED A1 uppers")
    frequencies = table["frequency_data"]
    require(len(frequencies) == table["N"] and all(type(item["q"]) is F
            and item["q"] == F(3 * (2 * j + 1), 2 * table["N"]) for j, item in enumerate(frequencies)),
            "SAME complete physical q grid as future quartic ledger")
    require(type(eta_cells) in (tuple, list) and 1 <= len(eta_cells) <= 128,
            "Bounded declared closed eta-cell list")
    eta_cells = tuple(tuple(cell) for cell in eta_cells)
    require(all(len(cell) == 2 and all(type(value) is F for value in cell)
                and 0 <= cell[0] <= cell[1] for cell in eta_cells)
            and all(left[1] == right[0] for left, right in zip(eta_cells, eta_cells[1:])),
            "Exact CLOSED nonnegative eta cells with every shared face")
    return box, nominal, tuple(item["q"] for item in frequencies), H_grid, eta_cells


def whole_contact_price_offsets(contact_bracket, guard):
    """Precompute COMPLETE fixed-price cell offsets on the ACTUAL box contact."""
    require(type(contact_bracket) in (tuple, list) and len(contact_bracket) == 2
            and all(type(x) is int for x in contact_bracket)
            and 0 < contact_bracket[0] <= contact_bracket[1] <= RADIUS * SCALE,
            "WHOLE actual contact bracket inside owner response domain")
    clo, chi = (F(value, SCALE) for value in contact_bracket)
    costs, domains, two_rays = [], [], 0
    for node in range(Y_NODES):
        guard()
        L, H = max(F(0), node * Y_STEP - Y_STEP / 2), min(RADIUS, node * Y_STEP + Y_STEP / 2)
        domain = point.reciprocal_domains(L - chi, H - clo)
        domains.append(domain)
        two_rays += len(domain) == 2
        costs.append(integer.floor_fraction_scaled(1 / (chi * chi * H)))
    # Pole prices do not depend on lambda0; compute their exact maxima ONCE.
    penalties_by_zeta = []
    for zeta in ZETAS:
        equality_choices = []
        for theta in THETAS:
            if zeta == 0 and theta != 0:
                continue
            guard()
            penalties = tuple(integer.ceil_fraction_scaled(point.penalty_maximum(zeta, theta, domain))
                              for domain in domains)
            equality_choices.append((theta, penalties))
        require(equality_choices, "At least zero equality price for every tag price")
        penalties_by_zeta.append(tuple(equality_choices))
    offsets = []
    for tau in TAUS:
        guard()
        # The floored nonnegative cost remains a LOWER price*k0 bound.
        cost_prices = [value * tau.numerator // tau.denominator for value in costs]
        tag_prices = [tuple((theta, tuple(penalty - cost for penalty, cost in zip(penalties, cost_prices)))
                            for theta, penalties in choices) for choices in penalties_by_zeta]
        offsets.append(tuple(tag_prices))
    return tuple(offsets), {"two_ray_cell_count": two_rays, "cell_count": Y_NODES,
        "cost_lower_floor_used": True, "signed_pole_upper_ceil_used": True}


def best_complete_equality_supremum(values, choices):
    """For EACH fixed theta MAX ALL cells first, THEN choose minimum theta."""
    require(type(values) in (tuple, list) and len(values) > 0
            and all(type(value) is int for value in values), "Signed exact pointwise cell uppers")
    require(type(choices) in (tuple, list) and len(choices) > 0,
            "Complete equality-price choices, not point-dependent coefficients")
    best = None
    for theta, offsets in choices:
        require(type(theta) is F and len(offsets) == len(values)
                and all(type(value) is int for value in offsets), "Same complete cell domain for fixed theta")
        maximum, active = None, None
        for index, (value, offset) in enumerate(zip(values, offsets)):
            candidate = value + offset
            if maximum is None or candidate > maximum:
                maximum, active = candidate, index
        record = (maximum, theta, active)
        if best is None or (record[0], record[1]) < (best[0], best[1]):
            best = record
    return best


def tag_supremum_grid(values, offsets, guard):
    result = []
    for tau_choices in offsets:
        row = []
        for choices in tau_choices:
            guard()
            row.append(best_complete_equality_supremum(values, choices))
        result.append(tuple(row))
    require(len(result) == len(TAUS) and all(len(row) == len(ZETAS) for row in result),
            "Every fixed lambda0/tag price has its complete signed supremum")
    return tuple(result)


def exact_midpoint_choice(candidates, midpoint, denominator):
    """Exact LCM-integer objective comparison, preserving negative Gamma."""
    require(type(midpoint) is F and midpoint >= 0 and type(denominator) is int
            and denominator > 0 and denominator % SCALE == 0 and candidates,
            "Exact nonnegative eta midpoint/common arithmetic denominator")
    factor = denominator // SCALE
    best = None
    for index, candidate in enumerate(candidates):
        A, S = candidate["A"], candidate["S_upper_int"]
        require(type(A) is F and A >= 0 and type(S) is int and denominator % A.denominator == 0,
                "Exact signed Gamma and intercept denominator, not rounded optimization")
        score = A.numerator * (denominator // A.denominator) * midpoint.denominator + midpoint.numerator * S * factor
        if best is None or score < best[0]:
            best = score, index
    return best[1]


def compute_verified_gamma_models(table, eta_cells, guard):
    """Preverified DIRECT fresh A1 table; no cache/CF/radius/CDF producer."""
    require(callable(guard), "Caller-owned cooperative time/256MiB guard")
    guard()
    source_drift_check()
    box, nominal, q_grid, H_grid, eta_cells = checked_preverified_A1_scope(table, eta_cells)
    contact_tables, contact_metadata = {}, {}
    for name in ("a", "b"):
        contact_tables[name], contact_metadata[name] = whole_contact_price_offsets(box[name + "_bracket"], guard)
    intercepts, denominator = {}, SCALE
    for it, tau in enumerate(TAUS):
        for ip, zp in enumerate(ZETAS):
            for im, zm in enumerate(ZETAS):
                A = box["p0_hi"] * tau + box["u_hi"] * (zp + zm)
                intercepts[it, ip, im] = A
                denominator = lcm(denominator, A.denominator)
    rows = []
    for response in table["rows"]:
        guard()
        orientation, H = response["orientation"], response["H"]
        plus_name, minus_name = (("b", "a") if orientation == 1 else ("a", "b"))
        plus = tag_supremum_grid(response["positive_cell_upper_int"], contact_tables[plus_name], guard)
        minus = tag_supremum_grid(response["negative_cell_upper_int"], contact_tables[minus_name], guard)
        candidates = []
        for it, tau in enumerate(TAUS):
            for ip, zp in enumerate(ZETAS):
                sp, tp, activep = plus[it][ip]
                for im, zm in enumerate(ZETAS):
                    sm, tm, activem = minus[it][im]
                    prices = checked_prices((tau, zp, zm, tp, tm))
                    candidates.append({"A": intercepts[it, ip, im], "S_upper_int": max(sp, sm),
                        "prices": prices, "positive_sup_upper_int": sp, "negative_sup_upper_int": sm,
                        "positive_active_cell": activep, "negative_active_cell": activem})
        require(len(candidates) == len(TAUS) * len(ZETAS) ** 2,
                "Every pair of tag budgets shares ONE lambda0 and complete equality prices")
        zero = next(candidate for candidate in candidates if candidate["prices"] == (F(0),) * 5)
        selected = {zero["prices"]: dict(zero, selected_eta_cell_indices=[])}
        for cell_index, (L, U) in enumerate(eta_cells):
            guard()
            candidate = candidates[exact_midpoint_choice(candidates, (L + U) / 2, denominator)]
            prices = candidate["prices"]
            model = selected.setdefault(prices, dict(candidate, selected_eta_cell_indices=[]))
            require(model["A"] == candidate["A"] and model["S_upper_int"] == candidate["S_upper_int"],
                    "Dedup FULL exact price tuple only, never mixed A/S coefficients")
            model["selected_eta_cell_indices"].append(cell_index)
        models = []
        for prices in sorted(selected):
            model = selected[prices]
            model["selected_eta_cell_indices"] = tuple(model["selected_eta_cell_indices"])
            require(model["A"] == box["p0_hi"] * prices[0] + box["u_hi"] * (prices[1] + prices[2]),
                    "EXACT canonical WHOLE-box budget intercept, signed equality costs zero")
            models.append(model)
        rows.append({"orientation": orientation, "H": H, "models": models})
    source_drift_check()
    guard()
    files = (Path(__file__), Path(A1_builder.__file__), Path(base.__file__),
        Path(point.__file__), Path(integer.__file__), Path(cached.geometry.__file__),
        Path(cached.previous.geometry_factory.__file__))
    return {"scale": SCALE, "N": table["N"], "box_geometry": box, "nominal_root_data": nominal,
        "q_grid": q_grid, "eta_cells": eta_cells, "rows": rows,
        "metadata": {"H_grid": H_grid, "price_order": PRICE_ORDER,
            "lambda0_grid": TAUS, "tag_inequality_grid": ZETAS, "tag_equality_grid": THETAS,
            "contact_cell_metadata": contact_metadata, "exact_objective_LCM_denominator": denominator,
            "theta_min_after_COMPLETE_cell_sup_not_per_point": True,
            "selected_eta_cell_indices_are_diagnostics_not_model_validity_restrictions": True,
            "zero_model_always_included": True, "all_models_valid_WHOLE_geometry_and_feasible_eta_fiber": True,
            "signed_S_and_Gamma_clipped": False, "A1_tail_mesh_geometry_or_center_margin_repeated": False,
            "radius_R2_physical_reserves_or_CDF_acceptance_computed": False,
            "preverified_DIRECT_fresh_A1_bound_truth_is_caller_math_premise": True,
            "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}}}


def self_tests():
    """Dormant small exact price/pole/selection checks; no real table producer."""
    checks = 0
    values = [0, 0]
    choices = ((F(-1), (0, 10)), (F(1), (10, 0)))
    require(best_complete_equality_supremum(values, choices)[0] == 10,
            "MINtheta AFTER MAXcells, not invalid per-point free equality pricing")
    checks += 1
    require(best_complete_equality_supremum([-SCALE, -SCALE], ((F(0), (0, 0)),))[0] == -SCALE,
            "Negative whole signed supremum retained")
    checks += 1
    for dlo, dhi in ((F(-2), F(-1)), (F(1), F(2)), (F(-1), F(1))):
        domains = point.reciprocal_domains(dlo, dhi)
        for zeta, theta in ((F(0), F(0)), (F(1, 100), F(-1, 50)), (F(1, 200), F(1, 100))):
            upper = point.penalty_maximum(zeta, theta, domains)
            for d in (dlo, dhi):
                z = 1 / d
                require(-zeta * z * z - theta * z <= upper,
                        "Signed full reciprocal-domain concave maximum contains both endpoints")
                checks += 1
    candidates = [{"A": F(1, 3), "S_upper_int": -SCALE},
                  {"A": F(1, 7), "S_upper_int": SCALE // 2},
                  {"A": F(0), "S_upper_int": -2 * SCALE}]
    denominator = lcm(SCALE, 3, 7)
    for midpoint in (F(0), F(1, 10), F(1)):
        chosen = exact_midpoint_choice(candidates, midpoint, denominator)
        exact = min(range(len(candidates)), key=lambda i:
            candidates[i]["A"] + midpoint * F(candidates[i]["S_upper_int"], SCALE))
        require(chosen == exact, "LCM integer comparison is EXACT Fraction objective comparison")
        checks += 1
    prices = checked_prices((F(1, 100), F(1, 200), F(1, 50), F(-1, 10), F(1, 5)))
    require(PRICE_ORDER == ("lambda0", "lambda_plus", "lambda_minus", "theta_plus", "theta_minus")
            and F(1, 3) * prices[0] + F(1, 4) * (prices[1] + prices[2]) == F(23, 2400),
            "Canonical budget order, no signed equality price used as an inequality budget")
    checks += 1
    rejected = False
    try:
        checked_prices((F(0), F(-1), F(0), F(0), F(0)))
    except RuntimeError:
        rejected = True
    require(rejected, "Negative inequality price rejected")
    checks += 1
    return {"status": "TINY_GENERIC_A1_GAMMA_PRICE_ALGEBRA_TESTS_ONLY", "exact_checks": checks,
        "CF_A1_radius_Gamma_table_or_CDF_producer_called": False,
        "synthetic_checks_prove_CDF_or_C4": False, "source_or_receipt_files_written": False}
