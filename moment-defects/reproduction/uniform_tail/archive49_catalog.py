"""Literal original cutoff49 source/suite identities, not theorem acceptance."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

if __package__:
    from .count_catalog import equal_typed, load, need, safe, sha
else:
    from count_catalog import equal_typed, load, need, safe, sha

ARCHIVE_BYTES = 16660566
ARCHIVE_SHA = "ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e"
PREFIX = "BE_cutoff49_20260930/"
MANIFEST_SHA = "58a770705c6e0bc500813ed37299753a16f6245ebea6ade238ad98078d7b4e26"
VERIFY_SHA = "766e9cee5d1cb8b173fd2db264cddbd227439e4e87fbcf3daec243ec2c9a1375"
NEW_JOBS_SHA = "edb42eef2e7e4110533173cc384ecb94167bf5c312fea8f371916fbdd6f013d6"
RETAINED_JOBS_SHA = "d92f0017fadc5c2f9601de599f2e1f97eb9c1042b02a17a695065c040f09d7ad"
FILE_COUNT = 1401
EXPANDED_BYTES = 33252205
TOP_NAMES = ["composition49", "support46", "independent_support46", "independent_selectors",
             "phase_product_controls", "new_phase_controls", "later_phase_domains",
             "independent_phase_scope", "corrected_legacy_acquisition", "corrected_barrier46",
             "finite_base", "entry_schedule_mapping", "local_formula_mapping", "retained_components"]


def manifest(raw):
    need(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, "Original exact BE49 manifest bytes")
    value = load(raw)
    need(set(value) == {"schema", "files"} and value["schema"] == "BE49_ARCHIVE_V1",
         "Original manifest schema")
    pins = value["files"]
    need(type(pins) is dict and len(pins) == FILE_COUNT - 1, "All 1400 original manifested inputs")
    for name, pin in pins.items():
        safe(name)
        need(type(pin) is str and len(pin) == 64 and set(pin) <= set("0123456789abcdef"),
             "Literal original source hash")
    need(pins["verify.py"] == VERIFY_SHA and pins["new_jobs.json"] == NEW_JOBS_SHA
         and pins["retained_jobs.json"] == RETAINED_JOBS_SHA, "Entire original full-suite driver/job pins")
    return pins


def verify_sources(root):
    pins = manifest((root / "MANIFEST.json").read_bytes())
    for name, pin in pins.items():
        path = root.joinpath(*safe(name))
        need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root.resolve())
             and sha(path) == pin, "Unchanged original BE49 input: " + name)
    return pins


def source_jobs(root):
    need(sha(root / "new_jobs.json") == NEW_JOBS_SHA and sha(root / "retained_jobs.json") == RETAINED_JOBS_SHA,
         "Exact original full job lists")
    new = load((root / "new_jobs.json").read_bytes())
    retained = load((root / "retained_jobs.json").read_bytes())
    need(len(new) == 10 and [j["name"] for j in new] == TOP_NAMES[:10]
         and len(retained) == 41 and len({j["name"] for j in retained}) == 41,
         "All 10 new and 41 retained native jobs, no quick-mode reduction")
    return new, retained


def successful(record, directory, name):
    need(type(record["returncode"]) is int and record["returncode"] == 0,
         "Actual successful integer native return code: " + name)
    for kind in ("stdout", "stderr"):
        path = directory / (name + "." + kind + ".txt")
        need(path.is_file() and not path.is_symlink() and path.stat().st_size <= 16 * 1024 ** 2
             and sha(path) == record[kind + "_sha256"], "Actual native captured bytes: " + name)
    need(not (directory / (name + ".stderr.txt")).read_bytes(), "No successful native stderr: " + name)


def validate_full_result(root, output, new_jobs, retained_jobs):
    """Audit real FULL output; quick, partial, old or changed captures fail."""
    result = load((output / "result.json").read_bytes())
    need(result["status"] == "PASS_BE49_SELECTED_ARITHMETIC"
         and result["quick"] is False and result["sources_unchanged"] is True
         and result["manifest_sha256"] == MANIFEST_SHA and result["manifested_files"] == 1400,
         "Complete original FULL suite, never quick or inventory-only acceptance")
    need(result["executable"] == sys.executable, "Current full Python executable, not a historical stub")
    rows = result["jobs"]
    need([row["name"] for row in rows] == TOP_NAMES, "All 14 original top-level executions in order")
    expected_commands = [[sys.executable, "-B", *job["argv"]] for job in new_jobs]
    expected_commands += [[sys.executable, "-B", script] for script in
                          ("accept_finite_base.py", "validate_schedule.py", "check_consolidation.py")]
    runner = root / "baseline/certificates/work/below50_20260929/release_tools/run_certificates_v2.py"
    expected_commands.append([sys.executable, "-B", str(runner), "--workspace-root",
                              str(root / "baseline/certificates"), "--job-file",
                              str(root / "retained_jobs.json"), "--output", str(output / "components")])
    for row, command in zip(rows, expected_commands):
        need(equal_typed(row["command"], command), "Entire actual original native command")
        successful(row, output, row["name"])
    components = output / "components"
    child = load((components / "metadata.json").read_bytes())
    need(child["schema"] == "BE_FIXED_CERTIFICATE_SUITE_V2" and child["status"] == "PASS"
         and child["selected_jobs"] == 41 and child["optimized"] is False
         and child["sources_unchanged"] is True
         and equal_typed(child["input_sha256"], child["input_sha256_after"]),
         "All retained components freshly run with unchanged complete source snapshot")
    need([j["name"] for j in child["jobs"]] == [j["name"] for j in retained_jobs],
         "Every one of the 41 selected native component jobs")
    for row, expected in zip(child["jobs"], retained_jobs):
        need(all(equal_typed(row[key], expected[key]) for key in ("name", "cwd", "argv", "source_run"))
             and equal_typed(row["command"], [sys.executable, "-B", *expected["argv"]]),
             "Exact retained native job; source_run is provenance only")
        successful(row, components, row["name"])
    return {"top_level_executions": len(rows), "retained_component_executions": len(child["jobs"]),
            "result_sha256": sha(output / "result.json"),
            "retained_metadata_sha256": sha(components / "metadata.json"),
            "quick_mode_used": False}
