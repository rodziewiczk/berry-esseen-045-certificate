"""All-name SHA-only probe for the 1748 critical cutoff25_20261013 OTHER files.

This is byte availability, NOT mathematical validation or historical replay.
Unlike the published A9 auditor, every ordinary non-Mac, non-directory member
of the six fixed ZIPs is read to EOF regardless of its basename. Nested ZIP
files are hashed as opaque ordinary members; their interiors are NOT opened.
Strict SHA matches are CANDIDATE_LOCATION only, never frozen-path rewrites.

Only this new module and arbitrary13.{json,txt} are task outputs. No extraction,
proof import, subprocess, numerical input, or mathematical producer is used.
The classification OTHER_SOURCE_OR_CERTIFICATE is exactly A9's name-based
classification, not a claim that every such file is itself a mathematical lemma.

Run bundled Python -B this_file.py --run. One sequential observer is guarded by
256 MiB peak working set, ABSOLUTE process CPU 300s, wall 1200s and 20 GiB of
hashed/member input. The small additional ledger-parser and ZIP-directory reads
are not counted in the last counter. No guard is reset or allowance enlarged.
"""
from __future__ import annotations

import time
START_WALL = time.monotonic()

import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
IMPORT = ROOT / 'tmp/cutoff20_import_2026-10-17'
LEDGER = IMPORT / 'continuation_cutoff20_20261016/b0/sequential_synthesis_v8/CONDITIONAL_CUTOFF20_COMPOSED.json'
LEDGER_SHA = '0247c2bbf7df6d101239818f097647e94f5f7a9fdef8ae49a60ebc71ed88ee08'
PREFIX = 'work/cutoff25_20261013/'
EMPTY_SHA = hashlib.sha256(b'').hexdigest()
ARCHIVES = (
 ('tmp/cutoff20_import_2026-10-17/continuation_cutoff20_20261016_final.zip',
  '1e3de8f03c28816d36258ddd84ee7f29166622b2390d5c3457eb1b193ef608b7'),
 ('tmp/cutoff20_import_2026-10-17/cutoff20_20261016.zip',
  'b1dd7e730187f62142faa1e82eff5a9fd13a879e933a2fafbd22af8a4709ef83'),
 ('tmp/cutoff20_import_2026-10-17/cutoff25_continue_20261015.zip',
  '2b848227a5f5e2f54f210a347829c6b3f1c56bd656ef0cf01482a7898e11d63a'),
 ('tmp/cutoff20_import_2026-10-17/cutoff25_rethink_20261015.zip',
  '47503aa52408b24243e554a080730f3d546c7ad425a5480af16e40678310f43b'),
 ('research/imports/drive_20261012/cutoff25_20261011.zip',
  '17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb'),
 ('research/imports/drive_20261012/continuation_20261011_wrap.zip',
  'c17670f2d4e6d4cd86786881a41be4461a1b518bcb5c9852af1a106af37ebbc7'),
)
READ_BYTES = 0
PEAK_BYTES = 0
WINDOWS_MEMORY_API = None


def need(value, message):
    if not value:
        raise ValueError(message)


def peak_memory():
    global WINDOWS_MEMORY_API
    if os.name != 'nt':
        import resource
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(peak if sys.platform == 'darwin' else peak * 1024)
    if WINDOWS_MEMORY_API is None:
        class Counters(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [
                (n, ctypes.c_size_t) for n in ('peak_ws', 'ws', 'peak_paged',
                'paged', 'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile')]
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p,
                                              ctypes.c_void_p, ctypes.c_ulong]
        WINDOWS_MEMORY_API = Counters, kernel, psapi
    Counters, kernel, psapi = WINDOWS_MEMORY_API
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    need(psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),
        ctypes.byref(counters), counters.cb), 'GetProcessMemoryInfo failed')
    return int(counters.peak_ws)


def guard():
    global PEAK_BYTES
    PEAK_BYTES = max(PEAK_BYTES, peak_memory())
    need(PEAK_BYTES <= 256 * 1024**2, 'observer peak working set exceeds 256 MiB')
    need(time.process_time() <= 300, 'observer absolute CPU exceeds 300 seconds')
    need(time.monotonic() - START_WALL <= 1200, 'observer wall exceeds 1200 seconds')
    need(READ_BYTES <= 20 * 1024**3, 'observer hashed/member input exceeds 20 GiB')


def digest(stream):
    global READ_BYTES
    h = hashlib.sha256()
    size = 0
    while True:
        guard()
        block = stream.read(1024 * 1024)
        if not block:
            break
        h.update(block)
        size += len(block)
        READ_BYTES += len(block)
    guard()
    return h.hexdigest(), size


def file_sha(path):
    with path.open('rb') as stream:
        return digest(stream)[0]


def category(path):
    """Exact A9 classification; not a semantic judgement of file contents."""
    name = PurePosixPath(path).name.lower()
    if ('stdout' in name or 'stderr' in name) and name.endswith(('.txt', '.json', '.log')):
        return 'LOG_STREAM'
    if name in ('metadata.json', 'execution.json', 'started.json', 'process.json') or \
            name.endswith(('.execution.json', '.process.json')):
        return 'EXECUTION_METADATA'
    return 'OTHER_SOURCE_OR_CERTIFICATE'


def targets():
    guard()
    need(file_sha(LEDGER) == LEDGER_SHA, 'pinned expected ledger hash mismatch')
    sys.path.insert(0, str(ROOT / 'tmp/cutoff20_audit_deps'))
    import ijson
    need(ijson.__version__ == '3.6.0', 'expected ijson3.6.0')
    paths, by_sha = {}, {}
    with LEDGER.open('rb') as stream:
        for path, row in ijson.kvitems(stream, 'historical_tail_edges'):
            guard()
            if not path.startswith(PREFIX) or category(path) != 'OTHER_SOURCE_OR_CERTIFICATE':
                continue
            need(path not in paths, 'duplicate critical path')
            sha = row['expected_sha256']
            need(type(sha) is str and re.fullmatch('[0-9a-f]{64}', sha),
                 'invalid expected SHA')
            paths[path] = sha
            by_sha.setdefault(sha, dict(expected_paths=[], candidate_locations=[],
                matching_members=0))['expected_paths'].append(path)
    need(len(paths) == 1748, 'expected exactly1748 critical OTHER requirements')
    return paths, by_sha


def summary(paths, by_sha):
    located = sum(bool(by_sha[sha]['matching_members']) for sha in paths.values())
    nonempty = [sha for sha in paths.values() if sha != EMPTY_SHA]
    return dict(expected_paths=len(paths), expected_distinct_sha256=len(by_sha),
        candidate_content_paths=located, not_located_paths=len(paths)-located,
        nonempty_expected_paths=len(nonempty),
        nonempty_candidate_content_paths=sum(bool(by_sha[s]['matching_members']) for s in nonempty),
        empty_expected_paths=len(paths)-len(nonempty),
        matched_distinct_sha256=sum(bool(r['matching_members']) for r in by_sha.values()))


def mac_metadata(name):
    parts = name.replace('\\', '/').split('/')
    return '__MACOSX' in parts or parts[-1] == '.DS_Store' or parts[-1].startswith('._')


def scan(rel, expected_archive_sha, paths, by_sha):
    path = ROOT / rel
    before = path.stat()
    need(file_sha(path) == expected_archive_sha, 'pinned raw archive SHA mismatch: ' + rel)
    row = dict(path=rel, sha256=expected_archive_sha, bytes=before.st_size,
        total_members=0, ordinary_members_hashed=0, directories_skipped=0,
        mac_metadata_skipped=0, special_members_skipped=0,
        uncompressed_bytes_hashed=0, opaque_nested_zip_members_hashed=0,
        matched_target_members=0)
    print('ARCHIVE_BEGIN ' + rel, flush=True)
    with zipfile.ZipFile(path) as archive:
        guard()
        for index, member in enumerate(archive.infolist()):
            guard()
            row['total_members'] += 1
            if member.is_dir():
                row['directories_skipped'] += 1
                continue
            if mac_metadata(member.filename):
                row['mac_metadata_skipped'] += 1
                continue
            mode = stat.S_IFMT(member.external_attr >> 16)
            if mode not in (0, stat.S_IFREG):
                row['special_members_skipped'] += 1
                continue
            # No basename/suffix filtering, size shortcut or CRC-as-SHA cache.
            # Names are never dereferenced as filesystem paths; even an unusual
            # member name cannot escape because nothing is extracted.
            with archive.open(member) as stream:
                actual, size = digest(stream)
            need(size == member.file_size, 'uncompressed member size mismatch')
            row['ordinary_members_hashed'] += 1
            row['uncompressed_bytes_hashed'] += size
            if member.filename.lower().endswith('.zip'):
                row['opaque_nested_zip_members_hashed'] += 1
            if actual in by_sha:
                target = by_sha[actual]
                target['matching_members'] += 1
                row['matched_target_members'] += 1
                if len(target['candidate_locations']) < 8:
                    target['candidate_locations'].append(dict(
                        archive=rel, member=member.filename, member_index=index,
                        header_offset=member.header_offset, bytes=size,
                        crc32=member.CRC, sha256=actual,
                        status='CANDIDATE_LOCATION_STRICT_SHA256_ONLY'))
            if row['ordinary_members_hashed'] % 5000 == 0:
                print('PROGRESS ' + json.dumps(dict(archive=rel,
                    ordinary_members_hashed=row['ordinary_members_hashed'],
                    summary=summary(paths, by_sha))), flush=True)
    guard()
    after = path.stat()
    need((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
         'raw archive stat drift: ' + rel)
    need(file_sha(path) == expected_archive_sha, 'END raw archive SHA drift: ' + rel)
    row['end_sha256_equal'] = True
    print('ARCHIVE_END ' + json.dumps(dict(archive=rel, summary=summary(paths, by_sha))), flush=True)
    return row


def reports(paths, by_sha, archives, self_sha):
    result = dict(status='COMPLETE_ALL_NAME_TOP_LEVEL_ORDINARY_MEMBER_SHA_PROBE',
        scope='Only exact content availability of1748 A9-classified critical OTHER requirements; '
              'no frozen-path resolution, mathematical validity or execution provenance.',
        auditor_sha256=self_sha, expected_ledger_sha256=LEDGER_SHA,
        expected_prefix=PREFIX, expected_classification='OTHER_SOURCE_OR_CERTIFICATE',
        summary=summary(paths, by_sha), archives=archives,
        mathematical_oracles_called=0, proof_modules_imported=False,
        source_archives_modified=False, archive_members_extracted=False,
        nested_zip_interiors_opened=False, frozen_paths_rewritten=False,
        historical_execution_reconstructed=False, mathematical_proof_validated=False,
        limits=dict(peak_MiB=256, absolute_process_CPU_seconds=300,
                    wall_seconds=1200, hashed_member_input_GiB=20),
        memory_peak_bytes=PEAK_BYTES, absolute_process_cpu_seconds=time.process_time(),
        wall_seconds=time.monotonic()-START_WALL, hashed_member_input_bytes=READ_BYTES,
        io_counter_scope='Hash/member reads; excludes additional ledger-parser and central-directory reads.',
        exclusions=['directories', 'Mac metadata (__MACOSX, .DS_Store, ._*)',
                    'nonregular/symlink/special entries', 'nested ZIP interiors'],
        caveat='Every included ordinary member reaches EOF and has its ZIP CRC checked. '
               'A SHA match is only candidate content. In particular empty content matches '
               'do not recover a particular historical source location or execution. '
               'At most8 example locations are retained per expected SHA; total matching '
               'member counts are complete. This does not test arbitrary encodings, '
               'concatenations, reconstructed files or nested archive interiors.',
        targets=[dict(expected_sha256=sha, **row) for sha, row in by_sha.items()])
    json_path, text_path = IMPORT / 'arbitrary13.json', IMPORT / 'arbitrary13.txt'
    need(not json_path.exists() and not text_path.exists(), 'new reports only; no overwrite')
    guard()
    with json_path.open('x', encoding='utf-8', newline='\n') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    with text_path.open('x', encoding='utf-8', newline='\n') as out:
        out.write('CUTOFF25_20261013 ARBITRARY-NAME CONTENT PROBE — NOT MATH/REPLAY\n\n')
        out.write(json.dumps(result['summary'], indent=2) + '\n\n')
        out.write('No basename filter: all ordinary non-Mac top-level members of6 pinned ZIPs hashed.\n')
        out.write('Nested ZIP interiors not opened; matching content is CANDIDATE_LOCATION only.\n\n')
        out.write('NOT LOCATED EXPECTED PATHS (with exact expected SHA):\n')
        for path, sha in paths.items():
            if not by_sha[sha]['matching_members']:
                out.write(path + ' ' + sha + '\n')
        out.write('\nCANDIDATE CONTENT (not proof of old location or execution):\n')
        for sha, row in by_sha.items():
            if row['matching_members']:
                out.write(json.dumps(dict(expected_sha256=sha, **row)) + '\n')
    guard()
    print('COMPLETE ' + json.dumps(dict(summary=result['summary'],
        memory_peak_bytes=PEAK_BYTES, absolute_process_cpu_seconds=time.process_time(),
        wall_seconds=time.monotonic()-START_WALL)), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return
    need(sys.flags.dont_write_bytecode, 'invoke with -B')
    guard()
    self_sha = file_sha(Path(__file__).resolve())
    paths, by_sha = targets()
    print('TARGETS ' + json.dumps(summary(paths, by_sha)), flush=True)
    archives = [scan(rel, sha, paths, by_sha) for rel, sha in ARCHIVES]
    need(file_sha(LEDGER) == LEDGER_SHA, 'END expected-ledger drift')
    need(file_sha(Path(__file__).resolve()) == self_sha, 'END auditor-source drift')
    guard()
    reports(paths, by_sha, archives, self_sha)


if __name__ == '__main__':
    main()
