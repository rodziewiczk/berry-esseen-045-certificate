"""Small synthetic actual-index component tests; never run native mathematics."""
from copy import deepcopy
import hashlib
import io
import json
import unittest
import zipfile

from . import component40_catalog as component


def pin(raw):
    return hashlib.sha256(raw).hexdigest()


class Native40CatalogTests(unittest.TestCase):
    def test_exactly_ten_distinct_literal_jobs_without_global_composer(self):
        jobs = component.definitions()
        self.assertEqual(len(jobs), 10)
        self.assertEqual(len({job["id"] for job in jobs}), 10)
        self.assertFalse(any("join" in job["script"] for job in jobs))
        self.assertEqual(sum(job["kind"] == "fixed_component" for job in jobs), 6)

    def fixture(self):
        job = component.definitions()[0]
        source = {"accept40.py": b"source only fixture", "native_core.py": b"unexecuted source",
                  "acquisition_candidate.json": b"untrusted full candidate fixture",
                  "initial40_candidate.json": b"explicit conditional parent candidate fixture"}
        manifest = {"schema": "SINGLE40_CENTRAL_FIXED_MANIFEST_V1", "component": "acquisition",
                    "sources": {name: pin(raw) for name, raw in source.items() if name.endswith(".py")},
                    "proof": {"acquisition_candidate.json": pin(source["acquisition_candidate.json"])},
                    "inputs": {"initial40_candidate.json": pin(source["initial40_candidate.json"])}}
        source["acquisition_manifest.json"] = json.dumps(manifest).encode()
        graph = {job["folder"] + "/" + name: pin(raw) for name, raw in source.items()}
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as archive:
            for name, raw in source.items():
                archive.writestr("cutoff25_20261011/" + job["folder"] + "/" + name, raw)
        data.seek(0)
        return job, graph, data

    def test_native_manifest_selects_full_sources_proof_and_parent_candidate(self):
        job, graph, data = self.fixture()
        with zipfile.ZipFile(data) as archive:
            selected = component.selected_inputs(archive, graph, job)
        self.assertEqual(len(selected["sources_sha256"]), 5)
        self.assertEqual(selected["proof"], "acquisition_candidate.json")
        self.assertFalse(selected["same_witness_and_parent_acquisitions_verified"])

    def test_manifest_cannot_use_a_different_native_source_epoch(self):
        job, graph, data = self.fixture()
        graph[job["folder"] + "/native_core.py"] = "0" * 64
        with zipfile.ZipFile(data) as archive, self.assertRaisesRegex(ValueError, "source graph agreement"):
            component.selected_inputs(archive, graph, job)

    def test_complete_final_json_after_progress_not_a_saved_pass_line(self):
        self.assertEqual(component.final_json('progress\n{"index":1}\n{"status":"fixed","x":2}\n'),
                         {"status": "fixed", "x": 2})
        for bad in ('PASS only', '{"x":1,"x":2}', '{"status":"ok"}\ntrailing garbage'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                component.final_json(bad)

    def tiny_fixture(self):
        job = next(job for job in component.definitions() if job["id"] == "left40_tiny")
        job["sources_sha256"] = {job["proof"]: "a" * 64, job["script"]: "b" * 64}
        result = {"status": job["expected_status"], "proof_sha256": "a" * 64,
                  "negative_controls": ["control_" + str(i) for i in range(12)],
                  "rows": 49, "phase_cases": 294, "minimum_reserve": "1/1000",
                  "acceptor_sha256": "b" * 64}
        return job, result

    def test_tiny_complete_census_and_original_proof_source_binding(self):
        job, result = self.tiny_fixture()
        self.assertIs(component.validate_result(job, result), result)
        for mutation in (lambda z: z.update(rows=True), lambda z: z.update(phase_cases=288),
                         lambda z: z.update(proof_sha256="0" * 64), lambda z: z["negative_controls"].pop(),
                         lambda z: z.update(acceptor_sha256="0" * 64)):
            bad = deepcopy(result)
            mutation(bad)
            with self.assertRaises(ValueError):
                component.validate_result(job, bad)

    def test_false_float_boolean_zero_or_noncanonical_reserve_rejected(self):
        job, result = self.tiny_fixture()
        for value in (False, True, 0.001, "0", "-1/1000", "01/1000"):
            bad = dict(result, minimum_reserve=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                component.validate_result(job, bad)

    def test_duplicate_corruption_control_cannot_replace_missing_one(self):
        job, result = self.tiny_fixture()
        result["negative_controls"][1] = result["negative_controls"][0]
        with self.assertRaises(ValueError):
            component.validate_result(job, result)

    def test_full_fixed_component_has_all_thirteen_original_controls(self):
        job = component.definitions()[0]
        job.update(proof="candidate.json", manifest="manifest.json",
                   sources_sha256={"candidate.json": "a" * 64, "manifest.json": "b" * 64})
        result = {"status": job["expected_status"], "proof_sha256": "a" * 64,
                  "source_manifest_sha256": "b" * 64, "negative_controls": 13}
        component.validate_result(job, result)
        for value in (True, 12):
            with self.assertRaises(ValueError):
                component.validate_result(job, dict(result, negative_controls=value))


if __name__ == "__main__":
    unittest.main()
