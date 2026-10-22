"""One protected resource replay and complete metadata-ported native acceptance.

The old parent receipts are immutable REFERENCE inputs. Their matching fresh
facts must be joined separately. This stage exports complete fresh arithmetic,
not c5.resources and not a proof supplied by old INITIAL status labels.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import time
import uuid

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from .c5_high_one import read, source_at, verify_sources
    from .c5_inputs import extended, safe_relative
    from .c5_acquisition_plan import RESOURCE_JOBS, inspect_job, description
    from .c5_resources_arithmetic import summarize_job, REPLAY_STATUS
    from .c5_resource_accept_port import worker_command
    from .stable_guard import install
    from .supervised import run_recorded
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from c5_high_one import read, source_at, verify_sources
    from c5_inputs import extended, safe_relative
    from c5_acquisition_plan import RESOURCE_JOBS, inspect_job, description
    from c5_resources_arithmetic import summarize_job, REPLAY_STATUS
    from c5_resource_accept_port import worker_command
    from stable_guard import install
    from supervised import run_recorded

sys.dont_write_bytecode=True


def private_epoch(runner):
    literal=BASE/'work';root=literal.resolve()
    need(not literal.is_symlink() and root.parent==BASE.resolve(),'Repository-owned regular work root')
    root.mkdir(exist_ok=True);plain=root/('r5-'+uuid.uuid4().hex[:12]);plain.mkdir(exist_ok=False)
    need(plain.resolve().parent==root and runner.inside(plain,BASE),'Exclusive new repository-owned epoch')
    epoch=extended(plain)
    need(shutil.disk_usage(epoch).free>=runner.DISK_FLOOR+runner.WORK_LIMIT,'Scratch quota plus4GiB floor')
    runner.RETAINED_WORK=epoch
    return epoch


def capture_replay(epoch, directory, job, command, request_sha, adapter, source_pins,
                   stdout_path, started_utc, elapsed):
    """New capture of the ACTUAL wrapper command, plus distinctly semantic argv."""
    capture=epoch.joinpath(*safe_relative(job.capture))
    need(not capture.exists(),'No old native capture may survive in the new epoch')
    capture.mkdir(parents=True,exist_ok=False)
    shutil.copyfile(stdout_path,capture/'stdout.txt')
    with (capture/'stderr.txt').open('xb'):pass
    local={PurePosixPath(name).name:pin for name,pin in source_pins.items()
           if str(PurePosixPath(name).parent)==job.directory}
    need(local and all(digest(directory/name)==pin for name,pin in local.items()),
         'All actual fixed local replay inputs are unchanged')
    meta=dict(command=command,source_semantic_command=[sys.executable,'-B','replay.py',*job.arguments],
        source_semantic_command_is_os_command=False,cwd=str(directory.resolve()),
        returncode=0,changed_inputs=[],input_sha256=local,
        stdout_sha256=digest(capture/'stdout.txt'),stderr_sha256=digest(capture/'stderr.txt'),
        original_script=job.directory+'/replay.py',
        original_script_sha256=source_pins[job.directory+'/replay.py'],
        adapter_sha256=digest(adapter),request_sha256=request_sha,
        source_port_report_sha256=digest(epoch/'PORT_REPLAY_REPORT.json'),
        result_sha256=digest(epoch/job.output_paths[0]),
        started_utc=started_utc,finished_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=elapsed,
        scope='NEW_ACTUAL_GUARDED_METADATA_PORT_EXECUTION_NOT_HISTORICAL_CAPTURE')
    with (capture/'metadata.json').open('x',encoding='utf-8')as stream:json.dump(meta,stream,indent=2)
    return capture


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--job',choices=tuple(j.job_id for j in RESOURCE_JOBS),required=True)
    args=parser.parse_args();need(__debug__ and not sys.flags.optimize,'Ordinary nonoptimized resource supervisor')
    supervisor_pin=digest(Path(__file__))
    job=next(j for j in RESOURCE_JOBS if j.job_id==args.job)
    spec=importlib.util.spec_from_file_location('resource_small_supervisor',BASE/'run_reproduction.py')
    runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    runner.HOST_FLOOR=1024*runner.MIB;install(runner);runner.parent_guard();runner.verify_sources()
    cache=extended(args.cache);final=source_at(cache,FINAL)
    need(digest(final)==FINAL_SHA,'Pinned complete selected C5 FINAL');graph=read(final)['files_sha256']
    need(len(graph)==16576,'Complete selected immutable source graph')
    inspection=inspect_job(cache,graph,job,guard=runner.parent_guard,include_sources=True)
    pins=inspection['source_files_sha256']
    need(not(set(job.fresh_outputs_to_exclude)&set(pins)),'Own native outputs/capture are genuinely fresh')
    runner.launch_gate();epoch=private_epoch(runner)
    full_guard=runner.parent_guard
    def epoch_guard(tiny=False,work=None):
        return full_guard(tiny=tiny,work=epoch if work is not None else None)
    runner.parent_guard=epoch_guard
    for name,pin in pins.items():
        target=epoch.joinpath(*safe_relative(name));target.parent.mkdir(parents=True,exist_ok=True)
        with source_at(cache,name).open('rb')as source,target.open('xb')as output:
            shutil.copyfileobj(source,output,length=runner.MIB)
        need(digest(target)==pin,'Byte-identical new private resource input: '+name)
    verify_sources(epoch,pins);runner.parent_guard(work=epoch)
    for name in job.fresh_outputs_to_exclude:need(not(epoch/name).exists(),'No old own result or capture: '+name)
    source_worker=Path(__file__).with_name('c5_resource_accept_port.py')
    adapter=epoch/source_worker.name;shutil.copyfile(source_worker,adapter);adapter_pin=digest(adapter)
    request=dict(schema='FRESH_C5_RESOURCE_ARITHMETIC_REQUEST_V1',job=description(job),
        source_files_sha256=pins,original_final_graph_sha256=FINAL_SHA,
        adapter_sha256=adapter_pin,fresh_parent_fact_joins_verified=False,
        scope='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY_NOT_C5_RESOURCES')
    request_path=epoch/'RESOURCE_REQUEST.json'
    with request_path.open('x',encoding='utf-8')as stream:json.dump(request,stream,indent=2)
    request_pin=digest(request_path);directory=epoch.joinpath(*safe_relative(job.directory))
    print(json.dumps(dict(event='fresh_resource_arithmetic_started',job_id=job.job_id,
        work=str(epoch),inputs=len(pins),fresh_parent_fact_joins_verified=False)),flush=True)
    command=worker_command(adapter,request_path,request_pin,'replay')
    runner.launch_gate();started_utc=datetime.now(timezone.utc).isoformat();started=time.monotonic()
    run_recorded(runner,command,directory,'resource-native-replay',7200,512*runner.MIB)
    verify_sources(epoch,pins)
    need(digest(adapter)==adapter_pin and digest(request_path)==request_pin,'Source-port adapter/request unchanged')
    capture=capture_replay(epoch,directory,job,command,request_pin,adapter,pins,
        directory/'resource-native-replay.stdout.txt',started_utc,time.monotonic()-started)
    replay=read(epoch/job.output_paths[0])
    need(replay['status']==REPLAY_STATUS[job.family][0],'Full native replay completed, no partial output')
    replay_pin=digest(epoch/job.output_paths[0])
    replay_port_pin=digest(epoch/'PORT_REPLAY_REPORT.json')
    capture_meta_pin=digest(capture/'metadata.json')
    # The next worker independently verifies the REAL capture before allowing
    # the one semantic-command lookup substitution in the original acceptor.
    runner.launch_gate();command2=worker_command(adapter,request_path,request_pin,'accept')
    run_recorded(runner,command2,directory,'resource-native-accept',7200,512*runner.MIB)
    verify_sources(epoch,pins);verify_sources(cache,pins)
    need(digest(adapter)==adapter_pin and digest(request_path)==request_pin,'Final adapter/request source identity')
    accepted=read(epoch/job.output_paths[1]);prepared=read(epoch/job.prepared)
    need(digest(epoch/job.output_paths[0])==replay_pin==accepted['resource_replay_sha256']
         and digest(epoch/'PORT_REPLAY_REPORT.json')==replay_port_pin
         and digest(capture/'metadata.json')==capture_meta_pin
         and digest(Path(__file__))==supervisor_pin,
         'Original fresh replay, exact capture, port report and supervisor preserved through acceptance')
    initial=read(epoch/job.case_directory/'INITIAL.json')
    result=summarize_job(epoch,job,prepared,initial,replay,accepted)
    result.update(original_final_graph_sha256=FINAL_SHA,source_files_sha256=pins,
        reference_parent_receipts_are_not_fresh_proofs=True,
        supervisor_source_sha256=supervisor_pin,
        real_replay_capture=str(capture),real_replay_metadata_sha256=digest(capture/'metadata.json'),
        actual_os_replay_command=command,actual_os_accept_command=command2,
        metadata_source_port_adapter_sha256=adapter_pin,
        replay_source_port_report=read(epoch/'PORT_REPLAY_REPORT.json'),
        accept_source_port_report=read(epoch/'PORT_ACCEPT_REPORT.json'),
        replay_source_port_report_sha256=digest(epoch/'PORT_REPLAY_REPORT.json'),
        accept_source_port_report_sha256=digest(epoch/'PORT_ACCEPT_REPORT.json'),
        source_catalog_inspection={k:v for k,v in inspection.items()if k!='source_files_sha256'})
    runner.verify_sources();runner.parent_guard(work=epoch)
    dest=epoch/'RESOURCE_ARITHMETIC_RESULT.json'
    with dest.open('x',encoding='utf-8')as stream:json.dump(result,stream,indent=2)
    runner.parent_guard(work=epoch)
    print(json.dumps(dict(scope='CONDITIONAL_RESOURCE_ARITHMETIC_ONLY',job_id=job.job_id,
        report=str(dest),sha256=digest(dest),panels=len(job.indices),
        fresh_parent_fact_joins_verified=False,register_as_c5_resources=False,
        all_index_conclusion_verified=False)),flush=True)


if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('C5_SINGLE_RESOURCE_ARITHMETIC_INCOMPLETE: '+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
