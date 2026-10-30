import time
import unittest

from base.log import initialize_logging, log_time_delta


class TestServicesFilters(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__services__filters__RemoveSamePoints__apply(self) -> None:
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

    @unittest.skip('TODO: implement test')
    def test__services__filters__Round__apply(self) -> None:
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

    @unittest.skip('TODO: implement test')
    def test__services__filters__Smooth__apply(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log_time_delta(cls.start)
