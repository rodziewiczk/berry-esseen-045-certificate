#!/usr/bin/env python3
"""Deterministically reproduce the publication parameter bank on an A100.

The GPU stage supplies untrusted parameter advice; the Arb checker recomputes
every selected bound.  Content-affecting work is fixed by the publication
profile and refinement plan.  Wall time and memory availability may change
batch sizes and diagnostics, but never the cells or recipes selected for work.

The construction is aligned with the later Arb workflow:

* the rho interval is partitioned into dyadic cells (base depth 6);
* each cell is searched at its centre, then the same candidate is tested at
  five Chebyshev--Lobatto points across the whole cell;
* only difficult/unstable cells are split to depths 7, 8 and 9;
* several recipes are kept per final cell, including cheap, medium, low-bound
  and high-safety alternatives;
* recommended integration grids are stored for immediate deterministic use;
* output is a minimal memory-mapped NPY directory;
* checkpoints are accepted only when bound to the exact source, dependency,
  configuration, and refinement-plan identity.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
from importlib import metadata as importlib_metadata
import json
import math
import os
import platform
import shutil
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd

import cupy as cp
from cupyx.scipy.special import exp1 as cp_exp1

from . import gpu_search as base

TARGET = base.TARGET
RHO_MAX = base.RHO_MAX
N_MAX = base.N_MAX
M_VALUES = base.M_VALUES
TOP_K = 6
PUBLICATION_PROFILE = "publication-a100-v1"
EXPECTED_ROWS = 886_998
EXPECTED_DEPTH_COUNTS = {6: 430_226, 8: 259_884, 9: 196_888}
EXPECTED_DEPTH9_PARENTS = 98_444
EXPECTED_DEPTH9_PARENT_SHA256 = (
    "86d683448a9c46bf8b9d903f6385cc1ba00b8908c4c31d372014e608e2a84bae"
)
EXPECTED_GEOMETRY_SHA256 = (
    "bcbe1ee1f583595a929a55043b10e1637a43cc1c76931eddad621c5ef8a3f849"
)
SAMPLE_FRACTIONS_5 = np.array(
    [0.0, 0.14644660940672624, 0.5, 0.8535533905932737, 1.0],
    dtype=np.float64,
)
SAMPLE_FRACTIONS_9 = 0.5 * (1.0 - np.cos(np.linspace(0.0, math.pi, 9)))


@dataclass(frozen=True)
class LevelSpec:
    depth: int
    search_grid: base.GridSpec
    q_count: int
    q_lo: float
    q_hi: float
    robust_samples: int
    label: str


LEVEL_SPECS = {
    6: LevelSpec(6, base.GridSpec(96, 8, 3, 0.25, 0.90, 192), 65, 4.35, 7.05, 5, "d6_p96"),
    7: LevelSpec(7, base.GridSpec(192, 8, 3, 0.25, 0.90, 320), 105, 5.35, 6.85, 5, "d7_p192"),
    8: LevelSpec(8, base.GridSpec(384, 8, 2, 0.25, 0.90, 384), 145, 5.55, 6.70, 5, "d8_p384"),
    9: LevelSpec(9, base.GridSpec(768, 12, 4, 0.25, 0.90, 512), 181, 5.70, 6.58, 9, "d9_p768"),
}

BOUND_THRESHOLDS = np.array([0.44, 0.445, 0.448, 0.4495, 0.45], dtype=np.float64)
CLASS_LABELS = (
    "very_large_margin",
    "comfortable",
    "good",
    "hard",
    "very_tight",
    "unresolved",
)
SELECTED_FIELDS = {
    "q", "t0", "eta", "lam", "m", "pieces", "order", "grid_power",
    "center_bound", "robust_bound", "rho_sensitivity", "source",
}
GPU_DISTRIBUTIONS = (
    "cupy-cuda12x",
    "cuda-pathfinder",
    "numpy",
    "pandas",
    "python-dateutil",
    "pytz",
    "six",
    "tzdata",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def distribution_fingerprint(name: str) -> dict:
    """Fingerprint the installed wheel metadata and its file-hash manifest."""
    distribution = importlib_metadata.distribution(name)
    files = distribution.files or []
    metadata_files: dict[str, Path] = {}
    for filename in ("METADATA", "WHEEL", "RECORD"):
        matches = [file for file in files if file.name == filename]
        if len(matches) != 1:
            raise RuntimeError(
                f"installed distribution {name!r} has {len(matches)} {filename} files"
            )
        metadata_files[filename] = Path(distribution.locate_file(matches[0]))
    return {
        "name": distribution.metadata["Name"],
        "version": distribution.version,
        "metadata_sha256": sha256_file(metadata_files["METADATA"]),
        "wheel_sha256": sha256_file(metadata_files["WHEEL"]),
        "record_sha256": sha256_file(metadata_files["RECORD"]),
    }


def publication_identity(
    plan_path: Path,
    reference_manifest: Path,
    gpu: dict,
) -> tuple[str, dict]:
    """Hash every content-affecting source, dependency, and profile setting."""
    repository = Path(__file__).resolve().parents[1]
    source_files = {
        "builder": Path(__file__).resolve(),
        "reproduction_package": repository / "reproduction" / "__init__.py",
        "gpu_search": Path(base.__file__).resolve(),
        "refinement_plan": plan_path.resolve(),
        "reference_manifest": reference_manifest.resolve(),
        "gpu_requirements": repository / "requirements-gpu.txt",
    }
    record = {
        "profile": PUBLICATION_PROFILE,
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "cupy": cp.__version__,
        "cuda_runtime": int(cp.cuda.runtime.runtimeGetVersion()),
        "cuda_driver": int(cp.cuda.runtime.driverGetVersion()),
        "gpu": {
            "name": gpu["name"],
            "compute_capability": list(gpu["compute_capability"]),
            "memory_total_GiB": gpu["memory_total_GiB"],
        },
        "distributions": {
            name: distribution_fingerprint(name) for name in GPU_DISTRIBUTIONS
        },
        "sources": {name: sha256_file(path) for name, path in source_files.items()},
        "levels": {
            str(depth): {
                "depth": spec.depth,
                "search_grid": asdict(spec.search_grid),
                "q_count": spec.q_count,
                "q_lo": spec.q_lo,
                "q_hi": spec.q_hi,
                "robust_samples": spec.robust_samples,
                "label": spec.label,
            }
            for depth, spec in LEVEL_SPECS.items()
        },
        "final_refinement_panels": [1536, 3072, 4096],
        "expected_depth9_parents": EXPECTED_DEPTH9_PARENTS,
        "expected_depth9_parent_sha256": EXPECTED_DEPTH9_PARENT_SHA256,
    }
    payload = json.dumps(
        record, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest(), record


def atomic_save_npz(path: Path, **arrays: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as stream:
        np.savez(stream, **arrays)
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=float) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(payload)
    os.replace(tmp, path)


def atomic_copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    shutil.copy2(source, tmp)
    os.replace(tmp, target)


def mirror_file(path: Path, mirror_dir: Path | None) -> None:
    if mirror_dir is None:
        return
    target = mirror_dir / "checkpoints" / path.name
    atomic_copy_file(path, target)


def restore_file(path: Path, mirror_dir: Path | None) -> bool:
    if path.exists() or mirror_dir is None:
        return path.exists()
    source = mirror_dir / "checkpoints" / path.name
    if source.exists():
        atomic_copy_file(source, path)
        return True
    return False


def named_arrays_digest(arrays: dict[str, np.ndarray]) -> str:
    """Return a stable digest of named array payloads, including schema."""
    digest = hashlib.sha256()
    for name in sorted(arrays):
        array = np.ascontiguousarray(np.asarray(arrays[name]))
        encoded_name = name.encode("utf-8")
        encoded_dtype = array.dtype.str.encode("ascii")
        encoded_shape = json.dumps(
            list(array.shape), separators=(",", ":")
        ).encode("ascii")
        for field in (encoded_name, encoded_dtype, encoded_shape):
            digest.update(len(field).to_bytes(8, "little"))
            digest.update(field)
        digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def cell_input_arrays(cells: pd.DataFrame) -> dict[str, np.ndarray]:
    return {
        "n": cells["n"].to_numpy(dtype="<i4"),
        "depth": cells["depth"].to_numpy(dtype="u1"),
        "cell_index": cells["cell_index"].to_numpy(dtype="<i4"),
        "rho_lo": cells["rho_lo"].to_numpy(dtype="<f8"),
        "rho_hi": cells["rho_hi"].to_numpy(dtype="<f8"),
    }


def cell_input_digest(cells: pd.DataFrame) -> str:
    return named_arrays_digest(cell_input_arrays(cells))


def frame_arrays(df: pd.DataFrame) -> dict[str, np.ndarray]:
    return {
        "n": df["n"].to_numpy(np.int32),
        "rho": df["rho"].to_numpy(np.float64),
        "bound": df["bound"].to_numpy(np.float64),
        "q": df["q"].to_numpy(np.float64),
        "t0": df["t0"].to_numpy(np.float64),
        "eta": df["eta"].to_numpy(np.float64),
        "lam": df["lambda"].to_numpy(np.float64),
        "m": df["m"].to_numpy(np.int16),
        "pieces": df["nominal_pieces"].to_numpy(np.int32),
        "actual_panels": df["panels"].to_numpy(np.int32),
        "order": df["order"].to_numpy(np.int16),
        "grid_power": df["grid_power"].to_numpy(np.int16),
    }


def frame_to_npz(df: pd.DataFrame, path: Path, metadata: dict) -> None:
    columns = frame_arrays(df)
    columns["metadata_json"] = np.array(json.dumps(metadata))
    atomic_save_npz(path, **columns)


def frame_from_npz(path: Path) -> tuple[pd.DataFrame, dict]:
    with np.load(path, allow_pickle=False) as z:
        df = pd.DataFrame(
            {
                "n": z["n"], "rho": z["rho"], "bound": z["bound"],
                "q": z["q"], "t0": z["t0"], "eta": z["eta"],
                "lambda": z["lam"], "m": z["m"],
                "nominal_pieces": z["pieces"], "panels": z["actual_panels"],
                "order": z["order"], "grid_power": z["grid_power"],
            }
        )
        meta = json.loads(str(z["metadata_json"].item()))
    return df, meta


def dyadic_cells_all_n(depth: int) -> pd.DataFrame:
    per_n = 1 << depth
    ns = np.arange(2, N_MAX + 1, dtype=np.int32)
    idx = np.tile(np.arange(per_n, dtype=np.int32), len(ns))
    n = np.repeat(ns, per_n)
    width = (RHO_MAX - 1.0) / per_n
    lo = 1.0 + idx.astype(np.float64) * width
    hi = lo + width
    hi[idx == per_n - 1] = RHO_MAX
    return pd.DataFrame(
        {
            "n": n,
            "depth": np.full(len(n), depth, dtype=np.uint8),
            "cell_index": idx,
            "rho_lo": lo,
            "rho_hi": hi,
            "rho": 0.5 * (lo + hi),
        }
    )


def split_cells(cells: pd.DataFrame) -> pd.DataFrame:
    n = np.repeat(cells["n"].to_numpy(np.int32), 2)
    depth = int(cells["depth"].iloc[0]) + 1
    parent_idx = np.repeat(cells["cell_index"].to_numpy(np.int32), 2)
    side = np.tile(np.array([0, 1], dtype=np.int32), len(cells))
    idx = 2 * parent_idx + side
    lo0 = np.repeat(cells["rho_lo"].to_numpy(np.float64), 2)
    hi0 = np.repeat(cells["rho_hi"].to_numpy(np.float64), 2)
    mid = 0.5 * (lo0 + hi0)
    lo = np.where(side == 0, lo0, mid)
    hi = np.where(side == 0, mid, hi0)
    parent_row = np.repeat(np.arange(len(cells), dtype=np.int64), 2)
    return pd.DataFrame(
        {
            "n": n,
            "depth": np.full(len(n), depth, dtype=np.uint8),
            "cell_index": idx,
            "rho_lo": lo,
            "rho_hi": hi,
            "rho": 0.5 * (lo + hi),
            "parent_row": parent_row,
        }
    )


def make_q_grid(spec: LevelSpec) -> np.ndarray:
    return base.make_q_grid(spec.q_count, spec.q_lo, spec.q_hi)


def run_center_search(
    cells: pd.DataFrame,
    spec: LevelSpec,
    *,
    target_memory_bytes: int,
    q_chunk: int,
    outdir: Path,
    mirror_dir: Path | None,
    profile_sha256: str,
) -> tuple[pd.DataFrame, dict]:
    checkpoint = outdir / "checkpoints" / f"center_{spec.label}.npz"
    input_sha256 = cell_input_digest(cells)
    if restore_file(checkpoint, mirror_dir):
        try:
            df, meta = frame_from_npz(checkpoint)
            valid = (
                len(df) == len(cells)
                and meta.get("depth") == spec.depth
                and meta.get("profile_sha256") == profile_sha256
                and meta.get("input_sha256") == input_sha256
                and meta.get("payload_sha256")
                == named_arrays_digest(frame_arrays(df))
                and np.array_equal(
                    df["n"].to_numpy(np.int32),
                    cells["n"].to_numpy(np.int32),
                )
                and np.array_equal(
                    df["rho"].to_numpy(np.float64),
                    cells["rho"].to_numpy(np.float64),
                )
            )
        except Exception as exc:
            # Checkpoints are optional acceleration data. Any decoding or
            # schema failure must fall back to deterministic recomputation.
            print(f"[{spec.label}] ignoring unreadable checkpoint: {exc}", flush=True)
            valid = False
        if valid:
            print(f"[{spec.label}] restored {len(df):,} center rows", flush=True)
            return df, meta
        print(f"[{spec.label}] checkpoint provenance mismatch; recomputing", flush=True)

    q = make_q_grid(spec)
    result, record = base.scan_pairs(
        cells["n"].to_numpy(np.int32),
        cells["rho"].to_numpy(np.float64),
        q,
        spec.search_grid,
        target_memory_bytes=target_memory_bytes,
        q_chunk=q_chunk,
        requested_batch=65536,
        m_slack=1e-7,
        stage_name=f"center_{spec.label}",
        checkpoint=None,
    )
    result["nominal_pieces"] = spec.search_grid.panels
    result.sort_values(["n", "rho"], inplace=True, ignore_index=True)
    meta = {
        "profile_sha256": profile_sha256,
        "depth": spec.depth,
        "label": spec.label,
        "input_sha256": input_sha256,
        "payload_sha256": named_arrays_digest(frame_arrays(result)),
        "grid": asdict(spec.search_grid),
        "q_points": len(q),
        "record": asdict(record),
    }
    frame_to_npz(result, checkpoint, meta)
    mirror_file(checkpoint, mirror_dir)
    return result, meta


def _grid_boundaries_numpy(spec: base.GridSpec) -> np.ndarray:
    lower_count = max(8, spec.panels // 2)
    upper_count = max(8, spec.panels - lower_count)
    lower_u = np.linspace(0.0, 1.0, lower_count + 1, dtype=np.float64)
    lower = 0.25 * lower_u**spec.power
    upper = np.linspace(0.25, 1.0, upper_count + 1, dtype=np.float64)
    anchors = np.array(
        [0.25, 1.0 / 3.0, 0.40, 0.41, 0.50, 0.60, 0.75, 0.90, 1.0],
        dtype=np.float64,
    )
    return np.unique(np.concatenate([lower, upper, anchors]))


def _nearest_boundary_indices(boundaries: np.ndarray, values: np.ndarray) -> np.ndarray:
    pos = np.searchsorted(boundaries, values, side="left")
    pos = np.clip(pos, 1, len(boundaries) - 1)
    left = boundaries[pos - 1]
    right = boundaries[pos]
    choose_right = np.abs(right - values) < np.abs(values - left)
    out = pos - 1 + choose_right.astype(np.int64)
    return np.clip(out, 0, len(boundaries) - 1).astype(np.int32)


def _release_unused_gpu_memory() -> None:
    """Release unused CuPy pool blocks without invalidating live arrays."""
    try:
        cp.cuda.Stream.null.synchronize()
    except Exception:
        pass
    gc.collect()
    cp.get_default_memory_pool().free_all_blocks()
    cp.get_default_pinned_memory_pool().free_all_blocks()


def evaluate_fixed_points(
    n: np.ndarray,
    rho: np.ndarray,
    q: np.ndarray,
    t0: np.ndarray,
    eta: np.ndarray,
    lam: np.ndarray,
    m: int,
    spec: base.GridSpec,
    *,
    target_memory_bytes: int,
    label: str,
) -> np.ndarray:
    """Evaluate fixed recipes pointwise on GPU; no parameter minimisation.

    Uses a conservative live-memory estimate. If CuPy still raises OOM, the
    exact same unfinished chunk is retried with half the batch size.
    """
    if not (len(n) == len(rho) == len(q) == len(t0) == len(eta) == len(lam)):
        raise ValueError("fixed-evaluation arrays must have equal lengths")
    if len(n) == 0:
        return np.empty(0, dtype=np.float64)

    # Recipes with different shapes fragment CuPy's cache. Free only unused
    # blocks before constructing the next reusable quadrature grid.
    _release_unused_gpu_memory()

    grid = base.build_grid(spec)
    boundaries_np = _grid_boundaries_numpy(spec)
    t_idx_cpu = _nearest_boundary_indices(boundaries_np, t0)
    eta_idx_cpu = _nearest_boundary_indices(boundaries_np, eta)
    lam_idx_cpu = _nearest_boundary_indices(boundaries_np, lam)

    nodes = grid.panels * spec.order
    raw_bytes_per_point = nodes * 8 * 16 + grid.panels * 8 * 12
    # Several broadcast temporaries coexist during ``majorants_scaled``.
    # This factor fills tens of GiB on an A100 80 GB while reserving space for
    # an additional multi-GiB temporary.
    estimated_live_bytes_per_point = max(1, int(3.25 * raw_bytes_per_point))

    free_b, _ = cp.cuda.runtime.memGetInfo()
    usable = min(int(target_memory_bytes), int(0.82 * free_b))
    batch = max(
        1,
        min(
            98304,
            int(usable / estimated_live_bytes_per_point),
        ),
    )

    out = np.empty(len(n), dtype=np.float64)
    start = time.perf_counter()

    s4 = grid.nodes[None, None, :, :]
    w4 = grid.weights[None, None, :, :]
    k4 = grid.k_abs[None, None, :, :]
    l4 = grid.l_by_m[int(m)][None, None, :, :]
    lam_coeff = math.sqrt(1.0 + 4.0 / (math.pi * math.pi))

    print(
        f"[{label}] safe_batch={batch:,}, free={free_b/2**30:.1f} GiB, "
        f"estimated={estimated_live_bytes_per_point/2**10:.1f} KiB/point",
        flush=True,
    )

    def _run_chunk(lo: int, hi: int) -> np.ndarray:
        # Keeping all large temporaries in this nested scope ensures that an
        # exception drops their Python references before the retry.
        n4 = cp.asarray(n[lo:hi], dtype=cp.int32)[:, None, None, None]
        r4 = cp.asarray(rho[lo:hi], dtype=cp.float64)[:, None, None, None]
        q4 = cp.asarray(q[lo:hi], dtype=cp.float64)[:, None, None, None]
        n1 = n4[:, 0, 0, 0].astype(cp.float64)
        r1 = r4[:, 0, 0, 0]
        q1 = q4[:, 0, 0, 0]

        R, M, gaussian = base.majorants_scaled(s4, q4, n4, r4)
        first_panel = cp.sum(2.0 * k4 * R * w4, axis=3)[:, 0, :]
        second_panel = cp.sum(2.0 * k4 * M * w4, axis=3)[:, 0, :]
        third_panel = cp.sum(2.0 * l4 * gaussian * w4, axis=3)[:, 0, :]

        count = hi - lo
        first_pre = cp.concatenate(
            [cp.zeros((count, 1), dtype=cp.float64),
             cp.cumsum(first_panel, axis=1)],
            axis=1,
        )
        second_pre = cp.concatenate(
            [cp.zeros((count, 1), dtype=cp.float64),
             cp.cumsum(second_panel, axis=1)],
            axis=1,
        )
        third_pre = cp.concatenate(
            [cp.zeros((count, 1), dtype=cp.float64),
             cp.cumsum(third_panel, axis=1)],
            axis=1,
        )

        ti = cp.asarray(t_idx_cpu[lo:hi], dtype=cp.int32)
        ei = cp.asarray(eta_idx_cpu[lo:hi], dtype=cp.int32)
        li = cp.asarray(lam_idx_cpu[lo:hi], dtype=cp.int32)
        rows = cp.arange(count)
        t_val = cp.asarray(boundaries_np[t_idx_cpu[lo:hi]], dtype=cp.float64)
        e_val = cp.asarray(boundaries_np[eta_idx_cpu[lo:hi]], dtype=cp.float64)
        l_val = cp.asarray(boundaries_np[lam_idx_cpu[lo:hi]], dtype=cp.float64)

        T = q1 * cp.sqrt(n1) / (r1 + 1.0)
        b = base.B_rho(r1)
        local_eta = (
            b * T**3 * e_val**3 / (9.0 * cp.sqrt(n1))
            + T**4 * e_val**4 / (12.0 * n1)
        )
        first = first_pre[rows, ti] + local_eta - first_pre[rows, ei]
        second = second_pre[:, -1] - second_pre[rows, ti]
        third = third_pre[rows, ti] - third_pre[rows, li] + lam_coeff * l_val
        tail = cp_exp1(0.5 * (T * t_val) ** 2) / (2.0 * math.pi)
        normalized = (first + second + third + tail) * cp.sqrt(n1) / r1

        result = cp.asnumpy(normalized)
        cp.cuda.Stream.null.synchronize()
        return result

    lo = 0
    completed_chunks = 0
    while lo < len(n):
        current = min(batch, len(n) - lo)
        while True:
            try:
                out[lo:lo + current] = _run_chunk(lo, lo + current)
                break
            except cp.cuda.memory.OutOfMemoryError:
                if current <= 1:
                    raise
                attempted_batch = current
                current = max(1, current // 2)
                batch = min(batch, current)
                _release_unused_gpu_memory()
                free_now, _ = cp.cuda.runtime.memGetInfo()
                print(
                    f"[{label}] OOM batch={attempted_batch:,} -> "
                    f"retry={current:,}; "
                    f"free={free_now/2**30:.1f} GiB",
                    flush=True,
                )

        lo += current
        completed_chunks += 1
        if completed_chunks % 10 == 0 or lo == len(n):
            elapsed = time.perf_counter() - start
            print(
                f"[{label}] {lo:,}/{len(n):,} fixed points, "
                f"{lo/max(elapsed,1e-9):,.0f}/s, batch={batch:,}",
                flush=True,
            )

    del grid, s4, w4, k4, l4
    _release_unused_gpu_memory()
    return out


def empty_candidate_arrays(n_rows: int, k: int) -> dict[str, np.ndarray]:
    return {
        "q": np.full((n_rows, k), np.nan, np.float64),
        "t0": np.full((n_rows, k), np.nan, np.float64),
        "eta": np.full((n_rows, k), np.nan, np.float64),
        "lam": np.full((n_rows, k), np.nan, np.float64),
        "m": np.full((n_rows, k), -1, np.int16),
        "pieces": np.full((n_rows, k), -1, np.int32),
        "order": np.full((n_rows, k), -1, np.int16),
        "grid_power": np.full((n_rows, k), -1, np.int16),
        "center_bound": np.full((n_rows, k), np.inf, np.float64),
        "robust_bound": np.full((n_rows, k), np.inf, np.float64),
        "rho_sensitivity": np.full((n_rows, k), np.inf, np.float64),
        "source": np.full((n_rows, k), -1, np.int16),
    }


def _copy_candidate(
    dst: dict[str, np.ndarray],
    j: int,
    src: pd.DataFrame,
    rows: np.ndarray,
    source: int,
) -> None:
    dst["q"][:, j] = src["q"].to_numpy(np.float64)[rows]
    dst["t0"][:, j] = src["t0"].to_numpy(np.float64)[rows]
    dst["eta"][:, j] = src["eta"].to_numpy(np.float64)[rows]
    dst["lam"][:, j] = src["lambda"].to_numpy(np.float64)[rows]
    dst["m"][:, j] = src["m"].to_numpy(np.int16)[rows]
    dst["pieces"][:, j] = src["nominal_pieces"].to_numpy(np.int32)[rows]
    dst["order"][:, j] = src["order"].to_numpy(np.int16)[rows]
    dst["grid_power"][:, j] = src["grid_power"].to_numpy(np.int16)[rows]
    dst["center_bound"][:, j] = src["bound"].to_numpy(np.float64)[rows]
    dst["source"][:, j] = source


def build_candidate_pool(
    cells: pd.DataFrame,
    center: pd.DataFrame,
    *,
    auxiliary_centers: list[pd.DataFrame] | None = None,
    parent_candidates: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    """Own/left/right/interpolated/safety/known/auxiliary/parent recipes."""
    n_rows = len(cells)
    auxiliary_centers = auxiliary_centers or []
    extra = 2 * len(auxiliary_centers) + (2 if parent_candidates is not None else 0)
    pool = empty_candidate_arrays(n_rows, 8 + extra)
    own = np.arange(n_rows, dtype=np.int64)

    # Cells are sorted by (n,rho); neighbour indices must remain within n.
    nvals = cells["n"].to_numpy(np.int32)
    left = np.maximum(own - 1, 0)
    right = np.minimum(own + 1, n_rows - 1)
    left[nvals[left] != nvals] = own[nvals[left] != nvals]
    right[nvals[right] != nvals] = own[nvals[right] != nvals]

    _copy_candidate(pool, 0, center, own, 0)
    _copy_candidate(pool, 1, center, left, 1)
    _copy_candidate(pool, 2, center, right, 2)

    # Interpolate neighbouring basins; use conservative larger m.
    for name in ("q", "t0", "eta", "lam"):
        pool[name][:, 3] = 0.5 * (pool[name][:, 1] + pool[name][:, 2])
    pool["m"][:, 3] = np.maximum(pool["m"][:, 1], pool["m"][:, 2])
    pool["pieces"][:, 3] = np.maximum(pool["pieces"][:, 1], pool["pieces"][:, 2])
    pool["order"][:, 3] = np.maximum(pool["order"][:, 1], pool["order"][:, 2])
    pool["grid_power"][:, 3] = pool["grid_power"][:, 0]
    pool["center_bound"][:, 3] = np.minimum(pool["center_bound"][:, 1], pool["center_bound"][:, 2])
    pool["source"][:, 3] = 3

    # Same geometric seed with m=100 is a cheap insurance candidate.
    for name in ("q", "t0", "eta", "lam", "pieces", "order", "grid_power", "center_bound"):
        pool[name][:, 4] = pool[name][:, 0]
    pool["m"][:, 4] = 100
    pool["source"][:, 4] = 4

    # Known hard anchors remain available even if the coarse q grid misses them.
    pool["q"][:, 5] = pool["q"][:, 0]
    pool["t0"][:, 5] = pool["t0"][:, 0]
    pool["eta"][:, 5] = pool["eta"][:, 0]
    pool["lam"][:, 5] = pool["lam"][:, 0]
    pool["m"][:, 5] = pool["m"][:, 0]
    pool["pieces"][:, 5] = np.maximum(pool["pieces"][:, 0], 2 * pool["pieces"][:, 0])
    pool["order"][:, 5] = pool["order"][:, 0]
    pool["grid_power"][:, 5] = pool["grid_power"][:, 0]
    pool["center_bound"][:, 5] = pool["center_bound"][:, 0]
    pool["source"][:, 5] = 5

    # Explicit known hard cases from earlier formal experiments.
    n_array = cells["n"].to_numpy(np.int32)
    known = np.isin(n_array, np.array([2, 3], dtype=np.int32))
    pool["q"][known, 6] = np.where(n_array[known] == 2, 5.94, 6.24)
    pool["t0"][known, 6] = np.where(n_array[known] == 2, 0.50, 0.41)
    pool["eta"][known, 6] = 1.0 / 1024.0
    pool["lam"][known, 6] = 1.0 / 1024.0
    pool["m"][known, 6] = 100
    pool["pieces"][known, 6] = 4096
    pool["order"][known, 6] = 12
    pool["grid_power"][known, 6] = 3
    pool["center_bound"][known, 6] = np.inf
    pool["source"][known, 6] = 6

    # Expensive safety recipe only where the centre scan already looks hard.
    hard = pool["center_bound"][:, 0] >= 0.447
    for name in ("q", "t0", "eta", "lam"):
        pool[name][hard, 7] = pool[name][hard, 0]
    pool["m"][hard, 7] = 100
    pool["pieces"][hard, 7] = 4096
    pool["order"][hard, 7] = 12
    pool["grid_power"][hard, 7] = pool["grid_power"][hard, 0]
    pool["center_bound"][hard, 7] = pool["center_bound"][hard, 0]
    pool["source"][hard, 7] = 7

    offset = 8
    for aux_i, aux in enumerate(auxiliary_centers):
        _copy_candidate(pool, offset, aux, own, 20 + 2 * aux_i)
        _copy_candidate(pool, offset + 1, aux, own, 21 + 2 * aux_i)
        pool["m"][:, offset + 1] = 100
        offset += 2

    if parent_candidates is not None:
        parent_rows = cells["parent_row"].to_numpy(np.int64)
        for parent_rank in (0, 3):
            for name in (
                "q", "t0", "eta", "lam", "m", "pieces", "order",
                "grid_power", "center_bound",
            ):
                pool[name][:, offset] = parent_candidates[name][parent_rows, parent_rank]
            pool["source"][:, offset] = 40 + parent_rank
            offset += 1
    return pool


def cell_sample_rho(cells: pd.DataFrame, count: int) -> np.ndarray:
    fractions = SAMPLE_FRACTIONS_9 if count == 9 else SAMPLE_FRACTIONS_5
    lo = cells["rho_lo"].to_numpy(np.float64)[:, None]
    hi = cells["rho_hi"].to_numpy(np.float64)[:, None]
    return lo + (hi - lo) * fractions[None, :]


def robust_evaluate_pool(
    cells: pd.DataFrame,
    pool: dict[str, np.ndarray],
    *,
    sample_count: int,
    target_memory_bytes: int,
    label: str,
) -> None:
    samples = cell_sample_rho(cells, sample_count)
    nvals = cells["n"].to_numpy(np.int32)
    N, K = pool["q"].shape
    for j in range(K):
        valid = (
            np.isfinite(pool["q"][:, j])
            & (pool["pieces"][:, j] > 0)
            & (pool["m"][:, j] > 0)
        )
        if not np.any(valid):
            continue
        # Group by exact computational recipe; this keeps one reusable GPU grid.
        keys = np.stack(
            [
                pool["pieces"][:, j],
                pool["order"][:, j],
                pool["grid_power"][:, j],
                pool["m"][:, j],
            ],
            axis=1,
        )
        unique_keys = np.unique(keys[valid], axis=0)
        per_sample = np.full((N, sample_count), np.inf, np.float64)
        for pieces, order, power, m in unique_keys:
            rows = np.flatnonzero(
                valid
                & (pool["pieces"][:, j] == pieces)
                & (pool["order"][:, j] == order)
                & (pool["grid_power"][:, j] == power)
                & (pool["m"][:, j] == m)
            )
            if len(rows) == 0:
                continue
            spec = base.GridSpec(
                int(pieces), int(order), int(power),
                0.25, 0.90, min(512, int(pieces) - 1),
            )
            flat_rows = np.repeat(rows, sample_count)
            vals = evaluate_fixed_points(
                np.repeat(nvals[rows], sample_count),
                samples[rows].reshape(-1),
                np.repeat(pool["q"][rows, j], sample_count),
                np.repeat(pool["t0"][rows, j], sample_count),
                np.repeat(pool["eta"][rows, j], sample_count),
                np.repeat(pool["lam"][rows, j], sample_count),
                int(m),
                spec,
                target_memory_bytes=target_memory_bytes,
                label=f"{label}:cand{j}:p{pieces}:m{m}",
            ).reshape(len(rows), sample_count)
            per_sample[rows, :] = vals
        maximum = np.max(per_sample, axis=1)
        minimum = np.min(per_sample, axis=1)
        sensitivity = np.full(N, np.inf, dtype=np.float64)
        finite = np.isfinite(maximum) & np.isfinite(minimum)
        sensitivity[finite] = maximum[finite] - minimum[finite]
        pool["robust_bound"][:, j] = maximum
        pool["rho_sensitivity"][:, j] = sensitivity


def predicted_cost(pool: dict[str, np.ndarray]) -> np.ndarray:
    return (
        pool["pieces"].astype(np.float64)
        * pool["order"].astype(np.float64)
        * (1.0 + 0.0125 * np.maximum(pool["m"], 0).astype(np.float64))
    )


def choose_recipe_indices(pool: dict[str, np.ndarray]) -> np.ndarray:
    """Return six useful recipe indices per cell without Python row loops."""
    b = pool["robust_bound"]
    cost = predicted_cost(pool)
    N, K = b.shape
    result = np.full((N, TOP_K), -1, np.int16)

    # 0: speed-first recipe. Prefer a comfortable 0.445 margin, but do not
    # force an expensive 0.44 recipe when a much cheaper 0.444... recipe exists.
    chosen = np.full(N, -1, np.int16)
    for threshold in (0.445, 0.448, 0.4495, 0.45):
        missing = chosen < 0
        score = np.where((b <= threshold) & missing[:, None], cost, np.inf)
        idx = np.argmin(score, axis=1)
        ok = missing & np.isfinite(score[np.arange(N), idx])
        chosen[ok] = idx[ok].astype(np.int16)
    fallback = np.argmin(b, axis=1).astype(np.int16)
    chosen[chosen < 0] = fallback[chosen < 0]
    result[:, 0] = chosen

    # 1/2/3: extra-margin and progressively cheaper fallback thresholds.
    for col, threshold in enumerate((0.44, 0.448, 0.4495), start=1):
        score = np.where(b <= threshold, cost, np.inf)
        idx = np.argmin(score, axis=1)
        ok = np.isfinite(score[np.arange(N), idx])
        result[:, col] = np.where(ok, idx, fallback).astype(np.int16)

    # 4: absolute minimum bound. 5: strongest/highest-cost tested fallback.
    result[:, 4] = fallback
    safety_score = np.where(np.isfinite(b), cost, -np.inf)
    result[:, 5] = np.argmax(safety_score, axis=1).astype(np.int16)
    return result


def gather_selected(pool: dict[str, np.ndarray], indices: np.ndarray) -> dict[str, np.ndarray]:
    rows = np.arange(indices.shape[0])[:, None]
    out = {}
    for name, values in pool.items():
        if values.ndim == 2:
            out[name] = values[rows, indices]
    return out


def classify_bounds(bounds: np.ndarray) -> np.ndarray:
    return np.searchsorted(BOUND_THRESHOLDS, bounds, side="right").astype(np.uint8)


def level_checkpoint_path(outdir: Path, depth: int) -> Path:
    return outdir / "checkpoints" / f"level_d{depth}.npz"


def save_level(
    cells: pd.DataFrame,
    selected: dict[str, np.ndarray],
    indices: np.ndarray,
    path: Path,
    metadata: dict,
) -> None:
    arrays = {
        "n": cells["n"].to_numpy(np.int32),
        "depth": cells["depth"].to_numpy(np.uint8),
        "cell_index": cells["cell_index"].to_numpy(np.int32),
        "rho_lo": cells["rho_lo"].to_numpy(np.float64),
        "rho_hi": cells["rho_hi"].to_numpy(np.float64),
        "recipe_indices": indices.astype(np.int16),
        "metadata_json": np.array(json.dumps(metadata)),
    }
    for name, values in selected.items():
        arrays[f"cand_{name}"] = values
    atomic_save_npz(path, **arrays)


def load_level(path: Path) -> tuple[pd.DataFrame, dict[str, np.ndarray], np.ndarray, dict]:
    with np.load(path, allow_pickle=False) as z:
        cells = pd.DataFrame(
            {
                "n": z["n"], "depth": z["depth"], "cell_index": z["cell_index"],
                "rho_lo": z["rho_lo"], "rho_hi": z["rho_hi"],
                "rho": 0.5 * (z["rho_lo"] + z["rho_hi"]),
            }
        )
        selected = {
            name[5:]: np.asarray(z[name])
            for name in z.files
            if name.startswith("cand_")
        }
        indices = np.asarray(z["recipe_indices"])
        metadata = json.loads(str(z["metadata_json"].item()))
    return cells, selected, indices, metadata


def level_input_digest(
    cells: pd.DataFrame,
    parent_selected: dict[str, np.ndarray] | None,
) -> str:
    arrays = cell_input_arrays(cells)
    arrays["parent_present"] = np.array(
        [parent_selected is not None], dtype=np.uint8
    )
    if parent_selected is not None:
        for name, values in parent_selected.items():
            arrays[f"parent_{name}"] = values
    return named_arrays_digest(arrays)


def level_payload_digest(
    cells: pd.DataFrame,
    selected: dict[str, np.ndarray],
    indices: np.ndarray,
) -> str:
    arrays = cell_input_arrays(cells)
    arrays["recipe_indices"] = np.asarray(indices, dtype=np.int16)
    for name, values in selected.items():
        arrays[f"cand_{name}"] = values
    return named_arrays_digest(arrays)


def process_level(
    cells: pd.DataFrame,
    spec: LevelSpec,
    *,
    target_memory_bytes: int,
    q_chunk: int,
    outdir: Path,
    mirror_dir: Path | None,
    parent_selected: dict[str, np.ndarray] | None,
    profile_sha256: str,
) -> tuple[pd.DataFrame, dict[str, np.ndarray], dict]:
    level_path = level_checkpoint_path(outdir, spec.depth)
    input_sha256 = level_input_digest(cells, parent_selected)
    if restore_file(level_path, mirror_dir):
        try:
            loaded_cells, selected, indices, meta = load_level(level_path)
            valid_shapes = (
                indices.shape == (len(cells), TOP_K)
                and set(selected) == SELECTED_FIELDS
                and all(value.shape == indices.shape for value in selected.values())
            )
            valid = (
                len(loaded_cells) == len(cells)
                and meta.get("depth") == spec.depth
                and meta.get("profile_sha256") == profile_sha256
                and meta.get("input_sha256") == input_sha256
                and cell_input_digest(loaded_cells) == cell_input_digest(cells)
                and valid_shapes
                and meta.get("payload_sha256")
                == level_payload_digest(loaded_cells, selected, indices)
            )
        except Exception as exc:
            # Checkpoints are optional acceleration data. Any decoding or
            # schema failure must fall back to deterministic recomputation.
            print(f"[d{spec.depth}] ignoring unreadable checkpoint: {exc}", flush=True)
            valid = False
        if valid:
            print(f"[d{spec.depth}] restored robust cell bank ({len(cells):,} cells)", flush=True)
            return loaded_cells, selected, meta
        print(f"[d{spec.depth}] checkpoint provenance mismatch; recomputing", flush=True)

    center, center_meta = run_center_search(
        cells,
        spec,
        target_memory_bytes=target_memory_bytes,
        q_chunk=q_chunk,
        outdir=outdir,
        mirror_dir=mirror_dir,
        profile_sha256=profile_sha256,
    )
    auxiliary_centers: list[pd.DataFrame] = []
    auxiliary_meta: list[dict] = []
    if spec.depth == 6:
        aux_spec = LevelSpec(
            6, base.GridSpec(192, 8, 2, 0.25, 0.90, 320),
            97, 4.70, 6.90, 5, "d6_global_p192",
        )
        aux_center, aux_meta = run_center_search(
            cells, aux_spec,
            target_memory_bytes=target_memory_bytes,
            q_chunk=max(4, q_chunk // 2),
            outdir=outdir, mirror_dir=mirror_dir,
            profile_sha256=profile_sha256,
        )
        auxiliary_centers.append(aux_center)
        auxiliary_meta.append(aux_meta)
    pool = build_candidate_pool(
        cells, center, auxiliary_centers=auxiliary_centers,
        parent_candidates=parent_selected,
    )
    robust_evaluate_pool(
        cells,
        pool,
        sample_count=spec.robust_samples,
        target_memory_bytes=target_memory_bytes,
        label=f"robust_d{spec.depth}",
    )
    recipe_indices = choose_recipe_indices(pool)
    selected = gather_selected(pool, recipe_indices)
    best = selected["robust_bound"][:, 0]
    meta = {
        "profile_sha256": profile_sha256,
        "depth": spec.depth,
        "input_sha256": input_sha256,
        "spec": {
            "search_grid": asdict(spec.search_grid),
            "q_count": spec.q_count,
            "q_range": [spec.q_lo, spec.q_hi],
            "robust_samples": spec.robust_samples,
        },
        "center_meta": center_meta,
        "auxiliary_meta": auxiliary_meta,
        "class_counts": {
            CLASS_LABELS[i]: int(np.sum(classify_bounds(best) == i))
            for i in range(len(CLASS_LABELS))
        },
        "worst_robust_bound": float(np.max(best)),
    }
    meta["payload_sha256"] = level_payload_digest(
        cells, selected, recipe_indices
    )
    save_level(cells, selected, recipe_indices, level_path, meta)
    mirror_file(level_path, mirror_dir)
    return cells, selected, meta


def refinement_mask(depth: int, selected: dict[str, np.ndarray]) -> np.ndarray:
    b = selected["robust_bound"][:, 0]
    sens = selected["rho_sensitivity"][:, 0]
    m = selected["m"][:, 0]
    if depth == 6:
        return (b >= 0.445) | (sens >= 2.5e-4)
    if depth == 7:
        return (b >= 0.4475) | (sens >= 1.2e-4) | (m >= 64)
    if depth == 8:
        # The known n=3 peak around 0.4482 is deliberately sent to depth 9.
        return (b >= 0.4480) | (sens >= 6e-5) | (m >= 100)
    return np.zeros(len(b), dtype=bool)


def load_refinement_plan(path: Path) -> np.ndarray:
    """Load and authenticate the fixed depth-8 parent plan."""
    with np.load(path, allow_pickle=False) as data:
        if set(data.files) != {"n", "cell_index"}:
            raise RuntimeError("refinement plan must contain n and cell_index")
        pairs = np.column_stack(
            (
                np.asarray(data["n"], dtype=np.int64),
                np.asarray(data["cell_index"], dtype=np.int64),
            )
        )
    pairs = np.unique(pairs, axis=0)
    if pairs.shape != (EXPECTED_DEPTH9_PARENTS, 2):
        raise RuntimeError("refinement plan has an unexpected number of parents")
    digest = hashlib.sha256(
        pairs.astype("<i8", copy=False).tobytes(order="C")
    ).hexdigest()
    if digest != EXPECTED_DEPTH9_PARENT_SHA256:
        raise RuntimeError("refinement-plan geometry digest mismatch")
    return pairs


def fixed_refinement_mask(
    depth: int,
    cells: pd.DataFrame,
    selected: dict[str, np.ndarray],
    depth8_plan: np.ndarray,
) -> np.ndarray:
    """Return the deterministic refinement mask fixed by the build profile."""
    eligible = refinement_mask(depth, selected)
    if depth in (6, 7):
        return eligible
    if depth == 8:
        plan_keys = depth8_plan[:, 0] * (1 << 8) + depth8_plan[:, 1]
        cell_keys = (
            cells["n"].to_numpy(np.int64) * (1 << 8)
            + cells["cell_index"].to_numpy(np.int64)
        )
        mask = np.isin(cell_keys, plan_keys, assume_unique=False)
        if int(np.sum(mask)) != EXPECTED_DEPTH9_PARENTS:
            raise RuntimeError("depth-8 cells do not match the publication plan")
        if np.any(mask & ~eligible):
            raise RuntimeError("publication plan contains an ineligible depth-8 cell")
        return mask
    return np.zeros(len(cells), dtype=bool)


def add_final_refinement_candidates(
    cells: pd.DataFrame,
    selected: dict[str, np.ndarray],
    *,
    target_memory_bytes: int,
) -> dict[str, np.ndarray]:
    """Evaluate every hard leaf at the three fixed publication resolutions."""
    b = selected["robust_bound"][:, 0]
    hard = np.flatnonzero(b >= 0.4475)
    if len(hard) != 173:
        raise RuntimeError(
            "publication profile expected 173 final-refinement leaves, "
            f"found {len(hard)}"
        )
    hard = hard[np.argsort(b[hard])[::-1]]
    specs = [
        base.GridSpec(1536, 12, 3, 0.25, 0.90, 512),
        base.GridSpec(3072, 12, 3, 0.25, 0.90, 512),
        base.GridSpec(4096, 12, 3, 0.25, 0.90, 512),
    ]
    for spec in specs:
        rows = hard
        q0 = selected["q"][rows, 4]  # minimum-bound basin
        t00 = selected["t0"][rows, 4]
        eta0 = selected["eta"][rows, 4]
        lam0 = selected["lam"][rows, 4]
        local_samples = cell_sample_rho(cells.iloc[rows].reset_index(drop=True), 9)
        vals = evaluate_fixed_points(
            np.repeat(cells["n"].to_numpy(np.int32)[rows], 9),
            local_samples.reshape(-1),
            np.repeat(q0, 9), np.repeat(t00, 9), np.repeat(eta0, 9), np.repeat(lam0, 9),
            100, spec,
            target_memory_bytes=target_memory_bytes,
            label=f"final_refinement_p{spec.panels}",
        ).reshape(len(rows), 9)
        rb = np.max(vals, axis=1)
        rs = np.max(vals, axis=1) - np.min(vals, axis=1)
        # Replace safety rank 5 whenever the refined candidate is stronger.
        improve = rb < selected["robust_bound"][rows, 5]
        rimp = rows[improve]
        if len(rimp):
            source_pos = np.flatnonzero(improve)
            for name, values in (("q", q0), ("t0", t00), ("eta", eta0), ("lam", lam0)):
                selected[name][rimp, 5] = values[source_pos]
            selected["m"][rimp, 5] = 100
            selected["pieces"][rimp, 5] = spec.panels
            selected["order"][rimp, 5] = spec.order
            selected["grid_power"][rimp, 5] = spec.power
            selected["center_bound"][rimp, 5] = rb[source_pos]
            selected["robust_bound"][rimp, 5] = rb[source_pos]
            selected["rho_sensitivity"][rimp, 5] = rs[source_pos]
            selected["source"][rimp, 5] = 100 + spec.panels // 100
        print(
            f"[final refinement] p={spec.panels}: "
            f"checked {len(rows):,} hard leaves; "
            f"best worst={np.max(np.minimum(selected['robust_bound'][rows,0], rb)):.12f}",
            flush=True,
        )
    return selected


def write_array(path: Path, array: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as stream:
        np.save(stream, array, allow_pickle=False)
    os.replace(tmp, path)


def geometry_digest(n: np.ndarray, depth: np.ndarray, index: np.ndarray) -> str:
    digest = hashlib.sha256()
    digest.update(np.asarray(n, dtype="<i4").tobytes(order="C"))
    digest.update(np.asarray(depth, dtype="u1").tobytes(order="C"))
    digest.update(np.asarray(index, dtype="<i4").tobytes(order="C"))
    return digest.hexdigest()


def validate_leaf_coverage(cells: pd.DataFrame) -> None:
    """Require an exact dyadic tiling for every n before publishing arrays."""
    if len(cells) != EXPECTED_ROWS:
        raise RuntimeError(f"expected {EXPECTED_ROWS:,} leaves, found {len(cells):,}")
    depth_values = cells["depth"].to_numpy(np.uint8)
    counts = {
        depth: int(np.sum(depth_values == depth)) for depth in EXPECTED_DEPTH_COUNTS
    }
    if counts != EXPECTED_DEPTH_COUNTS:
        raise RuntimeError(f"unexpected depth counts: {counts}")
    for n, group in cells.groupby("n", sort=True):
        maximum_depth = int(group["depth"].max())
        intervals = sorted(
            (
                int(row.cell_index) << (maximum_depth - int(row.depth)),
                (int(row.cell_index) + 1) << (maximum_depth - int(row.depth)),
            )
            for row in group.itertuples(index=False)
        )
        expected = 0
        for lower, upper in intervals:
            if lower != expected:
                raise RuntimeError(f"rho gap or overlap for n={int(n)}")
            expected = upper
        if expected != 1 << maximum_depth:
            raise RuntimeError(f"rho tiling for n={int(n)} does not reach rho0")


def array_metadata(path: Path, array: np.ndarray) -> dict:
    return {
        "file": path.name,
        "dtype": array.dtype.str,
        "shape": list(array.shape),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def write_authenticated_manifest(
    path: Path,
    generated_manifest: dict,
    reference_manifest: Path,
) -> str:
    """Validate semantics, then install the exact publication manifest bytes."""
    reference_bytes = reference_manifest.read_bytes()
    try:
        reference = json.loads(reference_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("publication reference manifest is not valid UTF-8 JSON") from exc
    if generated_manifest != reference:
        generated_arrays = generated_manifest.get("arrays", {})
        reference_arrays = reference.get("arrays", {})
        mismatches = sorted(
            name
            for name in set(generated_arrays) | set(reference_arrays)
            if generated_arrays.get(name) != reference_arrays.get(name)
        )
        raise RuntimeError(
            "reproduced bank does not match the publication manifest; "
            f"array mismatches={mismatches}"
        )
    atomic_write_bytes(path, reference_bytes)
    return hashlib.sha256(reference_bytes).hexdigest()


def directory_digest(root: Path) -> str:
    """Hash all regular files in a directory tree, including relative names."""
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        file_sha = sha256_file(path).encode("ascii")
        digest.update(len(relative).to_bytes(8, "little"))
        digest.update(relative)
        digest.update(file_sha)
    return digest.hexdigest()


def publish_bank_to_mirror(bank_dir: Path, mirror_dir: Path) -> dict:
    """Publish a complete content-addressed bank and then an atomic pointer.

    A disconnected Drive mount can leave a hidden staging directory, but it
    cannot make an incomplete directory visible through the publication
    pointer. Existing content-addressed publications are reused only after a
    full tree-digest comparison.
    """
    mirror_dir.mkdir(parents=True, exist_ok=True)
    manifest_sha256 = sha256_file(bank_dir / "manifest.json")
    source_tree_sha256 = directory_digest(bank_dir)
    publications = mirror_dir / "parameter_banks"
    publications.mkdir(parents=True, exist_ok=True)
    target = publications / manifest_sha256

    if target.exists():
        if directory_digest(target) != source_tree_sha256:
            raise RuntimeError(
                "existing Drive publication has the expected name but different content"
            )
    else:
        staging_root = Path(
            tempfile.mkdtemp(prefix=".parameter-bank-", dir=publications)
        )
        staged_bank = staging_root / "bank"
        try:
            shutil.copytree(bank_dir, staged_bank)
            if directory_digest(staged_bank) != source_tree_sha256:
                raise RuntimeError("Drive staging copy failed its tree-digest check")
            os.replace(staged_bank, target)
        finally:
            shutil.rmtree(staging_root, ignore_errors=True)

    pointer = {
        "format": "berry-esseen-parameter-bank-publication-v1",
        "artifact": target.relative_to(mirror_dir).as_posix(),
        "manifest_sha256": manifest_sha256,
        "tree_sha256": source_tree_sha256,
    }
    atomic_write_json(mirror_dir / "published_parameter_bank.json", pointer)
    return pointer


def write_final_bank(
    leaf_cells: pd.DataFrame,
    leaf_selected: dict[str, np.ndarray],
    outdir: Path,
    reference_manifest: Path,
) -> Path:
    validate_leaf_coverage(leaf_cells)
    bank_dir = outdir / "parameter_bank"
    tmp_dir = outdir / "parameter_bank.tmp"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    order = np.lexsort(
        (
            leaf_cells["cell_index"].to_numpy(np.int32),
            -leaf_cells["depth"].to_numpy(np.int16),
            leaf_cells["n"].to_numpy(np.int32),
        )
    )
    cells = leaf_cells.iloc[order].reset_index(drop=True)
    selected = {name: values[order] for name, values in leaf_selected.items()}
    for name in ("q", "t0", "eta", "lam"):
        if not np.all(np.isfinite(selected[name])):
            raise RuntimeError(f"selected {name} recipes contain non-finite values")
    if np.any(selected["pieces"] <= 0) or np.any(selected["grid_power"] <= 0):
        raise RuntimeError("selected grid recipes contain invalid integers")

    arrays = {
        "n.npy": cells["n"].to_numpy(np.int32),
        "depth.npy": cells["depth"].to_numpy(np.uint8),
        "cell_index.npy": cells["cell_index"].to_numpy(np.int32),
        "q.npy": selected["q"].astype(np.float64),
        "t0.npy": selected["t0"].astype(np.float64),
        "eta.npy": selected["eta"].astype(np.float64),
        "lam.npy": selected["lam"].astype(np.float64),
        "pieces.npy": selected["pieces"].astype(np.int32),
        "grid_power.npy": selected["grid_power"].astype(np.int16),
    }
    for name, array in arrays.items():
        write_array(tmp_dir / name, array)

    geometry_sha256 = geometry_digest(
        arrays["n.npy"], arrays["depth.npy"], arrays["cell_index.npy"]
    )
    if geometry_sha256 != EXPECTED_GEOMETRY_SHA256:
        raise RuntimeError("final leaf geometry differs from the publication geometry")
    manifest = {
        "format": "berry-esseen-parameter-bank-v1",
        "version": 1,
        "build_profile": PUBLICATION_PROFILE,
        "rows": int(len(cells)),
        "candidates_per_cell": TOP_K,
        "n_min": 2,
        "n_max": N_MAX,
        "rho0": "712569/589000",
        "recipe_denominator": 1 << 20,
        "geometry_sha256": geometry_sha256,
        "depth9_parent_sha256": EXPECTED_DEPTH9_PARENT_SHA256,
        "depth_counts": {str(key): value for key, value in EXPECTED_DEPTH_COUNTS.items()},
        "role": (
            "Untrusted parameter advice. The Arb checker independently "
            "recomputes every selected cell bound."
        ),
        "arrays": {
            Path(name).stem: array_metadata(tmp_dir / name, array)
            for name, array in arrays.items()
        },
    }
    write_authenticated_manifest(tmp_dir / "manifest.json", manifest, reference_manifest)

    if bank_dir.exists():
        shutil.rmtree(bank_dir)
    os.replace(tmp_dir, bank_dir)
    return bank_dir


def concatenate_leaf_levels(
    levels: list[tuple[pd.DataFrame, dict[str, np.ndarray], np.ndarray]],
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    cells = pd.concat([x[0].loc[~x[2]].copy() for x in levels], ignore_index=True)
    selected: dict[str, np.ndarray] = {}
    for name in levels[0][1]:
        selected[name] = np.concatenate([x[1][name][~x[2]] for x in levels], axis=0)
    return cells, selected


def build_publication_bank(
    *,
    output_dir: Path,
    mirror_dir: Path | None,
    refinement_plan: Path,
    reference_manifest: Path,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    gpu = base.gpu_info()
    if "A100" not in gpu["name"].upper():
        raise RuntimeError(f"publication profile requires an A100, got {gpu['name']}")
    if tuple(gpu["compute_capability"]) != (8, 0):
        raise RuntimeError("publication profile requires A100 compute capability 8.0")
    cuda_runtime = int(cp.cuda.runtime.runtimeGetVersion())
    if cuda_runtime // 1000 != 12:
        raise RuntimeError(
            f"publication profile requires CUDA runtime 12.x, got {cuda_runtime}"
        )
    mem = base.configure_gpu_memory(60.0)
    target_mem = int(mem["target_working_set_GiB"] * 2**30)
    q_chunk = 12
    profile_sha256, profile_record = publication_identity(
        refinement_plan, reference_manifest, gpu
    )
    depth8_plan = load_refinement_plan(refinement_plan)
    print(
        json.dumps(
            {
                "profile": PUBLICATION_PROFILE,
                "profile_sha256": profile_sha256,
                "gpu": gpu,
                "memory": mem,
            },
            indent=2,
        ),
        flush=True,
    )

    start = time.perf_counter()
    levels: list[tuple[pd.DataFrame, dict[str, np.ndarray], np.ndarray]] = []
    parent_cells = dyadic_cells_all_n(6)
    parent_selected = None
    stage_meta = []

    for depth in (6, 7, 8, 9):
        spec = LEVEL_SPECS[depth]
        if depth > 6:
            previous_cells, previous_selected, previous_mask = levels[-1]
            parents = previous_cells.loc[previous_mask].reset_index(drop=True)
            if len(parents) == 0:
                break
            parent_cells = split_cells(parents)
            # parent_row indexes the compact parent subset.
            parent_selected = {
                name: values[previous_mask]
                for name, values in previous_selected.items()
            }

        cells, selected, meta = process_level(
            parent_cells,
            spec,
            target_memory_bytes=target_mem,
            q_chunk=max(2, q_chunk // (1 + max(0, depth - 7))),
            outdir=output_dir,
            mirror_dir=mirror_dir,
            parent_selected=parent_selected,
            profile_sha256=profile_sha256,
        )
        stage_meta.append(meta)
        mask = fixed_refinement_mask(depth, cells, selected, depth8_plan)
        levels.append((cells, selected, mask))
        best = selected["robust_bound"][:, 0]
        print(
            f"[d{depth}] cells={len(cells):,}, refine={int(np.sum(mask)):,}, "
            f"worst robust={np.max(best):.12f}, elapsed={(time.perf_counter()-start)/60:.1f} min",
            flush=True,
        )
        atomic_write_json(
            output_dir / "progress.json",
            {
                "elapsed_seconds": time.perf_counter() - start,
                "completed_depth": depth,
                "stage_meta": stage_meta,
                "worst_robust_bound": float(np.max(best)),
                "refine_cells": int(np.sum(mask)),
                "profile_sha256": profile_sha256,
            },
        )
        if mirror_dir is not None:
            mirror_dir.mkdir(parents=True, exist_ok=True)
            atomic_copy_file(
                output_dir / "progress.json", mirror_dir / "progress.json"
            )

    leaf_cells, leaf_selected = concatenate_leaf_levels(levels)
    leaf_selected = add_final_refinement_candidates(
        leaf_cells,
        leaf_selected,
        target_memory_bytes=target_mem,
    )

    best = leaf_selected["robust_bound"][:, 0]
    classes = classify_bounds(best)
    report = {
        "profile": PUBLICATION_PROFILE,
        "profile_sha256": profile_sha256,
        "profile_record": profile_record,
        "gpu": gpu,
        "memory": mem,
        "leaf_cells": int(len(leaf_cells)),
        "depth_counts": {
            str(d): int(np.sum(leaf_cells["depth"].to_numpy() == d))
            for d in sorted(leaf_cells["depth"].unique())
        },
        "class_counts": {
            CLASS_LABELS[i]: int(np.sum(classes == i))
            for i in range(len(CLASS_LABELS))
        },
        "worst_robust_bound": float(np.max(best)),
        "worst_margin_to_045": float(TARGET - np.max(best)),
        "unresolved_cells": int(np.sum(best >= TARGET)),
        "stages": stage_meta,
        "note": (
            "robust_bound is the maximum over 5 or 9 float64 rho samples in a "
            "dyadic cell using one fixed recipe; it is not an interval proof"
        ),
    }
    bank_dir = write_final_bank(
        leaf_cells,
        leaf_selected,
        output_dir,
        reference_manifest,
    )
    report["bank_dir"] = str(bank_dir)
    report["elapsed_total_seconds"] = time.perf_counter() - start

    if mirror_dir is not None:
        report["mirror_publication"] = publish_bank_to_mirror(bank_dir, mirror_dir)

    atomic_write_json(output_dir / "build_report.json", report)
    if mirror_dir is not None:
        atomic_copy_file(
            output_dir / "build_report.json", mirror_dir / "build_report.json"
        )

    print(
        "PARAMETER BANK REPRODUCED\n"
        + json.dumps(
            {
                "bank_dir": str(bank_dir),
                "rows": report["leaf_cells"],
                "depth_counts": report["depth_counts"],
                "elapsed_seconds": report["elapsed_total_seconds"],
                "manifest_sha256": sha256_file(bank_dir / "manifest.json"),
            },
            indent=2,
        ),
        flush=True,
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repository = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/content/berry_esseen_parameter_bank"),
    )
    parser.add_argument("--mirror-dir", type=Path, default=None)
    parser.add_argument(
        "--refinement-plan",
        type=Path,
        default=repository / "reproduction" / "publication_refinement_plan.npz",
    )
    parser.add_argument(
        "--reference-manifest",
        type=Path,
        default=repository / "data" / "parameter_bank" / "manifest.json",
    )
    args, unknown = parser.parse_known_args()
    # Ignore only Jupyter's own -f kernel.json pair.
    if unknown:
        cleaned = []
        i = 0
        while i < len(unknown):
            if unknown[i] == "-f" and i + 1 < len(unknown):
                i += 2
            else:
                cleaned.append(unknown[i])
                i += 1
        if cleaned:
            parser.error(f"unrecognized arguments: {' '.join(cleaned)}")
    if not args.refinement_plan.is_file():
        parser.error(f"refinement plan not found: {args.refinement_plan}")
    if not args.reference_manifest.is_file():
        parser.error(f"reference manifest not found: {args.reference_manifest}")
    build_publication_bank(
        output_dir=args.output_dir,
        mirror_dir=args.mirror_dir,
        refinement_plan=args.refinement_plan,
        reference_manifest=args.reference_manifest,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
