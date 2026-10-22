"""Checked source catalog for12 INITIAL and15 resource jobs; NOT a replay.

No native module is imported and no numerical evaluator is called. Historical
receipts select immutable source closures only. They are not fresh premises.
An eventual replay controller MUST join every recomputed child to genuinely
fresh parent facts, including exact domains and candidate-input identities.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import importlib.util
import json
from pathlib import Path
import sys

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from .c5_high_one import read, source_at
    from .c5_inputs import extended, safe_relative
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from c5_high_one import read, source_at
    from c5_inputs import extended, safe_relative

sys.dont_write_bytecode = True
ENTRY = "work/cutoff5_20261020/entry/"
ALL_PANELS = tuple(range(100))


@dataclass(frozen=True)
class Job:
    job_id: str
    kind: str
    family: str
    case: str
    band: str
    sector: int | None
    arguments: tuple[str, ...]
    stages: int | None
    indices: tuple[int, ...]
    initial_parent: str | None
    owncap: str
    high: str
    expected_status: str
    source_index_files: int
    capture: str | None = None
    n: int = 5

    def __post_init__(self):
        need(type(self.n) is int and self.n == 5, "Literal sample size5, not Boolean")
        need(self.kind in ("initial", "resource"), "Declared acquisition kind")
        need(self.band in ("B0", "BN", "B2", "B3"), "Declared moment branch")
        need(self.sector is None or (type(self.sector) is int and 0 <= self.sector <= 3),
             "Literal sector, not Boolean")
        need(type(self.arguments) is tuple and all(type(x) is str for x in self.arguments),
             "Exact immutable native CLI arguments")
        need(type(self.indices) is tuple and self.indices and
             all(type(x) is int and 0 <= x < 100 for x in self.indices)
             and tuple(sorted(set(self.indices))) == self.indices, "Ordered literal p panels")
        need(type(self.source_index_files) is int and self.source_index_files > 0,
             "Positive fixed source-index census")
        for path in (self.directory, self.case_directory, self.prepared, self.source_index):
            safe_relative(path)
        if self.kind == "initial":
            need(type(self.stages) is int and self.stages in (4, 9)
                 and self.initial_parent is None and self.capture is None,
                 "INITIAL finite-stage and parent contract")
        else:
            need(self.stages is None and type(self.initial_parent) is str
                 and type(self.capture) is str, "Resource requires its INITIAL and actual capture")
            safe_relative(self.capture)

    @property
    def directory(self):
        return ENTRY + self.family

    @property
    def case_directory(self):
        return self.directory + "/" + self.case

    @property
    def prepared(self):
        return self.case_directory + "/PREPARED.json"

    @property
    def source_index(self):
        return self.prepared if self.kind == "initial" else self.case_directory + "/REPLAY_CHECKED.json"

    @property
    def output_paths(self):
        names = ("REPLAY_CHECKED.json",) if self.kind == "initial" else ("REPLAY.json", "REPLAY_CHECKED.json")
        return tuple(self.case_directory + "/" + name for name in names)

    @property
    def commands(self):
        commands = (("-B", "replay.py", *self.arguments),)
        return commands if self.kind == "initial" else commands + (("-B", "accept.py", *self.arguments),)

    @property
    def fresh_outputs_to_exclude(self):
        result = self.output_paths
        if self.capture is not None:
            result += tuple(self.capture + "/" + name for name in ("metadata.json", "stdout.txt", "stderr.txt"))
        return result

    @property
    def required_fresh_fact_joins(self):
        parents = ("n4: all-law C4<=CE under written analytic reduction",
                   "c5.support: same-law q0 acquired support containing the exact profile",
                   "c5.high: same-n full HIGH upper on a containing rho/support domain",
                   "c5.owncaps: same-n cap on a containing rho/support domain")
        if self.kind == "initial" and self.band in ("B0", "BN"):
            parents += ("coarse429: freshly replayed global C5<429/1000, not a supplied status",)
        if self.initial_parent is not None:
            parents += (self.initial_parent + ": fresh INPUT SHA, full profile, stages and domain match",)
        if self.kind == "resource":
            parents += ("Fresh result and original candidate agree at every selected panel",
                        "Historical parent hashes/statuses are references, never new arithmetic",
                        "Any signed-gamma/endpoint/B3 kernel-port analytic premises remain explicit")
        return parents


def initial(job_id, family, case, band, sector, stages, owncap, high, status, files):
    args = ("5", band) if sector is None else ("5", band, str(sector))
    return Job(job_id, "initial", family, case, band, sector, args, stages,
               ALL_PANELS, None, owncap, high, status, files)


INITIAL_JOBS = (
    initial("initial.B0", "initial5_accept_v1", "n5_B0", "B0", None, 9, "429/1000", "337/1000", "PASS_FRESH_CONDITIONAL_FULL_INITIAL5_ACQUISITION", 82),
    initial("initial.BN", "initial5_accept_v1", "n5_BN", "BN", None, 9, "429/1000", "369/1000", "PASS_FRESH_CONDITIONAL_FULL_INITIAL5_ACQUISITION", 82),
    initial("initial.B2.S0", "initial5_partition_accept_v1", "n5_B2_S0", "B2", 0, 9, "52/125", "393/1000", "PASS_FRESH_CONDITIONAL_INITIAL5_SECTOR_ACQUISITION", 84),
    initial("initial.B2.S1", "initial5_partition_accept_v1", "n5_B2_S1", "B2", 1, 9, "52/125", "393/1000", "PASS_FRESH_CONDITIONAL_INITIAL5_SECTOR_ACQUISITION", 84),
    initial("initial.B2.S2", "initial5_partition_short_accept_v2", "n5_B2_S2", "B2", 2, 4, "52/125", "393/1000", "PASS_FRESH_CONDITIONAL_INITIAL5_SECTOR_ACQUISITION", 84),
    initial("initial.B2.S3", "initial5_partition_accept_v1", "n5_B2_S3", "B2", 3, 9, "52/125", "393/1000", "PASS_FRESH_CONDITIONAL_INITIAL5_SECTOR_ACQUISITION", 84),
    initial("initial.B3.S0", "initial5_partition_short_accept_v2", "n5_B3_S0", "B3", 0, 4, "207/500", "193/500", "PASS_FRESH_CONDITIONAL_INITIAL5_SECTOR_ACQUISITION", 84),
    initial("initial.B3.S2", "initial5_partition_short_accept_v2", "n5_B3_S2", "B3", 2, 4, "207/500", "193/500", "PASS_FRESH_CONDITIONAL_INITIAL5_SECTOR_ACQUISITION", 84),
    initial("initial.B3.T0", "initial5_B3_top_accept_v3", "n5_B3_T0", "B3", 0, 4, "103/250", "193/500", "PASS_FRESH_CONDITIONAL_INITIAL5_TOPBETA_SECTOR_ACQUISITION", 84),
    initial("initial.B3.T1", "initial5_B3_top_accept_v3", "n5_B3_T1", "B3", 1, 4, "103/250", "193/500", "PASS_FRESH_CONDITIONAL_INITIAL5_TOPBETA_SECTOR_ACQUISITION", 84),
    initial("initial.B3.T2", "initial5_B3_top_accept_v3", "n5_B3_T2", "B3", 2, 4, "103/250", "193/500", "PASS_FRESH_CONDITIONAL_INITIAL5_TOPBETA_SECTOR_ACQUISITION", 84),
    initial("initial.B3.T3lower", "initial5_B3_T3lower_accept_v1", "n5_B3_T3lower", "B3", 3, 4, "103/250", "193/500", "PASS_FRESH_CONDITIONAL_INITIAL5_T3LOWER_SECTOR_ACQUISITION", 89),
)


def resource(job_id, family, case, band, sector, arguments, indices, parent,
             owncap, high, status, files, capture_name):
    return Job(job_id, "resource", family, case, band, sector, tuple(arguments), None,
               tuple(indices), parent, owncap, high, status, files,
               "runs/cutoff5_20261020/entry/" + capture_name)


RESOURCE_JOBS = (
    resource("resource.B0.selected", "resource5_selected_accept_v1", "B0", "B0", None, ("B0",), [i for i in ALL_PANELS if i not in range(37, 46)], "initial.B0", "53/125", "337/1000", "PASS_FRESH_CONDITIONAL_SELECTED_RESOURCE5_ACQUISITION", 443, "resource5_B0_selected_replay01"),
    resource("resource.BN.selected", "resource5_selected_accept_v1", "BN", "BN", None, ("BN",), [i for i in ALL_PANELS if i not in range(34, 41)], "initial.BN", "21/50", "369/1000", "PASS_FRESH_CONDITIONAL_SELECTED_RESOURCE5_ACQUISITION", 443, "resource5_BN_selected_replay01"),
    resource("resource.B0.gamma", "resource5_gamma_accept_v1", "B0", "B0", None, ("B0",), range(37, 46), "initial.B0", "53/125", "337/1000", "PASS_FRESH_CONDITIONAL_GAMMA_RESOURCE5_ACQUISITION", 561, "resource5_B0_gamma_replay01"),
    resource("resource.BN.gamma", "resource5_gamma_accept_v1", "BN", "BN", None, ("BN",), range(34, 41), "initial.BN", "21/50", "369/1000", "PASS_FRESH_CONDITIONAL_GAMMA_RESOURCE5_ACQUISITION", 557, "resource5_BN_gamma_replay01"),
    *(resource("resource.B2.S" + str(s) + ".base", "resource5_sector_accept_v1", "B2_S" + str(s) + "_base", "B2", s, (str(s), "base"), [i for i in ALL_PANELS if s != 3 or i not in (32, 33, 34)], "initial.B2.S" + str(s), "52/125", "377/1000", "PASS_FRESH_CONDITIONAL_SELECTED_SECTOR5_RESOURCE_ACQUISITION", 497 if s == 3 else 503, "resource5_B2_S" + str(s) + "_base_replay01") for s in range(4)),
    resource("resource.B2.S3.endpoint", "resource5_sector_accept_v1", "B2_S3_endpoint", "B2", 3, ("3", "endpoint"), (32, 33, 34), "initial.B2.S3", "52/125", "377/1000", "PASS_FRESH_CONDITIONAL_SELECTED_SECTOR5_RESOURCE_ACQUISITION", 339, "resource5_B2_S3_endpoint_replay01"),
    *(resource("resource.B3." + case, "resource5_B3_accept_v1", "B3_" + case, "B3", int(case[1]), (case,), ALL_PANELS, "initial.B3." + case, "103/250", "193/500", "PASS_FRESH_CONDITIONAL_B3_SECTOR5_RESOURCE_ACQUISITION", 672, "resource5_B3_" + case + "_replay01") for case in ("S0", "S2", "T0", "T1", "T2")),
    resource("resource.B3.T3lower", "resource5_B3_T3lower_accept_v1", "B3_T3lower", "B3", 3, ("T3lower",), ALL_PANELS, "initial.B3.T3lower", "103/250", "193/500", "PASS_FRESH_CONDITIONAL_B3_T3LOWER_RESOURCE_ACQUISITION", 741, "resource5_B3_T3lower_replay01"),
)
JOBS = INITIAL_JOBS + RESOURCE_JOBS


def validate_catalog(jobs=JOBS):
    need(len(jobs) == 27 and len({job.job_id for job in jobs}) == 27,
         "Exactly27 unique selected acquisition jobs")
    initials = {job.job_id: job for job in jobs if job.kind == "initial"}
    resources = [job for job in jobs if job.kind == "resource"]
    need(len(initials) == 12 and len(resources) == 15, "Exactly12 INITIAL and15 resource jobs")
    cover = {name: [] for name in initials}
    for job in resources:
        need(job.initial_parent in initials, "Every resource has a selected INITIAL parent")
        parent = initials[job.initial_parent]
        need(parent.n == job.n and parent.band == job.band and parent.sector == job.sector,
             "Exact resource/INITIAL literal scope")
        cover[job.initial_parent].extend(job.indices)
    need(all(sorted(indices) == list(ALL_PANELS) for indices in cover.values()),
         "Each selected INITIAL branch has exactly100 resource-panel obligations")


def description(job):
    result = asdict(job)
    result.update(directory=job.directory, prepared=job.prepared,
                  source_index=job.source_index, outputs=job.output_paths,
                  commands=job.commands, fresh_outputs_to_exclude=job.fresh_outputs_to_exclude,
                  closure_selector=("PREPARED.files_sha256 + explicit local control files"
                                    if job.kind == "initial" else
                                    "Historical own REPLAY_CHECKED.files_sha256 as source-index ONLY; exclude fresh outputs/capture"),
                  required_fresh_fact_joins=job.required_fresh_fact_joins,
                  fresh_parent_fact_joins_implemented=False)
    return result


def plan():
    validate_catalog()
    return {"scope": "C5_ACQUISITION_PLAN_ONLY_NOT_NUMERICAL_REPLAY",
            "original_final_graph_sha256": FINAL_SHA,
            "initial_jobs": 12, "resource_jobs": 15,
            "resource_probability_panel_obligations": sum(len(job.indices) for job in RESOURCE_JOBS),
            "jobs": [description(job) for job in JOBS],
            "arithmetic_executed": False, "arithmetic_accepted": False,
            "fresh_parent_fact_joins_implemented": False,
            "all_index_conclusion_verified": False}


def inspect_job(cache, graph, job, checked=None, guard=lambda: None):
    """Verify only exact bytes, runtime closure and the selected immutable plan."""
    checked = {} if checked is None else checked
    def bound(name):
        safe_relative(name)
        need(name in graph, "Source index absent from pinned FINAL: " + name)
        path = source_at(cache, name)
        if name not in checked:
            guard()
            need(digest(path) == graph[name], "Exact selected source bytes: " + name)
            checked[name] = path.stat().st_size
        return path
    prepared_path = bound(job.prepared)
    prepared = read(prepared_path)
    need(type(prepared.get("n")) is int and prepared["n"] == 5
         and prepared.get("band") == job.band, "Prepared literal n/band")
    if job.sector is not None:
        scoped = prepared.get("source_job", prepared)
        need(type(scoped.get("sector")) is int and scoped["sector"] == job.sector,
             "Prepared literal sector")
    source_index_path = bound(job.source_index)
    index = read(source_index_path)
    primary = index["files_sha256"]
    need(type(primary) is dict and len(primary) == job.source_index_files,
         "Exact selected source-index census")
    for name, pin in primary.items():
        need(graph.get(name) == pin, "Selected closure has exact FINAL member identity")
        bound(name)
    excluded = set(job.fresh_outputs_to_exclude)
    need(not (excluded & set(prepared["files_sha256"])),
         "A mandatory frozen prepared input cannot be omitted as a fresh output")
    closure = {name: pin for name, pin in primary.items() if name not in excluded}
    extra = [job.prepared]
    if job.kind == "initial":
        extra += [job.case_directory + "/INPUT.json"]
        extra += [job.directory + "/" + name for name in
                  ("replay.py", "prepare.py", "PROOF.txt", "SOURCE_PREPARED.json")]
        engine = source_at(cache, job.directory + "/engine/initial34_indexed.py").parent
        runtime = list(engine.glob("*.py"))
        need(len(runtime) == 20, "All20 original INITIAL runtime modules")
        for path in runtime:
            name = path.relative_to(cache).as_posix()
            need(prepared["files_sha256"].get(name) == graph.get(name),
                 "Every original INITIAL runtime module is loader-bound")
        need(index["n"] == 5 and index["band"] == job.band, "INITIAL prepared source-index identity")
    else:
        extra += [job.directory + "/" + name for name in ("common.py", "replay.py", "accept.py", "PROOF.txt")]
        need(index["status"] == job.expected_status and type(index["n"]) is int and index["n"] == 5,
             "Historical source-index identity only, NOT a new arithmetic acceptance")
    for name in extra:
        need(name not in excluded, "No old own output selected as source control")
        bound(name)
        closure[name] = graph[name]
    for name, pin in prepared["files_sha256"].items():
        need(closure.get(name) == pin, "Complete mandatory prepared input closure")
    total = sum(bound(name).stat().st_size for name in closure)
    need(total <= 128 * 1024**2, "Selected mirror inputs leave room under original256MiB scratch quota")
    return {"job_id": job.job_id, "source_index_sha256": graph[job.source_index],
            "prepared_sha256": graph[job.prepared],
            "verified_source_index_files": len(primary), "mirror_source_files": len(closure),
            "mirror_input_bytes": total,
            "fresh_output_paths_excluded": sorted(excluded),
            "fresh_parent_fact_joins_required": True, "arithmetic_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect-cache", type=Path,
                        help="Check pinned source bytes only; no checker is run")
    parser.add_argument("--job", choices=tuple(job.job_id for job in JOBS),
                        help="Optionally inspect exactly one selected job")
    args = parser.parse_args()
    need(__debug__ and not sys.flags.optimize, "Ordinary nonoptimized source inspection")
    result = plan()
    if args.inspect_cache is not None:
        spec = importlib.util.spec_from_file_location("catalog_resource_observer", BASE / "run_reproduction.py")
        observer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(observer)
        observer.HOST_FLOOR = 1024 * observer.MIB
        def guard():
            observer.parent_guard()
        guard()
        cache = extended(args.inspect_cache)
        final = source_at(cache, FINAL)
        need(digest(final) == FINAL_SHA, "Pinned complete selected FINAL identity")
        graph = read(final)["files_sha256"]
        need(len(graph) == 16576, "Complete selected original source graph")
        checked = {}
        chosen = [job for job in JOBS if args.job is None or job.job_id == args.job]
        result["scope"] = "C5_ACQUISITION_SOURCE_CATALOG_INSPECTION_ONLY"
        result["inspected"] = [inspect_job(cache, graph, job, checked, guard) for job in chosen]
        result["distinct_source_bytes_checked"] = sum(checked.values())
        result["distinct_source_files_checked"] = len(checked)
        guard()
    elif args.job is not None:
        result["jobs"] = [description(job) for job in JOBS if job.job_id == args.job]
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_ACQUISITION_CATALOG_INCOMPLETE: " + str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
