"""Read-only, bounded archive BYTE-AVAILABILITY audit, not a mathematical checker.

Reads pinned JSON ledgers using ijson.kvitems; never imports proof modules,
extracts archive members, changes source archives, or executes their contents.
An exact SHA at a basename/suffix recovery location is CANDIDATE_LOCATION only:
it does not repair a frozen path, authenticate an old execution, or prove a
mathematical statement. Only the two expressly requested report files are made.

Invoke bundled Python with -B and --run. The single audit process has a 256 MiB
peak-working-set guard, absolute CPU 300s, wall 1200s, and 20 GiB of hashed
input/member bytes. Parser and central-directory rereads are additional small
metadata I/O, not included in that last counter. These are observer limits,
not numerical-producer allowances. --critical-only scans only requirements
for cutoff25_20261013; other requirements are explicitly NOT_SCANNED.
ZIP CRC is checked ONLY for members actually read, not every archive member.
Nested ZIP contents are not opened: named embedded DIRECTORY trees are scanned.
"""
from __future__ import annotations

import argparse
import collections
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import time
import zipfile

START_CPU = time.process_time()
START_WALL = time.monotonic()
ROOT = Path(__file__).resolve().parents[2]
IMPORT = ROOT / 'tmp/cutoff20_import_2026-10-17'
PACKAGE = IMPORT / 'continuation_cutoff20_20261016'
DEPENDENCIES = ROOT / 'tmp/cutoff20_audit_deps'
FINAL = PACKAGE / 'b0/sequential_synthesis_v8/CONDITIONAL_CUTOFF20_COMPOSED.json'
BASE = PACKAGE / 'bn/global20_synthesis_v5/GLOBAL20_SYNTHESIS.json'
FINAL_SHA = '0247c2bbf7df6d101239818f097647e94f5f7a9fdef8ae49a60ebc71ed88ee08'
BASE_SHA = '26593a306b72106624c849c94af5c69a68a8cbd5cb85b126c498d207bd41e66a'
TAIL_SHA = 'c8c843f49d4b4a88f0a097774edad6eda6f1f4a4a420442160bdce82b1545b2a'
ARCHIVES = (
    IMPORT / 'continuation_cutoff20_20261016_final.zip',
    IMPORT / 'cutoff20_20261016.zip',
    IMPORT / 'cutoff25_continue_20261015.zip',
    IMPORT / 'cutoff25_rethink_20261015.zip',
    ROOT / 'research/imports/drive_20261012/cutoff25_20261011.zip',
    ROOT / 'research/imports/drive_20261012/continuation_20261011_wrap.zip',
)
NESTED_NAMES = ('BE_cutoff35_release_20261007', 'continuation_20261010',
                'continuation_20261011', 'threshold31_20261008')
EMPTY_SHA = hashlib.sha256(b'').hexdigest()
GROUPS = ('current_final', 'historical_tail', 'unresolved_base20')
READ_BYTES = 0
PEAK_BYTES = 0
WINDOWS_MEMORY_API = None


class AuditLimit(RuntimeError):
    pass


def memory_peak():
    global WINDOWS_MEMORY_API
    if os.name == 'nt':
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
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),
                                         ctypes.byref(counters), counters.cb):
            raise OSError(ctypes.get_last_error(), 'GetProcessMemoryInfo')
        return int(counters.peak_ws)
    import resource
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == 'darwin' else value * 1024)


def guard():
    global PEAK_BYTES
    PEAK_BYTES = max(PEAK_BYTES, memory_peak())
    if PEAK_BYTES > 256 * 1024**2:
        raise AuditLimit('observer peak working set exceeds 256 MiB')
    if time.process_time() > 300:
        raise AuditLimit('observer absolute CPU exceeds 300 seconds')
    if time.monotonic() - START_WALL > 1200:
        raise AuditLimit('observer absolute wall time exceeds 1200 seconds')
    if READ_BYTES > 20 * 1024**3:
        raise AuditLimit('observer streamed-input budget exceeds 20 GiB')


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(stream):
    global READ_BYTES
    h = hashlib.sha256()
    size = 0
    while True:
        guard()
        block = stream.read(1024 * 1024)
        if not block:
            break
        READ_BYTES += len(block)
        size += len(block)
        h.update(block)
    guard()
    return h.hexdigest(), size


def file_digest(path):
    with path.open('rb') as stream:
        return digest(stream)[0]


def safe_name(name):
    need(type(name) is str and name and '\\' not in name and '\x00' not in name,
         'invalid archive/ledger path encoding')
    p = PurePosixPath(name)
    need(not p.is_absolute() and '..' not in p.parts and ':' not in p.parts[0],
         'absolute/traversing archive/ledger path')
    return str(p)


def category(path):
    name = PurePosixPath(path).name.lower()
    if ('stdout' in name or 'stderr' in name) and name.endswith(('.txt', '.json', '.log')):
        return 'LOG_STREAM'
    if name in ('metadata.json', 'execution.json', 'started.json', 'process.json') or \
            name.endswith(('.execution.json', '.process.json')):
        return 'EXECUTION_METADATA'
    return 'OTHER_SOURCE_OR_CERTIFICATE'


def critical13(path):
    return path.startswith(('work/cutoff25_20261013/', 'cutoff25_20261013/'))


class Requirement:
    __slots__ = ('path', 'sha', 'groups', 'exact', 'candidate', 'suffix', 'scanned')

    def __init__(self, path, sha):
        self.path, self.sha = path, sha
        self.groups = set()
        self.exact = self.candidate = None
        self.suffix = 0
        self.scanned = True


def ledger_candidates(path):
    yield path, 'LITERAL_DECLARED_PATH'
    if path.startswith('work/'):
        yield path[5:], 'STRIP_LEADING_WORK'
    for name in NESTED_NAMES:
        prefix = 'work/cutoff25_20261011/' + name + '/'
        if path.startswith(prefix):
            yield name + '/' + path[len(prefix):], 'FROZEN_V8_NESTED_PREFIX'


def member_candidates(name):
    yield name, 'LITERAL_ARCHIVE_MEMBER'
    for nested in NESTED_NAMES:
        prefix = 'cutoff25_20261011/' + nested + '/'
        if name.startswith(prefix):
            yield name[len('cutoff25_20261011/'):], 'EXPLICIT_ARCHIVE_CONTAINER_PREFIX'


def load_ledgers():
    guard()
    sys.path.insert(0, str(DEPENDENCIES))
    import ijson
    need(ijson.__version__ == '3.6.0', 'expected ijson 3.6.0')
    need(file_digest(FINAL) == FINAL_SHA and file_digest(BASE) == BASE_SHA,
         'pinned input ledger SHA mismatch')
    records = {}
    group_counts = collections.Counter()

    def consume(file, prefix, group, wrapped):
        seen = set()
        with file.open('rb') as stream:
            for key, value in ijson.kvitems(stream, prefix):
                guard()
                need(key not in seen, 'duplicate path in ledger map ' + prefix)
                seen.add(key)
                path = safe_name(key)
                sha = value['expected_sha256'] if wrapped else value
                need(type(sha) is str and re.fullmatch('[0-9a-f]{64}', sha),
                     'invalid expected SHA256')
                if path in records:
                    need(records[path].sha == sha, 'conflicting expected SHA: ' + path)
                else:
                    records[path] = Requirement(path, sys.intern(sha))
                if group not in records[path].groups:
                    records[path].groups.add(group)
                    group_counts[group] += 1

    consume(FINAL, 'files_sha256', GROUPS[0], False)
    consume(FINAL, 'historical_tail_edges', GROUPS[1], True)
    for suffix, wrapped in (('unavailable_new_synthesis_edges', True),
                            ('retained_B0_missing_edges', True),
                            ('retained_BN_missing_edges', False)):
        consume(BASE, 'unresolved_dependencies.' + suffix, GROUPS[2], wrapped)
    need(dict(group_counts) == dict(zip(GROUPS, (31335, 37811, 186))),
         'ledger cardinality mismatch: ' + str(group_counts))
    return records, dict(group_counts)


def summaries(records, predicate=lambda _: True):
    result = {}
    for group in GROUPS + ('ALL_UNIQUE_PATHS',):
        counts = collections.Counter()
        by_kind = collections.defaultdict(collections.Counter)
        for r in records.values():
            if not predicate(r.path) or (group != 'ALL_UNIQUE_PATHS' and group not in r.groups):
                continue
            status = 'NOT_SCANNED' if not r.scanned else \
                     'EXPLICIT_LOCATOR_MATCH' if r.exact else \
                     'CANDIDATE_LOCATION' if r.candidate else 'NOT_LOCATED'
            counts[status] += 1
            counts['total'] += 1
            by_kind[category(r.path)][status] += 1
            if r.sha == EMPTY_SHA:
                counts['empty_content_expected'] += 1
        result[group] = dict(counts= dict(counts),
                             by_kind={k: dict(v) for k, v in by_kind.items()})
    return result


def common_suffix(left, right):
    n = 0
    for a, b in zip(reversed(PurePosixPath(left).parts),
                    reversed(PurePosixPath(right).parts)):
        if a != b:
            break
        n += 1
    return n


def scan_archive(path, records, explicit, basenames, unseen):
    rel = str(path.relative_to(ROOT)).replace('\\', '/')
    if not path.is_file():
        return dict(path=rel, available=False)
    before = path.stat()
    archive_sha = file_digest(path)
    info = dict(path=rel, available=True, bytes=before.st_size,
                sha256=archive_sha, members=0, hashed_members=0,
                hashed_uncompressed_bytes=0, skipped_basename=0,
                skipped_directory_or_mac_metadata=0, unsafe_or_symlink=0,
                nested_archives_not_opened=0)
    print('ARCHIVE_BEGIN ' + rel, flush=True)
    with zipfile.ZipFile(path) as archive:
        guard()
        for index, member in enumerate(archive.infolist()):
            guard()
            info['members'] += 1
            if member.is_dir() or member.filename.startswith('__MACOSX/'):
                info['skipped_directory_or_mac_metadata'] += 1
                continue
            try:
                name = safe_name(member.filename)
            except ValueError:
                info['unsafe_or_symlink'] += 1
                continue
            if stat.S_ISLNK(member.external_attr >> 16):
                info['unsafe_or_symlink'] += 1
                continue
            if name.lower().endswith('.zip'):
                info['nested_archives_not_opened'] += 1
            basename = PurePosixPath(name).name
            possible = basenames.get(basename)
            if not possible:
                info['skipped_basename'] += 1
                continue
            exact_pending = [(req, ledger_rule, member_rule)
                for candidate, member_rule in member_candidates(name)
                for req, ledger_rule in explicit.get(candidate, ())
                if req.exact is None]
            # No collision-prone CRC memo: skip only if every desired SHA for
            # this basename has already been SHA-located AND no explicit
            # unresolved locator could be upgraded by reading this member.
            if not exact_pending and not unseen[basename]:
                info['skipped_already_located_content'] = \
                    info.get('skipped_already_located_content', 0) + 1
                continue
            # Every read member reaches EOF, so zipfile validates its CRC.
            with archive.open(member) as stream:
                actual, size = digest(stream)
            need(size == member.file_size, 'ZIP size mismatch: ' + name)
            info['hashed_members'] += 1
            info['hashed_uncompressed_bytes'] += size
            locator = dict(archive=rel, member=name, member_index=index,
                           header_offset=member.header_offset, bytes=size,
                           crc32=member.CRC, sha256=actual)
            for req, ledger_rule, member_rule in exact_pending:
                if req.sha == actual:
                    req.exact = dict(locator, member_rule=member_rule,
                                     ledger_rule=ledger_rule)
                    req.candidate = None
            if actual in unseen[basename]:
                for req in possible[actual]:
                    if req.exact is None and req.candidate is None:
                        suffix = common_suffix(req.path, name)
                        req.candidate = dict(locator, rule='BASENAME_PLUS_EXACT_SHA256',
                                             shared_suffix_components=suffix)
                        req.suffix = suffix
                # First exact content location suffices for CANDIDATE_LOCATION.
                # Do not repeatedly traverse thousands of identical empty-log
                # requirements looking for a cosmetically longer suffix.
                unseen[basename].remove(actual)
            if info['hashed_members'] % 500 == 0:
                print('PROGRESS ' + json.dumps(dict(archive=rel,
                    hashed_members=info['hashed_members'],
                    critical13=summaries(records, critical13))), flush=True)
    guard()
    after = path.stat()
    need((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
         'source archive stat drift: ' + rel)
    need(file_digest(path) == archive_sha, 'source archive SHA drift: ' + rel)
    info['end_sha256_equal'] = True
    print('ARCHIVE_END ' + json.dumps(dict(archive=rel,
        hashed_members=info['hashed_members'],
        critical13=summaries(records, critical13))), flush=True)
    return info


def write_reports(records, header, replace=False):
    json_path, text_path = IMPORT / 'availability.json', IMPORT / 'availability.txt'
    if replace:
        need(json_path.is_file() and text_path.is_file(), 'replace only an existing report pair')
        # These files are this task's generated reports, never source inputs.
    else:
        need(not json_path.exists() and not text_path.exists(), 'reports already exist; no overwrite')
    header['summary'] = summaries(records)
    header['critical_cutoff25_20261013'] = summaries(records, critical13)
    with json_path.open('w' if replace else 'x', encoding='utf-8', newline='\n') as out:
        out.write('{\n')
        for key, value in header.items():
            out.write(json.dumps(key) + ':' + json.dumps(value, ensure_ascii=True) + ',\n')
        out.write('"requirements":[\n')
        for index, r in enumerate(records.values()):
            if index:
                out.write(',\n')
            if index % 100 == 0:
                guard()
            row = dict(declared_path=r.path, expected_sha256=r.sha,
                       groups=sorted(r.groups), kind=category(r.path),
                       empty_content_expected=r.sha == EMPTY_SHA,
                       critical_cutoff25_20261013=critical13(r.path),
                       status='NOT_SCANNED' if not r.scanned else
                       'EXPLICIT_LOCATOR_MATCH' if r.exact else
                       'CANDIDATE_LOCATION' if r.candidate else 'NOT_LOCATED',
                       explicit_locator=r.exact,
                       candidate_location=None if r.exact else r.candidate)
            json.dump(row, out, ensure_ascii=True, separators=(',', ':'))
        out.write('\n]}\n')
    with text_path.open('w' if replace else 'x', encoding='utf-8', newline='\n') as out:
        out.write('CUTOFF20 ARCHIVE BYTE-AVAILABILITY — NOT MATHEMATICAL REPLAY\n\n')
        out.write('Requirement scope: ' + header['requirement_scope'] + '\n\n')
        out.write(json.dumps(header['summary'], indent=2) + '\n\n')
        out.write('CRITICAL cutoff25_20261013:\n' +
                  json.dumps(header['critical_cutoff25_20261013'], indent=2) + '\n\n')
        out.write('Unlocated critical source/certificate paths:\n')
        for r in records.values():
            if critical13(r.path) and not r.exact and not r.candidate and \
                    category(r.path) == 'OTHER_SOURCE_OR_CERTIFICATE':
                out.write(r.path + ' ' + r.sha + '\n')
        out.write('\nCandidate locations are NOT frozen-ledger corrections or historical execution.\n')
        out.write('No proof module imported; no arithmetic replay; no analytic premise discharged.\n')
        out.write('Only members actually hashed have a checked ZIP CRC. Nested ZIP files were not opened.\n')
        out.write('See availability.json for every declared requirement and exact member locator.\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--critical-only', action='store_true')
    parser.add_argument('--replace-reports', action='store_true')
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return
    need(sys.flags.dont_write_bytecode, 'invoke with -B; no bytecode output')
    guard()
    self_sha = file_digest(Path(__file__).resolve())
    records, expected_counts = load_ledgers()
    print('LEDGERS ' + json.dumps(dict(expected_counts=expected_counts,
          unique_paths=len(records), critical13=summaries(records, critical13))), flush=True)
    explicit = collections.defaultdict(list)
    basenames = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in records.values():
        r.scanned = not args.critical_only or critical13(r.path)
        if not r.scanned:
            continue
        for name, rule in ledger_candidates(r.path):
            explicit[name].append((r, rule))
        basenames[PurePosixPath(r.path).name][r.sha].append(r)
    unseen = {name: set(digests) for name, digests in basenames.items()}
    archives = [scan_archive(path, records, explicit, basenames, unseen) for path in ARCHIVES]
    need(file_digest(FINAL) == FINAL_SHA and file_digest(BASE) == BASE_SHA,
         'END pinned ledger hash drift')
    need(file_digest(Path(__file__).resolve()) == self_sha, 'END auditor source drift')
    guard()
    header = dict(status='COMPLETE_READ_ONLY_ARCHIVE_AVAILABILITY_SCAN',
        requirement_scope='ONLY_CUTOFF25_20261013_OTHER_REQUIREMENTS_NOT_SCANNED'
            if args.critical_only else 'ALL_DECLARED_REQUIREMENTS',
        scope='Declared expected byte availability ONLY; no mathematical validation or replay.',
        auditor_sha256=self_sha, expected_group_counts=expected_counts,
        input_ledger_sha256=dict(final_v8=FINAL_SHA, base_GLOBAL20=BASE_SHA,
                                retained_tail_recorded_sha256=TAIL_SHA),
        archives=archives, numerical_oracle_calls=0, proof_modules_imported=False,
        archive_members_extracted=False, frozen_ledgers_modified=False,
        historical_execution_reconstructed=False, mathematical_proof_validated=False,
        candidate_locations_repair_frozen_paths=False,
        memory_peak_bytes=PEAK_BYTES, cpu_seconds=time.process_time()-START_CPU,
        wall_seconds=time.monotonic()-START_WALL, streamed_input_bytes=READ_BYTES,
        streamed_input_counter_scope='Hash/member reads only; excludes parser and ZIP central-directory rereads.',
        limits=dict(peak_MiB=256, absolute_CPU_seconds=300,
                    absolute_wall_seconds=1200, streamed_input_GiB=20),
        caveat='Basename+SHA proves only the existence of matching member content; '
               'identical empty logs do not recover a particular execution. '
               'Named embedded directory trees are included; nested ZIP interiors are not. '
               'Known corrupt standalone threshold31 ZIP is deliberately not an input.')
    write_reports(records, header, args.replace_reports)
    guard()
    print('COMPLETE ' + json.dumps(dict(critical13=header['critical_cutoff25_20261013'],
          summary=header['summary'], memory_peak_bytes=PEAK_BYTES,
          cpu_seconds=time.process_time()-START_CPU,
          wall_seconds=time.monotonic()-START_WALL)), flush=True)


if __name__ == '__main__':
    main()
