"""V2: cellwise cached CLOSED-BOX A1/center backend ONLY; no CDF assertion.

compute_verified_box_common_response(rectangle,N=256,H_grid=None) takes
four Fraction endpoints (w_lo,w_hi,beta_abs_lo,beta_abs_hi). It rebuilds
the exact midpoint common-response table ONCE, independently recomputes
audited full-box monotone geometry, and adds uniform per-tag perturbations
to the already CLOSED nominal y-cell uppers. Nominal and actual-box roots
are separate fields and are never relabelled as one another.

Both Q3 references are standardized. Exact geometric Eg is the minimum
of direct, mass-cancelled O(q), and matched-mean/variance O(q^3) bounds.
For a0>=|g_nominal|, e>=|g_actual-g_nominal|, p=min(1,a0+e),
 D3=e*(p^2+p*a0+a0^2),
 |g_actual^3-g_nominal^3|<=D3.
Hermite--Genocchi gives |r_nominal|<=q^3/6 and
|partial_c r|<=q^4/12 for PHYSICAL contact c (two c simplex weights).
Splitting g_actual^3*r_actual-g_nominal^3*r_nominal yields
 M_c[node]=sum4|kappa|*(D3*min(r_nom_closed_cell_mod[node],q^3/6)
+ p^3*q^4*Delta_c/12). Fresh raw nominal modulus caches include HGtail
+and y half-cell mesh and remain UNMODIFIED for radius consumers.
This bound is uniform in y, so M_c is added to nominal CLOSED cells with
their original HG tail/y mesh ALREADY included once. No actual additional
HG remainder or mesh margin is required. Reflection conjugates both g
values and swaps Delta_a/Delta_b, never changes H or the fixed kernel.

Actual reference centers use nominal_raw_Q+RAW2sum|kappa|*D4(e,a0),
with the audited fourth-power telescope/endpoint cap. This is ONLY center
geometry correction: no physical quadrature/H reserve is added here.
Gamma/radii/R2/CDF and physical owner premises belong to later consumers.

Pure integer/Fraction bounds, fresh in-memory API, no JSON numeric trust.
60s/256MiB/BLAS1. Heavy producer use is coordinated externally. Optional
CLI makes a new exclusive receipt<=8MiB for width1/1000 around the hard
geometry. Cell arrays are losslessly base64 fixed-width signed integers
IN THAT AUDIT RECEIPT ONLY to meet8MiB; API arrays remain ordinary ints.
--self-test runs pure tiny algebra/schema/encoding checks, not a producer.
"""

from __future__ import annotations

import argparse
import base64
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_exact_common_signed_response_table_2026_10_08 as nominal_backend
import n4_Q3_box_whole_eta_exact_CDF_gate_v2_2026_10_08 as reference_bridge
import n4_Q3_three_budget_exact_box_affine_radius_verifier_2026_10_08 as geometry_factory

integer, exact, SCALE = nominal_backend.integer, nominal_backend.exact, nominal_backend.SCALE
RADIUS, STEP = F(17, 4), F(1, 64)
H_GRID = tuple(F(-4) + F(j, 32) for j in range(229))
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 256 * 1024 * 1024, 8 * 1024 * 1024
W, BETA = F(243205, 266616), F(2, 5)
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_geometry(rectangle):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is F for value in rectangle), "Four exact Fraction box endpoints")
    rectangle = tuple(rectangle)
    root = geometry_factory.box_root_data(*rectangle)
    bridge = reference_bridge.geometry(rectangle)
    for key, bridge_key in (("a_bracket", "a"), ("b_bracket", "b"), ("rhoQ_bracket", "rho")):
        require(tuple(root[key]) == tuple(bridge[bridge_key]), "Independent monotone geometry agrees: " + key)
    nominal = dict(root["nominal_root_data"])
    require(nominal["w"] == sum(rectangle[:2], F(0)) / 2
            and nominal["beta"] == sum(rectangle[2:], F(0)) / 2, "Exact midpoint labels")
    require(tuple(nominal["a_bracket"]) == tuple(bridge["a0"])
            and tuple(nominal["b_bracket"]) == tuple(bridge["b0"]), "Independent midpoint roots agree")
    # Only true BOX coordinates belong to box_geometry. Midpoint fields
    # remain separate; no point roots/probabilities are labelled as box bounds.
    box = {key: value for key, value in root.items()
           if key not in ("nominal_root_data", "nominal_probabilities")}
    box["rectangle"] = rectangle
    return box, nominal, bridge


def cubic_absolute_upper(epsilon, nominal_modulus):
    require(type(epsilon) is int and type(nominal_modulus) is int
            and epsilon >= 0 and 0 <= nominal_modulus <= SCALE, "Outward nonnegative cubic inputs")
    p = min(SCALE, nominal_modulus + epsilon)
    return integer.ceil_div(epsilon * (p * p + p * nominal_modulus + nominal_modulus ** 2), SCALE ** 2)


def corrected_rows(nominal_rows, margin_a, margin_b, center_margin):
    require(len(margin_a) == len(margin_b) == 273
            and all(type(value) is int and value >= 0 for value in (*margin_a, *margin_b))
            and type(center_margin) is int and center_margin >= 0, "Cellwise outward geometry margins")
    result = []
    for row in nominal_rows:
        orientation = row["orientation"]
        require(orientation in (1, -1) and type(row["H"]) is F, "Exact orientation and H")
        positive_margin, negative_margin = ((margin_b, margin_a) if orientation == 1
                                             else (margin_a, margin_b))
        positive, negative = row["positive_cell_upper_int"], row["negative_cell_upper_int"]
        require(len(positive) == len(negative) == 273 and all(type(value) is int for value in (*positive, *negative)),
                "Complete signed nominal CLOSED-cell table")
        require(type(row["raw_Q_center_upper_int"]) is int, "Nominal raw Q integer center")
        result.append({"orientation": orientation, "H": row["H"],
                       "positive_cell_upper_int": [value + margin for value, margin in zip(positive, positive_margin)],
                       "negative_cell_upper_int": [value + margin for value, margin in zip(negative, negative_margin)],
                       "positive_contact_name": "b" if orientation == 1 else "a",
                       "negative_contact_name": "a" if orientation == 1 else "b",
                       "positive_geometry_margin_max_upper_int": max(positive_margin),
                       "negative_geometry_margin_max_upper_int": max(negative_margin),
                       "nominal_raw_Q_center_upper_int": row["raw_Q_center_upper_int"],
                       "raw_Q_center_upper_int": row["raw_Q_center_upper_int"] + center_margin})
    return result


def fresh_nominal_mod_cache(nominal, N, guard):
    """Raw |r_nom| CLOSED-cell bounds, not /q^3 and not |g_nom|."""
    data = nominal_backend.point.frequency_data(N, guard)
    matrices = {}
    for name in ("a", "b"):
        homogeneous = nominal_backend.homogeneous_table(nominal[name + "_bracket"])
        cells = []
        for node in range(273):
            guard()
            row = []
            for item in data:
                rectangle = integer.response_rectangle(item["coefficients"], homogeneous[node])
                row.append(integer.rectangle_modulus_upper(rectangle) + item["HG_tail"] + item["mesh"])
            cells.append(row)
        matrices[name] = cells
    q_grid = tuple(item["q"] for item in data)
    payload = [N, list(map(str, q_grid)), str(nominal["w"]), str(nominal["beta"]),
               tuple(nominal["a_bracket"]), tuple(nominal["b_bracket"]), matrices["a"], matrices["b"]]
    digest = hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode("ascii")).hexdigest()
    return {"scale": SCALE, "N": N, "R": RADIUS, "y_step": STEP, "HG_degree": 60,
            "q_grid": q_grid, "nominal_root_data": nominal,
            "a_cell_modulus_upper_int": matrices["a"], "b_cell_modulus_upper_int": matrices["b"],
            "includes_HG_tail_and_y_mesh": True, "cell_arrays_raw_r_not_normalized": True,
            "raw_cache_unmodified_by_global_HG_cap": True,
            "cache_sha256_integrity_only": digest,
            "mathematical_model": "Fresh nominal HG rectangle modulus+HGtail_q+q^4*h/48, uniform on the WHOLE y cell, scale units of r, conjugate sign has identical norm. Fresh API cache, never JSON trust."}


def cellwise_geometry_margins(cache, frequency_data, motion_a, motion_b, old_global_a, old_global_b):
    require(cache["scale"] == SCALE and len(cache["q_grid"]) == len(frequency_data), "Fresh cache physical scale/grid")
    coefficients, caps = [], []
    for q, item in zip(cache["q_grid"], frequency_data):
        require(q == item["q"], "Cache q matches center/kernel physical q")
        caps.append(integer.ceil_fraction_scaled(q ** 3 / 6))
        require(caps[-1] == integer.floor_fraction_scaled(q ** 3 / 6), "q^3/6 exactly represented on current dyadic grid")
        coefficients.append(4 * item["kernel_modulus_upper_int"] * item["D3_upper_int"])
    margins = {}
    for name, motion, old_global in (("a", motion_a, old_global_a), ("b", motion_b, old_global_b)):
        cells = cache[name + "_cell_modulus_upper_int"]
        require(len(cells) == 273 and all(len(row) == len(coefficients) for row in cells), "All raw cache cells/frequencies")
        values = []
        for row in cells:
            # kappa*D3*r has scale^3. Both scalar r bounds are valid on
            # the SAME WHOLE cell, hence their min is valid. Cache unchanged.
            accumulated = sum(coefficient * min(raw, cap)
                              for coefficient, raw, cap in zip(coefficients, row, caps))
            candidate = integer.ceil_div(accumulated, SCALE ** 2) + motion
            # Both complete margins are independently valid absolute
            # uppers; this is NOT a polynomial/coefficientwise minimum.
            values.append(min(candidate, old_global))
        require(all(0 <= value <= old_global for value in values), "Cellwise margins never worse than old global")
        margins[name] = values
    return margins["a"], margins["b"]


def compute_verified_box_common_response(rectangle, N=256, H_grid=None, time_limit_seconds=TIME_LIMIT):
    """Fresh in-memory BOX response producer; no input/output receipt trust."""
    started = time.monotonic()
    require(type(N) is int and N == 256, "Declared initial BOX physical grid N256")
    require(0 < time_limit_seconds <= TIME_LIMIT, "Cooperative budget<=60s")
    selected_H = H_GRID if H_grid is None else tuple(H_grid)
    require(1 <= len(selected_H) <= 229 and len(set(selected_H)) == len(selected_H)
            and all(type(H) is F and F(-4) <= H <= F(25, 8) for H in selected_H), "Exact unique H nodes")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "BOX common response time budget")
        peak = integer.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "BOX common response working-set budget")
    box, nominal, bridge = canonical_geometry(rectangle)
    guard()
    nominal_table = nominal_backend.compute_verified_common_response(nominal["w"], nominal["beta"],
        N=N, H_grid=selected_H, time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
    require(nominal_table["scale"] == SCALE and nominal_table["N"] == N, "Fresh nominal scale/N")
    require(nominal_table["root_data"]["w"] == nominal["w"]
            and nominal_table["root_data"]["beta"] == nominal["beta"], "Fresh midpoint exact labels")
    for key in ("a_bracket", "b_bracket", "u_bracket", "rhoQ_bracket"):
        require(tuple(nominal_table["root_data"][key]) == tuple(nominal[key]), "True NOMINAL roots agree: " + key)
    require(tuple(nominal_table["metadata"]["H_grid"]) == selected_H
            and nominal_table["metadata"]["cell_upper_includes_HG_tail_and_y_mesh"],
            "Nominal H grid and one-time closed-cell margins")
    margin_a_exact = margin_b_exact = center_exact = F(0)
    motion_a_exact = motion_b_exact = F(0)
    delta_a, delta_b = F(bridge["da"], SCALE), F(bridge["db"], SCALE)
    frequency_data = []
    require(len(nominal_table["frequency_data"]) == N, "Complete nominal frequency grid")
    for j, item in enumerate(nominal_table["frequency_data"]):
        guard()
        q = item["q"]
        require(q == F(3 * (2 * j + 1), 2 * N), "Same exact physical q")
        a0 = item["g_modulus_upper_int"]
        kappa = item["kernel_modulus_upper_int"]
        require(type(a0) is int and 0 <= a0 <= SCALE and type(kappa) is int and kappa >= 0,
                "Fresh nominal modulus/kernel uppers")
        Eg = integer.ceil_fraction_scaled(reference_bridge.reference_error(q, bridge))
        p = min(SCALE, a0 + Eg)
        D3 = cubic_absolute_upper(Eg, a0)
        D4 = exact.quartic_absolute_upper(Eg, a0)
        weight, cubic, quartic, p_actual = F(kappa, SCALE), F(D3, SCALE), F(D4, SCALE), F(p, SCALE)
        common = cubic * q ** 3 / 6
        motion_a = 4 * weight * p_actual ** 3 * q ** 4 * delta_a / 12
        motion_b = 4 * weight * p_actual ** 3 * q ** 4 * delta_b / 12
        motion_a_exact += motion_a; motion_b_exact += motion_b
        margin_a_exact += 4 * weight * common + motion_a
        margin_b_exact += 4 * weight * common + motion_b
        center_exact += 2 * weight * quartic
        frequency_data.append({"q": q, "kernel_rectangle": item["kernel_rectangle"],
                               "kernel_modulus_upper_int": kappa,
                               "g_nominal_rectangle": item["g_rectangle"],
                               "g_nominal_modulus_upper_int": a0,
                               "g_actual_modulus_upper_int": p,
                               "Eg_upper_int": Eg, "D3_upper_int": D3, "D4_upper_int": D4})
    margin_a, margin_b, center_margin = map(integer.ceil_fraction_scaled,
                                           (margin_a_exact, margin_b_exact, center_exact))
    cache = fresh_nominal_mod_cache(nominal, N, guard)
    require(tuple(cache["q_grid"]) == tuple(item["q"] for item in frequency_data), "Fresh cache and nominal table frequencies agree")
    M_a, M_b = cellwise_geometry_margins(cache, frequency_data,
        integer.ceil_fraction_scaled(motion_a_exact), integer.ceil_fraction_scaled(motion_b_exact), margin_a, margin_b)
    rows = corrected_rows(nominal_table["rows"], M_a, M_b, center_margin)
    nominal_metadata = dict(nominal_table["metadata"])
    nominal_pins = dict(nominal_table["source_pins_integrity_only"])
    # Do not retain duplicate nominal cell arrays in the BOX result; later
    # consumers need only the corrected arrays and explicit midpoint labels.
    del nominal_table
    expected = {(orientation, H) for H in selected_H for orientation in (1, -1)}
    require(len(rows) == len(expected) and {(row["orientation"], row["H"]) for row in rows} == expected,
            "Complete chosen H/reflection BOX table")
    guard()
    files = (Path(__file__), Path(nominal_backend.__file__), Path(reference_bridge.__file__),
             Path(geometry_factory.__file__), Path(exact.__file__), Path(integer.__file__), integer.SUPPORT_NOTE)
    pins = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    pins.update(nominal_pins)
    return {"status": "INTEGER_OUTWARD_CELLWISE_CACHED_BOX_COMMON_SIGNED_RESPONSE_TABLE", "scale": SCALE, "N": N,
            "box_geometry": box, "nominal_root_data": nominal, "rows": rows, "frequency_data": frequency_data,
            "nom_mod_cache": cache,
            "metadata": {"H_grid": selected_H, "orientations": (1, -1), "R": RADIUS, "y_step": STEP,
                         "y_nodes": 273, "A1_includes_nominal_HG_tail_y_mesh_once": True,
                         "A1_includes_box_geometry_margin": True,
                         "raw_Q_center_includes_box_geometry_correction": True,
                         "A1_margin_a_upper_int": max(M_a), "A1_margin_b_upper_int": max(M_b),
                         "A1_margin_a_cell_upper_int": M_a, "A1_margin_b_cell_upper_int": M_b,
                         "old_global_A1_margin_a_upper_int": margin_a, "old_global_A1_margin_b_upper_int": margin_b,
                         "contact_motion_a_upper_int": integer.ceil_fraction_scaled(motion_a_exact),
                         "contact_motion_b_upper_int": integer.ceil_fraction_scaled(motion_b_exact),
                         "nom_mod_cache_freshly_verified": True,
                         "A1_cellwise_geometry_margin_never_worse_than_old_global": True,
                         "raw_Q_geometry_correction_upper_int": center_margin,
                         "physical_Delta_a_upper": delta_a, "physical_Delta_b_upper": delta_b,
                         "nominal_closed_cell_metadata": nominal_metadata,
                         "Eg_model": "min(direct, mass-cancelled O(q), matched mass/mean/variance O(q^3)), exact audited geometry bridge",
                         "A1_margin_formula": "Per-node sum4|kappa|[D3(Eg,a0)*min(freshRAW_r_nom_CLOSEDcell_mod,q^3/6)+p^3*q^4*PHYSICAL_Delta_c/12], p=min1(a0+Eg); intersect complete integer margin with valid oldglobal upper. RAWcache unchanged for later radius consumer.",
                         "cache_margin_counting": "Nominal A1 HGtail/ymesh remains once. RAWnominalr cache is a separate norm premise inside the D3 geometry term; its tail/mesh is not added again to baseline A1 or cached radius.",
                         "center_margin_formula": "RAW2sum|kappa|D4(Eg,a0), no quadrature or H reserve here",
                         "reflection": "Actual/nominal g conjugated at sameH; positiveDelta=b,negativeDelta=a for+; swap for-",
                         "nominal_roots_relabelled_as_box": False, "negative_signed_values_clipped": False,
                         "table_sha256": nominal_backend.table_digest(rows),
                         "fresh_arithmetic": True, "numeric_JSON_or_float_bounds_trusted": False},
            "source_pins_integrity_only": pins,
            "premises": "Actual standardized P has its true Q3 parameters in the closed rectangle and supplied support |X|<=17/4. This backend bounds A1 and reference center only. Later physical CDF reserves require standing actualrho<46/25; an enlarged rectangle/eta face does not establish feasibility or owner status.",
            "conclusions": {"BOX_A1_cell_uppers_fresh_integer_outward": True,
                            "BOX_reference_center_geometry_correction_fresh": True,
                            "Gamma_verified": False, "modulus_radius_verified": False,
                            "CDF_bound_proved": False, "unrestricted_C4_proved": False,
                            "old_sources_or_receipts_modified": False},
            "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                          "peak_working_set_bytes": integer.peak_bytes(), "time_limit_seconds": time_limit_seconds,
                          "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
                          "NumPy_or_BLAS_imported": False, "cooperative_not_OS_limit": True}}


def packed_signed_integers(values):
    require(values and all(type(value) is int for value in values), "Nonempty exact signed integer array")
    bits = max((value.bit_length() + 1 if value >= 0 else (~value).bit_length() + 1) for value in values)
    width = max(1, (bits + 7) // 8)
    raw = b"".join(value.to_bytes(width, "big", signed=True) for value in values)
    return {"encoding": "base64_signed_big_endian_fixed_width", "byte_width": width,
            "count": len(values), "data": base64.b64encode(raw).decode("ascii")}


def unpacked_signed_integers(record):
    require(record["encoding"] == "base64_signed_big_endian_fixed_width", "Declared exact integer encoding")
    width, count = record["byte_width"], record["count"]
    require(type(width) is int and type(count) is int and width > 0 and count > 0, "Positive exact encoding sizes")
    raw = base64.b64decode(record["data"], validate=True)
    require(len(raw) == width * count, "Exact encoded array byte count")
    return [int.from_bytes(raw[j * width:(j + 1) * width], "big", signed=True) for j in range(count)]


def receipt_view(result):
    rows = [{**row, "positive_cell_upper_int": packed_signed_integers(row["positive_cell_upper_int"]),
             "negative_cell_upper_int": packed_signed_integers(row["negative_cell_upper_int"])} for row in result["rows"]]
    cache = result["nom_mod_cache"]
    cache_audit = {key: value for key, value in cache.items()
                   if key not in ("a_cell_modulus_upper_int", "b_cell_modulus_upper_int")}
    cache_audit["raw_cell_arrays_omitted_from_audit_receipt_not_reusable_as_proof"] = True
    cache_audit["raw_array_shape_per_contact"] = (273, result["N"])
    return {**result, "rows": rows, "nom_mod_cache": cache_audit,
            "audit_receipt_cell_encoding": "Lossless fixed-width signed big-endian base64 ONLY for receipt-size budget; fresh API always returns ordinary integer arrays. Never imported as a mathematical bound."}


def self_tests():
    rectangle = (W - F(1, 1000), W + F(1, 1000), BETA - F(1, 1000), BETA + F(1, 1000))
    box, nominal, bridge = canonical_geometry(rectangle)
    require(box["rectangle"] == rectangle and nominal["w"] == W and nominal["beta"] == BETA,
            "Distinct exact midpoint and BOX schema")
    require(box["a_bracket"][0] <= nominal["a_bracket"][0] <= nominal["a_bracket"][1] <= box["a_bracket"][1],
            "True midpoint roots enclosed in box")
    checks = 2
    from n4_signed_second_order_eta_bernstein_2026_10_08 import cpow, norm_squared
    for ar in (F(0), F(1, 3), F(3, 5), F(1)):
        for psi in ((F(0), F(0)), (F(1), F(0)), (F(-1), F(0)), (F(3, 5), F(4, 5)), (F(1, 3), F(1, 3))):
            a_int = integer.ceil_fraction_scaled(ar)
            eg_square = (psi[0] - ar) ** 2 + psi[1] ** 2
            eg_int = 0 if eg_square == 0 else integer.sqrt_fraction_interval(eg_square)[1]
            upper = F(cubic_absolute_upper(eg_int, a_int), SCALE)
            psi3, g3 = cpow(psi, 3), cpow((ar, F(0)), 3)
            difference = (psi3[0] - g3[0], psi3[1] - g3[1])
            require(norm_squared(difference) <= upper ** 2, "Exact complex cubic perturbation bound")
            checks += 1
    mock = [{"orientation": sign, "H": F(0), "positive_cell_upper_int": [-j for j in range(273)],
             "negative_cell_upper_int": [j for j in range(273)], "raw_Q_center_upper_int": -10} for sign in (1, -1)]
    corrected = corrected_rows(mock, [3] * 273, [7] * 273, 11)
    require(corrected[0]["positive_cell_upper_int"][0] == 7 and corrected[0]["negative_cell_upper_int"][0] == 3
            and corrected[1]["positive_cell_upper_int"][0] == 3 and corrected[1]["negative_cell_upper_int"][0] == 7
            and corrected[0]["raw_Q_center_upper_int"] == 1
            and mock[0]["positive_cell_upper_int"][0] == 0, "Reflection swaps margins, center added once, input untouched")
    checks += 1
    # One-frequency/all273cell cache is a tiny helper check, not an N256
    # producer. It checks RAW units and never-worse scalar intersections.
    tiny_cache = fresh_nominal_mod_cache(nominal, 1, lambda: None)
    q = tiny_cache["q_grid"][0]
    toy = [{"q": q, "kernel_modulus_upper_int": SCALE // 10, "D3_upper_int": SCALE // 20}]
    old_margin = integer.ceil_fraction_scaled(4 * F(1, 10) * F(1, 20) * q ** 3 / 6) + 5
    Ma, Mb = cellwise_geometry_margins(tiny_cache, toy, 5, 5, old_margin, old_margin)
    require(len(Ma) == len(Mb) == 273 and min(*Ma, *Mb) >= 5
            and max(*Ma, *Mb) <= old_margin, "Tiny cache RAW units and whole-margin no-worse bound")
    require(tiny_cache["includes_HG_tail_and_y_mesh"] and tiny_cache["cell_arrays_raw_r_not_normalized"],
            "Tiny cache proof schema")
    checks += 2
    for values in ((0,), (-1, 0, 1), (-128, 127), (-129, 128), (-10 ** 45, -SCALE, 0, SCALE, 10 ** 45)):
        require(unpacked_signed_integers(packed_signed_integers(values)) == list(values), "Lossless signed receipt encoding")
        checks += 1
    return {"status": "CELLWISE_BOX_A1_CACHE_GEOMETRY_TINY_TESTS_ONLY", "exact_checks": checks,
            "heavy_nominal_or_BOX_backend_called": False, "tiny_one_frequency_mod_cache_only": True, "CDF_bound_proved": False}


def main():
    cli_started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem + "_width1_1000_N256_H229.json")
    require(args.replay_existing or not output.exists(), "Never overwrite a BOX response receipt")
    require(not args.replay_existing or output.exists(), "Read-only BOX response replay receipt exists")
    rectangle = (W - F(1, 1000), W + F(1, 1000), BETA - F(1, 1000), BETA + F(1, 1000))
    result = compute_verified_box_common_response(rectangle)
    audit_view = receipt_view(result)
    raw = json.dumps(audit_view, sort_keys=True, separators=(",", ":"), allow_nan=False,
                     default=nominal_backend.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "BOX audit receipt<=8MiB")
    cli_peak = integer.peak_bytes()
    require(time.monotonic() - cli_started < TIME_LIMIT
            and (cli_peak is None or cli_peak <= MEMORY_LIMIT),
            "Whole optional CLI including lossless receipt encoding stays within60s/256MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Replay receipt size")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for field in fresh:
            if field != "resources":
                require(saved[field] == fresh[field], "Read-only BOX response replay field: " + field)
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "output_bytes": len(raw.encode("utf-8")),
                      "rows": len(result["rows"]), "table_sha256": result["metadata"]["table_sha256"],
                      "M_a_upper_int": result["metadata"]["A1_margin_a_upper_int"],
                      "M_b_upper_int": result["metadata"]["A1_margin_b_upper_int"],
                      "raw_center_geometry_correction_upper_int": result["metadata"]["raw_Q_geometry_correction_upper_int"],
                      "CLI_peak_working_set_bytes": cli_peak,
                      "CLI_elapsed_seconds_diagnostic_only": time.monotonic() - cli_started,
                      "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
