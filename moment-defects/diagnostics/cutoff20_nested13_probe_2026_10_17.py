"""Bounded nested-ZIP byte-availability probe; NOT a mathematical checker.

Only the three pinned outer archives below are inputs. Their non-__MACOSX ZIP
members are all read through CRC-checked EOF and SHA256, including duplicate
copies. Only AFTER those reads may identical ZIP bodies share an interior scan.
Every non-directory, non-__MACOSX interior member is hashed, regardless of its
name, and compared with all 1,748 substantive cutoff25_20261013 requirements
streamed from the pinned FULL v8 JSON. Interior ZIPs are detected by content,
not extension. A detected ZIP past depth 3 or any limit failure is fatal, never
a successful zero-match result. No filesystem extraction or proof import occurs.

The guard covers this observer's absolute process CPU (300s), peak RSS (256MiB),
wall time (1200s), and combined counted disk-read plus decoded-member bytes
(1GiB). A single member's compressed and decoded sizes are each <=64MiB. Raw
in-memory ZIP metadata reads are not counted again, but each decoded member is.
Outer archives are fully hashed once and their path/fd identities and same-API
stat signatures checked around reads; this is NOT a second full-archive hash.

Only nested13.json and nested13.txt in the selected output directory are new
outputs. A zero match excludes only exact expected bytes in the scanned scope;
it does not prove absence elsewhere, repair provenance, or validate a theorem.
Requires ordinary Python >=3.11, -B -S, and externally provided ijson==3.6.0.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import ctypes
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import time
import zipfile

START_WALL = time.monotonic()
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
FINAL_REL = ('tmp/cutoff20_import_2026-10-17/continuation_cutoff20_20261016/'
             'b0/sequential_synthesis_v8/CONDITIONAL_CUTOFF20_COMPOSED.json')
FINAL_SHA = '0247c2bbf7df6d101239818f097647e94f5f7a9fdef8ae49a60ebc71ed88ee08'
ARCHIVES = (
    ('tmp/cutoff20_import_2026-10-17/cutoff20_20261016.zip',
     'b1dd7e730187f62142faa1e82eff5a9fd13a879e933a2fafbd22af8a4709ef83', 10),
    ('tmp/cutoff20_import_2026-10-17/cutoff25_continue_20261015.zip',
     '2b848227a5f5e2f54f210a347829c6b3f1c56bd656ef0cf01482a7898e11d63a', 10),
    ('research/imports/drive_20261012/cutoff25_20261011.zip',
     '17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb', 30),
)
MEMBER_LIMIT = 64 * 1024**2
INPUT_LIMIT = 1024**3
CHUNK = 512 * 1024
DISK_BYTES = 0
DECODED_BYTES = 0
PEAK_BYTES = 0
MEMORY_API = None


def need(condition, message):
    if not condition:
        raise ValueError(message)


def peak_memory():
    global MEMORY_API
    if os.name != 'nt':
        import resource
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(value if sys.platform == 'darwin' else value * 1024)
    if MEMORY_API is None:
        class Counters(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in ('peak_ws', 'ws', 'peak_paged',
                 'paged', 'peak_nonpaged', 'nonpaged', 'pagefile', 'peak_pagefile')]
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                              ctypes.c_ulong]
        MEMORY_API = Counters, kernel, psapi
    Counters, kernel, psapi = MEMORY_API
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters),
                                      counters.cb):
        raise OSError(ctypes.get_last_error(), 'GetProcessMemoryInfo')
    return int(counters.peak_ws)


def guard():
    global PEAK_BYTES
    PEAK_BYTES = max(PEAK_BYTES, peak_memory())
    need(PEAK_BYTES <= 256 * 1024**2, 'INCOMPLETE: peak RSS exceeds 256MiB')
    need(time.process_time() < 300, 'INCOMPLETE: absolute process CPU exceeds 300s')
    need(time.monotonic() - START_WALL < 1200, 'INCOMPLETE: wall exceeds 1200s')
    need(DISK_BYTES + DECODED_BYTES <= INPUT_LIMIT,
         'INCOMPLETE: combined disk-read and decoded-member input exceeds 1GiB')


class CountedFile:
    def __init__(self, raw):
        self.raw = raw

    def read(self, size=-1):
        global DISK_BYTES
        guard()
        if size < 0:
            # zipfile reads to EOF after a bounded tail seek. Do not permit an
            # accidental unbounded whole-archive allocation at another offset.
            position = self.raw.tell()
            end = self.raw.seek(0, io.SEEK_END)
            self.raw.seek(position)
            size = end - position
        need(0 <= size <= MEMBER_LIMIT, 'bounded disk read required')
        data = self.raw.read(size)
        DISK_BYTES += len(data)
        guard()
        return data

    def readinto(self, buffer):
        global DISK_BYTES
        guard()
        need(len(buffer) <= MEMBER_LIMIT, 'bounded parser read required')
        count = self.raw.readinto(buffer)
        DISK_BYTES += count
        guard()
        return count

    def __getattr__(self, name):
        return getattr(self.raw, name)


def full_signature(value):
    return (value.st_size, value.st_mtime_ns, value.st_ctime_ns,
            value.st_ino, value.st_dev)


def common_identity(value):
    # Windows CPython may expose different ctime semantics via path and fd.
    return value.st_size, value.st_mtime_ns, value.st_ino, value.st_dev


@contextmanager
def stable_file(path):
    before = path.stat()
    with path.open('rb') as raw:
        fd_before = os.fstat(raw.fileno())
        need(common_identity(before) == common_identity(fd_before), 'path/fd identity')
        yield CountedFile(raw)
        fd_after = os.fstat(raw.fileno())
        after = path.stat()
        need(full_signature(before) == full_signature(after), 'path stat drift')
        need(full_signature(fd_before) == full_signature(fd_after), 'fd stat drift')
        need(common_identity(after) == common_identity(fd_after), 'END path/fd identity')


def file_hash(path):
    result = hashlib.sha256()
    with stable_file(path) as source:
        while chunk := source.read(CHUNK):
            result.update(chunk)
    return result.hexdigest()


def mac_metadata(name):
    return '__macosx' in (part.casefold() for part in name.replace('\\', '/').split('/'))


def critical13(name):
    return name.startswith(('work/cutoff25_20261013/', 'cutoff25_20261013/'))


def substantive(name):
    base = PurePosixPath(name).name.lower()
    if ('stdout' in base or 'stderr' in base) and base.endswith(('.txt', '.json', '.log')):
        return False
    return not (base in ('metadata.json', 'execution.json', 'started.json', 'process.json')
                or base.endswith(('.execution.json', '.process.json')))


def targets(root, parser_directory):
    guard()
    sys.path.insert(0, str(parser_directory))
    import ijson
    need(ijson.__version__ == '3.6.0', 'requires ijson 3.6.0')
    final = root / FINAL_REL
    need(file_hash(final) == FINAL_SHA, 'FULL v8 input SHA mismatch')
    seen, selected = set(), {}
    critical_count = 0
    with stable_file(final) as source:
        for name, expected in ijson.kvitems(source, 'files_sha256'):
            need(type(name) is str and name not in seen, 'duplicate or nonstring path')
            seen.add(name)
            need(type(expected) is str and re.fullmatch('[0-9a-f]{64}', expected),
                 'invalid expected SHA256')
            if critical13(name):
                critical_count += 1
                if substantive(name):
                    selected[name] = expected
            if len(seen) % 128 == 0:
                guard()
    need(len(seen) == 31335 and critical_count == 2344 and len(selected) == 1748,
         'FULL v8 requirement cardinality mismatch')
    return selected


def member_bytes(archive, member):
    global DECODED_BYTES
    guard()
    need(0 <= member.file_size <= MEMBER_LIMIT and
         0 <= member.compress_size <= MEMBER_LIMIT, 'INCOMPLETE: member exceeds 64MiB')
    need(not member.flag_bits & 1, 'INCOMPLETE: encrypted member')
    result, hasher, size = io.BytesIO(), hashlib.sha256(), 0
    with archive.open(member) as source:
        while chunk := source.read(CHUNK):
            size += len(chunk)
            DECODED_BYTES += len(chunk)
            guard()
            need(size <= member.file_size and size <= MEMBER_LIMIT, 'decoded member length')
            hasher.update(chunk)
            result.write(chunk)
    need(size == member.file_size, 'member length mismatch')
    guard()
    return result.getvalue(), hasher.hexdigest()


def scan_outer(root, relative, expected_sha, expected_count, unique, occurrences):
    path = root / relative
    signature = full_signature(path.stat())
    actual = file_hash(path)
    need(actual == expected_sha, 'outer archive SHA mismatch: ' + relative)
    counts = dict(all_zip_named=0, excluded_mac_zip_named=0, scanned_zip_bodies=0)
    with stable_file(path) as source, zipfile.ZipFile(source) as archive:
        guard()
        seen = set()
        for index, member in enumerate(archive.infolist()):
            if index % 128 == 0:
                guard()
            if member.is_dir() or not member.filename.lower().endswith('.zip'):
                continue
            counts['all_zip_named'] += 1
            if mac_metadata(member.filename):
                counts['excluded_mac_zip_named'] += 1
                continue
            need(member.filename not in seen, 'duplicate selected outer ZIP name')
            seen.add(member.filename)
            data, sha = member_bytes(archive, member)
            need(zipfile.is_zipfile(io.BytesIO(data)), 'selected .zip is not a valid ZIP')
            row = dict(outer_archive=relative, member=member.filename,
                       member_index=index, header_offset=member.header_offset,
                       compressed_bytes=member.compress_size, bytes=member.file_size,
                       crc32=member.CRC, sha256=sha, crc_checked_to_EOF=True)
            occurrences.append(row)
            if sha not in unique:
                unique[sha] = data
            else:
                need(unique[sha] == data, 'SHA collision or changed duplicate body')
            counts['scanned_zip_bodies'] += 1
        del data
    need(counts['scanned_zip_bodies'] == expected_count, 'outer nested ZIP count mismatch')
    need(full_signature(path.stat()) == signature, 'outer archive END stat drift')
    return dict(path=relative, bytes=signature[0], sha256=actual,
                full_hash_read_once=True, signature=signature, **counts)


def scan_interior(data, sha, depth, by_sha, scans, active):
    guard()
    need(depth <= 3, 'INCOMPLETE: nested ZIP depth exceeds 3')
    need(sha not in active, 'INCOMPLETE: recursive ZIP cycle')
    # All repeated bodies have ALREADY been fully SHA-hashed. Top-level copies
    # were additionally byte-compared. Check the cached recursive height too:
    # the same ZIP at a deeper location must not hide an out-of-scope ZIP.
    if sha in scans:
        need(depth - 1 + scans[sha]['zip_height'] <= 3,
             'INCOMPLETE: cached ZIP subtree exceeds depth 3 here')
        return
    active.add(sha)
    record = dict(zip_sha256=sha, depth_first_seen=depth, bytes=len(data),
                  excluded_mac_members=0, directories=0, zip_height=1, members=[])
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        guard()
        names = set()
        for index, member in enumerate(archive.infolist()):
            guard()
            need(member.filename not in names, 'duplicate interior member name')
            names.add(member.filename)
            if mac_metadata(member.filename):
                record['excluded_mac_members'] += 1
                continue
            if member.is_dir():
                record['directories'] += 1
                continue
            content, content_sha = member_bytes(archive, member)
            is_zip = zipfile.is_zipfile(io.BytesIO(content))
            matches = by_sha.get(content_sha, [])
            record['members'].append(dict(member=member.filename, member_index=index,
                bytes=member.file_size, compressed_bytes=member.compress_size,
                sha256=content_sha, crc32=member.CRC, crc_checked_to_EOF=True,
                is_zip_by_content=is_zip, matching_requirement_paths=matches))
            if is_zip:
                need(depth < 3, 'INCOMPLETE: found a ZIP below maximum depth 3')
                scan_interior(content, content_sha, depth + 1, by_sha, scans, active)
                record['zip_height'] = max(record['zip_height'],
                                          1 + scans[content_sha]['zip_height'])
    active.remove(sha)
    scans[sha] = record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--workspace-root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--ijson-directory', type=Path)
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return
    need(__debug__ and not sys.flags.optimize, 'ordinary nonoptimized Python required')
    need(sys.flags.dont_write_bytecode and sys.flags.no_site, 'invoke with -B -S')
    guard()
    root = args.workspace_root.resolve()
    output = root / 'tmp/cutoff20_import_2026-10-17'
    json_path, text_path = output / 'nested13.json', output / 'nested13.txt'
    need(output.is_dir() and not json_path.exists() and not text_path.exists(),
         'fresh named report pair required; nothing is overwritten')
    source_path = Path(__file__).resolve()
    source_sha = file_hash(source_path)
    selected = targets(root, args.ijson_directory or root / 'tmp/cutoff20_audit_deps')
    by_sha = {}
    for path, sha in sorted(selected.items()):
        by_sha.setdefault(sha, []).append(path)
    selected_digest = hashlib.sha256(json.dumps(selected, sort_keys=True,
        separators=(',', ':')).encode('utf-8')).hexdigest()
    unique, occurrences, archives = {}, [], []
    for relative, expected_sha, expected_count in ARCHIVES:
        archives.append(scan_outer(root, relative, expected_sha, expected_count,
                                   unique, occurrences))
    need(len(occurrences) == 50, 'all 50 nested ZIP bodies required')
    scans = {}
    for sha, data in unique.items():
        scan_interior(data, sha, 1, by_sha, scans, set())
    matched = sorted({path for record in scans.values() for member in record['members']
                      for path in member['matching_requirement_paths']})
    # The selected ZIP bodies themselves are also arbitrary-content candidates.
    matched = sorted(set(matched) | {path for sha in unique for path in by_sha.get(sha, [])})
    need(file_hash(root / FINAL_REL) == FINAL_SHA, 'END FULL ledger SHA drift')
    need(file_hash(source_path) == source_sha, 'END auditor source SHA drift')
    for archive in archives:
        need(full_signature((root / archive['path']).stat()) == tuple(archive['signature']),
             'END outer archive stat drift')
    guard()
    summary = dict(status='COMPLETE_BOUNDED_NESTED_ZIP_BYTE_SEARCH',
        expected_substantive_cutoff13_paths=len(selected),
        distinct_expected_sha256=len(by_sha), top_nested_zip_occurrences=len(occurrences),
        unique_top_nested_zip_sha256=len(unique), recursively_scanned_unique_zips=len(scans),
        hashed_unique_interior_members=sum(len(r['members']) for r in scans.values()),
        matched_requirement_count=len(matched), matched_requirement_paths=matched)
    report = dict(**summary, auditor_sha256=source_sha, final_v8_sha256=FINAL_SHA,
        selected_path_sha_map_sha256=selected_digest, outer_archives=archives,
        all_top_nested_zip_occurrences=occurrences,
        unique_zip_interior_scans=[scans[key] for key in sorted(scans)],
        limits=dict(absolute_CPU_seconds=300, peak_RSS_MiB=256, wall_seconds=1200,
                    combined_disk_plus_decoded_input_GiB=1, member_MiB=64, zip_depth=3),
        resources=dict(absolute_CPU_seconds=time.process_time(),
                       wall_seconds=time.monotonic() - START_WALL, peak_RSS_bytes=PEAK_BYTES,
                       disk_bytes=DISK_BYTES, decoded_member_bytes=DECODED_BYTES),
        proof_modules_imported=False, archive_members_extracted=False,
        mathematical_replay=False, provenance_repaired=False,
        absent_everywhere_claim=False,
        caveat='Only exact expected bytes in these nested ZIPs were sought. '
               '__MACOSX at ANY path component is excluded. No filename filter inside ZIPs. '
               'Outer flat non-ZIP members and unrelated archives are outside scope. '
               'A zero match is not mathematical validation or proof of global absence.')
    # Requested generated reports, not edits to source data or frozen records.
    with json_path.open('x', encoding='utf-8', newline='\n') as destination:
        json.dump(report, destination, indent=2, ensure_ascii=True)
        destination.write('\n')
    with text_path.open('x', encoding='utf-8', newline='\n') as destination:
        destination.write('NESTED CUTOFF13 EXACT-BYTE PROBE — NOT MATHEMATICAL REPLAY\n\n')
        destination.write(json.dumps(summary, indent=2) + '\n\n' + report['caveat'] + '\n')
        destination.write('Every one of the 50 selected top ZIP bodies was SHA-hashed, '
                          'CRC-checked and duplicates byte-compared before deduplication.\n')
        destination.write('See nested13.json for every locator and unique interior member SHA.\n')
    guard()
    print(json.dumps(dict(**summary, resources=report['resources'], auditor_sha256=source_sha)))


if __name__ == '__main__':
    main()
