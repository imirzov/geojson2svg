import time
import unittest

import log


class TestCore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.start = time.perf_counter()
        log.initialize_logging()

    @unittest.skip('TODO: implement test')
    def test__core____init____Dev__run(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good0__run(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good1__collapse_gaps(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good1__run(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good2__collapse_gaps(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good2__run(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good3__get_border_point_clouds(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good3__run(self) -> None:
        pass

    @unittest.skip('TODO: implement test')
    def test__core____init____Good4__run(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        log.log_time_delta(cls.start)
