#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time

from base.log import initialize_logging, log_time_delta
from settings import tests
from model.feature import get_features
from model.point import Point
from model.linestring import LineString
from model.polygon import Polygon
from model.multipoint import MultiPoint
from model.multilinestring import MultiLineString
from model.multipolygon import MultiPolygon


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()
        cls.files = tests.glob('*.geojson')

    def test__model(self) -> None:
        with self.subTest('point'):
            fpath = tests / 'point.geojson'
            for feature in get_features(fpath):
                Point(feature.geometry.coordinates)
        with self.subTest('linestring'):
            fpath = tests / 'linestring.geojson'
            for feature in get_features(fpath):
                LineString(feature.geometry.coordinates)
        with self.subTest('polygon'):
            fpath = tests / 'polygon.geojson'
            for feature in get_features(fpath):
                Polygon(feature.geometry.coordinates)
        with self.subTest('multipoint'):
            fpath = tests / 'multipoint.geojson'
            for feature in get_features(fpath):
                MultiPoint('test', feature.geometry.coordinates)
        with self.subTest('multilinestring'):
            fpath = tests / 'multilinestring.geojson'
            for feature in get_features(fpath):
                MultiLineString(feature.geometry.coordinates)
        with self.subTest('multipolygon'):
            fpath = tests / 'multipolygon.geojson'
            for feature in get_features(fpath):
                MultiPolygon('test', feature.geometry.coordinates)

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
