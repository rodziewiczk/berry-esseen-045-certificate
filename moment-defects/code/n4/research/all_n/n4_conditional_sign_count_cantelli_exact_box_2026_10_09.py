"""Fresh EXACT all-p/all-H five-count Cantelli on CLOSED moment boxes.

API compute_verified_conditional_cantelli_box(rectangle,eta_lower,Np=128,
NH=1024,time_limit_seconds=60) takes four Fraction endpoints
(wLO,wHI,betaAbsLO,betaAbsHI) and a Fraction eta_lower>=0. It proves an
all-law n4 CDF bound only if every exact cell passes. Standardized iid P
has u=EX+=EX-,v+=(1+beta)/2,v-=(1-beta)/2,w=4u^2/(1-beta^2), and
actualrho=rhoQ3+eta with eta>=eta_lower. No support/finite-atom assumption,
M4, imported binary/three-point axiom or saved numeric table is used.

ACTUAL p=P(X>=0) includes zero. p in[w(1-beta)/2,1-w(1+beta)/2].
Conditional Z=sum4X/2 on J positive signs has exact
 mu_j=u(j-4p)/(2pq),
 V_j=[j(v+/p-u^2/p^2)+(4-j)(v-/q-u^2/q^2)]/4.
Cantelli gives CLOSED upper Aj=1 ifH>=mu_j, otherwise
V_j/(V_j+(mu_j-H)^2), including deterministic V=0 and atom equality.

Each CLOSED p-cell retains necessary parameter dependence:
 betaEffLO=max(betaLO,1-2pU/wLO),
 betaEffHI=min(betaHI,2(1-pL)/wLO-1),
 wEffHI=min(wHI,2pU/(1-betaEffHI),2(1-pL)/(1+betaEffLO)).
These are OUTER NECESSARY Cauchy--Schwarz restrictions for every actual
law, not feasibility assertions about corners. Strictly reversed ranges
prove emptiness; equality/shared faces are retained. Fresh local rhoQ3LO
from wEffHI/minabsbetaEff pluseta_lower retains denominator correlation.

mu_j decreases in ACTUAL p for fixedu on all0<p<1; its derivative is
-u[j(1-2p)+4p^2]/(2p^2q^2). Fresh sign-aware u-root endpoints give its
whole-cell LOWER. V_j decreases in w; for fixedp,w it is convex in beta,
so beta endpoint maxima suffice. Each sign variance (v*r-u^2)/r^2 has
its maximum at clamp(2u^2/v) on the sign-mass interval. Taking those two
maxima at the SAME beta endpoint gives a conservative V_j upper; we do
not combine positive/negative maxima from different beta endpoints.

On CLOSED H-cell[HL,HU], each Aj upper uses HU,muLO,VUP. With those
FIVE constant Aj bounds, Binomial4 probabilities are retained JOINTLY.
Degree4 Bernstein coefficients are E Aj(K) for K=sum ofrBernoulli(pU)
and4-rBernoulli(pL),r0..4. Exact25 mixed probabilities, converted outward
to positive SCALE integers once/p-cell, bound ALLp by max5 expectations.
No assumption that Aj is monotone in j, no independent mass maxima.
Subtract fresh PhiLO(HL); monotonic CDF/Phi covers every threshold without
an interpolation reserve. TailH<=-2 has raw<=.4 by global Cantelli;
H>=25/16 has raw<.4 from fresh PhiLO(25/16)>.8. All shared faces included.

BOTH signed beta boxes are independently covered with actual P(X>=0).
For reflection we NEVER assert P(-X>=0)=1-P(X>=0) when zero has mass.
Upper-CDF bounds for P and -P imply both discrepancies by the atom-safe
inequality Phi(H)-F_Z(H)<=F_(-Z)(-H)-Phi(-H). No CDF density assumed.

Fraction/int atS1e40; Gaussian PURE integer60 recurrence from the audited
binary source, but NO binary certificate theorem/producer is imported.
Static monitor60s/64MiB. CLI defaults to synthetic/helper tests only;
explicit --produce writes a NEW exclusive<=1MiB receipt for the named
default rectangle, and --replay-existing recomputes read-only. Full
producer permission/source audits are coordinated outside.
No old source/receipt edit, no unrestricted C4/root closure claimed.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import comb
from itertools import product
from pathlib import Path
import time

import n4_binary_band_exact_certificate_2026_10_09 as gaussian_helpers
import n4_windows_resource_guard_2026_10_09 as resources

integer, gaussian, SCALE = gaussian_helpers.integer, gaussian_helpers.gaussian, gaussian_helpers.SCALE
TARGET, H_LO, H_HI = F(256, 625), F(-2), F(25, 16)
TIME_LIMIT, MEMORY_LIMIT = 60, 64 * 1024 * 1024
OUTPUT_LIMIT = 1024 * 1024
DEFAULT_RECTANGLE = (F(9, 10), F(19, 20), F(7, 20), F(9, 20))
DEFAULT_ETA_LOWER, DEFAULT_NP, DEFAULT_NH = F(1, 4), 128, 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def checked_request(rectangle, eta_lower, Np, NH, time_limit_seconds):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is F for value in rectangle), "Four Fraction moment-box endpoints")
    wl, wh, bl, bh = rectangle
    require(0 < wl <= wh <= 1 and 0 <= bl <= bh < 1, "Valid CLOSED w/beta-magnitude box")
    require(type(eta_lower) is F and eta_lower >= 0, "Exact actual eta LOWER, not dropped moment")
    require(type(Np) is int and Np in (16, 32, 64, 128, 256, 512)
            and type(NH) is int and NH in (64, 128, 256, 512, 1024), "Declared bounded dyadic p/H grids")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic<=60s timer only; no floating proof values")
    return tuple(rectangle)


def minmax_beta_square(beta_lo, beta_hi):
    require(type(beta_lo) is F and type(beta_hi) is F and -1 < beta_lo <= beta_hi < 1,
            "Exact ordered signed beta interval")
    low = F(0) if beta_lo <= 0 <= beta_hi else min(beta_lo ** 2, beta_hi ** 2)
    return low, max(beta_lo ** 2, beta_hi ** 2)


def necessary_outer_cuts(wl, wh, beta_lo, beta_hi, pL, pU):
    require(0 < pL <= pU < 1, "Closed actual sign-mass cell")
    blo = max(beta_lo, 1 - 2 * pU / wl)
    bhi = min(beta_hi, 2 * (1 - pL) / wl - 1)
    if blo > bhi:
        return {"empty": True, "reason": "strictly_reversed_necessary_beta_interval"}
    wup = min(wh, 2 * pU / (1 - bhi), 2 * (1 - pL) / (1 + blo))
    if wup < wl:
        return {"empty": True, "reason": "necessary_w_upper_strictly_below_w_lower"}
    return {"empty": False, "w_interval": (wl, wup), "beta_interval": (blo, bhi),
            "cuts_are_necessary_outer_not_corner_feasibility": True}


def local_geometry(cuts, eta_lower):
    require(not cuts["empty"], "Nonempty necessary outer cell")
    wl, wh = cuts["w_interval"]
    blo, bhi = cuts["beta_interval"]
    low_beta2, high_beta2 = minmax_beta_square(blo, bhi)
    ulo = integer.sqrt_fraction_interval(wl * (1 - high_beta2) / 4)[0]
    uhi = integer.sqrt_fraction_interval(wh * (1 - low_beta2) / 4)[1]
    require(0 < ulo <= uhi, "Fresh positive u root intervals at approved scale")
    rho_square = (1 + low_beta2) ** 2 / (wh * (1 - low_beta2))
    rho_lo = max(F(1), F(integer.sqrt_fraction_interval(rho_square)[0], SCALE))
    return {"u_bracket": (ulo, uhi), "rhoQ_lower": rho_lo,
            "actual_rho_lower": rho_lo + eta_lower, "rhoQ_min_square": rho_square}


def sign_variance_maximum(v, u2, rL, rU):
    require(v > 0 and u2 > 0 and 0 < rL <= rU < 1, "Positive exact sign-moment interval")
    r = min(rU, max(rL, 2 * u2 / v))
    return v / r - u2 / r ** 2


def count_variance_uppers(cuts, pL, pU):
    wl, wh = cuts["w_interval"]
    blo, bhi = cuts["beta_interval"]
    beta_rows = []
    for beta in (blo, bhi):
        vp, vm, u2 = (1 + beta) / 2, (1 - beta) / 2, wl * (1 - beta ** 2) / 4
        pos = sign_variance_maximum(vp, u2, pL, pU)
        neg = sign_variance_maximum(vm, u2, 1 - pU, 1 - pL)
        beta_rows.append(tuple((j * pos + (4 - j) * neg) / 4 for j in range(5)))
    upper = tuple(max(row[j] for row in beta_rows) for j in range(5))
    # A negative proven upper on actual V_j>=0 would prove this moment cell
    # empty. Do not silently assume a fake corner is feasible or clip it.
    if any(value < 0 for value in upper):
        return None
    return tuple(integer.ceil_fraction_scaled(value) for value in upper)


def count_mean_lowers_scaled(u_bracket, pU):
    require(0 < pU < 1 and 0 < u_bracket[0] <= u_bracket[1], "Exact positive u/p geometry")
    result = []
    for j in range(5):
        numerator = j - 4 * pU
        u = F(u_bracket[0] if numerator >= 0 else u_bracket[1], SCALE)
        result.append(integer.floor_fraction_scaled(u * numerator / (2 * pU * (1 - pU))))
    return tuple(result)


def mixed_binomial_probabilities(pL, pU):
    """Five EXACT mixed Bernoulli degree4 Bernstein coefficient laws."""
    require(type(pL) is F and type(pU) is F and 0 < pL <= pU < 1, "Exact closed p interval")
    rows = []
    for r in range(5):
        distribution = [F(1)]
        for p in (pU,) * r + (pL,) * (4 - r):
            updated = [F(0)] * (len(distribution) + 1)
            for j, mass in enumerate(distribution):
                updated[j] += mass * (1 - p)
                updated[j + 1] += mass * p
            distribution = updated
        require(len(distribution) == 5 and sum(distribution, F(0)) == 1
                and all(value >= 0 for value in distribution), "Exact mixed probability normalization")
        rows.append(tuple(distribution))
    return tuple(rows)


def mixed_probabilities_upper_scaled(exact_rows):
    return tuple(tuple(integer.ceil_fraction_scaled(value) for value in row) for row in exact_rows)


def count_cantelli_uppers_scaled(H_upper_scaled, mean_lowers, variance_uppers):
    result = []
    for mean, variance in zip(mean_lowers, variance_uppers):
        if H_upper_scaled >= mean:
            result.append(SCALE)  # CLOSED event, equality/zero-variance atom included
        elif variance == 0:
            result.append(0)
        else:
            gap = mean - H_upper_scaled
            result.append(integer.ceil_div(variance * SCALE ** 2, variance * SCALE + gap * gap))
    require(len(result) == 5 and all(0 <= value <= SCALE for value in result), "FIVE outward Cantelli cell uppers")
    return tuple(result)


def joint_binomial_cdf_upper_scaled(Aj, probability_uppers):
    require(len(Aj) == len(probability_uppers) == 5
            and all(type(value) is int and 0 <= value <= SCALE for value in Aj), "Complete FIVE count bounds")
    maximum = max(integer.ceil_div(sum(a * mass for a, mass in zip(Aj, row)), SCALE)
                  for row in probability_uppers)
    return min(SCALE, maximum)  # independent valid F<=1, not coefficient minima


def compute_verified_conditional_cantelli_box(rectangle, eta_lower, Np=128, NH=1024,
                                             time_limit_seconds=TIME_LIMIT):
    """Fresh exact whole-law/w/beta/actualp/H bound with eta>=LOWER."""
    started = time.monotonic()
    rectangle = checked_request(rectangle, eta_lower, Np, NH, time_limit_seconds)
    wl, wh, bl, bh = rectangle
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Exact conditional Cantelli elapsed budget")
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
    files = (Path(__file__), Path(gaussian_helpers.__file__), Path(gaussian.__file__), Path(integer.__file__), Path(resources.__file__))
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
        "source_pins_integrity_only": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "conclusions": {"conditional_all_law_all_actual_p_all_H_CDF_bound": passed,
            "entire_global_root_or_C4_proved": False, "old_sources_or_receipts_modified": False},
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": resources.peak_bytes(), "time_limit_seconds": time_limit_seconds,
            "memory_limit_bytes": MEMORY_LIMIT, "Prawitz_Fourier_or_binary_producer_called": False}}


def tiny_zero_atom_conditional_checks():
    """81 exact tuples/law test ACTUAL sign convention and sum/2 units."""
    laws = (((F(-2), F(1, 6)), (F(0), F(1, 2)), (F(1), F(1, 3))),
            ((F(-1), F(1, 3)), (F(0), F(1, 2)), (F(2), F(1, 6))))
    checks, actual_ps = 0, []
    for law in laws:
        mean = sum(x * mass for x, mass in law)
        second = sum(x * x * mass for x, mass in law)
        u = sum(x * mass for x, mass in law if x >= 0)
        vp = sum(x * x * mass for x, mass in law if x >= 0)
        vm = sum(x * x * mass for x, mass in law if x < 0)
        p = sum(mass for x, mass in law if x >= 0)
        q, beta = 1 - p, vp - vm
        rho = sum(abs(x) ** 3 * mass for x, mass in law)
        require(mean == 0 and second == 1 and u == F(1, 3)
                and 4 * u ** 2 / (1 - beta ** 2) == F(1, 2)
                and rho == (vp ** 2 + vm ** 2) / u == F(5, 3),
                "Exact standardized zero-atom law and canonical eta0 geometry")
        actual_ps.append(p)
        checks += 1
        distributions = [dict() for _ in range(5)]
        for indices in product(range(3), repeat=4):
            values = tuple(law[i][0] for i in indices)
            mass = F(1)
            for i in indices:
                mass *= law[i][1]
            count, Z = sum(x >= 0 for x in values), sum(values, F(0)) / 2
            distributions[count][Z] = distributions[count].get(Z, F(0)) + mass
        for j, distribution in enumerate(distributions):
            count_mass = sum(distribution.values(), F(0))
            require(count_mass == comb(4, j) * p ** j * q ** (4 - j),
                    "Exact ACTUAL sign-count binomial mass, zero includedpositive")
            mu = sum(Z * mass for Z, mass in distribution.items()) / count_mass
            V = sum(Z * Z * mass for Z, mass in distribution.items()) / count_mass - mu ** 2
            expected_mu = (j - 4 * p) * u / (2 * p * q)
            expected_V = (j * (vp / p - u ** 2 / p ** 2)
                         + (4 - j) * (vm / q - u ** 2 / q ** 2)) / 4
            require(mu == expected_mu and V == expected_V >= 0,
                    "Exact conditional mean/variance use SUM/2, no extra count-mixture variance")
            checks += 2
            thresholds = {mu}
            for Z in distribution:
                thresholds.update((Z - F(1, 100), Z, Z + F(1, 100)))
            for H in thresholds:
                cdf = sum(mass for Z, mass in distribution.items() if Z <= H) / count_mass
                bound = F(1) if H >= mu else V / (V + (mu - H) ** 2)
                require(cdf <= bound, "Exact Cantelli CLOSED atom/equality/nearby thresholds")
                checks += 1
    require(actual_ps == [F(5, 6), F(2, 3)] and actual_ps[1] != 1 - actual_ps[0],
            "Reflection withzero atom is NOT actual signprob complement")
    return checks + 1


def tiny_regressions():
    """Exact helper/topology tests only; NO p/H producer."""
    checks = 0
    wl, wh, bl, bh = F(9, 10), F(19, 20), F(7, 20), F(9, 20)
    checked_request((wl, wh, bl, bh), F(1, 3), 128, 1024, 60)
    cuts = necessary_outer_cuts(wl, wh, bl, bh, F(39, 100), F(157, 400))
    require(not cuts["empty"] and cuts["beta_interval"][1] < bh and cuts["w_interval"][1] < wh,
            "Cauchy necessary cuts preserve joint parameter dependence nearpHi")
    checks += 1
    at_face = necessary_outer_cuts(F(1), F(1), F(1, 5), F(1, 5), F(2, 5), F(2, 5))
    require(not at_face["empty"] and at_face["w_interval"] == (F(1), F(1)),
            "Closed binary equality face is retained, not declaredempty")
    impossible = necessary_outer_cuts(F(1), F(1), F(1, 5), F(1, 5), F(1, 10), F(1, 10))
    require(impossible["empty"], "Strictly incompatible necessary beta interval is empty")
    checks += 2
    for v, u2, L, U in ((F(3, 4), F(1, 8), F(1, 5), F(4, 5)),
                       (F(1, 2), F(1, 4), F(1, 3), F(2, 3))):
        maximum = sign_variance_maximum(v, u2, L, U)
        for n in range(21):
            r = L + (U - L) * F(n, 20)
            require(v / r - u2 / r ** 2 <= maximum, "Unimodal variance maximum exact samples")
            checks += 1
    pL, pU = F(1, 3), F(2, 5)
    mixed = mixed_binomial_probabilities(pL, pU)
    Aj = (F(1, 5), F(4, 5), F(0), F(3, 5), F(1))  # NONmonotone in j deliberately
    coeffs = tuple(sum(a * m for a, m in zip(Aj, row)) for row in mixed)
    for n in range(11):
        t, p = F(n, 10), pL + (pU - pL) * F(n, 10)
        binomial = tuple(comb(4, j) * p ** j * (1 - p) ** (4 - j) for j in range(5))
        direct = sum(a * m for a, m in zip(Aj, binomial))
        bernstein = sum(comb(4, r) * t ** r * (1 - t) ** (4 - r) * coeffs[r] for r in range(5))
        require(direct == bernstein <= max(coeffs), "Exact mixed-binomial Bernstein identity for NONmonotone counts")
        checks += 1
    A_ints = tuple(integer.ceil_fraction_scaled(value) for value in Aj)
    bound = F(joint_binomial_cdf_upper_scaled(A_ints, mixed_probabilities_upper_scaled(mixed)), SCALE)
    require(bound >= max(coeffs), "Positive integer probability/product rounding OUTWARD")
    checks += 1
    for H, expected in ((SCALE, SCALE), (SCALE - 1, 0), (0, 0)):
        result = count_cantelli_uppers_scaled(H, (SCALE,) * 5, (0,) * 5)
        require(result == (expected,) * 5, "Closed zero-variance atoms and mean equality")
        checks += 1
    for H in (-SCALE, 0, SCALE):
        v = integer.ceil_fraction_scaled(F(2, 7))
        m = 2 * SCALE
        upper = count_cantelli_uppers_scaled(H, (m,) * 5, (v,) * 5)[0]
        exact_value = F(v, SCALE) / (F(v, SCALE) + F(m - H, SCALE) ** 2)
        require(F(upper, SCALE) >= exact_value, "Exact integer Cantelli ratio scaling")
        checks += 1
    require(minmax_beta_square(F(-2, 5), F(-1, 5)) == (F(1, 25), F(4, 25))
            and minmax_beta_square(F(-1, 5), F(1, 5))[0] == 0, "Signed beta/root square geometry")
    checks += 1
    try:
        checked_request((0.9, wh, bl, bh), F(1, 3), 128, 1024, 60)
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("Floating moment-box proof endpoint accepted")
    checks += tiny_zero_atom_conditional_checks()
    return {"status": "EXACT_CONDITIONAL_CANTELLI_HELPER_TESTS_ONLY", "exact_checks": checks,
            "full_p_H_box_or_other_producer_called": False,
            "all_law_CDF_or_root_proved_by_tests": False, "old_sources_or_receipts_modified": False}


def json_ready(value):
    if type(value) is F:
        return str(value)
    raise TypeError("Unsupported exact conditional-Cantelli receipt value: " + type(value).__name__)


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--produce", action="store_true")
    mode.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if args.self_test or not (args.produce or args.replay_existing):
        print(json.dumps(tiny_regressions(), sort_keys=True))
        return
    output = Path(__file__).with_name(Path(__file__).stem
        + "_box9_10_19_20_beta7_20_9_20_eta1_4_Np128_NH1024.json")
    require(args.replay_existing or not output.exists(), "Never overwrite an exact conditional-Cantelli receipt")
    require(not args.replay_existing or output.exists(), "Read-only fresh replay receipt exists")
    result = compute_verified_conditional_cantelli_box(DEFAULT_RECTANGLE, DEFAULT_ETA_LOWER,
        Np=DEFAULT_NP, NH=DEFAULT_NH, time_limit_seconds=TIME_LIMIT - (time.monotonic() - started))
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False, default=json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Exact conditional-Cantelli receipt<=1MiB")
    peak = resources.peak_bytes()
    require(time.monotonic() - started < TIME_LIMIT and (peak is None or peak <= MEMORY_LIMIT),
            "Entire CLI within60s/64MiB, unchanged mathematical scope")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only receipt input")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        for key in fresh:
            if key != "resources":
                require(saved[key] == fresh[key], "Fresh exact conditional-Cantelli replay: " + key)
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "closed_rectangle": result["closed_rectangle"],
        "eta_lower": result["eta_lower"], "Np": result["Np"], "NH": result["NH"],
        "upper_exact": result["upper_exact"], "upper_decimal_diagnostic": result["upper_decimal_diagnostic"],
        "strict_margin_exact": result["strict_margin_exact"], "output_bytes": len(raw.encode("utf-8")),
        "resources": result["resources"]}, sort_keys=True, default=json_ready))


if __name__ == "__main__":
    main()
