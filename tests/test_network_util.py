from unittest import TestCase
from data import NetworkUtil


class TestNetworkUtil(TestCase):

    def test_get_authentication_url(self):
        result = NetworkUtil._get_authentication_url()
        expected = 'https://api.vrv.co/core/'
        self.assertEqual(result, expected)

    def test_get_discover_url(self):
        result = NetworkUtil._get_discover_url()
        expected = 'https://api.vrv.co/disc/public/v1/US/M2/-/-/'
        self.assertEqual(result, expected)

    def test_get_collection_url(self):
        result = NetworkUtil._get_collection_url()
        expected = 'https://api.vrv.co/cms/v2/US/M2/-/'
        self.assertEqual(result, expected)
