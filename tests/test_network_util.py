from unittest import TestCase
from data import NetworkUtil
from di import UtilityClientScopeProvider


class TestNetworkUtil(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.__network_util: NetworkUtil = UtilityClientScopeProvider.network_client()

    def test_create_session(self):
        result = self.__network_util.create_session()
        self.assertIsNotNone(result)

    def test_get_authentication_url(self):
        result = NetworkUtil.get_authentication_url()
        expected = 'https://api.vrv.co/core/'
        self.assertEqual(expected, result)

    def test_get_discover_url(self):
        result = NetworkUtil.get_discover_url()
        expected = 'https://api.vrv.co/disc/public/v1/US/M2/-/-/'
        self.assertEqual(expected, result)

    def test_get_collection_url(self):
        result = NetworkUtil.get_collection_url()
        expected = 'https://api.vrv.co/cms/v2/US/M2/-/'
        self.assertEqual(expected, result)
