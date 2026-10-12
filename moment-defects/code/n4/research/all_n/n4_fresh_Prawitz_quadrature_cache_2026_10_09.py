"""DIRECT-FRESH geometry-independent Prawitz quadrature cache; no CDF gate.

build_fresh_quadrature_cache(N=256,H_step=1/8) computes ONCE in memory:
 exact q grid, Machin pi/phi0, M32 kernel rectangles/norms,
 every phase exp(-i*q_j*H), normalCDF(H/2), positive-tail witness,
 sqrt10 and CE comparison for target4097/10000.
All H58/115/229 nodes and BOTH reflected-law uses share the same phases.
The data are immutable integer/Fraction tuples. No saved JSON/cache/status/
source hash supplies numerical mathematics; a caller MUST directly build
this fresh object with the audited builder in its coordinated producer.
Schema checks detect integration errors, not mathematical provenance.

These quantities are independent of w,beta,eta and the original law.
The phase is initialized by exact exponential(-3H/(2N)) and multiplied
by exact exponential(-3H/N), with the SAME outward unit-phase intersection
after each step as the frozen corrected leaf. Thus cached phase_j has
the identical integer rectangle produced by the old fresh recurrence.
Replacing repeated recurrence calls by these preverified rectangles
does not alter precision, signs, smoothing, quadrature or H reserves.
All used exponential primitives scale their physical Taylor remainders
correctly. NO legacy generic CF function is called.

No gQ, roots, probabilities, Eg, gradients, Hessians, response/r/r_c/y
cache, price/radius or eta-dependent object is cached across geometry.
Actual CF/whole-box correction and all physical CDF premises belong to a
NEW consumer; this module is not a monkeypatch of frozen e29 or any older
producer. A fresh-cache object is not itself a CDF acceptance certificate.

Separate PURE per-root helpers avoid duplicate derivative evaluations:
nominal_derivative_rectangles(q,a_bar,b_bar) may be computed ONCE for
ONE rational probability expansion point; the same preverified values
give signed center blocks8*kappa*g^3*gi and radial2Re(conjg*gi).
No root-dependent derivative data are shared across parameter boxes.
The bar-reference g inside these gradients is NOT the TRUE irrational
nominal CF baseline. Root shifts/Hessians/convex probability paths and
that separately correctly-scaled TRUE baseline remain consumer duties.
The product ordering matches the audited pure center/radial helpers.

Cached signed-gradient/center sums use the actual fixed H/q phase row,
multiply outward rectangles and then sum signed interval endpoints.
Fresh geometry-dependent blocks are caller mathematical inputs, not
JSON/status/hash values. Both orientations are retained explicitly;
reflection conjugates the characteristic data, NOT the H phase/kernel.

Stdlib, cooperative60s/256MiB builder; bounded N256/H<=229. One externally
coordinated producer. CLI runs ONLY dormant tiny pure regressions when
authorized, NO full cache/leaf/global producer or file write. No runtime
or speed-up claim before an authorized benchmark. All old files untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

import n4_Q3_first_critical_integer_abs_Prawitz_gate_strict_v2_2026_10_08 as arithmetic
import n4_Q3_contact_coordinate_derivative_algebra_2026_10_08 as derivatives
import n4_windows_resource_guard_2026_10_09 as resources

integer, SCALE = arithmetic.arith, arithmetic.S
TARGET, KERNEL_M = F(4097, 10000), 32
H_STEPS = (F(1, 8), F(1, 16), F(1, 32))
TIME_LIMIT, MEMORY_LIMIT = 60, 256 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def checked_rectangle(rectangle, label="complex rectangle"):
    require(type(rectangle) in (tuple, list) and len(rectangle) == 4
            and all(type(value) is int for value in rectangle)
            and rectangle[0] <= rectangle[1] and rectangle[2] <= rectangle[3],
            label + ": ordered four-integer SCALE rectangle")
    return tuple(rectangle)


def complete_H_grid(H_step):
    require(type(H_step) is F and H_step in H_STEPS, "Exact approved complete H spacing")
    width = F(57, 8) / H_step
    require(width.denominator == 1, "Exact H outer faces")
    result = tuple(F(-4) + H_step * j for j in range(width.numerator + 1))
    require(result[0] == -4 and result[-1] == F(25, 8), "Entire central H interval")
    return result


def fresh_phase_rectangles_for_H(H, N, guard=lambda: None):
    """Pure unchanged recurrence; small N permitted for algebra tests only."""
    require(type(H) is F and F(-4) <= H <= F(25, 8)
            and type(N) is int and 1 <= N <= 256, "Exact bounded phase arguments")
    phase = arithmetic.exponential_exact_argument(-3 * H / (2 * N))
    ratio = arithmetic.exponential_exact_argument(-3 * H / N)
    phases = []
    for j in range(N):
        guard()
        phases.append(checked_rectangle(phase, "fresh midpoint phase"))
        phase = arithmetic.unit_phase_intersection(arithmetic.complex_multiply(phase, ratio))
    return tuple(phases)


@dataclass(frozen=True)
class FreshQuadratureCache:
    """Immutable data from the DIRECT fresh builder, NOT a proof-by-type flag."""
    scale: int
    N: int
    kernel_M: int
    H_step: F
    H_grid: tuple
    q_grid: tuple
    pi_bracket: tuple
    phi0_bracket: tuple
    sqrt10_bracket: tuple
    kernel_rectangles: tuple
    kernel_modulus_uppers: tuple
    phase_rows: tuple
    normal_cdf_intervals: tuple
    positive_tail_Phi_interval: tuple
    CE_lower_exact: F
    source_pins_integrity_only: tuple
    cache_sha256_integrity_only: str
    elapsed_seconds_diagnostic: float
    peak_working_set_bytes_diagnostic: object

    def H_index(self, H):
        require(type(H) is F and H in self.H_grid, "Exact cached H label")
        return self.H_grid.index(H)

    def phases_at(self, H):
        return self.phase_rows[self.H_index(H)]

    def normal_at(self, H):
        return self.normal_cdf_intervals[self.H_index(H)]

    def compact_metadata(self):
        """No cache arrays exported as saved reusable numerical proof inputs."""
        return {"N": self.N, "kernel_M": self.kernel_M, "H_step": self.H_step,
            "H_nodes": len(self.H_grid), "phase_integer_endpoints": 4 * self.N * len(self.H_grid),
            "geometry_dependent_fields_cached": False,
            "cache_mathematical_precondition": "Direct freshly audited in-memory builder; immutable type/schema/hash alone are not proof.",
            "cache_sha256_integrity_only": self.cache_sha256_integrity_only,
            "source_pins_integrity_only": dict(self.source_pins_integrity_only)}

    def resource_metadata(self):
        """Place these nondeterministic fields ONLY in the caller's resources."""
        return {"elapsed_seconds_diagnostic": self.elapsed_seconds_diagnostic,
                "peak_working_set_bytes": self.peak_working_set_bytes_diagnostic,
                "time_limit_seconds": TIME_LIMIT, "memory_limit_bytes": MEMORY_LIMIT}


def build_fresh_quadrature_cache(N=256, H_step=F(1, 8), time_limit_seconds=TIME_LIMIT):
    """DIRECT-FRESH producer; no numerical cache/JSON arguments or file writes."""
    started = time.monotonic()
    require(type(N) is int and N == 256, "Shared physical cache grid fixedN256")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic cooperative cache budget<=60s")
    H_grid = complete_H_grid(H_step)
    def guard():
        require(time.monotonic() - started < time_limit_seconds, "Fresh quadrature cache elapsed budget")
        peak = resources.peak_bytes()
        require(peak is None or peak <= MEMORY_LIMIT, "Fresh quadrature cache256MiB working set")
    guard()
    pi, phi0 = arithmetic.pi_and_phi0()
    sqrt10 = integer.sqrt_fraction_interval(F(10))
    ce_lower = F((3 * SCALE + sqrt10[0]) * phi0[0], 6 * SCALE ** 2)
    require(TARGET < ce_lower, "Fresh geometry-independent CE comparison")
    q_grid, kernels, norms = [], [], []
    for j in range(N):
        guard()
        q_grid.append(F(3 * (2 * j + 1), 2 * N))
        kernel = checked_rectangle(arithmetic.kernel_rectangle(F(2 * j + 1, 2 * N), N, KERNEL_M, pi), "fresh kernel")
        kernels.append(kernel)
        norms.append(integer.rectangle_modulus_upper(kernel))
    phases, normals = [], []
    for H in H_grid:
        guard()
        phases.append(fresh_phase_rectangles_for_H(H, N, guard))
        normal = tuple(arithmetic.normal_cdf_interval(H / 2, phi0))
        require(len(normal) == 2 and all(type(value) is int for value in normal)
                and 0 <= normal[0] <= normal[1] <= SCALE, "Fresh normal CDF interval")
        normals.append(normal)
    tail = tuple(arithmetic.normal_cdf_interval(F(25, 16), phi0))
    require(tail == normals[-1] and 5 * tail[0] > 4 * SCALE, "Fresh positive-tail Gaussian witness")
    # Stream small rows into the integrity digest, avoiding a second large
    # full-cache serialization. The hash is NOT a numerical proof premise.
    digest = hashlib.sha256()
    digest.update(str((SCALE, N, H_step, pi, phi0, sqrt10, ce_lower)).encode("ascii"))
    for q, kernel, norm in zip(q_grid, kernels, norms):
        digest.update(str((q, kernel, norm)).encode("ascii"))
    for H, row, normal in zip(H_grid, phases, normals):
        guard()
        digest.update(str((H, normal)).encode("ascii"))
        for phase in row:
            digest.update(str(phase).encode("ascii"))
    guard()
    files = (Path(__file__), Path(arithmetic.__file__), Path(integer.__file__),
             Path(derivatives.__file__), Path(resources.__file__))
    return FreshQuadratureCache(SCALE, N, KERNEL_M, H_step, H_grid, tuple(q_grid),
        tuple(pi), tuple(phi0), tuple(sqrt10), tuple(kernels), tuple(norms), tuple(phases), tuple(normals),
        tail, ce_lower, tuple((path.name, hashlib.sha256(path.read_bytes()).hexdigest()) for path in files),
        digest.hexdigest(), time.monotonic() - started, resources.peak_bytes())


def validate_preverified_fresh_cache(cache, N=256, H_step=None):
    """Schema ONLY, under DIRECT-FRESH immutable-cache mathematical premise."""
    require(type(cache) is FreshQuadratureCache and type(N) is int and N == cache.N == 256,
            "Expected fresh immutable physicalN256 cache object")
    step = cache.H_step if H_step is None else H_step
    grid = complete_H_grid(step)
    require(cache.scale == SCALE and cache.kernel_M == KERNEL_M and cache.H_step == step
            and cache.H_grid == grid
            and cache.q_grid == tuple(F(3 * (2 * j + 1), 2 * N) for j in range(N)),
            "Exact same shared SCALE/kernel/q/H labels")
    require(len(cache.kernel_rectangles) == len(cache.kernel_modulus_uppers) == N
            and len(cache.phase_rows) == len(cache.normal_cdf_intervals) == len(grid)
            and all(len(row) == N for row in cache.phase_rows), "Every declared frequency/H phase present")
    require(cache.CE_lower_exact > TARGET and 5 * cache.positive_tail_Phi_interval[0] > 4 * SCALE,
            "Preverified scalar target/tail fields agree with intended scope")
    return cache


def _checked_derivative_values(values):
    """Pure schema; caller must prove these are SAME fresh rational-root derivatives."""
    require(type(values) is dict and all(name in values for name in ("g", "ga", "gb", "gaa", "gab", "gbb")),
            "Complete preverified rational probability-reference derivative values")
    return {name: checked_rectangle(values[name], "fresh derivative " + name)
            for name in ("g", "ga", "gb", "gaa", "gab", "gbb")}


def signed_center_gradient_blocks_from_values(values, kernel):
    """Fresh SAME-root values -> both8*kappa*g^3*gi blocks; old product order."""
    values = _checked_derivative_values(values)
    kernel = checked_rectangle(kernel, "preverified physical kernel")
    g = arithmetic.unit_phase_intersection(values["g"])
    blocks = {}
    for orientation in (1, -1):
        characteristic = g if orientation == 1 else integer.conjugate_rectangle(g)
        ga = values["ga"] if orientation == 1 else integer.conjugate_rectangle(values["ga"])
        gb = values["gb"] if orientation == 1 else integer.conjugate_rectangle(values["gb"])
        cube = arithmetic.complex_multiply(arithmetic.complex_multiply(characteristic, characteristic), characteristic)
        blocks[orientation] = tuple(tuple(8 * value for value in arithmetic.complex_multiply(kernel,
            arithmetic.complex_multiply(cube, derivative))) for derivative in (ga, gb))
    return blocks


def radial_gradient_intervals_from_values(values):
    """SAME fresh rational-root values -> signed2Re(conjg*gi), no baseline change."""
    values = _checked_derivative_values(values)
    g = arithmetic.unit_phase_intersection(values["g"])
    conjugate = integer.conjugate_rectangle(g)
    gradients = []
    for name in ("ga", "gb"):
        product = arithmetic.complex_multiply(conjugate, values[name])
        gradients.append((2 * product[0], 2 * product[1]))
    return tuple(gradients)


def fresh_per_root_derivative_bundle(q, a_bar, b_bar, kernel):
    """Compute geometry-dependent derivative values ONCE for one q/root ONLY."""
    require(type(q) is F and type(a_bar) is F and type(b_bar) is F, "Exact rational per-root parameters")
    values = derivatives.nominal_derivative_rectangles(q, a_bar, b_bar)
    return {"q": q, "a_bar": a_bar, "b_bar": b_bar,
        "signed_center_blocks": signed_center_gradient_blocks_from_values(values, kernel),
        "radial_gradient_intervals": radial_gradient_intervals_from_values(values),
        "true_nominal_CF_baseline_supplied_here": False,
        "geometry_dependent_data_shared_across_boxes": False}


def sum_signed_gradient_blocks_with_phases(blocks, phases, guard=lambda: None):
    """Pure signed sum; preverified phase row and SAME-root blocks are premises."""
    require(type(blocks) in (tuple, list) and type(phases) in (tuple, list)
            and 1 <= len(blocks) == len(phases) <= 256, "Complete small signed-gradient q/phase rows")
    accumulated = {orientation: [[0, 0], [0, 0]] for orientation in (1, -1)}
    for item, phase in zip(blocks, phases):
        guard()
        phase = checked_rectangle(phase, "preverified midpoint phase")
        require(type(item) is dict and set(item) == {1, -1} and all(type(key) is int for key in item),
                "BOTH genuine orientations in each fresh gradient block")
        for orientation in (1, -1):
            require(type(item[orientation]) in (tuple, list) and len(item[orientation]) == 2, "Both physical contact gradients")
            for index, block in enumerate(item[orientation]):
                value = arithmetic.complex_multiply(phase, checked_rectangle(block, "fresh contact gradient block"))
                accumulated[orientation][index][0] += value[0]
                accumulated[orientation][index][1] += value[1]
    return {orientation: tuple(tuple(pair) for pair in values) for orientation, values in accumulated.items()}


def cached_signed_gradient_intervals(blocks, H, cache, guard=lambda: None):
    """Geometry-dependent signed-gradient sum with preverified shared phases."""
    validate_preverified_fresh_cache(cache)
    require(len(blocks) == cache.N, "SAME physical q count as fresh cache")
    return sum_signed_gradient_blocks_with_phases(blocks, cache.phases_at(H), guard)


def sum_center_blocks_with_phases(blocks, phases, guard=lambda: None):
    """Pure both-orientation real sums; full true-Q fourth-power blocks remain fresh."""
    require(type(blocks) is dict and set(blocks) == {1, -1} and all(type(key) is int for key in blocks)
            and 1 <= len(phases) <= 256
            and all(len(blocks[orientation]) == len(phases) for orientation in (1, -1)),
            "BOTH complete fresh center frequency-block vectors")
    accumulated = {1: [0, 0], -1: [0, 0]}
    for j, phase in enumerate(phases):
        guard()
        phase = checked_rectangle(phase, "preverified midpoint phase")
        for orientation in (1, -1):
            value = arithmetic.complex_multiply(phase, checked_rectangle(blocks[orientation][j], "fresh true-Q kernel-fourth block"))
            accumulated[orientation][0] += value[0]
            accumulated[orientation][1] += value[1]
    return {orientation: tuple(value) for orientation, value in accumulated.items()}


def cached_center_real_sums(blocks, H, cache, guard=lambda: None):
    validate_preverified_fresh_cache(cache)
    return sum_center_blocks_with_phases(blocks, cache.phases_at(H), guard)


def self_tests():
    """Dormant scalar/short-row tests ONLY; NEVER full cache or leaf producer."""
    started, checks = time.monotonic(), 0
    def guard():
        require(time.monotonic() - started < 10, "Only tiny cache/helper algebra tests")
        peak = resources.peak_bytes()
        require(peak is None or peak <= 64 * 1024 * 1024, "Tiny cache/helper64MiB working set")
    for step, size in ((F(1, 8), 58), (F(1, 16), 115), (F(1, 32), 229)):
        require(len(complete_H_grid(step)) == size, "Complete exact H cache shape")
        checks += 1
    # Comparison invokes ONLY preserved PURE functions; no old producer or
    # flawed genericCF helper. Exact small rational references avoid an N/H job.
    import n4_Q3_signed_contact_center_taylor_resource_safe_2026_10_09 as old_center
    import n4_Q3_squared_modulus_contact_taylor_resource_safe_2026_10_09 as old_radial
    kernel = (SCALE // 7, integer.ceil_div(SCALE, 7), SCALE // 11, integer.ceil_div(SCALE, 11))
    for a, b in ((F(1), F(1)), (F(1, 2), F(2)), (F(3, 4), F(7, 4))):
        for q in (F(0), F(1, 8), F(3)):
            guard()
            values = derivatives.nominal_derivative_rectangles(q, a, b)
            require(signed_center_gradient_blocks_from_values(values, kernel)
                    == old_center.base_derivative_blocks(q, kernel, a, b), "Bit-for-bit same signed-gradient product ordering")
            require(radial_gradient_intervals_from_values(values)
                    == old_radial.radial_gradient_intervals(q, a, b), "Bit-for-bit same radial-gradient product ordering")
            bundle = fresh_per_root_derivative_bundle(q, a, b, kernel)
            require(bundle["signed_center_blocks"] == signed_center_gradient_blocks_from_values(values, kernel)
                    and bundle["radial_gradient_intervals"] == radial_gradient_intervals_from_values(values)
                    and not bundle["true_nominal_CF_baseline_supplied_here"], "ONE-root derivative bundle never substitutes the TRUE baseline")
            checks += 3
    Nsmall = 4
    blocks = [signed_center_gradient_blocks_from_values(
        derivatives.nominal_derivative_rectangles(F(3 * (2 * j + 1), 2 * Nsmall), F(1), F(2)), kernel)
        for j in range(Nsmall)]
    for H in (F(-4), F(-5, 8), F(0), F(25, 8)):
        guard()
        phases = fresh_phase_rectangles_for_H(H, Nsmall, guard)
        require(sum_signed_gradient_blocks_with_phases(blocks, phases, guard)
                == old_center.sum_signed_gradient_intervals(blocks, H, Nsmall, guard),
                "Cached phase vector and original fresh recurrence give identical signed sums")
        center_blocks = {orientation: [tuple(value for value in item[orientation][0]) for item in blocks]
                         for orientation in (1, -1)}
        sums = sum_center_blocks_with_phases(center_blocks, phases, guard)
        manual = {orientation: [0, 0] for orientation in (1, -1)}
        for j, phase in enumerate(phases):
            for orientation in (1, -1):
                product = arithmetic.complex_multiply(phase, center_blocks[orientation][j])
                manual[orientation][0] += product[0]
                manual[orientation][1] += product[1]
        require(sums == {orientation: tuple(value) for orientation, value in manual.items()}, "Cached center sum keeps both real endpoint signs")
        checks += 2
    try:
        checked_rectangle((True, 1, 0, 0))
    except RuntimeError:
        checks += 1
    else:
        raise RuntimeError("Bool fixed-point endpoint accepted")
    guard()
    return {"status": "FRESH_QUADRATURE_CACHE_AND_PER_ROOT_HELPERS_TINY_TESTS_ONLY", "exact_checks": checks,
        "full_cache_leaf_or_global_producer_called": False, "old_sources_or_receipts_modified": False,
        "performance_improvement_measured": False, "CDF_or_unrestricted_C4_proved": False}


if __name__ == "__main__":
    print(json.dumps(self_tests(), sort_keys=True))
