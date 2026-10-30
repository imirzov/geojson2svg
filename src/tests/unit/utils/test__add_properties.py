import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__utils__add_properties___fix_feature(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__utils__add_properties__add_properties(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
