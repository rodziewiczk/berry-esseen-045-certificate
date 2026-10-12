"""Exact continuous-frequency physical-H curvature; NOT a CDF certificate.

Mathematical precondition, not a status/receipt/provenance check
-----------------------------------------------------------
Let X be standardized, let its canonical Q3 reference have characteristic
function g, and set eta=rho(P)-rho(Q3)>=0. At the EXACT midfrequencies
q_j=3*(j+1/2)/N the caller has freshly proved, for the SAME whole geometry
class and CLOSED eta cell [L,U], that |g(q_j)|<=a_j<=1. Every supplied
affine model A+B*eta individually majorizes |phi_P(q_j)-g(q_j)| on this
entire cell. Bounds are mathematical premises; types, names, source pins,
JSON fields, and this module's return flags do not establish them. No
characteristic function or quadrature producer is called by this module.

For each model that is nonnegative at BOTH cell endpoints, its whole-cell
supremum is max(A+B*L,A+B*U). Their scalar minimum is a valid uniform radius
e_j. A signed slope is allowed; a negative endpoint model is discarded,
not clipped. We do NOT take a pointwise winner and extrapolate it, minimize
polynomial coefficients, or infer validity from sampled eta values.

Since E|X|<=sqrt(EX^2)=1, |phi_P(t)-phi_P(s)|<=|t-s|. Thus for EVERY u in
the CLOSED frequency cell [j/N,(j+1)/N], including joins,

 |phi_P(3u)| <= p_j := min(1,a_j+e_j+3/(2N)).                 (1)

The code ceilings p_j to the declared fixed-point scale. This Lipschitz
fill is for the actual P, not for a nominal reference or a sampled winner.
Both reflected laws have the SAME modulus bounds. No M4/support/contact
assumption is needed for this curvature lemma itself.

Two complete positive kernel majorants
-------------------------------------
Write K(u)=(1-u)+iR(u), R=(1-u)cot(pi*u)+1/pi, S=uR. On 0<u<1,
R>=0: for u<=1/2 cot is nonnegative; for u>1/2 put v=1-u and use
tan(pi*v)>=pi*v. The retained cotangent partial fraction identity is

 S(u)=(1/pi)*(1-2u^2*(1-u)*sum_{n>=1}1/(n^2-u^2)).           (2)

All summands are positive, so 0<=S<=1/pi<1/3. Retaining JUST the first
summand gives

 S <= (1-u)*(1+2u)/(pi*(1+u)) <= 3*(1-u)/(2*pi) < (1-u)/2. (3)

Here pi>3; endpoints follow by limits. Since |K|<=1-u+R, BOTH

 u^2|K(u)| <= W(u)=u^2*(1-u)+u/3,
 u^2|K(u)| <= V(u)=u^2*(1-u)+u*(1-u)/2                      (4)

hold on the whole interval. Define w_j=integral_cell W, v_j=integral_cell V.
Their exact primitives are u^3/3-u^4/4+u^2/6 and
u^2/4+u^3/6-u^4/4. Separately sum w_j=1/4 and sum v_j=1/6.
For EACH cell, d_j=min(w_j,v_j) is an upper on the integral of the SAME
nonnegative kernel u^2|K|. This is an intersection of complete scalar
integral bounds, NOT a coefficientwise minimum. Sum d_j is recorded
separately; we do not assert it equals either 1/4 or 1/6.

Physical threshold interpolation, not frequency quadrature
--------------------------------------------------------
The physical fourfold Prawitz function is

 J_P(x)=1/2+integral_0^1 Re[K(u)*exp(-6iu*x)*phi_P(3u)^4] du.

The real integrand is regular at zero; an improper COMPLEX integral is
not asserted. Finite E|X| and u*K integrability justify its first
x-derivative, and u^2*K integrability justifies the second. By (1)-(4),

 |J_P''(x)| <= B := 36*sum_j d_j*p_j^4.                     (5)

This is uniform in ALL x and the SAME entire geometry/eta class. No
midpoint estimate or new frequency-tail reserve is used in (5).
The elementary normal bound sup|Phi''(x)|=phi(1)<1/4 follows from
pi>3 and e>65/24, so 2*pi*e>65/4>16. For the raw-H physical function
G(H)=2*(J_P(H/2)-Phi(H/2)), |G''|<=(B+1/4)/2. Linear interpolation
between adjacent raw thresholds separated by h therefore needs

 physical_H_reserve = h^2*(B+1/4)/16.                       (6)

This REPLACES the previous ONE reserve 19*h^2/32. Do not add both. The
separately justified physical midpoint reserve 687/(8*N^2) is unchanged
and still counted ONCE by a CDF consumer. With p_j=1, the first-pole
majorant alone gives B<=6 and reserve<=25*h^2/64; at h=1/8 this already
saves at least 13/4096 against the old reserve. Profile bounds can do
better. A per-eta-cell reserve is constant on that WHOLE closed cell;
it need not come from the same chosen models as a finite transfer bound.

Convenience Q3 radii, when their canonical premises are proved
-----------------------------------------------------------
The wrapper below creates three independently valid affine models:
eta*q^3/6 (Hermite--Genocchi), M^2*p0*q^2, and 1+a_j. For the middle
bound, r=f[0,c,c,y]=(f[c,c,y]-f[0,c,c])/y gives |r|<=q^2/y for y>0.
With M>=c and the same necessary budget eta*E_nu[1/(c^2*y)]<=p0,
eta*E|r|<=M^2*p0*q^2. At eta=0 the canonical moment identity gives
delta=0 directly, without defining nu. The wrapper receives fresh
actual-reference modulus bounds and whole-box M,p0 uppers, NOT numeric
receipts and NOT a nominal-Q modulus in place of the actual reference.

This module supplies only exact scalar curvature arithmetic, with dormant
tiny tests. It establishes no Prawitz/CDF theorem, normalization/tail
bound, owner-support reduction, coverage completion, or unrestricted C4.
No import-time computation, resource-heavy tests, files, or external calls.
"""

from __future__ import annotations

from fractions import Fraction as F
import json

SCALE = 10 ** 40


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil_scaled(value, scale):
    require(type(value) is F and type(scale) is int and scale > 0,
            "Exact rational value and positive integer fixed-point scale")
    return -((-value.numerator * scale) // value.denominator)


def checked_eta_interval(eta_interval):
    require(type(eta_interval) in (tuple, list) and len(eta_interval) == 2
            and all(type(x) is F for x in eta_interval)
            and 0 <= eta_interval[0] <= eta_interval[1],
            "Exact nonnegative CLOSED eta cell")
    return tuple(eta_interval)


def whole_cell_radius_upper(models, eta_interval):
    """Min of COMPLETE-model endpoint maxima, never endpoint pointwise minima."""
    L, U = checked_eta_interval(eta_interval)
    require(type(models) in (tuple, list) and len(models) > 0,
            "At least one individually proved whole-cell affine radius")
    candidates, discarded = [], []
    for index, model in enumerate(models):
        require(type(model) in (tuple, list) and len(model) == 3
                and type(model[0]) is F and type(model[1]) is F
                and type(model[2]) is str,
                "Models are exact Fraction A,B and a diagnostic label")
        A, B, label = model
        endpoints = (A + B * L, A + B * U)
        if min(endpoints) < 0:
            discarded.append(index)
            continue
        candidates.append((max(endpoints), index, A, B, label, endpoints))
    require(candidates, "No nonnegative affine radius on this entire closed cell")
    upper, index, A, B, label, endpoints = min(candidates, key=lambda c: (c[0], c[1]))
    return {"upper": upper, "selected_model_index": index, "selected_model_label": label,
            "selected_affine_model": (A, B), "selected_endpoint_uppers": endpoints,
            "discarded_negative_endpoint_model_indices": tuple(discarded)}


def frequency_cell_weights(N, index):
    """Two whole-cell integral uppers and their valid scalar intersection."""
    require(type(N) is int and N > 0 and type(index) is int and 0 <= index < N,
            "Positive exact grid size and integer cell index")
    lo, hi = F(index, N), F(index + 1, N)

    def ordinary_primitive(u):
        return u ** 3 / 3 - u ** 4 / 4 + u ** 2 / 6

    def first_pole_primitive(u):
        return u ** 2 / 4 + u ** 3 / 6 - u ** 4 / 4

    ordinary = ordinary_primitive(hi) - ordinary_primitive(lo)
    first_pole = first_pole_primitive(hi) - first_pole_primitive(lo)
    require(ordinary > 0 and first_pole > 0, "Positive complete integral bounds")
    return {"u_interval": (lo, hi), "ordinary": ordinary,
            "first_pole": first_pole, "intersection": min(ordinary, first_pole)}


def physical_H_curvature_bound(frequencies, eta_interval, H_step, N=None, scale=SCALE):
    """Exact curvature from mathematically PREVERIFIED actual-reference bounds.

    frequencies[j] has q:Fraction, modulus_upper_int:int in [0,scale],
    models:tuple/list of (Fraction A,Fraction B,str diagnostic_label).
    All bound-validity premises are stated in the module proof, not proved
    by accepting this schema. No table's status/pin/provenance is trusted.
    """
    eta_interval = checked_eta_interval(eta_interval)
    require(type(frequencies) in (tuple, list) and len(frequencies) > 0,
            "Complete nonempty preverified midpoint frequency grid")
    if N is None:
        N = len(frequencies)
    require(type(N) is int and N == len(frequencies) and N > 0,
            "Exactly N ordered frequency cells, no omitted nodes")
    require(type(scale) is int and scale > 0 and type(H_step) is F and H_step > 0,
            "Exact positive scale and raw-H spacing")
    fill = F(3, 2 * N)
    ordinary_sum = first_pole_sum = intersection_sum = F(0)
    ordinary_J = first_pole_J = intersection_J = F(0)
    diagnostics = []
    for j, item in enumerate(frequencies):
        require(type(item) is dict and type(item.get("q")) is F
                and item["q"] == F(3 * (2 * j + 1), 2 * N),
                "Exact ordered q_j=3*(j+1/2)/N for every continuous cell")
        a_int = item.get("modulus_upper_int")
        require(type(a_int) is int and 0 <= a_int <= scale,
                "Fresh actual-reference modulus upper in fixed-point units")
        radius = whole_cell_radius_upper(item.get("models"), eta_interval)
        p_int = min(scale, ceil_scaled(F(a_int, scale) + radius["upper"] + fill, scale))
        require(0 <= p_int <= scale, "Outward continuous-cell actual-P modulus cap")
        p = F(p_int, scale)
        weights = frequency_cell_weights(N, j)
        ordinary_sum += weights["ordinary"]
        first_pole_sum += weights["first_pole"]
        intersection_sum += weights["intersection"]
        ordinary_J += 36 * weights["ordinary"] * p ** 4
        first_pole_J += 36 * weights["first_pole"] * p ** 4
        intersection_J += 36 * weights["intersection"] * p ** 4
        diagnostics.append({"q_index": j, "q": item["q"], "actual_reference_modulus_upper_int": a_int,
            "whole_eta_radius": radius, "actual_P_continuous_cell_modulus_upper_int": p_int,
            "weights": weights})
    require(ordinary_sum == F(1, 4) and first_pole_sum == F(1, 6),
            "Independent exact primitive totals; intersection total recorded separately")
    require(0 < intersection_sum <= min(ordinary_sum, first_pole_sum)
            and intersection_J <= min(ordinary_J, first_pole_J)
            and ordinary_J <= 9 and first_pole_J <= 6,
            "Complete integral intersections and uniform curvature ceilings")
    raw_curvature = (intersection_J + F(1, 4)) / 2
    reserve = H_step ** 2 * (intersection_J + F(1, 4)) / 16
    old_reserve = F(19, 32) * H_step ** 2
    first_pole_uniform = F(25, 64) * H_step ** 2
    require(reserve <= first_pole_uniform < old_reserve,
            "Replace ONE old threshold reserve by this no-larger whole-cell reserve")
    return {"kind": "EXACT_PHYSICAL_H_CURVATURE_ARITHMETIC_UNDER_EXPLICIT_BOUND_PREMISES",
        "scale": scale, "N": N, "closed_eta_cell": eta_interval, "H_step": H_step,
        "CF_Lipschitz_continuous_cell_fill": fill, "frequency_cells": diagnostics,
        "kernel_weight_sums": {"ordinary": ordinary_sum, "first_pole": first_pole_sum,
                               "complete_integral_intersection": intersection_sum},
        "J_second_derivative_uppers": {"ordinary": ordinary_J, "first_pole": first_pole_J,
                                      "complete_integral_intersection": intersection_J},
        "normal_second_derivative_upper": F(1, 4), "raw_H_second_derivative_upper": raw_curvature,
        "physical_H_reserve": reserve, "old_physical_H_reserve_NOT_added": old_reserve,
        "uniform_first_pole_H_reserve": first_pole_uniform,
        "raw_reserve_saving_against_old": old_reserve - reserve,
        "physical_midpoint_quad_reserve_unchanged_NOT_added_here": F(687, 8 * N * N),
        "proof_boundary": {"preverified_radius_and_actual_reference_moduli_are_math_premises": True,
            "continuous_frequency_cells_not_endpoint_only": True,
            "one_threshold_reserve_replaces_old": True,
            "this_is_a_CDF_or_global_C4_certificate": False,
            "fresh_CF_quadrature_reference_or_CDF_producer_called": False}}


def from_preverified_box_frequency_data(frequency_data, box_geometry, eta_interval,
                                       H_step, N=None, scale=SCALE):
    """Canonical cube/mass/unit radii; fresh actual-modulus/box premises required.

    Accepts the corrected fresh leaf's fields without importing any leaf,
    old CF producer, or numeric receipt. Box root uppers are schema checked,
    but their geometric/budget validity remains an explicit math premise.
    """
    require(type(scale) is int and scale > 0 and type(box_geometry) is dict,
            "Declared exact scale and freshly proved whole-box geometry")
    for key in ("a_bracket", "b_bracket"):
        bracket = box_geometry.get(key)
        require(type(bracket) in (tuple, list) and len(bracket) == 2
                and all(type(x) is int for x in bracket) and 0 < bracket[0] <= bracket[1],
                "Positive whole-box contact brackets at the declared scale")
    p0 = box_geometry.get("p0_hi")
    require(type(p0) is F and 0 <= p0 <= 1, "Exact whole-box zero-mass upper")
    M = F(max(box_geometry["a_bracket"][1], box_geometry["b_bracket"][1]), scale)
    require(type(frequency_data) in (tuple, list) and len(frequency_data) > 0,
            "Fresh complete corrected actual-reference frequency data")
    frequencies = []
    for item in frequency_data:
        require(type(item) is dict and type(item.get("q")) is F,
                "Exact preverified physical midpoint frequency")
        a_int = item.get("g_actual_modulus_upper_int")
        require(type(a_int) is int and 0 <= a_int <= scale,
                "Actual-Q modulus, not nominal-Q modulus or a saved bound")
        q, a = item["q"], F(a_int, scale)
        models = ((F(0), q ** 3 / 6, "cube"),
                  (M ** 2 * p0 * q ** 2, F(0), "mass"),
                  (1 + a, F(0), "unit"))
        frequencies.append({"q": q, "modulus_upper_int": a_int, "models": models})
    return physical_H_curvature_bound(frequencies, eta_interval, H_step, N, scale)


def self_tests():
    """Dormant SMALL exact tests only; no fresh reference/CF/CDF producer."""
    checks = 0
    for N in (1, 2, 3, 7, 16):
        weights = [frequency_cell_weights(N, j) for j in range(N)]
        require(sum((w["ordinary"] for w in weights), F(0)) == F(1, 4), "Ordinary primitive total")
        require(sum((w["first_pole"] for w in weights), F(0)) == F(1, 6), "First-pole primitive total")
        require(sum((w["intersection"] for w in weights), F(0)) <= F(1, 6), "Scalar cell intersection")
        checks += 3
        frequencies = [{"q": F(3 * (2 * j + 1), 2 * N), "modulus_upper_int": SCALE,
                        "models": ((F(0), F(0), "zero"),)} for j in range(N)]
        result = physical_H_curvature_bound(frequencies, (F(0), F(1)), F(1, 8), N)
        require(result["J_second_derivative_uppers"]["ordinary"] == 9
                and result["J_second_derivative_uppers"]["first_pole"] == 6, "Uniform separate ceilings")
        require(result["physical_H_reserve"] <= F(25, 4096)
                and result["raw_reserve_saving_against_old"] >= F(13, 4096), "Replacement uniform saving")
        checks += 2
    selected = whole_cell_radius_upper(((F(0), F(1), "increasing"),
        (F(1), F(-1), "decreasing")), (F(0), F(1)))
    require(selected["upper"] == 1, "Never replace min whole maxima by endpoint minima (which are zero)")
    checks += 1
    selected = whole_cell_radius_upper(((F(1, 2), F(-1), "negative_at_U"),
        (F(2), F(-1), "valid_decreasing")), (F(0), F(1)))
    require(selected["upper"] == 2 and selected["discarded_negative_endpoint_model_indices"] == (0,),
            "Negative endpoint model dropped without clipping; signed slope retained")
    checks += 1
    N, scale = 16, 1000
    frequencies = [{"q": F(3 * (2 * j + 1), 2 * N), "modulus_upper_int": 0,
                    "models": ((F(0), F(0), "zero"),)} for j in range(N)]
    result = physical_H_curvature_bound(frequencies, (F(0), F(0)), F(1, 32), N, scale)
    require(all(row["actual_P_continuous_cell_modulus_upper_int"] == 94
                for row in result["frequency_cells"]), "3/(2N)=.09375 ceilings upward to .094")
    require(result["J_second_derivative_uppers"]["complete_integral_intersection"] < F(1, 100),
            "Profile modulus bounds improve continuous-frequency curvature")
    checks += 2
    box = {"a_bracket": (SCALE, SCALE), "b_bracket": (SCALE, SCALE), "p0_hi": F(0)}
    data = [{"q": F(3 * (2 * j + 1), 2 * N), "g_actual_modulus_upper_int": SCALE}
            for j in range(N)]
    wrapped = from_preverified_box_frequency_data(data, box, (F(0), F(1)), F(1, 8), N)
    require(all(row["whole_eta_radius"]["upper"] == 0 for row in wrapped["frequency_cells"]),
            "Mass-zero model stays zero on whole cell without invoking a producer")
    checks += 1
    for bad in ((F(-1), F(0)), (F(1), F(0)), (0, F(1))):
        rejected = False
        try:
            checked_eta_interval(bad)
        except RuntimeError:
            rejected = True
        require(rejected, "Invalid/nonexact closed eta cell rejected")
        checks += 1
    tampered = [dict(row) for row in frequencies]
    tampered[0]["q"] = F(0)
    rejected = False
    try:
        physical_H_curvature_bound(tampered, (F(0), F(0)), F(1, 8), N, scale)
    except RuntimeError:
        rejected = True
    require(rejected, "Incomplete/mislabeled grid cannot fill continuous cells")
    checks += 1
    return {"status": "TINY_EXACT_CURVATURE_ARITHMETIC_TESTS_ONLY", "exact_checks": checks,
            "reference_CF_quadrature_CDF_or_global_producer_called": False,
            "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
