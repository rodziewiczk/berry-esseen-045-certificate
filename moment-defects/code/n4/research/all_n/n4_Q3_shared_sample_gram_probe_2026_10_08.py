"""Tiny floating Q3 shared-sample Fourier-residual diagnostic; not a proof.

Reuse only the previous probe's fixed-law generator and transforms. Add one
specified genuinely three-point Q3 law. No CDF or optimization module is used,
and no M4 is assumed/calculated. All matrices use the same finite sample law;
there is no inverse, pseudoinverse or ill-conditioned covariance division.

Bounds: <=32 laws, <=32 frequencies, <=4 atoms, matrices <=32x32, one BLAS
thread, JSON <=96 KiB, cooperative elapsed budget 30 s and Windows peak working
set budget 256 MiB checked after each law. The fixed finite dimensions bound
retained numeric arrays to well below 2 MiB; NumPy library memory is separate.
The output filename must not exist; no previous result is overwritten.
"""

from __future__ import annotations

import cmath
import ctypes
import json
import math
import os
from pathlib import Path
import time

for _thread_variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                         "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_thread_variable] = "1"

STARTED = time.monotonic()
import n4_shared_sample_gram_probe_2026_10_08 as fixed
try:
    import numpy as np
except ImportError:
    np = None

SOURCE = "n4_Q3_shared_sample_gram_probe_2026_10_08.py"
RESULT = "n4_Q3_shared_sample_gram_probe_2026_10_08.json"
FREQUENCIES = tuple(sorted({j / 8 for j in range(25)} | {math.pi / 2}))
TOLERANCE = 2e-10
TIME_BUDGET = 30.0
MEMORY_BUDGET = 256 * 1024 * 1024
OUTPUT_BUDGET = 96 * 1024

EXACT_ALGEBRA = {
    "hypotheses": "EX=0, EX^2=1, rho=E|X|^3<infinity; X+=max(X,0), X-=max(-X,0).",
    "reference": "u=EX+=EX->0; v+=EX+^2, v-=EX-^2; a=v-/u,b=v+/u. Q3 masses u/a at -a, u/b at b, 1-u/a-u/b at 0; v++v-=1.",
    "shared_moments": "P and Q3 share EX+,EX-,EX+^2,EX-^2; hence share Eg and E[gg*] for g=(1,X+,X-).",
    "defect": "rho_Q3=(v+^2+v-^2)/u; eta=rho-rho_Q3=E W(X); W(x)=x+*(x-b)^2+x-*(x+a)^2>=0.",
    "interpolant": "L_t(x)=1+c+(t)*x+ +c-(t)*x-; c+=(exp(i*t*b)-1)/b, c-=(exp(-i*t*a)-1)/a; h_t=exp(i*t*x)-L_t(x).",
    "zero_branch": "W(x)=0 implies x in {-a,0,b}, so h_t(x)=0 for every t; no division by W on this branch.",
    "matrix_orientation": "K_jk=E[exp(i*t_j*X)*conj(exp(i*t_k*X))]=phi(t_j-t_k); C_jr=E[exp(i*t_j*X)*g_r(X)]; c_j=(1,c+(t_j),c-(t_j)).",
    "B3": "[[1,u,u],[u,v+,0],[u,0,v-]]",
    "matrix_identity": "E[hh-adjoint]=K-C c-adjoint-c C-adjoint+c B3 c-adjoint, with ordinary matrix products.",
    "matrix_identity_unambiguous": "H=K-C@c.conj().T-c@C.conj().T+c@B3@c.conj().T",
    "pointwise_estimate_supplied_for_regression": "|h_t(x)|^2<=|t|^3*W(x), giving E|h_t(X)|^2<=eta*|t|^3.",
    "common_measure": "Set z_j(x)=h_tj(x)/sqrt(W(x)) when W(x)>0 and 0 otherwise. Then E[hh*]=E[W zz*]. If eta>0 this is eta times E_nu[zz*], dnu=W dP/eta, with every frequency using the SAME nu.",
    "cross_response": "E[h_tj*conj(h_tk)]=E[W*z_j*conj(z_k)]; therefore |entry_jk|<=eta*|t_j*t_k|^(3/2). The exact common-measure matrix retains more information than independent entrywise bounds.",
    "eta_zero": "eta=0 forces support in {-a,0,b}, so P=Q3 and every residual is zero. Q3 may have a positive zero atom; eta=0 does not force a two-point law.",
    "proof_scope": "These algebraic statements are retained separately from floating arithmetic. The numerical checks do not certify their all-law validity or a Berry-Esseen/CDF bound.",
    "M4_used": False, "matrix_inverse_used": False,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def peak_bytes():
    if os.name != "nt":
        return None

    class Counters(ctypes.Structure):
        _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in (
                "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage",
                "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), ctypes.c_ulong]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    return int(counters.PeakWorkingSetSize) if psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb) else None


def guard():
    require(time.monotonic() - STARTED < TIME_BUDGET, "Q3 elapsed-time budget")
    peak = peak_bytes()
    require(peak is None or peak <= MEMORY_BUDGET, "Q3 peak-working-set budget")


def csum(values):
    values = tuple(values)
    return complex(math.fsum(z.real for z in values), math.fsum(z.imag for z in values))


def sign_moments(points, probabilities):
    pairs = tuple(zip(probabilities, points))
    return {
        "u_plus": math.fsum(p * max(x, 0) for p, x in pairs),
        "u_minus": math.fsum(p * max(-x, 0) for p, x in pairs),
        "v_plus": math.fsum(p * max(x, 0) ** 2 for p, x in pairs),
        "v_minus": math.fsum(p * max(-x, 0) ** 2 for p, x in pairs),
        "rho": math.fsum(p * abs(x) ** 3 for p, x in pairs),
    }


def probe(law):
    guard()
    points, probabilities = law["points"], law["probabilities"]
    moments = sign_moments(points, probabilities)
    u = (moments["u_plus"] + moments["u_minus"]) / 2
    vp, vm, rho = moments["v_plus"], moments["v_minus"], moments["rho"]
    require(u > 0 and abs(moments["u_plus"] - moments["u_minus"]) < TOLERANCE, "Positive matching sign first moments")
    require(abs(vp + vm - 1) < TOLERANCE, "Standardized second moment")
    a, b = vm / u, vp / u
    qminus, qplus = u / a, u / b
    qzero_raw = 1 - qminus - qplus
    require(qzero_raw >= -TOLERANCE, "Numerical Q3 nonnegative zero mass")
    qprobabilities = (qminus, max(0.0, qzero_raw), qplus)
    qmass = math.fsum(qprobabilities)
    qprobabilities = tuple(p / qmass for p in qprobabilities)
    qpoints = (-a, 0.0, b)
    qmoments = sign_moments(qpoints, qprobabilities)
    shared_error = max(abs(moments[key] - qmoments[key]) for key in ("u_plus", "u_minus", "v_plus", "v_minus"))
    require(shared_error < TOLERANCE, "P/Q3 shared sign M1 and M2 regression")
    rho_q = (vp * vp + vm * vm) / u
    eta = rho - rho_q
    weights_w = tuple(max(x, 0) * (x - b) ** 2 + max(-x, 0) * (x + a) ** 2 for x in points)
    ew = math.fsum(p * w for p, w in zip(probabilities, weights_w))
    require(abs(eta - ew) < TOLERANCE * max(1, rho), "eta=EW identity regression")
    require(eta >= -TOLERANCE * max(1, rho), "Nonnegative eta regression")
    coefficient_rows, hrows, zrows, erows, crossrows = [], [], [], [], []
    diagrows, pointwise_excesses = [], []
    zero_w_count = sum(w == 0 for w in weights_w)
    for t in FREQUENCIES:
        cp = (cmath.exp(1j * t * b) - 1) / b
        cm = (cmath.exp(-1j * t * a) - 1) / a
        coefficient_rows.append((1 + 0j, cp, cm))
        erow = tuple(cmath.exp(1j * t * x) for x in points)
        hrow = tuple(e - 1 - cp * max(x, 0) - cm * max(-x, 0) for e, x in zip(erow, points))
        zrow = []
        for h, w in zip(hrow, weights_w):
            if w == 0:
                require(abs(h) < TOLERANCE, "W=0 has h=0 within floating tolerance")
                zrow.append(0j)
            else:
                zrow.append(h / math.sqrt(w))
            pointwise_excesses.append(abs(h) ** 2 - abs(t) ** 3 * w)
        erows.append(erow)
        hrows.append(hrow)
        zrows.append(tuple(zrow))
        phi = fixed.transforms(law, t)[0]
        crossrows.append((phi,
                          csum(p * e * max(x, 0) for p, e, x in zip(probabilities, erow, points)),
                          csum(p * e * max(-x, 0) for p, e, x in zip(probabilities, erow, points))))
        direct = math.fsum(p * abs(h) ** 2 for p, h in zip(probabilities, hrow))
        upper = max(0.0, eta) * abs(t) ** 3
        diagrows.append({"t": t, "residual_squared_expectation": direct,
                         "eta_times_abs_t_cubed": upper, "upper_excess": direct - upper,
                         "ratio_if_positive_upper": direct / upper if upper > 1e-14 else None})
    require(max(row["upper_excess"] for row in diagrows) <= TOLERANCE * max(1, rho), "Q3 diagonal eta|t|^3 regression")
    require(max(pointwise_excesses) <= TOLERANCE * max(1, rho), "Q3 pointwise |h|^2 <= |t|^3 W regression")
    matrices = {"available": False, "reason": "NumPy unavailable"}
    if np is not None:
        p = np.array(probabilities, dtype=float)
        h = np.array(hrows, dtype=np.complex128)
        z = np.array(zrows, dtype=np.complex128)
        c = np.array(coefficient_rows, dtype=np.complex128)
        C = np.array(crossrows, dtype=np.complex128)
        B3 = np.array(((1, u, u), (u, vp, 0), (u, 0, vm)), dtype=float)
        K = np.array([[fixed.transforms(law, tj - tk)[0] for tk in FREQUENCIES] for tj in FREQUENCIES], dtype=np.complex128)
        direct_matrix = (h * p) @ h.conjugate().T
        expansion = K - C @ c.conjugate().T - c @ C.conjugate().T + c @ B3 @ c.conjugate().T
        common_measure = (z * (p * np.array(weights_w))) @ z.conjugate().T
        identity_error = float(np.max(np.abs(direct_matrix - expansion)))
        common_error = float(np.max(np.abs(direct_matrix - common_measure)))
        eigs = np.linalg.eigvalsh((direct_matrix + direct_matrix.conjugate().T) / 2)
        expansion_eigs = np.linalg.eigvalsh((expansion + expansion.conjugate().T) / 2)
        require(identity_error < TOLERANCE * max(1, rho), "Common-sample Q3 residual matrix expansion")
        require(common_error < TOLERANCE * max(1, rho), "Common-measure cross-response matrix identity")
        require(float(eigs.min()) >= -TOLERANCE and float(expansion_eigs.min()) >= -TOLERANCE, "Floating residual matrix PSD")
        cross_cap = np.array([[max(0.0, eta) * abs(tj * tk) ** 1.5 for tk in FREQUENCIES] for tj in FREQUENCIES])
        cross_excess = float(np.max(np.abs(direct_matrix) - cross_cap))
        require(cross_excess <= TOLERANCE * max(1, rho), "Shared-measure cross-response entry bound")
        matrices = {"available": True, "dimension": len(FREQUENCIES),
                    "matrix_expansion_max_abs_error": identity_error,
                    "common_measure_max_abs_error": common_error,
                    "minimum_direct_residual_eigenvalue": float(eigs.min()),
                    "minimum_expansion_eigenvalue": float(expansion_eigs.min()),
                    "residual_rank_at_numeric_tolerance": int((eigs > TOLERANCE).sum()),
                    "residual_max_abs_entry": float(np.max(np.abs(direct_matrix))),
                    "maximum_cross_entry_upper_excess": cross_excess,
                    "no_matrix_inverse_or_pseudoinverse": True}
    eta_numerically_zero = abs(eta) < TOLERANCE * max(1, rho)
    if eta_numerically_zero:
        require(max(row["residual_squared_expectation"] for row in diagrows) < TOLERANCE, "eta=0 models have zero residual within tolerance")
    guard()
    ratios = [row["ratio_if_positive_upper"] for row in diagrows if row["ratio_if_positive_upper"] is not None]
    return {"label": law["label"], "P": {"points": list(points), "probabilities": list(probabilities), **moments},
            "Q3": {"points": list(qpoints), "probabilities": list(qprobabilities),
                   "zero_mass_before_roundoff_clamp": qzero_raw, "a": a, "b": b, **qmoments},
            "shared_sign_moment_max_abs_error": shared_error,
            "rho_Q3_formula": rho_q, "eta_raw": eta, "EW_direct": ew,
            "eta_numerically_zero": eta_numerically_zero,
            "eta_zero_but_positive_zero_atom": eta_numerically_zero and qprobabilities[1] > TOLERANCE,
            "literal_zero_W_atom_count": zero_w_count,
            "maximum_diagonal_upper_excess": max(row["upper_excess"] for row in diagrows),
            "maximum_pointwise_upper_excess": max(pointwise_excesses),
            "maximum_diagonal_ratio_if_positive_upper": max(ratios) if ratios else None,
            "selected_diagonal_rows": [row for row in diagrows if row["t"] in (0, .5, 1, 1.5, math.pi / 2, 2, 2.5, 3)],
            "matrices": matrices, "numeric_not_certified": True}


def main():
    output = Path(__file__).with_name(RESULT)
    require(not output.exists(), "Refuse to overwrite an existing Q3 result")
    laws = fixed.fixed_laws()
    root3 = math.sqrt(3)
    laws.append({"label": "genuine_Q3_exact_rational_raw_law",
                 "points": (-2 / root3, 0.0, 3 / root3), "probabilities": (.3, .5, .2), "binary": False})
    require(len(laws) <= 32 and len(FREQUENCIES) <= 32, "Fixed finite probe cardinality bounds")
    cases = [probe(law) for law in laws]
    result = {"status": "FLOATING_Q3_SHARED_SAMPLE_DIAGNOSTIC_ONLY",
              "date": "2026-10-08", "source": SOURCE,
              "reused_source": fixed.SOURCE, "law_count": len(laws), "frequency_count": len(FREQUENCIES),
              "frequencies": list(FREQUENCIES), "numpy_available": np is not None,
              "numpy_version": np.__version__ if np is not None else None,
              "exact_algebra_separate_from_floating_regressions": EXACT_ALGEBRA,
              "added_Q3_definition": "Raw nodes (-2,0,3), probabilities (3/10,1/2,1/5), divided by sqrt(3); genuinely three-point with eta=0 in exact arithmetic.",
              "cases": cases,
              "resources": {"elapsed_seconds": time.monotonic() - STARTED,
                            "time_budget_seconds": TIME_BUDGET, "peak_working_set_bytes_observed": peak_bytes(),
                            "memory_budget_bytes": MEMORY_BUDGET, "cooperative_not_OS_limit": True,
                            "BLAS_threads_requested": 1, "output_budget_bytes": OUTPUT_BUDGET,
                            "maximum_laws": 32, "maximum_frequencies": 32, "maximum_atoms": 4},
              "conclusions": {"all_floating_regressions_passed": True,
                              "eta_zero_models_include_genuine_three_point_laws": True,
                              "common_measure_cross_responses_checked": np is not None,
                              "M4_used": False, "matrix_inverse_used": False,
                              "numerical_certification": False, "CDF_target_tested_or_proved": False}}
    raw = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_BUDGET, "Q3 output size budget")
    guard()
    output.write_text(raw, encoding="utf-8")
    print(json.dumps({"status": result["status"], "result": str(output),
                      "laws": len(laws), "frequencies": len(FREQUENCIES),
                      "elapsed_seconds": result["resources"]["elapsed_seconds"],
                      "peak_working_set_bytes": result["resources"]["peak_working_set_bytes_observed"],
                      "max_shared_sign_moment_error": max(case["shared_sign_moment_max_abs_error"] for case in cases),
                      "max_diagonal_upper_excess": max(case["maximum_diagonal_upper_excess"] for case in cases),
                      "genuine_three_point_eta_zero_count": sum(case["eta_zero_but_positive_zero_atom"] for case in cases)}, sort_keys=True))


if __name__ == "__main__":
    main()
