"""PURE exact WHOLE-box/eta, PER-H physical midpoint reserve for n=4.

Scope: standardized iid actual P, canonical (w,beta) in the declared
closed rectangle, eta=rhoP-rhoQ in the closed eta interval, |X|<=17/4,
rhoP<46/25. Neither a finite original support nor an extra M4 input is
assumed. The first-critical placement and closed-CDF Prawitz theorem
remain separate inputs. This module is NOT a CDF/table producer.

For tag sigma, y=|X| and c=a or b, W=y(y-c)^2, EW=eta. The identities
 y^3=W+2c*y^2-c^2*y,
 y^4=(y+2c)*W+3c^2*y^2-2c^3*y
and EY(tag)=u, EY^2(tag)=u*c imply
 kappaP=(b-a)+E[sigma W],
 M4P=(a^2-ab+b^2)+E[(y+2c)W].
Thus |kappaP|<=min(rhoP,|b-a|+eta) and
 M4P<=min(R*rhoP,M4Q+(R+2max(a,b))*eta).
No defect probability nu is defined at eta=0; these EW identities apply
there directly. For beta>=0 the exact squares / moments are
 rhoQ^2=(1+beta^2)^2/[w(1-beta^2)],
 (b-a)^2=4beta^2/[w(1-beta^2)],
 M4Q=(1+3beta^2)/[w(1-beta^2)].
All three maxima are attained at wLo,betaHi, hence whole-rectangle bounds.
The physical contact upper is min(R,b_hi): actual c=EY^2/EY<=R, even
if the enclosing geometric rectangle contains nonphysical root points.

For Z=(X1+X2+X3+X4)/2 and x=H/2,
 ED^2=x^2+1,
 ED^4<=x^4+6x^2+2|x|kappaUp+(M4Up+9)/4, D=x-Z.
Cauchy bounds m1<=sqrt(ED2), m3<=sqrt(ED2*ED4).
The audited regular Prawitz integrand is F=(1-u)A+S L with
 0<=S<=1/3, |S'|<=2, |S''|<=5,
 |A'|<=6m1, |A''|<=36m2,
 |L|<=6m1, |L'|<=18m2, |L''|<=72m3.
Consequently |F''|<=42m1+108m2+24m3. Composite midpoint's RAW reserve
is that upper/(12N^2). Its scalar intersection with the independently
audited old687/(8N^2) is one complete physical reserve, not two reserves.

This is PER-H: combine it with M_H+2Gamma_H+remainder at the SAME H before
maximizing H. The continuous-H interpolation reserve is still required
ONCE. No radius, nonlinear remainder, Gamma, H reserve or acceptance is
computed here. Exact Fractions + isqrt only; floats never prove bounds.
Dormant tests enumerate small rational laws and check exact identities,
root rounding, physical moments and dominance over the old reserve.
They are not a complete original-law C4 certificate. No file writes,
foreign imports, producer/replay jobs or import-time computation.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import isqrt

SCALE = 10 ** 40
RADIUS, RHO_CAP = F(17, 4), F(46, 25)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sqrt_upper(value):
    """Pure outward rational square root, including exact zero."""
    require(type(value) is F and value >= 0, "Nonnegative exact rational radicand")
    floor = isqrt(value.numerator * SCALE * SCALE // value.denominator)
    upper = floor if floor * floor * value.denominator == value.numerator * SCALE * SCALE else floor + 1
    require(floor * floor * value.denominator <= value.numerator * SCALE * SCALE
            <= upper * upper * value.denominator, "Both exact integer square checks")
    return F(upper, SCALE)


def checked_rectangle_and_eta(rectangle, eta_interval):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(z) is F for z in rectangle), "Four exact whole-box endpoints")
    wl, wh, bl, bh = rectangle
    require(0 < wl <= wh <= 1 and 0 <= bl <= bh < 1, "Canonical magnitude geometry")
    require(type(eta_interval) in (tuple, list) and len(eta_interval) == 2
            and all(type(z) is F for z in eta_interval)
            and 0 <= eta_interval[0] <= eta_interval[1], "Closed nonnegative eta interval")
    return tuple(rectangle), tuple(eta_interval)


def whole_cell_moment_uppers(rectangle, eta_interval):
    """Under the stated ACTUAL-law premises; no table/status/JSON inputs."""
    rectangle, eta_interval = checked_rectangle_and_eta(rectangle, eta_interval)
    wl, _, _, bh = rectangle
    _, U = eta_interval
    denominator = wl * (1 - bh * bh)
    rhoQ_upper = sqrt_upper((1 + bh * bh) ** 2 / denominator)
    kappaQ_upper = sqrt_upper(4 * bh * bh / denominator)
    M4Q_upper = (1 + 3 * bh * bh) / denominator
    contact_upper = min(RADIUS, sqrt_upper((1 + bh) / (wl * (1 - bh))))
    rho_upper = min(RHO_CAP, rhoQ_upper + U)
    kappa_upper = min(rho_upper, kappaQ_upper + U)
    M4_upper = min(RADIUS * rho_upper, M4Q_upper + (RADIUS + 2 * contact_upper) * U)
    require(rho_upper >= 1 and M4_upper >= 1 and kappa_upper >= 0,
            "Necessary physical moment upper shapes")
    return {"closed_rectangle": rectangle, "closed_eta_interval": eta_interval,
        "physical_support_radius": RADIUS, "actual_rho_strict_cap": RHO_CAP,
        "rhoQ_upper_exact": rhoQ_upper, "kappaQ_abs_upper_exact": kappaQ_upper,
        "reference_M4_upper_exact": M4Q_upper, "actual_contact_upper_exact": contact_upper,
        "actual_rho_upper_exact": rho_upper, "actual_kappa_abs_upper_exact": kappa_upper,
        "actual_M4_upper_exact": M4_upper,
        "original_law_need_not_be_finitely_supported": True,
        "extra_fourth_moment_premise": False}


def physical_quad_at_H(moment_uppers, H, N=256):
    """ONE original-law midpoint reserve at this exact raw-H node.

    moment_uppers must come from the above direct pure whole-cell lemma
    under its stated actual-law premises. Its schema alone is NOT proof.
    """
    require(type(moment_uppers) is dict and type(H) is F and F(-4) <= H <= F(25, 8)
            and type(N) is int and N > 0, "Exact central H and positive frequency count")
    rectangle, eta_interval = checked_rectangle_and_eta(
        moment_uppers["closed_rectangle"], moment_uppers["closed_eta_interval"])
    require(moment_uppers == whole_cell_moment_uppers(rectangle, eta_interval),
            "Recompute ALL exact whole-cell moment uppers, not a declared shape")
    x = H / 2
    D2 = x * x + 1
    D4 = x ** 4 + 6 * x * x + 2 * abs(x) * moment_uppers["actual_kappa_abs_upper_exact"] \
         + (moment_uppers["actual_M4_upper_exact"] + 9) / 4
    m1, m3 = sqrt_upper(D2), sqrt_upper(D2 * D4)
    F2 = 42 * m1 + 108 * D2 + 24 * m3
    new = F2 / (12 * N * N)
    old = F(687, 8 * N * N)
    return {"H": H, "N": N, "D2_exact": D2, "D4_upper_exact": D4,
        "D_abs_first_upper_exact": m1, "D_abs_third_upper_exact": m3,
        "regular_integrand_second_derivative_abs_upper_exact": F2,
        "local_physical_quad_upper_exact": new, "old_uniform_physical_quad_upper_exact": old,
        "ONE_selected_physical_quad_upper_exact": min(new, old),
        "local_moment_bound_selected": new <= old,
        "H_interpolation_reserve_added": False, "CDF_or_C4_acceptance_claim": False}


def exact_law_geometry(law):
    require(sum(p for _, p in law) == 1 and sum(x * p for x, p in law) == 0
            and sum(x * x * p for x, p in law) == 1 and all(p >= 0 for _, p in law),
            "Exact standardized finite law ONLY for tiny tests")
    u = sum(x * p for x, p in law if x > 0)
    vp = sum(x * x * p for x, p in law if x > 0)
    vm = 1 - vp
    a, b = vm / u, vp / u
    beta = vp - vm
    rho = sum(abs(x) ** 3 * p for x, p in law)
    rhoQ = (a * a + b * b) / (a + b)
    return {"u": u, "a": a, "b": b, "beta": beta,
        "w": 4 * u * u / (1 - beta * beta), "rho": rho, "rhoQ": rhoQ, "eta": rho - rhoQ,
        "kappa": sum(x ** 3 * p for x, p in law), "M4": sum(x ** 4 * p for x, p in law)}


def self_tests():
    """Tiny pure exact regressions; no root/table/CF/receipt producer."""
    checks = 0
    for value in (F(0), F(1, 4), F(2), F(5, 2), F(19), F(1001, 97)):
        upper = sqrt_upper(value)
        require(upper * upper >= value and (upper == 0 or (upper - F(1, SCALE)) ** 2 <= value),
                "Independent outward rational sqrt comparisons")
        checks += 1
    laws = []
    for t in (F(0), F(1, 32), F(1, 16), F(3, 32)):
        laws.append(((F(-2), t), (F(-1), F(1, 2) - 4 * t), (F(0), 6 * t),
                     (F(1), F(1, 2) - 4 * t), (F(2), t)))
    for s in (F(1, 40), F(1, 12), F(1, 6)):
        law = ((F(-1), F(1, 2) - s), (F(0), 3 * s), (F(1), F(1, 2) - 3 * s), (F(2), s))
        laws.extend((law, tuple((-x, p) for x, p in law)))
    laws.append(((F(-3, 2), F(2, 9)), (F(0), F(5, 9)), (F(3, 2), F(2, 9))))
    for law in laws:
        g = exact_law_geometry(law)
        require(g["eta"] >= 0 and g["rho"] < RHO_CAP, "Physical exact tiny-law scope")
        defect = signed_defect = fourth_defect = F(0)
        for x, p in law:
            y = abs(x)
            c = g["b"] if x > 0 else g["a"]
            W = y * (y - c) ** 2
            require(y ** 3 == W + 2 * c * y * y - c * c * y
                    and y ** 4 == (y + 2 * c) * W + 3 * c * c * y * y - 2 * c ** 3 * y,
                    "Exact pointwise cubic and quartic contact identities")
            defect += p * W
            signed_defect += (1 if x > 0 else -1) * p * W
            fourth_defect += p * (y + 2 * c) * W
            checks += 1
        require(defect == g["eta"] and g["kappa"] == g["b"] - g["a"] + signed_defect
                and g["M4"] == g["a"] ** 2 - g["a"] * g["b"] + g["b"] ** 2 + fourth_defect,
                "Exact integrated contact identities including atoms at zero/contacts")
        checks += 1
        rect = (g["w"], g["w"], abs(g["beta"]), abs(g["beta"]))
        moments = whole_cell_moment_uppers(rect, (g["eta"], g["eta"]))
        require(g["rho"] <= moments["actual_rho_upper_exact"]
                and abs(g["kappa"]) <= moments["actual_kappa_abs_upper_exact"]
                and g["M4"] <= moments["actual_M4_upper_exact"], "Actual exact-law moment uppers")
        checks += 1
        for H in (F(-4), F(-2), F(0), F(1), F(25, 8)):
            result = physical_quad_at_H(moments, H)
            x = H / 2
            trueD4 = x ** 4 + 6 * x * x - 2 * x * g["kappa"] + (g["M4"] + 9) / 4
            require(trueD4 <= result["D4_upper_exact"]
                    and 0 <= result["ONE_selected_physical_quad_upper_exact"]
                        <= F(687, 8 * 256 * 256), "Physical D4 and complete-old-bound dominance")
            checks += 1
    rademacher = whole_cell_moment_uppers((F(1), F(1), F(0), F(0)), (F(0), F(0)))
    center = physical_quad_at_H(rademacher, F(0))
    require(center["ONE_selected_physical_quad_upper_exact"] < F(1, 4000)
            and center["old_uniform_physical_quad_upper_exact"]
                - center["ONE_selected_physical_quad_upper_exact"] > F(1, 1000),
            "Nontrivial exact improvement: eta0 Rademacher central quad")
    checks += 1
    return {"status": "TINY_EXACT_CONTACT_MOMENT_AND_LOCAL_QUADRATURE_TESTS_ONLY",
        "exact_checks": checks, "rational_original_laws_tested": len(laws),
        "no_finite_support_premise_in_lemma": True, "full_C4_or_CDF_certificate": False,
        "producer_or_file_write_called": False}
