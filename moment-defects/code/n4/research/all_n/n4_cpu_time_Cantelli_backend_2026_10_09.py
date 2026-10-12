"""NEW CPU-budget Cantelli timed API; unchanged frozen d7d576 mathematics.

Only the timed producer API body is copied. All arithmetic below is the
same five-count whole-law/CLOSED-p/H construction, Gaussian integer
helpers, mean/variance/Bernstein bounds, reflection/zero-atom conventions,
exact scale, grids and 64MiB limit. The only resource change is a
60-second PROCESS_CPU_USER_PLUS_SYSTEM budget instead of elapsed wall
time. process_time excludes host sleep, descheduling and blocking IO;
no hard wall deadline or power-policy change is introduced. monotonic
is used ONLY for nondeterministic wall diagnostics under resources.

Frozen old backend is imported ONLY for PURE math/constants. Its old
timed producer/CLI is never called, rebound or monkeypatched. No saved
numeric receipt, CPU flag, type/status/hash establishes the fresh math
precondition. Runtime/scope/resource failure raises, never a prefix
certificate. All scalar CDF/physical premises remain exactly the old
backend; this wrapper alone proves neither an entire root nor C4.

No producer CLI/import-time job/file write. Dormant PURE checks only.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_conditional_sign_count_cantelli_exact_box_2026_10_09 as previous

integer, gaussian, gaussian_helpers = previous.integer, previous.gaussian, previous.gaussian_helpers
resources, require = previous.resources, previous.require
SCALE, TARGET, H_LO, H_HI = previous.SCALE, previous.TARGET, previous.H_LO, previous.H_HI
TIME_LIMIT, MEMORY_LIMIT = previous.TIME_LIMIT, previous.MEMORY_LIMIT
CLOCK_KIND = "PROCESS_CPU_USER_PLUS_SYSTEM"
PREVIOUS_PIN = "d7d57607763c854f990aa5ff169930e1c227749309263f9f77c1b072d7d2f0ab"

# Explicit PURE aliases only. No old timed producer is forwarded.
checked_request = previous.checked_request
minmax_beta_square = previous.minmax_beta_square
necessary_outer_cuts = previous.necessary_outer_cuts
local_geometry = previous.local_geometry
count_variance_uppers = previous.count_variance_uppers
count_mean_lowers_scaled = previous.count_mean_lowers_scaled
mixed_binomial_probabilities = previous.mixed_binomial_probabilities
mixed_probabilities_upper_scaled = previous.mixed_probabilities_upper_scaled
count_cantelli_uppers_scaled = previous.count_cantelli_uppers_scaled
joint_binomial_cdf_upper_scaled = previous.joint_binomial_cdf_upper_scaled


def source_drift_check():
    require(hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == PREVIOUS_PIN,
            "Frozen old PURE math integrity only")
    require(TIME_LIMIT == 60 and MEMORY_LIMIT == 64 * 1024 * 1024 and SCALE == 10 ** 40,
            "Unchanged CPU cap, memory and exact arithmetic scale")


def dependency_pins():
    files = (Path(__file__), Path(previous.__file__), Path(gaussian_helpers.__file__),
             Path(gaussian.__file__), Path(integer.__file__), Path(resources.__file__))
    require(len({p.name for p in files}) == len(files), "Unique complete CPU backend source closure")
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def compute_verified_conditional_cantelli_box(rectangle, eta_lower, Np=128, NH=1024,
                                             time_limit_seconds=TIME_LIMIT):
    """Fresh exact whole-law/w/beta/actualp/H bound with eta>=LOWER."""
    started_cpu, started_wall = time.process_time(), time.monotonic()
    source_drift_check()
    initial_pins = dependency_pins()
    rectangle = checked_request(rectangle, eta_lower, Np, NH, time_limit_seconds)
    wl, wh, bl, bh = rectangle
    def guard():
        require(time.process_time() - started_cpu < time_limit_seconds, "Exact conditional Cantelli PROCESS_CPU budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Exact conditional Cantelli64MiB working set")
    pi, phi0 = gaussian.pi_and_phi0()
    H_faces = tuple(H_LO + (H_HI - H_LO) * F(j, NH) for j in range(NH + 1))
    H_scaled = []
    for H in H_faces:
        value = H * SCALE
        require(value.denominator == 1, "H faces exactly represented at integer scale")
        H_scaled.append(value.numerator)
    Phi_lowers = []
    for H in H_scaled:
        guard()
        Phi_lowers.append(gaussian_helpers.fast_normal_cdf_interval(H, phi0)[0])
    require(5 * Phi_lowers[-1] > 4 * SCALE, "Fresh Gaussian positive-tail Phi(25/16)>.8")
    global_cuts = {"empty": False, "w_interval": (wl, wh), "beta_interval": (bl, bh)}
    global_rho_lower = local_geometry(global_cuts, eta_lower)["actual_rho_lower"]
    tail_score = F(2, 5) / global_rho_lower
    rows, empties, H_checks = [], [], 0
    for orientation, beta_range in ((1, (bl, bh)), (-1, (-bh, -bl))):
        blo, bhi = beta_range
        pLo, pHi = wl * (1 - bhi) / 2, 1 - wl * (1 + blo) / 2
        require(0 < pLo <= pHi < 1, "Closed necessary ACTUAL p interval, each reflected law separately")
        p_faces = tuple(pLo + (pHi - pLo) * F(j, Np) for j in range(Np + 1))
        for p_index, (pL, pU) in enumerate(zip(p_faces, p_faces[1:])):
            guard()
            cuts = necessary_outer_cuts(wl, wh, blo, bhi, pL, pU)
            if cuts["empty"]:
                empties.append({"orientation": orientation, "p_index": p_index,
                    "lower": pL, "upper": pU, "reason": cuts["reason"]})
                continue
            local = local_geometry(cuts, eta_lower)
            variances = count_variance_uppers(cuts, pL, pU)
            if variances is None:
                empties.append({"orientation": orientation, "p_index": p_index,
                    "lower": pL, "upper": pU, "reason": "proven_negative_upper_on_nonnegative_conditional_variance"})
                continue
            means = count_mean_lowers_scaled(local["u_bracket"], pU)
            probability_uppers = mixed_probabilities_upper_scaled(mixed_binomial_probabilities(pL, pU))
            raw_max, worst_H = 0, 0
            for h in range(NH):
                if h % 64 == 0:
                    guard()
                Aj = count_cantelli_uppers_scaled(H_scaled[h + 1], means, variances)
                upper_cdf = joint_binomial_cdf_upper_scaled(Aj, probability_uppers)
                raw = 2 * (upper_cdf - Phi_lowers[h])
                if raw > raw_max:
                    raw_max, worst_H = raw, h
                H_checks += 1
            score = F(raw_max, SCALE) / local["actual_rho_lower"]
            rows.append({"orientation": orientation, "p_index": p_index,
                "lower": pL, "upper": pU, "raw_upper_int": raw_max,
                "score_upper": score, "worst_H_index": worst_H,
                "worst_H_closed_cell": (H_faces[worst_H], H_faces[worst_H + 1]),
                "necessary_outer_w_interval": cuts["w_interval"],
                "necessary_outer_signed_beta_interval": cuts["beta_interval"],
                "actual_rho_lower": local["actual_rho_lower"],
                "H_closed_cells_checked": NH})
    require(len(rows) + len(empties) == 2 * Np and H_checks == len(rows) * NH,
            "Complete two-signed-beta/p/H cover, empty cells have explicit necessary proof")
    upper = max([tail_score] + [row["score_upper"] for row in rows])
    passed = upper < TARGET
    guard()
    source_drift_check()
    require(dependency_pins() == initial_pins, "SAME frozen arithmetic through complete CPU backend")
    guard()
    return {"status": "EXACT_CONDITIONAL_FIVE_COUNT_CANTELLI_BOX_CDF_BOUND" if passed else "UNKNOWN",
        "date": "2026-10-09", "scale": SCALE, "target": TARGET,
        "closed_rectangle": rectangle, "eta_lower": eta_lower, "Np": Np, "NH": NH,
        "closed_H_domain": (H_LO, H_HI), "p_cells": rows, "proved_empty_p_cells": empties,
        "tail_score_upper": tail_score, "global_actual_rho_lower": global_rho_lower,
        "upper_exact": upper, "upper_decimal_diagnostic": float(upper), "strict_margin_exact": TARGET - upper,
        "fresh_Gaussian": {"pi": pi, "phi0": phi0, "Phi_25_16_lower_int": Phi_lowers[-1]},
        "metadata": {"H_cells_checked": H_checks, "p_cells_total_including_empty": 2 * Np,
            "actual_p_zero_convention": "P(X>=0), includingzero; reflectedlaw is recomputed with signedbetaflip and its OWNactualp",
            "no_false_complement_for_zero_atom": True,
            "necessary_Cauchy_outer_cuts": True, "corners_assumed_feasible": False,
            "normalization": "Perp-cell fresh rhoQ3(wEffHI,minabsbetaEff)LOW+actual etaLOW",
            "variance": "wLO; SAME beta endpoint for paired sign maxima, maxbetaendpoints byconvexity",
            "probabilities": "Exact25mixedBernoulli coefficients positiveSCALEceil, max5degree4Bernstein expectations; NO independent binmassmax",
            "CDF_cells": "AjUP(Hupper,muLOW,VUP)−PhiLOW(Hlower); monotonic endpoints, no interpolationreserve",
            "tails": "H<=−2 Cantelli raw<=2/5;H>=25/16 freshPhi>.8 givesraw<2/5",
            "atom_safe_reflection": "Phi(H)−F_Z(H)<=F_−Z(−H)−Phi(−H)",
            "saved_numeric_or_float_bounds_used": False},
        "premises": "Arbitrary standardized iid P with canonical w,|beta| in the declared CLOSED rectangle and actual rho−rhoQ3>=eta_lower. No support, density, finite-atom count or M4 requirement. This is a sufficient CDF majorant; UNKNOWN is not a counterexample.",
        "source_pins_integrity_only": initial_pins,
        "conclusions": {"conditional_all_law_all_actual_p_all_H_CDF_bound": passed,
            "entire_global_root_or_C4_proved": False, "old_sources_or_receipts_modified": False},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started_wall,
            "wall_elapsed_seconds_diagnostic": time.monotonic() - started_wall,
            "cpu_elapsed_seconds_diagnostic": time.process_time() - started_cpu,
            "clock_kind": CLOCK_KIND, "hard_wall_deadline_imposed": False,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "Prawitz_Fourier_or_binary_producer_called": False}}


def self_tests():
    """Dormant PURE scalar/alias checks; no backend/CF/ROOT producer."""
    source_drift_check()
    require(TIME_LIMIT == 60 and MEMORY_LIMIT == 64 * 1024 * 1024, "SAME resource caps")
    require(minmax_beta_square(F(-1, 4), F(1, 2)) == (F(0), F(1, 4)), "Unchanged exact PURE beta range")
    require(checked_request is previous.checked_request and count_variance_uppers is previous.count_variance_uppers,
            "PURE aliases retain exact frozen arithmetic")
    return {"exact_checks": 3, "clock_kind": CLOCK_KIND, "hard_wall_deadline_imposed": False,
            "producer_called_or_files_written": False, "unrestricted_C4_proved": False}

