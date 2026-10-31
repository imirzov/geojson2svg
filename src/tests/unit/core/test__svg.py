#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import traceback
import unittest

from base.log import r, initialize_logging, log_time_delta
from base.lands import (Point, Linestring, Polygon,
                        Multipoint, Multilinestring, Multipolygon)
from core import Good0 as MapObj
from core.svg import Svg


class TestCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def test__core__svg__Svg__run(self) -> None:
        for s in (Point, Linestring, Polygon,
                  Multipoint, Multilinestring, Multipolygon):
            with self.subTest(s.fpath.stem):
                svg_fpath = s.fpath.with_suffix('.svg')
                if svg_fpath.exists():
                    svg_fpath.unlink()

                try:
                    mo = MapObj(s)
                    Svg(mo).run()
                except Exception:
                    msg = traceback.format_exc()
                    r.error(msg)
                    self.fail(msg)

                assert svg_fpath.exists()

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
