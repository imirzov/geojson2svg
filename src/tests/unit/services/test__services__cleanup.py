import time
import unittest

from services.log import initialize_logging, log_time_delta


class TestServicesCleanup(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__services__cleanup__recursively_remove_keys(self) -> None:
        # f = ...
        # try:
        #     f(...)
        # except Exception as e:
        #     msg = f'{f.__name__} raised ' \
        #           f'{e.__class__.__name__}: {e}\n' \
        #           + traceback.format_exc()
        #     r.error(msg)
        #     self.fail(msg)
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
