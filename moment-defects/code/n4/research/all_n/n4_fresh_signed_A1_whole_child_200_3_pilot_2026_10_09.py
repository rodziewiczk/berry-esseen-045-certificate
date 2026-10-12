"""One fresh WHOLE-box signed A1 table pilot, NOT a CDF certificate.

The domain is the complete closed child3 of root class200, obtained by
the exact original root construction and the fixed four-child cover.
DIRECT audited fresh quadrature and compatibility-v2 A1 builders compute
all256 frequencies, all58 raw-H nodes, BOTH genuine orientations, and
both273 closed magnitude cells. No numerical JSON is a proof input.

The new exclusive projected receipt retains ALL signed A1/center rows,
all frequency data, whole/nominal geometry, and mathematical metadata.
The large auxiliary RAW response cache is represented ONLY by its
integrity digest; that digest does not establish any response bound.
Read-only replay recomputes everything directly and compares every
nonresource field of this projection. No Gamma, eta acceptance, physical
reserve, CDF, whole-root conclusion or unrestricted C4 is asserted.

One externally coordinated sequential60s/128MiB stdlib job. Default CLI
does only dormant exact geometry/interface tests; older files unchanged.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_fresh_generic_common_A1_response_table_v2_2026_10_09 as A1
import n4_fresh_Cantelli_linked_normalization_full_root_2026_10_09 as full

INDEX, CHILD = 200, 3
TIME_LIMIT, MEMORY_LIMIT = 60, 128 * 1024 * 1024
OUTPUT_LIMIT = 4 * 1024 * 1024
SCALE, require = A1.SCALE, A1.require
A1_PIN = "0a5cf384dd991e8c9f30bc653dc3b180fe0fa8b23d14808890e64b1d7b173a7f"
FULL_PIN = "e16285e11f10c144d5278accab1bf8468260543e0243c1ab6ffd53caeded6dbd"


def source_drift_check():
    A1.source_drift_check()
    full.source_drift_check()
    for module, pin in ((A1, A1_PIN), (full, FULL_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen mathematical producer integrity, not proof from a hash")


def dependency_pins():
    pins = full.dependency_pins()
    for module in (A1, A1.previous, A1.previous.HG):
        path = Path(module.__file__)
        pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    path = Path(__file__)
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def fresh_entire_request():
    parent = full.root.fresh_root_requests()[2][INDEX]
    rectangle = full.closed_four_children(parent["closed_rectangle"])[CHILD]
    require(rectangle == (F(71221, 84640), F(9089, 10580), F(11, 40), F(3, 10)),
            "Entire chosen closed root child, not a point or selected subset")
    return full.fresh_rectangle_request(rectangle, INDEX, (CHILD,))


def RAW_cache_digest(cache, guard):
    """Integrity ONLY; replay does not accept this as a numerical premise."""
    digest = hashlib.sha256()
    for name in ("a", "b"):
        digest.update(name.encode("ascii"))
        for row in cache[name + "_cell_modulus_upper_int"]:
            guard()
            digest.update(str(tuple(row)).encode("ascii"))
    return digest.hexdigest()


def compute_fresh_pilot():
    started = time.monotonic()
    source_drift_check()
    initial = dependency_pins()

    def guard():
        require(time.monotonic() - started < TIME_LIMIT, "Entire A1 pilot60s timer")
        peak = full.resources.peak_bytes()
        require(peak is not None and peak <= MEMORY_LIMIT, "Observed A1 pilot128MiB cap")

    guard()
    request = fresh_entire_request()
    cache = full.quadrature.build_fresh_quadrature_cache()
    table = A1.fresh_generic_common_A1_response_table(request["closed_rectangle"], cache, guard)
    require(len(table["frequency_data"]) == cache.N == 256
            and len(table["rows"]) == 2 * len(cache.H_grid) == 116
            and {(r["orientation"], r["H"]) for r in table["rows"]}
                == {(o, H) for H in cache.H_grid for o in (1, -1)},
            "Complete same-q/H/orientation scope after DIRECT producer")
    for row in table["rows"]:
        require(len(row["positive_cell_upper_int"]) == len(row["negative_cell_upper_int"]) == 273,
                "Every closed magnitude cell for each physical tag")
    abs_cap = sum(4 * F(item["kernel_modulus_upper_int"], SCALE)
                  * F(item["g_actual_modulus_upper_int"], SCALE) ** 3 * item["q"] ** 3 / 6
                  for item in table["frequency_data"])
    scalar_rows = [{"orientation": row["orientation"], "H": row["H"],
        "signed_A1_all_y_upper_exact": F(max(row["positive_cell_upper_int"]
                                             + row["negative_cell_upper_int"]), SCALE)}
        for row in table["rows"]]
    raw_digest = RAW_cache_digest(table["nom_mod_cache"], guard)
    # The auxiliary cache is deliberately NOT a future numerical proof input.
    projection = {key: table[key] for key in
                  ("scale", "N", "box_geometry", "nominal_root_data", "rows", "frequency_data", "metadata")}
    source_drift_check()
    final = dependency_pins()
    require(final == initial, "Frozen mathematical sources unchanged throughout fresh computation")
    guard()
    return {"status": "FRESH_ENTIRE_CLOSED_CHILD_SIGNED_A1_TABLE_ONLY",
        "root_class": INDEX, "fixed_geometry_path": (CHILD,), "fresh_request": request,
        "table_projection": projection,
        "auxiliary_RAW_cache_sha256_integrity_only": raw_digest,
        "diagnostics_not_CDF_bounds": {"whole_box_cubic_ABS_A1_cap_exact": abs_cap,
            "all_H_orientation_signed_A1_y_supremum_uppers": scalar_rows},
        "conclusions": {"fresh_signed_A1_entire_declared_box_built": True,
            "Gamma_eta_CDF_or_C4_proved": False, "saved_numerical_proof_inputs": False},
        "source_pins_integrity_only": final,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": full.resources.peak_bytes(),
            "time_limit_seconds": TIME_LIMIT, "memory_limit_bytes": MEMORY_LIMIT,
            "one_sequential_producer": True, "standard_library_only": True}}


def self_tests():
    source_drift_check()
    request = fresh_entire_request()
    require(request["geometry_path"] == (CHILD,) and not request["proved_root_empty"],
            "Nonempty complete child request")
    require(request["rhoQ_min_square_exact"] == full.root.root_algebra.rhoQ_min_square(
                request["closed_rectangle"]), "Direct exact whole-box rho arithmetic")
    return {"status": "TINY_EXACT_WHOLE_CHILD_AND_INTERFACE_TESTS_ONLY",
        "exact_checks": 2, "A1_compatibility": A1.self_tests(),
        "cache_CF_A1_Gamma_or_CDF_producer_called": False}


def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--produce", action="store_true")
    modes.add_argument("--replay-existing", action="store_true")
    args = parser.parse_args()
    if not (args.produce or args.replay_existing):
        print(json.dumps(self_tests(), sort_keys=True))
        return
    output = Path(__file__).with_suffix(".json")
    require(args.replay_existing or not output.exists(), "Never overwrite a receipt")
    require(not args.replay_existing or output.exists(), "Read-only replay needs existing result")
    result = compute_fresh_pilot()
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False,
                     default=full.root.json_ready) + "\n"
    require(len(raw.encode("utf-8")) <= OUTPUT_LIMIT, "Projected complete A1 result<=4MiB")
    require(time.monotonic() - started < TIME_LIMIT
            and full.resources.peak_bytes() <= MEMORY_LIMIT,
            "Entire CLI including serialization within60s/128MiB")
    if args.replay_existing:
        require(output.stat().st_size <= OUTPUT_LIMIT, "Bounded read-only receipt")
        saved, fresh = json.loads(output.read_text(encoding="utf-8")), json.loads(raw)
        require({k: v for k, v in saved.items() if k != "resources"}
                == {k: v for k, v in fresh.items() if k != "resources"},
                "ALL projected nonresource fields match direct fresh replay")
        status = "READ_ONLY_REPLAY_MATCH"
    else:
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
        status = result["status"]
    print(json.dumps({"status": status, "result": str(output), "resources": result["resources"],
        "Gamma_eta_CDF_or_C4_proved": False}, sort_keys=True))


if __name__ == "__main__":
    main()
