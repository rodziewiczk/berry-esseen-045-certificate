"""INITIAL adapter plumbing and fact-schema tests; no numerical replay."""
from copy import deepcopy
import unittest

from . import c5_initial_one as initial


class InitialArithmeticTests(unittest.TestCase):
    def fixture(self, name="initial.B0"):
        job = next(job for job in initial.INITIAL_JOBS if job.job_id == name)
        lo, hi = initial.expected_rho(job)
        radius = {"B0": "23/10", "BN": "12/5", "B2": "49/20", "B3": "99/40"}[job.band]
        profile = {"n": 5, "nmax": 5, "q_contact": "0", "barrier": "0", "cap": job.owncap,
                   "radius": radius, "radius_minus": radius, "radius_plus": radius,
                   "grid": [12, 12, 6, 3],
                   "invariants": {"rho_lo": str(lo), "rho": str(hi), "beta_lo": "-1/3", "beta_hi": "1/3"}}
        controls = ["wrong n", "missing cell", "duplicate JSON key"]
        prepared = {"input_sha256": "a" * 64}
        receipt = {"status": job.expected_status, "n": 5, "band": job.band,
                   "stages": job.stages, "total_cells_per_stage": 2592, "panels": 100,
                   "final_active": 123, "final_gap_active": 123, "negative_controls": controls,
                   "input_sha256": prepared["input_sha256"], "profile": profile,
                   "numerical_premises": {"predecessor_theorem": "user_assumed_C4_le_CE",
                       "contact_error": "0", "owncap": job.owncap, "HIGH": job.high},
                   "rho_interval": [str(lo), str(hi)], "final_raw": "1", "final_D": "1/10",
                   "signed_support_rows": 2}
        if job.sector is not None:
            receipt.update(sector=job.sector, beta_interval=["-1/3", "1/3"])
        if job.family == "initial5_B3_top_accept_v3":
            receipt["partition_kind"] = "B3_TOP_BETA_1_5_3_10_B"
        if job.family == "initial5_B3_T3lower_accept_v1":
            receipt["partition_kind"] = "B3_UPPER_RHO_BETA_3_10_17_50"
        return job, receipt, prepared, controls

    def test_extracts_original_controls_without_execution(self):
        source = "raise RuntimeError('must never execute')\nmutations=[('wrong n',lambda x:None),('missing cell',lambda x:None)]\n"
        self.assertEqual(initial.control_names(source), ["wrong n", "missing cell", "duplicate JSON key"])

    def test_native_windows_source_spelling_is_metadata_not_a_hash_rewrite(self):
        pin = "a" * 64
        graph = {"work/a/file.py": pin, "work\\a\\file.py": pin}
        self.assertEqual(initial.canonical_native_sources(graph), {"work/a/file.py": pin})
        self.assertEqual(len(graph), 2)
        with self.assertRaises(ValueError):
            initial.canonical_native_sources({"work/a.py": pin, "work\\a.py": "b" * 64})
        for name in ("../escape.py", "C:\\escape.py", "\\\\server\\escape.py"):
            with self.subTest(path=name), self.assertRaises(ValueError):
                initial.canonical_native_sources({name: pin})

    def test_facts_bind_exact_candidate_profile_and_closed_p_cover(self):
        job, receipt, prepared, controls = self.fixture()
        facts = initial.validate_receipt(job, receipt, prepared, controls)
        self.assertEqual(facts["input_candidate_sha256"], prepared["input_sha256"])
        self.assertEqual(facts["validated_closed_p_indices"], list(range(100)))
        self.assertEqual(facts["profile"], receipt["profile"])
        self.assertEqual(facts["numerical_premises"]["owncap"], "429/1000")

    def test_all12_selected_job_schemas(self):
        for job in initial.INITIAL_JOBS:
            with self.subTest(job=job.job_id):
                args = self.fixture(job.job_id)
                facts = initial.validate_receipt(*args)
                self.assertEqual(facts["stages"], job.stages)

    def test_wrong_boolean_n_partial_cover_and_stale_candidate_rejected(self):
        for field, value in (("n", True), ("panels", 99), ("stages", 8),
                             ("total_cells_per_stage", 2591), ("final_gap_active", 122),
                             ("input_sha256", "b" * 64), ("negative_controls", [])):
            job, receipt, prepared, controls = self.fixture()
            receipt[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                initial.validate_receipt(job, receipt, prepared, controls)

    def test_conditional_premise_cannot_be_replaced_with_a_numeric_predecessor(self):
        job, receipt, prepared, controls = self.fixture()
        receipt["numerical_premises"]["predecessor_theorem"] = "C4<=.4097"
        with self.assertRaises(ValueError):
            initial.validate_receipt(job, receipt, prepared, controls)

    def test_wrong_support_profile_and_rho_domain_rejected(self):
        for change in (lambda x: x["profile"].update(radius="4"),
                       lambda x: x.update(rho_interval=["1", "2"]),
                       lambda x: x["profile"].update(grid=[12, 12, 6, True])):
            job, receipt, prepared, controls = self.fixture()
            change(receipt)
            with self.assertRaises(ValueError):
                initial.validate_receipt(job, receipt, prepared, controls)

    def test_sector_and_partition_kind_are_not_interchangeable(self):
        job, receipt, prepared, controls = self.fixture("initial.B3.T3lower")
        receipt["partition_kind"] = "B3_TOP_BETA_1_5_3_10_B"
        with self.assertRaises(ValueError):
            initial.validate_receipt(job, receipt, prepared, controls)
        job, receipt, prepared, controls = self.fixture("initial.B2.S2")
        receipt["sector"] = True
        with self.assertRaises(ValueError):
            initial.validate_receipt(job, receipt, prepared, controls)


if __name__ == "__main__":
    unittest.main()
