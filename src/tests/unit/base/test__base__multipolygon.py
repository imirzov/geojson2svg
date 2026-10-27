import time
import unittest

from services.log import initialize_logging, log_time_delta


class TestMultiPolygon(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__base__multipolygon__create_multipolygon(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__multipolygon__find_overlapping_multipolygons(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__multipolygon__is_multipolygon(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__multipolygon__MultiPolygon__get_children(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__multipolygon__MultiPolygon__get_points(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__multipolygon__MultiPolygon__set_children(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
