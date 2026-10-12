"""NEW CPU HIGH preparation; SAME exact five requests and64MiB guards.

Only the small preparation functions are copied. Old6ad PURE request
factory, same-request validators and scalar/callable60 clamp are aliased.
Each nonempty request DIRECTLY calls the NEW CPU joint/backend chain;
the lexical old6ad->full.split timed producer is NEVER called. Parent
and ALL4 closed children, exact strict-cap equality emptiness, cut0/eta0,
all own cuts and every HIGH slot are unchanged. CPU budget is60 per
producer, old actual64MiB BEFORE/AFTER every call remains. ROOT caller
still must prepare ALL1300 before any cache/A1 arrays. No old numerical
checkpoint/status/proof input, resume, power-policy or math change.

No own wall deadline, producer CLI, file write or import job. All active
timer/remaining guards are CPU in joint/backend and the caller. A clock
flag/source hash/type alone does not prove direct fresh provenance.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path

import n4_fresh_optimized_qnorm_parent_four_child_coordinator_2026_10_09 as previous
import n4_cpu_time_joint_cut_2026_10_09 as joint

resources, require = previous.resources, previous.require
CHILD_LIMIT, HIGH_MEMORY_LIMIT = previous.CHILD_LIMIT, previous.HIGH_MEMORY_LIMIT
SCALE, TARGET, CLOCK_KIND = previous.SCALE, previous.TARGET, "PROCESS_CPU_USER_PLUS_SYSTEM"
PREVIOUS_PIN = "6ad87c2f8dc3bca497b6ba8d81afc0932bc059175299c09410ee83d934556cdd"
JOINT_PIN = "e4696bb2b968799f8392820debffc650e8032cc4869f1abe7859a4c921d7f428"

# Exact PURE source scope/checks/cap only; never old preparation/producer.
fresh_parent_and_child_requests = previous.fresh_parent_and_child_requests
_checked_high_pair = previous._checked_high_pair
_checked_direct_pairs = previous._checked_direct_pairs
_remaining_budget = previous._remaining_budget


def source_drift_check():
    previous.source_drift_check()
    joint.source_drift_check()
    for module, expected in ((previous, PREVIOUS_PIN), (joint, JOINT_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected,
                "Frozen PURE scopes/direct CPUproducer integrity")
    require(CHILD_LIMIT == joint.TIME_LIMIT == 60 and HIGH_MEMORY_LIMIT == 64 * 1024 * 1024
            and SCALE == joint.SCALE and TARGET == joint.TARGET, "SAME math/grids/CPU caps/HIGH64")


def dependency_pins():
    pins = previous.dependency_pins()
    for name, digest in joint.dependency_pins().items():
        require(name not in pins or pins[name] == digest, "Consistent HIGH/PURE source closure")
        pins[name] = digest
    path = Path(__file__)
    require(path.name not in pins, "Unique CPU HIGH source")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def prepare_fresh_high_requests(requests, guard, budget=CHILD_LIMIT):
    """ALL exact parent+4 HIGH FIRST; actual backend64MiB never overridden."""
    require(callable(guard) and type(requests) in (tuple, list) and len(requests) == 5,
            "Caller guard and all5 exact ordered requests")
    require(tuple(requests) == fresh_parent_and_child_requests(requests[0]["grid_index"]),
            "Parent and ALL4 complete closed children, no prefix/selected class")
    source_drift_check()
    pairs, resource_records = [], []
    for request in requests:
        guard()
        peak = resources.peak_bytes()
        require(peak is not None and peak <= HIGH_MEMORY_LIMIT, "ALL high preparation BEFORE A1/strict64MiB")
        if request["proved_root_empty"]:
            high = None
        else:
            fresh = joint.fresh_joint_cut_for_request(request, time_limit_seconds=_remaining_budget(budget))
            resource_records.append(fresh["resources"])
            high = {key: value for key, value in fresh.items() if key != "resources"}
        _checked_high_pair(request, high)
        pairs.append((request, high))
        guard()
        peak = resources.peak_bytes()
        require(peak is not None and peak <= HIGH_MEMORY_LIMIT, "High backend original64MiB still respected")
    require(len(pairs) == 5, "ALL5 high requests completed, no early result")
    source_drift_check()
    return tuple(pairs), tuple(resource_records)


def prepare_fresh_parent_high(index, guard, budget=CHILD_LIMIT):
    return prepare_fresh_high_requests(fresh_parent_and_child_requests(index), guard, budget)


def self_tests():
    """Dormant PURE scope/budget checks, never HIGH/cache/root producer."""
    source_drift_check()
    checks = 0
    for index in (0, 200, 254, 259):
        requests = fresh_parent_and_child_requests(index)
        require(len(requests) == 5 and tuple(r["geometry_path"] for r in requests)
                == ((), (0,), (1,), (2,), (3,)), "ALL5 original closed requests")
        checks += 1
    require(_remaining_budget(F(90)) == 60 and _remaining_budget(lambda: F(30)) == 30,
            "SAME positive scalar/callable CPU budget clamp")
    return {"exact_checks": checks + 1, "clock_kind": CLOCK_KIND,
            "producer_called_or_files_written": False, "unrestricted_C4_proved": False}

