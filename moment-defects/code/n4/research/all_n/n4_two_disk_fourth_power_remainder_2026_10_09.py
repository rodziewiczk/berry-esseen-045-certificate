"""Universal two-disk fourth-power remainder, pure scalar algebra ONLY.

For complex g,psi with |g|<=A<=1, |psi|<=1 and |psi-g|<=E, this module
gives a uniform bound for R2=psi^4-g^4-4*g^3*(psi-g). No CF, law,
quadrature, numerical receipt, optimizer, resource guard or CDF producer
is called. The disk/radius premises are mathematical inputs, not verified
by a field name, type, source hash, or sampled test. All arithmetic below
is exact Fraction, including outward rational square-root brackets.

Derivation: two disks, not the older integral-triangle cap
---------------------------------------------------------
Rotate g=a>=0 and delta=psi-g=x+iy, with r=|delta| and s=r^2. Exactly,

 R2=delta^2*(6*a^2+4*a*delta+delta^2),
 |R2|^2=s^2*F(a,s,x),
 F=36*a^4+4*a^2*s+s^2+8*a*x*(6*a^2+s)+24*a^2*x^2.

For fixed a,r>0 the feasible real interval is
 [-r,min(r,(1-a^2-s)/(2a))], with r<=1+a. F is convex in x.
Its maximum is at a negative collinear endpoint or at the other endpoint,
which is either positive collinear or the unit-circle boundary |psi|=1.
For a=0 the exact remainder is r^4 and the same final envelopes cover it.

The positive endpoint has a<=min(A,1-r), r<=1. Its largest remainder at
fixed r is r^2*(6*m^2+4*m*r+r^2), m=min(A,1-r). This increases in r:
for r<=1-A its positive-coefficient form increases; thereafter it equals
r^2*(6-8*r+3*r^2), whose derivative is 12*r*(1-r)^2. Thus its whole
radius maximum is at r=min(E,1).

The negative endpoint has max(0,r-1)<=a<=A. The positive factor
6*a^2-4*a*r+r^2 is convex in a, so its maximum is at an endpoint.
The a=A branch r^2*(6*A^2-4*A*r+r^2) increases in r, with derivative
4*r*(r^2-3*A*r+3*A^2)>=0. The lower-a branch is r^4 for r<=1,
and r^2*(3*r^2-8*r+6) for r>=1, again increasing because its latter
derivative is 12*r*(r-1)^2. Both are evaluated at r=min(E,1+A).

On the unit circle |1-a|<=r<=1+a and

 F=18*a^4+12*a^2+6-(12*a^2+8)*s+3*s^2.

This is convex in a^2 on |1-r|<=a<=A. Its lower-a endpoint is one of
the collinear branches already covered. The remaining a=A branch is

 Q_A(s)=s^2*[18*A^4+12*A^2+6-(12*A^2+8)*s+3*s^2],
 s in [(1-A)^2,min(E^2,(1+A)^2)].

For A>0 its only interior local maximum is
s_-=(3*A^2+2-A*sqrt(4-3*A^2))/2; the other stationary point s_+
is a local minimum. Hence endpoints and s_- suffice. For A=0 the
branch is degenerate and endpoint evaluation still suffices. The code
brackets the one radical outwards and bounds Q on that tiny critical
interval by C*s_hi^2-D*s_lo^3+3*s_hi^4. One further outward sqrt
converts the squared remainder upper. NO sampled maximization is used.

Finally the scalar minimum with TWO other independently complete bounds
is safe: the existing cap E^2*(p^2+2*p*A+3*A^2), p=min(1,A+E), and the
already known integral/unit-disk cap U*(4*A^2+2-U), U=min(E^2,2*A^2+1).
The latter is old constraints note (13), not a newly proved idea here.
The new lens envelope can be strictly smaller: A=E=1 gives sqrt(19)
(up to outward rounding), instead of the old disk cap5 or primary cap6.

Scope and genuine limitations
-----------------------------
A,E frozen uniformly on a WHOLE closed eta cell yield a CONSTANT R2
model valid on that entire cell. It may be selected against another
ENTIRE polynomial model; NEVER minimize coefficients or extrapolate a
pointwise branch. A signed/common linear transfer can add this R2 norm
bound with |kernel|. Pure ABS transfer may use the complete scalar min
of its old fourth-power telescope and 4*A^3*E+this remainder bound.
That does NOT by itself restore a signed/common linear calculation.

In fact the full ABS telescope is SHARP using ONLY these scalar premises
when E<=1-A: g=A and psi=A+E are admissible and realize
 |psi^4-g^4|=E*(p^3+p^2*A+p*A^2+A^3), p=A+E.
This is a rigorous lower limit on a UNIVERSAL SCALAR majorant, NOT an
obstruction from an actual standardized law. A per-frequency scalar
witness need not belong to the SAME characteristic function across q.
Numerical failed majorants/receipt fields alone prove no physical lower
floor, no contradiction, and no impossibility of the full C4 theorem.

The real-kernel helper exposes the EXACT signed quartic in x,y. To use
that directional information, a future consumer must keep fresh kernel
and g phases and prove a polynomial upper on the lens. With only kernel
modulus information no universal directional improvement is available:
its phase can be chosen to align with the remainder. No directional
continuum inequality or CDF certificate is claimed by this helper.

No import-time computation, file writes, CLI producer, numeric receipt,
or old CF import. Dormant exact scalar tests are not run on import.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import isqrt

SCALE = 10 ** 40


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact(value):
    require(type(value) in (F, int), "Exact Fraction/int inputs only; no bool/float")
    return F(value)


def root_interval(value, scale=SCALE):
    value = exact(value)
    require(value >= 0 and type(scale) is int and scale > 0,
            "Nonnegative exact square and positive integer root scale")
    lo = isqrt(value.numerator * scale * scale // value.denominator)
    hi = lo if F(lo, scale) ** 2 == value else lo + 1
    require(F(lo, scale) ** 2 <= value <= F(hi, scale) ** 2,
            "Exact outward rational square-root bracket")
    return F(lo, scale), F(hi, scale)


def unit_circle_squared_remainder(a, s):
    a, s = map(exact, (a, s))
    return s ** 2 * (18 * a ** 4 + 12 * a ** 2 + 6
                    - (12 * a ** 2 + 8) * s + 3 * s ** 2)


def two_disk_remainder_upper(a_upper, radius_upper, scale=SCALE):
    """Uniform |R2| for BOTH disks and whole-cell frozen scalar A,E.

    The result never proves its analytic disk/radius premises or a CDF.
    Exact radicals are bracketed freshly here; no stored bounds accepted.
    """
    A, E = map(exact, (a_upper, radius_upper))
    require(0 <= A <= 1 and E >= 0 and type(scale) is int and scale > 0,
            "Proven reference modulus and nonnegative common radius")
    rp = min(E, F(1))
    mp = min(A, 1 - rp)
    positive = rp ** 2 * (6 * mp ** 2 + 4 * mp * rp + rp ** 2)
    rn = min(E, 1 + A)
    negative_A = rn ** 2 * (6 * A ** 2 - 4 * A * rn + rn ** 2)
    negative_low = rn ** 4 if rn <= 1 else rn ** 2 * (3 * rn ** 2 - 8 * rn + 6)
    negative = max(negative_A, negative_low)
    s_lo, s_hi = (1 - A) ** 2, min(E ** 2, (1 + A) ** 2)
    circle_squared, critical = F(0), None
    if s_lo <= s_hi:
        endpoints = (unit_circle_squared_remainder(A, s_lo),
                     unit_circle_squared_remainder(A, s_hi))
        require(min(endpoints) >= 0, "Squared unit-circle endpoint norms")
        circle_squared = max(endpoints)
        root_lo, root_hi = root_interval(4 - 3 * A ** 2, scale)
        critical_lo = (3 * A ** 2 + 2 - A * root_hi) / 2
        critical_hi = (3 * A ** 2 + 2 - A * root_lo) / 2
        if critical_lo <= s_hi and s_lo <= critical_hi:
            lo, hi = max(s_lo, critical_lo), min(s_hi, critical_hi)
            C, D = 18 * A ** 4 + 12 * A ** 2 + 6, 12 * A ** 2 + 8
            critical_upper = C * hi ** 2 - D * lo ** 3 + 3 * hi ** 4
            require(0 <= lo <= hi and critical_upper >= 0,
                    "Whole critical-point interval upper, not a sampled stationary value")
            circle_squared = max(circle_squared, critical_upper)
            critical = {"s_minus_interval": (critical_lo, critical_hi),
                        "clipped_interval": (lo, hi),
                        "squared_remainder_upper": critical_upper}
    circle = root_interval(circle_squared, scale)[1]
    lens = max(positive, negative, circle)
    p = min(F(1), A + E)
    primary = E ** 2 * (p ** 2 + 2 * p * A + 3 * A ** 2)
    U = min(E ** 2, 2 * A ** 2 + 1)
    old_disk = U * (4 * A ** 2 + 2 - U)
    upper = min(lens, primary, old_disk)
    require(min(positive, negative, circle, lens, primary, old_disk, upper) >= 0,
            "Independent COMPLETE nonnegative scalar models")
    return {"remainder_upper": upper,
        "new_two_disk_lens_upper": lens,
        "existing_primary_cap_upper": primary,
        "existing_integral_disk_upper": old_disk,
        "positive_collinear_upper": positive,
        "negative_collinear_upper": negative,
        "unit_circle_squared_upper": circle_squared,
        "unit_circle_norm_upper": circle,
        "unit_circle_s_interval": (s_lo, s_hi) if s_lo <= s_hi else None,
        "critical_interval": critical,
        "reference_modulus_upper": A, "radius_upper": E, "root_scale": scale,
        "whole_cell_uniform_scalar_model": True,
        "CDF_or_law_realizability_proved": False}


def fourth_power_absolute_upper(a_upper, radius_upper, scale=SCALE):
    """Intersection of TWO complete ABS bounds; never a coefficient minimum."""
    A, E = map(exact, (a_upper, radius_upper))
    result = two_disk_remainder_upper(A, E, scale)
    p = min(F(1), A + E)
    telescope = E * (p ** 3 + p ** 2 * A + p * A ** 2 + A ** 3)
    linear_plus_R2 = 4 * A ** 3 * E + result["remainder_upper"]
    return {"absolute_fourth_power_difference_upper": min(telescope, linear_plus_R2),
        "complete_telescope_upper": telescope,
        "complete_triangle_linear_plus_R2_upper": linear_plus_R2,
        "R2": result, "signed_common_linear_information_used": False}


def rotated_remainder_components(a, x, y):
    """Exact signed quartic for g=a>=0 and delta=x+iy; NOT an upper bound."""
    a, x, y = map(exact, (a, x, y))
    require(a >= 0, "Nonnegative real rotated reference modulus")
    s = x ** 2 + y ** 2
    real = (8 * x ** 4 + 16 * a * x ** 3 + (12 * a ** 2 - 8 * s) * x ** 2
            - 12 * a * s * x + s ** 2 - 6 * a ** 2 * s)
    imag = 4 * y * (3 * a ** 2 * x + a * (4 * x ** 2 - s) + x * (2 * x ** 2 - s))
    return real, imag


def real_kernel_remainder(a, x, y, kernel_real, kernel_imag):
    """Exact directional expression only; no lens supremum/CDF inferred."""
    real, imag = rotated_remainder_components(a, x, y)
    kr, ki = map(exact, (kernel_real, kernel_imag))
    return kr * real - ki * imag


def self_tests():
    """DORMANT exact algebra tests; no optimizer, CF, files or producer."""
    checks = 0
    def cmul(z, w):
        return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]
    def power(z, n):
        result = (F(1), F(0))
        for _ in range(n):
            result = cmul(result, z)
        return result
    for A in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
        for a in (F(0), A / 2, A):
            for psi in ((F(0), F(0)), (F(1), F(0)), (F(-1), F(0)),
                        (F(0), F(1)), (F(3, 5), F(4, 5)), (F(1, 3), F(-1, 3))):
                x, y = psi[0] - a, psi[1]
                E = root_interval(x ** 2 + y ** 2, 10 ** 6)[1]
                cap = two_disk_remainder_upper(A, E, 10 ** 6)
                psi4 = power(psi, 4)
                expected = (psi4[0] - a ** 4 - 4 * a ** 3 * x,
                            psi4[1] - 4 * a ** 3 * y)
                actual = rotated_remainder_components(a, x, y)
                require(actual == expected
                        and actual[0] ** 2 + actual[1] ** 2 <= cap["remainder_upper"] ** 2,
                        "Exact signed remainder polynomial and universal TWO-disk norm cap")
                full = fourth_power_absolute_upper(A, E, 10 ** 6)
                require((psi4[0] - a ** 4) ** 2 + psi4[1] ** 2
                        <= full["absolute_fourth_power_difference_upper"] ** 2,
                        "Complete ABS intersection, not a signed-linear proof")
                require(real_kernel_remainder(a, x, y, F(2, 3), F(-3, 5))
                        == F(2, 3) * expected[0] + F(3, 5) * expected[1],
                        "Exact REAL-kernel phase expression")
                checks += 3
    strict = two_disk_remainder_upper(F(1), F(1), 10 ** 6)
    require(strict["unit_circle_squared_upper"] == 19
            and strict["remainder_upper"] < strict["existing_integral_disk_upper"] == 5,
            "Genuine new norm gain sqrt19 versus old integral cap5")
    checks += 1
    for A, E in ((F(0), F(1)), (F(1, 4), F(1, 2)),
                 (F(1, 2), F(1, 4)), (F(3, 4), F(1, 4))):
        full = fourth_power_absolute_upper(A, E, 10 ** 6)
        realized = (A + E) ** 4 - A ** 4
        require(A + E <= 1 and full["complete_telescope_upper"] == realized
                and full["absolute_fourth_power_difference_upper"] == realized,
                "SHARP scalar ABS lower limitation under inactive unit-disk cap")
        checks += 1
    for bad in (F(-1), F(2), True, 0.5):
        rejected = False
        try:
            two_disk_remainder_upper(bad, F(1))
        except ValueError:
            rejected = True
        require(rejected, "Invalid/float/bool modulus proof input rejected")
        checks += 1
    return {"exact_checks": checks, "CF_or_optimizer_or_CDF_producer_called": False,
        "scalar_disk_bounds_are_not_characteristic_law_realizability": True,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
