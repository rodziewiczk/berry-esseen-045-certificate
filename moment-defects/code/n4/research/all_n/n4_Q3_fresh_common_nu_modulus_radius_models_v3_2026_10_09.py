"""NEW compatibility wrapper for unchanged exact-LCM radius production.

Frozen193 source remains untouched. Its PRODUCTION compiler and optional
compact curvature helper already pass the correct scale to every ceil.
Only its DORMANT scalar regressions omitted scale in four curvature.ceil
calls. This new module uses the unchanged193 production math DIRECTLY
and supplies a NEW independently copied29-test suite with explicitSCALE.
The old failing self_tests function is NEVER invoked here.

compute_verified_modulus_radius_models(table,eta_cells,guard) calls the
fresh exact193 compiler once on the SAME DIRECT correct A1V2/RAW object.
It copies only top-level diagnostic/source metadata and appends this
wrapper/193 source-integrity hashes. Every physical A,S, normalized
coefficient, full price tuple, active cell, selection, sign signal and
response motion bound remains unchanged. Source pins are not proof.
No CF/A1/Gamma/CDF producer, numeric receipt or old global is called or
mutated. Fast norm and pure compact-curvature APIs are unchanged aliases.
All DIRECT-fresh mathematical prerequisites and closed eta/equality
scopes of10e/193 remain. No CDF or global root/C4 acceptance is added.

Pure Fraction/int definitions, no import-time tests, CLI or file writes.
Dormant exact29 scalar tests are not a real radius-table producer. No
runtime or performance theorem is inferred from the arithmetic rewrite.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from math import lcm
from pathlib import Path

import n4_Q3_fresh_common_nu_modulus_radius_models_v2_2026_10_09 as previous

price, integer, curvature = previous.price, previous.integer, previous.curvature
SCALE, require = previous.SCALE, previous.require
PREVIOUS_PIN = "19338724e73a17dac484ec68c3e76ea43682e4c06277be581caabc0060f83991"
actual_response_norm_uppers = previous.actual_response_norm_uppers
compact_refined_H_curvature = previous.compact_refined_H_curvature
nonnegative_models_for_closed_cell = previous.nonnegative_models_for_closed_cell
as_transfer_models = previous.as_transfer_models
exact_LCM_coefficients = previous.exact_LCM_coefficients
LCM_endpoint_numerator = previous.LCM_endpoint_numerator
exact_LCM_midpoint_choice = previous.exact_LCM_midpoint_choice
same_radius_math_except_new_source_pins = previous.same_radius_math_except_new_source_pins


def source_drift_check():
    previous.source_drift_check()
    require(hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == PREVIOUS_PIN,
            "Frozen unchanged LCM PRODUCTION math, not a numeric proof input")


def compute_verified_modulus_radius_models(table, eta_cells, guard):
    """DIRECT unchanged193 fresh math; ONLY new integrity metadata appended."""
    require(callable(guard), "Externally coordinated cooperative guard")
    guard()
    source_drift_check()
    result = dict(previous.compute_verified_modulus_radius_models(table, eta_cells, guard))
    metadata = dict(result["metadata"])
    pins = dict(metadata["source_pins_integrity_only"])
    for path in (Path(__file__), Path(previous.__file__)):
        pin = hashlib.sha256(path.read_bytes()).hexdigest()
        require(path.name not in pins or pins[path.name] == pin, "Consistent source integrity closure")
        pins[path.name] = pin
    metadata["source_pins_integrity_only"] = pins
    result["metadata"] = metadata
    source_drift_check()
    guard()
    return result


def self_tests():
    """DORMANT exact LCM equivalence and monotone curvature scalars ONLY."""
    checks = 0
    candidates = [{"A": F(1, 3), "S_upper_int": -SCALE},
                  {"A": F(1, 7), "S_upper_int": SCALE // 2},
                  {"A": F(0), "S_upper_int": SCALE // 10},
                  {"A": F(1, 3), "S_upper_int": -SCALE}]
    D = lcm(SCALE, 3, 7)
    for candidate in candidates:
        Ai, Si = exact_LCM_coefficients(candidate["A"], candidate["S_upper_int"], D)
        candidate.update({"_A_LCM_int": Ai, "_S_LCM_factor": Si})
    for eta in (F(0), F(1, 10), F(1, 3), F(2, 3), F(1)):
        require(exact_LCM_midpoint_choice(candidates, eta)
                == price.exact_midpoint_choice(candidates, eta, D), "Identical ordered midpoint ties/values")
        checks += 1
        for candidate in candidates:
            numerator = LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], eta)
            physical = candidate["A"] + F(candidate["S_upper_int"], SCALE) * eta
            require(F(numerator, D * eta.denominator) == physical
                    and (numerator < 0) == (physical < 0) and (numerator >= 0) == (physical >= 0),
                    "EXACT Fraction endpoint equality and signs including0 and negativeS")
            checks += 1
    L, U = F(1, 10), F(4, 5)
    old_eligible = [candidate for candidate in candidates if min(
        candidate["A"] + F(candidate["S_upper_int"], SCALE) * L,
        candidate["A"] + F(candidate["S_upper_int"], SCALE) * U) >= 0]
    new_eligible = [candidate for candidate in candidates if min(
        LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], L),
        LCM_endpoint_numerator(candidate["_A_LCM_int"], candidate["_S_LCM_factor"], U)) >= 0]
    require(old_eligible == new_eligible, "Identical candidate identities/order, no relaxed endpoint")
    checks += 1
    for old_upper, refined_upper in ((F(1), F(1)), (F(1), F(1, 2)), (F(1, 3), F(1, 4))):
        a, fill = F(1, 5), F(3, 512)
        old_p, new_p = min(F(1), a + old_upper + fill), min(F(1), a + refined_upper + fill)
        old_B, new_B = 6 * old_p ** 4, 6 * new_p ** 4
        old_Bi, new_Bi = curvature.ceil_scaled(old_B, SCALE), curvature.ceil_scaled(new_B, SCALE)
        old_Hi = curvature.ceil_scaled(F(1, 64) * (F(old_Bi, SCALE) + F(1, 4)) / 16, SCALE)
        new_Hi = curvature.ceil_scaled(F(1, 64) * (F(new_Bi, SCALE) + F(1, 4)) / 16, SCALE)
        require(new_p <= old_p and new_Bi <= old_Bi and new_Hi <= old_Hi,
                "Complete radius MAX/MIN fill and BOTH outward ceilings are monotone")
        checks += 1
    return {"status": "TINY_LCM_RADIUS_EQUIVALENCE_AND_CURVATURE_ALGEBRA_ONLY", "exact_checks": checks,
        "CF_cache_A1_Gamma_real_radius_compiler_CDF_or_global_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}


