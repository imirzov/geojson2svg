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
        mpt = create_multipoint('test', [(1.0, 2.0), (3.0, 4.0)])

        try:
            self.assertIs(MULTIPOINTS['test'], mpt)
            self.assertEqual(len(mpt.get_children()), 2)
        finally:
            MULTIPOINTS.pop('test', None)
            for point in mpt.get_points():
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
            for mpt in multipoints:
                for pt in mpt.get_points():
                    POINTS.pop(pt.id_, None)

    def test__model__multipoint__is_multipoint(self) -> None:
        self.assertTrue(is_multipoint([(1.0, 2.0), (3.0, 4.0)]))
        self.assertFalse(is_multipoint([[(1.0, 2.0)]]))

    def test__model__multipoint__MultiPoint__get_children(self) -> None:
        mpt = MultiPoint('test', [(1.0, 2.0)])

        try:
            self.assertEqual(len(mpt.get_children()), 1)
            self.assertIs(mpt.get_children()[0].parent, mpt)
        finally:
            for pt in mpt.get_points():
                POINTS.pop(pt.id_, None)

    def test__model__multipoint__MultiPoint__get_points(self) -> None:
        mpt = MultiPoint('test', [(1.0, 2.0), (3.0, 4.0)])

        try:
            self.assertEqual(len(mpt.get_points()), 2)
            self.assertEqual(mpt.get_points(),
                             mpt.get_children())
        finally:
            for pt in mpt.get_points():
                POINTS.pop(pt.id_, None)

    def test__model__multipoint__MultiPoint__set_children(self) -> None:
        mpt = MultiPoint('test', [(1.0, 2.0)])

        try:
            mpt.set_children([(3.0, 4.0)])
            self.assertEqual(len(mpt.get_children()), 2)
        finally:
            for pt in mpt.get_points():
                POINTS.pop(pt.id_, None)

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
