"""Literal actual n40--42 acquisition/confinement/profile/local native jobs.

Each fixed acceptor recomputes its complete proof object. All-law contact,
INITIAL predecessors and same-witness domain joins remain separate. This is
not the old source-bound global40 composer and does not call it.
"""
from fractions import Fraction
import hashlib
import json
from pathlib import PurePosixPath

if __package__:
    from .count_catalog import RECORD, RECORD_SHA, member, load, need, flat, unique
else:
    from count_catalog import RECORD, RECORD_SHA, member, load, need, flat, unique

RELEASE = "BE_cutoff35_release_20261007/work/cutoff40_release_20261007/"
WORK = RELEASE + "work/toward40_20261007/"


def definitions():
    jobs = []
    for region, folder, script, status in (
        ("central", "central40", "accept40.py", "PASS_SINGLE40_CENTRAL_"),
        ("left", "left40_accept", "accept_indexed.py", "PASS_INDEXED40_42_LEFT_")):
        for component in ("acquisition", "confinement", "profile"):
            jobs.append({"id": region + "40_" + component, "folder": WORK + folder,
                         "script": script, "argv": [component], "kind": "fixed_component",
                         "component": component, "expected_status": status + component.upper(),
                         "negative_controls": 13})
    for region, folder, tiny_status, mid_status in (
        ("central", "root/central_compare", "PASS_EXACT_CENTRAL_TINY40", "PASS_EXACT_CONDITIONAL_N40_SIGNED_PHASE_MID"),
        ("left", "local/actual_left40_final", "PASS_EXACT_FINITE_LEFT40_42_TINY", "PASS_EXACT_FINITE_LEFT40_42_SIGNED_PHASE_MID")):
        for kind, status in (("tiny", tiny_status), ("mid", mid_status)):
            jobs.append({"id": region + "40_" + kind, "folder": WORK + folder,
                         "script": "accept_" + kind + "40.py", "argv": [], "kind": kind,
                         "expected_status": status, "negative_controls": 12,
                         "rows": 48 if region == "central" else 49,
                         "proof": "tiny40_proof.json" if kind == "tiny" else "mid40_witnesses.json"})
    return jobs


def selected_inputs(archive, graph, job):
    folder = job["folder"]
    prefix = folder + "/"
    local = {name[len(prefix):]: pin for name, pin in graph.items()
             if name.startswith(prefix) and "/" not in name[len(prefix):]}
    need(job["script"] in local, "Pinned actual-index native acceptance script")
    sources = {name: pin for name, pin in local.items() if name.endswith(".py")}
    if job["kind"] == "fixed_component":
        manifest_name = job["component"] + "_manifest.json"
        need(manifest_name in local, "Original mathematical fixed-object manifest")
        manifest = load(member(archive, prefix + manifest_name, local[manifest_name]))
        need(manifest["component"] == job["component"]
             and set(manifest) == {"schema", "component", "sources", "proof", "inputs"},
             "Entire original fixed-object source/proof/input manifest")
        sources[manifest_name] = local[manifest_name]
        for group in ("sources", "proof", "inputs"):
            for name, pin in manifest[group].items():
                flat(name)
                need(local.get(name) == pin, "Native fixed-object input/final source graph agreement")
                sources[name] = pin
        need(len(manifest["proof"]) == 1, "One complete independently recomputed fixed object")
        proof_name = next(iter(manifest["proof"]))
        job = dict(job, proof=proof_name, manifest=manifest_name)
    else:
        # These original read-only comparison families do not generate any
        # source-local files. Preserve all their pinned flat mathematical
        # inputs, including the exact finite binomial tables and full witnesses.
        sources.update({name: pin for name, pin in local.items() if name.endswith(".json")})
        need(job["proof"] in sources and "fixed_inputs.json" in sources,
             "Full original finite-comparison proof and fixed inputs")
        fixed = load(member(archive, prefix + "fixed_inputs.json", sources["fixed_inputs.json"]))
        for name, pin in fixed.items():
            need(sources.get(flat(name)) == pin, "Every original comparison fixed input")
    need(not any(name.startswith("accepted_") or name in ("READBACK.json", "metadata.json") for name in sources),
         "No old acceptance/capture is a new mathematical premise")
    return dict(job, sources_sha256=sources, original_record_sha256=RECORD_SHA,
                same_witness_and_parent_acquisitions_verified=False)


def catalog(archive):
    record = load(member(archive, RECORD, RECORD_SHA, 8 * 1024 ** 2))
    graph = record["files_sha256"]
    need(len(graph) == 9518 and record["fully_reproduced_historical_dependency_DAG"] is False,
         "Exact retained-source scope")
    jobs = [selected_inputs(archive, graph, job) for job in definitions()]
    need(len(jobs) == 10 and len({j["id"] for j in jobs}) == 10, "All ten actual-index native jobs")
    return jobs, graph


def final_json(text):
    decoder = json.JSONDecoder(object_pairs_hook=unique)
    # Use our duplicate-key rejecting loader for the final complete object;
    # progress lines before it are not mathematical result objects.
    for index in reversed([i for i, char in enumerate(text) if char == "{" and (i == 0 or text[i - 1] == "\n")]):
        try:
            _, size = decoder.raw_decode(text[index:])
            if not text[index + size:].strip():
                result = load(text[index:index + size])
                need(type(result) is dict, "Complete native result object")
                return result
        except (ValueError, TypeError):
            continue
    raise ValueError("No complete final native JSON result")


def validate_result(job, result):
    need(result["status"] == job["expected_status"], "Exact original native actual-index scope/status")
    need(result["proof_sha256"] == job["sources_sha256"][job["proof"]], "Entire fixed proof was accepted")
    controls = result["negative_controls"]
    if job["kind"] == "fixed_component":
        need(type(controls) is int and controls == job["negative_controls"]
             and result["source_manifest_sha256"] == job["sources_sha256"][job["manifest"]],
             "All original fixed-object controls and source manifest")
    else:
        need(type(controls) is list and all(type(control) is str for control in controls)
             and len(controls) == len(set(controls)) == job["negative_controls"],
             "All original finite-comparison corruption controls")
        def positive_rational(value):
            need(type(value) is str, "Native exact reserve must be a rational string")
            number = Fraction(value)
            need(str(number) == value and number > 0, "Canonical strictly positive native reserve")
            return number
        if job["kind"] == "tiny":
            need(type(result["rows"]) is int and result["rows"] == job["rows"]
                 and type(result["phase_cases"]) is int and result["phase_cases"] == 6 * job["rows"]
                 and positive_rational(result["minimum_reserve"]) > 0
                 and result["acceptor_sha256"] == job["sources_sha256"][job["script"]],
                 "Complete closed tiny phase cover, positive reserve and original acceptor")
        else:
            need(type(result["blocks"]) is int and result["blocks"] > 0
                 and type(result["phase_cells"]) is int and result["phase_cells"] > 0
                 and positive_rational(result["minimum"]) > 0,
                 "Every native MID context and closed phase cell strictly accepted")
    return result
