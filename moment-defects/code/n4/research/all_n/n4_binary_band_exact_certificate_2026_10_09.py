"""Fresh EXACT n=4 standardized binary-law bound on a CLOSED p band.

For K~Binomial(4,p), Z=(K-4p)/(2sqrt(p(1-p))) has mean0,var1.
Its five nodes x_j(p) decrease in p. Its closed CDF values
 B_j(p)=sum_{i=0}^j choose(4,i)p^i(1-p)^(4-i)
decrease in p (B_-1=0,B_4=1). The normalized n4 Kolmogorov quantity is
 2/rhoB(p) * max_j(0, B_j(p)-Phi(x_j(p)), Phi(x_j(p))-B_{j-1}(p)),
 rhoB=(p^2+(1-p)^2)/sqrt(p(1-p)).
These two directions include BOTH the closed and left-limit CDF at every
atom. Between atoms Phi is continuous/monotone, so no other threshold can
increase the supremum. Reflection p->1-p exchanges those atom sides and
leaves rhoB and the full Kolmogorov distance unchanged; it is NOT a false
closed-CDF complement identity.

Partition [17/100,1/2] into1024 equal CLOSED p intervals. On [lo,hi],
rhoB decreases, so an outward LOWER rhoB(hi) is a valid denominator.
Nodes lie in fresh sqrt-derived [x_j(hi)_LO,x_j(lo)_HI]. In the central
intersection [-2,2], use
 2max(0,B_j(lo)-Phi_LO(clippedlower),Phi_HI(clippedupper)-B_{j-1}(hi))/rhoLO.
Clipping does NOT discard outside nodes. If node>=2 is possible, use the
separate finite-binomial bound
 2max(0,B_j(lo)-Phi_LO(2),1-B_{j-1}(hi))/rhoLO.
If node<=-2 is possible, use
 2max(0,B_j(lo),Phi_HI(-2)-B_{j-1}(hi))/rhoLO.
Both are immediate monotone Gaussian/binomial upper bounds on BOTH atom
sides. Coarse Cantelli0.4 is NOT used to certify the stricter target0.397.

Gaussian Phi endpoints on[-2,2] use fresh Machin pi/phi0 and sixty-order
integer-outward recurrence for t_n=|y|^(2n+1)/(2^n n!(2n+1)):
 t_0=|y|; t_(n+1)=t_n*y^2*(2n+1)/[2(n+1)(2n+3)].
Alternating signed terms are accumulated before multiplication byphi0;
the61st term upper bounds the remainder. Huge-root-denominator Fraction
powers are NEVER used by this new Gaussian loop. All proof data are
Fraction/int at scale10^40; floats/timing/source hashes are diagnostic.

Public compute_verified_binary_band(N=1024,time_limit_seconds=60) returns
a fresh in-memory exact CLOSED-band certificate or UNKNOWN. No stored
numeric certificate or imported three-point axiom is a mathematical input.
Stdlib, static resource monitor,60s/64MiB; no full Prawitz N/H producer.
CLI defaults to tiny self-tests. --produce is explicit and writes only a
NEW exclusive<=1MiB receipt; --replay-existing recomputes read-only.
Producer permission and independent source audits are coordinated outside
this module. No old sources/receipts are edited; no unrestrictedC4 claim.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path
import time

import n4_Q3_first_critical_integer_abs_Prawitz_gate_strict_v2_2026_10_08 as gaussian
import n4_windows_resource_guard_2026_10_09 as resources

integer, SCALE = gaussian.arith, gaussian.S
P_LO, P_HI = F(17, 100), F(1, 2)
REFLECTED_BAND = (F(17, 100), F(83, 100))
TARGET, GAUSSIAN_DEGREE = F(397, 1000), 60
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 60, 64 * 1024 * 1024, 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exact_probability(p):
    require(type(p) is F and 0 < p < 1, "Exact nondegenerate binary probability")
    return p


def binomial4_cdf_values(p):
    p = exact_probability(p)
    q = 1 - p
    values, running = [F(0)], F(0)  # index0 is B_-1
    for j in range(5):
        running += comb(4, j) * p ** j * q ** (4 - j)
        values.append(running)
    require(values[-1] == 1 and all(left <= right for left, right in zip(values, values[1:])),
            "Exact five-atom probability normalization and ordered CDF")
    return tuple(values)


def binary_root_data(p):
    p = exact_probability(p)
    q = 1 - p
    root = integer.sqrt_fraction_interval(p * q)
    require(all(type(value) is int for value in root) and 0 < root[0] <= root[1],
            "Fresh outward sqrt(pq) bracket")
    third_numerator = p * p + q * q
    raw_rho_lower = third_numerator.numerator * SCALE ** 2 // (third_numerator.denominator * root[1])
    # rhoB>=1 is independently exact: (p^2+q^2)^2-pq=(1-pq)(1-4pq)>=0.
    rho_lower = max(SCALE, raw_rho_lower)
    require(F(rho_lower, SCALE) ** 2 <= third_numerator ** 2 / (p * q),
            "Exact outward normalized third-moment LOWER")
    return {"p": p, "sqrt_pq_bracket": root, "rhoB_lower_int": rho_lower}


def node_interval_scaled(j, root_data):
    require(type(j) is int and 0 <= j <= 4, "One of the FIVE binary nodes")
    p, root = root_data["p"], root_data["sqrt_pq_bracket"]
    numerator = j - 4 * p
    # Bounds are in SCALE*x units. For a negative numerator the reciprocal
    # endpoint ordering reverses; // remains FLOOR for negative integers.
    denominator_lo, denominator_hi = ((root[1], root[0]) if numerator >= 0 else (root[0], root[1]))
    lower = numerator.numerator * SCALE ** 2 // (2 * numerator.denominator * denominator_lo)
    upper = integer.ceil_div(numerator.numerator * SCALE ** 2,
                             2 * numerator.denominator * denominator_hi)
    require(lower <= upper, "Correct sign-dependent exact node enclosure")
    return lower, upper


def fast_normal_cdf_interval(x_scaled, phi0):
    """Outward Phi(x_scaled/SCALE), using INTEGER sixty-order recurrence."""
    require(type(x_scaled) is int and abs(x_scaled) <= 2 * SCALE,
            "Exact scaled Gaussian endpoint in[-2,2]")
    require(type(phi0) in (tuple, list) and len(phi0) == 2
            and all(type(value) is int for value in phi0) and 0 < phi0[0] <= phi0[1] <= SCALE,
            "Fresh positive Gaussian normalization bracket")
    y = abs(x_scaled)
    if y == 0:
        return SCALE // 2, SCALE // 2
    term_lower = term_upper = y
    partial_lower = partial_upper = 0
    y_square, scale_square = y * y, SCALE * SCALE
    for n in range(GAUSSIAN_DEGREE + 1):
        if n % 2 == 0:
            partial_lower += term_lower
            partial_upper += term_upper
        else:
            partial_lower -= term_upper
            partial_upper -= term_lower
        factor = y_square * (2 * n + 1)
        denominator = scale_square * 2 * (n + 1) * (2 * n + 3)
        term_lower = term_lower * factor // denominator
        term_upper = integer.ceil_div(term_upper * factor, denominator)
    # term_upper is the61st integrated Taylor term. All terms decrease on
    # |y|<=2; a symmetric remainder enclosure is deliberately retained.
    integral_lower = max(0, partial_lower - term_upper)
    integral_upper = partial_upper + term_upper
    require(0 <= integral_lower <= integral_upper, "Gaussian alternating integral enclosure")
    product_lower = phi0[0] * integral_lower // SCALE
    product_upper = integer.ceil_div(phi0[1] * integral_upper, SCALE)
    if x_scaled >= 0:
        result = SCALE // 2 + product_lower, SCALE // 2 + product_upper
    else:
        result = SCALE // 2 - product_upper, SCALE // 2 - product_lower
    require(0 <= result[0] <= result[1] <= SCALE, "Whole exact Gaussian CDF range")
    return result


def cell_bound(lo, hi, data_lo, data_hi, cdf_lo, cdf_hi, phi_at):
    require(type(lo) is F and type(hi) is F and P_LO <= lo <= hi <= P_HI,
            "Exact closed p-cell in the declared magnitude band")
    denominator = F(data_hi["rhoB_lower_int"], SCALE)
    require(denominator >= 1, "Positive exact rhoB LOWER valid on the WHOLE cell")
    phi_pos2, phi_neg2 = phi_at(2 * SCALE), phi_at(-2 * SCALE)
    best_score, best_node, best_branch = F(0), 0, "none"
    branch_counts = {"central": 0, "positive_tail": 0, "negative_tail": 0}

    def record(delta_upper, j, branch):
        nonlocal best_score, best_node, best_branch
        require(type(delta_upper) is F and delta_upper >= 0, "Exact nonnegative two-sided CDF upper")
        score = 2 * delta_upper / denominator
        branch_counts[branch] += 1
        if score > best_score:
            best_score, best_node, best_branch = score, j, branch

    for j in range(5):
        before_node_branches = sum(branch_counts.values())
        # x_j decreases in p, so these endpoint enclosures cover its ENTIRE
        # actual range on the closed cell. No nominal point is substituted.
        node_lower = node_interval_scaled(j, data_hi)[0]
        node_upper = node_interval_scaled(j, data_lo)[1]
        require(node_lower <= node_upper, "Monotone whole-cell node enclosure")
        closed_lo, open_hi = cdf_lo[j + 1], cdf_hi[j]
        clipped_lower, clipped_upper = max(-2 * SCALE, node_lower), min(2 * SCALE, node_upper)
        if clipped_lower <= clipped_upper:
            normal_lower, normal_upper = phi_at(clipped_lower)[0], phi_at(clipped_upper)[1]
            record(max(F(0), closed_lo - F(normal_lower, SCALE),
                       F(normal_upper, SCALE) - open_hi), j, "central")
        if node_upper >= 2 * SCALE:
            # Separate outside closure; clipping Phi(>2) toPhi(2) alone
            # would underestimate the open-CDF direction and is forbidden.
            record(max(F(0), closed_lo - F(phi_pos2[0], SCALE), 1 - open_hi), j, "positive_tail")
        if node_lower <= -2 * SCALE:
            record(max(F(0), closed_lo, F(phi_neg2[1], SCALE) - open_hi), j, "negative_tail")
        require(sum(branch_counts.values()) > before_node_branches,
                "THIS binary atom has central or outside closure on the whole p-cell")
    require(sum(branch_counts.values()) >= 5, "Each of FIVE atom nodes has central/outside closure")
    return {"lower": lo, "upper": hi, "score_upper": best_score,
            "worst_node": best_node, "worst_branch": best_branch,
            "rhoB_lower_int": data_hi["rhoB_lower_int"], "branches_checked": branch_counts,
            "both_closed_and_left_limit_CDF_sides": True}


def compute_verified_binary_band(N=1024, time_limit_seconds=TIME_LIMIT):
    """Fresh whole-band exact computation, not a numeric receipt importer."""
    started = time.monotonic()
    require(type(N) is int and N == 1024, "Declared1024 equal CLOSED p cells")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic<=60s timer; not numerical proof input")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Exact binary band elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Exact binary band64MiB memory budget")
    require(SCALE == 10 ** 40 and gaussian.GAUSSIAN_DEGREE == GAUSSIAN_DEGREE,
            "Same exact approved Gaussian precision/degree")
    pi, phi0 = gaussian.pi_and_phi0()  # PURE fresh Machin/root primitives, no timed old producer
    phi_cache = {}
    def phi_at(x_scaled):
        if x_scaled not in phi_cache:
            guard()
            phi_cache[x_scaled] = fast_normal_cdf_interval(x_scaled, phi0)
        return phi_cache[x_scaled]
    endpoints = tuple(P_LO + (P_HI - P_LO) * F(j, N) for j in range(N + 1))
    cells = []
    data_lo, cdf_lo = binary_root_data(endpoints[0]), binomial4_cdf_values(endpoints[0])
    for lo, hi in zip(endpoints, endpoints[1:]):
        guard()
        data_hi, cdf_hi = binary_root_data(hi), binomial4_cdf_values(hi)
        cells.append(cell_bound(lo, hi, data_lo, data_hi, cdf_lo, cdf_hi, phi_at))
        data_lo, cdf_lo = data_hi, cdf_hi
    require(cells[0]["lower"] == P_LO and cells[-1]["upper"] == P_HI
            and all(left["upper"] == right["lower"] for left, right in zip(cells, cells[1:])),
            "Complete CLOSED p partition, ALL shared/end faces included")
    upper = max(cell["score_upper"] for cell in cells)
    passed = upper < TARGET
    guard()
    files = (Path(__file__), Path(gaussian.__file__), Path(integer.__file__), Path(resources.__file__))
    return {"status": "EXACT_CLOSED_BINARY_N4_BAND_CERTIFICATE" if passed else "UNKNOWN",
        "date": "2026-10-09", "scale": SCALE, "N": N, "target": TARGET,
        "closed_p_interval": (P_LO, P_HI), "reflected_band": REFLECTED_BAND,
        "closed_cells": cells, "upper_exact": upper,
        "upper_scaled_int": integer.ceil_fraction_scaled(upper),
        "upper_decimal_diagnostic": float(upper), "strict_margin_exact": TARGET - upper,
        "fresh_gaussian": {"pi_bracket": pi, "phi0_bracket": phi0,
            "Phi_2_bracket": phi_at(2 * SCALE), "Phi_minus2_bracket": phi_at(-2 * SCALE),
            "degree": GAUSSIAN_DEGREE, "endpoint_cache_count": len(phi_cache),
            "cache_fresh_in_memory_only": True},
        "metadata": {"five_nodes_per_cell": 5, "both_CDF_atom_sides_checked": True,
            "normalization": "2*Kolmogorov(Z,Phi)/rhoB; Z=(Binomial4(p)-4p)/(2sqrt(pq))",
            "rhoB_monotonicity": "rhoB' = -(1-2p)*(1+2pq)/(2*(pq)^(3/2))<=0 forp<=1/2",
            "node_monotonicity": "x_j' = -(j+(4-2j)*p)/(4*(pq)^(3/2))<0",
            "cdf_monotonicity": "B_j'=-4*choose(3,j)*p^j*q^(3-j)<=0,j0..3; B4=1",
            "central": "Whole node range intersect[-2,2]; separate binomial outside bounds, no lost clipping cases",
            "positive_outside": "max0(B_j(lo)-Phi_LO(2),1-B_(j-1)(hi))",
            "negative_outside": "max0(B_j(lo),Phi_HI(-2)-B_(j-1)(hi))",
            "coarse_Cantelli_0_4_used_for_0_397_acceptance": False,
            "Gaussian_integer_recurrence": "t0=|y|S; tnext=t*y_scaled^2*(2n+1)/(S^2*2(n+1)(2n+3)),positive floor/ceil; signed60sum±term61UP",
            "reflection": "p->1-p negates standardized sum; continuousPhi and both closed/openCDF sup give same normalized quantity",
            "no_saved_numeric_receipt_or_float_bound_premise": True,
            "no_imported_three_point_or_C4_axiom": True},
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "conclusions": {"entire_closed_binary_band_bound_below_target": passed,
            "nonbinary_original_law_coupling_proved_here": False,
            "entire_global_w_beta_root_covered": False, "unrestricted_C4_proved": False,
            "old_sources_or_receipts_modified": False},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "output_limit_bytes": OUTPUT_LIMIT,
            "Prawitz_N_H_or_BOX_producer_called": False, "standard_library_only": True}}


def self_tests():
    """Tiny exact Gaussian/root/atom checks; NO1024interval computation."""
    pi, phi0 = gaussian.pi_and_phi0()
    checks = 0
    for x in (F(-2), F(-3, 2), F(-1), F(-1, 2), F(-1, 8), F(0), F(1, 8), F(1, 2), F(1), F(2)):
        scaled = x * SCALE
        require(scaled.denominator == 1, "Tiny Gaussian endpoint exactly represented")
        fast, old = fast_normal_cdf_interval(scaled.numerator, phi0), gaussian.normal_cdf_interval(x, phi0)
        require(fast[0] <= old[0] <= old[1] <= fast[1],
                "New integer recurrence encloses independently exact Fraction Gaussian Taylor")
        require(fast_normal_cdf_interval(-scaled.numerator, phi0) == (SCALE - fast[1], SCALE - fast[0]),
                "Exact Gaussian reflection and signs")
        checks += 2
    for p in (P_LO, F(1, 4), P_HI):
        data = binary_root_data(p)
        for j in range(5):
            lo, hi = node_interval_scaled(j, data)
            n, root = j - 4 * p, data["sqrt_pq_bracket"]
            candidates = (n * SCALE / (2 * root[0]), n * SCALE / (2 * root[1]))
            require(F(lo, SCALE) <= min(candidates) <= max(candidates) <= F(hi, SCALE),
                    "Independent Fraction sign/root endpoint node arithmetic")
            if p == P_HI:
                require(lo == hi == (j - 2) * SCALE, "Exact balanced binary nodes including±2")
            checks += 1
        values = binomial4_cdf_values(p)
        require(values[0] == 0 and values[-1] == 1, "Both edge CDF sides retained")
        checks += 1
    low, high = binomial4_cdf_values(P_LO), binomial4_cdf_values(P_HI)
    require(all(low[j] >= high[j] for j in range(6)), "Tiny endpoint monotonic CDF identity")
    checks += 1
    # A SINGLE degenerate p-cell is a small helper test, not the band run.
    balanced = binary_root_data(P_HI)
    values = binomial4_cdf_values(P_HI)
    phi_at = lambda x: fast_normal_cdf_interval(x, phi0)
    cell = cell_bound(P_HI, P_HI, balanced, balanced, values, values, phi_at)
    require(cell["branches_checked"] == {"central": 5, "positive_tail": 1, "negative_tail": 1}
            and cell["score_upper"] < TARGET, "Both±2 boundaries get central AND separate outside closure")
    checks += 1
    for call in (lambda: fast_normal_cdf_interval(True, phi0),
                 lambda: fast_normal_cdf_interval(2 * SCALE + 1, phi0),
                 lambda: node_interval_scaled(True, balanced),
                 lambda: exact_probability(0.5)):
        try:
            call()
        except RuntimeError:
            checks += 1
        else:
            raise RuntimeError("Invalid exact binary/Gaussian interface accepted")
    return {"status": "EXACT_BINARY_BAND_TINY_TESTS_ONLY", "exact_checks": checks,
        "actual1024closed_interval_producer_called": False,
        "comparison_to_old_Gaussian_used_as_proof_axiom": False,
        "whole_binary_band_or_nonbinary_C4_proved_by_tests": False,
        "old_sources_or_receipts_modified": False}


def json_ready(value):
    if type(value) is F:
        return str(value)
    raise TypeError("Unsupported exact certificate value: " + type(value).__name__)


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--produce", action="store_true")
    mode.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if args.self_test or not (args.produce or args.replay_existing):
        print(json.dumps(self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem + "_N1024.json")
    require(args.replay_existing or not output.exists(), "Never overwrite an exact binary receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay receipt must exist")
    result = compute_verified_binary_band()
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Exact binary receipt<=1MiB")
    peak = resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and (peak is None or peak <= MEMORY_LIMIT),
            "Entire CLI including JSON within60s/64MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only replay input")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for key in fresh:
            if key != "resources":
                require(saved[key] == fresh[key], "Fresh exact read-only binary replay: " + key)
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "upper_exact": result["upper_exact"],
        "upper_decimal_diagnostic": result["upper_decimal_diagnostic"], "target": TARGET,
        "closed_p_interval": result["closed_p_interval"], "reflected_band": REFLECTED_BAND,
        "closed_cells": len(result["closed_cells"]), "output_bytes": len(raw.encode("utf-8")),
        "resources": result["resources"]}, sort_keys=True, default=json_ready))


if __name__ == "__main__":
    main()
