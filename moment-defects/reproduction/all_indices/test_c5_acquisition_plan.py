"""Catalog/control-plane tests, not numerical proof acceptances."""
from dataclasses import FrozenInstanceError, replace
import unittest

from . import c5_acquisition_plan as catalog


class AcquisitionPlanTests(unittest.TestCase):
    def test_exact_selected_census_and_resource_cover(self):
        catalog.validate_catalog()
        self.assertEqual(len(catalog.INITIAL_JOBS), 12)
        self.assertEqual(len(catalog.RESOURCE_JOBS), 15)
        self.assertEqual(sum(len(job.indices) for job in catalog.RESOURCE_JOBS), 1200)

    def test_jobs_are_immutable_and_typed(self):
        job = catalog.INITIAL_JOBS[0]
        with self.assertRaises(FrozenInstanceError):
            job.n = 6
        with self.assertRaises(ValueError):
            replace(job, n=True)
        with self.assertRaises(ValueError):
            replace(job, sector=True)
        with self.assertRaises(ValueError):
            replace(job, indices=(True,))

    def test_missing_or_duplicated_job_is_rejected(self):
        with self.assertRaises(ValueError):
            catalog.validate_catalog(catalog.JOBS[:-1])
        with self.assertRaises(ValueError):
            catalog.validate_catalog(catalog.JOBS[:-1] + (catalog.JOBS[0],))

    def test_missing_p_panel_cannot_hide_behind_the_job_count(self):
        jobs = list(catalog.JOBS)
        position = next(i for i, job in enumerate(jobs) if job.job_id == "resource.B0.gamma")
        jobs[position] = replace(jobs[position], indices=tuple(range(37, 45)))
        with self.assertRaisesRegex(ValueError, "exactly100"):
            catalog.validate_catalog(tuple(jobs))

    def test_stage_counts_and_short_sector_choice(self):
        jobs = {job.job_id: job for job in catalog.INITIAL_JOBS}
        self.assertEqual(jobs["initial.B2.S2"].stages, 4)
        self.assertEqual(jobs["initial.B2.S3"].stages, 9)
        self.assertEqual(jobs["initial.B3.T3lower"].arguments, ("5", "B3", "3"))
        self.assertNotIn("initial.B3.T3", jobs)

    def test_native_commands_and_fixed_output_paths(self):
        job = next(job for job in catalog.RESOURCE_JOBS if job.job_id == "resource.B2.S3.endpoint")
        self.assertEqual(job.commands, (("-B", "replay.py", "3", "endpoint"),
                                        ("-B", "accept.py", "3", "endpoint")))
        self.assertTrue(job.output_paths[0].endswith("B2_S3_endpoint/REPLAY.json"))
        self.assertEqual(job.indices, (32, 33, 34))
        self.assertEqual(len(job.fresh_outputs_to_exclude), 5)

    def test_plan_is_never_an_arithmetic_acceptance(self):
        plan = catalog.plan()
        self.assertFalse(plan["arithmetic_executed"])
        self.assertFalse(plan["arithmetic_accepted"])
        self.assertFalse(plan["all_index_conclusion_verified"])
        self.assertFalse(plan["fresh_parent_fact_joins_implemented"])
        self.assertNotIn("fresh_arithmetic", plan)
        for job in plan["jobs"]:
            self.assertTrue(job["required_fresh_fact_joins"])
            self.assertFalse(job["fresh_parent_fact_joins_implemented"])


if __name__ == "__main__":
    unittest.main()
