import time
import unittest

from services.log import initialize_logging, log_time_delta


class TestBBox(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__base__bbox__BBox____add__(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__bbox__BBox____str__(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
