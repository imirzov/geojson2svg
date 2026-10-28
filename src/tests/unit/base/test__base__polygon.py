#!python3
# -*- coding: utf-8 -*-

import time
import unittest

from base import get_nested_list_depth
from base.polygon import is_polygon
from services.log import initialize_logging, log_time_delta


class TestPolygon(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__base__polygon__create_polygon(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__polygon__find_overlapping_polygons(self) -> None:
        pass

    def test__base__polygon__is_polygon(self) -> None:
        with self.subTest('no'):
            coordinates = [
                [
                    (15.0, 50.0),
                    (16.0, 51.0),
                ],
                [
                    (15.0, 50.0),
                    (16.0, 51.0),
                ],
            ]
            print(get_nested_list_depth(coordinates))
            b = is_polygon(coordinates)
            self.assertFalse(b)
        with self.subTest('yes'):
            coordinates = [[(15.0, 50.0), (16.0, 51.0), ]]
            print(get_nested_list_depth(coordinates))
            b = is_polygon(coordinates)
            self.assertTrue(b)

    @unittest.skip('TODO: implement test')
    def test__base__polygon__Polygon__convert_coords_to_px(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__polygon__Polygon__get_children(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__polygon__Polygon__get_points(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__polygon__Polygon__remove_point(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__polygon__Polygon__set_children(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
