#!/usr/bin/env python3
"""Exact symbolic verification for the n^{-2} lattice correction.

The script reconstructs the fifth-order beta-saddle coefficient from the
recursion in the accompanying note and verifies every displayed closed form
by exact SymPy simplification.  No floating-point value enters an assertion.
"""
from __future__ import annotations

import sympy as sp


def gaussian_full_normalized(poly: sp.Poly, y: sp.Symbol) -> sp.Expr:
    """(2*pi)^(-1/2) integral_R exp(-y^2/2) poly(y) dy."""
    out = sp.Integer(0)
    for (degree,), coeff in poly.terms():
        if degree % 2 == 0:
            moment = sp.Integer(1) if degree == 0 else sp.factorial2(degree - 1)
            out += coeff * moment
    return sp.cancel(out)


def gaussian_negative_half_odd(poly: sp.Poly, y: sp.Symbol) -> sp.Expr:
    """Integral_{-infty}^0 exp(-y^2/2) poly(y) dy for an odd polynomial."""
    out = sp.Integer(0)
    for (degree,), coeff in poly.terms():
        if degree % 2 == 0:
            if coeff != 0:
                raise AssertionError("Expected an odd polynomial")
            continue
        j = (degree - 1) // 2
        out -= coeff * 2**j * sp.factorial(j)
    return sp.cancel(out)


def main() -> None:
    p, eta, y = sp.symbols("p eta y")
    q = 1 - p
    r2 = p * q
    D = p**2 + q**2

    # We use tilde ell_j = r^j ell_j.  This removes all square roots and
    # keeps the coefficient extraction in Q[p, eta, y].
    ell_tilde: dict[int, sp.Poly] = {}
    for j in range(1, 6):
        c_tilde = (
            q * (-1) ** (j + 3) * p ** (j + 2) - p * q ** (j + 2)
        ) / (sp.Integer(j + 2) * r2)
        d_tilde = (
            -(eta + 1) * (-1) ** (j + 1) * p**j - eta * q**j
        ) / sp.Integer(j)
        ell_tilde[j] = sp.Poly(c_tilde * y ** (j + 2) + d_tilde * y**j, y)

    E_tilde: dict[int, sp.Poly] = {0: sp.Poly(1, y)}
    for m in range(1, 6):
        accumulator = sp.Poly(0, y)
        for j in range(1, m + 1):
            accumulator += j * ell_tilde[j] * E_tilde[m - j]
        E_tilde[m] = sp.Poly(accumulator.as_expr() / m, y)
        assert sp.simplify(E_tilde[m].as_expr().subs(y, -y) - (-1) ** m * E_tilde[m].as_expr()) == 0

    A1 = gaussian_negative_half_odd(E_tilde[1], y)
    A3 = gaussian_negative_half_odd(E_tilde[3], y)
    A5 = gaussian_negative_half_odd(E_tilde[5], y)
    delta2 = gaussian_full_normalized(E_tilde[2], y)
    delta4 = gaussian_full_normalized(E_tilde[4], y)

    expected_A1 = eta + (2 - p) / 3
    expected_delta2 = (6 * eta**2 + 6 * eta + p**2 - p + 1) / 12
    expected_A3 = (
        45 * eta**3
        + 45 * eta**2 * p
        + 45 * eta**2
        + 45 * eta * p
        - 4 * p**3
        + 6 * p**2
        + 6 * p
        - 4
    ) / 135
    expected_delta4 = (
        36 * eta**4
        + 96 * eta**3 * p
        + 24 * eta**3
        + 12 * eta**2 * p**2
        + 132 * eta**2 * p
        - 24 * eta**2
        + 12 * eta * p**2
        + 36 * eta * p
        - 12 * eta
        + p**4
        - 2 * p**3
        + 3 * p**2
        - 2 * p
        + 1
    ) / 288
    expected_A5 = (
        189 * eta**5
        + 945 * eta**4 * p
        + 630 * eta**3 * p**2
        + 1260 * eta**3 * p
        - 315 * eta**3
        - 42 * eta**2 * p**3
        + 1008 * eta**2 * p**2
        + 63 * eta**2 * p
        - 42 * eta**2
        - 42 * eta * p**3
        + 378 * eta * p**2
        - 252 * eta * p
        + 84 * eta
        + 8 * p**5
        - 20 * p**4
        + 8 * p**3
        + 8 * p**2
        - 20 * p
        + 8
    ) / 2835

    assert sp.cancel(A1 - expected_A1) == 0
    assert sp.cancel(delta2 - expected_delta2) == 0
    assert sp.cancel(A3 - expected_A3) == 0
    assert sp.cancel(delta4 - expected_delta4) == 0
    assert sp.cancel(A5 - expected_A5) == 0

    # The bracket is r^5 times the fifth-order cdf coefficient before the
    # outer factor phi_0, including subtraction of the normal cdf term.
    bracket = sp.cancel(
        A5 - A3 * delta2 + A1 * (delta2**2 - delta4) - eta**5 / 40
    )

    P = (
        1260 * (4 - 5 * p) * eta**4
        + 420 * (25 * p**2 - 55 * p + 28) * eta**3
        + 1260 * (-p**3 + 14 * p**2 - 21 * p + 9) * eta**2
        + 21
        * (5 * p**4 - 70 * p**3 + 355 * p**2 - 470 * p + 189)
        * eta
        + 5
        * (25 * p**5 - 52 * p**4 - 17 * p**3 + 88 * p**2 - 115 * p + 46)
    )
    H_over_phi0 = sp.cancel(bracket / (D * r2**2))
    expected_H_over_phi0 = sp.cancel(P / (30240 * p**2 * q**2 * D))
    assert sp.cancel(H_over_phi0 - expected_H_over_phi0) == 0
    assert sp.Poly(P, eta).degree() == 4  # exact cancellation of eta^5

    sqrt10 = sp.sqrt(10)
    p_star = (4 - sqrt10) / 2
    eta_star = -(20 + sqrt10) / 72
    phi0 = 1 / sp.sqrt(2 * sp.pi)

    G = phi0 * (2 - p) / (3 * D)
    F = -phi0 * (
        270 * q * eta**2
        + 45 * (p**2 - 7 * p + 5) * eta
        + p**3
        + 21 * p**2
        - 69 * p
        + 46
    ) / (540 * p * q * D)
    H = phi0 * expected_H_over_phi0

    H_star = sp.simplify(H.subs({p: p_star, eta: eta_star}))
    Fp_star = sp.simplify(sp.diff(F, p).subs({p: p_star, eta: eta_star}))
    Gpp_star = sp.simplify(sp.diff(G, p, 2).subs(p, p_star))
    delta0 = sp.simplify(-Fp_star / Gpp_star)
    Q_star = sp.simplify(H_star - Fp_star**2 / (2 * Gpp_star))
    A2 = sp.simplify(-Gpp_star / 2)
    kappa2 = sp.simplify(-Q_star)

    expected_H_star = -phi0 * (653866157 + 211759711 * sqrt10) / 25395793920
    expected_Fp_star = -phi0 * (1483 + 463 * sqrt10) / 19440
    expected_Gpp_star = -phi0 * (60 + 19 * sqrt10) / 15
    expected_delta0 = (1010 - 397 * sqrt10) / 12960
    expected_Q_star = -phi0 * (
        3183580225 + 1028276063 * sqrt10
    ) / 126978969600

    assert sp.simplify(H_star - expected_H_star) == 0
    assert sp.simplify(Fp_star - expected_Fp_star) == 0
    assert sp.simplify(Gpp_star - expected_Gpp_star) == 0
    assert sp.simplify(delta0 - expected_delta0) == 0
    assert sp.simplify(Q_star - expected_Q_star) == 0
    assert sp.simplify(A2 + expected_Gpp_star / 2) == 0
    assert sp.simplify(kappa2 + expected_Q_star) == 0
    assert sp.simplify(Gpp_star < 0) is sp.true
    assert sp.simplify(Q_star < 0) is sp.true
    assert sp.simplify(A2 > 0) is sp.true
    assert sp.simplify(kappa2 > 0) is sp.true

    # Complete-square identity for the lattice variable u.
    u = sp.symbols("u")
    lattice_quadratic = H_star + Fp_star * u + Gpp_star * u**2 / 2
    completed = Q_star + Gpp_star * (u - delta0) ** 2 / 2
    assert sp.simplify(lattice_quadratic - completed) == 0

    print("PASS: exact fifth-order saddle coefficient and lattice constants verified")
    print("H(p,eta)/phi0 = P/(30240 p^2 q^2 (p^2+q^2))")
    print("degree_eta(P) =", sp.Poly(P, eta).degree())
    for name, value in (
        ("p_star", p_star),
        ("eta_star", eta_star),
        ("H_star", H_star),
        ("F_p_star", Fp_star),
        ("G_pp_star", Gpp_star),
        ("delta_0", delta0),
        ("A_2", A2),
        ("kappa_2", kappa2),
        ("lower_limit_coefficient", -kappa2 - A2 / 4),
    ):
        print(f"{name:24s} = {sp.N(value, 25)}")


if __name__ == "__main__":
    main()
