#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Format GeoJSON files with consistent indentation and encoding."""

import json
from pathlib import Path

from settings import files, encoding


def format_geojson_file(fpath: Path) -> None:
    with open(fpath, 'r', encoding=encoding) as f:
        data = json.load(f)
    formatted = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    with open(fpath, 'w', encoding=encoding) as f:
        f.write(formatted)


def main(folder: Path = files) -> None:
    for fpath in sorted(folder.rglob('*.geojson')):
        format_geojson_file(fpath)


if __name__ == '__main__':
    main()
