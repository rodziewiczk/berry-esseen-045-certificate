# Moment defects and sharp iid Berry--Esseen bounds

Kacper Rodziewicz and Bartosz Kołodziejek. Working draft, 12 October 2026.

[Read the manuscript](paper/manuscript.pdf) · [LaTeX source](paper/manuscript.tex)

For a standardized iid marginal $P$, write

$$
R_n(P)=\frac{\sqrt n\,\Delta_n(P)}{\rho(P)},\qquad
C_n=\sup_P R_n(P),\qquad
C_E=\frac{3+\sqrt{10}}{6\sqrt{2\pi}}.
$$

The six principal results are the exact matching-binary moment defect;
linear Fourier stability; eventual two-point optimality

$$
C_n=C_Q^*(n)<C_E;
$$

the oscillatory second-order asymptotic; the effective strict cutoff

$$
C_n<C_E\quad(n\ge31);
$$

and the unrestricted finite-index bounds

$$
C_2\le\frac{2\sqrt2}{7},\qquad
C_3\le\frac{59\sqrt3}{250},\qquad
C_4\le\frac{4097}{10000}<C_E.
$$

Eventual two-point optimality is qualitative: **31 is a cutoff for the strict
upper bound, not a claimed cutoff for two-point optimality.** The unrestricted
sharp bounds at indices 5--30 are not established here.

The opening section explains the elementary historical $C\le0.45$ argument,
then passes from a fixed Rademacher reference to the binary law matching the
third moment. Mattner--Shevtsova's comparison and Shevtsova's sharp moment
inequality are explicitly credited. The appendix records the elementary
interval-certificate argument. The original `0.45` project at the repository
root is unchanged.

## Reproduction

Use ordinary Python 3.11 or newer, without `-O`. Start from this directory.
The commands have deliberately different meanings:

```sh
# No imported proof code: check every archival cutoff-31 input byte.
python -B -S reproduction/closure31.py

# Extract the exact closure into a NEW directory, preserving its hierarchy.
python -B -S reproduction/closure31.py --extract work/cutoff31

# Small source/scalar and launcher fixtures; not a mathematical replay.
python -B run_reproduction.py --tiny

# Exact symbolic identities and scalar constants; installed SymPy required.
python -B run_reproduction.py --scalars

# Long, serial n2/n3 verification and TWO freshly computed entire ROOT4 passes.
# Requires 64-bit Windows, g++ C++17 and Boost.Multiprecision.
python -B run_reproduction.py --full
```

See [the arithmetic guide](reproduction/README.md) for the finite-index runner,
and [the cutoff-31 guide](reproduction/CUTOFF31.md) for its actual acceptors and
the distinction between integrity, composition and arithmetic replay. No source
or data is downloaded by these verification commands.

The cutoff-31 capsule contains **all 9,518 available inputs byte-bound by the
final statement**, plus that statement itself. Its three binary parts are an
ordered split ZIP, checked and joined by `closure31.py`; do not unzip a part
alone. This is a dependency-complete archival capsule at the final record's
explicit retained analytic/certificate scope. Packaging and hashing are not a
fresh verification of the mathematics. The source archive retains earlier
arithmetic acceptances and a documented substitution of available analytic
sources for one unavailable historical manuscript. It does not contain the
204 unavailable historical execution logs, and they have not been invented.

**There is not yet a single freshly tested command replaying the entire
historical cutoff-31 dependency DAG.** The full finite-index runner likewise
does not verify the manuscript's uniform analytic or asymptotic proofs: those
are written mathematical arguments, with their cited literature inputs.
These limits are explicit rather than hidden behind an `ACCEPTED` label.

## Authors, tools, and licenses

ChatGPT and Codex assisted mathematical development, certificate work and
manuscript preparation, using GPT-5.6 Sol, GPT-6.1 Sol and GPT-6 Astra. The
authors remain responsible for the claims and final text. This is a draft, not
a claim of peer review or a new whole-paper Lean verification.

Code follows the repository's MIT license. External dependencies and archival
documents retain their own applicable licenses and attribution. This catalog
does not change the historical `0.45` project or its archival date.
