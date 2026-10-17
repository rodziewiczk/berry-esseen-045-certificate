"""Inspect transport integrity only; never execute a mathematical checker."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile


ARCHIVE_NAME = "continuation_cutoff20_20261016_final.zip"
ARCHIVE_SHA256 = "1e3de8f03c28816d36258ddd84ee7f29166622b2390d5c3457eb1b193ef608b7"
PREFIX = "continuation_cutoff20_20261016/"
PINNED_ENTRIES = {
    "b0/sequential_synthesis_v8/CONDITIONAL_CUTOFF20_COMPOSED.json":
        "0247c2bbf7df6d101239818f097647e94f5f7a9fdef8ae49a60ebc71ed88ee08",
    "root/FINAL_CHAIN_READBACK.json":
        "df5f9983f6f682a01edda8fae612acda85e620fa1657cfee157ebab1c5510fd2",
    "analytic/SEQUENTIAL_CUTOFF20_FINAL_OUTPUT_REVIEW.json":
        "8ec666af11411d53be0c677d42581f2e4eb452f2dd7195d4373000e664aef237",
}


def stream_sha256(stream) -> str:
    digest = hashlib.sha256()
    while chunk := stream.read(1024 * 1024):
        digest.update(chunk)
    return digest.hexdigest()


def inspect_archive(path: Path) -> dict:
    with path.open("rb") as stream:
        if stream_sha256(stream) != ARCHIVE_SHA256:
            raise ValueError("Archive SHA-256 mismatch; no contents were trusted")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP entry")
        for relative, expected in PINNED_ENTRIES.items():
            entry = archive.getinfo(PREFIX + relative)
            if entry.file_size > 64 * 1024 * 1024:
                raise ValueError("Pinned entry exceeds its bounded inspection size")
            with archive.open(entry) as stream:
                if stream_sha256(stream) != expected:
                    raise ValueError("Pinned entry SHA-256 mismatch: " + relative)
        status_entry = archive.getinfo(PREFIX + "CURRENT_STATUS.json")
        if status_entry.file_size > 64 * 1024:
            raise ValueError("Status exceeds its bounded inspection size")
        status = json.loads(archive.read(status_entry))
    if status.get("conditional_eventual_cutoff") != 20:
        raise ValueError("Unexpected conditional cutoff")
    if status.get("conditional_cutoff20_composed") is not True:
        raise ValueError("Conditional composition not recorded as complete")
    for key in ("unqualified_cutoff20_proved", "fully_rechecked_unconditional_theorem",
                "fully_reproduced_historical_dependency_DAG"):
        if status.get(key) is not False:
            raise ValueError("Original verification qualification changed: " + key)
    return status


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path,
                        default=Path(__file__).resolve().parent / ARCHIVE_NAME)
    args = parser.parse_args()
    status = inspect_archive(args.archive)
    print("PASS: archive and three pinned entries match their recorded hashes.")
    print("Recorded finite indices:", status["finite_indices_completed"])
    print("Recorded conditional cutoff: 20; unconditional proof flag: False.")
    print("INTEGRITY ONLY: no mathematical checker or archived code was executed.")


if __name__ == "__main__":
    main()
