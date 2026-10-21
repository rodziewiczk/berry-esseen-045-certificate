"""Exact Python-integer replay of the published degree-five cube algorithm.

This is a distinct checker, not a claim that the C++ binary was executed.
Polynomial reconstruction, moment checking and normal enclosures are imported
from the byte-pinned, freshly copied original Python source.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
N = 216
TRIPLES = [(i, j, k) for i in range(6) for j in range(6) for k in range(6)]
LINES = [
    [[36*k+6*u+v for k in range(6)] for u in range(6) for v in range(6)],
    [[36*u+6*k+v for k in range(6)] for u in range(6) for v in range(6)],
    [[36*u+6*v+k for k in range(6)] for u in range(6) for v in range(6)],
]
LEFT = [[(j, comb(i,j)*(1 << (5-i))) for j in range(i+1)] for i in range(6)]
RIGHT = [[(j, comb(5-i,j-i)*(1 << i)) for j in range(i,6)] for i in range(6)]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def affine(b, den, slopes, target, side):
    lower = (0, 1) if side > 0 else None
    upper = (0, 1) if side < 0 else None
    for value, slope in zip(b, slopes):
        v = value - den if target else value
        if slope == 0:
            if v < 0:
                return False
        elif slope < 0:
            candidate = (-v, -slope)
            if lower is None or lower[0]*candidate[1] < candidate[0]*lower[1]:
                lower = candidate
        else:
            candidate = (v, slope)
            if upper is None or candidate[0]*upper[1] < upper[0]*candidate[1]:
                upper = candidate
        if lower is not None and upper is not None:
            if upper[0]*lower[1] < lower[0]*upper[1]:
                return False
    return True


def divide(box, axis):
    b, den, pos, lev, depth = box
    left, right = [0]*N, [0]*N
    for indices in LINES[axis]:
        line = [b[j] for j in indices]
        for i, index in enumerate(indices):
            left[index] = sum(line[j]*w for j, w in LEFT[i])
            right[index] = sum(line[j]*w for j, w in RIGHT[i])
    lp, rp, levels = list(pos), list(pos), list(lev)
    lp[axis] *= 2
    rp[axis] = rp[axis]*2+1
    levels[axis] += 1
    return ((left, den*32, tuple(lp), tuple(levels), depth+1),
            (right, den*32, tuple(rp), tuple(levels), depth+1))


def cubes(coefficients, threshold):
    tn, td = threshold.numerator, threshold.denominator
    require(0 < td <= 100000 and -7*td <= 2*tn <= 3*td, "Threshold scope")
    count = leaves = maximum_depth = 0
    for part, (b, den, origin) in enumerate(coefficients):
        require(origin == tuple(-7 if i < 3-part else 0 for i in range(3)),
                "Complete four-orthant coverage")
        require(den > 0 and len(b) == N, "Exact root coefficients")
        stack = [(b, den, (0,0,0), (0,0,0), 0)]
        while stack:
            box = stack.pop()
            b, den, pos, lev, depth = box
            count += 1
            maximum_depth = max(maximum_depth, depth)
            require(count <= 4000000 and depth <= 95, "Unresolved positivity")
            level = max(lev)
            require(level <= 35, "Dyadic coordinate depth")
            scale = 1 << level
            width = [7*(1 << (level-lev[i])) for i in range(3)]
            lower = [origin[i]*scale+pos[i]*width[i] for i in range(3)]
            upper = [lower[i]+width[i] for i in range(3)]
            if lower[0] > upper[1] or lower[1] > upper[2] or lower[0] > upper[2]:
                continue
            sl, su, minimum = sum(lower), sum(upper), min(b)
            if su*td <= tn*scale:
                accepted = minimum >= den
            elif sl*td > tn*scale:
                accepted = minimum >= 0
            else:
                slopes = [(5*sl+width[0]*i+width[1]*j+width[2]*k)*td-5*tn*scale
                          for i,j,k in TRIPLES]
                require(all(-(1 << 63) < s < (1 << 63)-1 for s in slopes),
                        "Original signed integer-coordinate domain")
                accepted = affine(b, den, slopes, 1, -1) and (
                    minimum >= 0 or affine(b, den, slopes, 0, 1))
            if accepted:
                leaves += 1
                continue
            axis = lev.index(min(lev))
            left, right = divide(box, axis)
            stack.append(right)
            stack.append(left)
    return count, leaves, maximum_depth


def unit_tests():
    require(affine([1]*N, 1, [0]*N, 1, -1), "Constant one accepted")
    require(not affine([0]*N, 1, [0]*N, 1, -1), "Constant zero cannot majorize one")
    require(not affine([-1]*N, 1, [0]*N, 0, 1), "Negative majorant rejected")
    for axis in range(3):
        children = divide(([7]*N, 11, (0,0,0), (0,0,0), 0), axis)
        require(all(child[0] == [224]*N and child[1] == 352 for child in children),
                "Constant preserved by exact midpoint subdivision")
        require(children[0][2][axis] == 0 and children[1][2][axis] == 1,
                "Both complete closed children retained")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--progress", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    progress = None
    if args.progress is not None:
        require(args.progress.resolve().parent == source.parents[2],
                "Progress stays in this private work directory")
        progress = args.progress.open("x", encoding="utf-8")
    spec = importlib.util.spec_from_file_location("original_n3", source/"verify.py")
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    unit_tests()
    started = time.monotonic()
    original.analytic_constants()
    records = original.load_records(source/"certificate")
    require(len(records) == 111, "All 111 original threshold intervals")
    nodes = leaves = moments = 0
    for index, (lo, hi, coefficients, name, digest) in enumerate(records):
        roots = []
        for signs in ((-1,-1,-1),(-1,-1,1),(-1,1,1),(1,1,1)):
            b, den = original.transform_bern(original.polynomial(coefficients, signs), signs)
            roots.append((b, den, tuple(-7 if s < 0 else 0 for s in signs)))
        nn, ll, dd = cubes(roots, hi)
        mm = original.check_moments(coefficients, lo)
        nodes += nn
        leaves += ll
        moments += mm
        event = json.dumps({"event":"cell_verified", "index":index, "file":name,
                            "sha256":digest, "nodes":nn, "leaves":ll, "depth":dd,
                            "moment_boxes":mm})
        print(event, flush=True)
        if progress is not None:
            progress.write(event+"\n")
            progress.flush()
    require((nodes, leaves, moments) == (501156, 219860, 349),
            "Exact full traversal must match the specified native algorithm")
    print("ACCEPTED_FULL_N3_PYTHON 111 501156 219860 349", flush=True)
    if progress is not None:
        progress.close()
    print(json.dumps({"scope":"FRESH_PYTHON_INTEGER_N3_REPLAY_NOT_CPP_EXECUTION",
                      "cells":111, "nodes":nodes, "leaves":leaves, "moment_boxes":moments,
                      "wall_seconds":time.monotonic()-started,
                      "worker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "all_index_conclusion_verified":False}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("REJECTED_PYTHON_N3: "+str(exc), file=sys.stderr, flush=True)
        raise SystemExit(1)
