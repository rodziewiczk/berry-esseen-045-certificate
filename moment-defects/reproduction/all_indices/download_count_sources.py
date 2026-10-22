"""Fetch pinned original count archives from GitHub; NOT mathematical replay."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
REPOSITORY = 'rodziewiczk/berry-esseen-045-certificate'
ASSETS = (
    dict(release_tag='cutoff20-sources-2026-10-17',name='cutoff25_20261011.zip',bytes=514958998,
         sha256='17fa140f63c5134ac48f1fd1040f4c5ae4bebdb2b92b2d7ce69f4048293d1fcb'),
    dict(release_tag='cutoff25-base-sources-2026-10-22',name='cutoff25_20261013.zip',bytes=529557492,
         sha256='a97f3e6e50e428df0893304bcd2f746851c9fccef2079b1ec66be9ab909d7f2c'),
)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,default=BASE/'reproduction_inputs/count-source-archives')
    p.add_argument('--download',action='store_true',help='Fetch missing pinned assets, never overwrite bad data')
    args = p.parse_args()
    source = BASE/'five-summands-2026-10-20/download_sources.py'
    spec = importlib.util.spec_from_file_location('pinned_archive_downloader',source)
    downloader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(downloader)
    if args.download: args.directory.mkdir(parents=True,exist_ok=True)
    for entry in ASSETS:
        if args.download:
            downloader.download(dict(repository=REPOSITORY,release_tag=entry['release_tag']),entry,args.directory)
        else:
            downloader.verify(args.directory/entry['name'],entry)
            print('Verified source bytes:',entry['name'],flush=True)
    print(json.dumps(dict(scope='ORIGINAL_SOURCE_AVAILABILITY_ONLY',assets=ASSETS,
                          arithmetic_replayed=False,all_index_conclusion_verified=False)),flush=True)


if __name__ == '__main__':
    main()
