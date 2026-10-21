"""Extract one externally pinned original search capsule; no proof acceptance."""
import argparse
import json
from pathlib import Path
import sys
import zipfile
from count_discovery import need, digest
import hashlib

sys.dont_write_bytecode = True
TARGETS = {
    'b4-q0': ('global_alpha_stoploss2_b4_p29_q0_v12','4d91657ddbab41e3324c00f9f28a9223526c0c1dc79bad5c5e77176240c231f7'),
    'b4-q1': ('global_alpha_stoploss2_b4_p29_q1_v12','a3cbdb1852bc51054ecc8cd3c71bd1c7121b6b201385e481b73195ad729189c4'),
    'b4-q2': ('global_alpha_stoploss2_b4_p29_q2_v12','2517c1b8c79949bad93eecdcaa43e389344411fd4c71d5d516dde1e40b732e2a'),
    'b4-q3': ('global_alpha_stoploss2_b4_p29_q3_v12','c8555b500c3e7d1ca1240b5f229f7fff5ed307571012209e022431ecd195b7ac'),
    'b3-p33': ('global_alpha_stoploss2_b3_p33_v12','e55bb3eeac06923f897263a65f2cde9fe77006313dd86f47bbba3f6047f30f08'),
    # Alternatives to the two missing selected V14 capsules, NOT their historical identities.
    'b3-p31-v12-alternative': ('global_alpha_stoploss2_b3_p31_v12','971204850bbb25e7444d4e9069e32b688aa20e238687da118cfdda9bf1d32d6f'),
    'b3-p32-v12-alternative': ('global_alpha_stoploss2_b3_p32_v12','39de43416357a20bb63b54cd337855a8b429362c1a250dd07b34c1d37339703e'),
}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--target',choices=tuple(TARGETS),required=True)
    p.add_argument('--output',type=Path,required=True)
    args = p.parse_args()
    name,pin = TARGETS[args.target]
    prefix = 'cutoff25_20261011/new_root/'+name+'/'
    need(not args.output.exists(),'Exclusive new capsule directory')
    with zipfile.ZipFile(args.archive) as archive:
        names = archive.namelist()
        design_name = prefix+'FROZEN_DESIGN.json'
        need(names.count(design_name) == 1,'Unique original design member')
        need(archive.getinfo(design_name).file_size <= 1024**2,'Bounded design')
        raw = archive.read(design_name)
        need(hashlib.sha256(raw).hexdigest() == pin,'Externally pinned capsule design')
        design = json.loads(raw)
        need(type(design.get('files')) is dict and len(design['files']) == 76,'All 76 frozen inputs')
        args.output.mkdir(parents=True,exist_ok=False)
        for filename,expected in dict(design['files'], **{'FROZEN_DESIGN.json':pin}).items():
            need(Path(filename).name == filename and '/' not in filename and '\\' not in filename,
                 'Flat source member')
            member = prefix+filename
            need(names.count(member) == 1,'Unique source member')
            info = archive.getinfo(member)
            need(not info.is_dir() and info.file_size <= 16*1024**2 and
                 (info.external_attr >> 16) & 0o170000 != 0o120000,'Bounded regular source')
            data = archive.read(info)
            need(hashlib.sha256(data).hexdigest() == expected,'Exact original source bytes')
            with (args.output/filename).open('xb') as stream:
                stream.write(data)
    print(json.dumps(dict(scope='ORIGINAL_SEARCH_INPUTS_ONLY',target=args.target,
                          design_sha256=pin,files=77,arithmetic_accepted=False)),flush=True)


if __name__ == '__main__':
    main()
