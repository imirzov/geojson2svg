import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestGeojson2ConfigGeo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__dev__geojson2configgeo__extract_features(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__geojson2configgeo__get_parent_by_id(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__dev__geojson2configgeo__Feature____str__(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
