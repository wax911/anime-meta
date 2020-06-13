from typing import Optional

from data import LoggingUtil, TimeUtil
from data.entity import CacheLogEntity
from data.source import CacheLogDao


class CacheLogUtil(object):
    __DEFAULT_CACHE_DURATION: int = 60 * 60 * 24 * 2  # 2 days cache time before our next request

    def __init__(self, local_source: CacheLogDao, logging_client: LoggingUtil, timezone_client: TimeUtil) -> None:
        self._local_source = local_source
        self._timezone_client = timezone_client
        self._logger = logging_client.get_default_logger(__name__)

    def get_cache_log(self, collection: str, identifier: Optional[str] = None) -> Optional[CacheLogEntity]:
        """
        Retries a cache log using the given params
        :param collection: Collection as the key of the cache record
        :param identifier: Optional identifier for the request if it is id driven
        :return: CacheLog entry
        """
        if identifier is not None:
            search_filter = {
                'collection': collection,
                'item_id': identifier
            }
        else:
            search_filter = {
                'collection': collection
            }
        self._logger.debug(f'Searching for cache entry using filter: {search_filter}')
        return self._local_source.get_cache_log_entry(search_filter)

    def save_or_update(self, collection: str, identifier: Optional[str] = None) -> bool:
        """
        Save or update for the given parameters
        :param collection: Collection as the key of the cache record
        :param identifier: Optional identifier for the request if it is id driven
        :return: True if operation was successful, otherwise False
        """
        time_stamp = self._timezone_client.get_current_timestamp()
        self._logger.debug(f'Saving or updating cache state -> collection: `{collection}` timestamp: `{time_stamp}`')
        cache_log = CacheLogEntity(collection, time_stamp, identifier)
        result = self._local_source.save_or_update_cache_entry(cache_log)
        return result.acknowledged

    def is_cache_expired(self, collection: str, identifier: Optional[str] = None) -> bool:
        """
        State of the cache for given parameters
        :param collection: Collection as the key of the cache record
        :param identifier: Optional identifier for the request if it is id driven
        :return: True if cache has expired, otherwise False
        """
        cache_log = self.get_cache_log(collection, identifier)
        if cache_log is not None:
            cache_time = cache_log.time_stamp
            current_time = self._timezone_client.get_current_timestamp()
            difference = current_time - cache_time
            has_expired = difference > self.__DEFAULT_CACHE_DURATION
            return has_expired
        return True
