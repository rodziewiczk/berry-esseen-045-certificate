"""Recompute all 295 selected C5 count forests; never certify their resource parents."""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import time
import zipfile

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
ARCHIVE_BYTES = 141304365
ARCHIVE_SHA = "8428002462d4e650613ea6e2ff673cb1e69c2079572cc40546d125349d582419"
INDEX = "cutoff5_20261020/entry/delivery_review_v1/SELECTED_REPLAY_COMMANDS.json"
INDEX_SHA = "74ca2086929fd68c92416f9c0acfe8c2dce08bd31a4a5e7388a95ffc49c70341"
PREFIX = "cutoff5_20261020/root/delivery_extract_v1/"
FINAL = "work/cutoff5_20261020/root/final_composition_v2/C5_CHECKED.json"
FINAL_SHA = "923a0d0cf3c481ae60c5e2b69d886098a7501f916a52668b37b0198f26fde4a0"
MIB = 1024**2


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON field")
        result[key] = value
    return result


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(MIB):
            h.update(chunk)
    return h.hexdigest()


def member(z, name, expected, maximum=16*MIB):
    info = z.getinfo(name)
    need(not info.is_dir() and info.file_size <= maximum, "Bounded exact archive member")
    need(not stat.S_ISLNK(info.external_attr >> 16), "No archived symlink")
    raw = z.read(info)
    need(hashlib.sha256(raw).hexdigest() == expected, "Member identity: "+name)
    return raw


def catalog(z):
    index = json.loads(member(z, INDEX, INDEX_SHA), object_pairs_hook=unique)
    final = json.loads(member(z, PREFIX+FINAL, FINAL_SHA), object_pairs_hook=unique)
    need(index["schema"] == "SELECTED_C5_REPLAY_COMMAND_INVENTORY_V1", "Selected index format")
    rows = index["count_acceptances"]
    need(type(rows) is list and len(rows) == 295, "All 295 selected forests")
    seen = set()
    for row in rows:
        need(row["command"] == ["PY", "-B", "count_protocol.py", "accept"],
             "Only selected exact acceptance, not discovery or a saved PASS")
        cwd = row["cwd"]
        need(re.fullmatch(r"work/[A-Za-z0-9_./-]+", cwd) is not None and
             all(p not in ("", ".", "..") for p in cwd.split("/")), "Safe original capsule path")
        need(type(row["index"]) is int and 0 <= row["index"] < 100, "Literal probability panel")
        need(cwd not in seen, "No duplicate selected count capsule")
        seen.add(cwd)
        for name, sha in row["files_sha256"].items():
            need(final["files_sha256"].get(name) == sha, "Count/final graph identity agreement")
    return rows, final["files_sha256"]


def prepare_capsule(z, row, graph, work):
    destination = work/"capsule"
    destination.mkdir(exist_ok=False)
    original_prefix = row["cwd"]+"/"
    copied = {}
    for original, sha in graph.items():
        if not original.startswith(original_prefix):
            continue
        tail = original[len(original_prefix):]
        need(PurePosixPath(tail).name == tail and tail not in ("", ".", ".."),
             "Flat complete capsule, no inferred path rewriting")
        raw = member(z, PREFIX+original, sha)
        # An old acceptance is provenance only, never fresh mathematical input.
        if tail == "COUNT_ACCEPTED.json":
            continue
        with (destination/tail).open("xb") as stream:
            stream.write(raw)
        copied[tail] = sha
    need(all(name in copied for name in
             ("count_protocol.py", "KERNEL_COPY_MANIFEST.json", "contract.json", "COUNT_FOREST.json")),
         "Complete unchanged protocol, kernel manifest, contract and forest")
    manifest = json.loads((destination/"KERNEL_COPY_MANIFEST.json").read_text(),
                          object_pairs_hook=unique)
    for name, sha in manifest["files"].items():
        need(copied.get(name) == sha, "Every frozen kernel input supplied")
    for original, sha in row["files_sha256"].items():
        name = PurePosixPath(original).name
        if name != "COUNT_ACCEPTED.json":
            need(copied.get(name) == sha, "Exact selected non-receipt input")
    return destination, copied


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    archive = args.archive.resolve()
    need(archive.is_file() and not archive.is_symlink(), "Explicit regular pinned source archive")
    need(archive.stat().st_size == ARCHIVE_BYTES and digest(archive) == ARCHIVE_SHA,
         "Exact public C5 source asset, not a substituted candidate")
    spec = importlib.util.spec_from_file_location("original_runner", BASE/"run_reproduction.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    def guard():
        need(r.own_peak() <= 256*MIB, "Archive coordinator peak at most 256 MiB")
        need(r.available_ram() >= 1024*MIB, "Host free RAM at least 1 GiB")
    guard()
    r.verify_sources()
    started = time.monotonic()
    with zipfile.ZipFile(archive) as z:
        rows, graph = catalog(z)
        guard()
        if args.inspect:
            print(json.dumps({"scope":"PINNED_C5_COUNT_INPUT_CATALOG_ONLY",
                              "selected_forests":len(rows),
                              "arithmetic_replayed":False,
                              "all_index_conclusion_verified":False}))
            return
        run = r.private_work()
        progress = (run/"C5_COUNTS_PROGRESS.jsonl").open("x", encoding="utf-8")
        nodes = leaves = 0
        for ordinal, row in enumerate(rows):
            guard()
            work = r.private_work()
            capsule, copied = prepare_capsule(z, row, graph, work)
            # ZIP central-directory metadata has a different memory budget
            # from the small native supervisor. Never relax its 64-MiB guard.
            child = None
            try:
                with (work/"SUPERVISOR.log").open("xb") as log:
                    child = subprocess.Popen(
                        [sys.executable, "-B", "-S", str(Path(__file__).with_name("c5_count_one.py")),
                         "--work", str(work)],
                        cwd=BASE, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                        **({"creationflags":subprocess.CREATE_NO_WINDOW} if sys.platform == "win32"
                           else {"start_new_session":True}))
                    while child.poll() is None:
                        guard()
                        need(log.tell() <= 16*MIB, "Bounded supervisor log")
                        time.sleep(.25)
                need(child.returncode == 0, "Complete fresh native count process: "+str(ordinal))
            finally:
                if child is not None and child.poll() is None:
                    child.terminate()
                    child.wait(timeout=10)
            # Output is recomputed by the pinned full-root exact oracle,
            # including its mutation controls; never imported from old receipts.
            fresh = capsule/"COUNT_ACCEPTED.json"
            need(fresh.is_file(), "Fresh native acceptance required")
            packet = json.loads(fresh.read_text(), object_pairs_hook=unique)
            need(type(packet["n"]) is int and packet["n"] == 5 and
                 type(packet["index"]) is int and packet["index"] == row["index"],
                 "Actual five, literal selected probability panel")
            need(packet["status"].startswith("PASS_FRESH_CONDITIONAL_"), "Native conditional count acceptance")
            need(packet["forest_sha256"] == copied["COUNT_FOREST.json"] and
                 packet["contract_sha256"] == copied["contract.json"] and
                 packet["checker_sha256"] == copied["count_protocol.py"], "Native input bindings")
            need(packet["kernel_sha256"] == json.loads(
                (capsule/"KERNEL_COPY_MANIFEST.json").read_text(),
                object_pairs_hook=unique)["files"], "Full native kernel bindings")
            statistics = packet["statistics"]
            need(type(statistics["nodes"]) is int and type(statistics["leaves"]) is int and
                 0 < statistics["leaves"] <= statistics["nodes"] and
                 packet["fresh_leaf_evaluations"] == statistics["leaves"] and
                 len(packet["negative_controls"]) >= 20, "All leaves and corruption controls replayed")
            # Recheck immutable inputs after the child returns.
            need(all(digest(capsule/name) == sha for name, sha in copied.items()),
                 "No source or forest changed during replay")
            guard()
            nodes += statistics["nodes"]
            leaves += statistics["leaves"]
            event = {"ordinal":ordinal, "original_capsule":row["cwd"],
                     "receipt":str(fresh.relative_to(BASE)), "nodes":statistics["nodes"],
                     "leaves":statistics["leaves"], "receipt_sha256":digest(fresh)}
            progress.write(json.dumps(event)+"\n")
            progress.flush()
            print(json.dumps({"event":"c5_count_replayed", **event}), flush=True)
        need((len(rows), nodes, leaves) == (295,148586,75178), "Entire selected count census")
        progress.close()
        result = {"scope":"ALL_295_C5_COUNT_FORESTS_FRESHLY_REPLAYED",
                  "forests":295, "original_count_roots":1770, "nodes":nodes, "leaves":leaves,
                  "source_archive_sha256":ARCHIVE_SHA,
                  "source_index_sha256":INDEX_SHA, "wall_seconds":time.monotonic()-started,
                  "resource_support_fourier_initial_and_gapfree_verified_by_this_stage":False,
                  "all_index_conclusion_verified":False}
        with (run/"C5_COUNTS_RESULT.json").open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_COUNT_REPLAY_INCOMPLETE: "+str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
