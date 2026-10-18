#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

from geojson2svg.common import Point


class TestPoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test__geojson2svg__common__point____hash__(self) -> None:
        a = Point(1, 2)
        b = Point(1, 2)
        c = Point(1, 3)
        assert a == b and hash(a) == hash(b)
        assert len({a, b, c}) == 2

    @classmethod
    def tearDownClass(cls) -> None:
        pass
