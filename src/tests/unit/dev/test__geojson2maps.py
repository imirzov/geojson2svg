#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestGeojson2Maps(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__dev__geojson2maps__extract_features(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__geojson2maps__get_parent_by_id(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__geojson2maps__Feature____str__(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
