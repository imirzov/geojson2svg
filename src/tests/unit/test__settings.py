import time
import unittest

import log


class TestSettings(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__settings__time_now(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__settings__to_en(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
