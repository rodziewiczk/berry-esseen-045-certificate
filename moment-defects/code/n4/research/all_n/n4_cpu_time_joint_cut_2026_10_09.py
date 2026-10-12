"""NEW PROCESS_CPU whole-box joint cut; unchanged db439 mathematics.

The resource-only API clone DIRECTLY calls the NEW CPU Cantelli backend
then the OLD audited PURE complete-root frontier consumers. No old timed
Cantelli, whole-frontier or joint producer is called. Every p/H/sign
class, exact necessary strict-rho pruning, closed Cantelli/SV cut and
all below-cut faces stay unchanged. process_time guards/remaining use
the same60-second budget; monotonic is ONLY wall resources. Sleep,
descheduling and blocking IO do not consume CPU; no hard wall deadline
or power-policy change is made. Memory caps remain256MiB outside and
the DIRECT backend64MiB. No numericJSON/CPUflag/status/hash proof gate,
partial result, checkpoint resume, low-eta or C4 theorem is added.
No import jobs, producer CLI or writes; dormant PURE tests only.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_Cantelli_SV_joint_low_eta_requests_2026_10_09 as previous
import n4_cpu_time_Cantelli_backend_2026_10_09 as backend

root, frontier = previous.root, previous.frontier
require, SCALE, TARGET = previous.require, previous.SCALE, previous.TARGET
Np, NH, TIME_LIMIT, MEMORY_LIMIT = previous.Np, previous.NH, previous.TIME_LIMIT, previous.MEMORY_LIMIT
CLOCK_KIND = "PROCESS_CPU_USER_PLUS_SYSTEM"
PREVIOUS_PIN = "db439ba1c86e6f533cdd2f5c9ec0354f2e7585c4b98211a758821c49a970f51a"
BACKEND_PIN = "95e4256267eb0ae9f3757cce3f10c75ebed38190f5ae97392c702e32ca07cd4b"
select_complete_cut = previous.select_complete_cut


def source_drift_check():
    previous.source_drift_check()
    backend.source_drift_check()
    for module, expected in ((previous, PREVIOUS_PIN), (backend, BACKEND_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected,
                "Frozen PURE/correct CPU-backend integrity only")
    require(TIME_LIMIT == backend.TIME_LIMIT == 60 and backend.MEMORY_LIMIT == 64 * 1024 * 1024
            and MEMORY_LIMIT == 256 * 1024 * 1024 and SCALE == backend.SCALE,
            "SAME math/CPU caps/actual original memory limits")


def dependency_pins():
    pins = backend.dependency_pins()
    for module in (previous, root, frontier, frontier.previous):
        path = Path(module.__file__)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(path.name not in pins or pins[path.name] == digest, "Consistent CPU/PURE source closure")
        pins[path.name] = digest
    path = Path(__file__)
    require(path.name not in pins, "Unique CPU joint source")
    pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return pins


def fresh_joint_cut_for_request(request, time_limit_seconds=TIME_LIMIT):
    """DIRECT backend plus audited exact complete-root consumer, no JSON."""
    started_cpu, started_wall = time.process_time(), time.monotonic()
    initial_pins = dependency_pins()
    source_drift_check()
    require(type(time_limit_seconds) in (int, float, F)
            and 0 < time_limit_seconds <= TIME_LIMIT, "Bounded fresh frontier timer")
    require(not request["proved_root_empty"], "Empty whole root classes need no backend")

    def guard():
        require(time.process_time() - started_cpu < time_limit_seconds, "Joint-cut PROCESS_CPU budget")
        peak = frontier.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Joint-cut256MiB")

    guard()
    rectangle = request["closed_rectangle"]
    fresh = backend.compute_verified_conditional_cantelli_box(rectangle, F(0),
        Np=Np, NH=NH, time_limit_seconds=time_limit_seconds - (time.process_time() - started_cpu))
    checked = frontier._root_frontier_from_fresh_backend(fresh, rectangle, Np, NH)
    require(checked["rhoQ_box_lower_exact"] == request["rhoQ_lower_exact"]
            and checked["SV_eta_cut_exact"] == request["etaSV_exact"],
            "Fresh exact denominator/SV cut agree, not a stale/sampled request")
    cut, route, score = select_complete_cut(checked["Cantelli_eta_cut_exact"],
        checked["Cantelli_score_at_cut_exact"], checked["SV_eta_cut_exact"],
        checked["SV_score_at_cut_exact"])
    require(cut == checked["joint_eta_cut_exact"] and route == checked["joint_complete_route"]
            and score == checked["joint_score_at_cut_exact"]
            and cut < request["actual_eta_capacity_outer_open"],
            "Same WHOLE selected route; all below-cut faces remain to be proved")
    source_drift_check()
    require(dependency_pins() == initial_pins, "Complete CPU joint source closure unchanged")
    guard()
    return {"joint_eta_cut_exact": cut, "joint_complete_route": route,
        "joint_high_eta_score_at_closed_cut_exact": score,
        "fresh_frontier_math": checked,
        "closed_low_eta_interval_still_to_prove": (F(0), cut),
        "SV_eta_cut_exact_unchanged": request["etaSV_exact"],
        "low_eta_or_unrestricted_C4_proved_here": False,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started_wall,
            "wall_elapsed_seconds_diagnostic": time.monotonic() - started_wall,
            "cpu_elapsed_seconds_diagnostic": time.process_time() - started_cpu,
            "clock_kind": CLOCK_KIND, "hard_wall_deadline_imposed": False,
            "peak_working_set_bytes": frontier.resources.peak_bytes(),
            "time_limit_seconds": time_limit_seconds, "memory_limit_bytes": MEMORY_LIMIT}}


def self_tests():
    """Dormant PURE cuts only, not a fresh high/low/root producer."""
    source_drift_check()
    for c, s in ((F(1, 10), F(1, 5)), (F(1, 5), F(1, 10)), (F(0), F(0))):
        cut, route, score = select_complete_cut(c, TARGET - F(1, 10000), s, TARGET)
        require(cut == min(c, s) and score <= TARGET, "UNCHANGED complete whole-route cut")
    return {"exact_checks": 3, "clock_kind": CLOCK_KIND, "producer_called_or_files_written": False,
            "hard_wall_deadline_imposed": False, "unrestricted_C4_proved": False}

