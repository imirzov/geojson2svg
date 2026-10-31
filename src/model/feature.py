#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Iterator

from model.obj import Obj


class Geometry:
    """GeoJSON geometry."""

    def __init__(self, d: dict[str, Any]) -> None:
        self.type: str = d.get('type', '')
        self.coordinates: Any = d.get('coordinates', {})


class Feature:
    """GeoJSON feature."""

    def __init__(self, d: dict[str, Any]) -> None:
        self.type: str = d.get('type', '')
        self.properties: dict[str, Any] = d.get('properties', {})
        self.geometry: Geometry = Geometry(d.get('geometry', {}))
        self.children: list[Obj] = [
            # Point, LineString, Polygon,
            # MultiPoint, MultiLineString, MultiPolygon
        ]

    def add_child(self, child: Obj) -> None:
        self.children.append(child)

    def get_children(self) -> list[Obj]:
        return self.children


def get_features(fpath: Path) -> Iterator[Feature]:
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for feature in data['features']:
        yield Feature(feature)
