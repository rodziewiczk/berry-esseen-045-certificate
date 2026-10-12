"""Small floating diagnostic of shared-frequency augmented Fourier Grams.

This script does not prove a law-class bound, certify numerical inequalities,
evaluate a CDF, assume/use M4, or import any repository optimization module.
The universal mathematical identities are stated separately in EXACT_ALGEBRA.
Only the floating sample checks below are executed.

Resource contract: <=32 fixed laws, <=32 fixed frequencies, <=4 atoms per law,
matrix dimension <=34, one BLAS thread, retained numeric-data budget <2 MiB,
JSON output <=128 KiB, elapsed budget 30 s. On Windows the process peak working
set is sampled after each law and checked against 768 MiB. These checks are
cooperative, not an operating-system deadline or a proof of an RSS limit.
NumPy is optional; without it the eigenvalue checks are reported unavailable.
The output name must be absent: an earlier diagnostic is never overwritten.
"""

from __future__ import annotations

import cmath
import ctypes
import json
import math
import os
from pathlib import Path
import sys
import time

# Set these before the optional NumPy import.
for _thread_variable in (
    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS",
):
    os.environ[_thread_variable] = "1"

STARTED = time.monotonic()
try:
    import numpy as np
except ImportError:
    np = None

SOURCE = "n4_shared_sample_gram_probe_2026_10_08.py"
RESULT = "n4_shared_sample_gram_probe_result_2026_10_08.json"
TIME_BUDGET_SECONDS = 30.0
PEAK_MEMORY_BUDGET_BYTES = 768 * 1024 * 1024
OUTPUT_BUDGET_BYTES = 128 * 1024
NUMERIC_TOLERANCE = 2e-10
FREQUENCIES = tuple(sorted({j / 8 for j in range(25)} | {math.pi / 2}))
TARGET_RHOS = (1.31145, 1.51381)

EXACT_ALGEBRA = {
    "scope": "Identities and implications under EX=0, EX^2=1, rho=E|X|^3<infinity; sample arithmetic is not their proof.",
    "augmented_gram": {
        "basis": "1, X, exp(i*t_1*X), ..., exp(i*t_m*X)",
        "definitions": "phi(t)=E exp(i*t*X); psi(t)=E[X exp(i*t*X)]",
        "schur_residual": "C_jk=phi(t_k-t_j)-conj(phi(t_j))*phi(t_k)-conj(psi(t_j))*psi(t_k)",
        "positivity": "C is the Gram matrix of exp(i*t_j*X)-phi(t_j)-psi(t_j)*X, so C>=0.",
        "diagonal": "R(t)=1-|phi(t)|^2-|psi(t)|^2>=0",
        "finite_M4_assumed_or_used": False,
    },
    "crude_modulus_cap": {
        "psi_lower": "|psi(t)-i*t|<=rho*t^2/2, by |exp(i*u)-1-i*u|<=u^2/2; hence |psi(t)|>=max(0,|t|-rho*t^2/2).",
        "cap": "|phi(t)|<=sqrt(1-max(0,|t|-rho*t^2/2)^2)",
        "rho_domain": "rho>=1",
        "domination_by_existing_symmetrized_cosine_cap": "Let y=|t|. On 0<=y<=2/rho, the difference of new and old radicands is y^3*[rho-(rho+1)/5-rho^2*y/4]>=y^3*(3*rho-2)/10>=0. Also y<=2/rho<=5/(rho+1), so the old radicand is <=1 there. For y>=2/rho the new cap is 1, while the old clipped cap is <=1. Therefore the new cap never improves min(1,sqrt(1-y^2+(rho+1)*y^3/5)) for rho>=1.",
    },
    "weighted_gram_redundancy": {
        "definitions": "K_jk=phi(t_k-t_j), D=diag(phi(t_j)), G_jk=phi(t_j)*conj(phi(t_k))*phi(t_k-t_j)",
        "identity": "G=D K D*",
        "consequence": "K>=0 implies G>=0; when D is invertible this is equivalent positivity. It adds no extra constraint beyond ordinary characteristic-function Gram positivity.",
    },
    "binary_defect_ledger": {
        "definitions": "gamma=EX^3; s=sqrt(gamma^2+4); a=(s-gamma)/2; b=(s+gamma)/2; ab=1; Q_gamma has mass b/s at -a and a/s at b; E Q_gamma^3=gamma.",
        "reference": "A=phi_Qgamma(t), B=psi_Qgamma(t); exp(i*t*x)=A+B*x at x=-a,b.",
        "defect": "d=rho-(gamma^2+2)/s",
        "identity": "E|exp(i*t*X)-A-B*X|^2=R(t)+|phi_P(t)-A|^2+|psi_P(t)-B|^2",
        "upper": "E|exp(i*t*X)-A-B*X|^2<=C_gamma(t)*d, C_gamma(t)=min(s^3*D^2/(4*a_star^2),s^3*t^2*D/(8*a_star)); D=|t|+|B|, a_star=min(a,b). In particular C_gamma(t)<=s^3*|t|^3/(4*a_star), since |B|<=|t|.",
        "scope": "The displayed upper bound is a proposed analytically derived ledger supplied for this diagnostic; finite floating samples do not certify its all-law validity.",
    },
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def peak_working_set_bytes():
    if os.name != "nt":
        return None

    class MemoryCounters(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(MemoryCounters), ctypes.c_ulong]
    psapi.GetProcessMemoryInfo.restype = ctypes.c_int
    counters = MemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    ok = psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb)
    return int(counters.PeakWorkingSetSize) if ok else None


def guard():
    require(time.monotonic() - STARTED < TIME_BUDGET_SECONDS, "Probe elapsed-time budget exceeded")
    peak = peak_working_set_bytes()
    require(peak is None or peak <= PEAK_MEMORY_BUDGET_BYTES, "Probe peak-working-set budget exceeded")


def complex_sum(values):
    values = tuple(values)
    return complex(math.fsum(value.real for value in values), math.fsum(value.imag for value in values))


def standardized(label, points, probabilities, binary=False):
    require(len(points) == len(probabilities) <= 4, "Fixed at-most-four-atom law")
    require(all(p > 0 for p in probabilities), "Strictly positive sample probabilities")
    mass = math.fsum(probabilities)
    probs = tuple(p / mass for p in probabilities)
    mean = math.fsum(p * x for p, x in zip(probs, points))
    variance = math.fsum(p * (x - mean) ** 2 for p, x in zip(probs, points))
    require(variance > 0, "Nondegenerate sample law")
    scale = math.sqrt(variance)
    atoms = tuple((x - mean) / scale for x in points)
    return {"label": label, "points": atoms, "probabilities": probs, "binary": binary}


def binary_for_rho(rho):
    gamma_squared = (rho * rho - 4 + rho * math.sqrt(rho * rho + 8)) / 2
    gamma = math.sqrt(max(0.0, gamma_squared))
    s = math.sqrt(gamma * gamma + 4)
    b = (s + gamma) / 2
    a = 1 / b  # ab=1; avoids subtraction cancellation in a rare binary tail.
    return standardized(f"binary_target_rho_{rho}", (-a, b), (b / s, a / s), binary=True)


def fixed_laws():
    laws = [
        standardized("binary_fair", (-1, 1), (.5, .5), binary=True),
        standardized("binary_p025", (0, 1), (.75, .25), binary=True),
        standardized("binary_p010", (0, 1), (.9, .1), binary=True),
        standardized("binary_p002", (0, 1), (.98, .02), binary=True),
        *(binary_for_rho(rho) for rho in TARGET_RHOS),
        standardized("three_lazy_zero", (-1, 0, 1), (.25, .5, .25)),
        standardized("three_asymmetric", (-3, .2, 2), (.15, .6, .25)),
        standardized("three_symmetric", (-2, 0, 2), (.4, .2, .4)),
        standardized("four_symmetric", (-2, -.5, .5, 2), (.1, .4, .4, .1)),
        standardized("four_asymmetric", (-3, -.2, .7, 4), (.1, .5, .3, .1)),
        standardized("rare_positive_20_eps_1e5", (-1, 1, 20), (.499995, .499995, .00001)),
        standardized("rare_positive_20_eps_1e4", (-1, 1, 20), (.49995, .49995, .0001)),
        standardized("rare_positive_100_eps_1e4", (-1, 1, 100), (.49995, .49995, .0001)),
        standardized("rare_symmetric_100_eps_1e4", (-100, -1, 1, 100), (.00005, .49995, .49995, .00005)),
        standardized("rare_two_tails_asymmetric", (-20, -1, 1, 40), (.00001, .49999, .49999, .00001)),
    ]
    require(len(laws) <= 32 and len(FREQUENCIES) <= 32, "Fixed sample cardinality budgets")
    return laws


def transforms(law, t):
    pairs = tuple(zip(law["probabilities"], law["points"]))
    phi = complex_sum(p * cmath.exp(1j * t * x) for p, x in pairs)
    psi = complex_sum(p * x * cmath.exp(1j * t * x) for p, x in pairs)
    return phi, psi


def caps(rho, t):
    y = abs(t)
    lower = max(0.0, y - rho * y * y / 2)
    require(lower <= 1 + NUMERIC_TOLERANCE, "Real Bessel cap radicand")
    new = math.sqrt(max(0.0, 1 - lower * lower))
    taylor = min(1.0, abs(1 - y * y / 2) + rho * y ** 3 / 6)
    existing = min(1.0, math.sqrt(max(0.0, 1 - y * y + (rho + 1) * y ** 3 / 5)))
    # Existing complex variation-of-constants comparison is used only on [0,pi].
    rademacher = min(1.0, abs(math.cos(y)) + math.sqrt(max(0.0, (rho - 1) * (rho + 5 / 3))) * (y - math.sin(y))) if y <= math.pi else None
    return {"trivial": 1.0, "taylor_triangle": taylor, "existing_cosine_cubic": existing,
            "existing_rademacher_comparison": rademacher, "new_crude_bessel": new}


def eigen_diagnostic(law, phis, psis):
    if np is None:
        return {"available": False, "reason": "NumPy not installed; no substitute eigenvalue claim"}
    count = len(FREQUENCIES)
    k = np.array([[transforms(law, tk - tj)[0] for tk in FREQUENCIES] for tj in FREQUENCIES], dtype=np.complex128)
    phi = np.array(phis, dtype=np.complex128)
    psi = np.array(psis, dtype=np.complex128)
    residual = k - np.outer(phi.conjugate(), phi) - np.outer(psi.conjugate(), psi)
    augmented = np.zeros((count + 2, count + 2), dtype=np.complex128)
    augmented[:2, :2] = np.eye(2)
    augmented[0, 2:], augmented[1, 2:] = phi, psi
    augmented[2:, 0], augmented[2:, 1] = phi.conjugate(), psi.conjugate()
    augmented[2:, 2:] = k
    d = np.diag(phi)
    weighted_from_entries = np.outer(phi, phi.conjugate()) * k
    weighted_from_congruence = d @ k @ d.conjugate().T
    matrices = {"ordinary_K": k, "augmented_1_X_fourier": augmented,
                "schur_residual": residual, "weighted_redundant_G": weighted_from_entries}
    minimums = {name: float(np.linalg.eigvalsh((matrix + matrix.conjugate().T) / 2).min())
                for name, matrix in matrices.items()}
    require(min(minimums.values()) >= -NUMERIC_TOLERANCE, "Sample floating Gram positivity regression")
    return {"available": True, "matrix_dimensions": [count, count + 2],
            "minimum_eigenvalues": minimums,
            "weighted_congruence_max_abs_error": float(np.max(np.abs(weighted_from_entries - weighted_from_congruence))),
            "binary_residual_max_abs_entry": float(np.max(np.abs(residual))) if law["binary"] else None,
            "numerical_PSD_tolerance": NUMERIC_TOLERANCE, "numeric_not_certified": True}


def law_diagnostic(law):
    guard()
    pairs = tuple(zip(law["probabilities"], law["points"]))
    mean = math.fsum(p * x for p, x in pairs)
    second = math.fsum(p * x * x for p, x in pairs)
    gamma = math.fsum(p * x ** 3 for p, x in pairs)
    rho = math.fsum(p * abs(x) ** 3 for p, x in pairs)
    s = math.sqrt(gamma * gamma + 4)
    if gamma >= 0:
        b = (s + gamma) / 2
        a = 1 / b
    else:
        a = (s - gamma) / 2
        b = 1 / a
    defect = rho - (gamma * gamma + 2) / s
    reference_pairs = ((b / s, -a), (a / s, b))
    reference_mean = math.fsum(p * x for p, x in reference_pairs)
    reference_variance = math.fsum(p * x * x for p, x in reference_pairs)
    reference_third = math.fsum(p * x ** 3 for p, x in reference_pairs)
    require(abs(a * b - 1) <= NUMERIC_TOLERANCE, "Qgamma ab=1 regression")
    require(abs(reference_mean) <= NUMERIC_TOLERANCE, "Qgamma mean-zero regression")
    require(abs(reference_variance - 1) <= NUMERIC_TOLERANCE, "Qgamma variance-one regression")
    require(abs(reference_third - gamma) <= NUMERIC_TOLERANCE * max(1, abs(gamma)), "Qgamma signed-third-moment orientation regression")
    require(abs(mean) < NUMERIC_TOLERANCE and abs(second - 1) < NUMERIC_TOLERANCE, "Sample standardization regression")
    require(defect >= -NUMERIC_TOLERANCE * max(1, rho), "Sample third-moment defect regression")
    phis, psis, rows, residuals, ledger_errors, ledger_excesses, ratios = [], [], [], [], [], [], []
    sharper_C_used_count = 0
    cap_violations = {}
    max_binary_ledger = 0.0
    for t in FREQUENCIES:
        phi, psi = transforms(law, t)
        phis.append(phi)
        psis.append(psi)
        residual = 1 - abs(phi) ** 2 - abs(psi) ** 2
        residuals.append(residual)
        A = (b * cmath.exp(-1j * t * a) + a * cmath.exp(1j * t * b)) / s
        B = (cmath.exp(1j * t * b) - cmath.exp(-1j * t * a)) / s
        direct = math.fsum(p * abs(cmath.exp(1j * t * x) - A - B * x) ** 2 for p, x in pairs)
        identity = residual + abs(phi - A) ** 2 + abs(psi - B) ** 2
        D = abs(t) + abs(B)
        quadratic_C = s ** 3 * D ** 2 / (4 * min(a, b) ** 2)
        cubic_C = s ** 3 * t ** 2 * D / (8 * min(a, b))
        C = min(quadratic_C, cubic_C)
        require(C <= s ** 3 * abs(t) ** 3 / (4 * min(a, b)) + NUMERIC_TOLERANCE * max(1, C), "Simple cubic cap regression")
        sharper_C_used_count += int(cubic_C < quadratic_C - NUMERIC_TOLERANCE)
        # Clamping a roundoff-sized negative binary defect is a diagnostic
        # convention, not a replacement for the exact mathematical defect.
        upper = C * max(0.0, defect)
        ledger_errors.append(abs(direct - identity))
        ledger_excesses.append(direct - upper)
        if upper > 1e-14:
            ratios.append(direct / upper)
        if law["binary"]:
            max_binary_ledger = max(max_binary_ledger, direct)
        values = caps(rho, t)
        for name, cap in values.items():
            if cap is not None:
                cap_violations[name] = max(cap_violations.get(name, -1.0), abs(phi) - cap)
        if t in (0.0, .5, 1.0, 1.5, 2.0, 2.5, 3.0, math.pi / 2):
            rows.append({"t": t, "phi": [phi.real, phi.imag], "psi": [psi.real, psi.imag],
                         "R": residual, "binary_ledger_direct": direct, "binary_ledger_Cd": upper,
                         "binary_ledger_quadratic_C": quadratic_C, "binary_ledger_cubic_C": cubic_C})
    require(min(residuals) >= -NUMERIC_TOLERANCE, "Floating augmented diagonal positivity")
    require(max(ledger_errors) <= NUMERIC_TOLERANCE * max(1, rho), "Floating binary-ledger identity regression")
    require(max(ledger_excesses) <= NUMERIC_TOLERANCE * max(1, rho), "Floating binary-ledger upper regression")
    require(max(cap_violations.values()) <= NUMERIC_TOLERANCE, "Floating sample sound-cap regression")
    if law["binary"]:
        require(max(abs(value) for value in residuals) <= NUMERIC_TOLERANCE, "Binary residual vanishes within tolerance")
        require(max_binary_ledger <= NUMERIC_TOLERANCE, "Binary ledger vanishes within tolerance")
    eigen = eigen_diagnostic(law, phis, psis)
    guard()
    return {"label": law["label"], "atom_count": len(pairs), "points": list(law["points"]),
            "probabilities": list(law["probabilities"]), "binary": law["binary"],
            "mean": mean, "second_moment": second, "rho": rho, "gamma": gamma,
            "binary_reference": {"a": a, "b": b, "s": s, "defect_d_raw": defect,
                                 "mean": reference_mean, "variance": reference_variance,
                                 "signed_third_moment": reference_third,
                                 "nodes": [-a, b], "probabilities": [b / s, a / s]},
            "minimum_R": min(residuals), "maximum_R": max(residuals),
            "binary_maximum_abs_R": max(abs(value) for value in residuals) if law["binary"] else None,
            "binary_ledger_max_abs_identity_error": max(ledger_errors),
            "binary_ledger_max_upper_excess": max(ledger_excesses),
            "binary_ledger_max_ratio_when_Cd_gt_1e_minus14": max(ratios) if ratios else None,
            "binary_ledger_cubic_C_stricter_frequency_count": sharper_C_used_count,
            "maximum_actual_modulus_minus_cap": cap_violations,
            "selected_transform_rows": rows, "multi_frequency": eigen}


def main():
    output_path = Path(__file__).with_name(RESULT)
    require(not output_path.exists(), "Refuse to overwrite an existing probe result")
    laws = fixed_laws()
    cases = [law_diagnostic(law) for law in laws]
    profiles = []
    for rho in TARGET_RHOS:
        rows = [{"t": t, **caps(rho, t)} for t in FREQUENCIES]
        differences = [row["new_crude_bessel"] - row["existing_cosine_cubic"] for row in rows]
        require(min(differences) >= -NUMERIC_TOLERANCE, "Regression of exact crude-cap domination")
        profiles.append({"rho": rho, "rows": rows,
                         "minimum_new_minus_existing_cosine": min(differences),
                         "maximum_new_minus_existing_cosine": max(differences),
                         "new_improves_existing_cosine_any_sample": any(value < -NUMERIC_TOLERANCE for value in differences),
                         "new_improves_trivial_any_sample": any(row["new_crude_bessel"] < 1 - NUMERIC_TOLERANCE for row in rows),
                         "new_improves_taylor_any_sample": any(row["new_crude_bessel"] < row["taylor_triangle"] - NUMERIC_TOLERANCE for row in rows)})
    guard()
    result = {
        "status": "FLOATING_DIAGNOSTIC_ONLY_NO_CDF_CERTIFICATE",
        "source": SOURCE, "executed_once_by_this_script": True,
        "date": "2026-10-08", "law_count": len(laws), "frequency_count": len(FREQUENCIES),
        "frequencies": list(FREQUENCIES), "numpy_available": np is not None,
        "numpy_version": np.__version__ if np is not None else None,
        "exact_algebra_separate_from_numeric_results": EXACT_ALGEBRA,
        "cases": cases, "target_rho_cap_profiles": profiles,
        "resources": {"elapsed_seconds": time.monotonic() - STARTED,
                      "time_budget_seconds": TIME_BUDGET_SECONDS,
                      "peak_working_set_bytes_observed": peak_working_set_bytes(),
                      "peak_working_set_budget_bytes": PEAK_MEMORY_BUDGET_BYTES,
                      "cooperative_budget_not_OS_limit": True,
                      "maximum_laws": 32, "maximum_frequencies": 32, "maximum_atoms": 4,
                      "maximum_matrix_dimension": 34, "BLAS_threads_requested": 1,
                      "retained_numeric_data_budget_bytes": 2 * 1024 * 1024,
                      "output_budget_bytes": OUTPUT_BUDGET_BYTES},
        "conclusions": {
            "all_sample_augmented_and_binary_ledger_regressions_passed": True,
            "binary_diagonal_and_multifrequency_residuals_zero_within_tolerance": True,
            "crude_new_cap_improves_existing_cosine_cubic": False,
            "weighted_gram_is_redundant": True,
            "potential_new_information": "The augmented multi-frequency Schur residual and binary-defect ledger couple phi and psi across frequencies; this probe does not optimize those constraints.",
            "CDF_target_proved_or_tested": False,
            "numerical_results_certified": False,
            "finite_M4_used": False,
        },
    }
    serialized = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    require(len(serialized.encode("utf-8")) <= OUTPUT_BUDGET_BYTES, "JSON output budget")
    guard()
    output_path.write_text(serialized, encoding="utf-8")
    print(json.dumps({"status": result["status"], "result": str(output_path),
                      "laws": len(laws), "frequencies": len(FREQUENCIES),
                      "numpy_available": np is not None,
                      "elapsed_seconds": result["resources"]["elapsed_seconds"],
                      "peak_working_set_bytes": result["resources"]["peak_working_set_bytes_observed"],
                      "max_ledger_identity_error": max(case["binary_ledger_max_abs_identity_error"] for case in cases),
                      "max_ledger_upper_excess": max(case["binary_ledger_max_upper_excess"] for case in cases),
                      "minimum_sample_R": min(case["minimum_R"] for case in cases),
                      "new_cap_improves_existing_cosine": False}, sort_keys=True))


if __name__ == "__main__":
    main()
