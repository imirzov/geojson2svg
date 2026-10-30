#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from base.log import initialize_logging, log_time_delta
from model.multipoint import (
    MULTIPOINTS,
    MultiPoint,
    create_multipoint,
    find_overlapping_multipoints,
    is_multipoint,
)
from model.point import POINTS


class TestMultiPoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def test__model__multipoint__create_multipoint(self) -> None:
        multipoint = create_multipoint('test', [(1.0, 2.0), (3.0, 4.0)])

        try:
            self.assertIs(MULTIPOINTS['test'], multipoint)
            self.assertEqual(len(multipoint.get_children()), 2)
        finally:
            MULTIPOINTS.pop('test', None)
            for point in multipoint.get_points():
                POINTS.pop(point.id_, None)

    def test__model__multipoint__find_overlapping_multipoints(self) -> None:
        first = MultiPoint('first', [(0.0, 0.0), (1.0, 1.0)])
        second = MultiPoint('second', [(0.5, 0.5)])
        third = MultiPoint('third', [(10.0, 10.0)])
        multipoints = [first, second, third]

        try:
            self.assertEqual(
                find_overlapping_multipoints(multipoints),
                [(first, second)],
            )
        finally:
            for multipoint in multipoints:
                for point in multipoint.get_points():
                    POINTS.pop(point.id_, None)

    def test__model__multipoint__is_multipoint(self) -> None:
        self.assertTrue(is_multipoint([(1.0, 2.0), (3.0, 4.0)]))
        self.assertFalse(is_multipoint([[(1.0, 2.0)]]))

    def test__model__multipoint__MultiPoint__get_children(self) -> None:
        multipoint = MultiPoint('test', [(1.0, 2.0)])

        try:
            self.assertEqual(len(multipoint.get_children()), 1)
            self.assertIs(multipoint.get_children()[0].parent, multipoint)
        finally:
            for point in multipoint.get_points():
                POINTS.pop(point.id_, None)

    def test__model__multipoint__MultiPoint__get_points(self) -> None:
        multipoint = MultiPoint('test', [(1.0, 2.0), (3.0, 4.0)])

        try:
            self.assertEqual(len(multipoint.get_points()), 2)
            self.assertEqual(multipoint.get_points(),
                             multipoint.get_children())
        finally:
            for point in multipoint.get_points():
                POINTS.pop(point.id_, None)

    def test__model__multipoint__MultiPoint__set_children(self) -> None:
        multipoint = MultiPoint('test', [(1.0, 2.0)])

        try:
            multipoint.set_children([(3.0, 4.0)])
            self.assertEqual(len(multipoint.get_children()), 2)
        finally:
            for point in multipoint.get_points():
                POINTS.pop(point.id_, None)

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
