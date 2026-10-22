"""Immutable archive/source catalog for the finite continuation.

Old receipts select byte identities only. In particular, a parent JSON in a
minimal arithmetic capsule remains a CONDITIONAL numerical input, never a
newly executed parent proof. No numerical engine is imported here.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import stat
import zipfile

if __package__:
    from ..all_indices.c5_counts import need, digest, unique
    from ..all_indices.c5_inputs import safe_relative
else:
    from reproduction.all_indices.c5_counts import need, digest, unique
    from reproduction.all_indices.c5_inputs import safe_relative


@dataclass(frozen=True)
class Asset:
    name: str
    size: int
    sha256: str
    roots: tuple[str,...]


CUTOFF6 = Asset('cutoff6_20261020.zip',69459175,
    'd45b1f99ca01ea4d1cfad445fdab3c48a508adf9fdcda17b6cded5236d77b8d6',('cutoff6_20261020',))
COMBINED = Asset('cutoff5_10_15.zip',224483065,
    '268f71662171764d7ebe116910b5df82dfd58cadb2de2a7ef82db7da98b66dae',
    ('cutoff6_20261018','cutoff10_20261018','cutoff15_20261017'))
SUPPORT = 'work/cutoff6_20261020/root/support6_9_join_v1'
SUPPORT_INDEX = SUPPORT+'/REPLAY_CHECKED.json'
SUPPORT_INDEX_SHA = '3919f9edf8b317018ebc0e8796d4d4f297c430dbc875549b86a0df70172eac1a'
PROTOCOL_SHA = '99cf3310e4589f3f541380eeb867c64a876ddae1e68bc16227d0f0511c7f1cbc'
FINAL = 'work/cutoff6_20261020/root/final_composition_v2/CUTOFF6_COMPLETE.json'
FINAL_SHA = 'c73ca47d7a4c8ccffd6c84be4d2805db4c43e86693989dd478b1ecc327517579'
PARENT_FILES = (
    'work/cutoff6_20261018/audit/auxiliary5_readback_v1/RESULT.json',
    'work/cutoff6_20261018/audit/supported_fourier_readback_v1/OWN_RESULT.json',
    'work/cutoff6_20261018/audit/supported_fourier_readback_v1/BRIDGE_RESULT.json',
    'work/cutoff6_20261018/audit/supported_fourier_readback_v1/RADIUS_RESULT.json',
)
REGIONS = (
    ('B0','1','11/10','23/10'),('BN','11/10','23/20','12/5'),
    ('B2','23/20','237/200','5/2'),('bridge','237/200','6/5','13/5'),
    ('A','6/5','7/5','3'),('B','7/5','3/2','16/5'),('C','3/2','8/5','17/5'),
    ('D','8/5','17/10','18/5'),('E','17/10','7361/4000','19/5'),
)


def parse(raw):
    return json.loads(raw.decode('utf-8'),object_pairs_hook=unique)


class Sources:
    """Bounded direct archive lookup; never extract an entire project tree."""
    def __init__(self,cutoff6,combined,*,guard=lambda:None):
        self.archives = []
        try:
            for path,asset in ((Path(cutoff6),CUTOFF6),(Path(combined),COMBINED)):
                guard()
                need(path.is_file() and not path.is_symlink() and path.stat().st_size == asset.size
                     and digest(path) == asset.sha256,'Exact public source archive: '+asset.name)
                archive = zipfile.ZipFile(path)
                self.archives.append((asset,path,archive))
        except BaseException:
            self.close();raise

    def close(self):
        for _,_,archive in self.archives:
            archive.close()
        self.archives.clear()

    def __enter__(self): return self
    def __exit__(self,*unused): self.close()

    def member(self,name,*,max_bytes=16*1024**2):
        safe_relative(name)
        need(name.startswith('work/'),'This minimal source catalog uses explicit work/ identities')
        member = name[len('work/'):]
        for asset,path,archive in self.archives:
            if member.split('/')[0] not in asset.roots:
                continue
            try: info = archive.getinfo(member)
            except KeyError: continue
            need(not info.is_dir() and info.file_size <= max_bytes,
                 'Bounded original source member')
            need(not stat.S_ISLNK(info.external_attr >> 16),'No archived source symlink')
            return archive,info
        raise FileNotFoundError('Original exact member not in these source archives: '+name)

    def read(self,name,pin,*,max_bytes=16*1024**2):
        archive,info = self.member(name,max_bytes=max_bytes)
        raw = archive.read(info)
        need(hashlib.sha256(raw).hexdigest() == pin,'Exact original source bytes: '+name)
        return raw


def support_plan(sources):
    """23 pinned files/191618 bytes; four parent bindings are NOT discharged."""
    original = parse(sources.read(SUPPORT_INDEX,SUPPORT_INDEX_SHA))
    graph = original['files_sha256']
    need(len(graph) == 293,'Original support293 source/reference index, not arithmetic acceptance')
    need(graph[SUPPORT+'/protocol.py'] == PROTOCOL_SHA,'Exact native protocol identity')
    source_manifest = SUPPORT+'/SOURCES.json'
    pins = parse(sources.read(source_manifest,graph[source_manifest]))
    need(type(pins) is dict and len(pins) == 16,'Original four engine copies and analytic source references')
    for name in ('SOURCES.json','protocol.py','PROOF.txt'):
        original_name = SUPPORT+'/'+name
        pins[original_name] = graph[original_name]
    parent_pins = {name:graph[name] for name in PARENT_FILES}
    pins.update(parent_pins)
    need(len(pins) == 23,'Complete minimal runtime plus explicit parent-input closure')
    total = 0
    for name,pin in pins.items():
        need(graph.get(name) == pin,'Every minimal source is in the original source index')
        total += len(sources.read(name,pin))
    need(total == 191618,'Exact selected minimal source byte census')
    # A complete unchanged invocation additionally verifies the historical
    # parents' reference graphs. Record direct unavailability; do not omit it
    # silently, and never substitute the reader's PASS for their replay.
    unavailable = []
    for name in graph:
        try: sources.member(name)
        except (FileNotFoundError,ValueError): unavailable.append(name)
    return dict(schema='CONTINUATION_SUPPORT6_9_SOURCE_PLAN_V1',
        scope='SOURCE_INSPECTION_ONLY_NO_ARITHMETIC_EXECUTED',n=[6,7,8,9],
        native_protocol=SUPPORT+'/protocol.py',original_protocol_sha256=PROTOCOL_SHA,
        original_support_source_index=dict(path=SUPPORT_INDEX,sha256=SUPPORT_INDEX_SHA,files=293),
        source_files_sha256=pins,source_files=23,source_bytes=total,
        conditional_parent_input_files=parent_pins,
        historical_parent_closure_directly_unavailable=unavailable,
        native_internal_actions=[['-B','protocol.py','construct'],['-B','protocol.py','replay']],
        support_targets=36,signed_support_rays=72,native_negative_controls=19,
        source_port_scope='REPLACE_ONLY_RECEIPT_REFERENCE_GRAPH_TRAVERSAL_WITH_PINNED_CONDITIONAL_PARENT_BINDING',
        retained_parent_obligations=[
            'Fresh global C5<429/1000; original four parent JSON are conditional inputs only.',
            'Fresh same-index supported OWN, BRIDGE and RADIUS Fourier facts with complete rho/support domains.',
            'Attainment/contact and each global predecessor: n6 uses q=579/5000; n7..9 use q=0 sequentially.',
            'The original analytic Fourier/profile/smoothing and published infinite-rho tail inequalities.'],
        fresh_parent_fact_joins_verified=False,all_index_conclusion_verified=False)
