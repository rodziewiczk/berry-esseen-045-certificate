# Read-only archive availability audit

`cutoff20_archive_availability_2026_10_17.py` is the exact source used for the
published byte-availability reports. It never imports a mathematical proof
module, executes archived code, changes a frozen ledger, or extracts a ZIP
member. It checks expected SHA-256 values and records explicit or candidate
archive locations. This is not numerical acceptance or a proof audit.

The completed scoped run used source SHA-256
`a9d41320a2f2524d440bd2530d0c671ae96e7d2770c1b8580ff61e91063e0654`.
Its [text report](../continuations/cutoff20-2026-10-16/reports/BASE13_AVAILABILITY.txt)
and [complete machine-readable report](../continuations/cutoff20-2026-10-16/reports/BASE13_AVAILABILITY.json)
are preserved separately from subsequent broader scans.

## Initial basename-filtered result and limits

The scoped run tested references to `cutoff25_20261013` against all six source
archives pinned by the [source catalog](../continuations/cutoff20-2026-10-16/source_archives.json).
It did not locate the expected contents for 1,748 source/certificate paths,
184 execution-metadata paths and 228 log paths in each of the two recorded
prefix representations. Another 184 log paths had only same-basename and
same-content candidates, largely shared empty contents. The two prefix
representations must not be added as independent missing physical inputs.

Other requirements in that scoped report are explicitly `NOT_SCANNED`.
Named directory trees inside a ZIP were scanned; interiors of ZIP files stored
as ZIP members were not opened. A candidate location is not an approved
rewrite of the frozen path or evidence of a particular historical execution.
The report is not a claim that matching bytes are absent everywhere.

## Completed filename-independent and nested searches

Two subsequent, separate reports extend the search; they do not replace or
retroactively change the earlier reports.

- [arbitrary13.txt](../continuations/cutoff20-2026-10-16/reports/arbitrary13.txt)
  and [arbitrary13.json](../continuations/cutoff20-2026-10-16/reports/arbitrary13.json):
  every one of the 103,031 ordinary non-Mac members of all six pinned ZIPs was
  read to CRC-checked EOF and SHA-hashed, irrespective of filename. All six
  outer archives were fully hashed before and after scanning. There are nine
  exact-content candidate paths among the 1,748 expected source/certificate
  paths: three empty files and six nonempty files, the latter representing
  only two distinct contents. In each of `local_contact_v13`,
  `local_contact_v14` and `local_contact_v14_combined`,
  `local_contact_binomial.py` matches `finite_binomial_core.py`, and
  `local_contact_heat.py` matches `heat_support50.py` in the continuation.
  **1,739 expected nonempty versions remain unlocated in this scope.**
- [nested13.txt](../continuations/cutoff20-2026-10-16/reports/nested13.txt)
  and [nested13.json](../continuations/cutoff20-2026-10-16/reports/nested13.json):
  every one of the 50 non-Mac ZIP occurrences in the three containing outer
  archives was hashed and CRC-checked; duplicates were byte-compared. The ten
  distinct ZIPs contain 106 non-Mac file members, all hashed irrespective of
  name, with zero matches to the 1,748 expected paths. No further ZIP children
  were detected by content, so there was no depth-limit truncation. This run
  fully hashed each outer archive once and checked stable path/fd identities
  and stat signatures, not a second full-archive hash.

The source pins are respectively
`8843d9a4c231d63c057a0c7f853709b17aa9abcfcd405304d18e77b61161d9d3`
and `c758e53eeb70ab8c1c75322b2f709370816f27c6d4fb2c2c07251f53daef57b6`.
The flat probe selected `historical_tail_edges` with the `work/` prefix;
the nested probe selected `files_sha256` without that prefix. Their complete
path-to-expected-SHA maps were compared, not merely their cardinalities:
after removing only the leading `work/` from the flat paths, the canonical
sorted compact JSON map has SHA-256
`d8bfc1f405db5080266739344b025bbd596fc9e96d56dd337c6f7b6375379fd3`,
exactly the digest recorded by the nested probe. There are 1,748 keys and
1,678 distinct expected SHA values. This comparison does not authorize any
rewrite of the frozen paths.
Both completed within their 256 MiB observer bounds, without proof imports,
mathematical workers, extraction, or source modification. Empty-byte matches
do not recover historical provenance. These searches concern exact bytes,
not reconstructed/concatenated/encoded content or other archives elsewhere.

The broader original audit's [complete reports](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff20-sources-2026-10-17)
are release assets named `CUTOFF20_ALL_ARCHIVE_AVAILABILITY.json` and `.txt`.
They preserve their original basename-filtered findings. The two probes above
refine availability for the baseline-13 source/certificate subset only; their
counts must not be added to duplicated prefix representations or other
overlapping ledger counters. None of these reports proves an analytic lemma
or freshly accepts a numerical certificate.

## Reproduce this diagnostic

First obtain the six original ZIPs with the published source downloader.
The auditor deliberately preserves the original workspace-relative layout;
its root is two directories above the directory containing this script.
Prepare the following layout beneath that root, copying bytes unchanged:

```text
tmp/cutoff20_import_2026-10-17/
  continuation_cutoff20_20261016_final.zip
  cutoff20_20261016.zip
  cutoff25_continue_20261015.zip
  cutoff25_rethink_20261015.zip
  continuation_cutoff20_20261016/
    b0/sequential_synthesis_v8/CONDITIONAL_CUTOFF20_COMPOSED.json
    bn/global20_synthesis_v5/GLOBAL20_SYNTHESIS.json
research/imports/drive_20261012/
  cutoff25_20261011.zip
  continuation_20261011_wrap.zip
```

The two JSON files are unchanged entries from the final continuation ZIP;
the auditor checks their pinned hashes before reading them. Install its
streaming JSON parser into the declared local dependency directory:

```sh
python -m pip install --target tmp/cutoff20_audit_deps ijson==3.6.0
python -B -S moment-defects/diagnostics/cutoff20_archive_availability_2026_10_17.py --run --critical-only
```

The reports are written below `tmp/cutoff20_import_2026-10-17`. Existing
reports are not replaced unless `--replace-reports` is explicitly supplied.
Omit `--critical-only` to inspect all declared requirements, rather than
only the missing predecessor baseline. Both modes retain bounded memory,
CPU, wall time and streamed hash-input limits. A limit exit is not a
successful complete audit. No limit increases or mathematical workers are
hidden in this diagnostic.

With the same fresh layout and pinned parser, reproduce the two additional
probes separately (each refuses to overwrite its report pair):

```sh
python -B -S moment-defects/diagnostics/cutoff20_archive_arbitrary_name_probe_2026_10_17.py --run
python -B -S moment-defects/diagnostics/cutoff20_nested13_probe_2026_10_17.py --run
```

The first probe streams all ordinary members, bounded at 20 GiB counted
hash/member input, 300 CPU seconds and 256 MiB peak working set. The nested
probe has a 1 GiB combined disk/decoded-input bound, 64 MiB per member, depth
three, 300 CPU seconds and 256 MiB peak working set. Limits and exclusions are
explicit in each source and report. A limit failure is not a complete result.

The small target-map comparison can be repeated from this directory:

```python
import hashlib, json
from pathlib import Path
p = Path('../continuations/cutoff20-2026-10-16/reports')
a = json.loads((p / 'arbitrary13.json').read_text())
n = json.loads((p / 'nested13.json').read_text())
m = {s.removeprefix('work/'): t['expected_sha256']
     for t in a['targets'] for s in t['expected_paths']}
d = hashlib.sha256(json.dumps(m, sort_keys=True,
    separators=(',', ':')).encode('utf-8')).hexdigest()
assert len(m) == 1748 and len(set(m.values())) == 1678
assert d == n['selected_path_sha_map_sha256']
```
