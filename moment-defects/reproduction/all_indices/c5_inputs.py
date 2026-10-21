"""Prepare the complete selected C5 source graph; this is not arithmetic replay."""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import zipfile
if __package__:
    from .c5_counts import BASE, MIB, ARCHIVE_BYTES, ARCHIVE_SHA, PREFIX, FINAL, FINAL_SHA
    from .c5_counts import need, digest, member, unique
else:
    from c5_counts import BASE, MIB, ARCHIVE_BYTES, ARCHIVE_SHA, PREFIX, FINAL, FINAL_SHA
    from c5_counts import need, digest, member, unique

sys.dont_write_bytecode = True
EXTRAS = "work/cutoff5_20261020/entry/delivery_review_v1/EXTRA_SOURCES.json"


def safe_relative(name):
    need(type(name) is str and not name.startswith("/") and "\\" not in name,
         "Explicit original POSIX relative source path")
    parts = PurePosixPath(name).parts
    need(parts and all(p not in (".","..") and ":" not in p for p in parts),
         "No source path escape or drive")
    need("/".join(parts) == name,"Canonical original relative path")
    return parts


def extended(path):
    path = path.resolve()
    if os.name == "nt" and not str(path).startswith("\\\\?\\"):
        return Path("\\\\?\\"+str(path))
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive",type=Path,required=True)
    p.add_argument("--destination",type=Path)
    args = p.parse_args()
    archive = args.archive.resolve()
    need(archive.is_file() and not archive.is_symlink() and
         archive.stat().st_size == ARCHIVE_BYTES and digest(archive) == ARCHIVE_SHA,
         "Exact public source asset")
    spec = importlib.util.spec_from_file_location("resource_observer",BASE/"run_reproduction.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    destination = extended(args.destination or BASE/"reproduction_inputs"/("c5-"+ARCHIVE_SHA[:16]))
    def guard():
        need(r.own_peak() <= 256*MIB and r.available_ram() >= 1024*MIB,
             "Input preparation memory cap and host reserve")
        need(shutil.disk_usage(destination.parent if destination.parent.exists() else BASE).free >= 4*1024**3,
             "At least 4 GiB free disk")
    guard()
    owner_value = {"schema":"C5_IMMUTABLE_INPUT_CACHE_V1","archive_sha256":ARCHIVE_SHA}
    if destination.exists():
        need(destination.is_dir() and not destination.is_symlink() and
             json.loads((destination/"CACHE_OWNER.json").read_text(),object_pairs_hook=unique)
             == owner_value,"Resume only this explicitly tagged byte cache")
    else:
        destination.mkdir(parents=True,exist_ok=False)
        with (destination/"CACHE_OWNER.json").open("x",encoding="utf-8") as stream:
            json.dump(owner_value,stream)
    copied = reused = total = 0
    with zipfile.ZipFile(archive) as z:
        receipt_raw = member(z,PREFIX+FINAL,FINAL_SHA)
        receipt = json.loads(receipt_raw,object_pairs_hook=unique)
        graph = dict(receipt["files_sha256"])
        need(len(graph) == 16576,"Complete selected v2 source graph")
        # Extra data are pinned by the complete source archive. Classifications
        # distinguish runtime inputs from history, never upgrade old statuses.
        extras_info = z.getinfo(PREFIX+EXTRAS)
        need(extras_info.file_size <= MIB,"Bounded extra-source catalog")
        extras_raw = z.read(extras_info)
        extras = json.loads(extras_raw,object_pairs_hook=unique)
        need(extras["schema"] == "DELIVERY_EXTRA_SOURCE_CLASSIFICATION_V1","Extra-source catalog")
        graph[FINAL] = FINAL_SHA
        graph[EXTRAS] = __import__("hashlib").sha256(extras_raw).hexdigest()
        for row in extras["files"]:
            name, pin = row["path"],row["sha256"]
            need(name not in graph or graph[name] == pin,"Consistent exact extra source")
            graph[name] = pin
        case_names = set()
        for name,pin in graph.items():
            parts = safe_relative(name)
            need(type(pin) is str and len(pin)==64 and all(c in "0123456789abcdef" for c in pin),
                 "Exact SHA256 source commitment")
            need(name.casefold() not in case_names,"No case-colliding input paths")
            case_names.add(name.casefold())
            target = destination.joinpath(*parts)
            info = z.getinfo(PREFIX+name)
            need(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16),
                 "Regular selected source member")
            total += info.file_size
            need(info.file_size <= 256*MIB and total <= 768*MIB,"Bounded streamed source set")
            guard()
            if target.exists():
                need(target.is_file() and not target.is_symlink() and digest(target) == pin,
                     "Existing cache bytes must match; never overwrite")
                reused += 1
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            h = __import__("hashlib").sha256()
            with z.open(info) as source, target.open("xb") as output:
                while chunk := source.read(MIB):
                    h.update(chunk)
                    output.write(chunk)
                    guard()
            need(h.hexdigest() == pin,"Exact source content: "+name)
            copied += 1
    inventory = {"schema":"C5_PREPARED_SOURCE_CACHE_V1","archive_sha256":ARCHIVE_SHA,
                 "final_index_sha256":FINAL_SHA,"files":graph,"source_bytes":total,
                 "arithmetic_replayed":False,"all_index_conclusion_verified":False}
    inventory_path = destination/"SOURCE_INVENTORY.json"
    if inventory_path.exists():
        need(json.loads(inventory_path.read_text(),object_pairs_hook=unique) == inventory,
             "Existing complete inventory unchanged")
    else:
        with inventory_path.open("x",encoding="utf-8") as stream:
            json.dump(inventory,stream,indent=2)
    print(json.dumps({"scope":"COMPLETE_PINNED_C5_INPUTS_PREPARED_ONLY",
                      "destination":str(destination),"files":len(graph),
                      "copied":copied,"reused":reused,"bytes":total,
                      "arithmetic_replayed":False}),flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_INPUT_PREPARATION_INCOMPLETE: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
