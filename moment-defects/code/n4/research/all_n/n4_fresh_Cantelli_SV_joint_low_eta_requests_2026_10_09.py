"""Fresh WHOLE-box Cantelli/SV eta split; no low-eta/C4 certificate.

For a nonempty exact root request, DIRECT fresh sign-count Cantelli at
eta_lower=0 supplies raw all-p/all-H bounds and local rhoQ lower bounds.
UNKNOWN status does not invalidate these raw bounds. The audited pure
frontier consumer checks complete signed-p coverage first, then prunes
only exact squared necessary-root emptiness under actualrho<46/25.
It derives a strict Cantelli cut by upward rational rounding+1/10000.
The supplied published SV theorem independently gives the closed cut
rhoSV-rhoQ_LO. Select ONE complete route with the lower cut; do not mix
p/H contributions. Every actual eta>=joint_cut has R4<=T<CE.

All eta in [0,joint_cut], including eta0 and the shared cut face, remain
for a separately DIRECT fresh low-eta producer. This module never closes
that remaining interval or unrestricted C4. No saved numerical JSON,
Boolean/status/hash as mathematics, old CF producer or file writes.
All external analytic/physical/owner premises stay explicit. Stdlib;
cooperative<=60s/256MiB; externally coordinated one heavy job only.
Default tiny tests cover pure cut/route arithmetic, not any CDF producer.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_corrected_global_root_SV_low_eta_controller_2026_10_09 as root
import n4_conditional_cantelli_exact_eta_frontier_v2_2026_10_09 as frontier

require, SCALE, TARGET = root.require, root.SCALE, root.TARGET
Np, NH = 32, 256
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024
FRONTIER_PIN = "fd602ccb4f3e51510ad4156a76f780c71db4061e2520689d75442ff43f130211"
ROOT_PIN = "397a32a2def85c262f1f9ef534dfcc63d8e8b443ac1605a68c6bdf4f70780e5c"


def source_drift_check():
    for module, pin in ((root, ROOT_PIN), (frontier, FRONTIER_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == pin,
                "Frozen source integrity only: " + Path(module.__file__).name)
    require(SCALE == frontier.SCALE and TARGET == frontier.TARGET
            and root.ROOT == frontier.ROOT and root.RHO_CAP == frontier.RHO_CAP,
            "SAME entire physical root, exact scale and target")


def select_complete_cut(cantelli_cut, cantelli_score, sv_cut, sv_score):
    require(all(type(v) is F for v in (cantelli_cut, cantelli_score, sv_cut, sv_score))
            and min(cantelli_cut, sv_cut) >= 0
            and 0 <= cantelli_score < TARGET and 0 <= sv_score <= TARGET,
            "Each WHOLE-box route has its independently proved CLOSED bound")
    if cantelli_cut <= sv_cut:
        return cantelli_cut, "Cantelli", cantelli_score
    return sv_cut, "Shevtsova_external", sv_score


def fresh_joint_cut_for_request(request, time_limit_seconds=TIME_LIMIT):
    """DIRECT backend plus audited exact complete-root consumer, no JSON."""
    started = time.monotonic()
    source_drift_check()
    require(type(time_limit_seconds) in (int, float, F)
            and 0 < time_limit_seconds <= TIME_LIMIT, "Bounded fresh frontier timer")
    require(not request["proved_root_empty"], "Empty whole root classes need no backend")

    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Joint-cut elapsed budget")
        peak = frontier.resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Joint-cut256MiB")

    guard()
    rectangle = request["closed_rectangle"]
    fresh = frontier.backend.compute_verified_conditional_cantelli_box(rectangle, F(0),
        Np=Np, NH=NH, time_limit_seconds=time_limit_seconds - (time.monotonic() - started))
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
    guard()
    return {"joint_eta_cut_exact": cut, "joint_complete_route": route,
        "joint_high_eta_score_at_closed_cut_exact": score,
        "fresh_frontier_math": checked,
        "closed_low_eta_interval_still_to_prove": (F(0), cut),
        "SV_eta_cut_exact_unchanged": request["etaSV_exact"],
        "low_eta_or_unrestricted_C4_proved_here": False,
        "resources": {"elapsed_seconds_diagnostic": time.monotonic() - started,
            "peak_working_set_bytes": frontier.resources.peak_bytes(),
            "time_limit_seconds": time_limit_seconds, "memory_limit_bytes": MEMORY_LIMIT}}


def self_tests():
    source_drift_check()
    checks = 0
    for c, s in ((F(1, 10), F(1, 5)), (F(1, 5), F(1, 10)), (F(1, 10), F(1, 10)),
                 (F(1, 10), F(0))):
        cut, route, score = select_complete_cut(c, TARGET - F(1, 10000), s, TARGET)
        require(cut == min(c, s) and score <= TARGET
                and route == ("Cantelli" if c <= s else "Shevtsova_external"),
                "Min of complete routes, including equality and zero SV face")
        checks += 1
    require(frontier.previous.upward_strict_cut(F(0)) == F(1, 10000)
            and frontier.previous.upward_strict_cut(F(1, 10)) == F(1001, 10000),
            "Positive Cantelli reserve, never a zero-eta disappearance")
    checks += 2
    return {"status": "TINY_COMPLETE_JOINT_CUT_ARITHMETIC_ONLY", "exact_checks": checks,
            "Cantelli_or_low_eta_CDF_producer_called": False, "unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
