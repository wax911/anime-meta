from requests_oauthlib import OAuth1Session

from core.util.file_system import InputOutputHelper

from ..source.remote_sources import DiscoverEndpoint, CollectionEndpoint, AuthenticationEndpoint


class BaseUtil(object):

    def __init__(self) -> None:
        self._attachment = InputOutputHelper.get_file_contents('secrets.json')


class DatabaseUtil(BaseUtil):

    def create_connection_string(self) -> str:
        __schema = "mongodb://"
        __client = self._attachment['client']
        __authenticator = self._attachment['authenticator']
        __apiKey = self._attachment['apiKey']
        __hostName = self._attachment['hostName']
        return f"{__schema}{__client}:{__apiKey}@{__hostName}/{__authenticator}"

    def get_collection_name(self):
        return self._attachment['collection']


class NetworkUtil(BaseUtil):

    def create_session(self) -> OAuth1Session:
        oauth = self._attachment['oauth']
        return OAuth1Session(
            oauth['key'],
            client_secret=oauth['secret']
        )

    @staticmethod
    def get_request_headers() -> dict:
        return {
            'User-Agent': 'VRV/968 (iPad; iOS 10.2; Scale/2.00)',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Accept-Language': 'en-US;q=1, ja-JP;q=0.9',
        }

    @staticmethod
    def __get_base_url() -> str:
        return 'https://api.vrv.co'

    @staticmethod
    def get_authentication_url():
        NetworkUtil.__get_base_url() + '/core/'

    @staticmethod
    def get_discover_url():
        NetworkUtil.__get_base_url() + '/disc/public/v1/US/M2/-/-/'

    @staticmethod
    def get_collection_url():
        NetworkUtil.__get_base_url() + '/cms/v2/US/M2/-/'


class RequestUtil(NetworkUtil):
    authentication_endpoint: AuthenticationEndpoint
    discover_endpoint: DiscoverEndpoint
    collection_endpoint: CollectionEndpoint

    def __init__(self) -> None:
        super().__init__()
        oauth_session_client = self.create_session()
        self.__create_endpoints(oauth_session_client)

    def __create_endpoints(self, oauth_session_client: OAuth1Session):
        self.authentication_endpoint = AuthenticationEndpoint(
            base_url=self.get_authentication_url(),
            client=oauth_session_client
        )
        self.discover_endpoint = DiscoverEndpoint(
            base_url=self.get_discover_url(),
            client=oauth_session_client
        )
        self.collection_endpoint = CollectionEndpoint(
            base_url=self.get_collection_url(),
            client=oauth_session_client
        )
