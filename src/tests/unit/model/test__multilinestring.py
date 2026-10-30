#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from base.log import initialize_logging, log_time_delta
from model.linestring import LINESTRINGS
from model.multilinestring import (
    MULTILINESTRINGS,
    MultiLineString,
    create_multilinestring,
    is_multilinestring,
)
from model.point import POINTS


class TestMultiLineString(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def _create_multilinestring(self) -> MultiLineString:
        multilinestring = MultiLineString([
            [(15.0, 50.0), (16.0, 51.0)],
            [(17.0, 52.0), (18.0, 53.0)],
        ])
        self.addCleanup(self._remove_multilinestring, multilinestring)
        return multilinestring

    def _remove_multilinestring(
            self, multilinestring: MultiLineString) -> None:
        for linestring in multilinestring.get_children():
            for point in linestring.get_points():
                POINTS.pop(point.id_, None)
            LINESTRINGS.pop(linestring.id_, None)

    def test__model__multilinestring__is_multilinestring(self) -> None:
        self.assertTrue(is_multilinestring([
            [(15.0, 50.0), (16.0, 51.0)],
        ]))
        self.assertFalse(is_multilinestring(
            [(15.0, 50.0), (16.0, 51.0)],
        ))
        self.assertFalse(is_multilinestring([
            [[(15.0, 50.0), (16.0, 51.0)]],
        ]))

    @unittest.skip('TODO: implement test')
    def test__model__multilinestring__MultiLineString__set_children(self) \
            -> None:
        # f = ...
        # try:
        #     f(...)
        # except Exception as e:
        #     msg = f'{f.__name__} raised ' \
        #           f'{e.__class__.__name__}: {e}\n' \
        #           + traceback.format_exc()
        #     r.error(msg)
        #     self.fail(msg)
        pass

    def test__model__multilinestring__MultiLineString__get_children(
            self) -> None:
        multilinestring = self._create_multilinestring()
        self.assertEqual(len(multilinestring.get_children()), 2)

    def test__model__multilinestring__MultiLineString__get_points(
            self) -> None:
        multilinestring = self._create_multilinestring()
        self.assertEqual(len(multilinestring.get_points()), 4)

    def test__model__multilinestring__create_multilinestring(self) -> None:
        multilinestring = create_multilinestring([
            [(15.0, 50.0), (16.0, 51.0)],
        ])
        self.addCleanup(self._remove_multilinestring, multilinestring)
        self.addCleanup(
            MULTILINESTRINGS.pop, multilinestring.id_, None,
        )
        self.assertIsInstance(multilinestring, MultiLineString)
        self.assertIs(
            MULTILINESTRINGS[multilinestring.id_], multilinestring,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
