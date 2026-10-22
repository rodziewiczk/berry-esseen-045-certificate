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
python -B -S reproduce.py --component c5.high --archive PATH/cutoff5_20261020.zip
python -B -S reproduce.py --component c5.owncaps --archive PATH/cutoff5_20261020.zip
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

Fresh local replay on 22 October completed `c5.gapfree` (all 60 roots, 1994
nodes, 1027 leaves and both exterior rays, plus corruption controls) and
`c5.support` (the original nine + nine + one support rows), and both `c5.high`
variants (3+4 supported scopes, two fresh native computations each, original
native acceptance with 8+9 corruption controls). This statement is
an execution report, not an input to subsequent mathematical acceptance.
The original analytic contact/C4/support/Fourier premises remain scoped exactly
as stated by the individual receipts. n4 and the all-index run remain incomplete.

The HIGH adapter creates honest new execution captures at its actual working
directory; it does not rewrite historical macOS paths. The owncaps adapter also
includes the separately needed global coarse bound 0.429 and its independent
readback. The selected stronger B3 cap 0.412 substitutes for the older 0.414
on the identical supported domain; no missing historical B3-v2 replay is
claimed. This new owncaps adapter is not counted as fresh arithmetic until
its complete numerical run succeeds. Its Fourier-extension adapter executes
the unchanged complete Fourier subproof of the pinned review, not the unrelated
B3 preparer audit; that scope is explicit in its receipt.

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
The default `root-first` traversal evaluates untouched original count roots
before returning to depth-first search. An in-memory frontier avoids a full
forest traversal at every step; complete geometry is checked on resume and at
the end. Neither optimization changes the oracle, closed boxes or node limits.
The search preserves original roots, exact closed subdivisions and the native
10,000-node/depth-128 limits. It never upgrades a partial tree into a proof.
Candidate checkpoint leaves are untrusted. When a candidate is complete, a
**separate original native checker process** recomputes every leaf and runs all
24 mutation controls before a conditional count acceptance is reported. Parent
resource hypotheses and whole-proof composition remain separate obligations.
Do not execute the underlying unprotected `count_discovery.py` directly.

Synthetic engine tests can be included in the test command by adding
`all_indices.test_discovery`. These tests are not numerical certificate runs.

`import_count_prefix.py` can reuse the externally pinned old B3/p33 prefix
(1329 candidate leaves), after matching its complete native header and
reconstructing every closed split and pending box. Reused leaf results are
untrusted and must all be recomputed by native acceptance. Its tests are in
`all_indices.test_import_count_prefix`.

The private-output scanner now retries an entire scan on an observed atomic
rename, requiring two matching complete file inventories. It retains or
strengthens the original containment, symlink, memory and disk guards and never
accepts a partially enumerated quota. It is a sampled guard, not a filesystem
transaction. Tests are in `all_indices.test_stable_guard`. Frozen proof sources
and the archived runner file are not edited.

## New conditional V14 source epochs

Both original count-source archives are now public GitHub release assets. Fetch
and verify them, without executing archived code:

```console
python -B -S reproduction/all_indices/download_count_sources.py --download --directory count-archives
python -B -S reproduction/all_indices/prepare_b3_v14_epoch_2026_10_22.py --old-archive count-archives/cutoff25_20261011.zip --base13-archive count-archives/cutoff25_20261013.zip --index 31 --output work/new-v14-p31
```

Use index 32 and a different new output directory for the other panel. Keep
the canonical archive basenames when recreating the pinned source-epoch
identities. The reviewed p31 design is
`6ca73188c5a6969c1f0ec69f41cb0fac660003cf0515fdcadeeda83afcf654f0`;
p32 is `230a6bb37696c1e79d62847d89090d4187d78d41aa6c98ccbe91c54e1f8f950b`.
The preparer checks source transforms, premise rejection and all 26 original
root geometries, but deliberately never evaluates a mathematical cell.

These are **new conditional source epochs**, not recovered historical V14
identities. They retain all 71 original V12 kernel/proof files and all 21
V14 additions, including nine runtime helpers. The two additional contract
fields explicitly require the same unrestricted attained positive-closed
witness and the deletion allowance 5/16. Bound written derivations explain
these hypotheses; fresh parent arithmetic and a new same-witness regional
composition remain required. Neither inserted fields nor source hashes
establish those premises.

Guarded discovery uses the same `discover_count.py` command with the new capsule
and design pin. Original roots, strict target, limits and 24 native mutation
controls remain. Separate distinct result identifiers prevent a new V14
acceptance from masquerading as a historical V12/V14 receipt. An incomplete
tree is never accepted, even if all source tests pass.

## Conditional acquisition arithmetic

`c5_acquisition_plan.py` records the exact 12 selected INITIAL jobs and 15
resource replay/accept jobs, including the full 1200-panel resource partition.
Its `--inspect-cache PATH` mode checks their pinned source closures only.
All 27 closures were located; each minimal per-job mirror is below 40 MiB.
The numerical substeps now have separate guarded entry points:

```console
python -B -S reproduce.py --arithmetic-only c5.initial --archive PATH/cutoff5_20261020.zip
python -B -S reproduce.py --arithmetic-only c5.resources --archive PATH/cutoff5_20261020.zip
python -B -S reproduce.py --arithmetic-only c5.complement --archive PATH/cutoff5_20261020.zip
```

Append `--inspect` to check inputs only. These commands intentionally do not
register `c5.initial` or `c5.resources` as acquired proof nodes. They recompute
the original finite arithmetic while leaving exact joins to genuinely
replayed support, HIGH, owncap and INITIAL parent facts outstanding. Historical
parent receipts are immutable candidate references, not new computations.
Neither the existence of these adapters nor their unit tests establishes a
successful numerical run.

The complement substep runs the original complete integration twice (all 41
closed strips and 42 attempted meshes), the pinned native arithmetic verifier
and its 10 mutation controls, and the independent Fourier arithmetic readback
with 16 Fourier/JSON controls. Its three support-corruption controls and all
fresh support/Fourier/contact parent joins are explicitly outside this substep;
no full native complement acceptance is claimed.

INITIAL runs all 12 original complete candidates, including every finite
transition, moment cell, probability panel and native mutation control. The
resource command runs all 15 selected jobs and all 1200 panel obligations.
Its original checker is executed through an explicitly declared, pinned
metadata-only source port: POSIX source-map keys, the emitted INITIAL path,
and one separately prevalidated semantic-command reference. Actual operating
system commands are captured under their real names; source bytes, old JSON,
numerical expressions and native corruption controls are not rewritten.
Every original source and the finite AST-edit inventory are checked. This
is not advertised as unchanged native Windows acceptance.

`c5_initial_join.py` checks exact support/HIGH/owncap implications for an
INITIAL artifact, including the whole closed rho/support domain, the candidate
input SHA, all finite transitions and the complete final cover. Its companion
`c5_parent_evidence.py` rechecks artifact/source/capture bindings. These are
post-hoc readers, not an authenticated execution history: their output leaves
`execution_observed_by_this_reader` and `fresh_parent_fact_joins_verified`
false. A separate executing controller must observe the numerical runs before
using those implications in a fresh proof composition. C4, attainment/contact
and the stated analytic Fourier/literature inputs remain explicit premises.

## Whole-proof obligations still outstanding

The missing work is broader than seven forest files. At this checkpoint:

- n4 still needs its two complete new 260-class ROOT passes.
- C5 needs fresh INITIAL/resource runs, their exact parent joins, the complete
  295-forest count run (75,178 leaf evaluations), the Fourier complement and
  the final same-law domain composition. The three completed C5 blocks above
  do not discharge these obligations.
- The currently selected n25 proof additionally needs seven complete native
  B3/B4 forest acceptances; checkpoints and newly prepared V14 source epochs
  are not those acceptances.
- The public guarded dispatcher does not yet implement the complete numerical
  continuation n6 through n30, the 31--34 base, the 35--48 bridge, or the
  support/resource/confinement/local stages of the genuinely uniform tail.
  Archived source entry points and identity-only closure checks are not a
  substitute for executing those stages and checking their parent domains.
- A global executing controller must compose all completed stages. It remains
  disabled; `--all` reports missing obligations and exits unsuccessfully.

Published literature and the manuscript's analytic reductions remain explicit
mathematical inputs. No claim of a Lean proof or a completed all-index replay
is made by this directory.
