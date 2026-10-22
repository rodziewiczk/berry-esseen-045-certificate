"""Select native count jobs from pinned composer coverage, never a directory glob.

The composer and old acceptances select source/forest identities only. Their
PASS fields do not count as numerical work. A separate guarded native call
must reconstruct all roots and re-evaluate every leaf with all controls.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import ast
from pathlib import PurePosixPath

from .catalog import parse,FINAL,FINAL_SHA
from ..all_indices.c5_counts import need
from ..all_indices.c5_inputs import safe_relative


@dataclass(frozen=True)
class CountJob:
    job_id: str
    n: int
    band: str
    index: int
    capsule: str
    contract_pin: str
    forest_pin: str
    old_receipt_pin: str
    target: str
    band_rho: tuple[str,str]
    composer_receipt: str
    composer_receipt_pin: str
    forest_name: str = 'COUNT_FOREST.json'
    receipt_name: str = 'COUNT_ACCEPTED.json'
    command: tuple[str,...] = ('-B','count_protocol.py','accept')


def count_jobs(sources):
    final = parse(sources.read(FINAL,FINAL_SHA))
    graph = final['files_sha256']
    need(len(graph) == 38166 and final['indices'] == [6,7,8,9], 'Exact selected finite composer source index')
    bands = final['chain']['bands']
    need([(row['n'],row['band']) for row in bands] == [(n,b) for n in range(6,10) for b in ('B0','BN','B2')],
         'All12 declared same-index moment bands')
    by_directory = {}
    for path,pin in graph.items():
        directory,basename = path.rsplit('/',1)
        by_directory.setdefault(directory,{})[basename] = pin
    jobs = []
    for branch in bands:
        name,pin = branch['receipt'],branch['receipt_sha256']
        need(graph[name] == pin,'Pinned source-selection receipt')
        band = parse(sources.read(name,pin))
        need(type(band['n']) is int and band['n'] == branch['n'] and band['band'] == branch['band']
             and band['rho'] == branch['rho'], 'Same exact source-selection band')
        rows = band['coverage']['rows']
        need(type(rows) is list and len(rows) == 100,'Complete original closed panel catalog')
        selected = []
        for i,row in enumerate(rows):
            need(type(row['index']) is int and row['index'] == i
                 and row['p'] == [str(F(i,100)),str(F(i+1,100))], 'Every ordered closed probability panel')
            if row['closure'] != 'count':continue
            source = row['source'];capsule = source['capsule'];safe_relative(capsule)
            local_graph = by_directory[capsule]
            chosen = {}
            for ending,key in (('_FOREST.json','forest_sha256'),('_ACCEPTED.json','acceptance_sha256')):
                matches = [name for name,pin in local_graph.items() if name.endswith(ending) and pin == source[key]]
                need(len(matches) == 1,'Composer chooses exactly one local original '+ending)
                chosen[key] = matches[0]
            need(graph[capsule+'/contract.json'] == source['contract_sha256'],'Composer binds original count contract')
            jobs.append(CountJob(f'n{band["n"]}.{band["band"]}.p{i:02}',band['n'],band['band'],i,capsule,
                source['contract_sha256'],source['forest_sha256'],source['acceptance_sha256'],
                branch['target'],tuple(branch['rho']),name,pin,
                forest_name=chosen['forest_sha256'],receipt_name=chosen['acceptance_sha256']))
            selected.append(i)
        need(len(selected) == branch['census']['count'],'Exact selected source count census')
    need(len(jobs) == len({job.job_id for job in jobs}) == 284,'Every selected forest exactly once')
    return tuple(jobs),graph


def job_sources(sources,job,graph,*,verify_bytes=False):
    prefix = job.capsule+'/'
    manifest_name = prefix+'KERNEL_COPY_MANIFEST.json'
    manifest = parse(sources.read(manifest_name,graph[manifest_name]))
    local = manifest['files']
    need(type(local) is dict and local,'Complete native runtime manifest')
    pins = {manifest_name:graph[manifest_name]}
    for name,pin in local.items():
        need(len(safe_relative(name)) == 1 and PurePosixPath(name).name == name,'Original count-local runtime path')
        need(graph[prefix+name] == pin,'Whole kernel manifest agrees with final source graph')
        pins[prefix+name] = pin
    for name,pin in (('contract.json',job.contract_pin),(job.forest_name,job.forest_pin),
                     ('count_protocol.py',graph[prefix+'count_protocol.py'])):
        need(graph[prefix+name] == pin,'Selected exact native input identity')
        pins[prefix+name] = pin
    need(prefix+job.receipt_name not in pins,'Old own acceptance is never copied as a new proof')
    # Two selected old acceptance outputs were not included in the source ZIP.
    # They are NOT runtime inputs: the unchanged checker recreates them. Its
    # source and the original forest/contract are fully available and pinned.
    try: old = parse(sources.read(prefix+job.receipt_name,job.old_receipt_pin))
    except FileNotFoundError: old = None
    native_schema = acceptance_schema(sources.read(prefix+'count_protocol.py',pins[prefix+'count_protocol.py']).decode('utf-8'))
    contract = parse(sources.read(prefix+'contract.json',job.contract_pin))
    need(native_schema['n'] == job.n and type(native_schema['n']) is int
         and native_schema['index'] == job.index and type(native_schema['index']) is int,
         'Same actual literal sample/panel in the unchanged native writer')
    if old is not None:
        need(type(old['n']) is int and old['n'] == job.n and type(old['index']) is int and old['index'] == job.index,
             'Same literal sample/panel in the optional reference schema')
        need(old['contract_sha256'] == job.contract_pin and old['forest_sha256'] == job.forest_pin
             and old['checker_sha256'] == pins[prefix+'count_protocol.py']
             and old['kernel_sha256'] == local,'Exact optional checker/kernel/contract/forest source bindings')
        need(old['negative_controls'] == native_schema['controls'],'Complete native mutation inventory reference')
    need(type(contract['rows']) is list and len(contract['rows']) == 1,'One acquired same-law panel contract')
    cfg = contract['rows'][0]
    need(type(cfg['n']) is int and cfg['n'] == job.n and type(cfg['index']) is int and cfg['index'] == job.index
         and cfg['p'] == [str(F(job.index,100)),str(F(job.index+1,100))]
         and F(cfg['rho_lower']) >= F(job.band_rho[0]) and F(cfg['rho_upper']) <= F(job.band_rho[1])
         and F(cfg['rho_lower']) <= F(cfg['rho_upper']) and cfg['K'] == '0',
         'Literal count contract and exact containing closed source domain')
    total = maximum = 0
    for name,pin in pins.items():
        _,info = sources.member(name,max_bytes=64*1024**2)
        total += info.file_size;maximum = max(maximum,info.file_size)
        if verify_bytes:sources.read(name,pin,max_bytes=64*1024**2)
    need(total <= 64*1024**2,'One capsule fits a bounded private64MiB source allowance')
    return dict(job=job,source_files_sha256=pins,source_files=len(pins),source_bytes=total,
                maximum_source_file_bytes=maximum,old_schema_reference=old,native_schema=native_schema,contract=contract,
                scope='COUNT_SOURCE_INSPECTION_ONLY_NOT_NUMERICAL_REPLAY',
                fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)


def acceptance_schema(source):
    """Read the exact unchanged writer/control declarations WITHOUT importing it."""
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name == 'accept']
    need(len(functions) == 1,'One original complete native acceptor')
    outputs = [node.value for node in ast.walk(functions[0]) if isinstance(node,ast.Assign)
               and any(isinstance(target,ast.Name) and target.id == 'out' for target in node.targets)]
    need(len(outputs) == 1 and isinstance(outputs[0],ast.Call) and isinstance(outputs[0].func,ast.Name)
         and outputs[0].func.id == 'dict' and not outputs[0].args,'Literal complete native acceptance writer')
    fields = {item.arg:item.value for item in outputs[0].keywords}
    need(None not in fields and len(fields) == len(outputs[0].keywords),'Explicit unique native output fields')
    mutations = [node.value for node in ast.walk(functions[0]) if isinstance(node,ast.Assign)
                 and any(isinstance(target,ast.Name) and target.id == 'mutations' for target in node.targets)]
    need(len(mutations) == 1 and isinstance(mutations[0],ast.List),'Complete original literal control inventory')
    names = [ast.literal_eval(row.elts[0]) for row in mutations[0].elts]
    need(len(names) == len(set(names)) == 24,'All24 original native count controls')
    result = {name:ast.literal_eval(fields[name]) for name in ('status','n','index','scope')}
    result.update(fields=sorted(fields),controls=names)
    return result
