"""Prepare a NEW CONDITIONAL B3/p31 or p32 V14 source epoch; no leaf evaluation.

This is a source preparer, not forest discovery, acceptance, acquisition, or an
all-index proof. Historical native identities are never reused for new code.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from fractions import Fraction as F
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
MIB = 1024**2
DESIGNS = {
    31: '971204850bbb25e7444d4e9069e32b688aa20e238687da118cfdda9bf1d32d6f',
    32: '39de43416357a20bb63b54cd337855a8b429362c1a250dd07b34c1d37339703e',
}
HELPER_PREFIX = 'cutoff25_20261013/b5/local_contact_v14_combined/'
HELPER_MANIFEST = 'LOCAL_CONTACT_V14_ADDITIONS.json'
HELPER_MANIFEST_SHA = 'ba80569735e7042a588eba6c8219fbd68c4deae354c3983ea518dbbb2d9a8336'
ANALYTIC_INPUTS = {
    'ATTAINMENT_AND_GLOBAL25_DAG_PROOF.txt': (
        'cutoff25_20261013/low/global25_composition_audit_v1/PROOF.txt',
        'a62cc3571e216d7d812de4fd64637d960494bad20686260af6109f7630d9f76d'),
    'POSITIVE_CLOSED_DELETION_DERIVATION.txt': (
        'cutoff25_20261013/archive_audit/independent_contact_positive_v1/DERIVATION.txt',
        '3076cfe6dfe5dab63144bdef054db30c4c2f911a69e2aef3b20aa78fd2fb5de7'),
    'INDEPENDENT_LOCAL_CONTACT_PROOF.txt': (
        'cutoff25_20261013/archive_audit/local_contact_independent_v1/PROOF.txt',
        'd8aa091f0756848145dde55aa64406f6a830f7c048cf5e6a43f09453a00adb39'),
    'INDEPENDENT_FINITE_FEEDBACK_PROOF.txt': (
        'cutoff25_20261013/b5/coupled_contact_feedback_review_v1/PROOF.txt',
        'ee85e36ec51158ec241a610c286a9ffbc1d2c29108c349417cc6e654bb8a3c78'),
}
PREMISE = {
    'schema': 'ATTAINED_POSITIVE_CLOSED_CONTACT_V1', 'sample_size': 25,
    'same_unrestricted_attained_witness': True, 'positive_closed_threshold': True,
    'score_at_least_CE': True,
}
RUNTIME_HELPERS = {
    'local_contact_v14.py', 'local_contact_outer_v14.py',
    'local_rho_upper_v14.py', 'local_contact_v13.py', 'local_contact_support.py',
    'local_contact_gaussian.py', 'local_contact_scale.py',
    'local_contact_binomial.py', 'local_contact_heat.py',
}

PORT_PROOF = r'''NEW CONDITIONAL B3/PANEL{index} COMBINED-V14 SOURCE EPOCH
22 October 2026. No finite region or arithmetic acceptance is asserted.

Conditional theorem. Fix the SAME unrestricted attained positive-closed n=25
maximizer P with score C=C25>=CE. Assume the original B3 all-probability INITIAL
and resource implications have been correctly acquired for this P, and assume
the retained published/contact/count framework. Restrict its parameters to
the original closed p panel and rho in [13/10,7/5]. A complete fresh forest
accepted by this new protocol excludes that witness on this original panel.
This is not a uniform estimate for arbitrary P or a restricted optimizer.

1. Discharge of the extra contact hypothesis, not merely a metadata gate.
The bound ATTAINMENT_AND_GLOBAL25_DAG_PROOF.txt, section1, derives fixed-index
unrestricted attainment by tightness, uniform integrability of second moments,
closed-set Portmanteau, and lower semicontinuity of the third moment. It does
not assume third-moment uniform integrability. The copied original B3 INITIAL
and STRONGER24 objects are explicit historical premises; they were NOT replayed
by this preparer. Under their global conclusion C24<CE+1/80, the same law has
25(C24(P)-C25)_+ <=25/80=5/16. The independent positive-closed deletion
derivation obtains, on the whole closed support,
  0 <= G25(H,y)+C[-|y|^3+3*rho*y^2/2+3*beta*y+rho*e]+rho*S*q,
where S=sqrt(25/24), e=25(S-1)-1/2, beta=E[X|X|], q=5/16. The predecessor
CDF coefficient is positive on BOTH support rays, so no reflected-law
predecessor or regionwise-to-global substitution is made. Contamination of
the raw law at a fixed closed event, followed by centering/scaling, gives the
derivative; integrating against P makes it zero almost surely, and upper
semicontinuity extends equality to the full closed support. Thus the two new
contract fields express actual CONDITIONAL hypotheses with a stated source
edge; setting those fields does not establish their premises computationally.

2. Exact unchanged original resource interface.
ORIGINAL_V12_CONTRACT.json is copied byte-for-byte from the pinned original
design. The new contract is EXACTLY that dictionary with ONLY the allowance
and attained-contact dictionary inserted into its one row. The new native
load function checks this entire dictionary equality. In particular D,d0,
Lambda, every affine/quadratic price, acquired beta/mean/theta, support and
endpoint guards are unchanged. PARENT_RESOURCE_* files bind the WHOLE B3
100-panel proof, receipt, source closure, and its WHOLE INITIAL predecessor.
The original prepare_global_theta_count_v2.py is retained: upper quantities
are rounded outward upward, prices downward, signed intervals outward, and
positive physical endpoint floors downward, without replacing the joint
Lambda intercept. The original mathematical resource/count lemmas remain
conditional dependencies, not consequences of source hashes.

Historical documentation caveat: the original resource GLOBAL_RESOURCE_PROOF
text has a B4 heading/profile despite residing in the B3 source closure. Its
bytes are preserved, NOT used as a stand-alone B3 warrant. The actual B3
BRANCH_SCOPE, resources_b3.PROFILE, original INITIAL profile and the resource
proof all explicitly use n25,rho[13/10,7/5],q5/16. This epoch assumes the
correctly acquired B3 resource theorem; it does not repair or waive any
upstream analytic or fresh-arithmetic obligation.

3. Necessary local state from the ORIGINAL closed count box.
Write v=p(1-p), s=lambda/25. Its raw threshold and signed second moment are
  H=(k+u-25p)/sqrt(v+s),
  beta=[v(1-2p)+s(2alpha-1)]/(v+s).
Outward rational interval arithmetic, then intersection with the original
acquired H and beta, gives necessary enclosures. These enclosures are computed
once from the ORIGINAL box and retained through all finite feedback stages.
No new cap is a premise of its own derivation. For the negative support ray
G(H,-R)=-G(-H,R): H is negated/reversed and beta contributes -beta_lower.

4. Three finite, acyclic support/moment steps.
Given previously justified support [-Rminus,Rplus], let hplus bound
sqrt(v+lambda/25) on the ORIGINAL box. Then conditional residual support is
  O0<=Rminus*hplus-p_lower, O1<=Rplus*hplus-(1-p_upper).
Intersect with old outer bounds; nonpositive proposals are omitted. The
pointwise nonnegative cubic (Y+O)(Y-EY^2/O)^2 proves the sharp cubic bound
  rho*(v+s)^(3/2) <= v(1-2v)+M*s-Cc*s^2,
  M=(3p+O0)(1-alpha)+(3(1-p)+O1)*alpha,
  Cc=(1-alpha)^2/((1-p)O0)+alpha^2/(p*O1).
The copied SHARP_CUBIC_PROOF and LOCAL_RHO_UPPER_PROOF derive its uniform
original-box version: M uses four corners; Cc uses the larger of the clipped
quadratic minimum and Cauchy lower bound; the concave s polynomial uses its
clipped vertex. Divide only by a positive outward lower denominator, round
the ratio UP, and intersect the preceding rho cap. A contradiction is STRICT
upper_rho<original_rho_lower; equality is retained. Using original H/beta and
this newly justified rho, every smaller radius has its own strict Gaussian
boundary estimate plus all six strict full-ray derivative gates. Failed
candidate radii license nothing. At most three such steps use ordinary finite
induction, not a simultaneous fixed point or a convergence claim.

5. Canonical fresh native evaluation and complete cover.
Only five temporary cfg fields may change inside the byte-identical wrapper:
rho_upper,radius_minus,radius_plus,outer0,outer1. Every final V12 call receives
ALL ORIGINAL p,lambda,alpha,u,a0 coordinates; intermediate contracted boxes
are never substituted. The unchanged V12/outer fallback remains available.
The 71 original native kernel/proof files are byte-identical. Only the native
protocol's evaluator import, explicit premise/interface check, and clearly
NEW schema/status identity differ. The original evaluate/replay/first
functions and all24 native corruption controls are syntactically unchanged.
There are exactly26 ordered count roots k=0..25, each the original five-
dimensional box; every split retains both CLOSED children with a strict
interior rational cut. Original limits10000nodes/depth128 and STRICT
score_upper<CE_LO are unchanged. Saved leaf arithmetic is never accepted:
native accept reconstructs every leaf from its root and recomputes its full
canonical result. New V14 output MUST NOT be mislabeled with historical V14
or V12 identities, nor may old V12 leaf payloads be treated as new results.

6. Execution boundary.
This source preparation checked only bytes, source transforms, import/load,
premise rejection, and original-root geometry. NO mathematical cell, resource
acquisition, ray, count forest, or native accept was run. It creates no accepted
receipt. Fresh discovery, complete native acceptance, correctly acquired
whole-parent resources, and a new same-witness regional join are still
required. The attained-contact theorem permits both B3 and B5 (the copied
LOCAL_CONTACT_PROOF section7), but no arithmetic completeness follows from
that theorem alone. All source/archive member hashes are in the new source
epoch and premise manifest, and all these documents are loader-bound.
'''


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    value = {}
    for key, item in pairs:
        need(key not in value, 'Duplicate JSON key')
        value[key] = item
    return value


def parsed(data):
    return json.loads(data, object_pairs_hook=unique)


def read_member(archive, name, expected=None, max_bytes=16*MIB):
    need(archive.namelist().count(name) == 1, 'Unique archive member: ' + name)
    info = archive.getinfo(name)
    need(not info.is_dir() and info.file_size <= max_bytes and
         (info.external_attr >> 16) & 0o170000 != 0o120000,
         'Bounded regular archive member: ' + name)
    data = archive.read(info)
    if expected is not None:
        need(sha(data) == expected, 'Exact pinned archive member: ' + name)
    return data


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode('utf-8')


def replace_once(source, old, new):
    need(source.count(old) == 1, 'Unique reviewed literal source transform: ' + old[:60])
    return source.replace(old, new)


def derive_protocol(original, index):
    source = original.decode('utf-8')
    result = replace_once(source, 'from rho_signed_moment_tightener import cell35',
                          'from local_contact_v14 import cell35\n'
                          'from local_contact_support import validate_premise')
    guard = "\n original=json.loads((HERE/'ORIGINAL_V12_CONTRACT.json').read_text(),object_pairs_hook=unique)"
    guard += "\n expected=deepcopy(original['rows'][0])"
    guard += "\n expected.update(local_contact_allowance='5/16',local_contact_premise=" + repr(PREMISE) + ')'
    guard += "\n need(same(contract,dict(original,rows=[expected])),'exact original B3 row plus explicit contact hypotheses')"
    guard += '\n validate_premise(cfg)'
    result = replace_once(result, " cfg=contract['rows'][0]", " cfg=contract['rows'][0]" + guard)
    old_schema = f'LOW25_B3_GLOBAL_ALPHA_STOPLOSS2_V12_PANEL{index}_RIGHT_HALF_CLOSED_COUNT_FOREST_V1'
    new_schema = f'NEW_CONDITIONAL_B3_V14_EPOCH_20261022_PANEL{index}_FULL_ROOTS_V1'
    result = replace_once(result, old_schema, new_schema)
    old_status = f'PASS_FRESH_CONDITIONAL_EXACT_COUNT{index}'
    new_status = f'PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT{index}'
    result = replace_once(result, old_status, new_status)
    before, after = ast.parse(source), ast.parse(result)
    functions = lambda tree: {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    a, b = functions(before), functions(after)
    for name in ('rootbox', 'children', 'evaluate', 'replay', 'first', 'construct'):
        need(ast.dump(a[name]) == ast.dump(b[name]), 'Unchanged native function: ' + name)
    for node in ast.walk(a['accept']):
        if isinstance(node, ast.Constant) and node.value == old_status:
            node.value = new_status
    need(ast.dump(a['accept']) == ast.dump(b['accept']),
         'Native accept changes ONLY its honest result identity')
    controls = [node.value for node in ast.walk(b['accept']) if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'mutations' for t in node.targets)]
    need(len(controls) == 1 and isinstance(controls[0], ast.List) and
         len(controls[0].elts) == 24, 'All24 unchanged native mutation controls')
    need("LIMIT=10000" in result and "depth<=128" in result and
         "F(z['score_upper'])<CE_LO" in result, 'Unchanged limits and strict target')
    return result.encode('utf-8'), new_schema, new_status


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--old-archive', type=Path, required=True)
    p.add_argument('--base13-archive', type=Path, required=True)
    p.add_argument('--index', type=int, choices=(31, 32), required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    need(__debug__ and not sys.flags.optimize, 'Ordinary non-optimized runtime')
    out = args.output.resolve()
    need(not out.exists(), 'Exclusive new conditional source epoch directory')
    payload, provenance = {}, {}

    def add(dest, data, archive_name=None, member=None, purpose=None):
        need(Path(dest).name == dest and '/' not in dest and '\\' not in dest,
             'Flat bounded epoch filename')
        need(dest not in payload and len(data) <= 16*MIB, 'Unique bounded output file')
        payload[dest] = data
        provenance[dest] = dict(archive=archive_name, member=member, sha256=sha(data),
                                bytes=len(data), purpose=purpose)

    def copy_member(archive, member, dest=None, expected=None, purpose=None):
        data = read_member(archive, member, expected)
        add(dest or Path(member).name, data, Path(archive.filename).name, member, purpose)
        return data

    with zipfile.ZipFile(args.old_archive) as old, zipfile.ZipFile(args.base13_archive) as base13:
        pre = f'cutoff25_20261011/new_root/global_alpha_stoploss2_b3_p{args.index}_v12/'
        design_raw = read_member(old, pre+'FROZEN_DESIGN.json', DESIGNS[args.index])
        old_design = parsed(design_raw)
        need(type(old_design.get('files')) is dict and len(old_design['files']) == 76,
             'Complete original76-file source design')
        original = {name: read_member(old, pre+name, pin)
                    for name, pin in old_design['files'].items()}
        for name, data in original.items():
            if name not in ('count_protocol.py', 'contract.json', 'KERNEL_COPY_MANIFEST.json'):
                add(name, data, Path(old.filename).name, pre+name, 'UNCHANGED_ORIGINAL_V12_SOURCE')
        for name in ('count_protocol.py', 'contract.json', 'KERNEL_COPY_MANIFEST.json'):
            add('ORIGINAL_V12_'+name, original[name], Path(old.filename).name, pre+name,
                'UNCHANGED_ORIGINAL_REFERENCE_NOT_NEW_IDENTITY')
        add('ORIGINAL_V12_FROZEN_DESIGN.json', design_raw, Path(old.filename).name,
            pre+'FROZEN_DESIGN.json', 'PINNED_ORIGINAL76_FILE_DESIGN')
        contract = parsed(original['contract.json'])
        need(len(contract['rows']) == 1 and contract['rows'][0]['index'] == args.index and
             contract['rows'][0]['n'] == 25, 'Literal original B3 panel')
        old_row = deepcopy(contract['rows'][0])
        contract['rows'][0].update(local_contact_allowance='5/16', local_contact_premise=deepcopy(PREMISE))
        need(set(contract['rows'][0])-set(old_row) ==
             {'local_contact_allowance', 'local_contact_premise'}, 'Exactly two new conditional fields')
        protocol, schema, status = derive_protocol(original['count_protocol.py'], args.index)
        add('count_protocol.py', protocol, purpose='NEW_REVIEWED_LITERAL_PROTOCOL_DERIVATION')
        add('contract.json', dumps(contract), purpose='ORIGINAL_CONTRACT_PLUS_TWO_CONDITIONAL_FIELDS')
        helpers_raw = read_member(base13, HELPER_PREFIX+HELPER_MANIFEST, HELPER_MANIFEST_SHA)
        helpers = parsed(helpers_raw)
        need(len(helpers['files']) == 21 and
             {n for n in helpers['files'] if n.endswith('.py')} == RUNTIME_HELPERS,
             'All9 unchanged runtime helpers and21 frozen additions')
        for name, pin in helpers['files'].items():
            copy_member(base13, HELPER_PREFIX+name, expected=pin,
                        purpose='BYTE_IDENTICAL_REVIEWED_COMBINED_V14_ADDITION')
        add(HELPER_MANIFEST, helpers_raw, Path(base13.filename).name,
            HELPER_PREFIX+HELPER_MANIFEST, 'EXTERNALLY_PINNED21_FILE_MANIFEST')
        for name, (member, pin) in ANALYTIC_INPUTS.items():
            copy_member(base13, member, name, pin, 'CONDITIONAL_ANALYTIC_PREMISE_WITH_WRITTEN_DERIVATION')

        resource_pre = 'cutoff25_20261011/new_root/resource25_b3_v1/'
        resource_pin = parsed(original['contract.json'])['source_inputs_sha256']
        proof_member = resource_pre+'RESOURCE_B3_GLOBAL_PROOF.json'
        proof_pin = resource_pin['work/cutoff25_20261011/new_root/resource25_b3_v1/RESOURCE_B3_GLOBAL_PROOF.json']
        proof_raw = copy_member(old, proof_member, 'PARENT_RESOURCE_PROOF.json', proof_pin,
                                'WHOLE100_PANEL_B3_RESOURCE_CANDIDATE_NOT_REPLAYED_HERE')
        resource = parsed(proof_raw)
        need(len(resource['rows']) == 100 and
             all(type(r['index']) is int and r['index'] == i for i, r in enumerate(resource['rows'])),
             'Whole ordered100-panel resource source')
        need(resource['rows'][args.index]['result']['excluded'] is False,
             'Original panel survives resource acquisition')
        for name, pin in resource['source_sha256'].items():
            copy_member(old, resource_pre+name, 'PARENT_RESOURCE_'+name, pin,
                        'ORIGINAL_WHOLE_PARENT_RESOURCE_SOURCE_AND_PROOF')
        copy_member(old, resource_pre+'RESOURCE_B3_GLOBAL_ACCEPTED.json',
                    'PARENT_RESOURCE_ACCEPTED_HISTORICAL.json',
                    resource_pin['work/cutoff25_20261011/new_root/resource25_b3_v1/RESOURCE_B3_GLOBAL_ACCEPTED.json'],
                    'HISTORICAL_PARENT_RECEIPT_NOT_NEW_ACCEPTANCE')
        initial_pre = 'cutoff25_20261011/new_root/initial25_b3_exact_v1/'
        for name, pin in resource['parent_source_sha256'].items():
            copy_member(old, initial_pre+name, 'PARENT_INITIAL_'+name, pin,
                        'WHOLE_INITIAL_SOURCE_AND_GLOBAL_AUXILIARY24_PREMISE')
        for name, pin in [('FROZEN_SOURCES.json', resource['parent_manifest_sha256']),
                          ('INITIAL25_B3_PROOF.json', resource['parent_proof_sha256']),
                          ('INITIAL25_B3_ACCEPTED.json', resource['parent_acceptance_sha256'])]:
            copy_member(old, initial_pre+name, 'PARENT_INITIAL_'+name, pin,
                        'WHOLE_INITIAL_HISTORICAL_INPUT_NOT_FRESH_REPLAY')
        prepname = 'cutoff25_20261011/new_root/prepare_global_theta_count_v2.py'
        copy_member(old, prepname, 'ORIGINAL_GLOBAL_RESOURCE_TO_COUNT_INTERFACE.py',
                    resource_pin['work/cutoff25_20261011/new_root/prepare_global_theta_count_v2.py'],
                    'EXACT_ORIGINAL_RESOURCE_INTERFACE_AND_OUTWARD_ROUNDING')

    add('RECONSTRUCTED_B3_V14_PROOF.txt', PORT_PROOF.format(index=args.index).encode('utf-8'),
        purpose='NEW_CONDITIONAL_COMPOSITION_PROOF_NOT_NUMERICAL_ACCEPTANCE')
    source_diff = ''.join(difflib.unified_diff(
        original['count_protocol.py'].decode().splitlines(True), protocol.decode().splitlines(True),
        fromfile='ORIGINAL_V12_count_protocol.py', tofile='count_protocol.py'))
    add('NATIVE_PROTOCOL_LITERAL_DIFF.txt', source_diff.encode('utf-8'),
        purpose='EXACT_REVIEWABLE_SOURCE_DIFF')
    source_epoch = dict(schema='NEW_CONDITIONAL_B3_V14_SOURCE_EPOCH_20261022_V1',
                        n=25, index=args.index, native_schema=schema, expected_native_status=status,
                        original_design_sha256=DESIGNS[args.index], helper_manifest_sha256=HELPER_MANIFEST_SHA,
                        preparer_sha256=sha(Path(__file__).read_bytes()), sources=provenance,
                        conditional_hypotheses=['Unrestricted attained positive-closed n25 maximizer of score>=CE',
                            'Global auxiliary C24<CE+1/80, hence q25<=5/16',
                            'Correct complete original B3 INITIAL and100-panel resource acquisition',
                            'Retained published/contact/Fourier/count framework'],
                        arithmetic_accepted=False, native_acceptance_run=False,
                        all_index_conclusion_verified=False)
    # Snapshot provenance before adding its own non-self-referential binding.
    add('B3_V14_SOURCE_EPOCH.json', dumps(source_epoch), purpose='COMPLETE_INPUT_SOURCE_HASHES_AND_CONDITIONAL_SCOPE')
    excluded = {'contract.json', 'count_protocol.py', 'KERNEL_COPY_MANIFEST.json', 'FROZEN_DESIGN.json'}
    manifest = dict(files={name: sha(data) for name, data in payload.items() if name not in excluded},
                    origin='NEW_CONDITIONAL_B3_V14_EPOCH_20261022_NOT_HISTORICAL_NATIVE_IDENTITY',
                    scope='All retained71 V12 kernel files, byte-identical V14 additions, '
                          'written conditional proofs, whole-parent source commitments. '
                          'Source identity does not establish any arithmetic or analytic premise.')
    old_kernel = parsed(original['KERNEL_COPY_MANIFEST.json'])['files']
    need(len(old_kernel) == 71 and all(manifest['files'].get(n) == pin for n, pin in old_kernel.items()),
         'All71 original V12 kernel/proof files byte identical')
    add('KERNEL_COPY_MANIFEST.json', dumps(manifest), purpose='NEW_COMPLETE_SOURCE_CLOSURE_BINDING')
    need(len(payload) <= 256 and sum(map(len, payload.values())) <= 128*MIB,
         'Bounded flat epoch compatible with protected discover_count')
    out.mkdir(parents=True, exist_ok=False)
    for name, data in payload.items():
        with (out/name).open('xb') as stream:
            stream.write(data)
    design = dict(files={name: sha(data) for name, data in payload.items()})
    design_bytes = dumps(design)
    with (out/'FROZEN_DESIGN.json').open('xb') as stream:
        stream.write(design_bytes)
    # Geometry/load tests only: the mathematical evaluator is replaced with an
    # explicit tripwire before any root checks, and is NEVER called here.
    sys.path.insert(0, str(out))
    try:
        spec = importlib.util.spec_from_file_location('new_conditional_b3_v14_protocol', out/'count_protocol.py')
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        cfg, bound = native.load()
        def forbidden(*unused, **kwargs):
            raise AssertionError('No mathematical evaluator may run during source preparation')
        native.evaluate = forbidden
        need(native.LIMIT == 10000 and native.header(bound)['schema'] == schema,
             'Literal original limit and new honest header')
        expected_box = [[F(x) for x in old_row['p']], [F(0), F(old_row['Lambda'])],
                        [F(0), F(1)], [F(-1,2), F(1,2)], [F(0), F(old_row['d0'])]]
        for k in range(26):
            need(native.rootbox(cfg) == expected_box, 'Original full5D count root')
            cut = sum(expected_box[0])/2
            left, right = native.children(expected_box, 0, cut)
            need(left[0][1] == right[0][0] == cut, 'Both closed children and seam')
        for altered in [dict(cfg, local_contact_allowance='0'),
                        dict(cfg, local_contact_premise=dict(PREMISE, sample_size=True))]:
            try:
                native.validate_premise(altered)
            except (ValueError, TypeError):
                pass
            else:
                raise ValueError('Premise rejection fixture unexpectedly passed')
        loaded = {}
        runtime_names = {Path(n).stem for n in old_kernel if n.endswith('.py')} | {Path(n).stem for n in RUNTIME_HELPERS}
        for name in runtime_names:
            module = sys.modules.get(name)
            if module is not None and getattr(module, '__file__', None):
                path = Path(module.__file__).resolve()
                need(path.parent == out, 'Loaded frozen runtime origin: '+name)
                loaded[name] = sha(path.read_bytes())
        need(native.load()[1] == bound, 'Unchanged bound source after smoke tests')
    finally:
        sys.path.pop(0)
    need(all(sha((out/name).read_bytes()) == pin for name, pin in design['files'].items()),
         'All final files remain byte-identical to this NEW design')
    report = dict(scope='UNTESTED_CONDITIONAL_NEW_V14_SOURCE_EPOCH_PREPARED_NO_ARITHMETIC',
                  output=str(out), index=args.index, design_sha256=sha(design_bytes),
                  files=len(design['files']), bytes=sum(map(len, payload.values())),
                  kernel_manifest_sha256=sha(payload['KERNEL_COPY_MANIFEST.json']),
                  protocol_sha256=sha(protocol), contract_sha256=sha(payload['contract.json']),
                  unchanged_native_kernel_files=71, unchanged_runtime_helpers=9,
                  unchanged_v14_addition_files=21, loaded_runtime_origins=loaded,
                  geometry_roots_checked=26, native_corruption_controls_preserved=24,
                  mathematical_evaluator_run=False, native_acceptance_run=False,
                  arithmetic_accepted=False, all_index_conclusion_verified=False,
                  expected_native_status=status,
                  acceptance_cli=[sys.executable, '-B', '-S', str(out/'count_protocol.py'), 'accept'],
                  remaining=['Independent source/analytic-premise review',
                             'Protected complete forest discovery and canonical leaf construction',
                             'Fresh complete native accept', 'Fresh parent arithmetic and new same-witness regional join'])
    with (out/'SOURCE_PREPARATION_REPORT.json').open('xb') as stream:
        stream.write(dumps(report))
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('NEW_CONDITIONAL_V14_PREPARATION_INCOMPLETE_NO_ACCEPTANCE: '+str(exc),
              file=sys.stderr, flush=True)
        raise SystemExit(1)
