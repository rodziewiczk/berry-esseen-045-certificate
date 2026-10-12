"""NEW compatibility adapter for the correct fresh generic A1 table.

DIRECT call to frozen cde754's fresh_generic_common_A1_response_table
builds every mathematical bound. This adapter then adds ONLY the exact
RAW-cache schema alias required by the preserved base cached-radius API:
    nom_mod_cache['cell_arrays_raw_r_not_normalized'] = True.

The existing cache is mathematically RAW |r_nom| over closed y cells,
already containing HG tail and y half-cell mesh ONCE, as proved by that
DIRECT audited producer. It is NOT q^3-normalized, a |g| cache, or an
r_c derivative cache. No r_c arrays/derivative flags are supplied, so
the stricter derivative-cache-v2 consumers are NOT made compatible.
Flags, schema validation, source pins or synthetic tests alone cannot
establish any cached bound; no numeric JSON importer is supplied.

All coefficient/response/geometry/price/CF/raw/normalized/modulus numbers
remain unchanged. Only schema/diagnostic metadata are appended. No older
source/receipt is edited. No Gamma/radius/CDF producer is called outside
the one DIRECT cde builder, and this module adds no eta decision, physical
reserve, price model, accepted CDF or unrestricted C4 claim.

API fresh_generic_common_A1_response_table(rectangle,cache,guard) has the
same mathematical prerequisites as cde's API. Source-only until explicit
authorization. Dormant tiny alias/interface tests invoke no CF/cache/A1
producer and write no files. No producer/replay CLI or import-time run.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path

import n4_Q3_fresh_generic_common_A1_response_table_2026_10_09 as previous

SCALE, TARGET, require = previous.SCALE, previous.TARGET, previous.require
PREVIOUS_PIN = "cde7549338e1e32f5398f68416b9b1428c3129f556d999b47cccb218e85a65ad"


def source_drift_check():
    previous.source_drift_check()
    require(hashlib.sha256(Path(previous.__file__).read_bytes()).hexdigest() == PREVIOUS_PIN,
            "Frozen correct A1 producer integrity, not proof from a source pin")


def add_RAW_cache_compatibility_alias(table):
    """Schema-only operation under DIRECT fresh cde cache-bound premises.

    This pure helper also permits tiny synthetic schema tests, which are
    NOT mathematical response/cache certificates. Numeric arrays are not
    copied, clipped, normalized, rounded or otherwise mutated.
    """
    require(type(table) is dict and type(table.get("scale")) is int and table["scale"] == SCALE,
            "Declared exact table scale")
    N = table.get("N")
    require(type(N) is int and N > 0, "Positive integer table frequency count")
    cache = table.get("nom_mod_cache")
    require(type(cache) is dict and type(cache.get("scale")) is int and cache["scale"] == SCALE
            and type(cache.get("N")) is int and cache["N"] == N,
            "Same directly fresh nominal RAW cache scale/N")
    require(type(cache.get("R")) is F and cache["R"] == previous.RADIUS
            and type(cache.get("y_step")) is F and cache["y_step"] == previous.Y_STEP
            and type(cache.get("HG_degree")) is int and cache["HG_degree"] == previous.DEGREE,
            "Exact RAW response domain/grid/HG degree")
    require(cache.get("includes_HG_tail_and_y_mesh") is True
            and cache.get("cell_arrays_are_RAW_r_modulus_not_q_cubic_normalized") is True,
            "DIRECT cde's RAW closed-cell norm cache, tails/mesh already included ONCE")
    require("cell_arrays_raw_r_not_normalized" not in cache
            or cache["cell_arrays_raw_r_not_normalized"] is True,
            "An existing conflicting alias is rejected, never silently overwritten")
    require(cache.get("nominal_root_data") == table.get("nominal_root_data")
            and type(cache.get("nominal_root_data")) is dict,
            "Same exact nominal geometry labels, not actual-box substitution")
    grid = cache.get("q_grid")
    require(type(grid) in (tuple, list) and len(grid) == N
            and all(type(q) is F and q == F(3 * (2 * j + 1), 2 * N) for j, q in enumerate(grid)),
            "Complete same physical q grid")
    for name in ("a", "b"):
        values = cache.get(name + "_cell_modulus_upper_int")
        require(type(values) in (tuple, list) and len(values) == previous.Y_NODES
                and all(type(row) in (tuple, list) and len(row) == N
                        and all(type(value) is int and value >= 0 for value in row) for row in values),
                "Every273xN RAW signed-tag norm array, never normalized/mutated")
    cache["cell_arrays_raw_r_not_normalized"] = True
    return table


def fresh_generic_common_A1_response_table(rectangle, cache, guard):
    """One DIRECT correct builder, then ONLY the strict base-cache alias."""
    require(callable(guard), "Caller-owned cooperative guard")
    guard()
    source_drift_check()
    table = previous.fresh_generic_common_A1_response_table(rectangle, cache, guard)
    add_RAW_cache_compatibility_alias(table)
    table["metadata"]["generic_A1_RAW_cache_compatibility"] = {
        "base_cache_exact_alias": "cell_arrays_raw_r_not_normalized",
        "RAW_r_norm_arrays_already_include_HG_tail_and_y_mesh_once": True,
        "q_cubic_normalized_response_claim": False,
        "r_c_contact_derivative_cache_provided": False,
        "numerical_bounds_or_prices_changed": False,
        "Gamma_radius_or_CDF_producer_called_by_adapter": False}
    table["metadata"]["generic_A1_compatibility_source_pins_integrity_only"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), Path(previous.__file__))}
    source_drift_check()
    guard()
    return table


def self_tests():
    """Dormant small synthetic schema checks only; no CF/cache/A1 producer."""
    nominal = {"w": F(1), "beta": F(0)}
    a, b = [[3] for _ in range(previous.Y_NODES)], [[7] for _ in range(previous.Y_NODES)]
    cache = {"scale": SCALE, "N": 1, "R": previous.RADIUS, "y_step": previous.Y_STEP,
        "HG_degree": previous.DEGREE, "q_grid": (F(3, 2),), "nominal_root_data": nominal,
        "a_cell_modulus_upper_int": a, "b_cell_modulus_upper_int": b,
        "includes_HG_tail_and_y_mesh": True,
        "cell_arrays_are_RAW_r_modulus_not_q_cubic_normalized": True}
    table = {"scale": SCALE, "N": 1, "nominal_root_data": nominal, "nom_mod_cache": cache}
    old_keys = set(cache)
    result = add_RAW_cache_compatibility_alias(table)
    require(result is table and table["nom_mod_cache"] is cache
            and cache["a_cell_modulus_upper_int"] is a and cache["b_cell_modulus_upper_int"] is b
            and a == [[3] for _ in range(previous.Y_NODES)] and b == [[7] for _ in range(previous.Y_NODES)],
            "ONLY schema changed; every existing RAW integer and identity retained")
    require(set(cache) == old_keys | {"cell_arrays_raw_r_not_normalized"}
            and cache["cell_arrays_raw_r_not_normalized"] is True,
            "Exact strict base-consumer alias supplied")
    require(not any("derivative" in key for key in cache), "No fictional r_c derivative cache flag")
    checks = 3
    for bad in (False, 1, "True"):
        changed = dict(cache, cell_arrays_raw_r_not_normalized=bad)
        rejected = False
        try:
            add_RAW_cache_compatibility_alias(dict(table, nom_mod_cache=changed))
        except RuntimeError:
            rejected = True
        require(rejected, "Conflicting/nonboolean strict alias rejected")
        checks += 1
    require(add_RAW_cache_compatibility_alias(table) is table, "Correct alias is idempotent")
    checks += 1
    return {"status": "TINY_GENERIC_A1_RAW_SCHEMA_COMPATIBILITY_TESTS_ONLY", "exact_checks": checks,
        "synthetic_schema_is_a_mathematical_response_certificate": False,
        "CF_cache_A1_Gamma_radius_or_CDF_producer_called": False,
        "source_or_receipt_files_written": False, "unrestricted_C4_proved": False}
