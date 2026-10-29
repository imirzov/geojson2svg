#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Format GeoJSON files with consistent indentation and encoding."""

import json
from pathlib import Path

from settings import encoding


def format_geojson(fpath: Path) -> None:
    with open(fpath, 'r', encoding=encoding) as f:
        data = json.load(f)
    # formatted = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    # with open(fpath, 'w', encoding=encoding) as f:
    #     f.write(formatted)
    with fpath.open('w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
