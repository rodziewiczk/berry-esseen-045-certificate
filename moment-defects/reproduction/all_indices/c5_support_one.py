"""Recompute the original C5 support protocols, conditional on their premises."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from c5_counts import BASE, FINAL, FINAL_SHA, need, digest, unique
from c5_inputs import safe_relative, extended
from supervised import run_recorded

sys.dont_write_bytecode = True
EXTRAS = 'work/cutoff5_20261020/entry/delivery_review_v1/EXTRA_SOURCES.json'
EXTRAS_SHA = 'b9bdcdd09b3411f47de91919bb4437362312873c951b9a29715ced6ffc64d00f'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache',type=Path,required=True)
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('original_runner',BASE/'run_reproduction.py')
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    r.HOST_FLOOR = 1024*r.MIB
    r.parent_guard()
    r.verify_sources()
    cache = extended(args.cache)
    final = cache/FINAL
    extra = cache/EXTRAS
    need(final.is_file() and digest(final) == FINAL_SHA,'Pinned original complete C5 graph')
    need(extra.is_file() and digest(extra) == EXTRAS_SHA,'Pinned omitted-import supplement')
    graph = json.loads(final.read_text(),object_pairs_hook=unique)['files_sha256']
    need(len(graph) == 16576,'Complete original selected graph')
    graph[FINAL],graph[EXTRAS] = FINAL_SHA,EXTRAS_SHA
    for row in json.loads(extra.read_text(),object_pairs_hook=unique)['files']:
        name,pin = row['path'],row['sha256']
        need(name not in graph or graph[name] == pin,'Consistent original extra input')
        graph[name] = pin
    def verify_cache():
        for i,(name,pin) in enumerate(graph.items()):
            parts = safe_relative(name)
            path = cache.joinpath(*parts)
            need(not any(cache.joinpath(*parts[:j]).is_symlink() for j in range(1,len(parts)+1)),
                 'No cached source symlink')
            need(path.is_file() and digest(path) == pin,'Exact unchanged support input graph: '+name)
            if i % 128 == 0: r.parent_guard()
    verify_cache()
    work = r.private_work()
    print(json.dumps(dict(event='fresh_support_start',work=str(work),arithmetic_accepted=False)),flush=True)
    receipts = []
    for name,status in [('support_v1','PASS_FRESH_LITERAL5_Q0_SUPPORT9'),
                        ('support_v2','PASS_FRESH_LITERAL5_Q0_SUPPORT9'),
                        ('support_A0_v1','PASS_FRESH_LITERAL5_Q0_SUPPORT_A0')]:
        source = cache/('work/cutoff5_20261020/high/'+name+'/protocol.py')
        output = work/(name+'-FRESH.json')
        label = name.replace('_','-').lower()
        prefix = work/(label+'-fresh-pycache')
        r.launch_gate()
        stdout = run_recorded(r,r.python_command(source,['replay',str(output)],prefix),
                              work,label,7200,512*r.MIB,prefix=prefix)
        need(stdout.splitlines()[-1] == status,'Original complete support acceptance line')
        result = json.loads(output.read_text(),object_pairs_hook=unique)
        need(result['status'] == status and result['n'] == 5 and
             all(row['status'] == 'CONDITIONAL_SUPPORT_PASS' for row in result['rows']),
             'All original support rows actually recomputed')
        receipts.append(dict(protocol=name,receipt=str(output),sha256=digest(output),
                             rows=len(result['rows']),hypotheses=result['hypotheses']))
    verify_cache()
    report = dict(scope='C5_SUPPORT_ARITHMETIC_CONDITIONAL_ON_ORIGINAL_ANALYTIC_AND_C4_PREMISES',
                  status='FRESH_SUPPORT_PROTOCOLS_ACCEPTED',fresh_arithmetic=True,
                  original_final_graph_sha256=FINAL_SHA,receipts=receipts,
                  all_index_conclusion_verified=False)
    with (work/'FRESH_SUPPORT_RESULT.json').open('x',encoding='utf-8') as stream:
        json.dump(report,stream,indent=2)
    print(json.dumps(report),flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('C5_SUPPORT_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
