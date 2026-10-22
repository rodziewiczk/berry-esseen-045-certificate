# Unchanged original cutoff49 suite on Linux

The original `audit/portable_audit_phase_scope.py` binds some paths using
`str(path.relative_to(root))` against a manifest of POSIX paths. The actual
Windows attempt rejected `work\below50_20260929\root\accept_predecessor_score_cap.py`
at that source-binding assertion. Nothing in the original capsule is patched
to bypass it. The separate Linux adapter preserves POSIX path semantics and
executes the same complete original suite.

Run from a **dedicated Linux Docker container**, using Python3.12 directly as
the main child of Docker `--init`:

```console
python -B -S /src/moment-defects/reproduction/uniform_tail/linux49_replay.py --archive /archives/BE_cutoff49_20260930.zip --run
```

Without `--run` it prepares and checks sources only. There is no quick-mode
option and no promotion of preparation, historical captures, unit fixtures,
or an old PASS to fresh native execution.

The host starts the container with `--memory=512m`,
`--memory-swap=512m`, `--cpus=1`, `--pids-limit=128`, `--cgroupns=private`,
`--network=none`, `--init`, `--cap-drop=ALL`, and
`--security-opt=no-new-privileges`. Mount the repository at `/src` read-only,
the source archive directory at `/archives` read-only, and a dedicated empty
work directory at `/src/moment-defects/work` read-write. Create that nested
mountpoint before mounting the repository read-only. Invoke Python directly,
not through an intervening shell. Run with the host work-directory owner's
UID/GID (`--user "$(id -u):$(id -g)"`): after dropping all capabilities, an
unmatched container root cannot override host bind-mount permissions.
No Docker engine or host launch is provided
by this Python adapter; the manual GitHub Actions workflow defines the host
container invocation.

Before numerical entry the controller reads the actual unified cgroup-v2
mount and its own private `0::/` membership. It requires exactly512MiB
`memory.max`, zero `memory.swap.max`, CPU bandwidth at most one CPU, and a
finite process/thread bound at most128. These kernel limits apply to the
**whole container**, including init, controller and all native descendants;
they are not per-process substitutes. It samples actual `cpu.stat` to enforce
7200 aggregate CPU seconds and a7800-second wall budget. Any OOM event,
OOM kill, process-limit exhaustion, counter reset, changed limit or unsupported
environment rejects the run.

Host `MemAvailable` must remain at least1GiB. Before a native launch two
readings five seconds apart must each be at least1536MiB. The entire private
source/output/TMP epoch is checked with the existing stable inventory:
256MiB total files,4GiB free disk,16MiB aggregate native stdout/stderr files,
and no symlink or special-file escape. The wrapper starts in its own process
group and that entire group is unconditionally terminated and reaped on both
success and failure. Before acceptance only Docker init and this controller
may remain in the cgroup. Exiting Docker init's main child also ends the
container PID namespace, including descendants that changed process group.

The native source archive is independently pinned to
`ecdb9acca0db29efc9fe2bf496c0bcc61b4881aecdcbc91a4eb6ad49b920c72e`
(16,660,566 bytes). Preparation reuses the original complete1401-file
manifest. The unchanged `archive49_worker.py` executes unchanged
`verify.py --output NEW_PATH`. Acceptance requires a newly observed successful
subprocess, all14 top-level executions, all41 retained native components,
all captures and commands, unchanged source bindings before and after, and
absence of old bytecode. Kernel and controller-source provenance is retained.

A successful run atomically publishes
`work/<fresh-epoch>/FRESH_BE49_FULL_SUITE_RESULT.json`, beside original native
results in `fresh-full-result/result.json` and
`fresh-full-result/components/metadata.json`. An uncommitted file or nonzero
controller exit is not successful verification. The status remains scoped to
the original **selected full native arithmetic suite**, not verification of
the analytic/literature premises, the cutoff31 composition, or all indices.

Small mocked kernel fixtures (no mathematical producer):

```console
python -B -S -m unittest reproduction.uniform_tail.test_linux_cgroup -q
```

The unit fixtures are not an actual Linux native run or an arithmetic certificate.
