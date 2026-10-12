"""Fresh integer-outward COMMON SIGNED Hermite response tables; no CDF flag.

API compute_verified_common_response(w,beta,N=256,H_grid=None) accepts exact
Fraction geometry and computes all273 nearest-node y cells on[0,17/4],
both tags and both true reflections. Default58 H=-4+j/8,j0..57. Every
cell upper contains BOTH the Hermite--Genocchi truncation tail and the
y half-cell mesh margin. The Gamma consumer must not add them again.
No numeric receipt/float bound/source hash substitutes for fresh arithmetic.

A1_H(y,tag)=Re sum_q Z_H(q)r_q(tag*y), Z=4*kappa_H*g(q)^3.
The finite HG expansion is r_sigma(q,y)=sum_(n=0)^60
 coeff(q,n)*(i*sigma)^(n+3)*hhat_n(c/R,c/R,y/R),
 coeff0=q^3/6, coeff_n=coeff_(n-1)*(qR)/(n+3),
 hhat0=1, hhat_n=(y/R)hhat_(n-1)+(n+1)(c/R)^n.
Pre-summing the SIGNED real coefficients W_(H,sigma,n) over q is an
exact rearrangement of the finite polynomial, not frequency separation.
The subsequent signed dot with positive outward hhat intervals encloses
the true truncated sum. All sums accumulate at scale^2 and round ONCE.
True HG remainder is bounded by q^3/6*(qR)^61/61!. |partial_y r|<=q^4/24
gives half-cell margin q^4*h/48 for h=1/64. A common norm upper for Z is
4|kappa|*|g|^3 (both reflection norms agree). These margins are added once
AFTER the signed joint polynomial is evaluated. Signed values never clipped.

Positive orientation: g,positivec=b/sign+,negativec=a/sign-.
Reflected orientation: conj(g),positivec=a/sign+,negativec=b/sign-.
This is exactly conjugation with the physical sign tags exchanged.
All g,kappa,phases,Gaussian center values use fresh degree60 integer
rectangles, exact Machin pi/cot-tail/root brackets from approved pure tools.
Owner support17/4 is an external conditional response-domain premise.
This module alone proves no Gamma, CDF, owner reduction or unrestrictedC4.

60s cooperative/256MiB/BLAS1, no NumPy/optimizer. Fulltable compact receipt
<=8MiB because116rows*2tags*273signed scale1e40 integers cannot fit128KiB.
Consumers receive the freshly rebuilt table in memory. CLI saves a NEW
exclusive receipt; --replay-existing rebuilds all arithmetic read-only.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import time

for _setting in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                 "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_setting] = "1"

import n4_Q3_first_critical_integer_abs_Prawitz_gate_strict_v2_2026_10_08 as exact
import n4_Q3_three_budget_exact_affine_radius_verifier_2026_10_08 as point

integer, SCALE = exact.arith, exact.S
RADIUS, STEP, DEGREE = F(17, 4), F(1, 64), 60
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 256 * 1024 * 1024, 8 * 1024 * 1024
H_GRID = tuple(F(-4) + F(j, 8) for j in range(58))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def signed_positive_product(left_lo, left_hi, positive_lo, positive_hi):
    """Unrounded interval product, scale^2; exactly two integer products."""
    require(left_lo <= left_hi and 0 <= positive_lo <= positive_hi, "Ordered signed/positive intervals")
    if left_lo >= 0:
        return left_lo * positive_lo, left_hi * positive_hi
    if left_hi <= 0:
        return left_lo * positive_hi, left_hi * positive_lo
    return left_lo * positive_hi, left_hi * positive_hi


def rotated_real_interval(rectangle, degree, sign):
    """Real part of (i*sign)^degree times this exact complex rectangle."""
    real_lo, real_hi, imag_lo, imag_hi = rectangle
    phase = degree % 4
    if phase == 0:
        lo, hi = real_lo, real_hi
    elif phase == 1:
        lo, hi = -imag_hi, -imag_lo
    elif phase == 2:
        lo, hi = -real_hi, -real_lo
    else:
        lo, hi = imag_lo, imag_hi
    if sign < 0 and degree % 2:
        lo, hi = -hi, -lo
    return lo, hi


def generic_characteristic(q, root):
    w, beta = root["w"], root["beta"]
    exp_tail = (q * RADIUS) ** 61 / math.factorial(61)
    negative = integer.weighted_rectangle(w * (1 + beta) / 2,
        integer.conjugate_rectangle(integer.outward_exponential(q, root["a_bracket"], exp_tail)))
    positive = integer.weighted_rectangle(w * (1 - beta) / 2,
        integer.outward_exponential(q, root["b_bracket"], exp_tail))
    zero = integer.fraction_interval(1 - w)
    return (negative[0] + positive[0] + zero[0], negative[1] + positive[1] + zero[1],
            negative[2] + positive[2], negative[3] + positive[3])


def homogeneous_table(c):
    normalized = (c[0] * 4 // 17, integer.ceil_div(c[1] * 4, 17))
    require(0 <= normalized[0] <= normalized[1] <= SCALE, "Normalized knot inside[0,1]")
    powers = [(SCALE, SCALE)]
    for degree in range(1, DEGREE + 1):
        powers.append(integer.positive_multiply(powers[-1], normalized))
    return [integer.homogeneous_at_node(powers, node) for node in range(273)]


def common_coefficients(z_values, frequency_data, sign):
    """Finite HG coefficients signed-summed before any y evaluation."""
    lows, highs = [0] * 61, [0] * 61
    for z, data in zip(z_values, frequency_data):
        for n, coefficient in enumerate(data["coefficients"]):
            lo, hi = rotated_real_interval(z, n + 3, sign)
            lower, upper = signed_positive_product(lo, hi, coefficient[0], coefficient[1])
            lows[n] += lower
            highs[n] += upper
    return [(lo // SCALE, integer.ceil_div(hi, SCALE)) for lo, hi in zip(lows, highs)]


def cell_uppers(coefficients, homogeneous, margin):
    values = []
    for row in homogeneous:
        upper_scale2 = 0
        for (lo, hi), (positive_lo, positive_hi) in zip(coefficients, row):
            _, upper = signed_positive_product(lo, hi, positive_lo, positive_hi)
            upper_scale2 += upper
        values.append(integer.ceil_div(upper_scale2, SCALE) + margin)
    require(len(values) == 273, "Every closed y cell has a signed upper")
    return values


def table_digest(rows):
    payload = [(row["orientation"], str(row["H"]), row["raw_Q_center_upper_int"],
                row["positive_cell_upper_int"], row["negative_cell_upper_int"]) for row in rows]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode("ascii")).hexdigest()


def json_ready(value):
    if type(value) is F:
        return str(value)
    raise TypeError("Unsupported table receipt value: " + type(value).__name__)


def compute_verified_common_response(w, beta, N=256, H_grid=None, time_limit_seconds=TIME_LIMIT):
    """Fresh arithmetic API; no input numeric table and no output file write."""
    started = time.monotonic()
    require(type(w) is F and type(beta) is F and 0 < w <= 1 and 0 <= beta < 1, "Exact magnitude geometry")
    require(type(N) is int and N in (256, 512), "Bounded dyadic physical frequency grid")
    require(0 < time_limit_seconds <= TIME_LIMIT, "Cooperative time limit<=60s")
    selected_H = H_GRID if H_grid is None else tuple(H_grid)
    require(1 <= len(selected_H) <= 229 and all(type(h) is F and F(-4) <= h <= F(25, 8) for h in selected_H),
            "Exact H nodes in the approved Gaussian/owner domain")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Common signed table elapsed budget")
        peak = integer.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Common signed table memory budget")
    root = point.root_data(w, beta)
    require(max(root["a_bracket"][1], root["b_bracket"][1]) <= RADIUS * SCALE, "HG knots inside owner radius")
    pi, phi0 = exact.pi_and_phi0()
    frequency_data = point.frequency_data(N, guard)
    homogeneous_a, homogeneous_b = homogeneous_table(root["a_bracket"]), homogeneous_table(root["b_bracket"])
    base_blocks = {1: [], -1: []}
    frequency_output = []
    tail_scale2 = mesh_scale2 = 0
    for j, data in enumerate(frequency_data):
        guard()
        q = data["q"]
        kernel = exact.kernel_rectangle(F(2 * j + 1, 2 * N), N, 32, pi)
        g = generic_characteristic(q, root)
        modulus = min(SCALE, integer.rectangle_modulus_upper(g))
        kernel_modulus = integer.rectangle_modulus_upper(kernel)
        z_modulus = integer.ceil_div(4 * kernel_modulus * modulus ** 3, SCALE ** 3)
        tail_scale2 += z_modulus * data["HG_tail"]
        mesh_scale2 += z_modulus * data["mesh"]
        for orientation, characteristic in ((1, g), (-1, integer.conjugate_rectangle(g))):
            square = exact.complex_multiply(characteristic, characteristic)
            cube = exact.complex_multiply(square, characteristic)
            fourth = exact.complex_multiply(square, square)
            kg3 = exact.complex_multiply(kernel, cube)
            z_base = tuple(4 * value for value in kg3)
            kg4 = exact.complex_multiply(kernel, fourth)
            base_blocks[orientation].append((z_base, kg4))
        frequency_output.append({"q": q, "kernel_rectangle": kernel, "kernel_modulus_upper_int": kernel_modulus,
                                 "g_rectangle": g, "g_modulus_upper_int": modulus,
                                 "Z_modulus_upper_int": z_modulus})
    hg_tail_margin = integer.ceil_div(tail_scale2, SCALE)
    y_mesh_margin = integer.ceil_div(mesh_scale2, SCALE)
    common_margin = hg_tail_margin + y_mesh_margin
    rows = []
    for H in selected_H:
        guard()
        phase = exact.exponential_exact_argument(-3 * H / (2 * N))
        ratio = exact.exponential_exact_argument(-3 * H / N)
        z_by_orientation, center_sums = {1: [], -1: []}, {1: 0, -1: 0}
        for j in range(N):
            for orientation in (1, -1):
                z_base, kg4 = base_blocks[orientation][j]
                z_by_orientation[orientation].append(exact.complex_multiply(phase, z_base))
                center_sums[orientation] += exact.complex_multiply(phase, kg4)[1]
            phase = exact.unit_phase_intersection(exact.complex_multiply(phase, ratio))
        normal = exact.normal_cdf_interval(H / 2, phi0)
        for orientation in (1, -1):
            guard()
            plus = common_coefficients(z_by_orientation[orientation], frequency_data, 1)
            minus = common_coefficients(z_by_orientation[orientation], frequency_data, -1)
            positive_h = homogeneous_b if orientation == 1 else homogeneous_a
            negative_h = homogeneous_a if orientation == 1 else homogeneous_b
            rows.append({"orientation": orientation, "H": H,
                         "positive_cell_upper_int": cell_uppers(plus, positive_h, common_margin),
                         "negative_cell_upper_int": cell_uppers(minus, negative_h, common_margin),
                         "raw_Q_center_upper_int": SCALE + 2 * center_sums[orientation] - 2 * normal[0]})
    require(len(rows) == 2 * len(selected_H) and all(len(row["positive_cell_upper_int"]) == 273
            and len(row["negative_cell_upper_int"]) == 273 for row in rows), "Complete H/reflection/tag/cell table")
    guard()
    inputs = (Path(__file__), Path(exact.__file__), Path(integer.__file__), Path(point.__file__), integer.SUPPORT_NOTE)
    return {"status": "INTEGER_OUTWARD_COMMON_SIGNED_RESPONSE_CELL_TABLE", "scale": SCALE, "N": N,
            "root_data": root, "rows": rows, "frequency_data": frequency_output,
            "metadata": {"HG_degree": DEGREE, "R": RADIUS, "y_step": STEP, "y_nodes": 273,
                         "H_grid": selected_H, "orientations": (1, -1), "cell_upper_includes_HG_tail_and_y_mesh": True,
                         "HG_tail_margin_upper_int": hg_tail_margin, "y_halfcell_mesh_margin_upper_int": y_mesh_margin,
                         "common_margin_upper_int": common_margin,
                         "HG_tail_formula": "sum4|kappa|a^3*q^3/6*(qR)^61/61!, |g|<=a<=1",
                         "mesh_formula": "sum4|kappa|a^3*q^4*(1/64)/48, original response Lipschitz not polynomial derivative",
                         "signed_sum_formula": "Pre-sum Re[Z_H(q)*(i*sigma)^(n+3)]*coeff_qn as a signed interval atscale^2; dot with nonnegative hhat intervals. HGtail+mesh once after joint signed polynomial.",
                         "reflection": "orientation+ g,cpositive=b,cnegative=a; orientation- conjg,cpositive=a,cnegative=b. Sign+ positive and sign- negative responses.",
                         "negative_signed_values_clipped": False, "kernel_partial_fraction_M": 32,
                         "table_sha256": table_digest(rows), "fresh_arithmetic": True,
                         "numeric_JSON_or_float_bounds_trusted": False},
            "source_pins_integrity_only": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
            "premises": "Supplied conditional owner response-domain |X|<=17/4. Q3 moment geometry standardized. Full closed y cells include endpoints for safety. No finite-support condition on original P; cost/pole/Gamma/eta/physical CDF work belongs to consumer.",
            "conclusions": {"signed_common_response_cell_uppers_fresh_integer_outward": True,
                            "Gamma_verified": False, "CDF_bound_proved": False,
                            "unrestricted_C4_proved": False, "old_sources_or_receipts_modified": False},
            "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                          "peak_working_set_bytes": integer.peak_bytes(), "time_limit_seconds": time_limit_seconds,
                          "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
                          "NumPy_or_BLAS_imported": False, "cooperative_not_OS_limit": True}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(256, 512), default=256)
    parser.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(args.N) + "_H58.json")
    require(args.replay_existing or not output.exists(), "Never overwrite a signed-response table receipt")
    require(not args.replay_existing or output.exists(), "Read-only signed-response table replay receipt exists")
    result = compute_verified_common_response(F(243205, 266616), F(2, 5), args.N)
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Common signed table output budget")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Replay receipt size")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for field in fresh:
            if field != "resources":
                require(saved[field] == fresh[field], "Read-only signed table replay field: " + field)
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    signed_values = [value for row in result["rows"]
                     for key in ("positive_cell_upper_int", "negative_cell_upper_int") for value in row[key]]
    print(json.dumps({"status": status, "result": str(output), "N": args.N, "H_count": len(H_GRID),
                      "rows_both_orientations": len(result["rows"]), "signed_cell_value_count": len(signed_values),
                      "negative_signed_upper_count": sum(value < 0 for value in signed_values),
                      "table_sha256": result["metadata"]["table_sha256"],
                      "HG_tail_margin_upper_int": result["metadata"]["HG_tail_margin_upper_int"],
                      "y_halfcell_mesh_margin_upper_int": result["metadata"]["y_halfcell_mesh_margin_upper_int"],
                      "output_bytes": len(raw.encode("utf-8")), "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
