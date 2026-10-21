"""Literal proof obligations. Integrity or composition alone never covers an index."""
from __future__ import annotations

LITERATURE = {
    "BentkusKirsa1989": "C1 <= 0.3704 in the manuscript's normalization",
    "Esseen1956": "C* >= C_E",
    "Prawitz1972": "One-sided smoothing with the stated kernel and endpoint convention",
    "Shevtsova2012": "The cited normalized smoothing statement",
    "Shevtsova2013": "The stated finite iid structural bounds",
    "Shevtsova2014": "The sharp third-moment inequality",
    "Schulz2016": "The binomial inequality for all n and all 0<p<1",
    "HeCheng2026": "The cited finite Gaussian estimate, not an all-index conclusion",
}


def obligations():
    nodes = {
        "n2": {"depends": [], "kind": "arithmetic", "covers": [2,2]},
        "n3": {"depends": [], "kind": "arithmetic", "covers": [3,3]},
        "n4": {"depends": ["n3"], "kind": "arithmetic", "covers": [4,4]},
        "c5.support": {"depends": ["n4"], "kind": "arithmetic"},
        "c5.high": {"depends": ["c5.support"], "kind": "arithmetic"},
        "c5.owncaps": {"depends": ["c5.support","c5.high"], "kind": "arithmetic"},
        "c5.initial": {"depends": ["c5.support","c5.owncaps"], "kind": "arithmetic"},
        "c5.resources": {"depends": ["c5.initial"], "kind": "arithmetic"},
        "c5.counts": {"depends": ["c5.resources"], "kind": "arithmetic"},
        "c5.gapfree": {"depends": [], "kind": "arithmetic"},
        "c5.complement": {"depends": ["c5.support","c5.high"], "kind": "arithmetic"},
        "n5": {"depends": ["n4","c5.support","c5.high","c5.owncaps","c5.initial",
                            "c5.resources","c5.counts","c5.gapfree","c5.complement"],
               "kind": "composition", "covers": [5,5]},
    }
    for n in range(6,31):
        nodes["n"+str(n)] = {"depends": ["n"+str(n-1)],
                             "kind": "arithmetic", "covers": [n,n]}
    nodes.update({
        "tail31.base31_34": {"depends":["n30"], "kind":"arithmetic"},
        "tail31.bridge35_48": {"depends":["tail31.base31_34"], "kind":"arithmetic"},
        "tail49.support": {"depends":[], "kind":"arithmetic"},
        "tail49.resources": {"depends":["tail49.support"], "kind":"arithmetic"},
        "tail49.confinement": {"depends":["tail49.resources"], "kind":"arithmetic"},
        "tail49.local": {"depends":["tail49.confinement"], "kind":"arithmetic",
                         "uniform_index_domain":"n >= 47, including reciprocal-index endpoint zero"},
        "tail49": {"depends":["tail49.support","tail49.resources","tail49.confinement","tail49.local"],
                    "kind":"composition", "covers":[49,None]},
        "tail31": {"depends":["tail31.base31_34","tail31.bridge35_48","tail49"],
                    "kind":"composition", "covers":[31,None]},
    })
    return nodes


def order(nodes):
    result, visiting, done = [], set(), set()
    def visit(name):
        if name in visiting:
            raise ValueError("Cyclic proof dependency: "+name)
        if name in done:
            return
        if name not in nodes:
            raise ValueError("Missing proof obligation: "+name)
        visiting.add(name)
        for dep in nodes[name]["depends"]:
            visit(dep)
        visiting.remove(name)
        done.add(name)
        result.append(name)
    for name in nodes:
        visit(name)
    return result


def check_index_cover(intervals):
    """Prove that the supplied INTEGER intervals cover all positive indices."""
    cleaned = []
    for lo, hi in intervals:
        if type(lo) is not int or lo < 1 or (hi is not None and
                (type(hi) is not int or hi < lo)):
            raise ValueError("Literal positive integer bounds required")
        cleaned.append((lo,hi))
    cleaned.sort(key=lambda x:(x[0],float("inf") if x[1] is None else x[1]))
    next_index = 1
    for lo, hi in cleaned:
        if lo > next_index:
            raise ValueError("Uncovered index: "+str(next_index))
        if hi is None:
            return
        next_index = max(next_index,hi+1)
    raise ValueError("No verified unbounded tail; first uncovered index "+str(next_index))


def computational_scope(records):
    """Summarize only fresh arithmetic outcomes supplied by this same run.

    This function is not an importer of historical PASS files. Its callers
    must obtain each record from a successfully executed exact component.
    """
    nodes = obligations()
    missing = []
    for name in order(nodes):
        record = records.get(name)
        if record is None or record.get("fresh_arithmetic") is not True:
            missing.append(name)
    if missing:
        return {"all_computational_obligations_verified":False, "outstanding":missing}
    intervals = [[1,1]]  # Separately cited Bentkus--Kirsa theorem.
    intervals += [node["covers"] for node in nodes.values() if "covers" in node]
    check_index_cover(intervals)
    return {"all_computational_obligations_verified":True,
            "relative_to_written_analytic_reductions_and_literature":True,
            "lean_formalization_claimed":False, "outstanding":[]}
