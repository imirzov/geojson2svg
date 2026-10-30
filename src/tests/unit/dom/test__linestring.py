#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from base.log import initialize_logging, log_time_delta
from dom.linestring import (
    LINESTRINGS,
    LineString,
    create_linestring,
    is_linestring,
)
from dom.point import POINTS


class TestLineString(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def _create_linestring(self) -> LineString:
        linestring = LineString([(15.0, 50.0), (16.0, 51.0)])
        self.addCleanup(self._remove_points, linestring)
        return linestring

    def _remove_points(self, linestring: LineString) -> None:
        for point in linestring.get_points():
            POINTS.pop(point.id_, None)

    def test__dom__linestring__is_linestring(self) -> None:
        self.assertTrue(is_linestring([(15.0, 50.0), (16.0, 51.0)]))
        self.assertFalse(is_linestring([(15.0, 50.0)]))
        self.assertFalse(is_linestring([[(15.0, 50.0), (16.0, 51.0)]]))

    def test__dom__linestring__LineString__get_children(self) -> None:
        linestring = self._create_linestring()
        self.assertEqual(len(linestring.get_children()), 2)

    def test__dom__linestring__LineString__get_points(self) -> None:
        linestring = self._create_linestring()
        self.assertEqual(linestring.get_points(), linestring.get_children())

    def test__dom__linestring__LineString__set_children(self) -> None:
        linestring = self._create_linestring()
        self.assertEqual(len(linestring.children), 2)

    def test__dom__linestring__create_linestring(self) -> None:
        linestring = create_linestring(
            [(15.0, 50.0), (16.0, 51.0)],
        )
        self.addCleanup(self._remove_points, linestring)
        self.addCleanup(LINESTRINGS.pop, linestring.id_, None)
        self.assertIsInstance(linestring, LineString)
        self.assertIs(LINESTRINGS[linestring.id_], linestring)
        self.assertEqual(linestring.get_children(), linestring.get_points())
        self.assertEqual(len(linestring.get_points()), 2)
        self.assertTrue(
            all(
                point.parent is linestring
                for point in linestring.get_points()
            )
        )

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
