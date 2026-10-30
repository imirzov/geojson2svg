#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)

    @unittest.skip('TODO: implement test')
    def test__base__log__time_now(self) -> None:
        pass


class TestServicesLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__base__log__float_to_time_str(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__log__get_time_delta(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__log__initialize_logging(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__log__log_time_delta(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
