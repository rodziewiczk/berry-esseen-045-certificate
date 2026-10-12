"""Stream-check or extract the exact archival input closure. No arithmetic replay."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
RECORD_SHA = "33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9"
RECORD_PATH = "continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json"
MANIFEST_SHA = "15b5f6aaac658925995fe3663c7560687913644727f788d4d8d5a3caa90cce3e"
CHUNK = 512 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def safe_name(name):
    require(isinstance(name, str) and name and "\\" not in name and "\x00" not in name,
            "portable member name")
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts and ":" not in name,
            "relative member inside closure")
    return name


@contextmanager
def owned_scratch():
    root = (HERE.parent / "work" / "closure31-cache").resolve()
    require(root.is_relative_to(HERE.parent.resolve()), "scratch inside this checkout")
    root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="join-", dir=root)).resolve()
    require(temporary.parent == root, "resolved owned temporary directory")
    try:
        yield temporary
    finally:
        joined = temporary / "closure31.zip"
        if joined.exists():
            require(not joined.is_symlink() and joined.resolve().parent == temporary,
                    "cleanup only the owned temporary archive")
            joined.unlink()
        # Nonrecursive removal: any unexpected extra file is retained and fails.
        temporary.rmdir()


def check_or_extract(destination):
    root = HERE / "closure31"
    with (root / "manifest.json").open("rb") as source:
        manifest_bytes = source.read(16385)
    require(len(manifest_bytes) <= 16384, "bounded manifest")
    require(hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST_SHA, "pinned complete manifest")
    manifest = json.loads(manifest_bytes, object_pairs_hook=unique)
    require(manifest["format"] == "exact-closure31-split-zip-v1", "manifest format")
    require(manifest["record_sha256"] == RECORD_SHA and manifest["record_path"] == RECORD_PATH,
            "pinned retained-scope statement")
    require(manifest["bound_input_count"] == 9518 and manifest["zip_member_count"] == 9519,
            "complete input count")
    require(manifest["fully_reproduced_historical_dependency_DAG"] is False,
            "do not upgrade historical execution scope")
    parts = manifest["parts"]
    require(isinstance(parts, list) and 1 <= len(parts) <= 8, "bounded split archive")
    if destination is not None:
        destination = destination.resolve()
        require(not destination.exists(), "fresh extraction directory required; nothing is overwritten")
    # The temporary join stays inside this checkout; cleanup removes only the
    # exact newly generated archive and its empty directory, never recursively.
    with owned_scratch() as temporary:
        joined = Path(temporary) / "closure31.zip"
        whole = hashlib.sha256()
        size = 0
        with joined.open("xb") as out:
            for number, part in enumerate(parts, 1):
                require(part["name"] == f"closure31.zip.{number:03d}", "ordered parts")
                require(0 < part["size"] <= 48 * 1024**2, "part length cap")
                source = root / part["name"]
                require(source.stat().st_size == part["size"], "exact physical part length")
                h = hashlib.sha256()
                count = 0
                with source.open("rb") as inp:
                    while data := inp.read(CHUNK):
                        count += len(data)
                        require(count <= part["size"], "bounded part stream")
                        h.update(data)
                        whole.update(data)
                        out.write(data)
                require(count == part["size"] and h.hexdigest() == part["sha256"], "part SHA")
                size += count
        require(size == manifest["zip_size"] <= 384 * 1024**2, "joined length cap")
        require(whole.hexdigest() == manifest["zip_sha256"], "whole archive SHA")
        with zipfile.ZipFile(joined) as archive:
            infos = archive.infolist()
            require(len(infos) == 9519, "complete ZIP members")
            index = {}
            expanded = 0
            for info in infos:
                safe_name(info.filename)
                require(info.filename not in index and not info.is_dir(), "unique regular members")
                require((info.external_attr >> 16) & 0o170000 == 0o100000,
                        "no symlinks or special members")
                require(info.file_size <= 64 * 1024**2, "per-member size cap")
                expanded += info.file_size
                require(expanded <= 2 * 1024**3, "expanded closure cap")
                index[info.filename] = info
            require(expanded == manifest["expanded_bytes"], "expanded length")
            info = index[RECORD_PATH]
            require(info.file_size <= 4 * 1024**2, "record size cap")
            record_bytes = archive.read(info)
            require(hashlib.sha256(record_bytes).hexdigest() == RECORD_SHA, "exact statement bytes")
            record = json.loads(record_bytes, object_pairs_hook=unique)
            require(record["status"] == "PASS_EVENTUAL_CUTOFF31_AT_EXPLICIT_RETAINED_SCOPE"
                    and record["cutoff"] == 31, "retained-scope statement")
            require(record["fully_reproduced_historical_dependency_DAG"] is False,
                    "retain execution limitation")
            commitments = record["files_sha256"]
            require(len(commitments) == 9518 and set(index) == set(commitments) | {RECORD_PATH},
                    "exact transitive closure; no missing or extra member")
            if destination is not None:
                destination.mkdir(parents=True)
            for number, name in enumerate(sorted(index), 1):
                info = index[name]
                h = hashlib.sha256()
                count = 0
                target = None
                if destination is not None:
                    target = destination.joinpath(*PurePosixPath(name).parts)
                    require(target.resolve().is_relative_to(destination), "resolved extraction path")
                    target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as src:
                    if target is None:
                        while data := src.read(CHUNK):
                            count += len(data)
                            require(count <= info.file_size, "bounded member")
                            h.update(data)
                    else:
                        with target.open("xb") as out:
                            while data := src.read(CHUNK):
                                count += len(data)
                                require(count <= info.file_size, "bounded member")
                                h.update(data)
                                out.write(data)
                require(count == info.file_size, "exact member length")
                expected = RECORD_SHA if name == RECORD_PATH else commitments[name]
                require(h.hexdigest() == expected, "committed member SHA: " + name)
                if number % 1000 == 0:
                    print(json.dumps({"phase": "FILE_IDENTITIES_ONLY", "checked": number}), flush=True)
    print(json.dumps({"status": "PASS_FILE_IDENTITIES", "bound_inputs": 9518,
                      "arithmetic_replay_performed": False,
                      "fully_reproduced_historical_dependency_DAG": False,
                      "extraction": None if destination is None else str(destination)}), flush=True)


if __name__ == "__main__":
    require(__debug__ and not sys.flags.optimize, "ordinary Python required")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extract", type=Path, help="fresh directory; default checks without extraction")
    args = parser.parse_args()
    check_or_extract(args.extract)
