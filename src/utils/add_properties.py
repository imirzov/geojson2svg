#!python3
# -*- coding: utf-8 -*-

"""Ensure each GeoJSON feature has properties dict with key name."""

import json
from pathlib import Path
from typing import Any, cast

from settings import encoding


def _fix_feature(f: dict[str, Any]) -> dict[str, Any]:
    """Move all keys except type and geometry into properties dict."""
    props: dict[str, Any] = {}
    raw = f.get('properties')
    if isinstance(raw, dict):
        props = cast(dict[str, Any], raw)
    keep = ('type', 'geometry', 'properties')
    for key in [k for k in f if k not in keep]:
        props[key] = f.pop(key)
    props.setdefault('name', '')
    f['properties'] = props
    return f


def add_properties(src: Path) -> int:
    """Convert file, return number of features."""
    with src.open('r', encoding=encoding) as f:
        data = json.load(f)
    features = data.get('features', [])
    for f in features:
        _fix_feature(f)
    with src.open('w', encoding=encoding) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(features)
