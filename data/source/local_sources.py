from logging import Logger
from typing import List, Dict, Optional, MutableMapping

from bson import CodecOptions
from bson.codec_options import TypeRegistry
from mongo_thingy import Thingy
from mongo_thingy.cursor import Cursor
from pymongo import MongoClient, ReplaceOne, InsertOne
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConfigurationError
from pymongo.results import BulkWriteResult, DeleteResult, UpdateResult

from data import TimeUtil, LoggingUtil, DatabaseUtil
from data.entity import CacheLogEntity, SigningPolicyEntity, IndexEntity, Entity, PanelEntity, SeasonEntity, \
    EpisodeEntity, MovieEntity, SeriesEntity
from data.mapper import SigningPolicyMapper, IndexMapper, EpisodeMapper, MovieMapper, SeriesMapper, \
    SeasonMapper, PanelMapper
from data.model import IndexModel, SigningPolicyModel, PanelModel, SeasonModel, SeriesModel, MovieModel, EpisodeModel, \
    AttributeDict
from data.type_registry import CoreEntityCodec, PanelEntityCodec, SeriesEntityCodec, SeasonEntityCodec, \
    MovieEntityCodec, EpisodeEntityCodec


class Dao(Thingy):
    """ Database access object contract """
    __DEFAULT_PROJECTION__: Dict = {'_id': False}

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: List[CoreEntityCodec]
    ) -> None:
        super().__init__()
        self._logger = logger_client.get_default_logger(__name__)
        self._timezone_client = timezone_client
        self._type_codecs = type_codecs
        self.__start_database(database_client, self._logger)

    @classmethod
    def __start_database(cls, database_client: DatabaseUtil, logger: Logger):
        __connection_uri = database_client.create_connection_string()
        cls._client: MongoClient = MongoClient(
            host=__connection_uri,
            maxIdleTimeMS=45_000,
            appname='anime-meta'
        )
        try:
            cls._database = cls._client.get_database()
        except ConfigurationError as e:
            logger.debug(
                f'Configuration error prevented database from connecting: {__connection_uri}',
                exc_info=e
            )

    @classmethod
    def close_database(cls, logger: Logger):
        try:
            cls.client.close()
            cls._client = None
            cls._database = None
        except Exception as e:
            logger.info(msg='Unable to disconnect from database', exc_info=e)

    def _get_current_timestamp(self) -> int:
        return self._timezone_client.get_current_timestamp()

    @staticmethod
    def _map_to_replace_query(entity: Entity) -> ReplaceOne:
        """
        Builds a replacement object for a given entity
        :param entity: The entity to replace with
        :return: A replace one operation
        """
        pass

    @classmethod
    def get_collection_name(cls) -> str:
        return cls._collection_name

    @classmethod
    def get_collection(cls) -> Collection:
        """
        Provide a collection without any codec options
        :return: Collection for the current database connection
        """
        db: Database = cls.get_database()
        return db.get_collection(
            name=cls._collection_name
        )
        # return super().get_collection()

    @classmethod
    def get_db_collection(
            cls,
            type_codecs: [CoreEntityCodec],
            document_class: MutableMapping = AttributeDict
    ):
        """
        Provide a collection with codec options
        :return: Collection for the current database connection
        """
        db: Database = cls.get_database()
        codec_options = CodecOptions(
            document_class=document_class,
            type_registry=TypeRegistry(type_codecs)
        )
        return db.get_collection(
            name=cls._collection_name,
            codec_options=codec_options
        )


class CacheLogDao(Dao):
    _collection_name = 'cache'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)

    @staticmethod
    def __create_filter(cache_log: CacheLogEntity) -> Dict:
        if cache_log.item_id is not None:
            return {
                'collection': cache_log.collection,
                'item_id': cache_log.item_id
            }
        else:
            return {
                'collection': cache_log.collection
            }

    def save_or_update_cache_entry(self, cache_log: CacheLogEntity) -> UpdateResult:
        update_filter = self.__create_filter(cache_log)
        result: UpdateResult = self.get_db_collection(
            type_codecs=self._type_codecs
        ).update_one(
            filter=update_filter,
            update={
                '$set': cache_log
            },
            upsert=True
        )
        self._logger.debug(
            f'Cache update result -> updated or inserted: {result.upserted_id}'
        )
        return result

    def get_cache_log_entry(self, search_filter: Dict) -> Optional[CacheLogEntity]:
        entity: Optional[CacheLogEntity] = self.get_db_collection(
            type_codecs=self._type_codecs
        ).find_one(
            filter=search_filter,
            projection=self.__DEFAULT_PROJECTION__
        )
        return entity


class AuthenticationDao(Dao):
    _collection_name = 'authentication'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: SigningPolicyMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    def __assure_only_valid_sessions_exist(self) -> None:
        query = {
            'expires': {
                '$lt': self._get_current_timestamp()
            }
        }
        delete_result: DeleteResult = self.get_db_collection(
            type_codecs=self._type_codecs
        ).delete_many(filter=query)
        deleted_count = delete_result.deleted_count
        if deleted_count > 0:
            self._logger.info(
                f'Invalidated database items with query: {query} and returned result: {deleted_count}'
            )

    def contains_valid_sessions(self, path_type: str) -> bool:
        query = {
            'expires': {
                '$gt': self._get_current_timestamp()
            },
            'path': {
                '$regex': f'/{path_type}/',
                '$options': 'g'
            }
        }
        valid_session_could = self.get_db_collection(
            type_codecs=self._type_codecs
        ).count_documents(query)
        self._logger.debug(f'Query results for query: {query} returned `{valid_session_could}` results')
        return valid_session_could > 0

    @staticmethod
    def _map_to_replace_query(entity: SigningPolicyEntity) -> InsertOne:
        return InsertOne(
            document=dict(entity)
        )

    def __add_items(self, entities: List[SigningPolicyEntity]) -> List[InsertOne]:
        replacements = map(self._map_to_replace_query, entities)
        return list(replacements)

    def save_or_update(self, response: Dict) -> BulkWriteResult:
        self.__assure_only_valid_sessions_exist()
        model: List[SigningPolicyModel] = self.mapper.to_model(response)
        entities: List[SigningPolicyEntity] = self.mapper.to_entity(model)
        replacement_items = self.__add_items(entities)
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_policy_matching(self, path_type: str) -> List[SigningPolicyEntity]:
        query = {
            'path': {
                '$regex': f'/{path_type}/',
                '$options': 'g'
            }
        }
        cursor = self.get_db_collection(
            type_codecs=self._type_codecs
        ).find(
            filter=query, projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)


class IndexDao(Dao):
    _collection_name = 'index'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: IndexMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    @staticmethod
    def _map_to_replace_query(entity: IndexEntity) -> ReplaceOne:
        return ReplaceOne(
            filter={
                'prefix': entity.prefix
            },
            replacement=dict(entity),
            upsert=True
        )

    def __replace_items(self, entities: List[IndexEntity]) -> List[ReplaceOne]:
        replacements = map(self._map_to_replace_query, entities)
        return list(replacements)

    def save_or_update(self, response: Dict) -> BulkWriteResult:
        models: List[IndexModel] = self.mapper.to_model(response)
        entities: List[IndexEntity] = self.mapper.to_entity(models)
        replacement_items = self.__replace_items(entities)
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_index_list(self) -> List[IndexEntity]:
        cursor: Cursor = self.get_db_collection(
            type_codecs=self._type_codecs
        ).find(
            projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)


class PanelDao(Dao):
    _collection_name = 'catalogue'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: PanelMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    @staticmethod
    def _map_to_replace_query(entity: PanelEntity) -> ReplaceOne:
        return ReplaceOne(
            filter={
                'id': entity.id
            },
            replacement=dict(entity),
            upsert=True
        )

    def __replace_items(self, entities: List[PanelEntity]) -> List[ReplaceOne]:
        replacements = map(self._map_to_replace_query, entities)
        return list(replacements)

    def save_or_update(self, response: Dict) -> BulkWriteResult:
        models: List[PanelModel] = self.mapper.to_model(response)
        entities: List[PanelEntity] = self.mapper.to_entity(models)
        replacement_items = self.__replace_items(entities)
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_catalogue_list(self) -> List[PanelEntity]:
        cursor: Cursor = self.get_db_collection(
            type_codecs=self._type_codecs + [PanelEntityCodec()]
        ).find(
            projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)


class SeasonDao(Dao):
    _collection_name = 'season'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: SeasonMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    @staticmethod
    def _map_to_replace_query(entity: SeasonEntity) -> ReplaceOne:
        return ReplaceOne(
            filter={
                'id': entity.id
            },
            replacement=dict(entity),
            upsert=True
        )

    def __replace_items(self, entities: List[SeasonEntity]) -> List[ReplaceOne]:
        replacements = map(self._map_to_replace_query, entities)
        return list(replacements)

    def save_or_update(self, response: Dict) -> BulkWriteResult:
        models: List[SeasonModel] = self.mapper.to_model(response)
        entities: List[SeasonEntity] = self.mapper.to_entity(models)
        replacement_items = self.__replace_items(entities)
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_season_list(self) -> List[SeasonEntity]:
        cursor: Cursor = self.get_db_collection(
            type_codecs=self._type_codecs + [SeasonEntityCodec()]
        ).find(
            projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)


class SeriesDao(Dao):
    _collection_name = 'series'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: SeriesMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    @staticmethod
    def _map_to_replace_query(entity: SeriesEntity) -> ReplaceOne:
        return ReplaceOne(
            filter={
                'id': entity.id
            },
            replacement=dict(entity),
            upsert=True
        )

    def save_or_update(self, response: SeriesModel) -> BulkWriteResult:
        entity = self.mapper.to_entity(response)
        replacement_items = [self._map_to_replace_query(entity)]
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_series_list(self) -> List[SeriesEntity]:
        cursor: Cursor = self.get_db_collection(
            type_codecs=self._type_codecs + [SeriesEntityCodec()]
        ).find(
            projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)


class MovieDao(Dao):
    _collection_name = 'movie'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: MovieMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    @staticmethod
    def _map_to_replace_query(entity: MovieEntity) -> ReplaceOne:
        return ReplaceOne(
            filter={
                'id': entity.id
            },
            replacement=dict(entity),
            upsert=True
        )

    def save_or_update(self, response: MovieModel) -> BulkWriteResult:
        entity: MovieEntity = self.mapper.to_entity(response)
        replacement_items = [self._map_to_replace_query(entity)]
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_movie_list(self) -> List[MovieEntity]:
        cursor: Cursor = self.get_db_collection(
            type_codecs=self._type_codecs + [MovieEntityCodec()]
        ).find(
            projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)


class EpisodeDao(Dao):
    _collection_name = 'episode'

    def __init__(
            self,
            logger_client: LoggingUtil,
            timezone_client: TimeUtil,
            database_client: DatabaseUtil,
            type_codecs: CoreEntityCodec,
            mapper: EpisodeMapper
    ) -> None:
        super().__init__(logger_client, timezone_client, database_client, type_codecs)
        self.mapper = mapper

    @staticmethod
    def _map_to_replace_query(entity: EpisodeEntity) -> ReplaceOne:
        return ReplaceOne(
            filter={
                'id': entity.id
            },
            replacement=dict(entity),
            upsert=True
        )

    def __replace_items(self, entities: List[EpisodeEntity]) -> List[ReplaceOne]:
        replacements = map(self._map_to_replace_query, entities)
        return list(replacements)

    def save_or_update(self, response: Dict) -> BulkWriteResult:
        models: List[EpisodeModel] = self.mapper.to_model(response)
        entities: List[EpisodeEntity] = self.mapper.to_entity(models)
        replacement_items = self.__replace_items(entities)
        try:
            bulk_write_result: BulkWriteResult = self.get_db_collection(
                type_codecs=self._type_codecs
            ).bulk_write(replacement_items)
            self._logger.info(
                f'{self._collection_name} bulk write results -> updated or inserted: {bulk_write_result.upserted_ids}'
            )
            return bulk_write_result
        except Exception as e:
            self._logger.warning(
                f'Unable to persist to collection: {self._collection_name} -> {replacement_items}', e
            )

    def fetch_episode_list(self) -> List[EpisodeEntity]:
        cursor: Cursor = self.get_db_collection(
            type_codecs=self._type_codecs + [EpisodeEntityCodec()]
        ).find(
            projection=self.__DEFAULT_PROJECTION__
        )
        return list(cursor)
