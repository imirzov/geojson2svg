import time
import unittest

import log


class TestGeojson2ConfigGeo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__geojson2configgeo__extract_features(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__geojson2configgeo__get_parent_by_id(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__geojson2configgeo__Feature____str__(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
