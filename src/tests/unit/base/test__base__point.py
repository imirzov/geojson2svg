#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

from base.point import Point


class TestPoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @unittest.skip("TODO: implement test")
    def test__base__point__create_point(self) -> None:
        ...

    @unittest.skip("TODO: implement test")
    def test__base__point__merge_points_to(self) -> None:
        ...

    @classmethod
    def tearDownClass(cls) -> None:
        pass


class TestPoint__Point(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test__base__point__Point____hash__(self) -> None:
        a = Point((1, 2))
        b = Point((1, 2))
        c = Point((1, 3))
        assert a == b and hash(a) == hash(b)
        assert len({a, b, c}) == 2

    @classmethod
    def tearDownClass(cls) -> None:
        pass
