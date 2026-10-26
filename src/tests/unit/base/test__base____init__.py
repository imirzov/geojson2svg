#!python3
# -*- coding: utf-8 -*-

import time
import unittest

from base import get_nested_list_depth
import log


class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    def test__base____init____get_wrapping_depth(self) -> None:
        with self.subTest('float'):
            f = 1.23
            wd0 = get_nested_list_depth(f)
            self.assertEqual(wd0, 0)
        with self.subTest('point'):
            p = [1, 2]
            wd0_int = get_nested_list_depth(p)
            self.assertEqual(wd0_int, 1)
        with self.subTest('polygon'):
            pg_coordinates = [[
                [14.810, 50.858],
                [14.810, 50.858],
                ]]
            wd1 = get_nested_list_depth(pg_coordinates)
            self.assertEqual(wd1, 3)
        with self.subTest('multi-polygon'):
            mpg_coordinates = [pg_coordinates]
            wd2 = get_nested_list_depth(mpg_coordinates)
            self.assertEqual(wd2, 4)

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
