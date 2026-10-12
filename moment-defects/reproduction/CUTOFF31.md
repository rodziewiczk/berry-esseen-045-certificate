# Cutoff 31: source closure and replay

The pinned final record is
`continuation_20261010/repair31/EVENTUAL_CUTOFF31_COMPOSED.json`, SHA-256
`33c73b3bd4c8cb25cedb6c9c8ce3768608db18f1f65932a0fcd6bb468c2b51b9`.
The 9,518 source/data commitments in that record and the record itself are
packaged without rewriting their contents. The package includes zero-byte
files and preserves the original relative hierarchy. Everything outside this
transitive closure, including later unfinished cutoff-25 research, is omitted.

## Three different checks

1. `closure31.py` checks the pinned manifest, part hashes, whole ZIP, final
   record, every member SHA and exact membership. It imports no proof code.
   `PASS_FILE_IDENTITIES` is **not** a theorem or leaf-arithmetic acceptance.
2. Original `--preflight` commands check recorded source closures and complete
   scalar compositions. They do not recompute the large count forests.
3. An arithmetic acceptor reconstructs its closed tree and recomputes every
   leaf. It verifies one explicitly scoped component; global completion still
   requires all same-law acquisition interfaces and the full union.

After extracting to a new directory, run the following **from that directory**:

```sh
python3 -B continuation_20261010/repair31/compose_sharp31_34.py --preflight
python3 -B continuation_20261010/repair31/compose_eventual31.py --preflight
python3 -B BE_cutoff35_release_20261007/verify_release.py
```

The third command checks the sealed release inventory, composition and four
actual resource interfaces. It does not rerun its large arithmetic loops.
Do not add new files inside that sealed release: its verifier checks the exact
inventory. Place newly captured logs outside it. Ordinary Python >=3.11 and
the standard library suffice for the documented sealed check; full historical
arithmetic has not been given a new platform/runtime-fit guarantee.

## A genuine count replay

An example is the selected B5 probability panel 21. Preserve the extracted
original. Make a disposable copy of the source hierarchy, remove **only the
generated report** `accepted_strict_21.json` in that disposable copy, and from
`threshold31_20261008/audit/highrho_counts31/b5` run:

```sh
python3 -B accept_strict.py 21
```

This acceptor reconstructs every count root and split, recomputes every leaf,
and performs malformed-object controls. It is not a construction-only command
or a hash check. Replaying all selected forests, support/INITIAL/resource
steps and their compositions requires their separate frozen component
entrypoints and fresh receipts. The supplied files expose those entrypoints;
there is no already tested one-command full-DAG replay.

Do not run default composers indiscriminately on a completed sealed tree:
they require exclusive fresh output files. In particular
`check_eventual31_assembly.py` expects an earlier incomplete state and is not
a final-reproduction command. Historic absolute executable paths in logs are
labels, not paths to install locally. Use the current Python executable and
preserve the relative source hierarchy.

Use a fresh extraction directory. `-B` prevents cache writes, not cache reads;
the new finite-index runner additionally uses private nonexistent cache
prefixes. Do not run concurrent heavy proof jobs. All mathematical assertions
retain the analytic and published-input scope recorded by their components.
The historical source map and unavailable-log limitations are recorded, not
discharged by changing a filename, timestamp or hash.
