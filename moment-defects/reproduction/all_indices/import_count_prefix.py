"""Import a pinned old discovery prefix; never accept its saved arithmetic.

Only candidate geometry and untrusted leaf payloads are reused. The unchanged
native acceptor must subsequently reconstruct all roots and recompute every
leaf. No numerical evaluator is called by this importer.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile

if __package__:
    from . import count_discovery as d
else:
    import count_discovery as d

sys.dont_write_bytecode = True
OLD_SCHEMA = 'UNTRUSTED_PREFIX_LOOKAHEAD_BYPASS_DISCOVERY_CHECKPOINT_V2'
MEMBER = ('cutoff25_20261011/new_root/global_alpha_stoploss2_b3_p33_v12/'
          'PREFIX2_CHECKPOINT_001.json')
PREFIX_BYTES = 2567382
PREFIX_SHA256 = '0d36c90850ed22a88079ca4892625791bfece704c11f65c7e2c54f513fbcd396'
DESIGN_SHA256 = 'e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08'


def unique(pairs):
    result = {}
    for key, value in pairs:
        d.need(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def convert_prefix(packet, native, cfg, expected_header):
    """Validate every closed split, including the old explicit pending boxes."""
    d.need(type(packet) is dict and set(packet) ==
           {'schema', 'header', 'discovery_source_sha256', 'origin', 'roots', 'run'},
           'Exact old discovery envelope')
    d.need(packet['schema'] == OLD_SCHEMA, 'Known untrusted discovery schema')
    d.need(native.same(packet['header'], expected_header),
           'Identical frozen native header, target and source commitments')
    roots = deepcopy(packet['roots'])
    d.need(type(roots) is list and len(roots) == cfg['n'] + 1,
           'Every original ordered count root')
    visited = 0

    def walk(node, box, depth):
        nonlocal visited
        visited += 1
        d.need(visited <= native.LIMIT and depth <= 128,
               'Original node and depth limits')
        d.need(type(node) is dict, 'Dictionary discovery node')
        kind = node.get('kind')
        if kind == 'pending':
            d.need(set(node) == {'kind', 'box'}, 'Old pending node has only geometry')
            d.need(native.same(node['box'], native.enc(box)),
                   'Old pending box equals reconstructed original geometry')
            # The new discovery schema reconstructs pending boxes itself.
            node.clear()
            node['kind'] = 'pending'
        elif kind == 'split':
            d.need(set(node) == {'kind', 'axis', 'cut', 'left', 'right'},
                   'Both closed children retained')
            d.need(type(node['cut']) is str, 'Text rational cut')
            left, right = native.children(box, node['axis'], F(node['cut']))
            walk(node['left'], left, depth + 1)
            walk(node['right'], right, depth + 1)
        else:
            d.need(kind == 'leaf' and
                   set(node) == {'kind', 'box', 'decision', 'result'},
                   'Exact untrusted native leaf fields')
            d.need(native.same(node['box'], native.enc(box)),
                   'Saved leaf box equals reconstructed original geometry')

    for k, root in enumerate(roots):
        d.need(type(root) is dict and set(root) == {'k', 'tree'} and
               type(root['k']) is int and root['k'] == k,
               'Ordered literal roots; no omitted or Boolean count')
        walk(root['tree'], native.rootbox(cfg), 0)
    pending, nodes, leaves = d.census(native, cfg, roots)
    return roots, dict(nodes=nodes, leaves=leaves, pending=len(pending),
                       arithmetic_accepted=False)


def verify_design(capsule):
    design_path = capsule / 'FROZEN_DESIGN.json'
    d.need(design_path.is_file() and not design_path.is_symlink() and
           design_path.stat().st_size <= 1024**2 and
           d.digest(design_path) == DESIGN_SHA256,
           'Externally pinned original p33 design')
    design = json.loads(design_path.read_text(encoding='utf-8'), object_pairs_hook=unique)
    d.need(type(design.get('files')) is dict and len(design['files']) == 76,
           'Complete original frozen design')
    for name, pin in design['files'].items():
        d.need(type(name) is str and Path(name).name == name and
               '/' not in name and '\\' not in name, 'Flat frozen source name')
        source = capsule / name
        d.need(source.is_file() and not source.is_symlink() and
               source.stat().st_size <= 16 * 1024**2 and d.digest(source) == pin,
               'Byte-identical frozen source: ' + name)
    return design


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--capsule', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True,
                        help='Exclusive new directory for an UNTRUSTED checkpoint')
    parser.add_argument('--alpha-priority', choices=('1', '4'), default='4')
    args = parser.parse_args()
    d.need(__debug__ and not sys.flags.optimize, 'Ordinary non-optimized Python')
    capsule = args.capsule.resolve()
    output = args.output.resolve()
    d.need(not output.exists(), 'Exclusive new output directory')
    verify_design(capsule)
    with zipfile.ZipFile(args.archive) as archive:
        d.need(archive.namelist().count(MEMBER) == 1, 'Unique pinned old prefix member')
        info = archive.getinfo(MEMBER)
        d.need(not info.is_dir() and info.file_size == PREFIX_BYTES and
               (info.external_attr >> 16) & 0o170000 != 0o120000,
               'Bounded regular prefix member')
        raw = archive.read(info)
    d.need(hashlib.sha256(raw).hexdigest() == PREFIX_SHA256,
           'Exact externally pinned old prefix bytes')
    packet = json.loads(raw, object_pairs_hook=unique)
    # Import only the already byte-pinned original runtime. load/header/geometry
    # do not call evaluate(), cell35(), or any numerical proof oracle.
    sys.path.insert(0, str(capsule))
    try:
        spec = importlib.util.spec_from_file_location(
            'original_p33_import_geometry', capsule / 'count_protocol.py')
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        cfg, bound = native.load()
        header = native.header(bound)
        roots, stats = convert_prefix(packet, native, cfg, header)
        d.need(native.load()[1] == bound, 'Unchanged original runtime')
    finally:
        sys.path.pop(0)
    verify_design(capsule)
    binding = dict(design_sha256=DESIGN_SHA256, native_header=header,
                   search_sha256=d.digest(Path(d.__file__)),
                   alpha_priority=args.alpha_priority)
    checkpoint = dict(schema=d.SCHEMA, binding=binding, roots=roots,
                      arithmetic_accepted=False)
    report = dict(scope='UNTRUSTED_DISCOVERY_GEOMETRY_IMPORT_ONLY',
                  source_member=MEMBER, source_sha256=PREFIX_SHA256,
                  design_sha256=DESIGN_SHA256, reused_statistics=stats,
                  numerical_evaluator_called=False, arithmetic_accepted=False,
                  all_index_conclusion_verified=False,
                  requirement='Complete missing leaves and run original native accept fresh.')
    output.mkdir(parents=True, exist_ok=False)
    d.save(output, checkpoint)
    with (output / 'IMPORT_REPORT.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('PREFIX_IMPORT_REJECTED_NO_ACCEPTANCE: ' + str(exc),
              file=sys.stderr, flush=True)
        raise SystemExit(1)
