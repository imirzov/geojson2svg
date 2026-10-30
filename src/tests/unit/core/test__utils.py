import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__core__utils__collapse_gap_1(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core__utils__collapse_gap_2(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core__utils__get_bbox(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core__utils__get_closest_point(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core__utils__recursive_quad_merge(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
