from datetime import datetime
from unittest import TestCase

from data.util import TimeUtil
from di import UtilityClientScopeProvider


class TestTimeUtil(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.time_util: TimeUtil = UtilityClientScopeProvider.time_zone_client()

    def test_default_timezone(self):
        default = self.time_util.default_timezone()
        self.assertIsNotNone(default)
        self.assertEqual('UTC', default.zone)

    def test_as_local_time(self):
        expected = datetime.strptime('2020-03-16T21:37:14+0200', '%Y-%m-%dT%H:%M:%S%z')
        result = self.time_util.as_local_time('2020-03-16T19:37:14+0000', '%Y-%m-%dT%H:%M:%S%z')
        self.assertEqual(expected.toordinal(), result.toordinal())
