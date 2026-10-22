"""Read source-bound C5 arithmetic artifacts; DO NOT certify their execution.

A hash, a plausible capture, and a PASS string cannot authenticate a past
subprocess. This post-hoc reader checks artifact identities, complete selected
source closures, commands, domains and exact mathematical inequalities only.
Only a separate controller which observes its own guarded subprocesses may
promote these implications to a fresh-parent proof composition.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import stat
import sys

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from .c5_high_one import read, source_at, collect_sources, VARIANTS as HIGH_VARIANTS, HIGH_ROOT
    from .c5_owncaps_one import selected_sources, VARIANTS as OWN_VARIANTS, HIGH, AUX, AUX_PLAN, AUX_REVIEW, EXTENSION
    from .c5_initial_one import canonical_native_sources
    from .c5_inputs import extended, safe_relative
    from .c5_parent_facts import support_facts, high_facts, owncap_facts, GlobalOwncapFact, global_coarse429
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from c5_high_one import read, source_at, collect_sources, VARIANTS as HIGH_VARIANTS, HIGH_ROOT
    from c5_owncaps_one import selected_sources, VARIANTS as OWN_VARIANTS, HIGH, AUX, AUX_PLAN, AUX_REVIEW, EXTENSION
    from c5_initial_one import canonical_native_sources
    from c5_inputs import extended, safe_relative
    from c5_parent_facts import support_facts, high_facts, owncap_facts, GlobalOwncapFact, global_coarse429


EXTRAS = 'work/cutoff5_20261020/entry/delivery_review_v1/EXTRA_SOURCES.json'
EXTRAS_SHA = 'b9bdcdd09b3411f47de91919bb4437362312873c951b9a29715ced6ffc64d00f'
SUPPORT_VARIANTS = (('support_v1','PASS_FRESH_LITERAL5_Q0_SUPPORT9',9),
                    ('support_v2','PASS_FRESH_LITERAL5_Q0_SUPPORT9',9),
                    ('support_A0_v1','PASS_FRESH_LITERAL5_Q0_SUPPORT_A0',1))


def exact_int(value, expected):
    need(type(value) is int and value == expected, 'Literal integer census')


def regular_owned(root, path, *, directory=False):
    """A concrete file/dir within an owned root; reject every reparse component."""
    root, path = Path(root).absolute(), Path(path).absolute()
    need(path.is_relative_to(root), 'Artifact path is inside its declared owned root')
    need(not any(part in ('.','..') for part in path.relative_to(root).parts), 'No lexical artifact path traversal')
    for item in (root, *[root.joinpath(*path.relative_to(root).parts[:i])
                         for i in range(1,len(path.relative_to(root).parts)+1)]):
        info = item.lstat()
        need(not stat.S_ISLNK(info.st_mode)
             and not (getattr(info,'st_file_attributes',0) & 0x400), 'No artifact symlink or reparse point')
    need(path.is_dir() if directory else path.is_file(), 'Regular owned artifact exists')
    need(path.resolve().is_relative_to(root.resolve()), 'Resolved artifact stays contained')
    return path


def checked_json(root, path, pin=None):
    path = regular_owned(root,path)
    need(path.stat().st_size <= 16*1024**2, 'Bounded artifact JSON, never an unbounded archive load')
    before = digest(path)
    need(pin is None or before == pin, 'Exact artifact identity')
    result = read(path)
    need(digest(path) == before, 'Artifact unchanged while reading')
    return result


def verify_graph(root, pins):
    normalized = canonical_native_sources(pins)
    for name,pin in normalized.items():
        need(digest(regular_owned(root,Path(root).joinpath(*safe_relative(name)))) == pin,
             'Every native artifact/source commitment still holds: '+name)
    return normalized


def verify_capture(epoch, capture, directory, command_tail, *, workspace_inputs=False,
                   metadata_pin=None, result=None):
    """Verify recorded bytes/command, NOT that the claimed command was executed."""
    capture = regular_owned(epoch,capture,directory=True)
    directory = regular_owned(epoch,directory,directory=True)
    metadata = checked_json(epoch,capture/'metadata.json',metadata_pin)
    need(metadata['command'] == [sys.executable,*command_tail], 'Exact recorded native invocation')
    need(Path(metadata['cwd']).resolve() == directory.resolve(), 'Actual private epoch cwd, not a historical cwd')
    exact_int(metadata['returncode'],0)
    for name in ('stdout','stderr'):
        path = regular_owned(epoch,capture/(name+'.txt'))
        need(digest(path) == metadata[name+'_sha256'], 'Exact recorded '+name+' bytes')
        need(path.stat().st_size <= 16*1024**2, 'Bounded recorded output')
    need((capture/'stderr.txt').stat().st_size == 0, 'Native successful stage has empty stderr')
    first,last = [datetime.fromisoformat(metadata[key]) for key in ('started_utc','finished_utc')]
    need(first.tzinfo is not None and last.tzinfo is not None and first <= last, 'Ordered timezone-aware capture times')
    need(type(metadata['elapsed_seconds']) in (int,float) and metadata['elapsed_seconds'] >= 0,
         'Typed nonnegative recorded elapsed time')
    pins = canonical_native_sources(metadata['input_sha256'])
    for name,pin in pins.items():
        if not workspace_inputs:
            need(len(safe_relative(name)) == 1, 'Original local captured input name')
        path = (Path(epoch) if workspace_inputs else directory).joinpath(*safe_relative(name))
        need(digest(regular_owned(epoch,path)) == pin, 'Recorded native input bytes')
    if result is not None:
        need(metadata.get('native_result_sha256',metadata.get('RESULT.json_sha256')) == digest(result),
             'Capture is bound to its exact numerical result')
    return dict(path=str(capture/'metadata.json'),sha256=digest(capture/'metadata.json'),
                scope='RECORDED_BYTES_AND_COMMAND_ONLY_NOT_EXECUTION_AUTHENTICATION')


def report_epoch(report_path, filename, work_root):
    report_path = regular_owned(work_root,report_path)
    need(report_path.name == filename and report_path.parent.parent.resolve() == Path(work_root).resolve(),
         'One report at the root of an exclusive private epoch')
    return report_path.parent


def validate_wrapper(report, scope, status):
    need(report.get('scope') == scope and report.get('status') == status,
         'Exact current adapter report, not an archived native PASS')
    need(report.get('original_final_graph_sha256') == FINAL_SHA and report.get('fresh_arithmetic') is True
         and report.get('all_index_conclusion_verified') is False, 'Explicit bounded arithmetic-only wrapper scope')


@dataclass(frozen=True)
class ParentEvidence:
    facts: tuple
    global_owncap: GlobalOwncapFact
    bindings: tuple
    captures: tuple

    def declaration(self):
        return dict(scope='SOURCE_BOUND_PARENT_ARTIFACT_EVIDENCE_ONLY',reports=list(self.bindings),
                    captures=list(self.captures),execution_observed_by_this_reader=False,
                    fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)


def load_parent_evidence(cache, support_report, high_report, owncaps_report, *, work_root=None):
    """Check selected source/artifact bindings and extract exact implication facts."""
    work_root = Path(work_root) if work_root is not None else BASE/'work'
    cache = extended(Path(cache))
    need(digest(source_at(cache,FINAL)) == FINAL_SHA, 'Immutable original final source graph')
    graph = read(source_at(cache,FINAL))['files_sha256']
    need(len(graph) == 16576, 'Complete original selected graph identity')
    facts,bindings,captures = [],[],[]

    epoch = report_epoch(support_report,'FRESH_SUPPORT_RESULT.json',work_root)
    report = checked_json(epoch,support_report)
    validate_wrapper(report,'C5_SUPPORT_ARITHMETIC_CONDITIONAL_ON_ORIGINAL_ANALYTIC_AND_C4_PREMISES',
                     'FRESH_SUPPORT_PROTOCOLS_ACCEPTED')
    need(digest(source_at(cache,EXTRAS)) == EXTRAS_SHA, 'Original omitted-import supplement')
    support_graph = dict(graph)
    support_graph.update({FINAL:FINAL_SHA,EXTRAS:EXTRAS_SHA})
    for row in read(source_at(cache,EXTRAS))['files']:
        need(row['path'] not in support_graph or support_graph[row['path']] == row['sha256'],
             'Consistent supplemental source binding')
        support_graph[row['path']] = row['sha256']
    receipts = report['receipts']
    need(type(receipts) is list and [r['protocol'] for r in receipts] == [v[0] for v in SUPPORT_VARIANTS],
         'All three original support protocols exactly once')
    for receipt,(variant,status,count) in zip(receipts,SUPPORT_VARIANTS):
        path = epoch/(variant+'-FRESH.json')
        need(Path(receipt['receipt']).resolve() == path.resolve(), 'Exact current support output path')
        native = checked_json(epoch,path,receipt['sha256'])
        need(native['status'] == status and native['action'] == 'replay', 'Original support replay action/status')
        exact_int(receipt['rows'],count);need(len(native['rows']) == count, 'Whole support row inventory')
        pins = canonical_native_sources(native['files_sha256'])
        need(all(support_graph.get(name) == pin for name,pin in pins.items()), 'Support source closure pinned by final graph')
        # The native support sources were run from this immutable cache, not mirrored.
        for name,pin in pins.items():
            need(digest(source_at(cache,name)) == pin, 'Original support input bytes')
        need(pins.get(HIGH_ROOT+variant+'/protocol.py') == graph[HIGH_ROOT+variant+'/protocol.py'],
             'The original support protocol itself is bound')
        output = regular_owned(epoch,epoch/(variant.replace('_','-').lower()+'.stdout.txt'))
        need(output.read_text(encoding='utf-8').splitlines()[-1] == status, 'Recorded guarded support acceptance line')
        facts.extend(support_facts(native,receipt['sha256']))
    bindings.append(dict(kind='support',path=str(support_report),sha256=digest(support_report)))

    epoch = report_epoch(high_report,'FRESH_HIGH_RESULT.json',work_root)
    report = checked_json(epoch,high_report)
    validate_wrapper(report,'C5_HIGH_NATIVE_FRESH_EPOCH_CONDITIONAL_ON_SUPPORT_AND_ANALYTIC_INPUTS',
                     'FRESH_BOTH_NATIVE_HIGH_PROTOCOLS_ACCEPTED')
    need(report.get('historical_captures_rewritten') is False, 'No relocated historical HIGH captures')
    expected = {}
    for variant,*_ in HIGH_VARIANTS:
        expected.update(collect_sources(cache,graph,variant))
    need(report['source_files_sha256'] == expected, 'Exact selected HIGH runtime closure')
    verify_graph(epoch,expected)
    receipts = report['receipts']
    need([r['variant'] for r in receipts] == [v[0] for v in HIGH_VARIANTS], 'Both original HIGH variants exactly once')
    for receipt,(variant,prefix,status,count,controls) in zip(receipts,HIGH_VARIANTS):
        directory = epoch/HIGH_ROOT/variant
        path = directory/'HIGH_CHECKED.json'
        need(Path(receipt['native_receipt']).resolve() == path.resolve(), 'Exact current HIGH receipt')
        native = checked_json(epoch,path,receipt['sha256'])
        need(native['status'] == status and len(native['rows']) == count, 'Full original HIGH result')
        exact_int(receipt['rows'],count);exact_int(receipt['negative_controls'],controls)
        need(len(native['negative_controls']) == controls, 'All HIGH negative controls')
        verify_graph(epoch,native['files_sha256'])
        for action,output in (('construct','CONSTRUCTED.json'),('replay','REPLAY.json')):
            capture = epoch/'runs/cutoff5_20261020/high'/(prefix+'_'+action+'01')
            captures.append(verify_capture(epoch,capture,directory,['-B','bound.py',output]))
        need(digest(directory/'CONSTRUCTED.json') == digest(directory/'REPLAY.json'), 'Complete HIGH construct/replay equality')
        facts.extend(high_facts(native,receipt['sha256']))
    bindings.append(dict(kind='HIGH',path=str(high_report),sha256=digest(high_report)))

    epoch = report_epoch(owncaps_report,'FRESH_OWNCAPS_RESULT.json',work_root)
    report = checked_json(epoch,owncaps_report)
    validate_wrapper(report,'C5_COARSE_AND_SELECTED_OWNCAPS_CONDITIONAL_ON_EXPLICIT_ANALYTIC_AND_SUPPORT_INPUTS',
                     'FRESH_COARSE_AND_SELECTED_OWNCAPS_ACCEPTED')
    need(report.get('historical_captures_rewritten') is False, 'No relocated historical owncap captures')
    expected = selected_sources(cache,graph)
    need(report['source_files_sha256'] == expected, 'Exact selected owncap/coarse runtime closure')
    verify_graph(epoch,expected)
    extension = epoch/EXTENSION/'FOURIER_CHECKED.json'
    need(Path(report['fresh_fourier_extension_review']).resolve() == extension.resolve(), 'Actual new Fourier-review destination')
    review = checked_json(epoch,extension)
    need(review.get('status') == 'PASS_INDEPENDENT_COTANGENT_AND_STABLE_RANGE_EXTENSION'
         and type(review.get('cotangent_comparisons')) is int and review['cotangent_comparisons'] == 25
         and len(review['negative_controls']) == 3, 'Complete selected Fourier-subproof artifact')
    verify_graph(epoch,review['files_sha256'])
    worker = regular_owned(epoch,epoch/'c5_extension_worker.py')
    need(digest(worker) == report['fourier_subproof_adapter_sha256']
         and digest(worker) == digest(Path(__file__).with_name(worker.name)), 'Exact published Fourier-only adapter')
    coarse = report['coarse_429']
    coarse_path = epoch/AUX_REVIEW/'RESULT.json'
    need(Path(coarse['native_receipt']).resolve() == coarse_path.resolve(), 'Exact new global-coarse readback')
    native = checked_json(epoch,coarse_path,coarse['sha256'])
    global_fact = GlobalOwncapFact(global_coarse429(native),coarse['sha256'])
    verify_graph(epoch,native['files_sha256'])
    request = checked_json(epoch,epoch/AUX_REVIEW/'FRESH_REQUEST.json')
    for action in ('construct','replay'):
        capture = epoch/'runs/cutoff6_20261018/fourier/auxiliary5_v2'/(action+'01')
        need(request[action+'_capture'] == capture.relative_to(epoch).as_posix(), 'New coarse capture reference')
        captures.append(verify_capture(epoch,capture,epoch/AUX,
            ['-B','protocol.py',action,str(epoch/AUX_PLAN),str(capture/'RESULT.json')],
            workspace_inputs=True,metadata_pin=request[action+'_metadata_sha256'],result=capture/'RESULT.json'))
    receipts = report['receipts']
    need([r['variant'] for r in receipts] == [v[0] for v in OWN_VARIANTS], 'Both selected owncap variants exactly once')
    for receipt,(variant,prefix,status,count) in zip(receipts,OWN_VARIANTS):
        directory = epoch/HIGH/variant;path = directory/'OWNCAPS_CHECKED.json'
        need(Path(receipt['native_receipt']).resolve() == path.resolve(), 'Exact new selected owncap receipt')
        native = checked_json(epoch,path,receipt['sha256'])
        need(native['status'] == status and len(native['bands']) == count, 'All selected owncap bands')
        exact_int(receipt['bands'],count);exact_int(receipt['negative_controls'],10)
        need(len(native['negative_controls']) == 10, 'All selected owncap negative controls')
        verify_graph(epoch,native['files_sha256'])
        for action,output in (('construct','CONSTRUCTED.json'),('replay','REPLAY.json')):
            capture = epoch/'runs/cutoff5_20261020/high'/(prefix+'_'+action+'01')
            captures.append(verify_capture(epoch,capture,directory,['-B','protocol.py',action,'PLAN.json',output]))
        facts.extend(owncap_facts(native,receipt['sha256']))
    bindings.append(dict(kind='owncaps',path=str(owncaps_report),sha256=digest(owncaps_report)))
    return ParentEvidence(tuple(facts),global_fact,tuple(bindings),tuple(captures))
