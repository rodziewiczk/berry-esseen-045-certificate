"""Exact post-hoc INITIAL parent implications, without an execution-freshness claim.

Revalidate the arithmetic artifact against its complete immutable source and
candidate closures, then join exact support/HIGH/owncap facts on the whole
same-law rho/support domain. Archived INITIAL PASS receipts are not evidence
inputs. The result deliberately leaves execution observation and the named
analytic premises to a separate end-to-end controller.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

if __package__:
    from .c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from .c5_high_one import read, source_at
    from .c5_inputs import extended
    from .c5_acquisition_plan import INITIAL_JOBS, inspect_job
    from .c5_initial_one import control_names, validate_receipt
    from .c5_parent_facts import entails_profile, same_initial_candidate
    from .c5_parent_evidence import (ParentEvidence, checked_json, report_epoch, regular_owned,
                                     verify_graph, verify_capture, load_parent_evidence)
else:
    from c5_counts import BASE, FINAL, FINAL_SHA, digest, need
    from c5_high_one import read, source_at
    from c5_inputs import extended
    from c5_acquisition_plan import INITIAL_JOBS, inspect_job
    from c5_initial_one import control_names, validate_receipt
    from c5_parent_facts import entails_profile, same_initial_candidate
    from c5_parent_evidence import (ParentEvidence, checked_json, report_epoch, regular_owned,
                                    verify_graph, verify_capture, load_parent_evidence)


ANALYTIC_PREMISES = (
    'Global C4 <= C_E for every standardized law with finite third absolute moment.',
    'Attainment and the unrestricted fixed-index same-law contact/support theorem, including q=0 from sharp C4.',
    'The exact Fourier/Prawitz and published tail inequalities assumed by the original support/HIGH/owncap protocols.',
    'The analytic validity of the original finite INITIAL moment-cell/100-panel transition and gap implications.',
)


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def numeric_join(facts,evidence):
    need(type(evidence) is ParentEvidence, 'Exact typed parent artifact evidence')
    need(facts['n'] == 5 and type(facts['n']) is int, 'Literal same-index INITIAL facts')
    implications = entails_profile(facts['profile'],facts['numerical_premises']['HIGH'],
                                   facts['numerical_premises']['owncap'],evidence.facts,evidence.global_owncap)
    return dict(numerical_parent_edges=implications['edges'],
                whole_child_rho=implications['whole_child_rho'],
                source_bound_parent_implications_verified=True,
                execution_observed_by_this_reader=False,
                fresh_parent_fact_joins_verified=False,
                retained_analytic_premises=list(ANALYTIC_PREMISES),
                all_index_conclusion_verified=False)


def load_initial_join(cache,initial_report,evidence,*,work_root=None):
    """No mathematical engine/import is executed; hash/schema/implication checks only."""
    work_root = Path(work_root) if work_root is not None else BASE/'work'
    cache = extended(Path(cache))
    final = source_at(cache,FINAL)
    need(digest(final) == FINAL_SHA, 'Original selected final source graph identity')
    graph = read(final)['files_sha256']
    need(len(graph) == 16576, 'Complete original graph')
    epoch = report_epoch(initial_report,'FRESH_INITIAL_ARITHMETIC_RESULT.json',work_root)
    report = checked_json(epoch,initial_report)
    need(report.get('schema') == 'C5_FRESH_CONDITIONAL_INITIAL_ARITHMETIC_V1'
         and report.get('scope') == 'FRESH_NATIVE_INITIAL_ARITHMETIC_ONLY_PARENT_FACT_JOINS_NOT_DISCHARGED',
         'New conditional INITIAL arithmetic artifact, not a historical native PASS')
    need(report.get('fresh_arithmetic') is True and report.get('fresh_parent_fact_joins_verified') is False
         and report.get('all_index_conclusion_verified') is False
         and report.get('original_final_graph_sha256') == FINAL_SHA, 'Original arithmetic-only declaration')
    jobs = [job for job in INITIAL_JOBS if job.job_id == report['job_id']]
    need(len(jobs) == 1, 'Exact selected INITIAL job identity')
    job = jobs[0]
    inspection = inspect_job(cache,graph,job,include_sources=True)
    pins = inspection['source_files_sha256']
    need(report['source_files_sha256'] == pins, 'Complete original selected INITIAL closure, no source substitution')
    need(report['required_fresh_parent_fact_joins'] == list(job.required_fresh_fact_joins),
         'No removed original parent obligation')
    verify_graph(epoch,pins)
    directory = epoch/job.directory
    output = epoch/job.output_paths[0]
    need(Path(report['native_result_path']).resolve() == output.resolve(), 'Exact selected new INITIAL output')
    native = checked_json(epoch,output,report['native_result_sha256'])
    prepared = checked_json(epoch,epoch/job.prepared)
    controls = control_names((directory/'replay.py').read_text(encoding='utf-8'))
    facts = validate_receipt(job,native,prepared,controls)
    same_initial_candidate(native,prepared['input_sha256'],job.stages,job.expected_status)
    verify_graph(epoch,native['files_sha256'])
    candidate_path = regular_owned(epoch,epoch/job.case_directory/'INPUT.json')
    need(digest(candidate_path) == prepared['input_sha256'], 'Actual fully replayed INPUT candidate identity')
    candidate = checked_json(epoch,candidate_path,prepared['input_sha256'])
    need(candidate['profile'] == facts['profile'] and type(candidate['n']) is int and candidate['n'] == 5
         and candidate['band'] == job.band and type(candidate['stages']) is list
         and len(candidate['stages']) == job.stages, 'Same complete raw candidate/profile and all transition stages')
    if job.sector is not None:
        need(type(candidate['sector']) is int and candidate['sector'] == job.sector, 'Same raw candidate sector')
    cover = candidate['stages'][-1]['cover']
    need(type(cover['total']) is int and cover['total'] == 2592
         and type(cover['panels']) is list and len(cover['panels']) == 100
         and type(cover['active']) is int and type(cover['gap_active']) is int
         and cover['active'] == cover['gap_active'] == facts['final_active'],
         'The same full2592-cell/100-panel final cover and every active gap license')
    exported = dict(facts,input_candidate_path=str(candidate_path),
                    validated_p_export_json_pointer='/stages/'+str(job.stages-1)+'/cover/panels')
    need(report['facts'] == exported and report['negative_controls'] == controls,
         'No altered exported INITIAL fact or control summary')
    capture = epoch/'capture'
    need(Path(report['capture_path']).resolve() == capture.resolve(), 'Exact current INITIAL capture path')
    capture_evidence = verify_capture(epoch,capture,directory,['-B','replay.py',*job.arguments],
        workspace_inputs=True,metadata_pin=report['capture_metadata_sha256'],result=output)
    metadata = checked_json(epoch,capture/'metadata.json',report['capture_metadata_sha256'])
    need(metadata['input_sha256'] == pins, 'Full exact captured INITIAL source closure')
    need(Path(report['report_path']).resolve() == Path(initial_report).resolve(), 'Exact saved INITIAL report self-binding')
    joined = numeric_join(facts,evidence)
    return dict(schema='C5_SOURCE_BOUND_JOINED_INITIAL_V1',
        scope='EXACT_INITIAL_PARENT_IMPLICATIONS_NOT_AUTHENTICATED_EXECUTION',
        job_id=job.job_id,n=5,band=job.band,sector=job.sector,
        input_candidate_path=str(candidate_path),input_candidate_sha256=prepared['input_sha256'],
        profile=facts['profile'],rho_interval=facts['rho_interval'],beta_interval=facts['beta_interval'],
        band_interval=candidate.get('band_interval'),beta_enclosing_interval=candidate.get('beta_enclosing_interval'),
        partition_kind=candidate.get('partition_kind'),stages=job.stages,
        cells_per_stage=2592,validated_closed_p_indices=list(range(100)),
        final_invariants=candidate['final_invariants'],final_cover_sha256=canonical_sha(cover),
        final_active=facts['final_active'],final_gap_active=facts['final_gap_active'],
        final_raw=facts['final_raw'],final_D=facts['final_D'],
        initial_arithmetic_report=dict(path=str(initial_report),sha256=digest(initial_report)),
        native_result=dict(path=str(output),sha256=digest(output)),capture_evidence=capture_evidence,
        parent_evidence=evidence.declaration(),arithmetic_artifact_binding_verified=True,**joined)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache',type=Path,required=True)
    parser.add_argument('--initial',type=Path,required=True)
    parser.add_argument('--support',type=Path,required=True)
    parser.add_argument('--high',type=Path,required=True)
    parser.add_argument('--owncaps',type=Path,required=True)
    args = parser.parse_args()
    parents = load_parent_evidence(args.cache,args.support,args.high,args.owncaps)
    print(json.dumps(load_initial_join(args.cache,args.initial,parents),indent=2),flush=True)


if __name__ == '__main__':
    main()
