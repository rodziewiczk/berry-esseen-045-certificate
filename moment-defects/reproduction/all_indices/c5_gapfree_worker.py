"""Fresh independent arithmetic; historical execution captures are not premises."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique(pairs):
    result = {}
    for k,v in pairs:
        need(k not in result,"Duplicate JSON field")
        result[k] = v
    return result


def main():
    need(__debug__ and not sys.flags.optimize,"Ordinary unoptimized Python")
    inputs = json.loads((HERE/"INPUTS.json").read_text(),object_pairs_hook=unique)
    need(inputs["schema"] == "C5_GAPFREE_INDEPENDENT_REPLAY_INPUTS_V1","Input schema")
    for name,pin in inputs["files"].items():
        need(Path(name).name == name and sha(HERE/name) == pin,"Exact pinned input")
    spec = importlib.util.spec_from_file_location("original_independent_gapfree",HERE/"check.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    forest = json.loads((HERE/"FOREST.json").read_text(),object_pairs_hook=unique)
    exterior = json.loads((HERE/"EXTERIOR.json").read_text(),object_pairs_hook=unique)["exterior"]
    # Do not call the old main(): it validates old captures and their absolute
    # working directories. These full arithmetic functions reconstruct all
    # domains, every leaf, the Gaussian bounds and both exterior inequalities.
    compact = module.validate(forest)
    rays = module.exterior(exterior)
    need((compact["roots"],compact["nodes"],compact["leaves"]) == (60,1994,1027),
         "Whole original forest")
    controls = []
    def reject(value, call, label):
        try:
            call(value)
        except (ValueError,KeyError,TypeError,IndexError,ZeroDivisionError):
            controls.append(label)
        else:
            raise ValueError("Corruption accepted: "+label)
    def first_leaf(tree):
        while tree[0] == "S":
            tree = tree[2]
        return tree
    mutations = [
        ("missing root",lambda q:q["roots"].pop()),
        ("duplicate root",lambda q:q["roots"].__setitem__(1,deepcopy(q["roots"][0]))),
        ("reordered roots",lambda q:q["roots"].reverse()),
        ("wrong rho",lambda q:q["rho"].__setitem__(0,"1")),
        ("wrong target",lambda q:q.update(target="1/2")),
        ("boolean root",lambda q:q["roots"][0]["domain"].update(beta_index=False)),
        ("boolean phase",lambda q:q["roots"][0]["domain"].update(phase=False)),
        ("root-domain gap",lambda q:q["roots"][0]["domain"]["p"].__setitem__(0,"1/3")),
        ("missing tree",lambda q:q["roots"][0].pop("tree")),
        ("false leaf",lambda q:first_leaf(q["roots"][0]["tree"]).__setitem__(1,-1)),
        ("boolean leaf",lambda q:first_leaf(q["roots"][0]["tree"]).__setitem__(1,False)),
        ("extra forest field",lambda q:q.update(accepted=True)),
    ]
    for label,mutation in mutations:
        bad = deepcopy(forest)
        mutation(bad)
        reject(bad,module.validate,label)
    for key,value in (("n",True),("left_score_upper","0"),("right_score_upper","0"),
                      ("beta",["347/1000",str(module.BH)])):
        bad = deepcopy(exterior)
        bad[key] = value
        reject(bad,module.exterior,"false exterior "+key)
    for name,pin in inputs["files"].items():
        need(sha(HERE/name) == pin,"Inputs unchanged after full arithmetic")
    result = {"status":"PASS_FRESH_C5_GAPFREE_INDEPENDENT_WHOLE_LINE",
              "scope":"Positive closed CDF branch, stated rho/beta rectangle, every real threshold",
              "n":5,"rho":forest["rho"],"beta":forest["beta"],"target":forest["target"],
              "compact":compact,"exteriors":rays,"negative_controls":controls,
              "inputs":inputs,"adapter_sha256":sha(Path(__file__)),
              "old_capture_metadata_used_as_a_mathematical_premise":False,
              "unrestricted_C5_or_all_indices_verified_by_this_stage":False}
    with (HERE/"FRESH_GAPFREE_RESULT.json").open("x",encoding="utf-8") as stream:
        json.dump(result,stream,indent=2)
    print(json.dumps(result),flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FRESH_GAPFREE_REPLAY_INCOMPLETE: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(1)
