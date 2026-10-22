import time
import unittest

import log


class TestLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__log__float_to_time_str(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__log__get_time_delta(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__log__initialize_logging(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__log__log_time_delta(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
