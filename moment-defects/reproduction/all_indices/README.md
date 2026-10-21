# Fresh arithmetic reproduction

This directory adds a single entry point to the archived proof sources. It does
not turn historical `PASS` files or successful hash comparisons into fresh
mathematical verification. The complete all-index replay is **not yet available**:
some adapters and seven selected n25 B3/B4 forests remain missing. `--all`
therefore exits with code 2 and lists the unimplemented obligations.

Run the following from the repository's `moment-defects` directory, using Python
3.12 without `-O` or `-OO`. No extra Python package is required for these entry
points. The existing protected numerical launcher currently requires Windows;
this is not advertised as a portable macOS/Linux full-proof verifier.

```console
python -B -S reproduce.py --plan
python -B -S reproduce.py --component n2
python -B -S reproduce.py --component n3 --backend cpp
python -B -S reproduce.py --component n4
```

Run numerical stages **one at a time**. n3 C++ requires `g++` and Boost headers.
Use `--compiler-dir PATH` and `--boost-dir PATH` for private installations; no
global environment modification is needed. The optional `windows_toolchain.py`
downloads pinned upstream toolchain archives into a new private directory.
Its `--verify-cache-only --cache EXISTING --directory UNUSED_NEW_PATH` mode only
checks existing assets and does not download or extract anything.

`--backend python` selects a separate exact-integer translation for n3, also
preceded by the original initial-polynomial identity audit. It is substantially
slower; a complete fresh acceptance of that translation is not claimed here.
The native C++ n3 checker and both n2 checkers have completed fresh local runs.

## Five-summand sources

The public source asset is on the repository's release
[`cutoff5-sources-2026-10-20`](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff5-sources-2026-10-20).
Fetch the pinned release assets without executing their archived code:

```console
python -B -S five-summands-2026-10-20/download_sources.py --download --directory source-archives
```

Then supply the downloaded archive explicitly (replace `PATH` with
`source-archives` when using that command):

```console
python -B -S reproduce.py --component c5.counts --archive PATH/cutoff5_20261020.zip --inspect
python -B -S reproduce.py --component c5.counts --archive PATH/cutoff5_20261020.zip
python -B -S reproduce.py --component c5.gapfree --archive PATH/cutoff5_20261020.zip
python -B -S reproduce.py --component c5.support --archive PATH/cutoff5_20261020.zip
```

`--inspect` is only a source-catalog check. The counts command reconstructs and
checks all 295 selected count forests, including their original mutation tests.
It does not discharge support, resource, initial-bound or composition premises.
The gap-free adapter calls the frozen independent arithmetic routines for all
1027 compact leaves and both exterior rays. It does not treat historical
execution-capture paths as mathematical premises, and its scope is only the
specified positive closed-CDF branch and moment rectangle, not the full theorem.
These new C5 replay adapters must themselves complete successfully before their
obligations can be counted as freshly checked.

The support adapter prepares and verifies the full selected source graph plus
the pinned omitted-import supplement, then runs the three unmodified original
support protocols with fresh outputs. Its acceptance remains conditional on
the original analytic contact theorem and C4 predecessor premise; it is not a
new C5 or all-index conclusion. `--inspect` prepares inputs only.

## Outputs and safety

Each attempt uses an exclusive directory under `work/`. Complete finite attempts
write `FRESH_REPLAY_RESULT.json`; count and gap-free stages write separately
scoped receipts. Failed children preserve bounded diagnostic logs and do not
produce successful receipts. Candidate certificates are never accepted merely
because an earlier run accepted them. Source identities are checked before use.

The protected supervisor retains at least 1 GiB of host RAM, waits for 1536 MiB
before launching, and enforces worker memory and CPU limits. Resource exhaustion
means **incomplete verification**, not an accepted certificate. Do not launch
several heavy stages concurrently or bypass a guard. Deep Windows paths use an
extended-path alias without changing archived proof code or acceptance rules.

Coverage is explicit in `coverage.py`: individual small indices, every finite
continuation, and a genuinely uniform infinite tail. The controller rejects a
finite tail, a missing index, missing parents, cycles, and historical receipts
without fresh arithmetic. Literature inputs remain explicitly external.

Control-plane regression tests (not mathematical certificate verification):

```console
cd reproduction
python -B -S -m unittest all_indices.test_coverage all_indices.test_reproducer -v
```

The existing historical certificates and manuscript are preserved. This work
does not assert Lean verification or a completed all-index computational replay.

## Reconstructing missing count forests

`prepare_missing_count.py` extracts all 77 original files of a selected capsule
from `cutoff25_20261011.zip`, checking an externally pinned design and every
source digest. Five targets have the original requested V12 implementation.
The two `*-v12-alternative` targets are available older implementations for the
missing selected B3/p31 and p32 V14 payloads: **they are not the missing historical
V14 certificates**, and a new composition/interface audit is required if they
produce useful replacements.

For example, from `moment-defects`:

```console
python -B -S reproduction/all_indices/prepare_missing_count.py --archive PATH/cutoff25_20261011.zip --target b4-q0 --output work/original-b4-q0
python -B -S reproduction/all_indices/discover_count.py --capsule work/original-b4-q0 --design-sha256 4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7 --seconds 600
```

The protected search creates its own private work directory, prints its path,
and stores `search/CHECKPOINT.json`. Continue with the same command and
`--resume PATH/TO/CHECKPOINT.json`; each continuation uses a new private epoch.
Two stable checkpoint filenames preserve a fallback without transient renames
that can race a supervisor's scratch-file scan. Resume can fall back to the
backup if the latest write was interrupted. Search-code changes may reuse
candidate topology only when the frozen native contract/source and strategy
bindings still match; original native arithmetic is never reused as acceptance.
The search preserves original roots, exact closed subdivisions and the native
10,000-node/depth-128 limits. It never upgrades a partial tree into a proof.
Candidate checkpoint leaves are untrusted. When a candidate is complete, a
**separate original native checker process** recomputes every leaf and runs all
24 mutation controls before a conditional count acceptance is reported. Parent
resource hypotheses and whole-proof composition remain separate obligations.
Do not execute the underlying unprotected `count_discovery.py` directly.

Synthetic engine tests can be included in the test command by adding
`all_indices.test_discovery`. These tests are not numerical certificate runs.
