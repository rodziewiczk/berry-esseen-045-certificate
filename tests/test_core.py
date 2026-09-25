from fractions import Fraction
import unittest

from proof.berry_core import (
    A,
    CertificateError,
    RHO0_Q,
    build_constants,
    certificate_partitions,
    evaluate_cell,
    geom_sum_upper,
    kernel_K_abs_upper,
    kernel_L_abs_upper,
    parse_q,
    psi_lower,
    qstr,
    rad_gauss_diff_upper,
    regularized_cot_d_upper_point,
    second_endpoint_integral_upper,
    self_test_global_reductions,
    stable_B_point,
    ub,
)


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.constants = build_constants(192)

    def test_canonical_rationals(self):
        self.assertEqual(parse_q("712569/589000"), RHO0_Q)
        self.assertEqual(qstr(Fraction(6, 8)), "3/4")
        for invalid in (0.5, "0.5", "06", "2/4", "-0", "1/0", True):
            with self.assertRaises(CertificateError):
                parse_q(invalid)

    def test_global_scalar_reduction(self):
        self_test_global_reductions(self.constants)

    def test_stable_B_at_rho_one(self):
        self.assertTrue(stable_B_point(Fraction(1), self.constants) == 0)

    def test_positive_geometric_sum(self):
        a, c = A(Fraction(1, 2)), A(Fraction(1, 3))
        bound = geom_sum_upper(a, c, 5)
        exact = sum(
            Fraction(1, 2) ** j * Fraction(1, 3) ** (4 - j)
            for j in range(5)
        )
        self.assertTrue(A(exact) <= bound)

    def test_endpoint_K_bound_encloses_points_and_vanishes(self):
        maximum_h = Fraction(1, 128)
        bound = kernel_K_abs_upper(1 - maximum_h, Fraction(1), self.constants)
        self.assertTrue(bound < A(Fraction(1, 200)))
        for h in (maximum_h, maximum_h / 2, maximum_h / 4):
            x = self.constants.pi * A(h)
            d = 1 / x - x.cos() / x.sin()
            direct = A(h) * (1 + d * d).sqrt() / 2
            self.assertTrue(ub(direct) <= bound)

    def test_quadratic_endpoint_integral(self):
        h = Fraction(1, 128)
        analytic = second_endpoint_integral_upper(1 - h, self.constants)
        rectangle = ub(
            2
            * A(h)
            * kernel_K_abs_upper(1 - h, Fraction(1), self.constants)
        )
        self.assertTrue(analytic <= rectangle)
        self.assertTrue(analytic < A(Fraction(1, 10000)))

    def test_regularized_cotangent_series(self):
        s = Fraction(1, 1024)
        x = self.constants.pi * A(s)
        direct = 1 / x - x.cos() / x.sin()
        bound_8 = regularized_cot_d_upper_point(s, self.constants, 8)
        bound_100 = regularized_cot_d_upper_point(s, self.constants, 100)
        self.assertTrue(ub(direct) <= bound_8)
        self.assertTrue(ub(direct) <= bound_100)
        self.assertTrue(bound_100 <= bound_8)

    def test_regularized_L_bound_near_zero(self):
        bound = kernel_L_abs_upper(
            Fraction(1, 1024), Fraction(3, 2048), self.constants, 8
        )
        self.assertTrue(bound.is_finite())
        self.assertTrue(bound < A(1))

    def test_gaussian_difference_encloses_points(self):
        n = 1000
        rho = Fraction(287079, 250000)
        q = Fraction(156, 25)
        left = Fraction(1, 1024)
        right = Fraction(1, 512)
        bound = rad_gauss_diff_upper(
            n, rho, rho, q, left, right, self.constants
        )
        self.assertTrue(bound < A(Fraction(1, 1000)))
        for s in (left, (left + right) / 2, right):
            u = A(q * s / (rho + 1))
            direct = (
                (u.cos() ** n) - (A(0) - A(n) * u * u / 2).exp()
            ).abs_upper()
            self.assertTrue(ub(direct) <= bound)

    def test_psi_guard_crossing_uses_global_lower_bound(self):
        bound = psi_lower(
            Fraction(6), Fraction(3, 5), Fraction(3, 4), self.constants
        )
        self.assertTrue(bound == 0)

    def test_compact_grid_recipe_reconstructs_all_integrals(self):
        first, second, third = certificate_partitions(
            1000,
            Fraction(1),
            Fraction(101, 100),
            Fraction(6),
            Fraction(3, 4),
            Fraction(1, 64),
            Fraction(1, 1024),
            32,
            3,
        )
        self.assertEqual((first[0], first[-1]), (Fraction(1, 64), Fraction(3, 4)))
        self.assertEqual((second[0], second[-1]), (Fraction(3, 4), Fraction(1)))
        self.assertEqual((third[0], third[-1]), (Fraction(1, 1024), Fraction(3, 4)))
        self.assertTrue(all(a < b for a, b in zip(first, first[1:])))
        self.assertTrue(all(a < b for a, b in zip(second, second[1:])))
        self.assertTrue(all(a < b for a, b in zip(third, third[1:])))

    def test_compact_cell_evaluates_finitely(self):
        cell = {
            "rho": ["1", "101/100"],
            "q": "6",
            "t0": "3/4",
            "eta": "1/1024",
            "lambda": "1/1024",
            "grid": {"pieces": 4, "power": 1},
        }
        result = evaluate_cell(2, cell, self.constants, regularized_cot_terms=8)
        self.assertTrue(result.ratio_upper.is_finite())

    def test_cell_rejects_lambda_above_one_half(self):
        cell = {
            "rho": ["1", "101/100"],
            "q": "6",
            "t0": "3/4",
            "eta": "1/1024",
            "lambda": "3/4",
            "grid": {"pieces": 4, "power": 1},
        }
        with self.assertRaisesRegex(CertificateError, "lambda"):
            evaluate_cell(2, cell, self.constants, regularized_cot_terms=8)


if __name__ == "__main__":
    unittest.main()
