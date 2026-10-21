"""Control-plane tests, not numerical proof certificates."""
import copy
import unittest
from .coverage import check_index_cover, computational_scope, obligations, order


class CoverageTests(unittest.TestCase):
    def test_full_literal_cover(self):
        check_index_cover([[1,30],[31,None]])

    def test_missing_one_index(self):
        with self.assertRaisesRegex(ValueError,"Uncovered index: 5"):
            check_index_cover([[1,4],[6,None]])

    def test_finite_tail_is_not_infinite(self):
        with self.assertRaisesRegex(ValueError,"No verified unbounded tail"):
            check_index_cover([[1,1000000]])

    def test_boolean_index_rejected(self):
        with self.assertRaises(ValueError):
            check_index_cover([[True,None]])

    def test_cycles_rejected(self):
        nodes = obligations()
        nodes["n3"]["depends"] = ["n4"]
        with self.assertRaisesRegex(ValueError,"Cyclic"):
            order(nodes)

    def test_missing_parent_rejected(self):
        nodes = obligations()
        del nodes["n3"]
        with self.assertRaisesRegex(ValueError,"Missing proof"):
            order(nodes)

    def test_small_indices_do_not_cover_all(self):
        records = {n:{"fresh_arithmetic":True} for n in ("n2","n3","n4")}
        self.assertFalse(computational_scope(records)["all_computational_obligations_verified"])

    def test_old_pass_or_integrity_is_not_fresh_arithmetic(self):
        records = {n:{"status":"PASS","hash_verified":True} for n in obligations()}
        self.assertFalse(computational_scope(records)["all_computational_obligations_verified"])

    def test_missing_c5_resource_cannot_be_hidden_by_counts(self):
        # Synthetic control-plane fixture, not a claim of real computation.
        records = {n:{"fresh_arithmetic":True} for n in obligations()}
        del records["c5.resources"]
        result = computational_scope(records)
        self.assertFalse(result["all_computational_obligations_verified"])
        self.assertIn("c5.resources",result["outstanding"])

    def test_synthetic_complete_fixture(self):
        records = {n:{"fresh_arithmetic":True} for n in obligations()}
        self.assertTrue(computational_scope(records)["all_computational_obligations_verified"])


if __name__ == "__main__":
    unittest.main()
