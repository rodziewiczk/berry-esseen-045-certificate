"""Fresh EXACT three-budget affine radius tables; no CDF assertion.

Float calculations choose rational price indices ONLY. Every selected model
is then rebuilt from degree60 integer-outward Hermite--Genocchi response
rectangles, HG tail, half-cell mesh, exact k0 lower costs and exact concave
reciprocal-pole penalty maxima. No numerical floating bound is imported.

Public API compute_verified_models(w,beta,N,anchor_count=17) returns actual
Fraction objects for q and A and signed integers S_upper_int at scale10^40.
Every model gives |delta(q)| <= q^3*(A+eta*S_upper_int/SCALE) throughout the
feasible eta fibre. No winner persistence or eta monotonicity is assumed.
The consumer must use nonnegative candidates (or rigorously exclude empty
subcells); at eta0 P=Q3 directly. Cube/mass/1+|g| caps are left to the engine.

Conditional owner support R17/4 is supplied separately. Original P need not
be finitely supported. Source pins are integrity data, not mathematical proof.
No old globals/files modified; pure arithmetic helper functions only.
Cooperative45s/256MiB, BLAS1, streaming, new exclusive receipt <=2MiB.
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

for _thread_setting in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                        "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_thread_setting] = "1"

import n4_Q3_first_critical_integer_response_radius_verifier_2026_10_08 as integer

SCALE, RADIUS, STEP, DEGREE = integer.SCALE, F(17, 4), F(1, 64), 60
ROOT_CAP = F(979013, 532500)
TIME_LIMIT, MEMORY_LIMIT, OUTPUT_LIMIT = 45.0, 256 * 1024 * 1024, 2 * 1024 * 1024
TAUS = tuple(map(F, ("0", "1/1000", "1/400", "1/200", "1/100", "1/50",
                    "1/25", "2/25", "4/25", "8/25", "16/25")))
ZETAS = tuple(map(F, ("0", "1/2000", "1/1000", "1/400", "1/200", "1/100", "1/50")))
XIS = tuple(map(F, ("-1/50", "-1/100", "-1/200", "0", "1/200", "1/100", "1/50")))
PAIRS = tuple((zeta, xi) for zeta in ZETAS for xi in XIS if zeta > 0 or xi == 0)
ceil_div = integer.ceil_div
ceil_scaled = integer.ceil_fraction_scaled


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def root_data(w, beta):
    require(isinstance(w, F) and isinstance(beta, F), "Exact Fraction reference parameters")
    require(0 < w <= 1 and -1 < beta < 1, "Nondegenerate standardized Q3 reference")
    a2 = (1 - beta) / (w * (1 + beta))
    b2 = (1 + beta) / (w * (1 - beta))
    u2 = w * (1 - beta * beta) / 4
    rho2 = (1 + beta * beta) ** 2 / (w * (1 - beta * beta))
    a, b, u, rho = map(integer.sqrt_fraction_interval, (a2, b2, u2, rho2))
    require(max(a[1], b[1]) <= RADIUS * SCALE, "Q3 knots inside supplied owner support")
    eta_max = ROOT_CAP - F(rho[0], SCALE)
    require(eta_max >= 0 and ROOT_CAP < F(46, 25), "Positive root eta cap and physical moment scope")
    return {"w": w, "beta": beta, "p0": 1 - w, "a_square": a2, "b_square": b2,
            "u_square": u2, "rhoQ_square": rho2, "a_bracket": a, "b_bracket": b,
            "u_bracket": u, "rhoQ_bracket": rho, "eta_max_upper": eta_max}


def reciprocal_domains(dlo, dhi):
    """None denotes the corresponding infinite endpoint; d=0 is excluded."""
    require(dlo <= dhi and not (dlo == dhi == 0), "Nonempty reciprocal difference enclosure")
    domains = []
    if dlo < 0:
        domains.append((1 / dhi if dhi < 0 else None, 1 / dlo))
    if dhi > 0:
        domains.append((1 / dhi, 1 / dlo if dlo > 0 else None))
    require(1 <= len(domains) <= 2, "One interval/ray or two reciprocal rays")
    return domains


def penalty_maximum(zeta, xi, domains):
    require(zeta >= 0 and (zeta > 0 or xi == 0), "Allowed rational contact prices")
    if zeta == 0:
        return F(0)
    vertex = -xi / (2 * zeta)
    values = []
    for lo, hi in domains:
        point = vertex
        if lo is not None:
            point = max(lo, point)
        if hi is not None:
            point = min(hi, point)
        values.append(-zeta * point * point - xi * point)
    return max(values)


def cell_tables(c, guard):
    clo, chi = F(c[0], SCALE), F(c[1], SCALE)
    require(0 < clo <= chi <= RADIUS, "Positive exact knot enclosure")
    costs, penalties, contact_counts = [], [], {"two_rays": 0, "one_unbounded_ray": 0}
    for node in range(273):
        guard()
        L, H = max(F(0), F(node, 64) - STEP / 2), min(RADIUS, F(node, 64) + STEP / 2)
        domains = reciprocal_domains(L - chi, H - clo)
        contact_counts["two_rays"] += len(domains) == 2
        contact_counts["one_unbounded_ray"] += len(domains) == 1 and any(endpoint is None for endpoint in domains[0])
        # Floor for a LOWER k0 value; all signed penalties are CEILED.
        k0 = 1 / (chi * chi * H)
        costs.append(integer.floor_fraction_scaled(k0))
        penalties.append([ceil_scaled(penalty_maximum(zeta, xi, domains)) for zeta, xi in PAIRS])
    return costs, penalties, contact_counts


def frequency_data(N, guard):
    """Reuse pure integer primitives, not the old helper's timed entry point."""
    result = []
    for j in range(N):
        guard()
        q = F(3 * (2 * j + 1), 2 * N)
        qr = integer.fraction_interval(q * RADIUS)
        require(qr[0] == qr[1], "Exactly represented qR")
        coefficients = [integer.fraction_interval(q ** 3 / 6)]
        for order in range(1, DEGREE + 1):
            previous = coefficients[-1]
            coefficients.append((previous[0] * qr[0] // (SCALE * (order + 3)),
                                 ceil_div(previous[1] * qr[1], SCALE * (order + 3))))
        exp_tail = (q * RADIUS) ** 61 / math.factorial(61)
        result.append({"q": q, "coefficients": coefficients,
                       "HG_tail": ceil_scaled(q ** 3 * exp_tail / 6),
                       "mesh": ceil_scaled(q ** 4 * STEP / 48)})
    return result


def float_search_seeds(root, N, anchor_count, table_by_tag, guard):
    """Return rational index triples ONLY; discard all numerical values."""
    import n4_Q3_signed_joint_response_pilot_2026_10_08 as search
    np = search.np
    require(np is not None, "Installed NumPy for SEARCH ONLY")
    q = 3 * (np.arange(N) + .5) / N
    tau_values = np.array(list(map(float, TAUS)))
    zetas = np.array([float(zeta) for zeta, _ in PAIRS])
    suprema = []
    nodes = np.arange(273) / 64
    for name, sign in (("b", 1), ("a", -1)):
        guard()
        c = sum(root[name + "_bracket"]) / (2 * SCALE)
        costs, penalties, _ = table_by_tag[name]
        penalty_float = np.array(penalties, dtype=float) / SCALE
        cost_float = np.array(costs, dtype=float) / SCALE
        values = np.full((len(TAUS), len(PAIRS), N), -math.inf)
        for start in range(0, 273, 64):
            guard()
            end = min(273, start + 64)
            norm = np.abs(search.responses(nodes[start:end], c, sign, q)) / q ** 3 + q * float(STEP) / 48
            for it, tau in enumerate(tau_values):
                v = norm[None, :, :] - tau * cost_float[start:end][None, :, None] + penalty_float[start:end, :, None].transpose(1, 0, 2)
                values[it] = np.maximum(values[it], v.max(axis=1))
        suprema.append(values)
    plus, minus = suprema
    cost = float(root["p0"]) * tau_values[:, None, None] + float(F(root["u_bracket"][1], SCALE)) * (zetas[None, :, None] + zetas[None, None, :])
    selected = [set() for _ in range(N)]
    negative_search_count = 0
    for anchor in range(anchor_count):
        guard()
        eta = float(root["eta_max_upper"] * F(anchor, anchor_count - 1))
        best = np.full(N, math.inf)
        best_indices = np.zeros((N, 3), dtype=int)
        for it in range(len(TAUS)):
            values = cost[it, :, :, None] + eta * np.maximum(plus[it, :, None, :], minus[it, None, :, :])
            mask = values < 0
            negative_search_count += int(np.count_nonzero(mask))
            values[mask] = math.inf
            flat = values.reshape(len(PAIRS) ** 2, N)
            indices = flat.argmin(axis=0)
            candidates = flat[indices, np.arange(N)]
            improve = candidates < best
            best[improve] = candidates[improve]
            best_indices[improve, 0] = it
            best_indices[improve, 1] = indices[improve] // len(PAIRS)
            best_indices[improve, 2] = indices[improve] % len(PAIRS)
        require(np.all(np.isfinite(best)), "At least one finite search seed per q/anchor")
        for iq, indices in enumerate(best_indices):
            selected[iq].add(tuple(map(int, indices)))
    # Validate the only objects allowed to cross into the exact verifier.
    for candidates in selected:
        require(candidates, "Nonempty per-frequency rational seed list")
        for it, ip, im in candidates:
            require(0 <= it < len(TAUS) and 0 <= ip < len(PAIRS) and 0 <= im < len(PAIRS), "Indices in predeclared exact price arrays")
    return [sorted(candidates) for candidates in selected], {"anchor_count": anchor_count,
                                                           "floating_negative_search_values_ignored": negative_search_count,
                                                           "floating_values_retained_as_proof_bounds": False}


def verify_tag(c, table, data, wanted, guard):
    costs, penalties, contact_counts = table
    normalized = (c[0] * 4 // 17, ceil_div(c[1] * 4, 17))
    powers = [(SCALE, SCALE)]
    for order in range(1, DEGREE + 1):
        powers.append(integer.positive_multiply(powers[-1], normalized))
    all_keys = sorted(set(key for keys in wanted for key in keys))
    offsets = {key: [penalties[node][key[1]] - costs[node] * TAUS[key[0]].numerator // TAUS[key[0]].denominator
                     for node in range(273)] for key in all_keys}
    maxima = [{key: None for key in keys} for keys in wanted]
    checks = 0
    for node in range(273):
        guard()
        homogeneous = integer.homogeneous_at_node(powers, node)
        for j, item in enumerate(data):
            rectangle = integer.response_rectangle(item["coefficients"], homogeneous)
            response = integer.rectangle_modulus_upper(rectangle) + item["HG_tail"] + item["mesh"]
            q = item["q"]
            normalized_upper = ceil_div(response * q.denominator ** 3, q.numerator ** 3)
            for key in wanted[j]:
                candidate = normalized_upper + offsets[key][node]
                if maxima[j][key] is None or candidate > maxima[j][key]:
                    maxima[j][key] = candidate
            checks += 1
    require(all(value is not None for row in maxima for value in row.values()), "Every selected tag model freshly evaluated on every cell")
    return maxima, {"node_frequency_response_count": checks, "unique_tag_price_pairs": len(all_keys),
                    "contact_cell_counts": contact_counts, "HG_interval_c_enclosure_used": True}


def compute_verified_models(w, beta, N, anchor_count=17, time_limit_seconds=TIME_LIMIT):
    """Fresh replay API. JSON tables/source hashes are never trusted inputs."""
    started = time.monotonic()
    require(N in (64, 512) and anchor_count in (17, 33), "Fixed small verified grid and search anchors")
    require(0 < time_limit_seconds <= TIME_LIMIT, "Cooperative time guard<=45s")
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Exact affine elapsed budget")
        peak = integer.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Exact affine working-set budget")
    root = root_data(w, beta)
    tables = {name: cell_tables(root[name + "_bracket"], guard) for name in ("a", "b")}
    selected, search_metadata = float_search_seeds(root, N, anchor_count, tables, guard)
    data = frequency_data(N, guard)
    plus_wanted = [sorted(set((it, ip) for it, ip, im in row)) for row in selected]
    minus_wanted = [sorted(set((it, im) for it, ip, im in row)) for row in selected]
    plus, plus_metadata = verify_tag(root["b_bracket"], tables["b"], data, plus_wanted, guard)
    minus, minus_metadata = verify_tag(root["a_bracket"], tables["a"], data, minus_wanted, guard)
    frequency_models = []
    u_hi = F(root["u_bracket"][1], SCALE)
    for j, tuples in enumerate(selected):
        models = []
        for it, ip, im in tuples:
            zeta_plus, xi_plus = PAIRS[ip]
            zeta_minus, xi_minus = PAIRS[im]
            require(TAUS[it] >= 0 and zeta_plus >= 0 and zeta_minus >= 0, "Nonnegative inequality multipliers")
            A = root["p0"] * TAUS[it] + u_hi * (zeta_plus + zeta_minus)
            S = max(plus[j][(it, ip)], minus[j][(it, im)])
            models.append({"A": A, "A_upper_int": ceil_scaled(A), "S_upper_int": S,
                           "price_indices": (it, ip, im)})
        frequency_models.append({"q": data[j]["q"], "models": models})
    guard()
    return {"status": "EXACT_AFFINE_DUAL_RADIUS_ENCLOSURES", "scale": SCALE, "N": N,
            "root_data": root, "frequency_models": frequency_models,
            "prices": {"tau": TAUS, "pairs": PAIRS}, "search_metadata": search_metadata,
            "verification_metadata": {"positive_tag": plus_metadata, "negative_tag": minus_metadata,
                                      "HG_degree": DEGREE, "R": RADIUS, "y_step": STEP,
                                      "HG_tail": "q^3/6*(qR)^61/61!", "raw_mesh": "q^4*h/48",
                                      "normalized_response": "ceil_SCALE[(rectangle_norm_up+HG_tail_up+mesh_up)/q^3]",
                                      "cost": "floor_SCALE[1/(c_hi^2*y_cell_hi)]",
                                      "pole": "exact Fraction concave maximum over actual interval/two-ray enclosure of1/(y-c), then CEIL_SCALE; signed values are not clipped",
                                      "model": "|delta(q)|<=q^3*(A+eta*S_upper_int/SCALE), valid all feasible eta>=0; candidate nonnegativity is a consumer obligation",
                                      "fresh_replay": True, "exact_cell_table_not_from_JSON": True,
                                      "source_pin_is_integrity_not_proof": True},
            "source_pins": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                            for path in (Path(__file__), Path(integer.__file__), integer.SUPPORT_NOTE)},
            "resources": {"elapsed_seconds_diagnostic_only": time.monotonic() - started,
                          "peak_working_set_bytes": integer.peak_bytes(), "time_limit_seconds": time_limit_seconds,
                          "memory_limit_bytes": MEMORY_LIMIT, "one_BLAS_thread": True},
            "conclusions": {"floating_bounds_used_as_proof_premises": False, "CDF_bound_proved": False,
                            "all_eta_CDF_certified": False, "all_w_beta_cover": False,
                            "old_globals_or_receipts_modified": False}}


def json_ready(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, choices=(64, 512), default=64)
    parser.add_argument("--anchors", type=int, choices=(17, 33), default=17)
    args = parser.parse_args()
    output = Path(__file__).with_name(Path(__file__).stem + "_N" + str(args.N) + ".json")
    require(not output.exists(), "Never overwrite an exact affine receipt")
    result = compute_verified_models(F(9, 10), F(9, 20), args.N, args.anchors)
    raw = json.dumps(json_ready(result), sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Exact affine receipt<=2MiB")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)
    counts = [len(item["models"]) for item in result["frequency_models"]]
    print(json.dumps({"status": result["status"], "result": str(output), "N": args.N,
                      "output_bytes": len(raw.encode("utf-8")), "model_count": sum(counts),
                      "models_per_frequency_min_max": [min(counts), max(counts)],
                      "verification_metadata": json_ready(result["verification_metadata"]),
                      "search_metadata": result["search_metadata"], "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
