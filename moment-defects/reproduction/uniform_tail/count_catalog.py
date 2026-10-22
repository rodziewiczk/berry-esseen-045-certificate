"""Pinned native count sub-DAG for n31--39, including auxiliary predecessors.

Historical receipts are used only to select exact source/candidate inputs and
expected scopes. Every selected native acceptor must still execute. This is
not a complete acquisition/INITIAL/Fourier/tail or all-law proof controller.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import PurePosixPath
import re
import stat

ARCHIVE_BYTES = 514958998
ARCHIVE_SHA = "17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb"
PREFIX = "cutoff25_20261011/"
RECORD = "continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json"
RECORD_SHA = "33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9"
EXPECTED_CENSUS = {31: 58, 32: 68, 33: 76, 34: 80, 35: 26, 36: 25, 37: 24, 38: 23, 39: 22}
STAGES = {"base31_34_counts": (31, 34), "bridge35_39_counts": (35, 39)}
MIB = 1024 ** 2


def need(value, message):
    if not value:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON field")
        result[key] = value
    return result


def load(raw):
    return json.loads(raw, object_pairs_hook=unique)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(path):
    result = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(MIB):
            result.update(block)
    return result.hexdigest()


def safe(name):
    need(type(name) is str and name and not any(c in name for c in ("\\", ":", "\x00")),
         "Explicit original portable relative name")
    parts = name.split("/")
    need(all(part not in ("", ".", "..") for part in parts), "No absolute/parent path")
    return parts


def member(archive, relative, pin, maximum=64 * MIB):
    safe(relative)
    info = archive.getinfo(PREFIX + relative)
    need(not info.is_dir() and info.file_size <= maximum and
         not stat.S_ISLNK(info.external_attr >> 16), "Bounded exact regular archive member")
    raw = archive.read(info)
    need(hashlib.sha256(raw).hexdigest() == pin, "Exact pinned archive input: " + relative)
    return raw


def flat(name):
    need(len(safe(name)) == 1, "Native count input must be a flat local file")
    return name


def job_from_receipt(relative, receipt, graph):
    """Build a literal job; old status is never recorded as fresh acceptance."""
    folder = str(PurePosixPath(relative).parent)
    n, index = receipt["n"], receipt["index"]
    need(type(n) is int and n in EXPECTED_CENSUS and type(index) is int and 0 <= index < 100,
         "Literal n31--39 probability panel")
    need(type(receipt["source_sha256"]) is dict and receipt["source_sha256"], "Native source closure")
    sources = dict(receipt["source_sha256"])
    scripts = [flat(name) for name in sources if re.fullmatch(r"accept_strict(?:_v2)?\.py", name)]
    need(len(scripts) == 1, "Exactly one reviewed strict native acceptance entrypoint")
    need("contract.json" in sources, "Full fixed resource contract")
    for name, pin in sources.items():
        flat(name)
        need(graph.get(folder + "/" + name) == pin, "Native source/final commitment agreement")
        need(not name.startswith("accepted_"), "No old accepted receipt is a native source input")
    candidate = "candidate_" + str(index) + ".json"
    need(graph.get(folder + "/" + candidate) == receipt["candidate_sha256"],
         "Exact candidate independently bound by pinned final closure")
    need(type(receipt["all_closed_leaves"]) is int and receipt["all_closed_leaves"] > 0
         and type(receipt["negative_controls"]) is int and receipt["negative_controls"] > 0,
         "Complete nonempty native expected census")
    need(Fraction(receipt["maximum_score"]) < Fraction(receipt["target_lower"]),
         "Pinned intended strict target; fresh arithmetic still required")
    return {"id": hashlib.sha256(relative.encode()).hexdigest()[:16], "n": n, "index": index,
            "original_receipt": relative, "historical_receipt_sha256": graph[relative],
            "folder": folder, "script": scripts[0], "output": flat(PurePosixPath(relative).name),
            "candidate": candidate, "candidate_sha256": receipt["candidate_sha256"],
            "sources_sha256": sources, "expected_mathematical_receipt": receipt,
            "historical_receipt_is_a_fresh_mathematical_premise": False}


def catalog(archive):
    record = load(member(archive, RECORD, RECORD_SHA, 8 * MIB))
    need(record["status"] == "PASS_EVENTUAL_CUTOFF31_AT_EXPLICIT_RETAINED_SCOPE"
         and record["fully_reproduced_historical_dependency_DAG"] is False,
         "Original retained-scope identity, not fresh global acceptance")
    graph = record["files_sha256"]
    need(type(graph) is dict and len(graph) == 9518, "Full pinned archival closure")
    jobs = []
    for relative, pin in graph.items():
        if re.fullmatch(r"accepted_strict(?:_v2)?_\d+\.json", PurePosixPath(relative).name) is None:
            continue
        receipt = load(member(archive, relative, pin, 4 * MIB))
        n = receipt.get("n")
        if type(n) is int and n in EXPECTED_CENSUS:
            jobs.append(job_from_receipt(relative, receipt, graph))
    need(dict(Counter(job["n"] for job in jobs)) == EXPECTED_CENSUS,
         "All 402 pinned strict-count obligations, not a silently reduced selection")
    need(len({job["id"] for job in jobs}) == len(jobs), "Unique exact count job identities")
    return sorted(jobs, key=lambda job: (job["n"], job["original_receipt"])), graph


def select(jobs, stage, job_id=None):
    lo, hi = STAGES[stage]
    chosen = [job for job in jobs if lo <= job["n"] <= hi]
    need(len(chosen) == sum(EXPECTED_CENSUS[n] for n in range(lo, hi + 1)), "Entire selected stage census")
    if job_id is not None:
        chosen = [job for job in chosen if job["id"] == job_id]
        need(len(chosen) == 1, "One exact reviewed job id in requested stage")
    return chosen


def equal_typed(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(equal_typed(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(equal_typed(a, b) for a, b in zip(left, right))
    return left == right


def verify_fresh_receipt(job, fresh):
    """Compare all native mathematical/source fields, never old runtime bytes."""
    expected = job["expected_mathematical_receipt"]
    omit = {"child_runtime"}
    need(equal_typed({k: v for k, v in fresh.items() if k not in omit},
                     {k: v for k, v in expected.items() if k not in omit}),
         "Every freshly recomputed native scope, leaf, strict bound, control and source field")
    for key in ("n", "index", "passed_cells", "empty_cells", "all_closed_leaves", "negative_controls"):
        need(type(fresh[key]) is int, "Literal native integer field: " + key)
    need(fresh["passed_cells"] + fresh["empty_cells"] == fresh["all_closed_leaves"]
         and fresh["n"] == job["n"] and fresh["index"] == job["index"], "All native closed leaves")
    need(Fraction(fresh["maximum_score"]) < Fraction(fresh["target_lower"]), "Fresh strict scalar target")
    if "child_runtime" in fresh:
        need(type(fresh["child_runtime"]["optimize"]) is int
             and fresh["child_runtime"]["optimize"] == 0, "Unoptimized fresh native child")
    return {"n": fresh["n"], "index": fresh["index"], "K": fresh["K"],
            "all_closed_leaves": fresh["all_closed_leaves"], "negative_controls": fresh["negative_controls"],
            "maximum_score": fresh["maximum_score"], "target_lower": fresh["target_lower"]}
