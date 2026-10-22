# Berry--Esseen proof material

Kacper Rodziewicz and Bartosz Kołodziejek.

## Fresh replay tooling: 21 October 2026

The [fresh arithmetic reproduction guide](reproduction/all_indices/README.md)
documents the new `reproduce.py` entry point, pinned source inputs, serial
resource-bounded workers, and explicit proof-obligation coverage. It includes
n2, native C++ or Python n3, n4, and selected C5 arithmetic adapters.
**Full all-index replay remains incomplete**; missing adapters and seven n25
forests are reported rather than silently accepted. Source integrity alone is
not a mathematical replay. Existing historical material is unchanged.

### Additional replay controllers: 22 October 2026

The [uniform-tail guide](reproduction/uniform_tail/README.md) adds an explicit
FULL replay of the unchanged original cutoff49 capsule, plus the 402 selected
strict-count jobs at n31--39 and ten native n40--42 components. The original
cutoff49 source archive is pinned and publicly downloadable. A manual
[native replay workflow](../.github/workflows/native-replay.yml) runs its full
suite on a separate Windows runner and preserves fresh results or failure
diagnostics; adding or dispatching that workflow is not itself acceptance.

The [finite-continuation controllers](reproduction/continuations/) and
[C5 domain composition checks](reproduction/c5_composition/README.txt) retain
their conditional parent obligations explicitly. Structural tests check code
and corruption cases, not the numerical proof. These additions do not make
the all-index entry point complete.

## Current focused manuscript: 20 October 2026

[Five summands in the iid Berry--Esseen conjecture](five-summands-2026-10-20/README.md):
[PDF](five-summands-2026-10-20/manuscript.pdf),
[LaTeX](five-summands-2026-10-20/manuscript.tex),
[abstract](five-summands-2026-10-20/abstract.txt),
[dependency graph](five-summands-2026-10-20/dependency_graph.svg).

The main fifth-index theorem is

$$C_4\le C_E\ \Longrightarrow\ C_5\le C_E.$$

The four-summand input is the previously published Hexagon version 3,
Theorem 26.1. Prawitz and Shevtsova are the other cited external inputs.
All 16,576 files bound by the supplied final fifth-index receipt, including
its 45 indexed continuous proof sources, were located and SHA-matched in the
new source bundle. This is byte availability/integrity, not a fresh
mathematical replay.

The finite 6--9 chain and retained tail from 10 are presented separately
with their explicit A6/F/T10 hypotheses. **No unconditional all-index
solution or Lean formalization is claimed by this release.**

The [original source packages](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff5-sources-2026-10-20)
and a bounded downloader are linked from the focused manuscript directory.
The Hexagon ZIP contains one self-contained TeX file, not proof code or data.

## Preserved earlier work

The [full structural/asymptotic manuscript of 17 October](paper/manuscript.pdf)
and [its source](paper/manuscript.tex) remain available. Its moment defects,
eventual two-point optimality, lattice asymptotics, stability refinements and
historical 0.45 exposition were not deleted. They are not included in the
focused fifth-index paper merely because they exist.

The earlier [conditional cutoff20](continuations/cutoff20-2026-10-16/README.md),
[archive diagnostics](diagnostics/README.md), [cutoff31 capsule](reproduction/CUTOFF31.md)
and [finite-index arithmetic guide](reproduction/README.md) retain their own
scope and reproduction boundaries. The new C5 proof does not silently
discharge retained premises in those older continuation branches.

The [22 October count-base source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff25-base-sources-2026-10-22)
adds the original 13 October archive required by the new conditional V14
reconstruction tooling. Its published SHA-256 matches the local original.
Source availability is not acceptance of the still-incomplete count forests.

The original 0.45 certificate project at the repository root is unchanged.
Its dates, attribution and historical files are preserved.

## Tools and licensing

ChatGPT and Codex assisted mathematical development, certificate work and
manuscript preparation using GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra. The
authors remain responsible for the claims and final text.

Code follows the repository MIT license. Archived external documents and
dependencies retain their applicable rights and attribution.
