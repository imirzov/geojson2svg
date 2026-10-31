#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest
from math import inf

from base.lands import (Point, Linestring, Polygon,
                        Multipoint, Multilinestring, Multipolygon)
from core import Good0 as MapObj
from base.log import r, initialize_logging, log_time_delta


class TestBBoxes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def test_bboxes(self) -> None:
        for s in (Point, Linestring, Polygon,
                  Multipoint, Multilinestring, Multipolygon):
            with self.subTest(s.fpath.stem):
                mo = MapObj(s)
                msg = f'{s.fpath.stem}\n{mo.bbox}'
                r.info(msg)
                assert inf not in (mo.bbox.xmin, mo.bbox.xmax,
                                   mo.bbox.ymin, mo.bbox.ymax), mo.bbox

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
