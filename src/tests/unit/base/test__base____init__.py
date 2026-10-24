#!python3
# -*- coding: utf-8 -*-

import time
import unittest

from base import get_wrapping_depth
import log


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    def test__base____init____get_wrapping_depth(self) -> None:
        with self.subTest('polygon'):
            pg_coordinates = [[[14.810, 50.858]]]
            wd1 = get_wrapping_depth(pg_coordinates)
            self.assertEqual(wd1, 2)
        with self.subTest('multi-polygon'):
            mpg_coordinates = [pg_coordinates]
            wd2 = get_wrapping_depth(mpg_coordinates)
            self.assertEqual(wd2, 3)

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
