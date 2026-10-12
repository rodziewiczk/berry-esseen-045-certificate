"""Package the exact transitive input closure; this does NOT replay arithmetic."""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
import time
import zipfile

SOURCE_ARCHIVE_SHA = "17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb"
RECORD_SHA = "33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9"
RECORD_PATH = "continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json"
PREFIX = "cutoff25_20261011/"
CHUNK = 512 * 1024
PART_LIMIT = 48 * 1024 * 1024
START = time.process_time()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard():
    require(time.process_time() - START < 600, "packaging CPU limit")
    if os.name == "nt":
        class Memory(ctypes.Structure):
            _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong),
                        ("total", ctypes.c_ulonglong), ("available", ctypes.c_ulonglong),
                        ("page_total", ctypes.c_ulonglong), ("page_available", ctypes.c_ulonglong),
                        ("virtual_total", ctypes.c_ulonglong), ("virtual_available", ctypes.c_ulonglong),
                        ("extended", ctypes.c_ulonglong)]
        memory = Memory()
        memory.length = ctypes.sizeof(memory)
        require(ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)), "RAM reading")
        require(memory.available >= 768 * 1024 * 1024, "host RAM floor")


def stream_hash(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(CHUNK):
            guard()
            h.update(chunk)
    return h.hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def safe_name(name):
    require(isinstance(name, str) and name and "\\" not in name and "\x00" not in name,
            "portable archive name")
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and ":" not in name,
            "archive path stays inside capsule")
    return name


def build(archive_path, record_path, output, scratch):
    require(not output.exists(), "fresh output directory required")
    require(not scratch.exists(), "fresh scratch archive required")
    require(stream_hash(archive_path) == SOURCE_ARCHIVE_SHA, "source archive SHA")
    with record_path.open("rb") as source:
        raw = source.read(4 * 1024 * 1024 + 1)
    require(len(raw) <= 4 * 1024 * 1024 and hashlib.sha256(raw).hexdigest() == RECORD_SHA,
            "final retained-scope record SHA")
    record = json.loads(raw, object_pairs_hook=unique)
    require(record["status"] == "PASS_EVENTUAL_CUTOFF31_AT_EXPLICIT_RETAINED_SCOPE"
            and record["cutoff"] == 31, "matching statement")
    require(record["fully_reproduced_historical_dependency_DAG"] is False,
            "preserve historical execution scope")
    commitments = record["files_sha256"]
    require(isinstance(commitments, dict) and len(commitments) == 9518, "complete bound closure")
    for name in commitments:
        safe_name(name)
    require(RECORD_PATH not in commitments, "record must not bind itself")
    scratch.parent.mkdir(parents=True, exist_ok=True)
    expanded = 0
    with zipfile.ZipFile(archive_path) as source_zip:
        index = {}
        for info in source_zip.infolist():
            guard()
            require(info.filename not in index, "unique source ZIP member")
            index[info.filename] = info
        require(all(PREFIX + name in index for name in commitments), "every committed input supplied")
        with scratch.open("xb") as file:
            with zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as capsule:
                for number, name in enumerate(sorted(commitments), 1):
                    info = index[PREFIX + name]
                    require(info.file_size <= 64 * 1024 * 1024, "per-member cap")
                    expanded += info.file_size
                    require(expanded <= 2 * 1024**3, "expanded payload cap")
                    target = zipfile.ZipInfo(name, date_time=(2026, 10, 12, 0, 0, 0))
                    target.compress_type = zipfile.ZIP_DEFLATED
                    target.external_attr = 0o100644 << 16
                    h = hashlib.sha256()
                    count = 0
                    with source_zip.open(info) as src, capsule.open(target, "w", force_zip64=True) as dst:
                        while chunk := src.read(CHUNK):
                            guard()
                            count += len(chunk)
                            require(count <= info.file_size, "bounded original member")
                            h.update(chunk)
                            dst.write(chunk)
                    require(count == info.file_size and h.hexdigest() == commitments[name],
                            "exact committed member: " + name)
                    if number % 500 == 0:
                        print(json.dumps({"phase": "PACKAGING_NOT_ARITHMETIC_REPLAY", "files": number}),
                              flush=True)
                target = zipfile.ZipInfo(RECORD_PATH, date_time=(2026, 10, 12, 0, 0, 0))
                target.compress_type = zipfile.ZIP_DEFLATED
                target.external_attr = 0o100644 << 16
                capsule.writestr(target, raw)
    output.mkdir(parents=True)
    parts = []
    whole_hash = hashlib.sha256()
    with scratch.open("rb") as src:
        number = 1
        while True:
            first = src.read(CHUNK)
            if not first:
                break
            name = f"closure31.zip.{number:03d}"
            h = hashlib.sha256()
            count = 0
            with (output / name).open("xb") as dst:
                chunk = first
                while chunk:
                    guard()
                    dst.write(chunk)
                    h.update(chunk)
                    whole_hash.update(chunk)
                    count += len(chunk)
                    if count == PART_LIMIT:
                        break
                    chunk = src.read(min(CHUNK, PART_LIMIT - count))
            parts.append({"name": name, "size": count, "sha256": h.hexdigest()})
            number += 1
    require(len(parts) <= 8 and scratch.stat().st_size <= 384 * 1024**2,
            "published package fits consumer limits")
    manifest = {"format": "exact-closure31-split-zip-v1", "source_archive_sha256": SOURCE_ARCHIVE_SHA,
                "record_path": RECORD_PATH, "record_sha256": RECORD_SHA,
                "bound_input_count": len(commitments), "zip_member_count": len(commitments) + 1,
                "expanded_bytes": expanded + len(raw), "zip_size": scratch.stat().st_size,
                "zip_sha256": whole_hash.hexdigest(), "parts": parts,
                "operation": "EXACT_BYTE_PACKAGING_NOT_ARITHMETIC_REPLAY",
                "fully_reproduced_historical_dependency_DAG": False}
    with (output / "manifest.json").open("x", encoding="utf-8", newline="\n") as dest:
        json.dump(manifest, dest, indent=2)
        dest.write("\n")
    guard()
    print(json.dumps({"status": "PACKAGED_ALL_9518_BOUND_INPUTS", "parts": len(parts),
                      "zip_bytes": manifest["zip_size"], "expanded_bytes": manifest["expanded_bytes"],
                      "arithmetic_replay_performed": False}), flush=True)


if __name__ == "__main__":
    require(__debug__ and not sys.flags.optimize, "ordinary Python required")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    build(args.archive.resolve(), args.record.resolve(), args.output.resolve(), args.scratch.resolve())
