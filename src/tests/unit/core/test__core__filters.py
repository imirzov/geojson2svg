import time
import unittest

import log


class TestFilters(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__core__filters__Round__apply(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core__filters__Smooth__apply(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
