"""Synthetic metadata/control-plane tests; no mathematical producer is run."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from . import archive49_catalog as archive49
from . import archive49_replay
from . import count_catalog as counts
from . import coordinator
from . import stages


def pin(value):
    return hashlib.sha256(value.encode()).hexdigest()


class CountCatalogTests(unittest.TestCase):
    def fixture(self):
        folder = "original/count31"
        sources = {"accept_strict.py": pin("acceptor"), "contract.json": pin("contract")}
        receipt = {"schema": "EXACT_NATIVE_FIXTURE", "status": "PASS", "n": 31,
                   "index": 21, "K": "0", "contract_sha256": sources["contract.json"],
                   "candidate_sha256": pin("untrusted candidate"), "passed_cells": 1,
                   "empty_cells": 1, "all_closed_leaves": 2, "maximum_score": "1/3",
                   "target_lower": "2/5", "negative_controls": 24, "source_sha256": sources}
        relative = folder + "/accepted_strict_21.json"
        graph = {folder + "/" + name: sha for name, sha in sources.items()}
        graph[folder + "/candidate_21.json"] = receipt["candidate_sha256"]
        graph[relative] = pin("old receipt provenance")
        return counts.job_from_receipt(relative, receipt, graph), receipt, graph

    def test_source_selection_does_not_call_or_count_old_pass_as_fresh(self):
        job, _, _ = self.fixture()
        self.assertEqual(job["script"], "accept_strict.py")
        self.assertFalse(job["historical_receipt_is_a_fresh_mathematical_premise"])
        self.assertFalse(any(name.startswith("accepted_") for name in job["sources_sha256"]))

    def test_native_candidate_must_be_bound_by_final_graph(self):
        job, receipt, graph = self.fixture()
        graph[job["folder"] + "/" + job["candidate"]] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Exact candidate independently"):
            counts.job_from_receipt(job["original_receipt"], receipt, graph)

    def test_two_possible_acceptors_cannot_be_guessed(self):
        job, receipt, graph = self.fixture()
        receipt["source_sha256"]["accept_strict_v2.py"] = pin("second")
        with self.assertRaisesRegex(ValueError, "Exactly one"):
            counts.job_from_receipt(job["original_receipt"], receipt, graph)

    def test_fresh_receipt_requires_all_fields_not_just_status(self):
        job, receipt, _ = self.fixture()
        fresh = deepcopy(receipt)
        self.assertEqual(counts.verify_fresh_receipt(job, fresh)["all_closed_leaves"], 2)
        for mutate in (lambda z: z.update(n=True), lambda z: z.update(negative_controls=0),
                       lambda z: z.update(maximum_score="0"), lambda z: z.update(scope="broader"),
                       lambda z: z["source_sha256"].update({"contract.json": "0" * 64})):
            fresh = deepcopy(receipt)
            mutate(fresh)
            with self.assertRaises(ValueError):
                counts.verify_fresh_receipt(job, fresh)

    def test_only_runtime_metadata_can_change_and_no_optimization(self):
        job, receipt, _ = self.fixture()
        fresh = deepcopy(receipt)
        fresh["child_runtime"] = {"executable": sys.executable, "version": "new", "optimize": 0}
        counts.verify_fresh_receipt(job, fresh)
        fresh["child_runtime"]["optimize"] = False
        with self.assertRaisesRegex(ValueError, "Unoptimized"):
            counts.verify_fresh_receipt(job, fresh)

    def test_auxiliary_nonzero_K_is_preserved_not_upgraded(self):
        job, _, _ = self.fixture()
        job["expected_mathematical_receipt"]["K"] = "9/50"
        fresh = deepcopy(job["expected_mathematical_receipt"])
        self.assertEqual(counts.verify_fresh_receipt(job, fresh)["K"], "9/50")
        fresh["K"] = "0"
        with self.assertRaises(ValueError):
            counts.verify_fresh_receipt(job, fresh)

    def test_whole_stage_cannot_drop_one_obligation(self):
        jobs = [{"n": n, "id": str(n) + "-" + str(i)}
                for n, count in counts.EXPECTED_CENSUS.items() for i in range(count)]
        self.assertEqual(len(counts.select(jobs, "base31_34_counts")), 282)
        self.assertEqual(len(counts.select(jobs, "bridge35_39_counts")), 120)
        with self.assertRaisesRegex(ValueError, "Entire selected stage"):
            counts.select(jobs[1:], "base31_34_counts")

    def test_unsafe_source_paths_and_duplicate_json_fail(self):
        for name in ("../source.py", "/source.py", "a\\source.py", "C:/source.py", "a//source.py"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                counts.safe(name)
        with self.assertRaises(ValueError):
            counts.load('{"n":31,"n":32}')


class Archive49MetadataTests(unittest.TestCase):
    def test_absent_whole_process_tree_guard_declines_before_work_or_math(self):
        runner = SimpleNamespace(NATIVE=None)
        with patch.object(archive49_replay, "run_recorded") as numerical_call:
            with self.assertRaisesRegex(ValueError, "Windows whole-process-tree"):
                archive49_replay.require_supported_full_guard(runner, True)
            numerical_call.assert_not_called()
        archive49_replay.require_supported_full_guard(runner, False)
        archive49_replay.require_supported_full_guard(SimpleNamespace(NATIVE=object()), True)

    def test_count_and_component_wrapper_are_in_original_owned512MiB_job(self):
        runner = SimpleNamespace(NATIVE=object(), MIB=1024**2, require=counts.need,
                                 launch_gate=__import__('unittest').mock.Mock())
        with patch.object(coordinator, "run_recorded", return_value="captured") as native:
            self.assertEqual(coordinator.run_branch(runner, [sys.executable, "-B", "wrapper.py"],
                                                    Path("owned"), "owned-stage"), "captured")
            native.assert_called_once_with(runner, [sys.executable, "-B", "wrapper.py"],
                                           Path("owned"), "owned-stage", 7200, 512 * 1024**2)
            runner.launch_gate.assert_called_once_with()

    def test_no_uncontained_branch_is_spawned_when_native_guard_missing(self):
        runner = SimpleNamespace(NATIVE=None, require=counts.need)
        with patch.object(coordinator, "run_recorded") as native, self.assertRaisesRegex(ValueError, "Windows"):
            coordinator.run_branch(runner, ["wrapper.py"], Path("owned"), "owned-stage")
        native.assert_not_called()

    def fixture(self, root):
        source = root / "original-BE49"
        output = root / "fresh-full-result"
        components = output / "components"
        source.mkdir()
        components.mkdir(parents=True)
        new_jobs = [{"name": name, "argv": [name + ".py"]} for name in archive49.TOP_NAMES[:10]]
        retained = [{"name": "component" + str(i), "cwd": "work/selected", "argv": ["accept.py"],
                     "source_run": "old/provenance/" + str(i)} for i in range(41)]
        def row(directory, name, command, **fields):
            for stream in ("stdout", "stderr"):
                (directory / (name + "." + stream + ".txt")).write_bytes(b"" if stream == "stderr" else b"fixture\n")
            return {"name": name, "command": command, "returncode": 0,
                    "stdout_sha256": archive49.sha(directory / (name + ".stdout.txt")),
                    "stderr_sha256": archive49.sha(directory / (name + ".stderr.txt")), **fields}
        commands = [[sys.executable, "-B", *job["argv"]] for job in new_jobs]
        commands += [[sys.executable, "-B", script] for script in
                     ("accept_finite_base.py", "validate_schedule.py", "check_consolidation.py")]
        commands.append([sys.executable, "-B", str(source / "baseline/certificates/work/below50_20260929/release_tools/run_certificates_v2.py"),
                         "--workspace-root", str(source / "baseline/certificates"), "--job-file",
                         str(source / "retained_jobs.json"), "--output", str(components)])
        top = {"status": "PASS_BE49_SELECTED_ARITHMETIC", "quick": False, "sources_unchanged": True,
               "manifest_sha256": archive49.MANIFEST_SHA, "manifested_files": 1400, "executable": sys.executable,
               "jobs": [row(output, name, command) for name, command in zip(archive49.TOP_NAMES, commands)]}
        child = {"schema": "BE_FIXED_CERTIFICATE_SUITE_V2", "status": "PASS", "selected_jobs": 41,
                 "optimized": False, "sources_unchanged": True,
                 "input_sha256": {"source.py": "pin"}, "input_sha256_after": {"source.py": "pin"},
                 "jobs": [row(components, job["name"], [sys.executable, "-B", *job["argv"]],
                              **{k: v for k, v in job.items() if k != "name"}) for job in retained]}
        (output / "result.json").write_text(json.dumps(top))
        (components / "metadata.json").write_text(json.dumps(child))
        return source, output, new_jobs, retained, top, child

    def test_all_14_top_and_41_retained_actual_capture_schemas_required(self):
        with tempfile.TemporaryDirectory() as name:
            source, output, new, retained, _, _ = self.fixture(Path(name))
            result = archive49.validate_full_result(source, output, new, retained)
            self.assertEqual((result["top_level_executions"], result["retained_component_executions"]), (14, 41))
            self.assertFalse(result["quick_mode_used"])

    def test_quick_mode_or_one_missing_execution_cannot_be_promoted(self):
        for mutation in (lambda z: z.update(quick=True), lambda z: z["jobs"].pop(),
                         lambda z: z.update(status="PASS_BE49_INTEGRITY_AND_QUICK_CHECKS")):
            with tempfile.TemporaryDirectory() as name:
                source, output, new, retained, top, _ = self.fixture(Path(name))
                mutation(top)
                (output / "result.json").write_text(json.dumps(top))
                with self.assertRaises(ValueError):
                    archive49.validate_full_result(source, output, new, retained)

    def test_native_command_and_runtime_executable_must_be_current(self):
        with tempfile.TemporaryDirectory() as name:
            source, output, new, retained, top, _ = self.fixture(Path(name))
            top["jobs"][0]["command"][0] = "python3-old-stub"
            (output / "result.json").write_text(json.dumps(top))
            with self.assertRaisesRegex(ValueError, "Entire actual"):
                archive49.validate_full_result(source, output, new, retained)

    def test_retained_component_cannot_be_omitted_or_optimized(self):
        for mutation in (lambda z: z["jobs"].pop(), lambda z: z.update(optimized=True),
                         lambda z: z["input_sha256_after"].update({"source.py": "changed"})):
            with tempfile.TemporaryDirectory() as name:
                source, output, new, retained, _, child = self.fixture(Path(name))
                mutation(child)
                (output / "components/metadata.json").write_text(json.dumps(child))
                with self.assertRaises(ValueError):
                    archive49.validate_full_result(source, output, new, retained)

    def test_returncode_boolean_or_corrupted_stream_fails(self):
        for mutate in (lambda z: z["jobs"][0].update(returncode=False),
                       lambda z: z["jobs"][0].update(stdout_sha256="0" * 64)):
            with tempfile.TemporaryDirectory() as name:
                source, output, new, retained, top, _ = self.fixture(Path(name))
                mutate(top)
                (output / "result.json").write_text(json.dumps(top))
                with self.assertRaises(ValueError):
                    archive49.validate_full_result(source, output, new, retained)

    def test_stage_catalog_does_not_claim_sharp40_48_from_weak_finite_ceiling(self):
        value = stages.stages()
        self.assertFalse(value["bridge40_48"]["fresh_full_replay_implemented"])
        self.assertFalse(value["tail49.full_suite"]["quick_mode_accepted"])
        self.assertEqual(value["tail49.full_suite"]["retained_native_components"], 41)


if __name__ == "__main__":
    unittest.main()
