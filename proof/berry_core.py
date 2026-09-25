"""Trusted numerical core for the Berry--Esseen 0.45 certificate.

The accompanying manuscript is *Toward a 0.45 Berry--Esseen Bound*.  Function
docstrings below identify the exact lemma or displayed equation implemented by
each bound.  Certificate files contain only exact rational parameters and a
compact, deterministic grid recipe.  This module reconstructs every grid and
recomputes every numerical bound with outward-rounded Arb arithmetic.

Any malformed datum, failed domain guard, non-finite value, or indeterminate
comparison is a certificate rejection.  Search heuristics and GPU calculations
are deliberately absent from this trusted module.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Sequence
import math
import re

try:
    from flint import acb, arb, ctx, fmpq
except ImportError as exc:  # pragma: no cover - deployment condition
    raise RuntimeError(
        "python-flint is required; install exactly python-flint==0.9.0"
    ) from exc

RAT_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?$")
ZERO_Q = Fraction(0, 1)
ONE_Q = Fraction(1, 1)
HALF_Q = Fraction(1, 2)
TARGET_Q = Fraction(9, 20)
RHO0_Q = Fraction(712569, 589000)
THETA_LO_Q = Fraction(3995895679, 1_000_000_000)
THETA_HI_Q = Fraction(3995895680, 1_000_000_000)
TWO_PI_LO_Q = Fraction(6283185307, 1_000_000_000)
TWO_PI_HI_Q = Fraction(6283185308, 1_000_000_000)


class CertificateError(ValueError):
    """Malformed data or a numerical statement that cannot be certified."""


def qstr(x: Fraction) -> str:
    """Canonical exact JSON representation of a rational number."""
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def parse_q(value: object, field: str = "rational") -> Fraction:
    """Parse a canonical integer or p/q string; JSON floats are forbidden."""
    if not isinstance(value, str) or RAT_RE.fullmatch(value) is None:
        raise CertificateError(
            f"{field}: expected canonical rational string, got {value!r}"
        )
    if "/" in value:
        p, q = value.split("/", 1)
        out = Fraction(int(p), int(q))
    else:
        out = Fraction(int(value), 1)
    if qstr(out) != value:
        raise CertificateError(
            f"{field}: non-canonical rational {value!r}; use {qstr(out)!r}"
        )
    return out


def A(x: Fraction | int) -> arb:
    """Exact Arb point from an integer or Fraction."""
    if isinstance(x, bool):
        raise TypeError("boolean is not a numerical proof datum")
    if isinstance(x, int):
        return arb(x)
    return arb(fmpq(x.numerator, x.denominator))


def ball(lo: Fraction, hi: Fraction) -> arb:
    """Arb ball containing the exact closed interval [lo,hi]."""
    if lo > hi:
        raise CertificateError(f"invalid interval [{qstr(lo)}, {qstr(hi)}]")
    mid = (lo + hi) / 2
    rad = (hi - lo) / 2
    return arb(
        fmpq(mid.numerator, mid.denominator),
        fmpq(rad.numerator, rad.denominator),
    )


def _finite(x: arb, label: str) -> arb:
    if not x.is_finite():
        raise CertificateError(f"non-finite Arb result in {label}: {x}")
    return x


def ub(x: arb) -> arb:
    """A finite point upper endpoint."""
    return _finite(x, "upper endpoint").upper()


def lb(x: arb) -> arb:
    """A finite point lower endpoint."""
    return _finite(x, "lower endpoint").lower()


def definitely_le(x: arb, y: arb) -> bool:
    """Return True only if x<=y is certified; ambiguous comparisons are False."""
    return bool(x <= y)


def exact_min(*xs: arb) -> arb:
    """Minimum of point upper bounds, rejecting an indeterminate comparison."""
    if not xs:
        raise ValueError("exact_min requires at least one argument")
    best = ub(xs[0])
    for x in xs[1:]:
        candidate = ub(x)
        if candidate <= best:
            best = candidate
        elif not (best <= candidate):
            raise CertificateError("indeterminate comparison between point bounds")
    return best


def lower_clamped_zero(x: arb) -> arb:
    """Clamp a lower endpoint at zero using ``psi >= 0`` stated after (13)."""
    y = lb(x)
    return y if y >= A(0) else A(0)


def upper_clamped_one(x: arb) -> arb:
    """Clamp an upper endpoint at one when the bounded quantity lies in [0,1]."""
    y = ub(x)
    return y if y <= A(1) else A(1)


@dataclass(frozen=True)
class Constants:
    pi: arb
    theta: arb
    kappa: arb


def _theta_function(x: arb) -> arb:
    return x * x + 2 * x * x.sin() + 6 * (x.cos() - 1)


def build_constants(precision_bits: int) -> Constants:
    """Certify ``theta_0`` and ``kappa`` as defined immediately before (11)."""
    if isinstance(precision_bits, bool) or not isinstance(precision_bits, int):
        raise CertificateError("precision_bits must be an integer")
    if not (96 <= precision_bits <= 16384):
        raise CertificateError("precision_bits must lie in [96,16384]")
    ctx.prec = precision_bits
    pi = arb.pi()
    theta = ball(THETA_LO_Q, THETA_HI_Q)

    flo = _theta_function(A(THETA_LO_Q))
    fhi = _theta_function(A(THETA_HI_Q))
    if not (ub(flo) < A(0) and lb(fhi) > A(0)):
        raise CertificateError("stored theta_0 bracket does not certify a sign change")
    if not (pi < A(THETA_LO_Q) and A(THETA_HI_Q) < 2 * pi):
        raise CertificateError("theta_0 bracket is not contained in (pi,2*pi)")
    if not (A(TWO_PI_LO_Q) < 2 * pi < A(TWO_PI_HI_Q)):
        raise CertificateError("stored rational bracket for 2*pi is invalid")

    # The uniqueness argument preceding (11) uses
    # F'(theta)=4*cos(theta/2)*(theta*cos(theta/2)-2*sin(theta/2))>0
    # on (pi,2*pi); hence the certified sign change isolates theta_0.
    kappa = (theta.cos() - 1 + theta * theta / 2) / (theta ** 3)
    if not (lb(kappa) > A(0)):
        raise CertificateError("failed to certify kappa>0")
    return Constants(pi=pi, theta=theta, kappa=kappa)


def stable_B_point(rho: Fraction, c: Constants) -> arb:
    """Upper enclosure of ``B(rho)`` from Lemma 4.1, equation (20)."""
    del c  # B(rho) in (20) does not depend on the remaining certified constants.
    if rho < ONE_Q:
        raise CertificateError("B(rho) called below rho=1")
    r = A(rho)
    # Cancellation-free identity (20) from Lemma 4.1.
    b2 = (r * r - 1) * (
        1 + (r * r + 9) / (r * (r * r + 8).sqrt() + 3)
    ) / 2
    if lb(b2) < A(0):
        raise CertificateError("stable B formula crosses the negative axis")
    return ub(b2.sqrt())


def geom_sum_upper(a: arb, c: arb, n: int) -> arb:
    """Positive ``O(log n)`` recursion of Lemma 4.2 for the power sum."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    a = ub(a)
    c = ub(c)
    if n == 1:
        return A(1)
    if n % 2 == 0:
        m = n // 2
        return ub(geom_sum_upper(a, c, m) * (a ** m + c ** m))
    # Odd-index recursion in Lemma 4.2.
    return ub(a ** (n - 1) + c * geom_sum_upper(a, c, n - 1))


def rational_grid(a: Fraction, b: Fraction, pieces: int) -> list[Fraction]:
    """Return the exact uniform partition of ``[a,b]`` into ``pieces`` parts."""
    if isinstance(pieces, bool) or not isinstance(pieces, int) or pieces < 1:
        raise CertificateError("grid pieces must be a positive integer")
    if a > b:
        raise CertificateError("grid interval endpoints are reversed")
    if a == b:
        return [a]
    return [a + (b - a) * Fraction(i, pieces) for i in range(pieces + 1)]


def concentrated_grid(
    a: Fraction,
    b: Fraction,
    pieces: int,
    power: int,
    *,
    n: int,
    q: Fraction,
    rho_mid: Fraction,
) -> list[Fraction]:
    """Reconstruct the exact compact grid recipe carried by a certificate.

    The union contains a polynomial mesh near the left endpoint, a uniform
    mesh, and (for ``n>=16``) a mesh in the natural variable
    ``u=q*sqrt(n)*s/(rho+1)``.  Certificate format v2 fixes the rational lower
    approximation to ``sqrt(n)``, so reconstruction is independent of any
    precomputed floating-point mesh.
    """
    if not (1 <= pieces <= 4096):
        raise CertificateError("grid pieces must lie in [1,4096]")
    if isinstance(power, bool) or not isinstance(power, int) or not (1 <= power <= 8):
        raise CertificateError("grid power must lie in [1,8]")
    if a > b:
        raise CertificateError("grid interval endpoints are reversed")
    if a == b:
        return [a]
    if power == 1 and n < 16:
        return rational_grid(a, b, pieces)

    points: set[Fraction] = {a, b}
    polynomial_pieces = max(8, pieces // 2)
    points.update(
        a + (b - a) * Fraction(i**power, polynomial_pieces**power)
        for i in range(polynomial_pieces + 1)
    )
    uniform_pieces = max(4, pieces // 8)
    points.update(rational_grid(a, b, uniform_pieces))

    if n >= 16:
        sqrt_denominator = 1_000_000
        sqrt_n_lower = Fraction(
            math.isqrt(n * sqrt_denominator * sqrt_denominator),
            sqrt_denominator,
        )
        scale = (rho_mid + 1) / (q * sqrt_n_lower)
        u_denominator = max(8, pieces // 4)
        for k in range(10 * u_denominator + 1):
            point = scale * Fraction(k, u_denominator)
            if a < point < b:
                points.add(point)
    return sorted(points)


def augmented_grid(
    a: Fraction,
    b: Fraction,
    pieces: int,
    q: Fraction,
    *,
    concentrated: bool,
    power: int,
    n: int,
    rho_mid: Fraction,
) -> list[Fraction]:
    """Add the exact guards around the piecewise definition (11) of ``psi``."""
    points = set(
        concentrated_grid(
            a,
            b,
            pieces,
            power,
            n=n,
            q=q,
            rho_mid=rho_mid,
        )
        if concentrated
        else rational_grid(a, b, pieces)
    )
    for guard in (THETA_LO_Q, THETA_HI_Q, TWO_PI_LO_Q, TWO_PI_HI_Q):
        cut = guard / q
        if a < cut < b:
            points.add(cut)
    return sorted(points)


def certificate_partitions(
    n: int,
    rho_lo: Fraction,
    rho_hi: Fraction,
    q: Fraction,
    t0: Fraction,
    eta: Fraction,
    lam: Fraction,
    pieces: int,
    power: int,
) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    """Reconstruct the three partitions in (18) from a format-v2 grid recipe."""
    rho_mid = (rho_lo + rho_hi) / 2
    first_pieces = 1 if eta == t0 else pieces
    third_pieces = 1 if lam == t0 else pieces
    first = augmented_grid(
        eta,
        t0,
        first_pieces,
        q,
        concentrated=True,
        power=power,
        n=n,
        rho_mid=rho_mid,
    )
    second = augmented_grid(
        t0,
        ONE_Q,
        pieces,
        q,
        concentrated=False,
        power=1,
        n=n,
        rho_mid=rho_mid,
    )
    third = augmented_grid(
        lam,
        t0,
        third_pieces,
        q,
        concentrated=True,
        power=power,
        n=n,
        rho_mid=rho_mid,
    )
    return first, second, third


def kernel_K_abs_upper(s_lo: Fraction, s_hi: Fraction, c: Constants) -> arb:
    """Bound ``|K|`` from (6), using (29)--(30) on a cell ending at one."""
    if not (ZERO_Q < s_lo <= s_hi <= ONE_Q):
        raise CertificateError("K cell must lie in (0,1]")
    if s_hi == ONE_Q:
        if s_lo < HALF_Q:
            raise CertificateError(
                "the final K cell ending at 1 must start at or above 1/2"
            )
        h = A(ONE_Q - s_lo)
        # Lemma 5.1, equation (29), and Lemma 5.2, equation (30), preserve
        # the removable endpoint value K(1)=0.
        shape = endpoint_kernel_shape_upper(ONE_Q - s_lo, c)
        return ub(h * shape / 2)

    s = ball(s_lo, s_hi)
    x = c.pi * s
    sinx = x.sin()
    if not (lb(sinx) > A(0)):
        raise CertificateError("sin(pi*s) not certified positive in a K cell")
    cotx = x.cos() / sinx
    re = (1 - s) / 2
    im = ((1 - s) * cotx + 1 / c.pi) / 2

    # Separate point upper bounds for |Re K| and |Im K| avoid dependency in
    # the interval evaluation of the Euclidean norm in equation (6).
    re_hi = ub(re.abs_upper())
    im_hi = ub(im.abs_upper())
    return ub((re_hi * re_hi + im_hi * im_hi).sqrt())


def regularized_cot_d_upper_point(
    s: Fraction, c: Constants, terms: int = 100
) -> arb:
    """Bound ``d(s)`` using Lemma 4.3, equations (21)--(23).

    For x=pi*s in (0,pi), use the positive partial-fraction expansion

        1/x-cot(x) = 2*x*sum_{k>=1} 1/(k^2*pi^2-x^2).

    The remainder after ``terms=m`` is bounded by

        2*x / (m * (pi^2 - x^2/(m+1)^2)),

    because sum_{k=m+1}^infinity 1/k^2 <= 1/m.  No subtraction of
    nearly equal singular quantities occurs.
    """
    if not (ZERO_Q < s < ONE_Q):
        raise CertificateError("regularized cotangent point must lie in (0,1)")
    if not isinstance(terms, int) or isinstance(terms, bool) or not (1 <= terms <= 10000):
        raise CertificateError("kernel series terms must lie in [1,10000]")

    x = c.pi * A(s)
    x2 = x * x
    pi2 = c.pi * c.pi
    total = A(0)
    for k in range(1, terms + 1):
        denominator = A(k * k) * pi2 - x2
        if not (lb(denominator) > A(0)):
            raise CertificateError("nonpositive denominator in cotangent series")
        total = total + 1 / denominator

    partial = 2 * x * total
    tail_denominator = pi2 - x2 / A((terms + 1) * (terms + 1))
    if not (lb(tail_denominator) > A(0)):
        raise CertificateError("nonpositive denominator in cotangent-series tail")
    tail = 2 * x / (A(terms) * tail_denominator)
    out = ub(partial + tail)
    if not (out >= A(0)):
        raise CertificateError("cotangent-series upper bound is negative")
    return out


def endpoint_kernel_shape_upper(
    h: Fraction, c: Constants, terms: int = 100
) -> arb:
    """Endpoint shape factor in Lemma 5.2, equation (30).

    For ``0<h<=1/2``, put ``d(h)=1/(pi*h)-cot(pi*h)`` as in (21).
    Lemma 4.3 and the endpoint identity (29) give, uniformly for
    ``0<=x<=h``,

        2 |K(1-x)| = x sqrt(1+d(x)^2)
                      <= x sqrt(1+d(h)^2).

    The returned factor is the square-root term on the right of (30).
    """
    if not (ZERO_Q < h <= HALF_Q):
        raise CertificateError("endpoint K scale must lie in (0,1/2]")
    d_hi = regularized_cot_d_upper_point(h, c, terms)
    return ub((1 + d_hi * d_hi).sqrt())


def second_endpoint_integral_upper(
    s_lo: Fraction, c: Constants, terms: int = 100
) -> arb:
    """Quadratic endpoint-tail bound of Theorem 5.3, equation (31).

    With ``h=1-s`` and ``H=1-s_lo``, Lemmas 5.1--5.2 and the bound
    ``M<=1`` in (17) imply

        integral_[s_lo,1] 2 |K(s)| M(Ts) ds
            <= integral_[0,H] h sqrt(1+d(H)^2) dh
            = H^2 sqrt(1+d(H)^2) / 2.

    Thus the contribution has the quadratic order recorded in Remark 5.4.
    """
    if not (HALF_Q <= s_lo < ONE_Q):
        raise CertificateError(
            "final second-integral cell must start in [1/2,1)"
        )
    h = ONE_Q - s_lo
    shape = endpoint_kernel_shape_upper(h, c, terms)
    return ub(A(h * h) * shape / 2)


def second_integral_upper(
    n: int,
    rho_lo: Fraction,
    rho_hi: Fraction,
    q: Fraction,
    grid: Sequence[Fraction],
    c: Constants,
    cotangent_terms: int = 100,
) -> arb:
    """Finite cutoff minimum from Lemma 5.5, equation (32).

    Each dyadic cutoff ``s*=1-2^-k``, ``k=1,...,14``, in the integration
    range gives an independent upper bound:

    * interval upper sums cover the prefix up to ``s*``;
    * ``second_endpoint_integral_upper`` covers the entire tail ``[s*,1]``.

    The implementation restricts ``s*`` to ``s*>=1/2``, as required when
    applying Theorem 5.3 with ``H=1-s*<=1/2``.  The certificate grid is
    refined by exact dyadic cutoffs, and the left endpoint of its final cell
    is retained as one additional candidate.
    """
    if len(grid) < 2 or grid[-1] != ONE_Q:
        raise CertificateError("second-integral grid must end at 1")

    dyadic_cutoffs = {
        ONE_Q - Fraction(1, 2**power) for power in range(1, 15)
    }
    refined = sorted(
        set(grid)
        | {cut for cut in dyadic_cutoffs if grid[0] < cut < ONE_Q}
    )
    candidate_cutoffs = set(dyadic_cutoffs)
    if grid[-2] >= HALF_Q:
        candidate_cutoffs.add(grid[-2])

    prefix = A(0)
    candidates: list[arb] = []
    for s_lo, s_hi in zip(refined, refined[1:]):
        if s_lo in candidate_cutoffs and s_lo >= HALF_Q:
            candidates.append(
                ub(
                    prefix
                    + second_endpoint_integral_upper(
                        s_lo, c, terms=cotangent_terms
                    )
                )
            )

        if s_hi == ONE_Q:
            break
        height = ub(
            2
            * kernel_K_abs_upper(s_lo, s_hi, c)
            * r_and_m_upper(n, rho_lo, rho_hi, q, s_lo, s_hi, c)[1]
        )
        prefix = ub(prefix + A(s_hi - s_lo) * height)

    if not candidates:
        raise CertificateError("no valid analytic second-integral tail cutoff")
    return exact_min(*candidates)


def kernel_L_abs_upper(
    s_lo: Fraction,
    s_hi: Fraction,
    c: Constants,
    series_terms: int = 100,
) -> arb:
    """Bound ``|L|`` by (24)--(25), with ``d`` bounded by equation (23).

    Put ``d(s)=1/(pi*s)-cot(pi*s)`` as in (21).  Lemma 4.3 gives

        2|L(s)|=(1-s)*sqrt(1+d(s)^2)
          <= (1-s_lo)*sqrt(1+d(s_hi)^2).

    Equation (23) supplies the finite upper bound for ``d(s_hi)``.
    """
    if not (ZERO_Q < s_lo <= s_hi < ONE_Q):
        raise CertificateError("regular L cell must lie strictly inside (0,1)")
    d_hi = regularized_cot_d_upper_point(s_hi, c, series_terms)
    factor = A(ONE_Q - s_lo) / 2
    return ub(factor * (1 + d_hi * d_hi).sqrt())


def psi_lower(q: Fraction, s_lo: Fraction, s_hi: Fraction, c: Constants) -> arb:
    """Lower bound for ``psi`` defined in (11) and used in (13).

    The statement ``0<=psi<=2`` immediately after (13) justifies the lower
    bound zero on a cell crossing ``theta_0`` or ``2*pi``.  Exact rational
    guards ensure that a branch formula from (11) is used only on its domain.
    """
    z_lo_q = q * s_lo
    z_hi_q = q * s_hi
    z = A(q) * ball(s_lo, s_hi)

    if z_hi_q <= THETA_LO_Q:
        return lower_clamped_zero(z * z / 2 - c.kappa * z ** 3)
    if z_lo_q >= THETA_HI_Q and z_hi_q <= TWO_PI_LO_Q:
        return lower_clamped_zero(1 - z.cos())
    if z_lo_q >= TWO_PI_HI_Q:
        return A(0)
    return A(0)


def half_power_upper(base_hi: arb, n: int) -> arb:
    """Evaluate the exponent ``n/2`` in (13) for a base in ``[0,1]``."""
    b = upper_clamped_one(base_hi)
    if not (lb(b) >= A(0)):
        raise CertificateError("negative upper base in half_power_upper")
    if n % 2 == 0:
        return ub(b ** (n // 2))
    return ub((b ** n).sqrt())


def rad_gauss_diff_upper(
    n: int,
    rho_lo: Fraction,
    rho_hi: Fraction,
    q: Fraction,
    s_lo: Fraction,
    s_hi: Fraction,
    c: Constants,
) -> arb:
    """Lemma 4.5 and Corollary 4.6, equations (26)--(28).

    Here ``u=q*s/(rho+1)``.  Direct interval subtraction is catastrophically
    wide near zero because the two functions are almost identical.  Whenever
    the whole cell lies in ``0<=u<pi/2``, use the exact identity

        cos(u)^n = exp(-n*u^2/2) * exp(-n*h(u)),
        h(u) = -log(cos(u)) - u^2/2 >= 0.

    On that interval ``h`` is increasing and the Gaussian is decreasing, so

        |cos(u)^n-exp(-n*u^2/2)|
          <= exp(-n*u_lo^2/2) * (1-exp(-n*h(u_hi))).

    The final factor is also bounded by ``min(1,n*h(u_hi))``.  All endpoint
    values are exact rationals converted to Arb points.  Outside the certified
    positive-cosine region, direct interval evaluation supplies the fallback.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise CertificateError("n must be a positive integer")

    u_lo_q = q * s_lo / (rho_hi + 1)
    u_hi_q = q * s_hi / (rho_lo + 1)
    if u_lo_q < ZERO_Q:
        raise CertificateError("negative u endpoint in Gaussian-difference bound")

    u_hi = A(u_hi_q)
    if u_hi < c.pi / 2:
        cos_hi = u_hi.cos()
        if lb(cos_hi) > A(0):
            # Point evaluation preserves the nonnegative factorization (27).
            h_hi = ub(A(0) - cos_hi.log() - u_hi * u_hi / 2)
            if h_hi >= A(0):
                x_hi = ub(A(n) * h_hi)
                exp_bound = ub(1 - (A(0) - x_hi).exp())
                one_minus_hi = exact_min(A(1), x_hi, exp_bound)
                u_lo = A(u_lo_q)
                gaussian_hi = ub((A(0) - A(n) * u_lo * u_lo / 2).exp())
                return ub(gaussian_hi * one_minus_hi)

    # Direct interval form of the difference in (14) for cells not covered by
    # Corollary 4.6 or with an indeterminate positive-cosine comparison.
    rho = ball(rho_lo, rho_hi)
    s = ball(s_lo, s_hi)
    u = A(q) * s / (rho + 1)
    t = A(q) * arb(n).sqrt() * s / (rho + 1)
    return ub(((u.cos() ** n) - (A(0) - t * t / 2).exp()).abs_upper())


def r_and_m_upper(
    n: int,
    rho_lo: Fraction,
    rho_hi: Fraction,
    q: Fraction,
    s_lo: Fraction,
    s_hi: Fraction,
    c: Constants,
) -> tuple[arb, arb]:
    """Implement ``D, R, M_R, M_P, M`` from equations (8)--(17).

    Lemmas 4.1--4.2 and Corollary 4.6 supply the stable cellwise evaluations.
    """
    rho = ball(rho_lo, rho_hi)
    s = ball(s_lo, s_hi)
    denom = rho + 1
    u = A(q) * s / denom

    cosu = u.cos()
    rad_gauss_diff = rad_gauss_diff_upper(
        n, rho_lo, rho_hi, q, s_lo, s_hi, c
    )

    c_hi = upper_clamped_one(cosu.abs_upper())
    b_hi = stable_B_point(rho_hi, c)  # Monotonicity is part of Lemma 4.1.
    delta_hi = ub(b_hi * (u.abs_upper() ** 3) / 6)
    a_hi = exact_min(A(1), c_hi + delta_hi)
    d_pow_hi = ub(delta_hi * geom_sum_upper(a_hi, c_hi, n))
    d_hi = exact_min(A(2), n * delta_hi, d_pow_hi)

    r_hi = exact_min(A(2), rad_gauss_diff + d_hi)
    mr_hi = exact_min(A(1), c_hi ** n + d_hi)

    p_lo = psi_lower(q, s_lo, s_hi, c)
    # In (13), psi>=0 and the base is largest at rho=rho_hi.
    base_hi = ub(1 - 2 * p_lo / (A(rho_hi) + 1) ** 2)
    mp_hi = half_power_upper(base_hi, n)
    m_hi = exact_min(mr_hi, mp_hi)
    return r_hi, m_hi


def third_integrand_upper(
    n: int,
    rho_lo: Fraction,
    rho_hi: Fraction,
    q: Fraction,
    s_lo: Fraction,
    s_hi: Fraction,
    c: Constants,
    regularized_cot_terms: int = 100,
) -> arb:
    """Bound the third integrand in (18) using Corollary 4.4, equation (25)."""
    l_hi = kernel_L_abs_upper(s_lo, s_hi, c, regularized_cot_terms)
    rho = ball(rho_lo, rho_hi)
    s = ball(s_lo, s_hi)
    t = A(q) * arb(n).sqrt() * s / (rho + 1)
    e_hi = ub((A(0) - t * t / 2).exp())
    return ub(2 * l_hi * e_hi)


def e1_upper(x: arb) -> arb:
    """Bound ``E1(x)`` from the identity following (7), for use in (18)."""
    if not (lb(x) > A(0)):
        raise CertificateError("E1 argument is not certified positive")
    z = acb(x).expint(1)
    if not z.is_finite():
        raise CertificateError("non-finite exponential integral")
    if not z.imag.contains(0):
        raise CertificateError("E1 unexpectedly has a nonzero imaginary enclosure")
    return ub(z.real)


def upper_sum(grid: Sequence[Fraction], evaluator: Callable[[Fraction, Fraction], arb]) -> arb:
    """Upper Riemann sum as specified in Section 6 before Proposition 6.3."""
    total = A(0)
    for a, b in zip(grid, grid[1:]):
        height = ub(evaluator(a, b))
        total = total + A(b - a) * height
    return ub(total)


@dataclass(frozen=True)
class CellResult:
    local_zero: arb
    first_proper: arb
    second: arb
    third_zero: arb
    third_proper: arb
    tail: arb
    U_upper: arb
    ratio_upper: arb


def evaluate_cell(
    n: int,
    cell: dict,
    c: Constants,
    regularized_cot_terms: int = 100,
) -> CellResult:
    """Verify one cell under Proposition 6.3, equation (35).

    The components reconstruct the functional (18): Lemma 6.1, equation (33),
    handles the first near-zero interval; Theorem 5.3, equation (31), and
    Lemma 5.5, equation (32), handle the second integral; and Lemma 6.2,
    equation (34), handles the third near-zero interval.  The remaining compact
    intervals use the upper Riemann sums specified before Proposition 6.3.
    The returned ``ratio_upper`` is the left-hand side of (35).
    """
    if not isinstance(n, int) or isinstance(n, bool) or not (2 <= n <= 8123):
        raise CertificateError(f"n={n!r} is outside [2,8123]")
    if not isinstance(cell, dict):
        raise CertificateError("cell must be an object")
    rho_pair = cell.get("rho")
    if not isinstance(rho_pair, list) or len(rho_pair) != 2:
        raise CertificateError("cell.rho must be a two-element list")
    rlo = parse_q(rho_pair[0], "rho[0]")
    rhi = parse_q(rho_pair[1], "rho[1]")
    if not (ONE_Q <= rlo < rhi <= RHO0_Q):
        raise CertificateError("rho cell must be nondegenerate in [1,rho0]")

    q = parse_q(cell.get("q"), "q")
    t0 = parse_q(cell.get("t0"), "t0")
    eta = parse_q(cell.get("eta"), "eta")
    lam = parse_q(cell.get("lambda"), "lambda")
    if q <= ZERO_Q:
        raise CertificateError("q must be positive")
    # Lemma 6.2 and Section 6 require lambda<=1/2 in addition to lambda<=t0.
    if not (ZERO_Q < lam <= min(t0, HALF_Q) and t0 < ONE_Q):
        raise CertificateError("require 0<lambda<=min(t0,1/2) and t0<1")
    if not (ZERO_Q < eta <= min(t0, HALF_Q)):
        raise CertificateError("require 0<eta<=min(t0,1/2)")
    if q * eta > rlo + 1:
        raise CertificateError("endpoint condition q*eta/(rho+1)<=1 fails")

    grid = cell.get("grid")
    if not isinstance(grid, dict) or set(grid) != {"pieces", "power"}:
        raise CertificateError("cell.grid must contain exactly pieces and power")
    pieces = grid["pieces"]
    power = grid["power"]
    if isinstance(pieces, bool) or not isinstance(pieces, int) or not (1 <= pieces <= 4096):
        raise CertificateError("cell.grid.pieces must lie in [1,4096]")
    if isinstance(power, bool) or not isinstance(power, int) or not (1 <= power <= 8):
        raise CertificateError("cell.grid.power must lie in [1,8]")
    p1, p2, p3 = certificate_partitions(
        n, rlo, rhi, q, t0, eta, lam, pieces, power
    )

    sqrt_n = arb(n).sqrt()
    b_hi = stable_B_point(rhi, c)
    t_hi = ub(A(q) * sqrt_n / (A(rlo) + 1))
    local_zero = ub(
        b_hi * t_hi ** 3 * A(eta) ** 3 / (9 * sqrt_n)
        + t_hi ** 4 * A(eta) ** 4 / (12 * n)
    )

    # Proper part of the first integral in (18); (14) and (17) provide R.
    first_proper = upper_sum(
        p1,
        lambda a, b: 2
        * kernel_K_abs_upper(a, b, c)
        * r_and_m_upper(n, rlo, rhi, q, a, b, c)[0],
    )
    # Second integral in (18), bounded by Theorem 5.3 and Lemma 5.5.
    second = second_integral_upper(
        n, rlo, rhi, q, p2, c, cotangent_terms=regularized_cot_terms
    )

    # Lemma 6.2, equation (34).
    third_zero = ub(A(lam) * (1 + 4 / (c.pi * c.pi)).sqrt())
    # Proper part of the third integral in (18), using Corollary 4.4.
    third_proper = upper_sum(
        p3,
        lambda a, b: third_integrand_upper(
            n, rlo, rhi, q, a, b, c, regularized_cot_terms
        ),
    )

    # The E1 identity following (7) and the monotonicity invoked in Section 6:
    # T is smallest at rho=rhi, so use a lower bound for x=T^2*t0^2/2.
    t_min_lo = lb(A(q) * sqrt_n / (A(rhi) + 1))
    x_min_lo = lb(t_min_lo * t_min_lo * A(t0) ** 2 / 2)
    tail = ub(e1_upper(x_min_lo) / (2 * c.pi))

    U = ub(local_zero + first_proper + second + third_zero + third_proper + tail)
    ratio = ub(sqrt_n * U / A(rlo))
    return CellResult(
        local_zero=local_zero,
        first_proper=first_proper,
        second=second,
        third_zero=third_zero,
        third_proper=third_proper,
        tail=tail,
        U_upper=U,
        ratio_upper=ratio,
    )


def self_test_global_reductions(c: Constants) -> None:
    """Certify the threshold inequality in Lemma 2.2 and Appendix A."""
    ce = (arb(10).sqrt() + 3) / (6 * (2 * c.pi).sqrt())
    rhs = ce + 3 * A(RHO0_Q) / arb(8124).sqrt()
    if not (ub(rhs) < lb(A(TARGET_Q))):
        raise CertificateError(
            "failed to certify C_E+3*rho0/sqrt(8124)<9/20"
        )


def fmt_upper(x: arb, digits: int = 18) -> str:
    """Human-readable non-proof output; never parsed back as a bound."""
    return ub(x).str(digits, radius=False)
