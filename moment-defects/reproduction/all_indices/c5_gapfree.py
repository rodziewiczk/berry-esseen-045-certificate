"""Prepare and independently recompute all compact gap-free leaves and both rays."""
from __future__ import annotations
import argparse
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile
if __package__:
    from .c5_counts import BASE, MIB, ARCHIVE_BYTES, ARCHIVE_SHA, PREFIX, FINAL, FINAL_SHA
    from .c5_counts import need, digest, member, unique
else:
    from c5_counts import BASE, MIB, ARCHIVE_BYTES, ARCHIVE_SHA, PREFIX, FINAL, FINAL_SHA
    from c5_counts import need, digest, member, unique

sys.dont_write_bytecode = True
FILES = {
    "check.py":"work/cutoff5_20261020/audit/gapfree5_readback_v1/check.py",
    "FOREST.json":"work/cutoff5_20261020/root/gapfree5_exact_v1/FOREST.json",
    "EXTERIOR.json":"work/cutoff5_20261020/high/gap_free_count_review_v2/CHECKED.json",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive",type=Path,required=True)
    parser.add_argument("--prepare-only",action="store_true")
    args = parser.parse_args()
    archive = args.archive.resolve()
    need(archive.is_file() and not archive.is_symlink() and
         archive.stat().st_size == ARCHIVE_BYTES and digest(archive) == ARCHIVE_SHA,
         "Exact public source archive")
    spec = importlib.util.spec_from_file_location("original_runner",BASE/"run_reproduction.py")
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    def guard():
        need(r.own_peak() <= 256*MIB and r.available_ram() >= 1024*MIB,
             "Bounded archive coordinator and host reserve")
    guard()
    work = r.private_work()
    capsule = work/"capsule"
    capsule.mkdir()
    pins = {}
    with zipfile.ZipFile(archive) as z:
        final = json.loads(member(z,PREFIX+FINAL,FINAL_SHA),object_pairs_hook=unique)
        graph = final["files_sha256"]
        for name,original in FILES.items():
            raw = member(z,PREFIX+original,graph[original])
            with (capsule/name).open("xb") as stream:
                stream.write(raw)
            pins[name] = graph[original]
            guard()
    worker = Path(__file__).with_name("c5_gapfree_worker.py")
    shutil.copyfile(worker,capsule/worker.name)
    with (capsule/"INPUTS.json").open("x",encoding="utf-8") as stream:
        json.dump({"schema":"C5_GAPFREE_INDEPENDENT_REPLAY_INPUTS_V1",
                   "files":pins,"original_source_paths":FILES,
                   "original_archive_sha256":ARCHIVE_SHA,
                   "original_final_index_sha256":FINAL_SHA},stream,indent=2)
    guard()
    if args.prepare_only:
        print(json.dumps({"scope":"FRESH_GAPFREE_INPUT_PREPARATION_ONLY","work":str(work),
                          "arithmetic_replayed":False}))
        return
    # The coordinator needs only the three small source pins after preparation.
    # Do not retain the full archive directory and 16k-file graph during replay.
    del final, graph, z, raw
    gc.collect()
    child = None
    try:
        with (work/"SUPERVISOR.log").open("xb") as log:
            child = subprocess.Popen(
                [sys.executable,"-B","-S",str(Path(__file__).with_name("c5_gapfree_one.py")),
                 "--work",str(work)],cwd=BASE,stdin=subprocess.DEVNULL,
                stdout=log,stderr=subprocess.STDOUT,
                **({"creationflags":subprocess.CREATE_NO_WINDOW} if sys.platform=="win32"
                   else {"start_new_session":True}))
            while child.poll() is None:
                guard()
                need(log.tell() <= 16*MIB,"Bounded stage log")
                time.sleep(.25)
        need(child.returncode == 0,"Complete fresh independent gap-free process")
    finally:
        if child is not None and child.poll() is None:
            child.terminate()
            child.wait(timeout=10)
    result = json.loads((capsule/"FRESH_GAPFREE_RESULT.json").read_text(),object_pairs_hook=unique)
    need(result["status"] == "PASS_FRESH_C5_GAPFREE_INDEPENDENT_WHOLE_LINE",
         "Complete fresh whole-line acceptance")
    need(result["adapter_sha256"] == digest(worker) == digest(capsule/worker.name),
         "Unchanged reviewed arithmetic adapter")
    need(all(digest(capsule/name)==pin for name,pin in pins.items()),"Original inputs unchanged")
    print(json.dumps({"event":"fresh_c5_gapfree_complete",
                      "result":str(capsule/"FRESH_GAPFREE_RESULT.json"),
                      "compact":result["compact"],"exteriors":result["exteriors"],
                      "all_index_conclusion_verified":False}),flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("C5_GAPFREE_INCOMPLETE: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
