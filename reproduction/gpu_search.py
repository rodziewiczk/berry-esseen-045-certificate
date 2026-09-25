#!/usr/bin/env python3
"""CUDA numerical primitives for the publication parameter-bank builder.

For fixed ``(n,rho,q)`` the scan minimizes the decomposed Prawitz objective over

    t0, eta, lambda, m in {8,16,32,64,100}

without forming their full Cartesian product.  Prefix sums make the ``eta``,
``lambda``, and ``t0`` searches inexpensive after node evaluation.  This module
contains no stage selection or wall-clock policy; those deterministic choices
belong to :mod:`reproduction.build_parameter_bank`.
"""
from __future__ import annotations

import gc
import math
import platform
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import cupy as cp
    from cupyx.scipy.special import exp1 as cp_exp1
except ImportError as exc:  # pragma: no cover - deployment condition
    raise RuntimeError(
        "CuPy is required; install the pinned GPU requirements"
    ) from exc

PI = math.pi
TWO_PI = 2.0 * math.pi
THETA0 = 3.99589567
KAPPA = 0.09916191
TARGET = 0.45
RHO_MAX = 0.3322 * 0.429 / (0.45 - 0.3322)
C_ESSEEN = (math.sqrt(10.0) + 3.0) / (6.0 * math.sqrt(2.0 * math.pi))
N_MAX = math.ceil((3.0 * RHO_MAX / (TARGET - C_ESSEEN)) ** 2) - 1
M_VALUES = (8, 16, 32, 64, 100)


@dataclass(frozen=True)
class GridSpec:
    panels: int
    order: int
    power: int
    t0_min: float = 0.25
    t0_max: float = 0.90
    max_t0_points: int = 256


@dataclass(frozen=True)
class StageRecord:
    name: str
    pairs: int
    q_points: int
    panels: int
    order: int
    grid_power: int
    t0_points: int
    batch_pairs: int
    q_chunk: int
    seconds: float
    node_evaluations: int
    logical_parameter_tuples_upper: int
    worst_bound: float
    device_used_GiB_at_end: float


def gpu_info() -> dict:
    device = cp.cuda.runtime.getDevice()
    props = cp.cuda.runtime.getDeviceProperties(device)
    name = props.get("name", b"unknown")
    if isinstance(name, bytes):
        name = name.decode(errors="replace")
    free_b, total_b = cp.cuda.runtime.memGetInfo()
    return {
        "device": int(device),
        "name": str(name),
        "compute_capability": (
            int(props.get("major", -1)), int(props.get("minor", -1))
        ),
        "memory_free_GiB": free_b / 2**30,
        "memory_total_GiB": total_b / 2**30,
        "cupy": cp.__version__,
        "python": platform.python_version(),
    }


def configure_gpu_memory(requested_gib: float) -> dict:
    """Set a pool limit and a target working-set size.

    On an A100 80 GB the default request of 60 GiB makes the batch estimator
    aim at roughly 60 GiB.  On smaller devices it automatically uses at most
    78% of physical memory.  CuPy's pool is deliberately not flushed between
    ordinary batches, so nvidia-smi should show a persistently large allocation
    after the first full batch.
    """
    free_b, total_b = cp.cuda.runtime.memGetInfo()
    requested = int(requested_gib * 2**30)
    target = min(requested, int(0.78 * total_b))
    limit = min(int(0.94 * total_b), max(target + 2 * 2**30, target))
    pool = cp.get_default_memory_pool()
    pool.set_limit(size=limit)
    return {
        "target_working_set_GiB": target / 2**30,
        "pool_limit_GiB": limit / 2**30,
        "physical_GiB": total_b / 2**30,
        "initial_free_GiB": free_b / 2**30,
    }


def memory_snapshot() -> dict:
    free_b, total_b = cp.cuda.runtime.memGetInfo()
    pool = cp.get_default_memory_pool()
    return {
        "device_used_GiB": (total_b - free_b) / 2**30,
        "device_free_GiB": free_b / 2**30,
        "pool_used_GiB": pool.used_bytes() / 2**30,
        "pool_total_GiB": pool.total_bytes() / 2**30,
    }


def B_rho(rho: cp.ndarray) -> cp.ndarray:
    # Cancellation-free identity also used by the rigorous code.
    r2 = rho * rho
    b2 = (r2 - 1.0) * (
        1.0 + (r2 + 9.0) / (rho * cp.sqrt(r2 + 8.0) + 3.0)
    ) / 2.0
    return cp.sqrt(cp.maximum(b2, 0.0))


def stable_power(base: cp.ndarray, exponent: cp.ndarray) -> cp.ndarray:
    return cp.where(base > 0.0, cp.exp(exponent * cp.log(base)), 0.0)


def geometric_power_sum(a: cp.ndarray, c: cp.ndarray, n: cp.ndarray) -> cp.ndarray:
    """sum_{j=0}^{n-1} a^j c^(n-1-j), stably for 0<=c<=a<=1."""
    positive = a > 0.0
    ratio = cp.where(positive, c / cp.maximum(a, 1e-300), 0.0)
    ratio = cp.clip(ratio, 0.0, 1.0)
    den = 1.0 - ratio
    log_ratio = cp.where(ratio > 0.0, cp.log(ratio), -cp.inf)
    numerator = -cp.expm1(n * log_ratio)
    factor = cp.where(den > 2e-10, numerator / cp.maximum(den, 1e-300), n)
    a_pow = cp.where(
        positive,
        cp.exp((n - 1.0) * cp.log(cp.maximum(a, 1e-300))),
        0.0,
    )
    return a_pow * factor


def stable_abs_rad_minus_gaussian(
    cos_u: cp.ndarray, n: cp.ndarray, gaussian: cp.ndarray
) -> cp.ndarray:
    """Stable |cos(u)^n-exp(-n u^2/2)|.

    The direct subtraction loses relative precision for large n and small u.
    For equal signs use a log-domain expm1 difference; for opposite signs use
    the exact sum of magnitudes.
    """
    c = cp.abs(cos_u)
    log_rad = cp.where(c > 0.0, n * cp.log(c), -cp.inf)
    log_g = cp.log(cp.maximum(gaussian, 1e-300))
    hi = cp.maximum(log_rad, log_g)
    lo = cp.minimum(log_rad, log_g)
    same_sign = (cos_u >= 0.0) | ((n.astype(cp.int64) % 2) == 0)
    same = cp.exp(hi) * (-cp.expm1(lo - hi))
    opposite = cp.exp(log_rad) + gaussian
    return cp.where(same_sign, same, opposite)


def majorants_scaled(
    s: cp.ndarray, q: cp.ndarray, n_int: cp.ndarray, rho: cp.ndarray
) -> tuple[cp.ndarray, cp.ndarray, cp.ndarray]:
    """Pointwise majorants in scaled variables.

    Shapes are broadcast-compatible with
        s=(1,1,P,G), q=(1,Q,1,1), n,rho=(B,1,1,1).
    """
    n = n_int.astype(cp.float64)
    rp1 = rho + 1.0
    z = q * s
    u = z / rp1
    abs_u = cp.abs(u)
    cos_u = cp.cos(u)
    c = cp.abs(cos_u)

    b = B_rho(rho)
    delta = b * abs_u**3 / 6.0
    a = cp.minimum(1.0, c + delta)
    c_n = stable_power(c, n)
    d_power = delta * geometric_power_sum(a, c, n)
    d_direct = n * delta
    d_rad = cp.minimum(cp.minimum(d_power, d_direct), 2.0)

    gaussian = cp.exp(-0.5 * n * u * u)
    rad_gauss = stable_abs_rad_minus_gaussian(cos_u, n, gaussian)
    R = cp.minimum(2.0, rad_gauss + d_rad)

    m_rad = cp.minimum(1.0, c_n + d_rad)
    denom = rp1 * rp1
    chi_1 = (0.5 * z * z - KAPPA * cp.abs(z) ** 3) / denom
    chi_2 = (1.0 - cp.cos(z)) / denom
    chi_n = cp.where(
        cp.abs(z) <= THETA0,
        chi_1,
        cp.where(cp.abs(z) <= TWO_PI, chi_2, 0.0),
    )
    chi_n = cp.maximum(chi_n, 0.0)
    base = cp.clip(1.0 - 2.0 * chi_n, 0.0, 1.0)
    m_prawitz = stable_power(base, 0.5 * n)
    M = cp.clip(cp.minimum(m_rad, m_prawitz), 0.0, 1.0)
    return R, M, gaussian


def kernel_K_abs(s: cp.ndarray) -> cp.ndarray:
    x = PI * s
    r = 1.0 - s
    cot = cp.cos(x) / cp.sin(x)
    # Stable (1-s)cot(pi s) near s=1.
    prod_near_1 = (
        -1.0 / PI
        + PI * r * r / 3.0
        + PI**3 * r**4 / 45.0
        + 2.0 * PI**5 * r**6 / 945.0
    )
    prod = cp.where(r < 2e-3, prod_near_1, r * cot)
    return cp.hypot(0.5 * r, 0.5 * (prod + 1.0 / PI))


def kernel_L_abs_series(s: cp.ndarray, terms: int) -> cp.ndarray:
    """Positive partial-fraction upper model for |K-i/(2*pi*s)|.

    It mirrors the stable m-term formula and explicit tail used by Arb.  This
    is evaluated in float64 for reconnaissance only.
    """
    x = PI * s
    x2 = x * x
    pi2 = PI * PI
    total = cp.zeros_like(s)
    for k in range(1, terms + 1):
        total += 1.0 / (k * k * pi2 - x2)
    tail = 1.0 / (
        terms * (pi2 - x2 / ((terms + 1) * (terms + 1)))
    )
    d_upper = 2.0 * x * (total + tail)
    r = 1.0 - s
    return cp.hypot(0.5 * r, 0.5 * r * d_upper)


@dataclass
class GLGrid:
    spec: GridSpec
    panels: int
    boundaries: cp.ndarray
    nodes: cp.ndarray
    weights: cp.ndarray
    k_abs: cp.ndarray
    l_by_m: dict[int, cp.ndarray]
    t0_indices: cp.ndarray


def build_grid(spec: GridSpec) -> GLGrid:
    x, w = np.polynomial.legendre.leggauss(spec.order)
    # Mirror the formal geometry: strong concentration only near zero, then a
    # uniform safety mesh over the t0/second-integral region.  Explicit t0
    # anchors keep known hard values such as 0.41 and 0.50 available even in
    # the cheapest global pass.
    lower_count = max(8, spec.panels // 2)
    upper_count = max(8, spec.panels - lower_count)
    lower_u = np.linspace(0.0, 1.0, lower_count + 1, dtype=np.float64)
    lower = 0.25 * lower_u**spec.power
    upper = np.linspace(0.25, 1.0, upper_count + 1, dtype=np.float64)
    anchors = np.array(
        [0.25, 1.0/3.0, 0.40, 0.41, 0.50, 0.60, 0.75, 0.90, 1.0],
        dtype=np.float64,
    )
    boundaries_np = np.unique(np.concatenate([lower, upper, anchors]))
    actual_panels = len(boundaries_np) - 1
    left = boundaries_np[:-1, None]
    right = boundaries_np[1:, None]
    nodes_np = 0.5 * (left + right) + 0.5 * (right - left) * x[None, :]
    weights_np = 0.5 * (right - left) * w[None, :]

    t_candidates = np.flatnonzero(
        (boundaries_np >= spec.t0_min) & (boundaries_np <= spec.t0_max)
    )
    t_candidates = t_candidates[(t_candidates > 0) & (t_candidates < actual_panels)]
    if len(t_candidates) > spec.max_t0_points:
        choose = np.rint(
            np.linspace(0, len(t_candidates) - 1, spec.max_t0_points)
        ).astype(np.int64)
        t_candidates = np.unique(t_candidates[choose])

    nodes = cp.asarray(nodes_np)
    return GLGrid(
        spec=spec,
        panels=actual_panels,
        boundaries=cp.asarray(boundaries_np),
        nodes=nodes,
        weights=cp.asarray(weights_np),
        k_abs=kernel_K_abs(nodes),
        l_by_m={m: kernel_L_abs_series(nodes, m) for m in M_VALUES},
        t0_indices=cp.asarray(t_candidates, dtype=cp.int64),
    )


def make_q_grid(count: int, lo: float = 4.35, hi: float = 7.05) -> np.ndarray:
    # Broad coverage plus additional density around 2*pi and observed hard area.
    base = np.linspace(lo, hi, count, dtype=np.float64)
    dense = np.linspace(5.85, 6.50, max(17, count // 2), dtype=np.float64)
    anchors = np.array(
        [5.5, 5.75, 5.94, 6.0, 6.10, 6.18, 6.20, 6.24, 6.25,
         TWO_PI, 6.30, 6.35, 6.42, 6.5, 6.75, 7.0],
        dtype=np.float64,
    )
    q = np.unique(np.concatenate([base, dense, anchors]))
    return q[(q >= lo) & (q <= hi)]


def estimate_batch_pairs(
    grid: GLGrid,
    q_chunk: int,
    target_bytes: int,
    requested_max: int = 65536,
) -> int:
    nodes = grid.panels * grid.spec.order
    panels = grid.panels
    # Deliberately conservative model of live float64 and index temporaries.
    bytes_per_pair = q_chunk * (
        nodes * 8 * 18 + panels * 8 * 18 + (panels + 1) * 8 * 14
    )
    return max(1, min(requested_max, int(0.92 * target_bytes / bytes_per_pair)))


def _prefix(panel_values: cp.ndarray) -> cp.ndarray:
    zeros = cp.zeros(panel_values.shape[:2] + (1,), dtype=panel_values.dtype)
    return cp.concatenate([zeros, cp.cumsum(panel_values, axis=2)], axis=2)


_CUMMIN_WITH_ARG_KERNEL = cp.RawKernel(
    r"""
    extern "C" __global__
    void cummin_with_arg_f64(
        const double* values,
        double* cumulative,
        int* arg,
        const long long rows,
        const int width
    ) {
        const long long row = (long long)blockDim.x * blockIdx.x + threadIdx.x;
        if (row >= rows) return;

        const long long base = row * (long long)width;
        double best = values[base];
        int best_i = 0;
        cumulative[base] = best;
        arg[base] = best_i;

        for (int k = 1; k < width; ++k) {
            const double v = values[base + k];
            // The latest equal minimum is the canonical tie winner.
            if (v <= best) {
                best = v;
                best_i = k;
            }
            cumulative[base + k] = best;
            arg[base + k] = best_i;
        }
    }
    """,
    "cummin_with_arg_f64",
)


def _cummin_with_arg(values: cp.ndarray) -> tuple[cp.ndarray, cp.ndarray]:
    """Running minimum and latest argmin along axis 2.

    CuPy 14 does not implement ``cp.minimum.accumulate``.  This kernel
    handles the exact 3-D float64 layout used by the GPU search.
    """
    if values.ndim != 3:
        raise ValueError(f"expected a 3-D array, got shape={values.shape}")
    if values.dtype != cp.float64:
        values = values.astype(cp.float64, copy=False)
    values = cp.ascontiguousarray(values)

    rows = int(values.shape[0]) * int(values.shape[1])
    width = int(values.shape[2])
    cumulative = cp.empty_like(values)
    arg = cp.empty(values.shape, dtype=cp.int32)

    if rows == 0 or width == 0:
        return cumulative, arg

    threads = 256
    blocks = (rows + threads - 1) // threads
    _CUMMIN_WITH_ARG_KERNEL(
        (blocks,),
        (threads,),
        (values, cumulative, arg, np.int64(rows), np.int32(width)),
    )
    return cumulative, arg


def _scan_batch(
    n_cpu: np.ndarray,
    rho_cpu: np.ndarray,
    q_values: np.ndarray,
    grid: GLGrid,
    q_chunk: int,
    m_slack: float,
) -> pd.DataFrame:
    B = len(n_cpu)
    n4 = cp.asarray(n_cpu, dtype=cp.int32)[:, None, None, None]
    r4 = cp.asarray(rho_cpu, dtype=cp.float64)[:, None, None, None]
    n2 = n4[:, 0, 0, 0].astype(cp.float64)
    r2 = r4[:, 0, 0, 0]

    best_bound = cp.full(B, cp.inf)
    best_q = cp.full(B, cp.nan)
    best_t0 = cp.full(B, cp.nan)
    best_eta = cp.full(B, cp.nan)
    best_lam = cp.full(B, cp.nan)
    best_m = cp.full(B, -1, dtype=cp.int32)

    s4 = grid.nodes[None, None, :, :]
    w4 = grid.weights[None, None, :, :]
    k4 = grid.k_abs[None, None, :, :]
    boundaries = grid.boundaries
    t_idx = grid.t0_indices
    t_values = boundaries[t_idx]
    boundary4 = boundaries[None, None, :]

    for qlo in range(0, len(q_values), q_chunk):
        qhi = min(qlo + q_chunk, len(q_values))
        q_cpu = q_values[qlo:qhi]
        q4 = cp.asarray(q_cpu)[None, :, None, None]
        q2 = q4[:, :, 0, 0]

        R, M, gaussian = majorants_scaled(s4, q4, n4, r4)
        first_panel = cp.sum(2.0 * k4 * R * w4, axis=3)
        second_panel = cp.sum(2.0 * k4 * M * w4, axis=3)
        first_pre = _prefix(first_panel)
        second_pre = _prefix(second_panel)

        T = q2 * cp.sqrt(n2)[:, None] / (r2[:, None] + 1.0)
        b = B_rho(r2)[:, None]
        eta = boundary4
        local = (
            b[:, :, None] * T[:, :, None] ** 3 * eta**3
            / (9.0 * cp.sqrt(n2)[:, None, None])
            + T[:, :, None] ** 4 * eta**4 / (12.0 * n2[:, None, None])
        )
        eta_valid = (
            (eta > 0.0)
            & (eta <= 0.5)
            & (q2[:, :, None] * eta <= r2[:, None, None] + 1.0)
        )
        eta_raw = cp.where(eta_valid, local - first_pre, cp.inf)
        eta_cum, eta_arg = _cummin_with_arg(eta_raw)

        third_best = cp.full(first_pre.shape, cp.inf)
        third_best_lam_arg = cp.full(first_pre.shape, -1, dtype=cp.int32)
        third_best_m = cp.full(first_pre.shape, -1, dtype=cp.int32)
        lam_coeff = math.sqrt(1.0 + 4.0 / (PI * PI))
        lam_valid = (boundary4 > 0.0) & (boundary4 <= 0.5)

        # Ascending m and a tolerance implement: use the smallest m unless a
        # larger m produces a material improvement.
        for m in M_VALUES:
            l4 = grid.l_by_m[m][None, None, :, :]
            third_panel = cp.sum(2.0 * l4 * gaussian * w4, axis=3)
            third_pre = _prefix(third_panel)
            lam_raw = cp.where(
                lam_valid,
                lam_coeff * boundary4 - third_pre,
                cp.inf,
            )
            lam_cum, lam_arg = _cummin_with_arg(lam_raw)
            candidate = third_pre + lam_cum
            improve = candidate < (third_best - m_slack)
            third_best = cp.where(improve, candidate, third_best)
            third_best_lam_arg = cp.where(improve, lam_arg, third_best_lam_arg)
            third_best_m = cp.where(improve, m, third_best_m)

        first_t = first_pre[:, :, t_idx]
        second_t = second_pre[:, :, -1][:, :, None] - second_pre[:, :, t_idx]
        eta_t = eta_cum[:, :, t_idx]
        third_t = third_best[:, :, t_idx]
        tail_arg = 0.5 * (T[:, :, None] * t_values[None, None, :]) ** 2
        tail = cp_exp1(tail_arg) / (2.0 * PI)

        U = first_t + eta_t + second_t + third_t + tail
        normalized = U * cp.sqrt(n2)[:, None, None] / r2[:, None, None]
        flat = normalized.reshape(B, -1)
        arg = cp.argmin(flat, axis=1)
        rows = cp.arange(B)
        local_bound = flat[rows, arg]
        nt = len(t_idx)
        iq = arg // nt
        it = arg % nt

        eta_choice = eta_arg[:, :, t_idx].reshape(B, -1)[rows, arg]
        lam_choice = third_best_lam_arg[:, :, t_idx].reshape(B, -1)[rows, arg]
        m_choice = third_best_m[:, :, t_idx].reshape(B, -1)[rows, arg]
        q_vec = q4[0, :, 0, 0]
        local_q = q_vec[iq]
        local_t0 = t_values[it]
        local_eta = boundaries[eta_choice]
        local_lam = boundaries[lam_choice]

        improve = local_bound < best_bound
        best_bound = cp.where(improve, local_bound, best_bound)
        best_q = cp.where(improve, local_q, best_q)
        best_t0 = cp.where(improve, local_t0, best_t0)
        best_eta = cp.where(improve, local_eta, best_eta)
        best_lam = cp.where(improve, local_lam, best_lam)
        best_m = cp.where(improve, m_choice, best_m)

        del (
            R, M, gaussian, first_panel, second_panel, first_pre, second_pre,
            local, eta_raw, eta_cum, eta_arg, third_best,
            third_best_lam_arg, third_best_m, first_t, second_t, eta_t,
            third_t, tail, U, normalized, flat,
        )

    return pd.DataFrame(
        {
            "n": n_cpu.astype(np.int32),
            "rho": rho_cpu.astype(np.float64),
            "bound": cp.asnumpy(best_bound),
            "q": cp.asnumpy(best_q),
            "t0": cp.asnumpy(best_t0),
            "eta": cp.asnumpy(best_eta),
            "lambda": cp.asnumpy(best_lam),
            "m": cp.asnumpy(best_m),
            "panels": grid.panels,
            "order": grid.spec.order,
            "grid_power": grid.spec.power,
        }
    )


def scan_pairs(
    n_values: np.ndarray,
    rho_values: np.ndarray,
    q_values: np.ndarray,
    spec: GridSpec,
    *,
    target_memory_bytes: int,
    q_chunk: int,
    requested_batch: int = 65536,
    m_slack: float = 2e-6,
    stage_name: str,
    checkpoint: Path | None = None,
) -> tuple[pd.DataFrame, StageRecord]:
    grid = build_grid(spec)
    batch = estimate_batch_pairs(grid, q_chunk, target_memory_bytes, requested_batch)
    print(
        f"[{stage_name}] pairs={len(n_values):,}, q={len(q_values)}, "
        f"grid={grid.panels}x{spec.order} (nominal {spec.panels}), power={spec.power}, "
        f"batch={batch:,}, q_chunk={q_chunk}",
        flush=True,
    )
    start = time.perf_counter()
    frames: list[pd.DataFrame] = []
    i = 0
    while i < len(n_values):
        current = min(batch, len(n_values) - i)
        while True:
            try:
                frame = _scan_batch(
                    n_values[i : i + current],
                    rho_values[i : i + current],
                    q_values,
                    grid,
                    q_chunk,
                    m_slack,
                )
                cp.cuda.Stream.null.synchronize()
                break
            except cp.cuda.memory.OutOfMemoryError:
                # OOM is the one situation where releasing the pool is useful.
                cp.get_default_memory_pool().free_all_blocks()
                gc.collect()
                current //= 2
                batch = min(batch, current)
                if current < 1:
                    raise
                print(f"[{stage_name}] OOM -> batch={current}", flush=True)
        frame["stage"] = stage_name
        frames.append(frame)
        i += current
        if len(frames) % 5 == 0 or i == len(n_values):
            elapsed = time.perf_counter() - start
            rate = i / max(elapsed, 1e-9)
            mem = memory_snapshot()
            print(
                f"[{stage_name}] {i:,}/{len(n_values):,} pairs, "
                f"{rate:,.1f} pairs/s, GPU used={mem['device_used_GiB']:.1f} GiB, "
                f"pool={mem['pool_total_GiB']:.1f} GiB",
                flush=True,
            )
            if checkpoint is not None:
                checkpoint.parent.mkdir(parents=True, exist_ok=True)
                pd.concat(frames, ignore_index=True).to_csv(checkpoint, index=False)

    result = pd.concat(frames, ignore_index=True)
    result["margin"] = TARGET - result["bound"]
    result.sort_values("bound", ascending=False, inplace=True, ignore_index=True)
    seconds = time.perf_counter() - start
    record = StageRecord(
        name=stage_name,
        pairs=len(result),
        q_points=len(q_values),
        panels=grid.panels,
        order=spec.order,
        grid_power=spec.power,
        t0_points=int(len(grid.t0_indices)),
        batch_pairs=batch,
        q_chunk=q_chunk,
        seconds=seconds,
        node_evaluations=(
            len(result) * len(q_values) * grid.panels * spec.order
        ),
        logical_parameter_tuples_upper=(
            len(result)
            * len(q_values)
            * int(len(grid.t0_indices))
            * (grid.panels + 1)
            * (grid.panels + 1)
            * len(M_VALUES)
        ),
        worst_bound=float(result.iloc[0]["bound"]),
        device_used_GiB_at_end=float(memory_snapshot()["device_used_GiB"]),
    )
    if checkpoint is not None:
        result.to_csv(checkpoint, index=False)
    del grid
    return result, record
