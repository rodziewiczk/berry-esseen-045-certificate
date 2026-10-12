"""Generic fresh centre-only BOX x closed-eta Prawitz leaf; NOT full C4.

API compute_verified_low_eta_box_leaf(rectangle, eta_interval, N=256,
H_step=1/32) uses arbitrary exact w/|beta| rectangles whose entire Q3
contacts lie in [0,17/4]. The expansion reference is the exact midpoint
probability Q3. It is NOT required to satisfy an old price-seed rho cap.
No saved numerical table, price seed, common-A1 y table, r/r_c cache,
optimizer, finite-support reduction of the original P, or CDF(Q3)-to-
Prawitz replacement is used.

All characteristic-function exponential remainders are FIRST converted
to fixed-point units: ceil(S*(q*R)^61/61!). The preserved legacy generic
CF helper mistakenly passed the physical Fraction remainder directly to
an integer fixed-point routine. This module never uses that helper in a
proof path. Its exact tiny regression demonstrates the old bracket can
miss an independently evaluated degree120 exponential near contact4.
Old Fourier results require corrected fresh verification; this module
does not retrospectively validate their receipts or edit their sources.

The TRUE nominal finite Prawitz centres are computed freshly for both
conjugate orientations. Whole-box Eg=min(matched/direct mass geometry,
q^3*(physicalDelta_a+Delta_b)/6) gives the independently valid correction
2sum|kappa|D4(Eg,|g_nom|upper) and old actual-Q modulus cap min(1,a0+Eg).
Optional contact-Taylor tightening uses ONLY audited pure derivative,
signed-gradient, Hessian, and radial square-root helpers. It does not call
legacy high-level APIs that rebuild the flawed CF. Its baseline is this
module's correctly scaled TRUE nominal rectangle, not a rational-contact
baseline. Probability contact paths are convex: b>=a and ab>=1.

For actual Q3 and eta=rhoP-rhoQ>=0, the common Hermite response proves
|phiP(q)-g_actual(q)|<=eta*q^3/6. The zero-mass budget also gives the
independent cap M_Q^2*p0*q^2, and the unit disk gives1+|g_actual|upper.
Any one nonnegative affine radius is frozen on each entire CLOSED eta
cell. Its complete fourth-power telescope has a frozen-p affine upper;
the complete endpoint constant may replace it on the entire cell. Never
minimize polynomial coefficients or assume persistence of a point winner.
Upward-rounded affine coefficients preserve order because eta>=0. Exact
degree1 Bernstein/endpoint tests cover each whole cell, including joins.

Standing physical premises: standardized iid actual P, its canonical
coordinates in the declared box/eta interval, |X|<=17/4, rhoP<46/25,
one-sided closed-CDF Prawitz and the retained physical bridge. The latter
derives P.M4<8 from these premises, not from a new M4 axiom. Add ONE raw
midpoint reserve687/(8N^2) and ONE threshold reserve19*h^2/32. The bridge
proves that formula for arbitrary spacingh; allowed complete raw-H grids
are58/115/229 nodes (h1/8,1/16,1/32) on[-4,25/8]. Both orientations and
the actual-law tails2/5 are included. Actual normalization is rhoQ+eta,
bounded below by rhoQ_LO_BOX+eta. An enlarged numerical eta interval
does not assert feasibility or the physical rho premise at every point.

Target4097/10000 is independently checked below CE=(3+sqrt10)*phi0/6.
Only strict whole-cell bounds and tails permit conditional acceptance.
UNKNOWN means a failed upper estimate, not a counterexample. Full root
or unrestricted C4 is NEVER asserted. Pure stdlib, one externally
coordinated producer, cooperative60s/256MiB. Import/CLI runs only tiny
tests; this source supplies an API, NO producer CLI or file write.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import time

import n4_windows_resource_guard_2026_10_09 as resources
import n4_Q3_signed_contact_center_taylor_resource_safe_2026_10_09 as center
import n4_Q3_squared_modulus_contact_taylor_resource_safe_2026_10_09 as radial
import n4_eta_affine_transfer_bernstein_2026_10_08 as algebra

integer, arithmetic, SCALE = center.integer, center.arithmetic, center.SCALE
geometry_factory, geometry = center.box_backend.geometry_factory, center.box_backend
RADIUS, RHO_CAP, TARGET = F(17, 4), F(46, 25), F(4097, 10000)
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
ALLOWED_H_STEPS = (F(1, 8), F(1, 16), F(1, 32))
CONSTRAINT_NOTE = Path(__file__).with_name("n4_Q3_signed_response_constraints_2026_10_08.md")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def checked_request(rectangle, eta_interval, N, H_step, initial_eta_cells, max_eta_cells):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is F for value in rectangle), "Four exact Fraction box endpoints")
    wl, wh, bl, bh = rectangle
    require(0 < wl <= wh <= 1 and 0 <= bl <= bh < 1, "Closed standardized Q3 magnitude box")
    require(type(eta_interval) in (tuple, list) and len(eta_interval) == 2
            and all(type(value) is F for value in eta_interval)
            and 0 <= eta_interval[0] <= eta_interval[1], "Exact nonnegative CLOSED eta interval")
    require(type(N) is int and N == 256, "Initial physical frequency grid fixed at N256")
    require(type(H_step) is F and H_step in ALLOWED_H_STEPS, "Approved complete physical H spacing")
    require(type(initial_eta_cells) is int and type(max_eta_cells) is int
            and 1 <= initial_eta_cells <= max_eta_cells <= 128, "Bounded complete eta partition")
    return tuple(rectangle), tuple(eta_interval)


def complete_H_grid(H_step):
    require(type(H_step) is F and H_step in ALLOWED_H_STEPS, "Exact approved H spacing")
    length = F(57, 8) / H_step
    require(length.denominator == 1, "Exact outer H faces")
    grid = tuple(F(-4) + j * H_step for j in range(length.numerator + 1))
    require(grid[0] == -4 and grid[-1] == F(25, 8)
            and all(right - left == H_step for left, right in zip(grid, grid[1:])), "No H gaps")
    return grid


def generic_characteristic_correctly_scaled(q, root):
    """Fresh true Q3 CF rectangle; remainder in SCALE units, never physical units."""
    require(type(q) is F and 0 <= q <= 3, "Exact approved raw frequency")
    w, beta = root["w"], root["beta"]
    require(type(w) is F and type(beta) is F and 0 < w <= 1 and 0 <= beta < 1,
            "Exact nominal probability geometry, NO rho seed restriction")
    require(max(root["a_bracket"][1], root["b_bracket"][1]) <= RADIUS * SCALE,
            "Nominal contact enclosure inside support radius")
    physical_remainder = (q * RADIUS) ** 61 / factorial(61)
    fixedpoint_remainder = integer.ceil_fraction_scaled(physical_remainder)
    require(type(fixedpoint_remainder) is int
            and F(fixedpoint_remainder, SCALE) >= physical_remainder,
            "Exponential remainder is outward fixed-point, not an unscaled Fraction")
    negative = integer.weighted_rectangle(w * (1 + beta) / 2,
        integer.conjugate_rectangle(integer.outward_exponential(q, root["a_bracket"], fixedpoint_remainder)))
    positive = integer.weighted_rectangle(w * (1 - beta) / 2,
        integer.outward_exponential(q, root["b_bracket"], fixedpoint_remainder))
    zero = integer.fraction_interval(1 - w)
    result = (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
              negative[2] + positive[2], negative[3] + positive[3])
    require(all(type(value) is int for value in result), "Fixed-point CF rectangle has integer endpoints")
    return result


def fresh_target_certificate(pi=None, phi0=None):
    if pi is None or phi0 is None:
        pi, phi0 = arithmetic.pi_and_phi0()
    sqrt10 = integer.sqrt_fraction_interval(F(10))
    ce_lower = F((3 * SCALE + sqrt10[0]) * phi0[0], 6 * SCALE ** 2)
    require(TARGET < ce_lower, "Fresh exact Gaussian/sqrt10 target comparison")
    return {"target": TARGET, "CE_formula": "(3+sqrt(10))*phi(0)/6",
            "pi_bracket": pi, "phi0_bracket": phi0, "sqrt10_bracket": sqrt10,
            "CE_lower_exact": ce_lower, "strict_target_comparison": True}


def fresh_center_table(rectangle, N, H_grid, use_contact_taylor, guard):
    """No common A1/y response table. Every CF and true center is freshly rebuilt."""
    box, nominal, bridge = geometry.canonical_geometry(rectangle)
    pi, phi0 = arithmetic.pi_and_phi0()
    da, db = F(bridge["da"], SCALE), F(bridge["db"], SCALE)
    blocks, frequencies, triangle_scale2 = {1: [], -1: []}, [], 0
    for j in range(N):
        guard()
        q = F(3 * (2 * j + 1), 2 * N)
        kernel = arithmetic.kernel_rectangle(F(2 * j + 1, 2 * N), N, 32, pi)
        k = integer.rectangle_modulus_upper(kernel)
        g0 = generic_characteristic_correctly_scaled(q, nominal)
        a0 = min(SCALE, integer.rectangle_modulus_upper(g0))
        Eg = integer.ceil_fraction_scaled(min(geometry.reference_bridge.reference_error(q, bridge),
                                              q ** 3 * (da + db) / 6))
        actual = min(SCALE, a0 + Eg)
        D4 = arithmetic.quartic_absolute_upper(Eg, a0)
        triangle_scale2 += 2 * k * D4
        frequencies.append({"q": q, "kernel_rectangle": kernel, "kernel_modulus_upper_int": k,
            "g_nominal_rectangle": g0, "g_nominal_modulus_upper_int": a0,
            "g_actual_modulus_upper_int": actual, "Eg_upper_int": Eg, "D4_upper_int": D4})
        for orientation, characteristic in ((1, g0), (-1, integer.conjugate_rectangle(g0))):
            square = arithmetic.complex_multiply(characteristic, characteristic)
            fourth = arithmetic.complex_multiply(square, square)
            blocks[orientation].append(arithmetic.complex_multiply(kernel, fourth))
    triangle = integer.ceil_div(triangle_scale2, SCALE)
    rows = []
    for H in H_grid:
        guard()
        phase = arithmetic.exponential_exact_argument(-3 * H / (2 * N))
        ratio = arithmetic.exponential_exact_argument(-3 * H / N)
        sums = {1: 0, -1: 0}
        for j in range(N):
            for orientation in (1, -1):
                sums[orientation] += arithmetic.complex_multiply(phase, blocks[orientation][j])[1]
            phase = arithmetic.unit_phase_intersection(arithmetic.complex_multiply(phase, ratio))
        normal = arithmetic.normal_cdf_interval(H / 2, phi0)
        for orientation in (1, -1):
            raw_nominal = SCALE + 2 * sums[orientation] - 2 * normal[0]
            rows.append({"orientation": orientation, "H": H,
                         "nominal_raw_Q_center_upper_int": raw_nominal,
                         "raw_Q_center_upper_int": raw_nominal + triangle})
    table = {"scale": SCALE, "N": N, "box_geometry": box, "nominal_root_data": nominal,
             "rows": rows, "frequency_data": frequencies, "metadata": {"H_grid": H_grid}}
    taylor_metadata = {"used": False}
    if use_contact_taylor:
        taylor_metadata = tighten_with_pure_contact_taylor(table, rectangle, N, H_grid, guard)
    normal_tail = arithmetic.normal_cdf_interval(F(25, 16), phi0)
    require(5 * normal_tail[0] > 4 * SCALE, "Fresh exact positive-tail Gaussian witness")
    require(len(rows) == 2 * len(H_grid)
            and {(row["orientation"], row["H"]) for row in rows}
                == {(orientation, H) for H in H_grid for orientation in (1, -1)}, "ALL H/reflection centers")
    table["metadata"].update({"no_common_A1_or_response_cache": True,
        "nominal_reference_rho_cap_imposed": False, "exponential_tail_in_fixedpoint_units": True,
        "raw_Q_geometry_margin_upper_int": triangle, "contact_Taylor": taylor_metadata,
        "positive_tail_Phi_lower_int": normal_tail[0],
        "fresh_target_certificate": fresh_target_certificate(pi, phi0)})
    return table


def tighten_with_pure_contact_taylor(table, rectangle, N, H_grid, guard):
    """Only pure corrected-derivative tools; NEVER legacy CF rebuilding APIs."""
    inputs = center.canonical_inputs(table, rectangle, N, H_grid)
    box, nominal, bridge, _, _, ai, bi, a_bar, b_bar, da, db, ea, eb = inputs
    gradient_blocks = []
    for item in table["frequency_data"]:
        guard()
        gradient_blocks.append(center.base_derivative_blocks(item["q"], item["kernel_rectangle"], a_bar, b_bar))
    hessian = center.center_hessian_majorants(table["frequency_data"], ai, bi)
    indexed = {(row["orientation"], row["H"]): row for row in table["rows"]}
    center_improvements = 0
    for H in H_grid:
        guard()
        gradients = center.sum_signed_gradient_intervals(gradient_blocks, H, N, guard)
        for orientation in (1, -1):
            row = indexed[orientation, H]
            ga, gb = center.expand_true_nominal_gradient(*gradients[orientation], ea, eb, hessian)
            taylor = center.whole_box_taylor_upper_int(row["nominal_raw_Q_center_upper_int"], ga, gb, da, db, hessian)
            center_improvements += taylor < row["raw_Q_center_upper_int"]
            row["raw_Q_center_upper_int"] = min(taylor, row["raw_Q_center_upper_int"])
    modulus_improvements = 0
    for item in table["frequency_data"]:
        guard()
        q = item["q"]
        nominal_square = radial.nominal_squared_norm_upper(item["g_nominal_rectangle"])
        Hess = radial.modulus_squared_hessian_majorants(q, ai, bi)
        ga, gb = center.expand_true_nominal_gradient(*radial.radial_gradient_intervals(q, a_bar, b_bar), ea, eb, Hess)
        square_upper = radial.squared_modulus_taylor_upper(nominal_square, ga, gb, da, db, Hess)
        old = item["g_actual_modulus_upper_int"]
        actual, _ = radial.outward_modulus_from_squared_upper(square_upper, old)
        require(item["g_nominal_modulus_upper_int"] <= actual <= old, "Actual norm tightening contains true nominal reference")
        modulus_improvements += actual < old
        item["g_actual_modulus_upper_int"] = actual
    return {"used": True, "center_rows_improved": center_improvements,
        "moduli_improved": modulus_improvements, "raw_center_Hessian_abs_bounds": hessian,
        "probability_path": "b>=a,ab>=1 convex; |g|<=1 on actual/true-nominal/rational-upper-root paths",
        "baseline": "Correctly scaled TRUE nominal CF and raw-Q center from THIS fresh producer",
        "legacy_high_level_CF_rebuild_or_check_called": False}


def affine_radius_models(q, actual_modulus, box):
    """Each model individually bounds delta=P-Q_ACTUAL on every eta>=0."""
    require(type(q) is F and type(actual_modulus) is F and 0 <= actual_modulus <= 1,
            "Exact physical q and actual reference modulus cap")
    M = F(max(box["a_bracket"][1], box["b_bracket"][1]), SCALE)
    p0 = box["p0_hi"]
    require(M > 0 and 0 <= p0 <= 1, "Actual whole-box knot/p0 uppers")
    return ((F(0), q ** 3 / 6, "cube"), (M ** 2 * p0 * q ** 2, F(0), "mass"),
            (1 + actual_modulus, F(0), "unit"))


def frozen_complete_ABS_cell(frequencies, raw_constant, rho_lower, L, U):
    """Approved frozen-p COMPLETE fourth-power transfer; degree1 endpoint proof."""
    require(type(L) is F and type(U) is F and 0 <= L <= U and type(rho_lower) is F and rho_lower >= 1,
            "Exact closed eta interval and positive lower normalization")
    intercept_scale2 = slope_scale2 = 0
    choices, counts = [], {"cube": 0, "mass": 0, "unit": 0, "endpoint": 0}
    for item in frequencies:
        allowed = [model for model in item["models"] if min(model[0] + model[1] * L, model[0] + model[1] * U) >= 0]
        require(allowed, "Cube always supplies a whole-cell nonnegative radius")
        A, B, name = min(allowed, key=lambda model: model[0] + model[1] * (L + U) / 2)
        a = item["modulus"]
        transfer = algebra.frozen_cap_linear_transfer(a, A, B, L, U)
        C, D = transfer[0], transfer[1] if len(transfer) == 2 else F(0)
        p = min(F(1), a + max(A + B * L, A + B * U))
        endpoint = p ** 4 + a ** 4
        if endpoint <= min(C + D * L, C + D * U):
            C, D = endpoint, F(0)
            counts["endpoint"] += 1
        # All complete E functions are nonnegative on the WHOLE cell.
        # Ceiling C,D raises E for eta>=0; ceiling weight preserves order.
        k = item["weight_int"]
        require(type(k) is int and k >= 0, "Fresh nonnegative outward kernel weight")
        intercept_scale2 += k * integer.ceil_fraction_scaled(C)
        slope_scale2 += k * integer.ceil_fraction_scaled(D)
        counts[name] += 1
        choices.append(name)
    C = F(integer.ceil_div(intercept_scale2, SCALE), SCALE)
    D = F(integer.ceil_div(slope_scale2, SCALE), SCALE)
    target_poly = algebra.raw_target_for_transfers(raw_constant, [(F(1), (C, D))], rho_lower, TARGET)
    passed, coefficients = algebra.bernstein_strict_negative(target_poly, L, U, degree=1)
    raw_L, raw_U = raw_constant + 2 * (C + D * L), raw_constant + 2 * (C + D * U)
    score = max(F(0), raw_L / (rho_lower + L), raw_U / (rho_lower + U))
    require(passed == (raw_L < TARGET * (rho_lower + L) and raw_U < TARGET * (rho_lower + U)),
            "Whole-cell degree1 Bernstein equals exact endpoint tests")
    return {"lower": L, "upper": U, "passed": passed, "score_upper": score,
        "raw_endpoint_uppers": (raw_L, raw_U), "target_polynomial": target_poly,
        "target_Bernstein_coefficients": coefficients, "transfer_affine_upper": (C, D),
        "selected_model_counts": counts,
        "choices_digest_integrity_only": hashlib.sha256(json.dumps(choices).encode("ascii")).hexdigest()}


def compute_verified_low_eta_box_leaf(rectangle, eta_interval, N=256, H_step=F(1, 32),
                                    use_contact_taylor=True, initial_eta_cells=16,
                                    max_eta_cells=64, time_limit_seconds=TIME_LIMIT):
    """One coordinated fresh generic conditional CDF leaf; no source/file writes."""
    started = time.monotonic()
    rectangle, eta_interval = checked_request(rectangle, eta_interval, N, H_step, initial_eta_cells, max_eta_cells)
    require(type(use_contact_taylor) is bool, "Explicit optional pure contact-Taylor switch")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic overall budget<=60s")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Generic leaf elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Generic leaf256MiB working set")
    H_grid = complete_H_grid(H_step)
    table = fresh_center_table(rectangle, N, H_grid, use_contact_taylor, guard)
    box, rho_lower = table["box_geometry"], table["box_geometry"]["rhoQ_lo"]
    require(rho_lower >= 1, "Actual reference third absolute moment lower>=1")
    frequencies = []
    for item in table["frequency_data"]:
        a = F(item["g_actual_modulus_upper_int"], SCALE)
        frequencies.append({"modulus": a, "weight_int": item["kernel_modulus_upper_int"],
            "models": affine_radius_models(item["q"], a, box)})
    worst_Q = max(table["rows"], key=lambda row: row["raw_Q_center_upper_int"])
    quad, H_reserve = F(687, 8 * N * N), F(19, 32) * H_step ** 2
    raw_constant = F(worst_Q["raw_Q_center_upper_int"], SCALE) + quad + H_reserve
    L, U = eta_interval
    intervals = [(L, U)] if L == U else [(L + (U - L) * F(j, initial_eta_cells),
        L + (U - L) * F(j + 1, initial_eta_cells)) for j in range(initial_eta_cells)]
    cells = [frozen_complete_ABS_cell(frequencies, raw_constant, rho_lower, l, u) for l, u in intervals]
    stopped = False
    while len(cells) < max_eta_cells:
        failed = [(u - l, i) for i, ((l, u), cell) in enumerate(zip(intervals, cells)) if not cell["passed"] and l < u]
        if not failed:
            break
        if time.monotonic() - started > time_limit_seconds - 5:
            stopped = True
            break
        _, index = max(failed)
        l, u = intervals[index]
        mid = (l + u) / 2
        pieces = [(l, mid), (mid, u)]
        new = [frozen_complete_ABS_cell(frequencies, raw_constant, rho_lower, x, y) for x, y in pieces]
        intervals[index:index + 1], cells[index:index + 1] = pieces, new
        guard()
    require(intervals[0][0] == L and intervals[-1][1] == U
            and all(left[1] == right[0] for left, right in zip(intervals, intervals[1:])), "COMPLETE closed eta cover")
    tail = F(2, 5)
    upper = max(tail, max(cell["score_upper"] for cell in cells))
    passed = all(cell["passed"] for cell in cells) and tail < TARGET
    require(not passed or upper < TARGET, "Every H/reflection/eta cell AND tails strictly pass")
    guard()
    files = (Path(__file__), Path(resources.__file__), Path(center.__file__), Path(radial.__file__),
        Path(center.derivatives.__file__), Path(geometry.__file__), Path(geometry_factory.__file__),
        Path(geometry.reference_bridge.__file__), Path(arithmetic.__file__), Path(integer.__file__),
        Path(algebra.__file__), arithmetic.SUPPORT_NOTE, arithmetic.PHYSICAL_BRIDGE, CONSTRAINT_NOTE)
    return {"status": "EXACT_CONDITIONAL_GENERIC_LOW_ETA_BOX_CDF_LEAF" if passed else "UNKNOWN",
        "date": "2026-10-09", "scale": SCALE, "N": N, "H_step": H_step, "target": TARGET,
        "closed_rectangle": rectangle, "closed_eta_cover": eta_interval, "box_geometry": box,
        "nominal_root_data": table["nominal_root_data"], "cells": cells,
        "reference_centers_both_orientations": table["rows"], "frequency_data": table["frequency_data"],
        "reference_metadata": table["metadata"], "worst_Q_center": worst_Q,
        "reserves_once": {"physical_quad": quad, "physical_H": H_reserve},
        "tail": {"score_upper": tail, "Phi_25_16_lower_int": table["metadata"]["positive_tail_Phi_lower_int"]},
        "summary": {"score_upper_exact": upper, "strict_margin_exact": TARGET - upper,
            "initial_eta_cells": 1 if L == U else initial_eta_cells, "final_eta_cells": len(cells),
            "failed_eta_cells": sum(not cell["passed"] for cell in cells), "adaptive_scheduling_stopped": stopped,
            "ALL_H_rows": len(table["rows"]), "ALL_H_nodes": len(H_grid)},
        "physical_premises": "Standardized iid actual P, actual canonical geometry/eta in the declared CLOSED box/interval, |X|<=17/4,actualrho=rhoQ(actual)+eta<46/25. One-sided closed-CDF Prawitz and retained physical quadrature/H bridge are external analytic inputs. No atom-count or separate M4 assumption. First-critical C3/attainment/HC input only places a hypothetical critical owner in this class.",
        "proof_scope": "Fresh finite TRUE raw-Q Prawitz centers, whole-box geometric correction, actual-reference modulus cap, complete iid fourth-power ABS transfer, one physical reserve of each type, both orientations/all central H/closed eta cells and actual-law tails. Numerical outer parameter points need not be realizable. No substitution of exactCDF(Q3) for J_Q.",
        "conclusions": {"conditional_CDF_on_entire_declared_BOX_and_eta": passed,
            "entire_global_root_covered": False, "unrestricted_C4_proved": False,
            "saved_numeric_JSON_or_float_proof_inputs": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "standard_library_only": True}}


def independent_degree120_exponential(argument):
    """Tiny independent EXACT rational Taylor, not a producer/floating oracle."""
    require(type(argument) is F, "Exact independent exponential argument")
    re = im = F(0)
    for degree in range(121):
        term = argument ** degree / factorial(degree)
        phase = degree % 4
        if phase == 0:
            re += term
        elif phase == 1:
            im += term
        elif phase == 2:
            re -= term
        else:
            im -= term
    remainder = abs(argument) ** 121 / factorial(121)
    return (integer.floor_fraction_scaled(re - remainder), integer.ceil_fraction_scaled(re + remainder),
            integer.floor_fraction_scaled(im - remainder), integer.ceil_fraction_scaled(im + remainder))


def independent_degree120_characteristic(q, root):
    """Independent high-degree CF for a TRUE irrational-contact reference.

    Evaluate at each rational upper root and enlarge by the exact physical
    Lipschitz bound q*(root_hi-root_lo)/S before weighting. Thus this is an
    enclosure of the TRUE reference, not a changed rational-contact law.
    """
    require(type(q) is F and q >= 0, "Exact independent physical frequency")
    contact_rectangles = {}
    for name in ("a", "b"):
        lo, hi = root[name + "_bracket"]
        rectangle = independent_degree120_exponential(q * F(hi, SCALE))
        shift = integer.ceil_fraction_scaled(q * F(hi - lo, SCALE))
        contact_rectangles[name] = (rectangle[0] - shift, rectangle[1] + shift,
                                    rectangle[2] - shift, rectangle[3] + shift)
    w, beta = root["w"], root["beta"]
    negative = integer.weighted_rectangle(w * (1 + beta) / 2,
        integer.conjugate_rectangle(contact_rectangles["a"]))
    positive = integer.weighted_rectangle(w * (1 - beta) / 2, contact_rectangles["b"])
    zero = integer.fraction_interval(1 - w)
    return (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
            negative[2] + positive[2], negative[3] + positive[3])


def tiny_regressions():
    """Only exact scalar/helper/ledger tests; NO N/H centre leaf producer."""
    checks = 0
    for step, count, reserve in ((F(1, 8), 58, F(19, 2048)),
                                 (F(1, 16), 115, F(19, 8192)),
                                 (F(1, 32), 229, F(19, 32768))):
        grid = complete_H_grid(step)
        require(len(grid) == count and F(19, 32) * step ** 2 == reserve, "Exact generic physical grid/reserve")
        checks += 1
    outside_seed = geometry_factory.nominal_root_data(F(739, 2500), F(0))
    require(outside_seed["rhoQ_square"] > geometry_factory.point.ROOT_CAP ** 2
            and outside_seed["rhoQ_square"] < RHO_CAP ** 2
            and generic_characteristic_correctly_scaled(F(1, 8), outside_seed), "Actual root point beyond OLD seed cap is accepted")
    checks += 1
    # Contact4 gives a genuine disjointness witness, not just a wider
    # correctly-rounded interval that happens to overlap the legacy one.
    root = geometry_factory.nominal_root_data(F(1, 16), F(0))
    q = F(3)
    precise = independent_degree120_exponential(F(12))
    negative = integer.weighted_rectangle(F(1, 32), integer.conjugate_rectangle(precise))
    positive = integer.weighted_rectangle(F(1, 32), precise)
    zero = integer.fraction_interval(F(15, 16))
    independent_CF = (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
                      negative[2] + positive[2], negative[3] + positive[3])
    legacy = center.nominal_backend.generic_characteristic(q, root)  # deliberately flawed PURE scalar regression only
    corrected = generic_characteristic_correctly_scaled(q, root)
    require(legacy[0] > independent_CF[1] or legacy[1] < independent_CF[0]
            or legacy[2] > independent_CF[3] or legacy[3] < independent_CF[2],
            "Legacy physical-tail CF bracket misses an independent rigorous higher-degree CF")
    require(corrected[0] <= independent_CF[0] <= independent_CF[1] <= corrected[1]
            and corrected[2] <= independent_CF[2] <= independent_CF[3] <= corrected[3],
            "Correctly scaled CF encloses independent degree120 bracket")
    checks += 2
    # Also expose the bug at a TRUE necessary-root point that the OLD
    # seeded nominal entry accepted: b=sqrt(40/9), a=sqrt(5/18),
    # rhoQ^2=289/90<ROOT_CAP^2. No support/root-domain objection applies.
    root_feasible = geometry_factory.nominal_root_data(F(9, 10), F(3, 5))
    q_feasible = F(1533, 512)
    require(root_feasible["rhoQ_square"] < geometry_factory.point.ROOT_CAP ** 2
            and root_feasible["rhoQ_square"] < RHO_CAP ** 2,
            "Second CF unit witness lies in the TRUE physical and old seeded moment roots")
    rigorous_CF = independent_degree120_characteristic(q_feasible, root_feasible)
    old_CF = center.nominal_backend.generic_characteristic(q_feasible, root_feasible)
    new_CF = generic_characteristic_correctly_scaled(q_feasible, root_feasible)
    require(old_CF[3] < rigorous_CF[2],
            "Legacy generic CF IMAGINARY upper misses a true root-feasible independent interval")
    require(new_CF[0] <= rigorous_CF[0] <= rigorous_CF[1] <= new_CF[1]
            and new_CF[2] <= rigorous_CF[2] <= rigorous_CF[3] <= new_CF[3],
            "Correctly scaled CF encloses true irrational-contact root-feasible interval")
    checks += 3
    for a in (F(0), F(1, 3), F(1)):
        for L, U in ((F(0), F(0)), (F(0), F(1, 8)), (F(1, 10), F(2, 5))):
            frequency = {"modulus": a, "weight_int": SCALE // 7,
                         "models": ((F(0), F(1, 2), "cube"), (F(1, 3), F(0), "mass"), (1 + a, F(0), "unit"))}
            receipt = frozen_complete_ABS_cell([frequency], F(1, 10), F(1), L, U)
            C, D = receipt["transfer_affine_upper"]
            for j in range(9):
                eta = L + (U - L) * F(j, 8)
                epsilon = min(eta / 2, F(1, 3), 1 + a)
                actual_transfer = algebra.direct_transfer(a, epsilon)
                require(C + D * eta >= F(SCALE // 7, SCALE) * actual_transfer,
                        "Frozen whole-cell transfer/rounding contains the complete quartic envelope")
                checks += 1
    require(fresh_target_certificate()["CE_lower_exact"] > TARGET, "Fresh CE target witness")
    checks += 1
    for arguments in (((.9, F(1), F(0), F(1, 10)), (F(0), F(1, 10)), 256, F(1, 32), 1, 1),
                      ((F(9, 10), F(1), F(0), F(1, 10)), (0.0, F(1, 10)), 256, F(1, 32), 1, 1),
                      ((F(9, 10), F(1), F(0), F(1, 10)), (F(0), F(1, 10)), True, F(1, 32), 1, 1)):
        try:
            checked_request(*arguments)
        except RuntimeError:
            checks += 1
        else:
            raise RuntimeError("Floating/bool proof input accepted")
    return {"status": "GENERIC_LOW_ETA_CENTER_ONLY_EXACT_TINY_TESTS_ONLY", "exact_checks": checks,
        "legacy_generic_CF_missing_scaled_tail_detected": True,
        "full_N_H_leaf_producer_called": False, "old_sources_or_receipts_modified": False,
        "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(tiny_regressions(), sort_keys=True))
