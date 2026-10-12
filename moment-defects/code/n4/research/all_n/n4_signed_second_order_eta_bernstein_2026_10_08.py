"""Exact whole-eta polynomial ledger for SIGNED common first order.

For psi=g+delta,
psi^4-g^4-4*g^3*delta=delta^2*(psi^2+2*psi*g+3*g^2).
A proven |g|<=a<=1, |delta|<=e(eta), |psi|<=1 therefore give
|R2|<=e^2*(p^2+2*p*a+3*a^2), p=min(1,a+e).
Freeze p upward on a closed eta cell: the remainder is quadratic.
A common-nu signed dual Gamma=A_gamma+B_gamma*eta may be negative.
Its signed slope/intercept are NEVER clipped or replaced by zero.

The target polynomial is raw_Q+ONE physical reserves+2Gamma+2sumR2
minus target*(rhoQ_LO+eta). Exact Bernstein negativity proves the ledger
only after all response, radius, kernel, root and physical inputs are
proved independently. This helper supplies no CDF or full-root claim.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path

import n4_eta_affine_transfer_bernstein_2026_10_08 as algebra


def frozen_second_order_remainder(a, intercept, slope, lower, upper):
    a, intercept, slope, lower, upper = algebra.checked_radius(a, intercept, slope, lower, upper)
    algebra.require(lower >= 0, "Nonnegative physical eta interval")
    p = min(F(1), a + max(intercept + slope * lower, intercept + slope * upper))
    multiplier = p ** 2 + 2 * p * a + 3 * a ** 2
    return algebra.poly_scale(algebra.affine_power(intercept, slope, 2), multiplier)


def signed_raw_target(raw_constant, gamma_intercept, gamma_slope,
                      weighted_remainders, rho_q_lower, target):
    gamma_intercept, gamma_slope = map(algebra.exact, (gamma_intercept, gamma_slope))
    result = algebra.raw_target_for_transfers(raw_constant, weighted_remainders, rho_q_lower, target)
    return algebra.poly_add(result, (2 * gamma_intercept, 2 * gamma_slope))


def cmul(left, right):
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def cpow(value, degree):
    result = (F(1), F(0))
    for _ in range(degree):
        result = cmul(result, value)
    return result


def norm_squared(value):
    return value[0] ** 2 + value[1] ** 2


def regressions():
    checks = 0
    for a, A, B, L, U in ((F(0), F(0), F(1), F(0), F(1)),
                          (F(1), F(0), F(1), F(0), F(1)),
                          (F(3, 5), F(0), F(1, 2), F(0), F(1)),
                          (F(1, 2), F(1, 2), F(-1, 3), F(0), F(1)),
                          (F(1, 3), F(1, 7), F(0), F(1, 4), F(1, 4))):
        polynomial = frozen_second_order_remainder(a, A, B, L, U)
        for j in range(17):
            eta = L + (U - L) * F(j, 16)
            e = A + B * eta
            p = min(F(1), a + e)
            direct = e ** 2 * (p ** 2 + 2 * p * a + 3 * a ** 2)
            upper = algebra.evaluate(polynomial, eta)
            algebra.require(upper >= direct >= 0, "Whole-cell frozen-p quadratic upper")
            checks += 1
            for direction in ((F(1), F(0)), (F(-1), F(0)), (F(0), F(1)),
                              (F(3, 5), F(4, 5)), (F(-3, 5), F(4, 5))):
                g, delta = (a, F(0)), (e * direction[0], e * direction[1])
                psi = (g[0] + delta[0], g[1] + delta[1])
                if norm_squared(psi) > 1:
                    continue
                psi4, g4, first = cpow(psi, 4), cpow(g, 4), cmul(cpow(g, 3), delta)
                remainder = (psi4[0] - g4[0] - 4 * first[0], psi4[1] - g4[1] - 4 * first[1])
                factor = (cpow(psi, 2)[0] + 2 * cmul(psi, g)[0] + 3 * cpow(g, 2)[0],
                          cpow(psi, 2)[1] + 2 * cmul(psi, g)[1] + 3 * cpow(g, 2)[1])
                algebra.require(remainder == cmul(cpow(delta, 2), factor), "Exact complex fourth-power factorization")
                algebra.require(norm_squared(remainder) <= upper ** 2, "Exact complex R2 norm upper")
                checks += 1
    # Negative Gamma is a signed quantity, not a failed modulus radius.
    target = signed_raw_target(F(1, 2), F(1, 20), F(-1, 3),
                              [(F(2, 7), (F(1, 100), F(-1, 200), F(1, 20)))],
                              F(1), F(256, 625))
    for eta in (F(0), F(1, 4), F(1)):
        direct = (F(1, 2) + 2 * (F(1, 20) - eta / 3)
                  + 2 * F(2, 7) * (F(1, 100) - eta / 200 + eta ** 2 / 20)
                  - F(256, 625) * (1 + eta))
        algebra.require(algebra.evaluate(target, eta) == direct, "Signed Gamma/factor2/variable normalization")
        checks += 1
    passed, coefficients = algebra.bernstein_strict_negative((F(-1), F(1, 10), F(1, 10)), F(0), F(1), degree=2)
    algebra.require(passed and max(coefficients) < 0, "Exact degree2 Bernstein acceptance")
    checks += 1
    return checks


def main():
    output = Path(__file__).with_suffix(".json")
    algebra.require(not output.exists(), "Never overwrite signed ledger regression receipt")
    count = regressions()
    result = {"status": "EXACT_SIGNED_SECOND_ORDER_POLYNOMIAL_REGRESSIONS_ONLY", "date": "2026-10-08",
              "exact_regression_count": count,
              "identity": "psi^4-g^4-4g^3delta=delta^2(psi^2+2psi*g+3g^2)",
              "scope": "Proven affine radius and common signed Gamma inputs are required; frozen-p yields degree2 wholecell remainder, both signed Gamma coefficients retained, raw target has factor2 for both terms and exact variable denominator subtraction.",
              "CDF_proved": False, "whole_root_C4_proved": False}
    with output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({**result, "result": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
