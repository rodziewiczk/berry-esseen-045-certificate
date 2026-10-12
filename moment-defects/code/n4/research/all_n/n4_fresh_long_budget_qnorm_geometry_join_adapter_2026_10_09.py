"""NEW resource-only adapter for a DIRECT own-request A1/Gamma/V6 join.

This preserves frozen6ad's complete mathematical pipeline and result
shape: SAME exact request/high/cut, SAME original correct A1V2, SAME
exact Gamma compiler, SAME V5 arithmetic in the NEW V6 consumer, SAME
all16 closed eta/H58/BOTH reflection/tail scope, ONE quad/H reserve,
and SAME pure complete low/high postconsumer. No older file, producer,
receipt, global or mathematical bound is changed or monkeypatched.

The authorized resource correction is TOTAL complete optimized low
180s instead of60s. A1 and Gamma EACH still get their own <=60s phase
guard. V6 gets at most the remaining total180, including input checks,
fresh radius compiler, every complete CDF row and output integrity checks.
The adapter finally checks total180 AFTER full join/compaction. Outer
256MiB is unchanged. Actual peak is checked here as well as by the
caller/unchanged analytic builders. The caller must have DIRECTLY
completed ALL own-request HIGH proofs BEFORE cache/A1 under the old
64MiB high limit; no high proof is made here and none is serialized input.

IMPORTANT integration: the caller's OPTIMIZED remaining-budget supplier
must cap180, NOT the old MASTER/6ad supplier capped60. This adapter has
its OWN budget clamp and never calls old6ad._complete_join_from_pair or
its public128MiB parent wrapper. HIGH/cheap/cache retain old60 clamps
outside this module. A type/schema/status/hash cannot establish fresh
analytic provenance. The required proof pair/cache are DIRECT in-memory
outputs on SAME scopes, not old numeric JSON or retained runtime prefixes.

Public complete_geometry_join_from_pair(pair,cache,guard,budget=180)
returns (complete_record,diagnostic_resources). Alias _complete_join_from_pair
supports the new whole-root adapter. Empty classes use the identical
STRICT-rho square criterion INCLUDING equality; high cut0 covers eta0
and all actual eta without inventing a low interval. Positive cut uses
ENTIRE[0,own-cut], and every UNKNOWN16-cell/failure face remains. Raw
budget-stage limits are explicit metadata, not analytic assumptions.
Compaction ONLY follows the complete DIRECT mathematical consumer.

Standing scope and outside hypotheses are exactly6ad/V5: standardized
iid original P, canonical declaredBOX/eta, |X|<=17/4, actualrho<46/25,
closed-CDF Prawitz/original-P bridge and own complete Cantelli/SV high
route. No finite-atom/density/additionalM4 hypothesis. This one geometry
never proves entireROOT/C4. The prior actual total60 timeout produced NO
final complete-root receipt; it is not a numerical or mathematical rejection.

No producer CLI/file writes/import-time jobs. Dormant pure budget/scope
checks only until explicitly authorized. Source pins are integrity only.
No genuine CDF equivalence/result is inferred merely from tiny tests.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_optimized_qnorm_parent_four_child_coordinator_2026_10_09 as previous
import n4_fresh_signed_A1_CDF_cell_consumer_v6_2026_10_09 as consumer

full, geometry, A1, gamma_compiler = previous.full, previous.geometry, previous.A1, previous.gamma_compiler
resources, quadrature, require = previous.resources, previous.quadrature, previous.require
SCALE, TARGET, N, H_STEP, ETA_CELLS = previous.SCALE, previous.TARGET, previous.N, previous.H_STEP, previous.ETA_CELLS
TIME_LIMIT, PHASE_LIMIT, MEMORY_LIMIT, HIGH_MEMORY_LIMIT = 180, 60, 256 * 1024 * 1024, previous.HIGH_MEMORY_LIMIT
PREVIOUS_PIN = "6ad87c2f8dc3bca497b6ba8d81afc0932bc059175299c09410ee83d934556cdd"
CONSUMER_PIN = "5a74e8b3849e077fb2316d6b46ec14e0d8aaf1ba3d7d22452a12c0399d386566"
_checked_high_pair = previous._checked_high_pair
compact_complete_low_result = previous.compact_complete_low_result


def source_drift_check():
    previous.source_drift_check()
    consumer.source_drift_check()
    for module, pin in ((previous, PREVIOUS_PIN), (consumer, CONSUMER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen unchanged mathematics/resource-only source integrity")
    require(SCALE == consumer.SCALE and TARGET == consumer.TARGET and consumer.TIME_LIMIT == TIME_LIMIT
            and consumer.MEMORY_LIMIT == MEMORY_LIMIT and HIGH_MEMORY_LIMIT == 64 * 1024 * 1024,
            "Resource changes ONLY total/postconsumer180; SAME256/HIGH64 and math units")


def dependency_pins():
    pins = previous.dependency_pins()
    for name, pin in consumer.dependency_pins().items():
        require(name not in pins or pins[name] == pin, "Consistent complete mathematical source closure")
        pins[name] = pin
    path = Path(__file__)
    require(path.name not in pins, "Unique new long-budget adapter")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def remaining_pair_budget(budget):
    """OWN clamp180; do not delegate to old6ad/full clamp60."""
    value = budget() if callable(budget) else budget
    require(type(value) in (int, float, F) and value > 0, "Positive caller optimized remaining budget")
    return min(TIME_LIMIT, value)


def remaining_phase_budget(budget):
    return min(PHASE_LIMIT, remaining_pair_budget(budget))


def complete_geometry_join_from_pair(pair, cache, guard, budget=TIME_LIMIT):
    """DIRECT own-scope full low/high math, TOTAL180/A1<=60/Gamma<=60."""
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
        require(time.monotonic() - low_started < low_limit, "COMPLETE A1+Gamma+V6 low join<=180s")
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
            require(time.monotonic() - phase_started < limit, name + " SAME original phase<=60s")
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
            "Gamma_maximum": PHASE_LIMIT, "V6_postconsumer_maximum": TIME_LIMIT,
            "TOTAL_A1_Gamma_V6_join_maximum": TIME_LIMIT}}
    resource = {"complete_A1_Gamma_V6_low_elapsed_seconds_diagnostic": time.monotonic() - low_started,
        "time_limit_seconds": low_limit, "A1_phase": A1_resources, "Gamma_phase": Gamma_resources,
        "V6_postconsumer": low["resources"]}
    source_drift_check()
    require(dependency_pins() == initial_pins, "Complete frozen math/resource source closure unchanged")
    low_guard()
    del table, gamma, low
    guard()
    return record, resource


_complete_join_from_pair = complete_geometry_join_from_pair
complete_fresh_geometry_join_from_pair = complete_geometry_join_from_pair


def self_tests():
    """Dormant PURE budget/high scope only; no cache/CF/A1/Gamma/V6 producer."""
    source_drift_check()
    for value in (F(1, 10), F(60), F(90), F(180), F(240)):
        require(remaining_pair_budget(value) == min(F(180), value)
                and remaining_pair_budget(lambda: value) == min(F(180), value), "Optimized scalar/callable cap180")
        require(remaining_phase_budget(value) == min(F(60), value), "Each unchanged A1/Gamma cap60")
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
