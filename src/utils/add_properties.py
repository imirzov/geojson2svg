#!python3
# -*- coding: utf-8 -*-

"""Ensure each GeoJSON feature has properties dict with key name."""

import json
from pathlib import Path
from typing import Any

from settings import files, encoding


def fix_feature(f: dict[str, Any]) -> dict[str, Any]:
    """Move name into properties dict, creating it when missing."""
    props = f.get('properties')
    if not isinstance(props, dict):
        props = {}
    if 'name' not in props:
        props['name'] = f.get('name', '')
    f['properties'] = props
    return f


def add_properties(src: Path) -> int:
    """Convert file, return number of features."""
    with src.open('r', encoding=encoding) as f:
        data = json.load(f)
    features = data.get('features', [])
    for f in features:
        fix_feature(f)
    with src.open('w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(features)


def main() -> None:
    src = files / 'districts' / '4.geojson'
    count = add_properties(src)
    print(f'{count} features written to {src}')


if __name__ == '__main__':
    main()
