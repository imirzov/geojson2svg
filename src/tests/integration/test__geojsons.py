#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import unittest
from collections.abc import Iterator
import time
from typing import Any

from model.point import Point
from model.linestring import LineString
from model.polygon import Polygon
from model.multipoint import MultiPoint
from model.multilinestring import MultiLineString
from model.multipolygon import MultiPolygon
from settings import files, encoding
from base.log import initialize_logging, log_time_delta

GEOMETRY_TYPES = ('Polygon', 'MultiPolygon')


def get_feature_subdict(fpath: Path, key: str) -> Iterator[Any]:
    with fpath.open(encoding=encoding) as f:
        data: dict[str, Any] = json.load(f)

    if data.get('type') == 'FeatureCollection':
        for feature in data['features']:
            if feature.get('type') == 'Feature' and key in feature:
                yield feature[key]


def get_feature_properties(fpath: Path) -> Iterator[dict[str, Any]]:
    with fpath.open(encoding=encoding) as f:
        data: dict[str, Any] = json.load(f)

    if data.get('type') == 'FeatureCollection':
        for feature in data['features']:
            if feature.get('type') == 'Feature' and 'properties' in feature:
                yield feature['properties']


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()
        # folder = files / 'districts'
        cls.paths = sorted(files.rglob('*.geojson'))

    def test__feature_keys(self) -> None:
        for fpath in self.paths:
            with self.subTest(str(fpath.relative_to(files))):
                with fpath.open(encoding=encoding) as f:
                    data: dict[str, Any] = json.load(f)
                    for feature in data['features']:
                        assert 'type' in feature
                        assert 'properties' in feature
                        assert 'geometry' in feature

    def test__geometries(self) -> None:
        for fpath in self.paths:
            with self.subTest(str(fpath.relative_to(files))):
                for geometry in get_feature_subdict(fpath, 'geometry'):
                    if geometry['type'] == 'Polygon':
                        Polygon(geometry['coordinates'])
                    if geometry['type'] == 'MultiPolygon':
                        MultiPolygon('test', geometry['coordinates'])

    def test__name_in_properties(self) -> None:
        for fpath in self.paths:
            with self.subTest(str(fpath.relative_to(files))):
                with fpath.open(encoding=encoding) as f:
                    data: dict[str, Any] = json.load(f)
                for i, feature in enumerate(data.get('features', [])):
                    props: dict[str, Any] = feature.get('properties') or {}
                    self.assertIn(
                        'name',
                        props,
                        f'Feature #{i} has no "name" in properties',
                    )

    def test__geojson_types(self) -> None:
        fpaths = Path(files / 'tests').glob('*.geojson')
        for fpath in fpaths:
            with self.subTest(str(fpath.relative_to(files))):
                for geometry in get_feature_subdict(fpath, 'geometry'):
                    if geometry['type'] == 'Point':
                        Point(geometry['coordinates'])
                    if geometry['type'] == 'LineString':
                        LineString(geometry['coordinates'])
                    if geometry['type'] == 'Polygon':
                        Polygon(geometry['coordinates'])
                    if geometry['type'] == 'MultiPoint':
                        MultiPoint('test', geometry['coordinates'])
                    if geometry['type'] == 'MultiLineString':
                        MultiLineString(geometry['coordinates'])
                    if geometry['type'] == 'MultiPolygon':
                        MultiPolygon('test', geometry['coordinates'])

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
