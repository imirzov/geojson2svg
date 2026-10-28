#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import unittest
from collections.abc import Iterator
import time
from typing import Any
import traceback

from base.polygon import Polygon
from base.multipolygon import MultiPolygon
from settings import files
from services.log import r, initialize_logging, log_time_delta

GEOMETRY_TYPES = ('Polygon', 'MultiPolygon')


def get_feature_geometries(fpath: Path) -> Iterator[tuple[int, Any]]:
    with fpath.open(encoding='utf-8') as f:
        data: dict[str, Any] = json.load(f)

    if data.get('type') == 'FeatureCollection':
        for i, feature in enumerate(data['features']):
            if feature.get('type') == 'Feature' and 'geometry' in feature:
                yield i, feature['geometry']


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()
        cls._paths = sorted(files.rglob('*.geojson'))

    def test__geojsons(self) -> None:
        self.assertTrue(self._paths, f'No geojson files in {files}')
        for path in self._paths:
            with self.subTest(str(path.relative_to(files))):
                for i, geometry in get_feature_geometries(path):
                    type_ = geometry['type']
                    assert type_ in GEOMETRY_TYPES
                    assert 'coordinates' in geometry
                    try:
                        if type_ == 'Polygon':
                            Polygon(geometry['coordinates'])
                        elif type_ == 'MultiPolygon':
                            MultiPolygon('test', geometry['coordinates'])
                    except Exception:
                        e = traceback.format_exc()
                        msg = f'Feature #{i} in\n{path}\n{e}'
                        r.error(msg)
                        self.fail()

    def test__nazev_in_properties(self) -> None:
        self.assertTrue(self._paths, f'No geojson files in {files}')
        for path in self._paths:
            with self.subTest(str(path.relative_to(files))):
                with path.open(encoding='utf-8') as f:
                    data: dict[str, Any] = json.load(f)
                for i, feature in enumerate(data.get('features', [])):
                    props = feature.get('properties') or {}
                    self.assertIn(
                        'nazev',
                        props,
                        f'Feature #{i} has no "nazev" in properties',
                    )

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
