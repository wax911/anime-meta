from typing import List

from mongo_thingy import Thingy, Cursor
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConfigurationError
from requests import Response

from data import TimeUtil, LoggingUtil, DatabaseUtil
from data.mapper import SigningPolicyMapper
from domain.entity import SigningPolicy


class Dao(Thingy):
    """ Database access object contract """

    def __init__(self, logger_client: LoggingUtil, timezone_client: TimeUtil, database_client: DatabaseUtil) -> None:
        super().__init__()
        self._logger = logger_client.get_default_logger(__name__)
        self._timezone_client = timezone_client
        self._database_client = database_client
        self._database_client.connect()
        # self.__init_database()

    def __init_database(self):
        __connection = self._database_client.create_connection_string()
        self._client = MongoClient(__connection)
        try:
            self._database = self._client.get_database()
        except ConfigurationError as e:
            self._logger.error(
                "Configuration error prevented database from connecting: %s",
                __connection,
                exc_info=e
            )

    @classmethod
    def get_collection(cls) -> Collection:
        return super().get_collection()


class AuthenticationDao(Dao):
    _collection_name = 'authentication'

    def __get_current_timestamp(self) -> int:
        current_date_time = self._timezone_client.get_current_time()
        current_time_stamp = self._timezone_client.from_date_time_to_time_stamp(current_date_time)
        return current_time_stamp

    def __assure_only_valid_sessions_exist(self) -> None:
        query = {
            "expires": {
                "$lt": self.__get_current_timestamp()
            }
        }
        delete_result = self.get_collection().delete_many(filter=query)
        if delete_result.deleted_count > 0:
            self._logger.info(
                'Invalidated database items with query: %s and returned result: %s',
                query,
                delete_result.deleted_count
            )

    def contains_valid_sessions(self) -> Cursor:
        query = {
            "expires": {
                "$gt": self.__get_current_timestamp()
            }
        }
        filtered = self.find(query)
        self._logger.debug('Query results for query: %s returned `%s` results', query, filtered.count())
        return filtered

    def save_new_policy(self, response: Response) -> List[SigningPolicy]:
        self.__assure_only_valid_sessions_exist()
        singing_policies = SigningPolicyMapper.map_from_response(
            response,
            self._timezone_client
        )
        singing_policies_map = SigningPolicyMapper.map_to_dict(singing_policies)
        inserted = self.get_collection().insert_many(singing_policies_map)
        self._logger.debug('Inserted items for transaction: %s', inserted.inserted_ids)
        return singing_policies

    def fetch_policy_matching(self, match: str) -> List[SigningPolicy]:
        query = {
            "path": {
                    "$regex": f"/{match}/",
                    "$options": "g"
                }
        }
        result = self.get_collection().find(
            query, {'_id': False}
        )
        return SigningPolicyMapper.map_from_dict(result)


class IndexDao(Dao):
    _collection_name = 'index'


class PanelDao(Dao):
    _collection_name = 'catalogue'


class SeasonDao(Dao):
    _collection_name = 'season'


class SeriesDao(Dao):
    _collection_name = 'series'


class MovieDao(Dao):
    _collection_name = 'movie'


class EpisodeDao(Dao):
    _collection_name = 'episode'
