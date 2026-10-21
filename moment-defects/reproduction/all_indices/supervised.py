"""Keep failure diagnostics without changing the original bounded launcher's rules."""
from __future__ import annotations
import json
from pathlib import Path


def run_recorded(runner, argv, work, label, cpu_limit, memory_limit, **kwargs):
    try:
        return runner.run_child(argv,work,label,cpu_limit,memory_limit,**kwargs)
    except Exception as exc:
        trace, frame = exc.__traceback__, None
        guard_file = None
        while trace is not None:
            candidate = trace.tb_frame
            if (candidate.f_code.co_name == 'parent_guard' and
                    Path(candidate.f_code.co_filename).resolve() == Path(runner.__file__).resolve()):
                value = candidate.f_locals.get('file')
                if isinstance(value,Path):
                    guard_file = str(value)
            if (candidate.f_code.co_name == "run_child" and
                    Path(candidate.f_code.co_filename).resolve() == Path(runner.__file__).resolve()):
                frame = candidate
            trace = trace.tb_next
        details = {"scope":"FAILED_STAGE_DIAGNOSTICS_ONLY","stage":label,
                   "error":str(exc),"arithmetic_accepted":False,
                   "all_index_conclusion_verified":False}
        if guard_file is not None:
            details['guard_file_at_failure'] = guard_file
        if frame is not None:
            local = frame.f_locals
            outputs = local.get("outputs",{})
            total = 0
            for channel in ("stdout","stderr"):
                raw = outputs.get(channel,b"") if isinstance(outputs,dict) else b""
                if not isinstance(raw,(bytes,bytearray)):
                    continue
                total += len(raw)
                if total > 16*1024**2:
                    break
                with (work/(label+".failed."+channel+".txt")).open("xb") as stream:
                    stream.write(raw)
                details[channel+"_bytes"] = len(raw)
            process = local.get("process")
            details["child_returncode"] = None if process is None else process.returncode
            for field in ("cpu","active","peak"):
                value = local.get(field)
                if type(value) in (int,float):
                    details["last_sample_"+field] = value
        with (work/(label+".failure.json")).open("x",encoding="utf-8") as stream:
            json.dump(details,stream,indent=2)
        raise
