# Five summands in the iid Berry--Esseen conjecture

Kacper Rodziewicz and Bartosz Kołodziejek. Working draft, 20 October 2026.

[PDF](manuscript.pdf) · [LaTeX](manuscript.tex) ·
[abstract](abstract.txt) · [dependency graph](dependency_graph.svg)

The focused manuscript proves the isolated implication

$$C_4\le C_E\quad\Longrightarrow\quad C_5\le C_E.$$

The adopted four-summand input is Theorem 26.1 of the authors' previously
published [Hexagon version 3](https://hexagonmath.org/2610.00147v3).
The other cited inputs are Prawitz smoothing and Shevtsova's iid estimates.
The new fifth-index proof does not use an eventual-in-n theorem.
It does **not** assert strict C5 < CE.

A separate section records the completed finite 6--9 chain and the retained
tail from 10. Its all-n>=6 statement remains conditional on the explicitly
named analytic, Fourier and historical continuation premises A6/F/T10.
The supplied cutoff6 final receipt expressly sets its unqualified and
full-conjecture flags false. The manuscript does not turn these into an
unconditional solution.

## What was retained

The PDF contains the fixed-index attainment/contact reduction, the complete
moment cover, the new gap-free conditional-binomial/Cantelli proof, the
gapped count mechanism, the contradiction, and the precise conditional
dependency boundary. Its continuous Fourier/support/resource reductions
are part of the proof supplement, not deductions from successful hashes.
The previous structural/asymptotic/stability and historical 0.45 exposition
is preserved in the [archived full manuscript](../paper/manuscript.pdf),
but is not a dependency of this focused fifth-index argument.

The original 0.45 project and its dates are unchanged.

## Retrieve original sources

The [source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff5-sources-2026-10-20)
hosts all three original packages pinned by source_archives.json.
No Drive account is needed. With Python 3.11 or newer:

    python -B -S download_sources.py --download --directory source-archives
    python -B -S download_sources.py --directory source-archives --extract-to source-tree

The extraction directory must be new. Source epochs are kept separate.
The downloader checks transport integrity and archive paths; it never imports
or executes proof code and is not a mathematical verifier.

The older packages still relevant to the conditional tail are preserved in
the [previous source release](https://github.com/rodziewiczk/berry-esseen-045-certificate/releases/tag/cutoff20-sources-2026-10-17).
No dependency-complete global replay is claimed.

## Fifth-index reproduction boundary

Inside the extracted fifth-index package, the directory
cutoff5_20261020/root/delivery_extract_v1/ is the original bundled proof
workspace. It includes README.txt, REPRODUCTION.txt, the source manifest,
the verifier and the continuous mathematical proof sources.
Read those original instructions before executing archived code.

The original entry points, run from that bundled directory, are:

    python -B verify_package.py
    python -B verify_package.py --compose

The first checks the package bytes. The second reconstructs and reruns the
final assembly in a temporary workspace. Neither reruns all expensive native
arithmetic. Source-specific commands for the native acquisitions and complete
leaf acceptances are documented in the original REPRODUCTION.txt.

Our new read-only availability scan located and SHA-matched **all 16,576
files** bound by the final fifth-index receipt, including all 45 indexed
continuous proof sources. The final receipt SHA-256 is
923a0d0cf3c481ae60c5e2b69d886098a7501f916a52668b37b0198f26fde4a0.
This is file completeness/integrity evidence, not a new arithmetic replay or
independent mathematical verification. The fifth-index package and the
conditional tail have different completeness and trust boundaries.

## Rebuild the paper

The manuscript.tex source has no external LaTeX inputs, figures or bibliography
files. It was checked with the desktop compiler and Tectonic 0.17.0.
For an installed Tectonic:

    tectonic manuscript.tex

The separate Hexagon source ZIP contains exactly that one TeX source, without
PDFs, Lean code, proof data or executable programs. The validate_hexagon.py
script checks source structure, references and exact ZIP bytes; it does not
verify mathematics or compile TeX. Supply its optional paths explicitly when
running outside the original workspace; its defaults preserve that layout.

ChatGPT and Codex assisted proofs, certificates and manuscript preparation,
using GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra. This is not a Lean formalization
or a claim of external referee acceptance. Code follows the repository MIT
license; original archived documents retain their applicable rights and
attribution.
