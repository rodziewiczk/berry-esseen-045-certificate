"""Fetch the exact original BE49 archive; availability is not mathematics."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "reproduction"))
from uniform_tail.archive49_catalog import ARCHIVE_BYTES, ARCHIVE_SHA

ASSET = {"name": "BE_cutoff49_20260930.zip", "bytes": ARCHIVE_BYTES, "sha256": ARCHIVE_SHA}
RELEASE = {"repository": "rodziewiczk/berry-esseen-045-certificate",
           "release_tag": "cutoff49-sources-2026-10-22"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=BASE / "reproduction_inputs/uniform-tail-archives")
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    path = BASE / "five-summands-2026-10-20/download_sources.py"
    spec = importlib.util.spec_from_file_location("existing_bounded_source_downloader", path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    if args.download:
        args.directory.mkdir(parents=True, exist_ok=True)
        helper.download(RELEASE, ASSET, args.directory)
    else:
        helper.verify(args.directory / ASSET["name"], ASSET)
    print(json.dumps({"scope": "ORIGINAL_BE49_SOURCE_AVAILABILITY_ONLY", "asset": ASSET,
                      "release": RELEASE, "arithmetic_replayed": False}), flush=True)


if __name__ == "__main__":
    main()
