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
            pg_coordinates = [
                [
                    [
                        14.810392701669292,
                        50.85844717947565
                    ]
                ]
            ]
            wd1 = get_wrapping_depth(pg_coordinates)
            self.assertEqual(wd1, 2)
        with self.subTest('multi-polygon'):
            mpg_coordinates = [
                [
                    [
                        [
                            14.304,
                            51.055
                        ]
                    ]
                ]
            ]
            wd2 = get_wrapping_depth(mpg_coordinates)
            self.assertEqual(wd2, 3)

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
