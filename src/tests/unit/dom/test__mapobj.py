import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestMapObj(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__dom__mapobj__MapObj____add__(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dom__mapobj__MapObj____str__(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dom__mapobj__MapObj__get_children(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dom__mapobj__MapObj__get_points(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dom__mapobj__MapObj__read_children(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dom__mapobj__MapObj__remove_close_points(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
