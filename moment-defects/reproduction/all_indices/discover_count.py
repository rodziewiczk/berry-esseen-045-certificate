"""Protected serial supervisor for an untrusted original count-tree search."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[2]
DERIVED_V14_DESIGNS = {
    31: '6ca73188c5a6969c1f0ec69f41cb0fac660003cf0515fdcadeeda83afcf654f0',
    32: '230a6bb37696c1e79d62847d89090d4187d78d41aa6c98ccbe91c54e1f8f950b',
}


def acceptance_identity(capsule,index,design_sha):
    metadata = capsule/'B3_V14_SOURCE_EPOCH.json'
    if not metadata.exists():
        return 'PASS_FRESH_CONDITIONAL_EXACT_COUNT'+str(index), 'ONE_ORIGINAL_CONDITIONAL_COUNT_ONLY'
    if DERIVED_V14_DESIGNS.get(index) != design_sha:
        raise ValueError('Derived V14 source epoch needs its independently reviewed exact design')
    epoch = json.loads(metadata.read_text())
    expected = 'PASS_FRESH_CONDITIONAL_B3_V14_EPOCH_20261022_COUNT'+str(index)
    if not (epoch.get('schema') == 'NEW_CONDITIONAL_B3_V14_SOURCE_EPOCH_20261022_V1'
            and type(epoch.get('n')) is int and epoch['n'] == 25
            and type(epoch.get('index')) is int and epoch['index'] == index
            and epoch.get('native_schema') == 'NEW_CONDITIONAL_B3_V14_EPOCH_20261022_PANEL'+str(index)+'_FULL_ROOTS_V1'
            and epoch.get('expected_native_status') == expected
            and epoch.get('helper_manifest_sha256') == 'ba80569735e7042a588eba6c8219fbd68c4deae354c3983ea518dbbb2d9a8336'
            and epoch.get('arithmetic_accepted') is False):
        raise ValueError('Explicit distinct derived V14 identity and conditional scope')
    return expected,'ONE_NEW_DERIVED_CONDITIONAL_B3_V14_COUNT_ONLY'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capsule',type=Path,required=True)
    p.add_argument('--design-sha256',required=True)
    p.add_argument('--resume',type=Path)
    p.add_argument('--seconds',type=int,default=600)
    p.add_argument('--alpha-priority',choices=('1','4'),default='4')
    p.add_argument('--order',choices=('depth','breadth','root-first'),default='root-first')
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('original_runner',BASE/'run_reproduction.py')
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    from stable_guard import install
    install(r)
    from supervised import run_recorded
    from count_discovery import digest
    r.HOST_FLOOR = 1024*r.MIB
    r.parent_guard()
    r.verify_sources()
    r.require(1 <= args.seconds <= 7200, 'Bounded discovery slice')
    capsule = args.capsule.resolve()
    design = capsule/'FROZEN_DESIGN.json'
    r.require(design.is_file() and not design.is_symlink() and design.stat().st_size <= r.MIB
              and digest(design) == args.design_sha256, 'Externally pinned source design')
    value = json.loads(design.read_text(encoding='utf-8'))
    r.require(type(value.get('files')) is dict and len(value['files']) <= 256, 'Bounded source set')
    work = r.private_work()
    copy = work/'capsule'
    copy.mkdir()
    for name, pin in dict(value['files'], **{'FROZEN_DESIGN.json':args.design_sha256}).items():
        r.require(Path(name).name == name and '/' not in name and '\\' not in name,
                  'Flat original capsule')
        source = capsule/name
        r.require(source.is_file() and not source.is_symlink() and source.stat().st_size <= 16*r.MIB
                  and digest(source) == pin, 'Exact original source: '+name)
        with source.open('rb') as src, (copy/name).open('xb') as dst:
            shutil.copyfileobj(src,dst,length=r.MIB)
        r.require(digest(copy/name) == pin, 'Exact private copy')
        r.parent_guard(work=work)
    worker = work/'count_discovery.py'
    shutil.copyfile(Path(__file__).with_name('count_discovery.py'),worker)
    command = ['--capsule',str(copy),'--design-sha256',args.design_sha256,
               '--output',str(work/'search'),'--seconds',str(args.seconds),
               '--alpha-priority',args.alpha_priority,'--order',args.order]
    if args.resume:
        source = args.resume.resolve()
        r.require(source.is_file() and not source.is_symlink() and source.stat().st_size <= 128*r.MIB,
                  'Bounded candidate checkpoint; not an accepted certificate')
        with source.open('rb') as src, (work/'resume.json').open('xb') as dst:
            shutil.copyfileobj(src,dst,length=r.MIB)
        backup = source.with_suffix('.backup.json')
        if backup.exists():
            r.require(backup.is_file() and not backup.is_symlink() and backup.stat().st_size <= 128*r.MIB,
                      'Bounded fallback candidate checkpoint')
            with backup.open('rb') as src, (work/'resume.backup.json').open('xb') as dst:
                shutil.copyfileobj(src,dst,length=r.MIB)
        command += ['--resume',str(work/'resume.json')]
    print(json.dumps(dict(event='untrusted_discovery_start',work=str(work),
                          arithmetic_accepted=False)),flush=True)
    prefix = work/'search-fresh-pycache'
    r.launch_gate()
    stdout = run_recorded(r,r.python_command(worker,command,prefix),work,'count-discovery',
                          args.seconds+120,512*r.MIB,prefix=prefix)
    result = json.loads(stdout.splitlines()[-1])
    r.require(result.get('arithmetic_accepted') is False, 'Search never claims acceptance')
    r.require(result.get('status') in ('CANDIDATE_COMPLETE_NOT_ACCEPTED','SEARCH_CHECKPOINTED_INCOMPLETE'),
              'Explicit candidate outcome')
    result.update(scope='UNTRUSTED_SEARCH_ONLY_NATIVE_ACCEPTANCE_STILL_REQUIRED',work=str(work))
    if result['status'] == 'CANDIDATE_COMPLETE_NOT_ACCEPTED':
        candidate = work/'search/CANDIDATE_FOREST.json'
        # Literal original native filenames; no source rewrite or old acceptance.
        contract = json.loads((copy/'contract.json').read_text())
        index = contract['rows'][0]['index']
        r.require(type(index) is int and 0 <= index <= 100,'Literal original panel index')
        expected_status,accepted_scope = acceptance_identity(copy,index,args.design_sha256)
        forest = copy/('COUNT'+str(index)+'_FOREST.json')
        receipt = copy/('COUNT'+str(index)+'_ACCEPTED.json')
        r.require(not forest.exists() and not receipt.exists(),'Fresh native acceptance epoch')
        with candidate.open('rb') as src, forest.open('xb') as dst:
            shutil.copyfileobj(src,dst,length=r.MIB)
        prefix2 = work/'native-accept-fresh-pycache'
        r.launch_gate()
        run_recorded(r,r.python_command(copy/'count_protocol.py',['accept'],prefix2),
                     work,'native-count-accept',7200,512*r.MIB,prefix=prefix2)
        accepted = json.loads(receipt.read_text())
        r.require(accepted.get('status') == expected_status
                  and accepted.get('forest_sha256') == digest(forest), 'Fresh original acceptance binding')
        r.require(accepted.get('fresh_leaf_evaluations') == result['leaves']
                  and len(accepted.get('negative_controls',[])) == 24,'Every leaf and corruption control')
        result.update(scope=accepted_scope,
                      status='NATIVE_COUNT_ACCEPTED',arithmetic_accepted=True,
                      native_receipt=str(receipt),all_index_conclusion_verified=False)
    with (work/'SEARCH_RESULT.json').open('x',encoding='utf-8') as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('COUNT_DISCOVERY_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
