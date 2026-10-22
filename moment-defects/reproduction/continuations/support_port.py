"""Execute the entire pinned support protocol with conditional parent bindings.

Exactly one function changes: receipt() binds a fixed numerical input instead
of accepting its archived execution/reference graph as a replayed proof.
Every target, Gaussian threshold/tail calculation, signed ray, original
construct/replay comparison and native corruption control is untouched.
This is explicitly NOT unchanged-native or independent-readback acceptance.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
PROTOCOL_SHA = '99cf3310e4589f3f541380eeb867c64a876ddae1e68bc16227d0f0511c7f1cbc'
PARENT_PINS = {
    'work/cutoff6_20261018/audit/auxiliary5_readback_v1/RESULT.json':
        'c841e4d7f08df44e189ece1efcdcac6a1ee5bc25f40795aed3536aad2754b3d4',
    'work/cutoff6_20261018/audit/supported_fourier_readback_v1/OWN_RESULT.json':
        '78f2fbb6cc911983aefd5386ab077ab8a8c2965a028e7775edc212f7933f6a64',
    'work/cutoff6_20261018/audit/supported_fourier_readback_v1/BRIDGE_RESULT.json':
        '467f430ba9b297edbf6a1d63551263d6e080e72d89bc0b3d5fff53daeea70e5c',
    'work/cutoff6_20261018/audit/supported_fourier_readback_v1/RADIUS_RESULT.json':
        'd84fa6ab25bf6c9bdf7cb58516dee4cc8a449b9d3ea5c8edcdeacf0559290f86',
}


def need(value,message):
    if not value: raise ValueError(message)


def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024**2),b''):result.update(block)
    return result.hexdigest()


def port(tree):
    matches = [node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name == 'receipt']
    need(len(matches) == 1,'One original reference-graph reader')
    original = matches[0]
    need(len(original.args.args) == 1 and original.args.args[0].arg == 'p'
         and not original.decorator_list,'Exact original receipt-reader signature')
    replacement = ast.parse('def receipt(p):\n    return __conditional_parent_read(p)\n').body[0]
    tree.body[tree.body.index(original)] = ast.copy_location(replacement,original)
    return ast.fix_missing_locations(tree)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--protocol',type=Path,required=True)
    parser.add_argument('--action',choices=('construct','replay'),required=True)
    parser.add_argument('--inputs',type=Path,required=True)
    args = parser.parse_args()
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary Python -B')
    protocol = args.protocol.resolve();raw = protocol.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == PROTOCOL_SHA,'Exact original complete numerical protocol')
    spec = json.loads(args.inputs.read_text(encoding='utf-8'))
    need(spec['scope'] == 'PINNED_CONDITIONAL_PARENT_INPUTS_NOT_FRESH_PROOFS'
         and type(spec['parent_files_sha256']) is dict and len(spec['parent_files_sha256']) == 4,
         'Explicit four unresolved numerical parent inputs')
    root = protocol.parent.parents[3]
    pins = spec['parent_files_sha256']
    need(pins == PARENT_PINS,'Exactly the four original conditional parent identities, no replacement numbers')
    namespace = {'__name__':'__main__','__file__':str(protocol)}
    def conditional_parent_read(path):
        name = path.relative_to(root).as_posix()
        need(name in pins and sha(path) == pins[name],'Exact frozen conditional numerical parent identity')
        result = namespace['read'](path)
        namespace['bind'](path)
        return result
    namespace['__conditional_parent_read'] = conditional_parent_read
    sys.argv = [str(protocol),args.action]
    exec(compile(port(ast.parse(raw,filename=str(protocol))),str(protocol),'exec'),namespace)
    need(sha(protocol) == PROTOCOL_SHA,'Original source unchanged after complete ported-body execution')
    need(all(sha(root/name) == pin for name,pin in pins.items()),'Conditional inputs unchanged after numerical replay')


if __name__ == '__main__':main()
