"""NEW CPU-budget fresh quadrature builder; unchanged frozen6eca mathematics.

Only the old timed builder body is copied. Its resource clock starts,
guards and elapsed diagnostic use time.process_time with the SAME60-second
budget and256MiB cap. Host sleep, descheduling and blocking IO do not
spend this process's CPU budget. No hard wall deadline or power-policy
change is introduced. Callers retain their own wall-time diagnostics.

FreshQuadratureCache is the EXACT old frozen immutable class, not a new
subclass or a flag: unchanged PURE consumers require type(cache) to be
that class. Its elapsed_seconds_diagnostic field records CPU elapsed
time for this builder. No frozen class, method, module global or validator
is modified. The old timed producer is never called or monkeypatched.

All exact q/H grids, N256, approved H spacings, Machin pi/phi0, degree60
Taylor exponential/normal-CDF arithmetic, phase recurrence, M32 kernel,
norms, positive-tail witness, sqrt10 and target4097/10000 CE comparison
remain unchanged. The same old PURE helpers and signed sum routines are
explicitly aliased below; no dynamic forwarding of an old timed API.

Source pins include this NEW source, the frozen cache source and every
old helper source used by these aliases. Pins/type/schema/digest are
integrity checks ONLY, never mathematical inputs or proof of freshness.
The caller must DIRECTLY run this builder in its coordinated producer.
No saved cache/JSON/status/checkpoint/resume supplies numerical math.
No geometry-dependent CF/root/radius/CDF data are shared across geometry.

Stdlib; externally coordinated ONE producer. No import-time job, CLI,
file write, runtime claim, entire-root certificate or unrestricted C4
claim is added. All old sources and receipts remain untouched.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from pathlib import Path
import time

import n4_fresh_Prawitz_quadrature_cache_2026_10_09 as previous

arithmetic, integer, derivatives, resources = (
    previous.arithmetic, previous.integer, previous.derivatives, previous.resources)
SCALE, TARGET, KERNEL_M = previous.SCALE, previous.TARGET, previous.KERNEL_M
H_STEPS = previous.H_STEPS
TIME_LIMIT, MEMORY_LIMIT = previous.TIME_LIMIT, previous.MEMORY_LIMIT
CLOCK_KIND = "PROCESS_CPU_USER_PLUS_SYSTEM"
PREVIOUS_PIN = "6eca3207f22f510752a3939491fbfa1ba883db7e1a0dfad8608f3db4655b904e"
ARITHMETIC_PIN = "1c6fd24479b030e9357b85467cc07c353eef199d471b43a9b05083fa5d30cddc"
INTEGER_PIN = "722ebde13cc08d1e82b0b92e0faf7af2db8cc0ce191f277494937818d9e50aa0"
DERIVATIVES_PIN = "ecbeb4285194dc4c642258fdb4aa77fcff50f8b29f69daeba40b26a5f4d0a7c1"
RESOURCES_PIN = "b0cc505146011adce03a2b84d0c551d56d7b407f11bb4786cf10704b6c05d6de"

# Exact old immutable type and explicit PURE aliases ONLY. No timed builder
# or old self-test/CLI API is forwarded, and no old module is modified.
FreshQuadratureCache = previous.FreshQuadratureCache
require = previous.require
checked_rectangle = previous.checked_rectangle
complete_H_grid = previous.complete_H_grid
fresh_phase_rectangles_for_H = previous.fresh_phase_rectangles_for_H
validate_preverified_fresh_cache = previous.validate_preverified_fresh_cache
_checked_derivative_values = previous._checked_derivative_values
signed_center_gradient_blocks_from_values = previous.signed_center_gradient_blocks_from_values
radial_gradient_intervals_from_values = previous.radial_gradient_intervals_from_values
fresh_per_root_derivative_bundle = previous.fresh_per_root_derivative_bundle
sum_signed_gradient_blocks_with_phases = previous.sum_signed_gradient_blocks_with_phases
cached_signed_gradient_intervals = previous.cached_signed_gradient_intervals
sum_center_blocks_with_phases = previous.sum_center_blocks_with_phases
cached_center_real_sums = previous.cached_center_real_sums


def source_drift_check():
    """Frozen complete PURE helper integrity, not mathematical provenance."""
    for module, expected in ((previous, PREVIOUS_PIN), (arithmetic, ARITHMETIC_PIN),
                             (integer, INTEGER_PIN), (derivatives, DERIVATIVES_PIN),
                             (resources, RESOURCES_PIN)):
        require(hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest() == expected,
                "Frozen CPU cache PURE source integrity: " + Path(module.__file__).name)
    require(FreshQuadratureCache is previous.FreshQuadratureCache
            and SCALE == 10 ** 40 and TARGET == F(4097, 10000) and KERNEL_M == 32
            and H_STEPS == (F(1, 8), F(1, 16), F(1, 32))
            and TIME_LIMIT == 60 and MEMORY_LIMIT == 256 * 1024 * 1024,
            "Exact old immutable type and unchanged quadrature/resource constants")


def dependency_pins():
    """Complete NEW builder plus frozen cache/PURE helper source closure."""
    files = (Path(__file__), Path(previous.__file__), Path(arithmetic.__file__),
             Path(integer.__file__), Path(derivatives.__file__), Path(resources.__file__))
    require(len({path.name for path in files}) == len(files), "Unique complete CPU cache source closure")
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def build_fresh_quadrature_cache(N=256, H_step=F(1, 8), time_limit_seconds=TIME_LIMIT):
    """DIRECT-FRESH CPU producer; no numerical cache/JSON arguments or writes."""
    started = time.process_time()
    source_drift_check()
    initial_pins = dependency_pins()
    require(type(N) is int and N == 256, "Shared physical cache grid fixedN256")
    require(type(time_limit_seconds) in (int, float, F) and 0 < time_limit_seconds <= TIME_LIMIT,
            "Diagnostic cooperative cache CPU budget<=60s")
    H_grid = complete_H_grid(H_step)
    def guard():
        require(time.process_time() - started < time_limit_seconds, "Fresh quadrature cache process CPU budget")
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
    result = FreshQuadratureCache(SCALE, N, KERNEL_M, H_step, H_grid, tuple(q_grid),
        tuple(pi), tuple(phi0), tuple(sqrt10), tuple(kernels), tuple(norms), tuple(phases), tuple(normals),
        tail, ce_lower, tuple(initial_pins.items()),
        digest.hexdigest(), time.process_time() - started, resources.peak_bytes())
    source_drift_check()
    require(dependency_pins() == initial_pins, "Complete CPU cache source closure unchanged")
    guard()
    return result
