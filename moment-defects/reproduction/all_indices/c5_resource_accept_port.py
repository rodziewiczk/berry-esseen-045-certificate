"""NEW metadata-only source port for frozen C5 resource replay/acceptance.

Not an unchanged native Windows execution. Numerical statements, comparisons,
source hashes, schemas and corruption controls remain unchanged. Only frozen
POSIX source-map lookups, the emitted INITIAL reference, and an explicitly
prevalidated semantic-command reference are adapted. Old JSON is never edited.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

sys.dont_write_bytecode = True
PINS = {
    'resource5_selected_accept_v1': (
        'fa8767cf7b5360118f83cf218624eb2f42b3b51624d5621140d98aca7f88fb5b',
        '6e621ca843d085269977b41cd65bb5e35b1f5a244b2dae7710b655885ff5d9e5', (0,0), (0,0)),
    'resource5_gamma_accept_v1': (
        '19226c291fa5f1f93f9065985154808f415954c8455a98a7f5a93996f33dd834',
        '8f7257037d25dc1cb728d0574e19cba4ac88265a6206cd855dec3679ebbe9434', (1,0), (1,1)),
    'resource5_sector_accept_v1': (
        '873071d29d053b4d8320f0c8bce3e41256bd451e1f9b8ff99cfce6babe8adac8',
        '0523b7dd38da628538500d42da16ca6e480c900adc5a37b05b0fe444ef895ae1', (1,0), (2,0)),
    'resource5_B3_accept_v1': (
        '9666cf094ebb746e5d11af742409dd98a3bfd70e0b141a62c89827eaa68a1cad',
        'd0fc8b2aec210e9a32d3ad1a635d007d4f3e089cfdd88217ee1e76931ae0d194', (1,0), (1,1)),
    'resource5_B3_T3lower_accept_v1': (
        '68dc384fbbac593f256b947878aad452f6c2a0c0b382b67caf39f72c30ea2a3c',
        'b33e715d79225549d13435195739ae784ab30275ba5009cdcf55d229d8bd51aa', (1,0), (1,1)),
}


def need(ok, message):
    if not ok: raise ValueError(message)


def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk:=stream.read(1024**2): value.update(chunk)
    return value.hexdigest()


def unique(pairs):
    result={}
    for key,value in pairs:
        need(key not in result,'Duplicate JSON key');result[key]=value
    return result


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique)


def relative_parts(name):
    need(type(name)is str and '\\'not in name and not name.startswith('/'),'Canonical POSIX input path')
    parts=PurePosixPath(name).parts
    need(parts and '/'.join(parts)==name and all(p not in('.','..') and ':'not in p for p in parts),
         'No relative source escape')
    return parts


def str_relative(node):
    return (isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='str'
            and len(node.args)==1 and not node.keywords and isinstance(node.args[0],ast.Call)
            and isinstance(node.args[0].func,ast.Attribute) and node.args[0].func.attr=='relative_to'
            and len(node.args[0].args)==1 and isinstance(node.args[0].args[0],ast.Name)
            and node.args[0].args[0].id=='R' and not node.args[0].keywords)


def posix(node):
    return ast.copy_location(ast.Call(func=ast.Attribute(value=node.args[0],attr='as_posix',ctx=ast.Load()),
                                     args=[],keywords=[]),node)


def transform(raw, family, stage, *, verify_pin=True):
    """Finite AST whitelist; a source hash rejects every unrelated source edit."""
    need(family in PINS and stage in('replay','accept'),'Known frozen family/action')
    pin=PINS[family][stage=='accept']
    need(not verify_pin or hashlib.sha256(raw).hexdigest()==pin,'Exact frozen native source bytes')
    tree=ast.parse(raw);records=[];counts={'initial_receipt':0,'get':0,'pop':0,'capture_command':0}
    def record(kind,node):
        counts[kind]+=1
        records.append(dict(kind=kind,line=node.lineno,original_ast=ast.dump(node,include_attributes=False)))
    class Port(ast.NodeTransformer):
        def visit_Call(self,node):
            # WhitelistA: only lookups/removals in a files_sha256 dictionary.
            if (stage=='accept' and isinstance(node.func,ast.Attribute) and node.func.attr in('get','pop')
                and isinstance(node.func.value,ast.Subscript)
                and isinstance(node.func.value.slice,ast.Constant)
                and node.func.value.slice.value=='files_sha256'
                and len(node.args)==1 and not node.keywords and str_relative(node.args[0])):
                record(node.func.attr,node.args[0]);node.args[0]=posix(node.args[0])
            return self.generic_visit(node)
        def visit_keyword(self,node):
            # WhitelistB: only the INITIAL reference keyword in the result writer.
            if stage=='replay' and node.arg=='initial_receipt' and str_relative(node.value):
                record('initial_receipt',node.value);node.value=posix(node.value)
            return self.generic_visit(node)
        def visit_Subscript(self,node):
            # WhitelistC: the OS command was checked in full by preflight_capture.
            if (stage=='accept' and isinstance(node.value,ast.Name) and node.value.id=='m'
                and isinstance(node.slice,ast.Constant) and node.slice.value=='command'):
                record('capture_command',node);node.slice=ast.copy_location(ast.Constant('source_semantic_command'),node.slice)
            return self.generic_visit(node)
    tree=Port().visit(tree);ast.fix_missing_locations(tree)
    expected_initial=PINS[family][2][0] if stage=='replay' else 0
    expected_get,expected_pop=PINS[family][3] if stage=='accept' else (0,0)
    need(counts==dict(initial_receipt=expected_initial,get=expected_get,pop=expected_pop,
                      capture_command=1 if stage=='accept'else 0),'Exact per-source metadata-port census')
    return tree,records


def worker_command(adapter, request, request_sha, stage):
    return [sys.executable,'-B','-S',str(Path(adapter).resolve()),'--request',str(Path(request).resolve()),
            '--request-sha256',request_sha,'--stage',stage]


def verify_inputs(epoch, pins):
    need(type(pins)is dict and 1<=len(pins)<=2000,'Bounded pinned resource closure')
    for name,pin in pins.items():
        parts=relative_parts(name);path=epoch.joinpath(*parts)
        need(not any(epoch.joinpath(*parts[:i]).is_symlink()for i in range(1,len(parts)+1))
             and path.is_file()and path.resolve().is_relative_to(epoch.resolve())
             and digest(path)==pin,'Exact immutable resource input: '+name)


def preflight_capture(epoch, request, request_path, request_sha, adapter):
    job=request['job'];cap=epoch.joinpath(*relative_parts(job['capture']))
    meta=read(cap/'metadata.json');directory=epoch.joinpath(*relative_parts(job['directory']))
    expected=worker_command(adapter,request_path,request_sha,'replay')
    need(type(meta['returncode'])is int and meta['returncode']==0 and meta['changed_inputs']==[],
         'Actual successful unchanged resource process')
    need(meta['command']==expected,'Actual OS command exactly matches frozen resource adapter invocation')
    semantic=[sys.executable,'-B','replay.py',*job['arguments']]
    need(meta['source_semantic_command']==semantic and meta['source_semantic_command_is_os_command']is False,
         'Explicit native source argv is not falsely labeled the OS command')
    need(meta['cwd']==str(directory.resolve()) and meta['adapter_sha256']==digest(adapter)==request['adapter_sha256']
         and meta['request_sha256']==request_sha,'Actual cwd, request and adapter identities')
    replay_rel=job['directory']+'/replay.py'
    need(meta['original_script']==replay_rel and meta['original_script_sha256']==request['source_files_sha256'][replay_rel]
         ==PINS[job['family']][0],'Frozen replay source identity')
    need(meta['stdout_sha256']==digest(cap/'stdout.txt')and meta['stderr_sha256']==digest(cap/'stderr.txt')
         ==hashlib.sha256(b'').hexdigest(),'Actual stdout and empty stderr bytes')
    local={PurePosixPath(n).name:h for n,h in request['source_files_sha256'].items()
           if str(PurePosixPath(n).parent)==job['directory']}
    need(local and meta['input_sha256']==local,'Entire fixed local source capture, no omitted inputs')
    report=epoch/'PORT_REPLAY_REPORT.json'
    need(meta['source_port_report_sha256']==digest(report),'Actual replay source-port report binding')
    port=read(report)
    _,expected_edits=transform((epoch.joinpath(*relative_parts(replay_rel))).read_bytes(),
                              job['family'],'replay')
    need(port['original_source_sha256']==PINS[job['family']][0]and port['adapter_sha256']==digest(adapter)
         and port['request_sha256']==request_sha and port['stage']=='replay'
         and port['exact_ast_transforms']==expected_edits
         and port['scope']=='NEW_METADATA_ONLY_SOURCE_PORT_NOT_UNCHANGED_NATIVE_WINDOWS_EXECUTION'
         and port['original_source_bytes_modified']is False and port['old_json_or_hashes_modified']is False
         and port['mathematical_expressions_and_all_native_negative_controls_unchanged']is True,
         'Complete fresh replay source-port provenance and exact allowed transform list')
    need(meta['result_sha256']==digest(epoch.joinpath(*relative_parts(job['outputs'][0]))),
         'Actual recomputed replay result binding')
    return meta


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--request',type=Path,required=True)
    p.add_argument('--request-sha256',required=True)
    p.add_argument('--stage',choices=('replay','accept'),required=True)
    args=p.parse_args();need(__debug__ and not sys.flags.optimize,'Ordinary nonoptimized metadata port')
    request_path=args.request.resolve();need(request_path.stat().st_size<=1024**2 and
        digest(request_path)==args.request_sha256,'Externally pinned bounded current request')
    request=read(request_path);epoch=request_path.parent;job=request['job'];adapter=Path(__file__).resolve()
    need(digest(adapter)==request['adapter_sha256']and job['kind']=='resource'and type(job['n'])is int
         and job['n']==5,'Actual source-bound resource adapter and literal5')
    directory=epoch.joinpath(*relative_parts(job['directory']))
    need(Path.cwd().resolve()==directory.resolve(),'Actual native source cwd')
    verify_inputs(epoch,request['source_files_sha256'])
    if args.stage=='accept':preflight_capture(epoch,request,request_path,args.request_sha256,adapter)
    script=directory/(args.stage+'.py');raw=script.read_bytes()
    need(digest(script)==request['source_files_sha256'][job['directory']+'/'+script.name],
         'Native source agrees with the pinned complete FINAL closure')
    tree,edits=transform(raw,job['family'],args.stage)
    old_argv=sys.argv[:];sys.argv=[script.name,*job['arguments']];sys.path.insert(0,str(directory))
    try:
        namespace={'__name__':'__main__','__file__':str(script),'__builtins__':__builtins__}
        exec(compile(tree,str(script),'exec'),namespace)
    finally:
        sys.path.pop(0);sys.argv=old_argv
    verify_inputs(epoch,request['source_files_sha256'])
    need(digest(request_path)==args.request_sha256 and digest(adapter)==request['adapter_sha256'],
         'Current request and executing metadata-port source unchanged after native body')
    report=dict(scope='NEW_METADATA_ONLY_SOURCE_PORT_NOT_UNCHANGED_NATIVE_WINDOWS_EXECUTION',
        stage=args.stage,original_source_sha256=hashlib.sha256(raw).hexdigest(),adapter_sha256=digest(adapter),
        request_sha256=args.request_sha256,exact_ast_transforms=edits,
        original_source_bytes_modified=False,old_json_or_hashes_modified=False,
        mathematical_expressions_and_all_native_negative_controls_unchanged=True,
        fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)
    output=epoch/('PORT_'+args.stage.upper()+'_REPORT.json')
    with output.open('x',encoding='utf-8')as stream:json.dump(report,stream,indent=2)
    print(json.dumps(dict(event='resource_metadata_source_port_completed',stage=args.stage,
        report=str(output),all_index_conclusion_verified=False)),flush=True)


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('C5_RESOURCE_METADATA_PORT_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
