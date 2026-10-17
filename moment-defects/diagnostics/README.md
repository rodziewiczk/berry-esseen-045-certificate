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

## Result and limits

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
