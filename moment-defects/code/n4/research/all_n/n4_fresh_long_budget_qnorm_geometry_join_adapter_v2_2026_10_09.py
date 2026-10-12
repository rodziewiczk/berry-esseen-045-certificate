"""NEW robust-budget adapter V2; SAME complete frozen e57/6ad mathematics.

This NEW mechanical clone changes only resource budgets/bindings and
source-integrity diagnostics: TOTAL complete optimized low600s, A1 and
Gamma EACH at most180s, NEW V7 postconsumer at most remaining TOTAL600.
The actual independent I254 replay exhausted its remaining TOTAL180
without MATCH; neither that failure nor longer deadlines prove a bound
or guarantee performance. All older sources/receipts stay untouched.

SAME DIRECT own-request high pair, original correct A1V2, exact Gamma,
V5/V6 arithmetic in V7, all16 closed eta/H58/both-reflection/tail scope,
ONE quad/H reserves, complete low/high postconsumer and compaction are
unchanged. MEMORY_LIMIT256MiB and caller HIGH64-before-cache remain.
HIGH/cheap/cache retain their old60 clamps OUTSIDE this module.
The caller OPTIMIZED budget supplier MUST allow600; this module never
calls the old60/180 pair producer, parent128 wrapper or old CDF evaluate.

Public complete_geometry_join_from_pair(pair,cache,guard,budget=600)
returns SAME (complete_record,diagnostic_resources). Empty strict-cap
classes include equality; cut0 HIGH covers eta0; positive cuts prove
ENTIRE[0,own-cut]. Every UNKNOWN cell/failure remains. No coefficient
min, eta mask, extra moment/atom/density premise, source/hash/status or
JSON proof truth is introduced. Fresh pair/cache provenance is a DIRECT
mathematical precondition. Uniform physical scope is exactly e57/6ad:
canonical iid original P, support17/4, actualrho<46/25, closed Prawitz
bridge and own Cantelli/SV HIGH. One geometry never proves entire C4.

Frozen e57 is imported ONLY for source integrity; no old producer is
called. TOTAL600 is checked after COMPLETE mathematical validation and
compaction. No producer CLI, writes, monkeypatch or import jobs. Pure
dormant budget tests only until explicit separate authorization.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_optimized_qnorm_parent_four_child_coordinator_2026_10_09 as previous
import n4_fresh_signed_A1_CDF_cell_consumer_v7_2026_10_09 as consumer
import n4_fresh_long_budget_qnorm_geometry_join_adapter_2026_10_09 as frozen_adapter

full, geometry, A1, gamma_compiler = previous.full, previous.geometry, previous.A1, previous.gamma_compiler
resources, quadrature, require = previous.resources, previous.quadrature, previous.require
SCALE, TARGET, N, H_STEP, ETA_CELLS = previous.SCALE, previous.TARGET, previous.N, previous.H_STEP, previous.ETA_CELLS
TIME_LIMIT, PHASE_LIMIT, MEMORY_LIMIT, HIGH_MEMORY_LIMIT = 600, 180, 256 * 1024 * 1024, previous.HIGH_MEMORY_LIMIT
PREVIOUS_PIN = "6ad87c2f8dc3bca497b6ba8d81afc0932bc059175299c09410ee83d934556cdd"
CONSUMER_PIN = "2ef250675761cd0bbeb7925c73b7ec3239dcdeb5b17fc35b67c6a95e341b2f1d"
FROZEN_ADAPTER_PIN = "e57eb5aa3143f87219551bca202651efec9031538da9368ed40bb307c80ead4f"
_checked_high_pair = previous._checked_high_pair
compact_complete_low_result = previous.compact_complete_low_result


def source_drift_check():
    previous.source_drift_check()
    consumer.source_drift_check()
    frozen_adapter.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (consumer, CONSUMER_PIN), (frozen_adapter, FROZEN_ADAPTER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen unchanged mathematics/resource-only source integrity")
    require(SCALE == consumer.SCALE and TARGET == consumer.TARGET and consumer.TIME_LIMIT == TIME_LIMIT
            and consumer.MEMORY_LIMIT == MEMORY_LIMIT and HIGH_MEMORY_LIMIT == 64 * 1024 * 1024,
            "Resource changes ONLY total/postconsumer600/phases180; SAME256/HIGH64 and math units")


def dependency_pins():
    pins = previous.dependency_pins()
    for name, pin in consumer.dependency_pins().items():
        require(name not in pins or pins[name] == pin, "Consistent complete mathematical source closure")
        pins[name] = pin
    origin = Path(frozen_adapter.__file__)
    origin_pin = hashlib.sha256(origin.read_bytes()).hexdigest()
    require(origin.name not in pins or pins[origin.name] == origin_pin, "Frozen origin consistent integrity only")
    pins[origin.name] = origin_pin
    path = Path(__file__)
    require(path.name not in pins, "Unique new long-budget adapter")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def remaining_pair_budget(budget):
    """OWN clamp600; do not delegate to old60/180 optimized supplier."""
    value = budget() if callable(budget) else budget
    require(type(value) in (int, float, F) and value > 0, "Positive caller optimized remaining budget")
    return min(TIME_LIMIT, value)


def remaining_phase_budget(budget):
    return min(PHASE_LIMIT, remaining_pair_budget(budget))


def complete_geometry_join_from_pair(pair, cache, guard, budget=TIME_LIMIT):
    """DIRECT own-scope full low/high math, TOTAL600/A1<=180/Gamma<=180."""
    require(callable(guard) and type(pair) in (tuple, list) and len(pair) == 2,
            "Caller outer guard and SAME DIRECT high proof pair")
    request, high = pair
    guard()
    source_drift_check()
    initial_pins = dependency_pins()
    _checked_high_pair(request, high)
    if request["proved_root_empty"]:
        return {"request": request, "kind": "EXACT_EMPTY_BY_STRICT_RHO_CAP_INCLUDING_EQUALITY",
            "whole_geometry_all_actual_eta_closed": True, "whole_geometry_score_upper_exact": F(0),
            "own_joint_eta_cut_exact": None, "fresh_complete_low_eta_result": None}, None
    cut = high["joint_eta_cut_exact"]
    if cut == 0:
        return {"request": request, "kind": "ALL_ACTUAL_ETA_CLOSED_HIGH_ROUTE_INCLUDING_ETA0",
            "whole_geometry_all_actual_eta_closed": True,
            "whole_geometry_score_upper_exact": high["joint_high_eta_score_at_closed_cut_exact"],
            "own_joint_eta_cut_exact": cut, "fresh_complete_low_eta_result": None}, None
    quadrature.validate_preverified_fresh_cache(cache, N, H_STEP)
    low_started, low_limit = time.monotonic(), remaining_pair_budget(budget)

    def low_guard():
        require(time.monotonic() - low_started < low_limit, "COMPLETE A1+Gamma+V7 low join<=600s")
        peak = resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Unchanged optimized low/outer256MiB")
        guard()

    def low_remaining():
        value = min(remaining_pair_budget(budget), low_limit - (time.monotonic() - low_started))
        require(value > 0, "No partial optimized low proof after total expiry")
        return value

    def run_phase(name, operation):
        phase_started, limit = time.monotonic(), remaining_phase_budget(low_remaining)

        def phase_guard():
            require(time.monotonic() - phase_started < limit, name + " explicit complete phase<=180s")
            low_guard()

        phase_guard()
        value = operation(phase_guard)
        phase_guard()
        return value, {"name": name, "elapsed_seconds_diagnostic": time.monotonic() - phase_started,
                       "time_limit_seconds": limit}

    eta_interval = F(0), cut
    table, A1_resources = run_phase("A1", lambda stage_guard:
        A1.fresh_generic_common_A1_response_table(request["closed_rectangle"], cache, stage_guard))
    eta_cells = consumer.fixed_eta_cells(eta_interval)
    gamma, Gamma_resources = run_phase("Gamma", lambda stage_guard:
        gamma_compiler.compute_verified_gamma_models(table, eta_cells, stage_guard))
    low_guard()
    low = consumer.evaluate_fresh_signed_A1_CDF(table, gamma, eta_interval,
        rectangle=request["closed_rectangle"], N=N, H_step=H_STEP, use_two_disk=True,
        modulus_radius_mode="five_budget", time_limit_seconds=low_remaining())
    low_guard()
    require(low["closed_rectangle"] == request["closed_rectangle"] and low["closed_eta_cover"] == eta_interval,
            "SAME entire geometry and OWN complete low eta interval")
    joined = geometry.previous.previous.exact_complete_join_summary(high, low, cut)
    closed = joined["conditional_entire_declared_child_all_actual_eta_closed"]
    summary = {key: value for key, value in joined.items() if key not in (
        "conditional_entire_declared_child_all_actual_eta_closed",
        "whole_parent_200_or_full_root_or_unrestricted_C4_proved")}
    summary["conditional_entire_declared_geometry_all_actual_eta_closed"] = closed
    summary["entire_260_root_or_unrestricted_C4_proved"] = False
    record = {"request": request, "kind": "COMPLETE_OWN_LOW_HIGH_JOIN" if closed else "UNKNOWN_LOW_CELLS_RETAINED",
        "whole_geometry_all_actual_eta_closed": closed,
        "whole_geometry_score_upper_exact": joined["whole_geometry_score_upper_exact"],
        "own_joint_eta_cut_exact": cut, "complete_low_high_join_summary": summary,
        "fresh_complete_low_eta_result": compact_complete_low_result(low),
        "complete_low_stage_budget_seconds": {"A1_maximum": PHASE_LIMIT,
            "Gamma_maximum": PHASE_LIMIT, "V7_postconsumer_maximum": TIME_LIMIT,
            "TOTAL_A1_Gamma_V7_join_maximum": TIME_LIMIT}}
    resource = {"complete_A1_Gamma_V7_low_elapsed_seconds_diagnostic": time.monotonic() - low_started,
        "time_limit_seconds": low_limit, "A1_phase": A1_resources, "Gamma_phase": Gamma_resources,
        "V7_postconsumer": low["resources"]}
    source_drift_check()
    require(dependency_pins() == initial_pins, "Complete frozen math/resource source closure unchanged")
    low_guard()
    del table, gamma, low
    guard()
    return record, resource


_complete_join_from_pair = complete_geometry_join_from_pair
complete_fresh_geometry_join_from_pair = complete_geometry_join_from_pair


def self_tests():
    """Dormant PURE budget/high scope only; no cache/CF/A1/Gamma/V7 producer."""
    source_drift_check()
    for value in (F(1, 10), F(60), F(180), F(600), F(720)):
        require(remaining_pair_budget(value) == min(F(600), value)
                and remaining_pair_budget(lambda: value) == min(F(600), value), "Optimized scalar/callable cap600")
        require(remaining_phase_budget(value) == min(F(180), value), "Each explicit A1/Gamma cap180")
    rejected = False
    try:
        remaining_pair_budget(F(0))
    except RuntimeError:
        rejected = True
    require(rejected, "Expired budget is not a partial proof")
    # SAME five audited empty/cut0/order checks, definitions/scalars only.
    original = previous.self_tests()
    return {"status": "TINY_LONG_BUDGET_ADAPTER_GEOMETRY_ONLY", "exact_checks": original["exact_checks"] + 11,
        "old60_pair_or_V5_CDF_evaluate_called": False,
        "cache_CF_A1_Gamma_radius_CDF_or_root_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}


