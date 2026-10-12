"""Small signed Q3 Fourier-polynomial pilot, NOT a CDF/n4 certificate.

The exact Hermite and quartic formulas have been independently audited.
The grid, coefficients, and transcendental evaluations below are floating;
analytic mesh/tail margins are recorded but floating roundoff is NOT certified.
Only two preselected problematic charts, 24 frequencies, five thresholds,
three smoothing widths, and 17 fixed laws are used. Arrays are streamed in
batches of 128, BLAS uses one thread, and no optimizer or Lean build runs.
Cooperative budgets: 30 seconds, 256 MiB peak working set, 96 KiB output.
An existing result is never replaced.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import time

STARTED = time.monotonic()
import n4_Q3_shared_sample_gram_probe_2026_10_08 as previous
np = previous.np

RESULT = "n4_Q3_signed_joint_response_pilot_2026_10_08.json"
TIME_LIMIT = 30.0
MEMORY_LIMIT = 256 * 1024 * 1024
OUTPUT_LIMIT = 96 * 1024
STEP = 1 / 32
RADIUS = 128.0
BATCH = 128
T_VALUES = (.75, 1.0, 1.5)
H_VALUES = (-.8, -.4, 0.0, .4, .8)
T_NODES = tuple(j / 12 for j in range(1, 25))
DUAL_LAMBDAS = (0.0, .001, .0025, .005, .01, .02, .04, .08, .16, .32)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def guard():
    require(time.monotonic() - STARTED < TIME_LIMIT, "Elapsed budget")
    peak = previous.peak_bytes()
    require(peak is None or peak <= MEMORY_LIMIT, "Peak-working-set budget")


def responses(y_values, c, sign, raw_frequencies):
    """f[0,c,c,y], using a convergent series near removable contacts."""
    y = np.asarray(y_values, dtype=float)
    k = sign * raw_frequencies
    ik = 1j * k
    fc = np.exp(ik * c)
    alpha = (2 * np.expm1(ik * c) - c * ik * fc) / c
    beta = (c * ik * fc - np.expm1(ik * c)) / (c * c)
    result = np.empty((len(y), len(k)), dtype=np.complex128)
    series_mask = (y <= 4) if c <= 4 else np.zeros(len(y), dtype=bool)
    if np.any(series_mask):
        ys = y[series_mask]
        homogeneous = np.ones(len(ys))
        c_power = 1.0
        coefficient = ik ** 3 / 6
        block = homogeneous[:, None] * coefficient
        for n in range(1, 61):
            c_power *= c
            homogeneous = ys * homogeneous + (n + 1) * c_power
            coefficient = coefficient * ik / (n + 3)
            block += homogeneous[:, None] * coefficient
        result[series_mask] = block
    direct_mask = ~series_mask
    zero_mask = direct_mask & (y == 0)
    contact_mask = direct_mask & (y == c)
    if np.any(zero_mask):
        result[zero_mask] = (ik - alpha) / (c * c)
    if np.any(contact_mask):
        result[contact_mask] = (-k * k * fc / 2 - beta) / c
    regular_mask = direct_mask & ~zero_mask & ~contact_mask
    if np.any(regular_mask):
        yr = y[regular_mask, None]
        numerator = np.expm1(yr * ik) - alpha * yr - beta * yr * yr
        result[regular_mask] = numerator / (yr * (yr - c) ** 2)
    require(np.all(np.isfinite(result)), "Finite Hermite responses")
    return result


def coefficients(t_nodes, smoothing_width, threshold):
    return (1j / (12 * math.pi * t_nodes)
            * np.exp(-t_nodes * t_nodes / (2 * smoothing_width ** 2))
            * np.exp(-1j * t_nodes * threshold))


def chart_probe(w, beta_chart, exact_eta):
    guard()
    w, beta_chart = float(w), float(beta_chart)
    u = math.sqrt(w * (1 - beta_chart * beta_chart)) / 2
    a, b = (1 - beta_chart) / (2 * u), (1 + beta_chart) / (2 * u)
    rho_q = (1 + beta_chart * beta_chart) / (2 * u)
    eta = float(Fraction(exact_eta))
    require(RADIUS >= 2 * max(a, b), "Analytic tail domain")
    t = np.array(T_NODES)
    q = t / 2
    phi_q = (w * (1 + beta_chart) / 2 * np.exp(-1j * q * a)
             + 1 - w + w * (1 - beta_chart) / 2 * np.exp(1j * q * b))
    labels = [(width, h) for width in T_VALUES for h in H_VALUES]
    kappas = np.array([coefficients(t, width, h) for width, h in labels])
    z = 4 * kappas * phi_q[None, :] ** 3
    maxima = np.zeros(len(labels))
    minima = np.zeros(len(labels))
    argmax = [(0, 0.0)] * len(labels)
    individual_maxima = np.zeros((len(labels), len(q)))
    individual_minima = np.zeros_like(individual_maxima)
    dual_maxima = np.zeros((len(labels), len(DUAL_LAMBDAS)))
    dual_negative_maxima = np.zeros_like(dual_maxima)
    lambdas = np.array(DUAL_LAMBDAS)
    pointwise_excess = -math.inf
    count = int(RADIUS / STEP) + 1
    for sign, c in ((1, b), (-1, a)):
        for start in range(0, count, BATCH):
            guard()
            ys = np.arange(start, min(count, start + BATCH)) * STEP
            r = responses(ys, c, sign, q)
            pointwise_excess = max(pointwise_excess, float(np.max(np.abs(r) - q ** 3 / 6)))
            values = (r @ z.T).real
            # In a nearest-node half-cell, y <= y_node + mesh/2. Thus this
            # is a lower bound on the singular positive cost throughout it.
            cost_lower = 1 / (c * c * (ys + STEP / 2))
            for j in range(len(labels)):
                penalty = cost_lower[:, None] * lambdas
                dual_maxima[j] = np.maximum(dual_maxima[j], np.max(values[:, j, None] - penalty, axis=0))
                dual_negative_maxima[j] = np.maximum(dual_negative_maxima[j], np.max(-values[:, j, None] - penalty, axis=0))
            batch_indices = np.argmax(values, axis=0)
            batch_maxima = values[batch_indices, np.arange(len(labels))]
            for j in range(len(labels)):
                if batch_maxima[j] > maxima[j]:
                    argmax[j] = (sign, float(ys[batch_indices[j]]))
            maxima = np.maximum(maxima, batch_maxima)
            minima = np.minimum(minima, np.min(values, axis=0))
            for j, row in enumerate(z):
                individual = (r * row).real
                individual_maxima[j] = np.maximum(individual_maxima[j], np.max(individual, axis=0))
                individual_minima[j] = np.minimum(individual_minima[j], np.min(individual, axis=0))
    require(pointwise_excess < 2e-10, "Hermite pointwise-bound regression")
    slope = np.abs(z) * q ** 4 / 24
    tail = np.abs(z) * (8 / RADIUS ** 3 + 12 * q / RADIUS ** 2 + 2 * q ** 2 / RADIUS)
    mesh_margins = np.sum(slope, axis=1) * STEP / 2
    tail_caps = np.sum(tail, axis=1)
    joint_upper = np.maximum(maxima + mesh_margins, tail_caps)
    joint_lower = np.minimum(minima - mesh_margins, -tail_caps)
    separate_upper = np.sum(np.maximum(individual_maxima + slope * STEP / 2, tail), axis=1)
    separate_lower = np.sum(np.minimum(individual_minima - slope * STEP / 2, -tail), axis=1)
    triangle = np.sum(np.abs(z) * q ** 3 / 6, axis=1)
    epsilon = np.minimum(2, eta * q ** 3 / 6)
    remainder = np.sum(np.abs(kappas) * (
        6 * np.abs(phi_q) ** 2 * epsilon ** 2
        + 4 * np.abs(phi_q) * epsilon ** 3 + epsilon ** 4), axis=1)
    dual_upper_all = ((1 - w) * lambdas[None, :] + eta * np.maximum(
        dual_maxima + mesh_margins[:, None], tail_caps[:, None]))
    dual_negative_upper_all = ((1 - w) * lambdas[None, :] + eta * np.maximum(
        dual_negative_maxima + mesh_margins[:, None], tail_caps[:, None]))
    rows = []
    for j, (width, h) in enumerate(labels):
        chosen_dual = int(np.argmin(dual_upper_all[j]))
        chosen_negative_dual = int(np.argmin(dual_negative_upper_all[j]))
        constrained_linear = float(dual_upper_all[j, chosen_dual])
        rows.append({
            "smoothing_width": width, "H": h,
            "sampled_signed_maximum": float(maxima[j]),
            "sampled_signed_minimum": float(minima[j]),
            "sampled_maximizer_sign_and_magnitude": argmax[j],
            "analytic_mesh_margin_evaluated_in_float": float(mesh_margins[j]),
            "analytic_tail_cap_evaluated_in_float": float(tail_caps[j]),
            "joint_linear_upper_per_eta_float": float(joint_upper[j]),
            "joint_linear_lower_per_eta_float": float(joint_lower[j]),
            "independent_signed_upper_per_eta_float": float(separate_upper[j]),
            "independent_signed_lower_per_eta_float": float(separate_lower[j]),
            "triangle_linear_per_eta_float": float(triangle[j]),
            "quartic_remainder_upper_float": float(remainder[j]),
            "joint_full_proxy_upper_float": float(eta * joint_upper[j] + remainder[j]),
            "joint_full_proxy_lower_float": float(eta * joint_lower[j] - remainder[j]),
            "triangle_full_proxy_upper_float": float(eta * triangle[j] + remainder[j]),
            "linear_triangle_to_joint_ratio_float": float(triangle[j] / joint_upper[j]),
            "independent_signed_to_joint_ratio_float": float(separate_upper[j] / joint_upper[j]),
            "full_triangle_to_joint_ratio_float": float((eta * triangle[j] + remainder[j])
                                                         / (eta * joint_upper[j] + remainder[j])),
            "zero_mass_constraint_linear_upper_float": constrained_linear,
            "zero_mass_constraint_linear_lower_float": -float(dual_negative_upper_all[j, chosen_negative_dual]),
            "chosen_upper_dual_lambda": DUAL_LAMBDAS[chosen_dual],
            "chosen_lower_dual_lambda": DUAL_LAMBDAS[chosen_negative_dual],
            "zero_mass_constrained_full_proxy_upper_float": constrained_linear + float(remainder[j]),
            "zero_mass_constrained_full_proxy_lower_float": -float(dual_negative_upper_all[j, chosen_negative_dual] + remainder[j]),
            "joint_to_zero_mass_constrained_linear_ratio_float": float(eta * joint_upper[j] / constrained_linear),
            "triangle_to_zero_mass_constrained_full_ratio_float": float((eta * triangle[j] + remainder[j])
                                                                       / (constrained_linear + remainder[j])),
        })
    return {"w": w, "beta": beta_chart, "exact_eta": exact_eta, "eta": eta,
            "a": a, "b": b, "rho_Q3": rho_q, "rho": rho_q + eta,
            "measure_relaxation": "Unconstrained common nu and tighter eta*integral[1/(c^2*y)]dnu<=p0=1-w. The latter is necessary but not sufficient for an actual law.",
            "pointwise_modulus_regression_max_excess": pointwise_excess, "rows": rows}


def actual_law_regression(law):
    guard()
    x, p = np.array(law["points"]), np.array(law["probabilities"])
    moments = previous.sign_moments(x, p)
    u = (moments["u_plus"] + moments["u_minus"]) / 2
    a, b = moments["v_minus"] / u, moments["v_plus"] / u
    t, q = np.array(T_NODES), np.array(T_NODES) / 2
    phi_q = u / a * np.exp(-1j * q * a) + 1 - u / a - u / b + u / b * np.exp(1j * q * b)
    phi_p = np.sum(p[:, None] * np.exp(1j * x[:, None] * q), axis=0)
    response = np.empty((len(x), len(q)), dtype=np.complex128)
    for sign, c in ((1, b), (-1, a)):
        mask = x >= 0 if sign == 1 else x < 0
        if np.any(mask):
            response[mask] = responses(np.abs(x[mask]), c, sign, q)
    weights = np.maximum(x, 0) * (x - b) ** 2 + np.maximum(-x, 0) * (x + a) ** 2
    eta = float(np.sum(p * weights))
    zero_mass_reference = 1 - u / a - u / b
    zero_mass_actual = float(np.sum(p[x == 0]))
    sign_radius = np.where(x >= 0, b, a)
    active = weights > 1e-24
    cost_integral = float(np.sum(p[active] * weights[active]
                                / (sign_radius[active] ** 2 * np.abs(x[active]))))
    cost_identity_error = abs(cost_integral - (zero_mass_reference - zero_mass_actual))
    require(cost_identity_error < 2e-10 * max(1, moments["rho"]), "Zero-mass cost identity regression")
    represented = np.sum((p * weights)[:, None] * response, axis=0)
    identity_error = float(np.max(np.abs(phi_p - phi_q - represented)))
    require(identity_error < 2e-10 * max(1, moments["rho"]), "Exact signed-response identity regression")
    max_remainder_excess = -math.inf
    for width in T_VALUES:
        for h in H_VALUES:
            kappa = coefficients(t, width, h)
            first_order = np.real(np.sum(4 * kappa * phi_q ** 3 * represented))
            direct_difference = np.real(np.sum(kappa * (phi_p ** 4 - phi_q ** 4)))
            epsilon = np.minimum(2, eta * q ** 3 / 6)
            cap = np.sum(np.abs(kappa) * (6 * np.abs(phi_q) ** 2 * epsilon ** 2
                                         + 4 * np.abs(phi_q) * epsilon ** 3 + epsilon ** 4))
            max_remainder_excess = max(max_remainder_excess, float(abs(direct_difference - first_order) - cap))
    require(max_remainder_excess < 2e-10 * max(1, moments["rho"]), "Quartic remainder regression")
    return {"label": law["label"], "rho": moments["rho"], "eta": eta,
            "zero_mass_cost_identity_abs_error": cost_identity_error,
            "response_identity_max_abs_error": identity_error,
            "quartic_remainder_max_upper_excess": max_remainder_excess}


def main():
    output = Path(__file__).with_name(RESULT)
    require(not output.exists(), "Refuse to overwrite a previous pilot")
    require(np is not None, "NumPy required for this bounded pilot")
    charts = [chart_probe(.97, .3, "1633550843/10796617633"),
              chart_probe(.9, .3, "113089567/365551652")]
    laws = previous.fixed.fixed_laws()
    root3 = math.sqrt(3)
    laws.append({"label": "genuine_Q3_exact_rational_raw_law",
                 "points": (-2 / root3, 0.0, 3 / root3), "probabilities": (.3, .5, .2)})
    regressions = [actual_law_regression(law) for law in laws]
    rows = [row for chart in charts for row in chart["rows"]]
    result = {
        "status": "FLOATING_SIGNED_FINITE_FOURIER_PROXY_PILOT_NOT_CDF_CERTIFICATE",
        "date": "2026-10-08",
        "source_pins": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in (Path(__file__), Path(previous.__file__), Path(previous.fixed.__file__))},
        "finite_proxy": "F_H(P)=Re sum_j kappa_j phi_P(t_j/2)^4; kappa_j=i/(12*pi*t_j)*exp(-t_j^2/(2*T^2))*exp(-i*t_j*H). This is only a finite smooth Fourier polynomial, NOT a CDF bound.",
        "frequencies": list(T_NODES), "raw_frequencies": [t / 2 for t in T_NODES],
        "grid": {"radius": RADIUS, "step": STEP, "batch": BATCH, "points_per_tag": int(RADIUS / STEP) + 1},
        "necessary_zero_mass_constraint": "eta*integral[1/(c^2*y)]dnu=p0-P(X=0)<=p0; c=b on positive tag and c=a on negative tag. Dual: eta*E K <= lambda*p0 + eta*sup(K-lambda/(c^2*y)).",
        "tested_dual_lambdas": list(DUAL_LAMBDAS),
        "charts": charts, "actual_law_regressions": regressions,
        "summary": {
            "linear_triangle_to_joint_ratio_min": min(r["linear_triangle_to_joint_ratio_float"] for r in rows),
            "linear_triangle_to_joint_ratio_max": max(r["linear_triangle_to_joint_ratio_float"] for r in rows),
            "independent_signed_to_joint_ratio_min": min(r["independent_signed_to_joint_ratio_float"] for r in rows),
            "independent_signed_to_joint_ratio_max": max(r["independent_signed_to_joint_ratio_float"] for r in rows),
            "full_triangle_to_joint_ratio_min": min(r["full_triangle_to_joint_ratio_float"] for r in rows),
            "full_triangle_to_joint_ratio_max": max(r["full_triangle_to_joint_ratio_float"] for r in rows),
            "triangle_to_zero_mass_constrained_full_ratio_min": min(r["triangle_to_zero_mass_constrained_full_ratio_float"] for r in rows),
            "triangle_to_zero_mass_constrained_full_ratio_max": max(r["triangle_to_zero_mass_constrained_full_ratio_float"] for r in rows),
            "joint_to_zero_mass_constrained_linear_ratio_max": max(r["joint_to_zero_mass_constrained_linear_ratio_float"] for r in rows),
            "response_identity_max_abs_error": max(r["response_identity_max_abs_error"] for r in regressions),
        },
        "resources": {"elapsed_seconds": time.monotonic() - STARTED,
                      "peak_working_set_bytes": previous.peak_bytes(), "time_limit_seconds": TIME_LIMIT,
                      "memory_limit_bytes": MEMORY_LIMIT, "BLAS_threads_requested": 1,
                      "cooperative_not_OS_limit": True},
        "conclusions": {"analytic_formulas_independently_audited": True,
                        "floating_regressions_passed": True, "floating_roundoff_certified": False,
                        "numeric_interval_certificate": False, "CDF_target_tested_or_proved": False,
                        "unrestricted_n4_closed": False, "M4_used": False},
    }
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Output budget")
    guard()
    with output.open("x", encoding="utf-8") as stream:
        stream.write(raw)
    print(json.dumps({"status": result["status"], "result": str(output),
                      "summary": result["summary"], "resources": result["resources"]}, sort_keys=True))


if __name__ == "__main__":
    main()
