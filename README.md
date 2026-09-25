# Berry--Esseen 0.45 Certificate

This repository constructs and then verifies, in a fresh process, the complete interval
certificate accompanying *A Reproducible Route to a 0.45 Berry--Esseen
Bound*. A successful
run covers every integer `n = 2,...,8123` and every
`rho in [1, 712569/589000]`. The public checker prints `ACCEPTED_FULL` only
after it has recomputed every bound with outward-rounded Arb arithmetic.

## Complete verification on Windows

Prerequisites are Docker Desktop with the Linux engine running and the
parameter bank downloaded by Git LFS. From Command Prompt in the repository
root, run:

```cmd
verify.cmd
```

The command builds the pinned verifier image, constructs the compact
certificate bundle, and runs the checker in a fresh process. The computation is
restart-safe: after an interruption, run the same command again. To limit or
increase parallelism, for example:

```cmd
set VERIFY_WORKERS=4
verify.cmd
```

Both phases start at `n=2` and proceed toward `n=8123`. The console reports
each completed `n` through `n=10`, then reports progress at every multiple of
ten. Each message includes the total number of successful `n` values. Any
failed `n` is reported immediately with the corresponding log path.
Construction messages use the largest contiguous completed `n`, so the
display remains ordered even though six workers finish tasks concurrently.

The final lines of a successful run begin with:

```text
ACCEPTED_FULL
```

The certificate and its audit are written to
`artifacts/certificate/`; restart markers and logs are written to
`artifacts/work/`. Exit code zero is returned only after the complete bundle
has been accepted. This is a long-running computation; keep the machine awake
and allow many hours, depending on the processor and worker count.
The publication entry point fixes the archival precision and grid cap; helper
module command-line options are not separate verification interfaces.

## Reproducible container

Docker isolates the formal Python runtime and dependency versions. The base
image, Dockerfile frontend, and Linux wheel files are locked by SHA-256. Git
LFS must have populated `data/parameter_bank` on the host. Build and run with:

```cmd
docker compose run --build --rm verify
```

Set a different worker count through `VERIFY_WORKERS`, if desired:

```cmd
set VERIFY_WORKERS=4
docker compose run --build --rm verify
```

The parameter bank is mounted read-only, while `artifacts/` is persisted on
the host. Repeating the command resumes compatible completed shards and then
performs a fresh complete check. Never start two verification commands against
the same `artifacts/` directory: `verify.cmd` rejects an already-running Compose
verifier, and the launcher also holds an operating-system lock for the full run.

## Proof authority and construction helpers

The audit surface is deliberately separated from search and orchestration:

| Path | Role | Trusted for acceptance |
| --- | --- | --- |
| `proof/berry_core.py` | Arb implementations of the analytic bounds and exact grid decoder | Yes |
| `proof/check_certificate.py` | Strict parser, coverage checks, hash binding, and complete recomputation | Yes |
| Package initializers and `construction/verify.py` | One-shot launch, manifest assembly, and faithful reporting | Yes for execution integrity; not a mathematical premise |
| `construction/generate_certificate.py` | Deterministic recipe selection and shard construction | No |
| `construction/parameter_bank.py` | Parameter-advice loader used only during construction | No |
| `data/parameter_bank/` | A100-generated parameter advice with per-array hashes | No |
| `reproduction/` and `notebooks/` | Deterministic A100 reproduction of the parameter bank | No |

Acceptance does not rely on a floating-point GPU bound. Candidate parameters
are converted to canonical rationals and every selected cell is recomputed by
the checker using `python-flint==0.9.0`. The bundle-v2 manifest binds the
complete shard set to every project source file imported or executed by the
one-shot path and separately records the parameter-bank provenance. This source
binding is an audit aid, not a substitute for authenticating the Git commit or
container image and reviewing the trusted code.

The trusted numerical functions correspond to the manuscript as follows:

| Implementation | Manuscript result |
| --- | --- |
| `stable_B_point` | Lemma 4.1, equation (20) |
| `geom_sum_upper` | Lemma 4.2 |
| `regularized_cot_d_upper_point` | Lemma 4.3, equations (21)--(23) |
| `kernel_L_abs_upper` | Corollary 4.4, equation (25) |
| `rad_gauss_diff_upper` | Lemma 4.5 and Corollary 4.6, equations (26)--(28) |
| `kernel_K_abs_upper` and `endpoint_kernel_shape_upper` | Lemmas 5.1--5.2, equations (29)--(30) |
| `second_endpoint_integral_upper` | Theorem 5.3, equation (31) |
| `second_integral_upper` | Lemma 5.5, equation (32), applied with `s* >= 1/2` |
| `evaluate_cell` | Lemmas 6.1--6.2 and Proposition 6.3, equations (33)--(35) |
| `self_test_global_reductions` | Lemma 2.2 and Appendix A |

The docstrings in `proof/berry_core.py` give the detailed correspondence and
state every domain restriction used by the implementation.

## Manuscript

The publication manuscript is maintained in LaTeX at
`paper/berry_esseen_045.tex`; the typeset reference PDF is
`output/pdf/berry_esseen_045_publication.pdf`. Build instructions and the
strict post-verification finalization procedure are documented in
`paper/README.md`. After the public checker records `ACCEPTED_FULL`, the single
command `paper\finalize.cmd` validates the audit, injects its exact archival
fields, builds the unconditional manuscript, and creates the arXiv source
archive. The manuscript never treats exploratory GPU scores as proof data.

## Certificate format

The output is a streaming bundle rather than one monolithic JSON file:

```text
artifacts/certificate/
|-- manifest.json
|-- verification.json
`-- n/
    |-- 0002.json
    |-- 0003.json
    `-- ...
```

The bundle manifest uses `berry-esseen-045-certificate-bundle-v2`, and each shard uses
`berry-esseen-045-cert-v2`. A cell stores exact rational
parameters and a compact `grid = {pieces, power}` recipe. The checker
reconstructs all three exact rational partitions. `bundle.schema.json` and
`certificate.schema.json` document the serialized structures; the executable
checker remains authoritative and enforces stricter global invariants such as
the exact ordered range and the gap-free rho cover.

## Reproducing the parameter bank on Colab

Parameter-bank construction requires an NVIDIA A100 with compute capability
8.0. Open `notebooks/build_parameter_bank_colab.ipynb` in Google Colab, select
an A100 runtime, and add these Colab secrets:

- `BERRY_ESSEEN_REPOSITORY`: the Git repository URL.
- `BERRY_ESSEEN_REF`: the exact 40-character commit SHA to reproduce.

Choose **Runtime > Run all**. The notebook contains no embedded source or
stored execution output. It installs `requirements-gpu.txt`, invokes
`reproduction.build_parameter_bank`, mirrors checkpoints to Google Drive, and
accepts the result only if the complete bank matches
`data/parameter_bank/manifest.json` byte-for-byte through all recorded array
hashes. The Linux x86-64 CPython 3.12 wheels and their complete Python
dependency closure are pinned by SHA-256 and forcibly reinstalled; the
Colab-provided CUDA runtime must be 12.x, and the exact runtime and driver are
recorded separately. The fixed
profile refines all prescribed depth-6 and depth-7 cells,
uses the committed set of 98,444 depth-8 parents, completes depth 9, and
applies the fixed final refinement schedule.

The verifier and GPU search use separate pinned numerical environments:
`requirements-container.txt` is authoritative for the CPU proof, while
`requirements-gpu.txt` is authoritative for the A100 reproduction. They are
not combined as a Python package extra because CuPy 14 requires NumPy 2,
whereas the archival verifier fixes NumPy 1.26.4.

The equivalent command on an A100 Linux host is:

```bash
python -m reproduction.build_parameter_bank \
  --output-dir ./artifacts/parameter-bank-build \
  --mirror-dir ./artifacts/parameter-bank-mirror
```

The canonical bank contains 886,998 dyadic cells and six candidate recipes per
cell. Its manifest validates file names, dtypes, shapes, byte counts, SHA-256
digests, the complete dyadic tiling, and the final geometry digest.

## Development checks

The unit suite is separate from the full certificate run:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install --requirement requirements.txt
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The repository targets Python 3.12 and uses only pinned runtime dependencies.
Generated certificates, logs, caches, environments, and checkpoints are
excluded from version control. The NPY parameter-bank arrays are managed by
Git LFS.

## Repository layout

```text
proof/           trusted numerical core and complete checker
construction/    deterministic certificate construction and orchestration
reproduction/    fixed A100 parameter-bank builder and CUDA primitives
notebooks/       output-free Colab entry point
data/            canonical hashed parameter bank
paper/           publication LaTeX source and result switch
output/pdf/      rendered publication manuscript
tests/           fast deterministic unit tests
```

License: MIT. Citation metadata are provided in `CITATION.cff`.
