import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestDev(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__dev__dev__check_order(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__dev__get_border_points(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__dev__remove_points_without_pair(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__dev__swap_points(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__dev__test(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__dev__tie_border_points(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
