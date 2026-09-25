# Publication manuscript

The manuscript source is `berry_esseen_045.tex`. Its only external source
fragment is `certificate-results.tex`, which keeps the archival computation
record separate from the mathematics.

## Build

With Tectonic installed, run from Command Prompt:

```cmd
paper\build.cmd
```

The script writes `output\pdf\berry_esseen_045_publication.pdf`. If Tectonic
is unavailable, it falls back to `latexmk` with `pdflatex`. Both routes stop
on a LaTeX error.

## Finalizing the accepted publication

Leave `certificate-results.tex` in its pending state until the complete
repository command has finished successfully:

```cmd
verify.cmd
```

After `verify.cmd` has printed `ACCEPTED_FULL`, run:

```cmd
paper\finalize.cmd
```

This is the only post-verification publication command. It refuses every
status other than `ACCEPTED_FULL` and requires bundle v2, target `9/20`, exact
scope `n = 2,...,8123`, the pinned FLINT versions, the complete ordered list
of 8,122 per-`n` summaries, agreement of the audit and manifest digests, and
byte-for-byte agreement of every source file bound by the accepted audit.
It then generates `certificate-results.tex` from the audit, builds the final
PDF, and creates:

```text
output\arxiv\berry_esseen_045_arxiv.zip
```

The archive contains the self-contained LaTeX submission source. No numerical
result is copied by hand. A bundle-v1 receipt or a GPU search score cannot
populate the publication. If the LaTeX build fails, the finalizer restores the
previous result fragment instead of leaving a partially finalized manuscript.
