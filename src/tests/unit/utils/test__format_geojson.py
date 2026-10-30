#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__utils__format_geojson__format_geojson(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
