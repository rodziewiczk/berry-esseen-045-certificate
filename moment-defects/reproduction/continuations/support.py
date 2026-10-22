"""Guarded full36-target support arithmetic for n6..9; unresolved parents explicit.

--inspect-only reads/hashes sources only. Otherwise execute construct AND
replay through the declared single-function reference-binding port. The full
native arithmetic and all19 native controls run, but this is not unchanged
native final/readback acceptance and establishes no C_n or all-index theorem.
"""
from __future__ import annotations
import argparse
import ast
from datetime import datetime,timezone
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import time
import uuid

if not __package__:
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from reproduction.all_indices.c5_counts import BASE,digest,need,unique
from reproduction.all_indices.c5_inputs import safe_relative
from reproduction.all_indices.c5_initial_one import canonical_native_sources
from reproduction.continuations.archive_guard import install
from reproduction.all_indices.supervised import run_recorded
from reproduction.continuations.catalog import (Sources,support_plan,SUPPORT,PROTOCOL_SHA,
                                                 REGIONS,CUTOFF6,COMBINED)

sys.dont_write_bytecode = True


def read(path):
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)


def controls(source):
    tree = ast.parse(source)
    matches = [node for node in ast.walk(tree) if isinstance(node,ast.Assign)
               and any(isinstance(target,ast.Name) and target.id == 'changes' for target in node.targets)]
    need(len(matches) == 1 and isinstance(matches[0].value,ast.List),'Original complete mutation inventory')
    names = [ast.literal_eval(row.elts[0]) for row in matches[0].value.elts]
    names.append('duplicate JSON key')
    need(len(names) == len(set(names)) == 19,'Every original complete support corruption control')
    return names


def validate_outputs(constructed,replayed,construction_sha,pins,control_names):
    need(constructed['schema'] == 'CONDITIONAL_SUPPORT6_9_36_TARGETS_V1'
         and constructed['status'] == 'CONSTRUCTED_EXACT_SUPPORT_AND_FOURIER_INTERFACES',
         'Exact complete construction scope')
    need(replayed['status'] == 'PASS_FRESH_CONDITIONAL_SUPPORT6_9_AND_COMPLEMENT_JOIN'
         and replayed['n'] == [6,7,8,9] and all(type(n) is int for n in replayed['n'])
         and replayed['cutoff6_proved'] is False,'Exact native conditional replay scope, no cutoff assertion')
    need(replayed['construction_sha256'] == construction_sha,'Actual new full construction was consumed')
    need(replayed['negative_controls'] == control_names,'All original native negative controls, not a prefix')
    for field in ('rows','fourier_interfaces','published_tail','files_sha256'):
        need(constructed[field] == replayed[field],'Complete exact native construct/replay equality: '+field)
    need(canonical_native_sources(replayed['files_sha256']) == pins,'Entire declared minimal conditional source closure')
    inventory = [(n,*region) for n in range(6,10) for region in REGIONS]
    need(len(replayed['rows']) == len(replayed['fourier_interfaces']) == len(inventory) == 36,
         'All36 support targets and same-domain Fourier numerical interfaces')
    for row,interface,(n,name,left,right,radius) in zip(replayed['rows'],replayed['fourier_interfaces'],inventory):
        need(type(row['n']) is int and row['n'] == n and row['region'] == name
             and row['rho'] == [left,right] and row['radius'] == radius,'Whole ordered same-index support domain')
        q = '579/5000' if n == 6 else '0'
        need(row['q'] == q and row['proof']['q_contact'] == q,'Unchanged n6 allowance and later sequential sharp allowance')
        proof = row['proof'];gaussian = proof['gaussian']
        need(type(proof['n']) is int and proof['n'] == n and proof['K'] == '0'
             and type(proof['support_sign']) is int and proof['support_sign'] == 0
             and proof['radius'] == radius and proof['rho_upper'] == right,'Literal original direct support contract')
        need([ray['sign'] for ray in proof['ray_rows']] == [-1,1]
             and all(type(ray['sign']) is int and F(ray['contact_upper']) < 0 for ray in proof['ray_rows']),
             'Both complete closed signed rays strictly excluded')
        need(type(gaussian['cells']) is int and type(gaussian['mesh']) is int
             and F(gaussian['H0']).denominator == 1
             and gaussian['cells'] == 2*int(F(gaussian['H0']))*gaussian['mesh']
             and F(gaussian['tail_upper']) > 0,'Full original threshold mesh and nonzero infinite tails')
        need(type(interface['n']) is int and interface['n'] == n and interface['region'] == name
             and interface['rho'] == [left,right] and interface['support'] == radius
             and F(interface['fourier_upper']) < F(interface['target']),
             'Exact installed conditional Fourier input on the same domain')
    need(replayed['published_tail'] == str(F(3031,10000)*(1+F(323,500)/F(7361,4000))),
         'Unchanged published infinite-rho numerical comparison')
    return dict(n=[6,7,8,9],support_targets=36,signed_support_rays=72,
                native_negative_controls=19,q6='579/5000',later_q='0')


def verify_sources(epoch,pins):
    for name,pin in pins.items():
        path = epoch.joinpath(*safe_relative(name))
        need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(epoch.resolve())
             and digest(path) == pin,'Frozen minimal original source/input: '+name)


def new_epoch(runner):
    root = (BASE/'work').resolve()
    need(not (BASE/'work').is_symlink() and root.parent == BASE.resolve(),'Repository-owned private scratch root')
    root.mkdir(exist_ok=True)
    epoch = root/('s69-'+uuid.uuid4().hex[:12]);epoch.mkdir(exist_ok=False)
    need(epoch.parent == root and not epoch.is_symlink() and runner.inside(epoch,BASE),'Exclusive contained source epoch')
    need(shutil.disk_usage(epoch).free >= runner.DISK_FLOOR+runner.WORK_LIMIT,'Private quota plus4GiB free disk')
    runner.RETAINED_WORK = epoch
    return epoch


def write(path,value):
    with path.open('x',encoding='utf-8') as stream:json.dump(value,stream,indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cutoff6-archive',type=Path,required=True)
    parser.add_argument('--combined-archive',type=Path,required=True)
    parser.add_argument('--inspect-only',action='store_true')
    args = parser.parse_args()
    need(__debug__ and sys.flags.dont_write_bytecode and not sys.flags.optimize,'Ordinary nonoptimized Python -B')
    spec = importlib.util.spec_from_file_location('original_continuation_guard',BASE/'run_reproduction.py')
    runner = importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    runner.HOST_FLOOR = 1024*runner.MIB
    install(runner);runner.parent_guard();runner.verify_sources()
    code_files = {name:digest(Path(__file__).with_name(name)) for name in ('catalog.py','support.py','support_port.py','archive_guard.py')}
    with Sources(args.cutoff6_archive,args.combined_archive,guard=runner.parent_guard) as sources:
        plan = support_plan(sources)
        if args.inspect_only:
            print(json.dumps(plan,indent=2),flush=True);return
        runner.launch_gate();epoch = new_epoch(runner)
        pins = plan['source_files_sha256']
        for name,pin in pins.items():
            target = epoch.joinpath(*safe_relative(name));target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(sources.read(name,pin))
    # Close both large archive indexes before launching any numerical child.
    full_guard = runner.parent_guard
    def epoch_guard(tiny=False,work=None):
        return full_guard(tiny=tiny,work=epoch if work is not None else None)
    runner.parent_guard = epoch_guard
    worker = epoch/'support_port.py'
    shutil.copyfile(Path(__file__).with_name(worker.name),worker)
    need(digest(worker) == code_files[worker.name],'Frozen declared reference-binding port')
    inputs = epoch/'CONDITIONAL_INPUTS.json'
    write(inputs,dict(scope='PINNED_CONDITIONAL_PARENT_INPUTS_NOT_FRESH_PROOFS',
                      parent_files_sha256=plan['conditional_parent_input_files']))
    inputs_pin = digest(inputs)
    directory = epoch/SUPPORT;protocol = directory/'protocol.py'
    need(digest(protocol) == PROTOCOL_SHA,'Original native source on disk remains unmodified')
    expected_controls = controls(protocol.read_text(encoding='utf-8'))
    verify_sources(epoch,pins)
    need(not any((directory/name).exists() for name in ('CONSTRUCTED.json','REPLAY_CHECKED.json')),
         'No old own target output in the new private epoch')
    captures = []
    print(json.dumps(dict(event='support6_9_conditional_arithmetic_started',work=str(epoch),
        support_targets=36,source_files=len(pins),fresh_parent_fact_joins_verified=False)),flush=True)
    for action,output in (('construct','CONSTRUCTED.json'),('replay','REPLAY_CHECKED.json')):
        runner.launch_gate();verify_sources(epoch,pins)
        command = [sys.executable,'-B',str(worker),'--protocol',str(protocol),'--action',action,'--inputs',str(inputs)]
        started = datetime.now(timezone.utc).isoformat();tick = time.monotonic()
        stdout = run_recorded(runner,command,directory,'support-'+action,7200,512*runner.MIB)
        status = 'CONSTRUCTED_EXACT_SUPPORT_AND_FOURIER_INTERFACES' if action == 'construct' else 'PASS_FRESH_CONDITIONAL_SUPPORT6_9_AND_COMPLEMENT_JOIN'
        need(stdout.splitlines()[-1] == status,'Whole original numerical-body acceptance line')
        verify_sources(epoch,pins)
        need(digest(worker) == code_files[worker.name] and digest(inputs) == inputs_pin,'Frozen new port and declared parent inputs unchanged')
        capture = epoch/'captures'/action;capture.mkdir(parents=True,exist_ok=False)
        shutil.copyfile(directory/('support-'+action+'.stdout.txt'),capture/'stdout.txt')
        with (capture/'stderr.txt').open('xb'):pass
        metadata = dict(command=command,cwd=str(directory.resolve()),returncode=0,
            started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,
            input_sha256=pins,port_worker_sha256=digest(worker),conditional_inputs_sha256=inputs_pin,
            stdout_sha256=digest(capture/'stdout.txt'),stderr_sha256=digest(capture/'stderr.txt'),
            native_result_path=str(directory/output),native_result_sha256=digest(directory/output),
            source_port_scope=plan['source_port_scope'],
            scope='ACTUAL_GUARDED_PORTED_BODY_EXECUTION_NOT_UNCHANGED_NATIVE_ACCEPTANCE')
        write(capture/'metadata.json',metadata)
        captures.append(dict(path=str(capture),metadata_sha256=digest(capture/'metadata.json')))
    constructed,replayed = read(directory/'CONSTRUCTED.json'),read(directory/'REPLAY_CHECKED.json')
    facts = validate_outputs(constructed,replayed,digest(directory/'CONSTRUCTED.json'),pins,expected_controls)
    verify_sources(epoch,pins)
    need(all(digest(Path(__file__).with_name(name)) == pin for name,pin in code_files.items()),'Published adapter code unchanged')
    runner.verify_sources();runner.parent_guard(work=epoch)
    report = dict(schema='CONTINUATION_SUPPORT6_9_CONDITIONAL_ARITHMETIC_V1',
        scope='FULL36_TARGET_ARITHMETIC_ONLY_PARENT_PROOFS_AND_GLOBAL_COMPOSITION_NOT_DISCHARGED',
        status='FRESH_CONDITIONAL_SUPPORT6_9_ARITHMETIC_ACCEPTED',
        facts=facts,source_files_sha256=pins,source_assets_sha256={CUTOFF6.name:CUTOFF6.sha256,COMBINED.name:COMBINED.sha256},
        adapter_files_sha256=code_files,source_port_scope=plan['source_port_scope'],
        changed_native_functions=['receipt'],numerical_native_body_unchanged=True,
        original_protocol_sha256=PROTOCOL_SHA,conditional_parent_input_files=plan['conditional_parent_input_files'],
        historical_parent_closure_directly_unavailable=plan['historical_parent_closure_directly_unavailable'],
        retained_parent_obligations=plan['retained_parent_obligations'],captures=captures,
        constructed_path=str(directory/'CONSTRUCTED.json'),constructed_sha256=digest(directory/'CONSTRUCTED.json'),
        native_result_path=str(directory/'REPLAY_CHECKED.json'),native_result_sha256=digest(directory/'REPLAY_CHECKED.json'),
        execution_observed_by_this_controller=True,fresh_support_arithmetic=True,
        unchanged_native_acceptance_claimed=False,independent_native_readback_claimed=False,
        fresh_parent_fact_joins_verified=False,any_global_Cn_conclusion_verified=False,all_index_conclusion_verified=False)
    destination = epoch/'FRESH_SUPPORT6_9_ARITHMETIC_RESULT.json';write(destination,report)
    print(json.dumps(dict(event='support6_9_arithmetic_finished',report=str(destination),sha256=digest(destination),
                          **facts,fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)),flush=True)


if __name__ == '__main__':
    try:main()
    except Exception as exc:
        print('CONTINUATION_SUPPORT6_9_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
