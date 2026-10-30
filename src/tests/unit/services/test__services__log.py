import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestServicesLog(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__services__log__float_to_time_str(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__services__log__get_time_delta(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__services__log__initialize_logging(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__services__log__log_time_delta(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
