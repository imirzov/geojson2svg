import time
import unittest

import log


class TestObj(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__base__obj__Obj__is_overlapping_with(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__base__obj__Obj__set_bbox(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
