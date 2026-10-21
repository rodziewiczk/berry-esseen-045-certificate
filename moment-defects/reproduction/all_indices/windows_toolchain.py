"""Pinned private Windows compiler/headers; no global installation or proof claim."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import urllib.request

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
MIB = 1024**2
ASSETS = [
    {"name":"w64devkit-x64-2.4.0.7z.exe","bytes":38806674,
     "sha256":"80678c29a56982d7d3b342f12a0060157df5654c38d82d4adc40704070d6aafb",
     "url":"https://github.com/skeeto/w64devkit/releases/download/v2.4.0/w64devkit-x64-2.4.0.7z.exe"},
    {"name":"boost-1.89.0-b2-nodocs.tar.gz","bytes":73030502,
     "sha256":"aa25e7b9c227c21abb8a681efd4fe6e54823815ffc12394c9339de998eb503fb",
     "url":"https://github.com/boostorg/boost/releases/download/boost-1.89.0/boost-1.89.0-b2-nodocs.tar.gz"},
]


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(MIB):
            h.update(chunk)
    return h.hexdigest()


def get_asset(asset, cache, guard):
    path = cache/asset["name"]
    if not path.exists():
        request = urllib.request.Request(asset["url"],headers={"User-Agent":"BerryEsseenReproduction/1"})
        with urllib.request.urlopen(request,timeout=90) as source, path.open("xb") as target:
            total = 0
            while chunk := source.read(MIB):
                guard()
                total += len(chunk)
                need(total <= asset["bytes"],"Download larger than pinned source asset")
                target.write(chunk)
    need(path.is_file() and not path.is_symlink() and path.stat().st_size == asset["bytes"]
         and digest(path) == asset["sha256"],"Exact publisher asset: "+asset["name"])
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",type=Path,required=True,help="NEW private destination")
    parser.add_argument("--cache",type=Path,help="Optional existing verified-download cache")
    parser.add_argument("--verify-cache-only",action="store_true")
    args = parser.parse_args()
    if args.verify_cache_only:
        need(args.cache is not None and args.cache.is_dir(),
             "Cache-only mode requires --cache pointing to existing downloads")
        for asset in ASSETS:
            path = args.cache / asset["name"]
            need(path.is_file() and not path.is_symlink()
                 and path.stat().st_size == asset["bytes"]
                 and digest(path) == asset["sha256"],
                 "Exact existing publisher asset: " + asset["name"])
        print(json.dumps({"scope":"UPSTREAM_TOOLCHAIN_ASSET_IDENTITIES_ONLY",
                          "assets":ASSETS,"proof_replayed":False}))
        return
    need(os.name == "nt","This optional setup is Windows-specific; other OSes use their compiler")
    spec = importlib.util.spec_from_file_location("original_runner",BASE/"run_reproduction.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    r.HOST_FLOOR = 1024*MIB
    def guard():
        r.parent_guard()
    guard()
    destination = args.directory.resolve()
    need(not destination.exists(),"Toolchain destination must be new; no overwrite")
    cache = args.cache.resolve() if args.cache else destination/"downloads"
    if args.cache:
        need(cache.is_dir() and not cache.is_symlink(),"Explicit existing private cache")
    else:
        cache.mkdir(parents=True,exist_ok=False)
    paths = [get_asset(asset,cache,guard) for asset in ASSETS]
    destination.mkdir(exist_ok=True)
    compiler_dir = destination/"compiler"
    compiler_dir.mkdir(exist_ok=False)
    tar = shutil.which("tar.exe")
    need(tar is not None,"Windows tar.exe is required for this private setup")
    listing = subprocess.run([tar,"-tf",str(paths[0])],capture_output=True,text=True,timeout=120)
    need(listing.returncode == 0 and len(listing.stdout) <= 8*MIB,"Bounded readable compiler archive")
    for name in listing.stdout.splitlines():
        need(name.startswith("w64devkit/") and
             all(p not in ("..",".") and ":" not in p and "\\" not in p
                 for p in PurePosixPath(name).parts),"Safe compiler member")
    work = r.private_work()
    r.launch_gate()
    r.run_child([tar,"-xf",str(paths[0]),"-C",str(compiler_dir)],
                work,"private-compiler-extraction",300,512*MIB)
    headers = destination/"headers"
    headers.mkdir(exist_ok=False)
    files = size = 0
    with tarfile.open(paths[1],mode="r|gz") as archive:
        for entry in archive:
            name = entry.name
            if not (name.startswith("boost-1.89.0/boost/") or
                    name == "boost-1.89.0/LICENSE_1_0.txt"):
                continue
            parts = PurePosixPath(name).parts
            need(not name.startswith("/") and
                 all(p not in ("..",".") and ":" not in p and "\\" not in p for p in parts),
                 "Safe Boost member")
            target = headers.joinpath(*parts)
            if entry.isdir():
                target.mkdir(parents=True,exist_ok=True)
                continue
            need(entry.isfile() and entry.size <= 8*MIB,"Only regular bounded headers/license")
            files += 1
            size += entry.size
            need(files <= 30000 and size <= 256*MIB,"Bounded Boost header set")
            guard()
            target.parent.mkdir(parents=True,exist_ok=True)
            with archive.extractfile(entry) as source, target.open("xb") as output:
                shutil.copyfileobj(source,output,length=MIB)
    compiler = compiler_dir/"w64devkit/bin/g++.exe"
    include = headers/"boost-1.89.0"
    need(compiler.is_file() and (include/"boost/multiprecision/cpp_int.hpp").is_file(),
         "Ready compiler and arbitrary-integer headers")
    result = {"scope":"PRIVATE_COMPILER_DEPENDENCY_SETUP_ONLY","assets":ASSETS,
              "compiler_directory":str(compiler.parent),"boost_directory":str(include),
              "compiler_sha256":digest(compiler),"header_files":files,"header_bytes":size,
              "proof_replayed":False,
              "licensing":"Upstream toolchain licenses and Boost Software License remain applicable."}
    with (destination/"TOOLCHAIN.json").open("x",encoding="utf-8") as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps(result),flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("PRIVATE_TOOLCHAIN_SETUP_INCOMPLETE: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
