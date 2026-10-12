"""Correct fresh generic WHOLE-box common signed A1 table; NO Gamma/CDF.

API fresh_generic_common_A1_response_table(rectangle,cache,guard) DIRECTLY
calls the audited linked3f50 normalized-center builder once. This gives
fresh correctly-scaled TRUE nominal CF rectangles, WHOLE-box raw and
normalized centers, ACTUAL-reference modulus caps p, and nominal/actual
geometry kept separate. The cache must come from the DIRECT fresh audited
quadrature builder. Status/schema/source hashes/numeric JSON do not prove
any of those mathematical premises. Raw and normalized centers remain
distinct, and this module changes neither original field.

Only the retained legacy PURE homogeneous_table, common_coefficients and
cell_uppers are reused. NEVER call its flawed generic_characteristic, its
old point/root/price-seed producer, its old timed/high-level entry points,
or its per-call leaking resource monitor. Fresh HG coefficients and tails
are assembled HERE with explicit fixed-point units. The only other old
integer response primitive used is the pure truncated response_rectangle.

For sign sigma and contact c, with R=17/4, y_j=j/64, h=1/64,

 r_q(sigma*y)=sum_(n=0)^60 (i*sigma)^(n+3)*b_(q,n)*hhat_n+E_q,
 b_0=q^3/6, b_n=b_(n-1)*(qR)/(n+3),
 hhat_0=1, hhat_n=(y/R)*hhat_(n-1)+(n+1)*(c/R)^n.

Hermite--Genocchi gives |E_q|<=q^3/6*(qR)^61/61!, no exponential factor,
and |partial_y r_q|<=q^4/24. The half-cell margin is q^4*h/48. Both
positive margins are FIRST CEILED after multiplying by SCALE. Unlike
the quarantined legacy CF helper, physical remainders are never passed
as fixed-point integers. Each nearest-node CLOSED cell is clipped to
[0,R], and contains the original response including endpoints/contact
limits. No division at y=0 or y=c is used to evaluate the response.

At a raw threshold H let Z_H(q)=4*kappa_H(q)*g_nominal(q)^3. For each
orientation/sign, common_coefficients sums SIGNED real coefficients
Re[Z_H(q)*(i*sigma)^(n+3)]*b_(q,n) across q BEFORE any y dot or supremum.
cell_uppers then dots them with positive hhat intervals. The complete HG
tail and ORIGINAL-response y half-cell mesh are added ONCE afterwards,
with TRUE |Z_H(q)|<=4*|kappa(q)|*a0(q)^3, a0>=|g_nominal|. Phase norm
is exactly one; rectangle uncertainty is enclosed in the polynomial.
No independent absolute value is substituted for the signed q sum.

WHOLE-box correction, not a nominal-only response
------------------------------------------------
The same fresh table proves |g_actual-g_nominal|<=e and |g_actual|<=p,
|g_nominal|<=a0. Hence D3=e*(p^2+p*a0+a0^2) bounds their cube difference.
Fresh nominal modulus cells contain |r_nominal| including HGtail+mesh;
their scalar intersection with q^3/6 is another WHOLE-cell bound R0.
For Delta_c>=|c_actual-c_nominal|, |partial_c r|<=q^4/12 gives

 M_c(cell)=sum_q 4|kappa(q)|[D3(q)*R0(q,cell)+p(q)^3*q^4*Delta_c/12].

This follows from gA^3*rA-g0^3*r0=(gA^3-g0^3)*r0+gA^3*(rA-r0).
It is uniform over the WHOLE geometry box and closed y cell. Add M_c to
the already CLOSED nominal A1 upper, without another HGtail or y mesh.
We also intersect M_c with the independently valid global q^3/6 version
as complete scalar bounds, never as polynomial coefficients. The RAW
nominal modulus cache is retained unchanged, not q^3-normalized/clipped.

Orientation+: g_nominal, positive contact b/sign+, negative a/sign-.
Orientation-: conjugate(g_nominal), positive contact a/sign+, negative b/sign-.
Thus contact homogeneous tables and M_a/M_b arrays SWAP on reflection;
the polynomial sign still follows the physical positive/negative tag.
The SAME raw-H phase is used, not its conjugate or a naive CDF complement.

Proof boundary for a future consumer
-----------------------------------
For actual standardized P, eta=E W=rhoP-rhoQ>=0, owner support |X|<=R,
and eta>0, the SAME positive probability nu=W*P/eta satisfies
delta_q=phiP(q)-g_actual(q)=eta*E_nu r_q. Then A1 is this table's
Re sum4*kappa*g_actual^3*r_actual and the original finite raw transfer
has linear part2*eta*E_nu A1. A Gamma dual proving eta*E_nu A1<=A+eta*S
must therefore be multiplied by2 by the raw CDF consumer, with its
complete quartic remainder also counted at raw factor2. At eta0, delta0
holds directly without defining nu. No Gamma prices, eta optimization,
R2, CDF acceptance, physical reserves, tails/coverage or C4 theorem are
computed here. Original P need not be finitely supported.

Streaming one H at a time, no q*y*H tensor. Caller owns the cooperative
time/256MiB guard; it is called between every bounded outer operation.
SOURCE ONLY until authorized. Dormant tiny tests are scalar HG/algebra
checks, not a cache/CF/table producer. No producer/replay/file-write CLI.
All older sources/receipts remain untouched; hashes are integrity only.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from math import factorial
from pathlib import Path

import n4_Q3_fresh_linked_w_beta_normalized_center_2026_10_09 as linked_center
import n4_Q3_exact_common_signed_response_table_2026_10_08 as HG

cached = linked_center.contact_center.cached
quad, integer, arithmetic = cached.quadrature, cached.integer, cached.arithmetic
SCALE, TARGET, require = cached.SCALE, cached.TARGET, cached.require
RADIUS, Y_STEP, DEGREE, Y_NODES = F(17, 4), F(1, 64), 60, 273
LINKED_CENTER_PIN = "3f50db40de37b5220ee1ce011f62f4f9e5d3429af61be5c871c604c8d952c523"


def source_drift_check():
    linked_center.source_drift_check()
    require(hashlib.sha256(Path(linked_center.__file__).read_bytes()).hexdigest() == LINKED_CENTER_PIN,
            "Frozen corrected builder integrity, not proof from a hash")
    require(SCALE == HG.SCALE and DEGREE == HG.DEGREE and RADIUS == HG.RADIUS
            and Y_STEP == HG.STEP and integer is HG.integer and arithmetic is HG.exact,
            "Same exact PURE HG coefficient/normalization units and arithmetic modules")


def fresh_HG_frequency_data(q_grid, guard):
    """Positive coefficient intervals and SCALED tail/mesh; no old producer."""
    require(type(q_grid) in (tuple, list) and len(q_grid) > 0 and callable(guard),
            "Exact physical frequency grid and caller guard")
    data = []
    for q in q_grid:
        guard()
        require(type(q) is F and 0 < q <= 3, "Exact positive raw frequency")
        qr = integer.fraction_interval(q * RADIUS)
        require(qr[0] == qr[1], "qR exactly representable at this fixed-point scale")
        coefficients = [integer.fraction_interval(q ** 3 / 6)]
        require(coefficients[0][0] == coefficients[0][1], "Exact dyadic cubic coefficient")
        for n in range(1, DEGREE + 1):
            previous = coefficients[-1]
            coefficients.append((previous[0] * qr[0] // (SCALE * (n + 3)),
                integer.ceil_div(previous[1] * qr[1], SCALE * (n + 3))))
        tail = integer.ceil_fraction_scaled(q ** 3 * (q * RADIUS) ** 61 / (6 * factorial(61)))
        mesh = integer.ceil_fraction_scaled(q ** 4 * Y_STEP / 48)
        require(type(tail) is int and type(mesh) is int and tail >= 0 and mesh >= 0
                and len(coefficients) == 61 and all(0 <= lo <= hi for lo, hi in coefficients),
                "OUTWARD fixed-point tails and all61 positive coefficient intervals")
        data.append({"q": q, "coefficients": coefficients, "HG_tail": tail, "mesh": mesh})
    return data


def checked_homogeneous_table(contact_bracket):
    """ONLY retained PURE homogeneous-table builder, with no zip truncation."""
    require(type(contact_bracket) in (tuple, list) and len(contact_bracket) == 2
            and all(type(x) is int for x in contact_bracket)
            and 0 < contact_bracket[0] <= contact_bracket[1] <= RADIUS * SCALE,
            "TRUE nominal contact bracket inside the HG response domain")
    table = HG.homogeneous_table(contact_bracket)
    require(len(table) == Y_NODES and all(len(row) == 61
        and all(type(lo) is int and type(hi) is int and 0 <= lo <= hi for lo, hi in row) for row in table),
        "All273 positive homogeneous61 rows, never silently truncated")
    return table


def fresh_nominal_modulus_cache(data, homogeneous_a, homogeneous_b, nominal, guard):
    """RAW |r| upper in EACH closed cell; HGtail+mesh included ONCE."""
    arrays = {}
    for name, table in (("a", homogeneous_a), ("b", homogeneous_b)):
        rows = []
        for homogeneous in table:
            guard()
            row = []
            for item in data:
                rectangle = integer.response_rectangle(item["coefficients"], homogeneous)
                # Conjugating the response for negative physical sign preserves its norm.
                row.append(integer.rectangle_modulus_upper(rectangle) + item["HG_tail"] + item["mesh"])
            rows.append(row)
        arrays[name] = rows
    return {"scale": SCALE, "N": len(data), "R": RADIUS, "y_step": Y_STEP,
        "HG_degree": DEGREE, "q_grid": tuple(item["q"] for item in data),
        "nominal_root_data": nominal,
        "a_cell_modulus_upper_int": arrays["a"], "b_cell_modulus_upper_int": arrays["b"],
        "includes_HG_tail_and_y_mesh": True,
        "cell_arrays_are_RAW_r_modulus_not_q_cubic_normalized": True}


def box_geometry_margins(frequency_data, data, nom_mod_cache, delta_a, delta_b, guard):
    """Complete WHOLE-box M_a/M_b(cell), plus unchanged raw cache diagnostics."""
    require(len(frequency_data) == len(data) == nom_mod_cache["N"]
            and type(delta_a) is F and type(delta_b) is F and min(delta_a, delta_b) >= 0,
            "Same fresh q rows and positive PHYSICAL knot-motion uppers")
    factors, cube_caps, global_first_scale3 = [], [], 0
    motion_a = motion_b = F(0)
    for item, hg in zip(frequency_data, data):
        guard()
        require(item["q"] == hg["q"], "Exact matching HG/CF frequency")
        k, a0, p, e = (item["kernel_modulus_upper_int"], item["g_nominal_modulus_upper_int"],
                      item["g_actual_modulus_upper_int"], item["Eg_upper_int"])
        require(all(type(value) is int for value in (k, a0, p, e))
                and k >= 0 and 0 <= a0 <= p <= SCALE and e >= 0,
                "Fresh actual/nominal modulus and cube-error premisses at SAME scale")
        D3 = integer.ceil_div(e * (p * p + p * a0 + a0 * a0), SCALE ** 2)
        factor = 4 * k * D3
        cube = hg["coefficients"][0][1]
        require(hg["coefficients"][0][0] == cube
                and F(cube, SCALE) == hg["q"] ** 3 / 6, "Exact global cubic response cap")
        factors.append(factor)
        cube_caps.append(cube)
        global_first_scale3 += factor * cube
        movement_weight = 4 * F(k, SCALE) * F(p, SCALE) ** 3 * hg["q"] ** 4 / 12
        motion_a += movement_weight * delta_a
        motion_b += movement_weight * delta_b
    global_first = integer.ceil_div(global_first_scale3, SCALE ** 2)
    arrays, globals_by_tag, motion_by_tag, improved = {}, {}, {}, {}
    for name, motion in (("a", motion_a), ("b", motion_b)):
        motion_int = integer.ceil_fraction_scaled(motion)
        global_int = global_first + motion_int
        margins = []
        for row in nom_mod_cache[name + "_cell_modulus_upper_int"]:
            guard()
            require(len(row) == len(data) and all(type(raw) is int and raw >= 0 for raw in row),
                    "Complete RAW nominal modulus cell")
            first_scale3 = sum(factor * min(raw, cube)
                              for factor, raw, cube in zip(factors, row, cube_caps))
            candidate = integer.ceil_div(first_scale3, SCALE ** 2) + motion_int
            margins.append(min(candidate, global_int))
        require(len(margins) == Y_NODES and all(0 <= value <= global_int for value in margins),
                "All273 complete local/global scalar intersections")
        arrays[name], globals_by_tag[name] = margins, global_int
        motion_by_tag[name] = motion_int
        improved[name] = sum(value < global_int for value in margins)
    return arrays, {"physical_contact_delta_uppers": (delta_a, delta_b),
        "global_complete_geometry_margin_upper_int": globals_by_tag,
        "contact_motion_margin_upper_int": motion_by_tag,
        "cellwise_margin_sharpened_counts": improved,
        "nominal_RAW_modulus_cache_not_modified": True}


def fresh_generic_common_A1_response_table(rectangle, cache, guard):
    """DIRECT fresh corrected linked table + streamed complete signed A1 rows."""
    require(callable(guard), "Caller-owned cooperative time/256MiB guard")
    guard()
    source_drift_check()
    quad.validate_preverified_fresh_cache(cache)
    require(cache.N == 256, "Initial correct generic physical q grid fixedN256")
    table = linked_center.fresh_normalized_center_table(rectangle, cache, guard)
    nominal, box, frequency_data = table["nominal_root_data"], table["box_geometry"], table["frequency_data"]
    require(table["scale"] == SCALE and table["N"] == cache.N and len(frequency_data) == cache.N
            and tuple(table["metadata"]["H_grid"]) == tuple(cache.H_grid)
            and tuple(box["rectangle"]) == tuple(rectangle), "SAME entire geometry/q/H scale")
    for name in ("a", "b"):
        nl, nh = nominal[name + "_bracket"]
        al, ah = box[name + "_bracket"]
        require(0 < al <= nl <= nh <= ah <= RADIUS * SCALE,
                "Whole actual/TRUE nominal contact envelopes inside owner response domain")
    data = fresh_HG_frequency_data(cache.q_grid, guard)
    require(all(item["q"] == hg["q"] == F(3 * (2 * j + 1), 2 * cache.N)
                for j, (item, hg) in enumerate(zip(frequency_data, data))), "ALL exact physical frequencies")
    homogeneous_a = checked_homogeneous_table(nominal["a_bracket"])
    homogeneous_b = checked_homogeneous_table(nominal["b_bracket"])
    nom_mod_cache = fresh_nominal_modulus_cache(data, homogeneous_a, homogeneous_b, nominal, guard)
    delta_a = F(max(nominal["a_bracket"][1] - box["a_bracket"][0],
                    box["a_bracket"][1] - nominal["a_bracket"][0]), SCALE)
    delta_b = F(max(nominal["b_bracket"][1] - box["b_bracket"][0],
                    box["b_bracket"][1] - nominal["b_bracket"][0]), SCALE)
    margins, geometry_metadata = box_geometry_margins(
        frequency_data, data, nom_mod_cache, delta_a, delta_b, guard)
    blocks = {1: [], -1: []}
    tail_scale2 = mesh_scale2 = 0
    for j, (item, hg) in enumerate(zip(frequency_data, data)):
        guard()
        require(tuple(item["kernel_rectangle"]) == cache.kernel_rectangles[j]
                and item["kernel_modulus_upper_int"] == cache.kernel_modulus_uppers[j],
                "Kernel from THIS DIRECT fresh cache, not a legacy CF producer")
        k, a0 = item["kernel_modulus_upper_int"], item["g_nominal_modulus_upper_int"]
        Z_norm = integer.ceil_div(4 * k * a0 ** 3, SCALE ** 3)
        tail_scale2 += Z_norm * hg["HG_tail"]
        mesh_scale2 += Z_norm * hg["mesh"]
        g0 = item["g_nominal_rectangle"]
        for orientation, g in ((1, g0), (-1, integer.conjugate_rectangle(g0))):
            cube = arithmetic.complex_multiply(arithmetic.complex_multiply(g, g), g)
            base = arithmetic.complex_multiply(item["kernel_rectangle"], cube)
            blocks[orientation].append(tuple(4 * endpoint for endpoint in base))
    tail_margin, mesh_margin = (integer.ceil_div(tail_scale2, SCALE), integer.ceil_div(mesh_scale2, SCALE))
    common_margin = tail_margin + mesh_margin
    indexed = {(row["orientation"], row["H"]): row for row in table["rows"]}
    expected = {(orientation, H) for H in cache.H_grid for orientation in (1, -1)}
    require(len(table["rows"]) == len(expected) and set(indexed) == expected, "ALL H/reflection rows")
    for H in cache.H_grid:
        guard()
        phases = cache.phases_at(H)
        require(len(phases) == len(data), "No q-phase zip truncation")
        for orientation in (1, -1):
            guard()
            z_values = [arithmetic.complex_multiply(phase, base)
                        for phase, base in zip(phases, blocks[orientation])]
            plus = HG.common_coefficients(z_values, data, 1)
            minus = HG.common_coefficients(z_values, data, -1)
            require(len(z_values) == len(data) and len(plus) == len(minus) == 61,
                    "Complete signed q SUM before61-term positive homogeneous dot")
            positive_name, negative_name = (("b", "a") if orientation == 1 else ("a", "b"))
            positive_h = homogeneous_b if positive_name == "b" else homogeneous_a
            negative_h = homogeneous_a if negative_name == "a" else homogeneous_b
            nominal_plus = HG.cell_uppers(plus, positive_h, common_margin)
            nominal_minus = HG.cell_uppers(minus, negative_h, common_margin)
            row = indexed[(orientation, H)]
            row["positive_cell_upper_int"] = [value + margin for value, margin in
                zip(nominal_plus, margins[positive_name])]
            row["negative_cell_upper_int"] = [value + margin for value, margin in
                zip(nominal_minus, margins[negative_name])]
            require(len(row["positive_cell_upper_int"]) == len(row["negative_cell_upper_int"]) == Y_NODES,
                    "Both physical tags have EVERY273 CLOSED cell, signed values unclipped")
    table["nom_mod_cache"] = nom_mod_cache
    table["metadata"].update({"R": RADIUS, "y_step": Y_STEP, "y_nodes": Y_NODES, "HG_degree": DEGREE,
        "A1_includes_nominal_HG_tail_y_mesh_once": True, "A1_includes_box_geometry_margin": True,
        "raw_Q_center_includes_box_geometry_correction": True,
        "nominal_HG_tail_margin_upper_int": tail_margin, "nominal_y_halfcell_mesh_margin_upper_int": mesh_margin,
        "common_nominal_tail_and_mesh_margin_upper_int": common_margin,
        "A1_whole_box_geometry": geometry_metadata,
        "A1_formula": "Re sum4*kappa_H*g_actual^3*r_actual; signed nominal q sum before y dot +whole-box geometry margin",
        "reflection": "orientation+ g0,positiveb/sign+,negativea/sign-; orientation- conjg0,positivea/sign+,negativeb/sign-; SAME raw-H phase",
        "legacy_generic_CF_point_seed_highlevel_producer_or_peak_monitor_called": False,
        "scaled_HG_tail_and_mesh_integer_units": True, "negative_signed_A1_values_clipped": False,
        "original_raw_and_normalized_Q_center_and_actual_modulus_fields_unchanged": True,
        "physical_reserves_eta_Gamma_R2_or_CDF_decision_added": False})
    files = (Path(__file__), Path(linked_center.__file__), Path(linked_center.linked.__file__),
        Path(linked_center.contact_center.__file__), Path(cached.__file__), Path(quad.__file__),
        Path(cached.previous.__file__), Path(HG.__file__), Path(integer.__file__), Path(arithmetic.__file__),
        Path(cached.center.__file__), Path(cached.radial.__file__), Path(cached.center.derivatives.__file__),
        Path(cached.geometry.__file__), Path(cached.previous.geometry_factory.__file__),
        Path(cached.geometry.reference_bridge.__file__), Path(cached.previous.resources.__file__))
    table["metadata"]["generic_A1_source_pins_integrity_only"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    source_drift_check()
    guard()
    return table


def self_tests():
    """Dormant small exact HG/algebra regressions, NOT a response-table producer."""
    checks = 0
    q_grid = tuple(F(3 * (2 * j + 1), 8) for j in range(4))
    data = fresh_HG_frequency_data(q_grid, lambda: None)
    for item in data:
        q = item["q"]
        require(F(item["HG_tail"], SCALE) >= q ** 3 * (q * RADIUS) ** 61 / (6 * factorial(61))
                and F(item["mesh"], SCALE) >= q ** 4 * Y_STEP / 48,
                "Positive remainders FIRST converted to SCALE units")
        checks += 1
        for n, (lo, hi) in enumerate(item["coefficients"]):
            exact = q ** 3 * (q * RADIUS) ** n / factorial(n + 3)
            require(F(lo, SCALE) <= exact <= F(hi, SCALE), "Independent exact HG coefficient enclosure")
            checks += 1
    coefficient_row = [(SCALE, SCALE)] + [(0, 0)] * 60
    fake_data = [{"coefficients": coefficient_row} for _ in range(2)]
    values = [(0, 0, SCALE, SCALE), (0, 0, -SCALE, -SCALE)]
    common = HG.common_coefficients(values, fake_data, 1)
    require(common == [(0, 0)] * 61, "Signed imaginary coefficients cancel across q BEFORE y supremum")
    checks += 1
    homogeneous = [[(SCALE, SCALE)] * 61 for _ in range(Y_NODES)]
    require(HG.cell_uppers(common, homogeneous, 7) == [7] * Y_NODES,
            "Margin added ONCE after joint polynomial")
    checks += 1
    one_plus = HG.common_coefficients(values[:1], fake_data[:1], 1)
    one_minus = HG.common_coefficients(values[:1], fake_data[:1], -1)
    require(one_plus[0] == (SCALE, SCALE) and one_minus[0] == (-SCALE, -SCALE),
            "Correct physical-sign rotation at degree3, signed negative values retained")
    checks += 1
    require(HG.signed_positive_product(-3, -1, 2, 5) == (-15, -2), "Signed negative times positive interval")
    checks += 1
    return {"status": "GENERIC_A1_TINY_SCALED_HG_AND_SIGNED_ALGEBRA_TESTS_ONLY", "exact_checks": checks,
        "fresh_cache_CF_center_A1_Gamma_or_CDF_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
