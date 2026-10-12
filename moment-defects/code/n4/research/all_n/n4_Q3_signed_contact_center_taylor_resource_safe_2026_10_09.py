"""Fresh exact SIGNED contact-Taylor Q3 center bounds ONLY, not a CDF gate.

The supplied BOX response table is an in-memory mathematical API object,
not a JSON receipt. Its A1/caches/Gamma/radii are not inspected as proof
premises here. Canonical geometry, kernels, nominal Q3 characteristic
rectangles, Gaussian centers, and ALL center derivatives are independently
rebuilt. The returned raw center bounds can replace the corresponding
center fields in a fresh box table without changing its A1 inequalities.
No physical quadrature or H interpolation reserve is added here.

For f(x)=exp(i*q*x), standardized Q3 at -a,0,b satisfies
 g=1+f[-a,0,b],
 ga=-f[-a,-a,0,b], gb=f[-a,0,b,b],
 gaa=2f[-a,-a,-a,0,b], gab=-f[-a,-a,0,b,b],
 gbb=2f[-a,0,b,b,b].
Hermite--Genocchi gives |ga|,|gb|<=q^3/6,
|gaa|,|gbb|<=q^4/12, |gab|<=q^4/24. These are intersected
with independently valid direct weight/exponential and moment-remnant
bounds, as SCALAR norm bounds, never polynomial-coefficient minima.

C_H=1+2Re sum kappa_H*g^4-2Phi(H/2) has
 Ci=8Re sum kappa_H*g^3*gi,
 |Cij|<=8 sum |kappa|[3*Di*Dj+Eij].
The first formula is summed with its SIGNS before an interval upper is
taken. The second uses |g|<=1 along feasible contact segments. The set
{a>0,b>=a,ab>=1} is convex (b>=1/a), so every segment between
the true nominal and any actual probability reference is feasible. We
DO NOT assume a w,beta rectangle is convex in its contact image, or use
its tighter actual-g cap on intermediate segments.

Derivatives are evaluated at exact rational contacts a_bar=a_nom_hi/S,
b_bar=b_nom_hi/S, just above the true irrational nominal contacts.
Both are still a probability Q3. The TRUE nominal center baseline is
rebuilt and retained; it is not replaced by the rational-center baseline.
Hessian envelopes times the root-bracket widths enclose the difference
between rational and true nominal gradients. Signed linear contact
increments plus a uniform quadratic remainder then cover the WHOLE box.
This Taylor bound is intersected with an independently freshly rebuilt
HG/moment-matched absolute center bound. No numeric source hash, saved
status, supplied center value, or floating bound is a proof premise.

A nominal Q needs probability/standardization/contact<=17/4 only. There
is no LOW-rho or eta-seed-cap requirement at the expansion point. The
later CDF consumer still owns all physical premises, eta, denominator,
tails, A1/Gamma/radius/R2, quadrature and H reserves. This file proves no
whole-fibre CDF claim or unrestricted C4. CLI runs only tiny exact tests;
there is no producer CLI or file write. A coordinated consumer may call
the fresh API with its existing in-memory box table (60s/256MiB guard).
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_windows_resource_guard_2026_10_09 as resources

import n4_Q3_contact_coordinate_derivative_algebra_2026_10_08 as derivatives
import n4_Q3_exact_common_signed_response_table_2026_10_08 as nominal_backend
import n4_Q3_exact_box_common_signed_response_v2_2026_10_08 as box_backend

integer, arithmetic, SCALE = nominal_backend.integer, nominal_backend.exact, nominal_backend.SCALE
RADIUS = F(17, 4)
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
H_GRID = tuple(F(-4) + F(j, 32) for j in range(229))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact(value):
    require(type(value) in (F, int), "Exact Fraction/int arithmetic only")
    return F(value)


def interval(values):
    require(type(values) in (tuple, list) and len(values) == 2, "Exact two-endpoint interval")
    lo, hi = map(exact, values)
    require(lo <= hi, "Ordered exact interval")
    return lo, hi


def direct_derivative_majorants(q, a_interval, b_interval):
    """Uniform direct weight/exponential norms, useful at high q.

    g=p0+pm*exp(-iqa)+pp*exp(iqb). All absolute weight-derivative
    formulas decrease in each positive contact, so lower endpoints
    suffice. This estimate makes no probability claim about corners.
    """
    q = exact(q)
    al, ah = interval(a_interval)
    bl, bh = interval(b_interval)
    require(q >= 0 and al > 0 and bl > 0, "Positive physical derivative domain")
    s = al + bl
    pm, pp = 1 / (al * s), 1 / (bl * s)
    pma = 1 / (al ** 2 * s) + 1 / (al * s ** 2)
    pmb = 1 / (al * s ** 2)
    ppa = 1 / (bl * s ** 2)
    ppb = 1 / (bl ** 2 * s) + 1 / (bl * s ** 2)
    p0a, p0b = 1 / (al ** 2 * bl), 1 / (al * bl ** 2)
    pmaa = 2 / (al ** 3 * s) + 2 / (al ** 2 * s ** 2) + 2 / (al * s ** 3)
    ppaa = 2 / (bl * s ** 3)
    pmbb = 2 / (al * s ** 3)
    ppbb = 2 / (bl ** 3 * s) + 2 / (bl ** 2 * s ** 2) + 2 / (bl * s ** 3)
    pmab = 1 / (al ** 2 * s ** 2) + 2 / (al * s ** 3)
    ppab = 1 / (bl ** 2 * s ** 2) + 2 / (bl * s ** 3)
    return {
        "ga": p0a + pma + ppa + q * pm,
        "gb": p0b + pmb + ppb + q * pp,
        "gaa": 2 / (al ** 3 * bl) + pmaa + ppaa + 2 * q * pma + q ** 2 * pm,
        "gab": 1 / (al ** 2 * bl ** 2) + pmab + ppab + q * (pmb + ppa),
        "gbb": 2 / (al * bl ** 3) + pmbb + ppbb + 2 * q * ppb + q ** 2 * pp,
    }


def contact_derivative_majorants(q, a_interval, b_interval):
    """Intersection of three complete scalar analytic norm uppers."""
    q = exact(q)
    require(q >= 0, "Nonnegative physical frequency")
    hg = {"ga": q ** 3 / 6, "gb": q ** 3 / 6,
          "gaa": q ** 4 / 12, "gab": q ** 4 / 24, "gbb": q ** 4 / 12}
    direct = direct_derivative_majorants(q, a_interval, b_interval)
    matched = derivatives.derivative_majorants(q, a_interval, b_interval)
    return {key: min(hg[key], direct[key], matched[key]) for key in hg}


def center_hessian_majorants(frequencies, a_interval, b_interval):
    """Whole-feasible-path |Caa|,|Cab|,|Cbb| using |g|<=1."""
    haa = hab = hbb = F(0)
    for item in frequencies:
        q = exact(item["q"])
        k = item["kernel_modulus_upper_int"]
        require(type(k) is int and k >= 0, "Outward kernel norm integer")
        m = contact_derivative_majorants(q, a_interval, b_interval)
        weight = F(8 * k, SCALE)
        haa += weight * (3 * m["ga"] ** 2 + m["gaa"])
        hab += weight * (3 * m["ga"] * m["gb"] + m["gab"])
        hbb += weight * (3 * m["gb"] ** 2 + m["gbb"])
    return haa, hab, hbb


def expand_true_nominal_gradient(gradient_a_int, gradient_b_int,
                                 nominal_shift_a, nominal_shift_b, hessian):
    """Enclose true-nominal gradients from rational-above-nominal ones."""
    ga, gb = gradient_a_int, gradient_b_int
    require(all(type(x) is int for x in (*ga, *gb)) and ga[0] <= ga[1] and gb[0] <= gb[1],
            "Ordered integer signed-gradient intervals")
    ea, eb = map(exact, (nominal_shift_a, nominal_shift_b))
    haa, hab, hbb = map(exact, hessian)
    require(min(ea, eb, haa, hab, hbb) >= 0, "Nonnegative proven shifts/Hessians")
    enlarge_a = integer.ceil_fraction_scaled(haa * ea + hab * eb)
    enlarge_b = integer.ceil_fraction_scaled(hab * ea + hbb * eb)
    return ((ga[0] - enlarge_a, ga[1] + enlarge_a),
            (gb[0] - enlarge_b, gb[1] + enlarge_b))


def whole_box_taylor_upper_int(nominal_upper_int, gradient_a_int, gradient_b_int,
                               delta_a_interval, delta_b_interval, hessian):
    """Outward signed-linear plus quadratic remainder, scale S."""
    require(type(nominal_upper_int) is int, "True nominal raw-center upper integer")
    ga = tuple(F(x, SCALE) for x in gradient_a_int)
    gb = tuple(F(x, SCALE) for x in gradient_b_int)
    upper = derivatives.joint_taylor_upper(F(nominal_upper_int, SCALE), ga, gb,
        interval(delta_a_interval), interval(delta_b_interval), hessian)
    return integer.ceil_fraction_scaled(upper)


def base_derivative_blocks(q, kernel, a_bar, b_bar):
    """Both TRUE reflections at rational probability contacts, no eta cap."""
    values = derivatives.nominal_derivative_rectangles(q, a_bar, b_bar)
    # Every rational reference here is a probability; coordinate unit
    # intersection is valid. It is not a claim about a contact-box corner.
    g = arithmetic.unit_phase_intersection(values["g"])
    blocks = {}
    for orientation in (1, -1):
        characteristic = g if orientation == 1 else integer.conjugate_rectangle(g)
        ga = values["ga"] if orientation == 1 else integer.conjugate_rectangle(values["ga"])
        gb = values["gb"] if orientation == 1 else integer.conjugate_rectangle(values["gb"])
        cube = arithmetic.complex_multiply(arithmetic.complex_multiply(characteristic, characteristic), characteristic)
        blocks[orientation] = tuple(tuple(8 * value for value in arithmetic.complex_multiply(kernel,
            arithmetic.complex_multiply(cube, derivative))) for derivative in (ga, gb))
    return blocks


def sum_signed_gradient_intervals(blocks, H, N, guard=lambda: None):
    """Real signed sums across q first; arithmetic midpoint phase recurrence."""
    require(type(H) is F and type(N) is int and N > 0 and len(blocks) == N, "Exact phase grid")
    phase = arithmetic.exponential_exact_argument(-3 * H / (2 * N))
    ratio = arithmetic.exponential_exact_argument(-3 * H / N)
    accumulated = {orientation: [[0, 0], [0, 0]] for orientation in (1, -1)}
    for item in blocks:
        guard()
        for orientation in (1, -1):
            for index, block in enumerate(item[orientation]):
                value = arithmetic.complex_multiply(phase, block)
                accumulated[orientation][index][0] += value[0]
                accumulated[orientation][index][1] += value[1]
        phase = arithmetic.unit_phase_intersection(arithmetic.complex_multiply(phase, ratio))
    return {orientation: tuple(tuple(pair) for pair in values) for orientation, values in accumulated.items()}


def canonical_inputs(table, rectangle=None, N=None, H_grid=None):
    """Rebuild roots, do not trust numeric table geometry/status/hash."""
    require(type(table) is dict and table.get("scale") == SCALE, "Declared exact in-memory scale")
    table_box = table["box_geometry"]
    selected_rectangle = tuple(table_box["rectangle"] if rectangle is None else rectangle)
    require(selected_rectangle == tuple(table_box["rectangle"]), "Expected exact rectangle labels")
    box, nominal, bridge = box_backend.canonical_geometry(selected_rectangle)
    for key in ("a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket", "w_interval", "beta_abs_interval"):
        require(tuple(table_box[key]) == tuple(box[key]), "Fresh actual geometry agrees: " + key)
    supplied_nominal = table["nominal_root_data"]
    for key in ("w", "beta", "a_square", "b_square", "a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket"):
        require(supplied_nominal[key] == nominal[key], "Nominal is NOT actual BOX geometry: " + key)
    selected_N = table["N"] if N is None else N
    require(type(selected_N) is int and selected_N in (256, 512) and table["N"] == selected_N,
            "Exact physical frequency N256/512")
    selected_H = tuple(table["metadata"]["H_grid"] if H_grid is None else H_grid)
    require(selected_H == tuple(table["metadata"]["H_grid"]) and 1 <= len(selected_H) <= 229
            and len(set(selected_H)) == len(selected_H)
            and all(type(H) is F and F(-4) <= H <= F(25, 8) for H in selected_H), "Exact unique declared H grid")
    frequency_data = table["frequency_data"]
    require(len(frequency_data) == selected_N and all(item["q"] == F(3 * (2 * j + 1), 2 * selected_N)
            for j, item in enumerate(frequency_data)), "Exact complete physical q labels")
    rows = table["rows"]
    expected = {(orientation, H) for H in selected_H for orientation in (1, -1)}
    require(len(rows) == len(expected) and {(row["orientation"], row["H"]) for row in rows} == expected,
            "Complete selected H/both-reflection rows")
    a_bar, b_bar = F(nominal["a_bracket"][1], SCALE), F(nominal["b_bracket"][1], SCALE)
    derivatives.coordinates(a_bar, b_bar)
    require(b_bar <= RADIUS, "Rational expansion center inside supported contact domain")
    # A bar endpoint may differ from the true nominal by one scale unit;
    # its value is included in the same full contact rectangle for all paths.
    ai, bi = tuple(F(x, SCALE) for x in box["a_bracket"]), tuple(F(x, SCALE) for x in box["b_bracket"])
    require(ai[0] <= a_bar <= ai[1] and bi[0] <= b_bar <= bi[1], "Reference bar inside full interval envelope")
    da = (F(box["a_bracket"][0] - nominal["a_bracket"][1], SCALE),
          F(box["a_bracket"][1] - nominal["a_bracket"][0], SCALE))
    db = (F(box["b_bracket"][0] - nominal["b_bracket"][1], SCALE),
          F(box["b_bracket"][1] - nominal["b_bracket"][0], SCALE))
    ea = F(nominal["a_bracket"][1] - nominal["a_bracket"][0], SCALE)
    eb = F(nominal["b_bracket"][1] - nominal["b_bracket"][0], SCALE)
    return box, nominal, bridge, selected_N, selected_H, ai, bi, a_bar, b_bar, da, db, ea, eb


def compute_verified_box_center_taylor(table, rectangle=None, N=None, H_grid=None,
                                       time_limit_seconds=TIME_LIMIT):
    """Fresh center-only arithmetic; never executes a nominal/BOX A1 producer.

    Existing raw center upper values are CHECKED against independently
    rebuilt baseline+triangle bounds, not trusted. Neither A1 arrays nor
    modulus caches are copied. To preserve other inequalities, a consumer
    can join these rows by exact (orientation,H) into its same fresh table.
    """
    started = time.monotonic()
    require(type(time_limit_seconds) in (int, float) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic cooperative budget <=60s")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Center Taylor elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Center Taylor working-set budget")
    inputs = canonical_inputs(table, rectangle, N, H_grid)
    box, nominal, bridge, N, selected_H, ai, bi, a_bar, b_bar, da, db, ea, eb = inputs
    pi, phi0 = arithmetic.pi_and_phi0()
    blocks, nominal_fourth, frequencies = [], {1: [], -1: []}, []
    triangle_exact = F(0)
    delta_a, delta_b = max(map(abs, da)), max(map(abs, db))
    for j in range(N):
        guard()
        q = F(3 * (2 * j + 1), 2 * N)
        kernel = arithmetic.kernel_rectangle(F(2 * j + 1, 2 * N), N, 32, pi)
        require(tuple(table["frequency_data"][j]["kernel_rectangle"]) == kernel, "Fresh kernel rectangle, not receipt trust")
        k = integer.rectangle_modulus_upper(kernel)
        require(table["frequency_data"][j]["kernel_modulus_upper_int"] == k, "Fresh kernel norm, not receipt trust")
        frequencies.append({"q": q, "kernel_modulus_upper_int": k})
        blocks.append(base_derivative_blocks(q, kernel, a_bar, b_bar))
        g0 = nominal_backend.generic_characteristic(q, nominal)
        a0 = min(SCALE, integer.rectangle_modulus_upper(g0))
        old_Eg = box_backend.reference_bridge.reference_error(q, bridge)
        Eg = integer.ceil_fraction_scaled(min(old_Eg, q ** 3 * (delta_a + delta_b) / 6))
        D4 = arithmetic.quartic_absolute_upper(Eg, a0)
        triangle_exact += F(2 * k * D4, SCALE ** 2)
        for orientation, characteristic in ((1, g0), (-1, integer.conjugate_rectangle(g0))):
            square = arithmetic.complex_multiply(characteristic, characteristic)
            fourth = arithmetic.complex_multiply(square, square)
            nominal_fourth[orientation].append(arithmetic.complex_multiply(kernel, fourth))
    triangle_margin_int = integer.ceil_fraction_scaled(triangle_exact)
    hessian = center_hessian_majorants(frequencies, ai, bi)
    indexed_source_rows = {(row["orientation"], row["H"]): row for row in table["rows"]}
    rows = []
    for H in selected_H:
        guard()
        gradient_by_orientation = sum_signed_gradient_intervals(blocks, H, N, guard)
        phase = arithmetic.exponential_exact_argument(-3 * H / (2 * N))
        ratio = arithmetic.exponential_exact_argument(-3 * H / N)
        sums = {1: 0, -1: 0}
        for j in range(N):
            for orientation in (1, -1):
                sums[orientation] += arithmetic.complex_multiply(phase, nominal_fourth[orientation][j])[1]
            phase = arithmetic.unit_phase_intersection(arithmetic.complex_multiply(phase, ratio))
        normal = arithmetic.normal_cdf_interval(H / 2, phi0)
        for orientation in (1, -1):
            source = indexed_source_rows[(orientation, H)]
            nominal_upper = SCALE + 2 * sums[orientation] - 2 * normal[0]
            require(type(source["nominal_raw_Q_center_upper_int"]) is int
                    and source["nominal_raw_Q_center_upper_int"] == nominal_upper,
                    "True nominal raw center FRESH arithmetic match; no rational-baseline substitution")
            bar_a, bar_b = gradient_by_orientation[orientation]
            grad_a, grad_b = expand_true_nominal_gradient(bar_a, bar_b, ea, eb, hessian)
            taylor = whole_box_taylor_upper_int(nominal_upper, grad_a, grad_b, da, db, hessian)
            triangle = nominal_upper + triangle_margin_int
            # The supplied old bound is diagnostic only. This intersection
            # uses TWO freshly independently rebuilt whole-box bounds.
            require(type(source["raw_Q_center_upper_int"]) is int
                    and source["raw_Q_center_upper_int"] >= triangle,
                    "Existing corrected raw center is at least the rebuilt HG/matched absolute bound")
            selected = min(taylor, triangle)
            rows.append({"orientation": orientation, "H": H,
                "nominal_raw_Q_center_upper_int": nominal_upper,
                "rational_reference_gradient_a_interval_int": bar_a,
                "rational_reference_gradient_b_interval_int": bar_b,
                "true_nominal_gradient_a_interval_int": grad_a,
                "true_nominal_gradient_b_interval_int": grad_b,
                "raw_Q_center_Taylor_upper_int": taylor,
                "raw_Q_center_absolute_upper_int": triangle,
                "supplied_previous_raw_center_upper_int_diagnostic_only": source["raw_Q_center_upper_int"],
                "raw_Q_center_upper_int": selected,
                "Taylor_selected": taylor < triangle,
                "physical_or_H_reserves_added": False})
    guard()
    files = (Path(__file__), Path(derivatives.__file__), Path(nominal_backend.__file__),
             Path(box_backend.__file__), Path(arithmetic.__file__), Path(integer.__file__), Path(resources.__file__))
    return {"status": "FRESH_INTEGER_OUTWARD_SIGNED_CONTACT_TAYLOR_BOX_Q_CENTER_ONLY",
        "scale": SCALE, "N": N, "box_geometry": box, "nominal_root_data": nominal, "rows": rows,
        "metadata": {"H_grid": selected_H, "orientations": (1, -1),
            "rational_reference_contacts": (a_bar, b_bar),
            "nominal_root_shift_upper": (ea, eb), "actual_minus_true_nominal_contact_intervals": (da, db),
            "uniform_raw_center_Hessian_abs_bounds": hessian,
            "fresh_absolute_center_margin_upper_int": triangle_margin_int,
            "signed_frequency_sum_before_linear_upper": True,
            "true_nominal_baseline_rebuilt_unchanged": True,
            "probability_path_justification": "ab>=1 is epigraph b>=1/a; intersection with b>=a convex. Actual, true nominal and rational-above-nominal references are probabilities. Use |g|<=1 only along their segments, not all rectangle corners.",
            "g_derivative_majorants": "min(HG order3/order4 volumes, direct weights+unit exponentials, matched moment-remnant quotient), independently valid scalar bounds",
            "center_hessian": "8sum|kappa|*(3DiDj+Eij), p=1 on feasible segments",
            "seed_cap_imposed_at_expansion_reference": False,
            "table_center_numbers_or_status_trusted_as_proof": False,
            "A1_Gamma_radius_or_R2_bounds_modified": False,
            "physical_quadrature_or_H_reserves_added": False,
            "Taylor_selected_row_count": sum(row["Taylor_selected"] for row in rows)},
        "premises": "The original law's TRUE Q3 w,beta-magnitude parameters belong to the declared box; standardized references have nonnegative masses. Later CDF work needs the separately supplied physical owner/rho/support inputs. This module supplies finite raw Q-center bounds only, for its stated H nodes and reflections.",
        "conclusions": {"box_reference_center_integer_outward": True,
            "whole_H_continuum_or_tails_proved_here": False, "CDF_bound_proved": False,
            "unrestricted_C4_proved": False, "old_sources_or_receipts_modified": False},
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "standard_library_only": True}}


def self_tests():
    checks = 0
    for a, b in ((F(1), F(1)), (F(1, 2), F(2)), (F(3, 4), F(7, 4))):
        for q in (F(0), F(1, 8), F(1), F(3)):
            values = derivatives.nominal_derivative_rectangles(q, a, b)
            majorants = contact_derivative_majorants(q, (a, a), (b, b))
            for name, bound in majorants.items():
                rect = values[name]
                norm_square = F(max(abs(rect[0]), abs(rect[1])) ** 2
                    + max(abs(rect[2]), abs(rect[3])) ** 2, SCALE ** 2)
                require(norm_square <= bound ** 2, "Tiny independent rectangle norm vs analytic contact majorants")
                checks += 1
    ma = contact_derivative_majorants(F(3), (F(2, 3), F(3, 4)), (F(3, 2), F(7, 4)))
    hg = {"ga": F(27, 6), "gb": F(27, 6), "gaa": F(81, 12), "gab": F(81, 24), "gbb": F(81, 12)}
    require(all(ma[name] <= bound for name, bound in hg.items()), "Scalar intersection never worse than HG")
    checks += 1
    H = (F(2), F(1), F(3))
    ga, gb = expand_true_nominal_gradient((-2 * SCALE, -SCALE), (3 * SCALE, 4 * SCALE),
        F(1, 10), F(1, 20), H)
    require(ga == (-integer.ceil_fraction_scaled(F(9, 4)), -integer.floor_fraction_scaled(F(3, 4)))
            and gb == (integer.floor_fraction_scaled(F(11, 4)), integer.ceil_fraction_scaled(F(17, 4))),
            "Hessian root-shift expansion includes both signs")
    checks += 1
    raw = whole_box_taylor_upper_int(SCALE, (-2 * SCALE, -SCALE), (3 * SCALE, 4 * SCALE),
        (F(-1, 10), F(1, 10)), (F(-1, 20), F(1, 20)), H)
    require(raw == integer.ceil_fraction_scaled(F(1) + F(2, 5) + F(15, 800)),
            "Whole-box signed products and quadratic Taylor units")
    checks += 1
    q, a, b = F(3, 2), F(3, 4), F(7, 4)
    # One-frequency algebra only: real kernel and H0 imply reflected
    # derivative real parts are exactly enclosed by conjugation.
    kernel = (SCALE // 3, integer.ceil_div(SCALE, 3), 0, 0)
    block = base_derivative_blocks(q, kernel, a, b)
    accumulated = sum_signed_gradient_intervals([block], F(0), 1)
    require(accumulated[1] == accumulated[-1], "TRUE conjugated reference gradient at H0/real kernel")
    checks += 1
    W, beta = F(243205, 266616), F(2, 5)
    rectangle = (W - F(1, 1000), W + F(1, 1000), beta - F(1, 1000), beta + F(1, 1000))
    box, nom, bridge = box_backend.canonical_geometry(rectangle)
    rational_a, rational_b = F(nom["a_bracket"][1], SCALE), F(nom["b_bracket"][1], SCALE)
    require(derivatives.coordinates(rational_a, rational_b)["pzero"] >= 0
            and box["a_bracket"][0] <= nom["a_bracket"][0] <= nom["a_bracket"][1] <= box["a_bracket"][1],
            "Rational-above-irrational center is a probability inside actual envelopes")
    checks += 1
    # Rational probability centers are allowed even outside the physical
    # low-rho cap; this test explicitly avoids any seeded point factory.
    require(derivatives.coordinates(F(2), F(2))["rhoQ"] == 2
            and derivatives.nominal_derivative_rectangles(F(1, 8), F(2), F(2))["ga"],
            "No rho/eta seed cap imposed on expansion probability reference")
    checks += 1
    try:
        direct_derivative_majorants(0.1, (F(1), F(1)), (F(1), F(1)))
        raise RuntimeError("Float proof input was accepted")
    except RuntimeError as error:
        require(str(error) == "Exact Fraction/int arithmetic only", "Float proof input rejected")
    checks += 1
    return {"status": "SIGNED_CONTACT_CENTER_TAYLOR_EXACT_TINY_TESTS_ONLY", "exact_checks": checks,
        "full_N_H_BOX_producer_called": False, "source_or_receipt_files_written_by_tests": False,
        "CDF_bound_proved": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
