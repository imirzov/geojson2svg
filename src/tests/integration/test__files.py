#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time

from model.feature import get_features
from model.polygon import Polygon
from model.multipolygon import MultiPolygon
from settings import files
from base.log import initialize_logging, log_time_delta

GEOMETRY_TYPES = ('Polygon', 'MultiPolygon')


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()
        # folder = files / 'districts'
        cls.paths = sorted(files.rglob('*.geojson'))

    def test_features(self) -> None:
        for fpath in self.paths:
            with self.subTest(str(fpath.relative_to(files))):
                for feature in get_features(fpath):
                    assert feature.type == 'Feature'
                    assert feature.properties
                    assert feature.geometry
                    assert feature.geometry.type
                    assert feature.geometry.coordinates

    def test_geometry_types(self) -> None:
        for fpath in self.paths:
            with self.subTest(str(fpath.relative_to(files))):
                for feature in get_features(fpath):
                    g = feature.geometry
                    c = g.coordinates
                    if g.type == 'Polygon':
                        Polygon(c)
                    if g.type == 'MultiPolygon':
                        MultiPolygon('test', c)

    def test_name_in_properties(self) -> None:
        for fpath in self.paths:
            with self.subTest(str(fpath.relative_to(files))):
                for i, feature in enumerate(get_features(fpath)):
                    self.assertIn(
                        'name',
                        feature.properties,
                        f'Feature #{i} has no "name" in properties',
                    )

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
