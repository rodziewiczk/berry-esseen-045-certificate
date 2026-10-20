"""Fetch and inspect pinned GitHub source assets; NOT a mathematical verifier."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import urllib.request
import zipfile


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path, entry: dict) -> None:
    if path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
        raise ValueError("Pinned size or hash mismatch: " + path.name)
    # Check the archive directory without extracting or executing anything.
    with zipfile.ZipFile(path) as archive:
        if not archive.infolist():
            raise ValueError("Empty source archive: " + path.name)


def download(manifest: dict, entry: dict, destination: Path) -> None:
    filename = entry["name"]
    if Path(filename).name != filename:
        raise ValueError("Invalid manifest filename")
    target = destination / filename
    if target.exists():
        verify(target, entry)
        print("Already verified:", filename, flush=True)
        return
    url = ("https://github.com/" + manifest["repository"] + "/releases/download/"
           + manifest["release_tag"] + "/" + filename)
    partial = destination / (filename + ".part")
    # Never overwrite an unverified pre-existing download.
    with partial.open("xb") as output:
        request = urllib.request.Request(url, headers={"User-Agent": "BerryEsseenSourceCapsule/1"})
        with urllib.request.urlopen(request, timeout=90) as response:
            total = 0
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > entry["bytes"]:
                    raise ValueError("Download larger than pinned size: " + filename)
                output.write(chunk)
    verify(partial, entry)
    # Exclusive creation also protects against a concurrent destination writer
    # on POSIX, where rename() could otherwise overwrite a newly created file.
    with partial.open("rb") as source, target.open("xb") as output:
        shutil.copyfileobj(source, output, length=1024 * 1024)
    verify(target, entry)
    partial.unlink()
    print("Downloaded and verified:", filename, flush=True)


def extract_isolated(path: Path, destination: Path) -> None:
    """Keep source epochs separate; never pretend to relocate old execution captures."""
    if destination.exists():
        raise FileExistsError("Extraction target must be new: " + str(destination))
    with zipfile.ZipFile(path) as archive:
        selected = []
        seen = set()
        components = {}
        kinds = {}
        reserved = {"con", "prn", "aux", "nul"}
        reserved.update("com" + str(i) for i in range(1, 10))
        reserved.update("lpt" + str(i) for i in range(1, 10))
        reserved.update(prefix + digit for prefix in ("com", "lpt") for digit in "\u00b9\u00b2\u00b3")
        total = 0
        for info in archive.infolist():
            original = info.orig_filename
            name = PurePosixPath(original)
            if "\\" in original or name.is_absolute() or ".." in name.parts:
                raise ValueError("Unsafe ZIP path")
            if not name.parts or name.parts[0] == "__MACOSX" or name.name.startswith("._"):
                continue  # Finder resource forks are not proof inputs.
            prefix = ()
            for part in name.parts:
                if (any(char in part for char in '<>:"|?*') or part.endswith((".", " "))
                        or any(ord(char) < 32 for char in part)
                        or part.split(".", 1)[0].casefold() in reserved):
                    raise ValueError("Unsafe cross-platform path")
                prefix += (part.casefold(),)
                if components.setdefault(prefix, part) != part:
                    raise ValueError("Case-colliding path component")
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Symbolic link in source archive")
            identity = str(name).casefold()
            if identity in seen:
                raise ValueError("Duplicate or case-colliding ZIP path")
            seen.add(identity)
            kinds[tuple(part.casefold() for part in name.parts)] = info.is_dir()
            total += info.file_size
            if total > 16 * 1024**3:
                raise ValueError("Archive exceeds bounded extraction budget")
            selected.append((info, name))
        for key in kinds:
            for length in range(1, len(key)):
                if kinds.get(key[:length]) is False:
                    raise ValueError("File used as a directory in ZIP")
        disk_parent = destination.parent.resolve()
        while not disk_parent.exists():
            disk_parent = disk_parent.parent
        if shutil.disk_usage(disk_parent).free < total + 64 * 1024**2:
            raise OSError("Insufficient space for bounded source extraction")
        destination.mkdir(parents=True)
        for info, name in selected:
            target = destination.joinpath(*name.parts)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, target.open("xb") as output:
                    shutil.copyfileobj(source, output, length=1024 * 1024)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=HERE / "source-archives")
    parser.add_argument("--download", action="store_true", help="Fetch missing assets from GitHub")
    parser.add_argument("--extract-to", type=Path, help="New directory for separate immutable source epochs")
    args = parser.parse_args()
    manifest = json.loads((HERE / "source_archives.json").read_text(encoding="utf-8"))
    if args.extract_to and args.extract_to.exists():
        parser.error("--extract-to must name a new directory")
    if args.download:
        args.directory.mkdir(parents=True, exist_ok=True)
    for entry in manifest["archives"]:
        if args.download:
            download(manifest, entry, args.directory)
        else:
            verify(args.directory / entry["name"], entry)
            print("Verified:", entry["name"], flush=True)
    if args.extract_to:
        for entry in manifest["archives"]:
            extract_isolated(args.directory / entry["name"], args.extract_to / Path(entry["name"]).stem)
        print("Extracted separate epochs; historical paths/captures were not rewritten.")
    print("INTEGRITY/AVAILABILITY ONLY: no mathematical replay or archived code execution.")
    print("Portable end-to-end mathematical replay verified:", manifest["portable_end_to_end_replay_verified"])


if __name__ == "__main__":
    main()
