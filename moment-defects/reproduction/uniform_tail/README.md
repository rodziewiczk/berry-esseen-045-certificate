# Fresh native tail replays

These adapters do not replace leaf arithmetic with historical `PASS`, a
composer, a source hash, or a finite sample of indices. They also do not
formally verify the analytic reductions or cited literature. No complete
fresh tail run is claimed merely by adding this directory.

## Original cutoff49 full suite

The explicit source is `BE_cutoff49_20260930.zip`, 16,660,566 bytes, SHA-256
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`.
The archive is the original authored source capsule; its documents, attribution,
original interfaces and third-party statements are preserved unchanged. This
adapter does not relicense archived material. The exact asset is public on
[the source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff49-sources-2026-10-22).
Fetch it without executing archived code:

```console
python -B -S reproduction/uniform_tail/download_sources.py --download --directory source-archives
```

From `moment-defects`, using the actual full Python3.12 executable on Windows:

```console
python -B -S reproduction/uniform_tail/archive49_replay.py --archive PATH/BE_cutoff49_20260930.zip
python -B -S reproduction/uniform_tail/archive49_replay.py --archive PATH/BE_cutoff49_20260930.zip --run
```

The first command prepares and checks all 1,401 original files (33,252,205
bytes); it executes no native mathematics. The second runs the **unchanged**
original `verify.py --output NEW_PATH`, without `--quick`. All ten new or
sign-repaired jobs, three base/mapping checks, and the complete 41-component
retained suite are required. Its top-level execution ledger therefore has
14 entries, one of which is the retained-suite driver. All native captures,
return codes, command arguments and source snapshots are checked afterwards.
No old execution is relabelled as a new capture. The invocation wrapper only
sets the original argv/environment, executes the unchanged driver, and
excludes existing bytecode. It does not transform mathematical source code.

Full mode currently requires64-bit Windows: the adapter rejects an absent
whole-process-tree Job guard before creating work or starting mathematics.
It does not substitute per-process POSIX limits for that guarantee. Source
catalogs and metadata tests remain usable on other platforms.

The original phase-scope audit itself has a Windows path-separator mismatch,
observed in the first hosted run. The separate
[Linux/Docker full-suite controller](LINUX49.md) executes the original source
unchanged in a verified aggregate-limited cgroup instead. Its manual workflow
is [here](../../../.github/workflows/native-replay-linux.yml). A failed Windows
attempt is not a full arithmetic acceptance.

The entire process tree is serial within one owned Job: 512MiB, 7,200 total
CPU seconds, at least 1GiB host RAM reserved, launch after two readings of at
least 1,536MiB five seconds apart. The original 256MiB private-file quota,
4GiB free-disk reserve and 16MiB diagnostic limit remain. Nested temporary
files stay inside the owned work directory. Exhaustion or platform failure
means incomplete verification, never acceptance. Use this only after the
current numerical job finishes; do not run several heavy adapters together.

Successful complete execution writes
`work/<private-epoch>/FRESH_BE49_FULL_SUITE_RESULT.json`. The original native
results are in `fresh-full-result/result.json` and
`fresh-full-result/components/metadata.json`, with each native stdout/stderr.
The result is scoped to the original **selected full native suite**, relative
to its analytic/literature assumptions, not a Lean proof or a completed
all-index composition. No full run has been performed by the structural tests.

## Concrete n31--39 count sub-DAG

Use the already public pinned `cutoff25_20261011.zip`. The catalog is derived
from the exact retained cutoff31 record; old receipts select sources and
expected mathematical scopes only. For each panel a new capsule contains the
original acceptor, all its declared source inputs and its full candidate tree,
but **not** its old acceptance output. The unchanged acceptor reconstructs
every root and split, recomputes every leaf and runs its original corruption
controls. Fresh output must match every original mathematical/source field;
only the interpreter runtime metadata may differ.

```console
python -B -S reproduction/uniform_tail/count_replay.py --archive PATH/cutoff25_20261011.zip --stage base31_34_counts
python -B -S reproduction/uniform_tail/count_replay.py --archive PATH/cutoff25_20261011.zip --stage bridge35_39_counts
```

These commands only print the exact job catalog. Add `--run` for real native
arithmetic, or `--job ID --run` for one catalogued panel. There are 282 jobs
with n31--34 and 120 with n35--39, in52 source families. Auxiliary nonsharp
predecessor counts are retained and are **not** advertised as sharp scalar
theorems for their indices. The archive coordinator uses the separately
disclosed256MiB guard; the original64MiB numerical supervisor is unchanged.
An outer original Windows Job contains each entire supervisor+native branch
from suspended startup, with512MiB/7,200CPU seconds TOTAL and1GiB host reserve.
There is no uncontained wrapper termination window. Numerical mode refuses a
platform without that complete-branch guard. Every attempted panel retains
its work/logs, including resource failures.

Successful individual results are `FRESH_TAIL_COUNT_RESULT.json`; completion
of an explicitly selected count stage additionally writes
`FRESH_TAIL_COUNT_STAGE_RESULT.json`. Neither discharges support, INITIAL,
resource acquisition, Fourier, same-witness or final-composition obligations.
The original n40--48 continuation uses other protocols and is still separately
incomplete here; the weaker BE49 finite-base ceilings must not be mistaken
for those sharp n40--48 results.

## Actual native n40--42 components

The next adapter executes six original full acquisition/confinement/profile
rebuilders, and four complete TINY/MID comparison acceptors (central and
finite left40--42). It does **not** merely call the old global40 composer.
Their full fixed proof objects, exact phase covers and 13 or12 original
corruption controls are checked by their unchanged native acceptors.

```console
python -B -S reproduction/uniform_tail/component40_replay.py --archive PATH/cutoff25_20261011.zip
python -B -S reproduction/uniform_tail/component40_replay.py --archive PATH/cutoff25_20261011.zip --job left40_mid --run
```

Without `--job`, explicit `--run` selects all ten native jobs serially. Each
stage creates a new minimal source/proof capsule. The native fixed-object
manifests bind actual inputs, instead of importing unrelated mutable historical
progress logs as theorem assumptions. Native generated progress remains fresh
output. Every mathematical source/proof input is immutable across its run.
The largest supplied MID witness is about25MB; it is not parsed by the small
supervisor. Numerical workers retain the512MiB/7,200CPU-second ceiling and1GiB
host reserve. Actual resource-to-count, INITIAL/contact and same-witness joins
remain explicit separate obligations. Neither a successful conditional
component nor its status label proves all-law C40--42 or the complete40--48
bridge on its own.

Individual results are `FRESH_COMPONENT40_RESULT.json`; the selected serial
stage writes `FRESH_COMPONENT40_STAGE_RESULT.json`. These are fresh only after
the actual corresponding native numerical job succeeds, not after unit tests.

`stages.py` identifies the exact original support/resource/confinement/local
jobs selected by the full BE49 driver. It is a catalog, not a PASS receipt.

## Structural tests

From `moment-defects/reproduction`:

```console
python -B -S -m unittest uniform_tail.test_tail_adapters uniform_tail.test_component40 -v
```

Synthetic captures and unit tests validate the controller, not the mathematics.
