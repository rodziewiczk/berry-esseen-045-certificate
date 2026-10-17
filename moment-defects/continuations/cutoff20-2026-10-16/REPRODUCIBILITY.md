# Source availability and mathematical replay

This guide separates four different tasks. None is silently substituted for
another.

| Task | What a successful result establishes |
|---|---|
| Source retrieval | The published archive bytes are available from GitHub |
| Integrity inspection | They match the pinned sizes and SHA-256 values |
| Arithmetic acceptance | The original numerical acceptor recomputes every required inequality |
| Whole-proof composition | Every mathematical premise, domain and dependency is discharged |

The first two are supplied by the tools here. A portable fresh whole-proof
replay of the cutoff-20 dependency graph is **not yet verified**. Original
conditional qualifications are preserved in the manuscript and archives.

## Get the source archives from GitHub

From this directory, with Python 3.11 or newer:

```sh
python -B -S download_sources.py --download --directory source-archives
```

No Drive access or Google account is used. The release assets and their exact
hashes are listed in `source_archives.json`. The available historical baselines
are large; streaming downloads use bounded buffers. An existing complete file
is checked, not overwritten. An interrupted `.part` file is retained for
inspection rather than silently replaced.

To inspect already downloaded archives without network access:

```sh
python -B -S download_sources.py --directory source-archives
```

To unpack into a **new** directory, preserving source epochs separately:

```sh
python -B -S download_sources.py --directory source-archives --extract-to unpacked
```

This does not merge snapshots, rewrite captured paths, or execute proof code.
Finder resource forks are omitted; original mathematical files are copied
unchanged. The original ZIPs remain intact. Do not substitute the incomplete
standalone historical threshold-31 ZIP: the full older cutoff-25 archive embeds
that source folder, and the separately published `reproduction/closure31`
capsule preserves its pinned inputs.

## Reproduce the manuscript PDF

The self-contained source is `../../paper/manuscript.tex`. It has no external
LaTeX inputs or figure dependencies. The delivered PDF was compiled from that
source with Tectonic 0.17.0 and also checked with the desktop LaTeX compiler.
For a local Tectonic installation:

```sh
tectonic ../../paper/manuscript.tex
```

A normal TeX Live installation with the packages named in the preamble can
also compile the source; repeated passes resolve its cross-references. This
is document compilation, not numerical certificate verification.

## Fresh arithmetic replay: actual commands and current boundary

The count capsules contain standard-library Python arithmetic, including
`Fraction`, `isqrt` and `comb`. For a selected capsule, the original entry point
is `python -B -u count_protocol.py accept`, run from that capsule. It needs its
unchanged contract, full forest, manifest and every source/data file listed by
the manifest. It freshly evaluates the complete forest and negative controls;
the constructor need not be rerun merely to accept an existing complete forest.

Other indispensable layers are the actual-index INITIAL, resource and
high-moment support calculations. They are not replaced by successful count
panels. The exact original commands, working directories and inputs are stored
in the archived captures. Older launchers have fixed past deadlines and
POSIX-specific process controls; they are not current portable run commands.

Fresh acceptance must take place in new named copies, preserving the original
evidence. New receipts contain new timings, so their hashes normally differ
from historical receipts. They must be bound by a **new** replay ledger, not
written into an old hash graph or passed off as old executions.

The historical composers compare absolute captured paths and commands.
Windows also differs in path separators in some source-review lookups. A
reviewed relocation/normalization layer or fresh capture/composition layer is
therefore needed for a true end-to-end port. No such layer is claimed by the
source downloader. Linux/POSIX is the simplest first target for those older
resource tools; the byte-retrieval tools themselves use ordinary portable
Python and do not import archived mathematical code.

## Remaining obligations

The supplied final continuation explicitly retains parts of the older
analytic/contact/resource/Fourier framework and historical computations.
References to a `cutoff25_20261013` baseline are being reconciled against the
available source archives; a matching filename alone is not sufficient.
Missing recorded paths may correspond to relocated bytes, but locating equal
bytes is not a fresh arithmetic replay or a proof of an analytic implication.

Before advertising a fully reproducible cutoff-20 theorem, these dependencies
must be resolved or replaced by independently checked proofs, and a fresh
complete replay/composition must pass. Source availability, stored successful
receipts and the completed conditional chain alone do not establish that claim.
