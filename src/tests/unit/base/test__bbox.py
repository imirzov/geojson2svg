import time
import unittest

from base.bbox import BBox
from base.log import initialize_logging, log_time_delta


class TestBBox(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    def test__base__bbox__BBox____add__(self) -> None:
        bbox = BBox() + BBox(1, 4, 2, 5)

        self.assertEqual((bbox.xmin, bbox.xmax), (1, 4))
        self.assertEqual((bbox.ymin, bbox.ymax), (2, 5))

    @unittest.skip('TODO: implement test')
    def test__base__bbox__BBox____str__(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
