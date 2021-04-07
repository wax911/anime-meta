from unittest import TestCase
from data import NetworkUtil
from di import UtilityClientScopeProvider


class TestNetworkUtil(TestCase):
    __network_util: NetworkUtil

    def setUp(self) -> None:
        super().setUp()
        self.__network_util = UtilityClientScopeProvider.network_client()

    def test_create_session(self):
        result = self.__network_util.create_session()
        self.assertIsNotNone(result)

    def test_get_authentication_url(self):
        result = self.__network_util.get_authentication_url()
        self.assertIsNotNone(result)

    def test_get_discover_url(self):
        result = self.__network_util.get_discover_url()
        self.assertIsNotNone(result)

    def test_get_collection_url(self):
        result = self.__network_util.get_collection_url()
        self.assertIsNotNone(result)
