#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import unittest

from base.point import POINTS, Point, create_point
from services.log import initialize_logging, log_time_delta


class TestPoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def test__base__point__create_point(self) -> None:
        points = [
            create_point((float(i), float(i)))
            for i in range(3)
        ]
        POINTS.pop(points[0].id_)

        try:
            new_point = create_point((3.0, 3.0))

            self.assertIs(POINTS[points[2].id_], points[2])
            self.assertIs(POINTS[new_point.id_], new_point)
            self.assertNotEqual(new_point.id_, points[2].id_)
        finally:
            for point in points:
                POINTS.pop(point.id_, None)

    @unittest.skip("TODO: implement test")
    def test__base__point__merge_points_to(self) -> None:
        ...

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)


class TestPoint__Point(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip("TODO: implement test")
    def test__base__point__Point____str__(self) -> None:
        ...

    @unittest.skip("TODO: implement test")
    def test__base__point__Point__close_to(self) -> None:
        ...

    @unittest.skip("TODO: implement test")
    def test__base__point__Point__get_children(self) -> None:
        ...

    @unittest.skip("TODO: implement test")
    def test__base__point__Point__get_points(self) -> None:
        ...

    @unittest.skip("TODO: implement test")
    def test__base__point__Point__round(self) -> None:
        ...

    def test__base__point__Point____hash__(self) -> None:
        a = Point((1, 2))
        b = Point((1, 2))
        c = Point((1, 3))
        assert a == b and hash(a) == hash(b)
        assert len({a, b, c}) == 2

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
