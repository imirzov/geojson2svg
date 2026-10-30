import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__settings__time_now(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__settings__to_en(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
