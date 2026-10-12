# Moment-defect arithmetic reproduction

This separate catalog contains verbatim source/data copies for the manuscript's
two- and three-summand certificates, the accepted conditional four-summand
physical ROOT calculation, and selected exact analytic/symbolic checks. It does
**not** reproduce the whole paper, its later cutoff packages, uniform asymptotic
arguments, or a Lean formalization. The repository's inherited MIT license is
unchanged. Boost and SymPy are external dependencies under their own licenses.

From `moment-defects/`:

```
python run_reproduction.py --tiny
python run_reproduction.py --scalars
python run_reproduction.py --full
```

The default is `--tiny`: exact file-integrity checks, supplied scalar fixtures,
and a bounded launcher child which calls no mathematical producer. Hashes and
that fixture are not certificate replay. `--scalars` additionally runs exact
SymPy identities and rational analytic constants; install SymPy in the selected
Python environment yourself. No dependency is downloaded by this runner.

`--full` is a deliberately long calculation. The unchanged n4 peak-memory guard
requires **64-bit Windows**; the runner rejects full mode on other platforms
instead of disabling or monkeypatching that guard. The n3 checker additionally
requires `g++`, C++17 and Boost.Multiprecision headers. Its compiler/kernel is
rebuilt from source, never supplied as a binary. No performance or successful
combined-runtime fit is asserted merely by shipping these files. Stop other
heavy mathematical jobs before starting; only this runner's owned stage is
controlled, not every process on the machine.

## Exact finite paths

| Component | Frozen path below `code/` | Actual operation |
|---|---|---|
| n2 | `n2/BE_two_summand_certificate/` | `tensor_certificate.py check` and independent `independent_integer_check.py`; all 70 rational shards |
| n3 | `n3/BE_three_summand_certificate/` | initial polynomial-identity audit; `verify.py` freshly compiles `check_cube.cpp`, then checks all 111 rational shards |
| ROOT4 | `n4/research/all_n/n4_cpu_time_entire_root_2026_10_09.py` | fresh `--produce`, followed by independently fresh `--replay-existing` |
| Analytic identities | `structural/checks/` and three n4 analytic companions | exact identities/constants only, not verification of uniform analytic proofs |

The 79-file n4 source/provenance closure includes frozen older versions and
three proof notes required by its integrity checks. Their presence is not
permission to call old numerical producers. `-B -S` and a new nonexistent
`pycache_prefix` are used for standard-library stages; `-S` is omitted only for
the explicitly SymPy-dependent scalar checks. Optional NumPy imports in two
historical diagnostic modules take their absent-library fallback under `-S`;
NumPy and numerical discovery are not acceptance dependencies.

Candidate construction is separate and untrusted. The n2 module's optional
`generate` command uses SciPy; it is never invoked here. The retained dependent
n3 obstruction is a limitation of a moment relaxation, not an iid
counterexample. The supplied n2/n3 rational candidate data are necessary inputs
to exact verification. The optional construction/algebra files are retained as
source, but verification does not trust their discovery scores.

## Freshness and resource boundary

Full/scalar runs create a new private source tree below the catalog's gitignored
`moment-defects/work/` directory, not the system temporary folder. Tiny launcher
fixtures use a new private directory there too. No existing checkout receipt or
historic output is copied. For ROOT4, the first complete receipt is
new output; the second pass rebuilds all 1,300 own-request HIGH slots, the cache,
and all 260 complete parent portfolios before comparing every nonresource byte
and final EOF. Only its **top-level** `resources` object is omitted by the frozen
comparator. Every complete UNKNOWN remains represented; the runner rejects a
claimed target result unless all 260 are closed, all required geometry/H/eta
scopes are complete, and the genuine full ROOT upper is at most 4097/10000.
Checkpoints are output/evidence, never resume authority or mathematical inputs.

Stages are serial. The launcher uses two available-RAM readings of at least
1536 MiB, five seconds apart, and a 768 MiB host floor. The runner itself is
limited to a guarded 64 MiB peak RSS. On Windows, children start suspended,
enter an owned kill-on-close Job Object before user code runs, and only their
startup thread is resumed. Job private-memory limits and sampled sums of active
process peak working sets cover nested compiler/kernel processes as well.
These are enforced limits, not an exhaustive measurement/fit proof.

ROOT4 retains 256 MiB whole-process / 64 MiB HIGH limits, 60 CPU-second short
stages, 180 CPU-second A1/Gamma phases, 600 CPU-second optimized joins, and
43,200 CPU seconds per fresh full pass. The outer launcher adds whole-job CPU
accounting including startup/imports. Other finite stages have a 512 MiB owned
job ceiling; scalar stages have 256 MiB. Pipe diagnostics are bounded by 16 MiB,
private source/output/checkpoint files by 256 MiB, with a 4 GiB disk-free floor.
Any source, resource, terminal, pipe or prefix failure is fatal; it is not a
numerical UNKNOWN or successful reproduction. Private working evidence is retained
on success and failure; the runner does not delete old files.

## Mathematical trust boundary

The finite programs verify inequalities over their entire declared continuous
domains, not sampled scores. They do not formally verify compactness,
variation, probability or uniform-asymptotic arguments. The manuscript's written
analytic reductions and explicitly cited literature remain premises.

ROOT4 itself proves a conditional bound for arbitrary standardized original iid
laws in its whole physical class, including bounded infinite supports, zero
atoms, both reflected laws, closed shared faces and tails. The unrestricted
conclusion `C4 <= 0.4097 < C_E` additionally uses the all-law n3 result, the
written attainment/contact/support reduction, published iid Shevtsova bound,
and applicable closed-CDF Prawitz/physical bridge. The three analytic companion
scripts recheck finite identities/constants; their test output is not an actual
ROOT or unrestricted n4 certificate. The n4 old receipt need not be published:
all numerical ROOT evidence can be regenerated from the frozen code in two new
passes. This catalog makes no claim about the remaining indices or the complete
new manuscript's cutoff proof packages.

`code/SHA256SUMS.json` binds exact raw bytes, not mathematical truth. Git must
preserve these frozen files without newline normalization; the parent catalog's
`.gitattributes` supplies that policy. Keep the original file names and the
`research/all_n` ancestor layout when copying the n4 closure.
# Release-test scope, 12 October 2026

All 277 frozen input-file hashes were checked. The cutoff-31 capsule passed
its separate complete byte-identity check. The new finite-index runner has
been source-audited; its first `--tiny` invocation declined to launch because
the host did not have the required two available-memory readings. That is a
resource-gate rejection, not a successful launcher fixture or arithmetic
replay. A second invocation, after sufficient headroom was available, passed
all 277 source identities and the owned bounded launcher fixture with a clean
exit. This establishes that small fixture only, not mathematics or a VM test.
No fresh end-to-end `--full` run is claimed for this publication copy.

