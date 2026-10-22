"""Resumable UNTRUSTED count-forest search; only native replay can accept it.

No arithmetic oracle, root domain, target or native tree limit is changed.
Checkpoints preserve candidate search work, never mathematical acceptance.
Run this worker only through a resource-bounded supervisor.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
SCHEMA = 'UNTRUSTED_COUNT_SEARCH_CHECKPOINT_V1'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024**2):
            h.update(chunk)
    return h.hexdigest()


def census(c, cfg, roots):
    """Validate candidate topology, including all still-pending closed boxes."""
    n = cfg['n']
    need(type(n) is int and n >= 1, 'Literal sample size')
    need(type(roots) is list and len(roots) == n+1, 'Every original count root')
    pending, nodes, leaves = [], 0, 0
    def visit(node, k, box, path):
        nonlocal nodes, leaves
        nodes += 1
        need(nodes <= c.LIMIT and len(path) <= 128, 'Original finite tree limits')
        need(type(node) is dict, 'Candidate node dictionary')
        if node.get('kind') == 'pending':
            need(set(node) == {'kind'}, 'Pending node carries no success claim')
            pending.append((k, path, node, box))
        elif node.get('kind') == 'leaf':
            need(set(node) == {'kind','box','decision','result'}, 'Exact native leaf fields')
            need(c.same(node['box'], c.enc(box)), 'Reconstructed original leaf geometry')
            # Saved decisions/results are deliberately NOT trusted here.
            # The original independent accept process must recompute them all.
            leaves += 1
        else:
            need(node.get('kind') == 'split' and
                 set(node) == {'kind','axis','cut','left','right'}, 'Complete native binary split')
            need(type(node['cut']) is str, 'Exact rational cut text')
            left, right = c.children(box, node['axis'], F(node['cut']))
            visit(node['left'], k, left, path+'L')
            visit(node['right'], k, right, path+'R')
    for k, root in enumerate(roots):
        need(type(root) is dict and set(root) == {'k','tree'} and
             type(root['k']) is int and root['k'] == k, 'Ordered literal count roots')
        visit(root['tree'], k, c.rootbox(cfg), '')
    return pending, nodes, leaves


def split_axis(cfg, box, alpha_priority):
    scales = [F('.001'),F('.006'),F('.15'),F('.02'),F(1)]
    widths = [(box[i][1]-box[i][0])/scales[i] for i in range(5)]
    need(F(cfg['Lambda']) > 0, 'Positive original Lambda')
    widths[2] *= max(box[1][1]/F(cfg['Lambda']), F(1,10000))*alpha_priority
    axis = max(range(5), key=lambda i: widths[i])
    need(widths[axis] > 0, 'Unresolved zero-width original box')
    return axis


def advance(c, cfg, item, nodes, alpha_priority):
    k, path, node, box = item
    decision, result = c.evaluate(cfg, k, box)
    if decision is not None:
        node.clear()
        node.update(kind='leaf', box=c.enc(box), decision=decision, result=result)
        return 'leaf', decision
    need(len(path) < 128 and nodes+2 <= c.LIMIT, 'Original split depth/node budget exhausted')
    axis = split_axis(cfg, box, alpha_priority)
    cut = sum(box[axis])/2
    c.children(box, axis, cut)  # Original strict-interior validation.
    node.clear()
    node.update(kind='split', axis=axis, cut=str(cut),
                left={'kind':'pending'}, right={'kind':'pending'})
    return 'split', None


def choose_pending(pending, order):
    need(order in ('depth','breadth','root-first'), 'Named discovery traversal only')
    need(bool(pending), 'Nonempty candidate frontier')
    if order == 'depth':
        return 0
    if order == 'root-first':
        return next((i for i,item in enumerate(pending) if item[1] == ''),0)
    return min(range(len(pending)),key=lambda i:(len(pending[i][1]),pending[i][0],pending[i][1]))


def save(output, packet):
    """Two stable filenames: never race the supervisor by unlinking a temp file.

    Backup is fully flushed before overwriting the primary. A killed write
    leaves at least one parseable prior/current snapshot after the first save.
    """
    for name in ('CHECKPOINT.backup.json','CHECKPOINT.json'):
        target = output/name
        need(not target.is_symlink() and (not target.exists() or target.is_file()),
             'Only this new epoch\'s own regular checkpoint files')
        with target.open('w', encoding='utf-8') as stream:
            json.dump(packet, stream, separators=(',',':'))
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capsule', type=Path, required=True)
    p.add_argument('--design-sha256', required=True, help='Externally pinned FROZEN_DESIGN.json identity')
    p.add_argument('--output', type=Path, required=True, help='New private checkpoint directory')
    p.add_argument('--resume', type=Path, help='Candidate checkpoint only, never an accepted proof')
    p.add_argument('--seconds', type=int, default=600)
    p.add_argument('--alpha-priority', choices=('1','4'), default='4')
    p.add_argument('--order', choices=('depth','breadth','root-first'), default='root-first')
    args = p.parse_args()
    need(__debug__ and not sys.flags.optimize, 'Ordinary non-optimized Python')
    need(1 <= args.seconds <= 7200, 'Bounded discovery slice')
    capsule, output = args.capsule.resolve(), args.output.resolve()
    design = capsule/'FROZEN_DESIGN.json'
    need(design.is_file() and not design.is_symlink() and
         digest(design) == args.design_sha256, 'Externally bound original design')
    specdata = json.loads(design.read_text(encoding='utf-8'))
    need(type(specdata.get('files')) is dict and len(specdata['files']) <= 256,
         'Bounded original source design')
    for name, pin in specdata['files'].items():
        need(Path(name).name == name and '/' not in name and '\\' not in name,
             'Flat frozen source names')
        source = capsule/name
        need(source.is_file() and not source.is_symlink() and digest(source) == pin,
             'Original frozen source: '+name)
    need('count_protocol.py' in specdata['files'], 'Original native checker is design-bound')
    sys.path.insert(0, str(capsule))
    spec = importlib.util.spec_from_file_location('original_count_protocol', capsule/'count_protocol.py')
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    cfg, bound = c.load()
    binding = dict(design_sha256=args.design_sha256, native_header=c.header(bound),
                   search_sha256=digest(Path(__file__)), alpha_priority=args.alpha_priority,
                   traversal=args.order)
    if args.resume:
        source = args.resume.resolve()
        need(source.is_file() and not source.is_symlink() and source.stat().st_size <= 128*1024**2,
             'Bounded previous candidate snapshot')
        candidates = [source]
        backup = source.with_suffix('.backup.json')
        if backup.is_file() and not backup.is_symlink() and backup.stat().st_size <= 128*1024**2:
            candidates.append(backup)
        old = None
        for candidate in sorted(candidates,key=lambda x:x.stat().st_mtime_ns,reverse=True):
            try:
                old = json.loads(candidate.read_text(encoding='utf-8'),object_pairs_hook=c.unique)
                break
            except (ValueError,UnicodeError):
                continue
        need(type(old) is dict and old.get('schema') == SCHEMA and
             old.get('arithmetic_accepted') is False, 'Parseable untrusted checkpoint')
        # Search code may evolve: only candidate topology is reused. Original
        # arithmetic/contract/strategy bindings must agree; native acceptance
        # still recomputes all saved leaves in a separate process.
        previous = old.get('binding',{})
        need(all(previous.get(key) == binding[key] for key in
                 ('design_sha256','native_header','alpha_priority')),
             'Same frozen native source/contract and search strategy')
        roots = old['roots']
    else:
        roots = [dict(k=k,tree={'kind':'pending'}) for k in range(cfg['n']+1)]
    pending,nodes,leaves = census(c, cfg, roots)
    need(not output.exists(), 'New search output epoch only')
    output.mkdir(parents=True, exist_ok=False)
    began, last_save, evaluations = time.monotonic(), 0.0, 0
    def checkpoint():
        save(output, dict(schema=SCHEMA,binding=binding,roots=roots,arithmetic_accepted=False))
    checkpoint()
    complete = False
    try:
        while True:
            if not pending:
                complete = True
                break
            if time.monotonic()-began >= args.seconds:
                break
            item = pending.pop(choose_pending(pending,args.order))
            action, decision = advance(c, cfg, item, nodes, F(args.alpha_priority))
            if action == 'split':
                k,path,node,box = item
                left,right = c.children(box,node['axis'],F(node['cut']))
                pending[0:0] = [(k,path+'L',node['left'],left),
                                (k,path+'R',node['right'],right)]
                nodes += 2
            else:
                leaves += 1
            evaluations += 1
            print(json.dumps(dict(event='candidate_search_step',k=item[0],path=item[1],
                                  action=action,decision=decision,evaluations=evaluations,
                                  nodes=nodes,leaves=leaves,pending=len(pending),
                                  elapsed_seconds=round(time.monotonic()-began,3),
                                  arithmetic_accepted=False)),flush=True)
            if evaluations % 10 == 0 or time.monotonic()-last_save >= 15:
                checkpoint()
                last_save = time.monotonic()
    finally:
        checkpoint()
    need(c.load()[1] == bound, 'Original runtime unchanged after discovery')
    for name, pin in specdata['files'].items():
        need(digest(capsule/name) == pin, 'Frozen source unchanged after discovery')
    pending, nodes, leaves = census(c, cfg, roots)
    if complete:
        candidate = dict(**c.header(bound),roots=roots)
        with (output/'CANDIDATE_FOREST.json').open('x',encoding='utf-8') as stream:
            json.dump(candidate,stream)
            stream.write('\n')
    print(json.dumps(dict(status='CANDIDATE_COMPLETE_NOT_ACCEPTED' if complete else 'SEARCH_CHECKPOINTED_INCOMPLETE',
                          nodes=nodes,leaves=leaves,pending=len(pending),
                          arithmetic_accepted=False,output=str(output))),flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('DISCOVERY_INCOMPLETE_NO_ACCEPTANCE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
