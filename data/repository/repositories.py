from json import JSONDecodeError
from typing import List, Optional, Dict, Iterable

from mongo_thingy import Thingy
from uplink import Consumer

from domain.entity import Index, Panel, Season, Series, Movie, Episode, Item
from domain.model import LoginQuery
from domain.repository import CommonRepository
from .. import LoggingUtil
from ..entity import SigningPolicyEntity, PanelEntity, Entity, IndexEntity, MovieEntity, SeriesEntity, SeasonEntity, \
    EpisodeEntity
from ..model import MovieModel, SeriesModel
from ..source import AuthenticationEndpoint, AuthenticationDao, DiscoverEndpoint, IndexDao, CacheLogUtil, PanelDao, \
    SeasonDao, SeriesDao, MovieDao, EpisodeDao, CollectionEndpoint


class IRepository(CommonRepository):

    @staticmethod
    def _from_entity(entities: List[Entity]) -> Iterable[Item]:
        """
        Convert data entities to domain entities
        :param entities:
        :return: Iterable of domain entries
        """
        pass


class AuthenticationRepository(IRepository):
    _remote_source: AuthenticationEndpoint
    _local_source: AuthenticationDao

    def __make_request(self) -> Optional[Dict]:
        try:
            return self._remote_source.get_authorization_token()
        except JSONDecodeError as e:
            self._logger.error(f"Failed to authenticate: {e.doc}", exc_info=e)
            return None

    async def signing_policies(self, path_type: str = 'cms') -> List[SigningPolicyEntity]:
        if not self._local_source.contains_valid_sessions(path_type):
            response = self.__make_request()
            result = self._local_source.save_or_update(response)

        self._logger.debug("Skipping singing policy authentication")
        return self._local_source.fetch_policy_matching(path_type)

    async def login(self, credentials: LoginQuery):
        pass


class IndexRepository(IRepository):
    _remote_source: DiscoverEndpoint
    _local_source: IndexDao

    def __init__(
            self,
            remote_source: Consumer,
            local_source: Thingy,
            logging_client: LoggingUtil,
            cache_log_client: CacheLogUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._cache_log_client = cache_log_client
        self._authentication = authentication_repository

    def __make_request(
            self,
            service: str,
            signing_policies: List[SigningPolicyEntity]
    ) -> Optional[Dict]:
        try:
            return self._remote_source.get_index(
                channel_id=service,
                policy=signing_policies[0].value,
                signature=signing_policies[1].value,
                key_pair=signing_policies[2].value
            )
        except JSONDecodeError as e:
            self._logger.error(f"Failed to request signing  policies: {e.doc}", exc_info=e)
            return None

    @staticmethod
    def _from_entity(entities: List[IndexEntity]) -> Iterable[Index]:
        def map_to(entity: IndexEntity) -> Index:
            return Index(
                prefix=entity.prefix,
                offset=entity.offset,
                count=entity.count
            )

        return map(map_to, entities)

    async def index(self, service: str) -> Iterable[Index]:
        key = self._local_source.get_collection_name()
        if self._cache_log_client.is_cache_expired(key):
            signing_policies = await self._authentication.signing_policies('public')
            response = self.__make_request(service, signing_policies)
            result = self._local_source.save_or_update(response)
            self._cache_log_client.save_or_update(key)
        index = self._local_source.fetch_index_list()
        self._logger.debug("Index collection: %s", len(index))
        return self._from_entity(index)


class PanelRepository(IRepository):
    _remote_source: DiscoverEndpoint
    _local_source: PanelDao

    def __init__(
            self,
            remote_source: Consumer,
            local_source: Thingy,
            logging_client: LoggingUtil,
            cache_log_client: CacheLogUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._cache_log_client = cache_log_client
        self._authentication = authentication_repository

    def __make_request(
            self,
            service: str,
            index: Index,
            signing_policies: List[SigningPolicyEntity]
    ) -> Optional[Dict]:
        try:
            return self._remote_source.get_catalogue_by_prefix(
                channel_id=service,
                sort_by='alphabetical',
                start=0,
                count=index.count,
                query=index.prefix,
                policy=signing_policies[0].value,
                signature=signing_policies[1].value,
                key_pair=signing_policies[2].value
            )
        except JSONDecodeError as e:
            self._logger.error(f"Request failed with reason: {e.doc}", exc_info=e)
            return None

    async def panel(self, service: str, index: Index) -> None:
        key = self._local_source.get_collection_name()
        if self._cache_log_client.is_cache_expired(key, index.prefix):
            signing_policies = await self._authentication.signing_policies('public')
            response = self.__make_request(service, index, signing_policies)
            result = self._local_source.save_or_update(response)
            self._cache_log_client.save_or_update(key, index.prefix)

    @staticmethod
    def _from_entity(entities: List[PanelEntity]) -> Iterable[Panel]:
        def map_to(entity: PanelEntity) -> Panel:
            return Panel(
                id=entity.id,
                channel_id=entity.channel_id,
                title=entity.title,
                external_id=entity.external_id,
                type=entity.type,
                locale=entity.locale,
                last_public=entity.last_public,
                new=entity.new
            )

        return map(map_to, entities)

    async def all_panels(self) -> Iterable[Panel]:
        catalogues = self._local_source.fetch_catalogue_list()
        self._logger.debug("Catalogue collection: %s", len(catalogues))
        return self._from_entity(catalogues)


class SeasonRepository(IRepository):
    _remote_source: CollectionEndpoint
    _local_source: SeasonDao

    def __init__(
            self,
            remote_source: Consumer,
            local_source: Thingy,
            logging_client: LoggingUtil,
            cache_log_client: CacheLogUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._cache_log_client = cache_log_client
        self._authentication = authentication_repository

    def __make_request(
            self,
            series: Series,
            signing_policies: List[SigningPolicyEntity]
    ) -> Optional[Dict]:
        try:
            return self._remote_source.get_seasons_for_series_id(
                series_id=series.id,
                policy=signing_policies[0].value,
                signature=signing_policies[1].value,
                key_pair=signing_policies[2].value
            )
        except JSONDecodeError as e:
            self._logger.error(f"Request failed with reason: {e.doc}", exc_info=e)
            return None

    async def seasons(self, series: Series) -> None:
        key = self._local_source.get_collection_name()
        if self._cache_log_client.is_cache_expired(key, series.id):
            signing_policies = await self._authentication.signing_policies()
            response = self.__make_request(series, signing_policies)
            result = self._local_source.save_or_update(response)
            self._cache_log_client.save_or_update(key, series.id)

    @staticmethod
    def _from_entity(entities: List[SeasonEntity]) -> Iterable[Season]:
        def map_to(entity: SeasonEntity) -> Season:
            return Season(
                id=entity.id,
                channel_id=entity.channel_id,
                title=entity.title,
                series_id=entity.series_id,
                season_number=entity.season_number,
                is_mature=entity.is_mature,
                is_subbed=entity.is_subbed,
                is_dubbed=entity.is_dubbed
            )

        return map(map_to, entities)

    async def all_seasons(self) -> Iterable[Season]:
        seasons = self._local_source.fetch_season_list()
        self._logger.debug("Seasons collection: %s", len(seasons))
        return self._from_entity(seasons)


class SeriesRepository(IRepository):
    _remote_source: CollectionEndpoint
    _local_source: SeriesDao

    def __init__(
            self,
            remote_source: Consumer,
            local_source: Thingy,
            logging_client: LoggingUtil,
            cache_log_client: CacheLogUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._cache_log_client = cache_log_client
        self._authentication = authentication_repository

    def __make_request(
            self,
            panel: Panel,
            signing_policies: List[SigningPolicyEntity]
    ) -> Optional[SeriesModel]:
        try:
            return self._remote_source.get_series_by_id(
                series_id=panel.id,
                policy=signing_policies[0].value,
                signature=signing_policies[1].value,
                key_pair=signing_policies[2].value
            )
        except JSONDecodeError as e:
            self._logger.error(f"Request failed with reason: {e.doc}", exc_info=e)
            return None

    async def series(self, panel: Panel) -> None:
        key = self._local_source.get_collection_name()
        if self._cache_log_client.is_cache_expired(key, panel.id):
            signing_policies = await self._authentication.signing_policies()
            response = self.__make_request(panel, signing_policies)
            result = self._local_source.save_or_update(response)
            self._cache_log_client.save_or_update(key, panel.id)

    @staticmethod
    def _from_entity(entities: List[SeriesEntity]) -> Iterable[Series]:
        def map_to(entity: SeriesEntity) -> Series:
            return Series(
                id=entity.id,
                channel_id=entity.channel_id,
                title=entity.title,
                slug=entity.slug,
                maturity_ratings=entity.maturity_ratings,
                episode_count=entity.episode_count,
                season_count=entity.season_count,
                media_count=entity.media_count,
                content_provider=entity.content_provider,
                is_mature=entity.is_mature,
                is_subbed=entity.is_subbed,
                is_dubbed=entity.is_dubbed
            )

        return map(map_to, entities)

    async def all_series(self) -> Iterable[Series]:
        series = self._local_source.fetch_series_list()
        self._logger.debug("Series collection: %s", len(series))
        return self._from_entity(series)


class MovieRepository(IRepository):
    _remote_source: CollectionEndpoint
    _local_source: MovieDao

    def __init__(
            self,
            remote_source: Consumer,
            local_source: Thingy,
            logging_client: LoggingUtil,
            cache_log_client: CacheLogUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._cache_log_client = cache_log_client
        self._authentication = authentication_repository

    def __make_request(
            self,
            panel: Panel,
            signing_policies: List[SigningPolicyEntity]
    ) -> Optional[MovieModel]:
        try:
            return self._remote_source.get_movie_by_id(
                movie_id=panel.id,
                policy=signing_policies[0].value,
                signature=signing_policies[1].value,
                key_pair=signing_policies[2].value
            )
        except JSONDecodeError as e:
            self._logger.error(f"Request failed with reason: {e.doc}", exc_info=e)
            return None

    async def movie(self, panel: Panel) -> None:
        key = self._local_source.get_collection_name()
        if self._cache_log_client.is_cache_expired(key, panel.id):
            signing_policies = await self._authentication.signing_policies()
            response = self.__make_request(panel, signing_policies)
            result = self._local_source.save_or_update(response)
            self._cache_log_client.save_or_update(key, panel.id)

    @staticmethod
    def _from_entity(entities: List[MovieEntity]) -> Iterable[Movie]:
        def map_to(entity: MovieEntity) -> Movie:
            return Movie(
                id=entity.id,
                channel_id=entity.channel_id,
                title=entity.title,
                slug=entity.slug,
                maturity_ratings=entity.maturity_ratings,
                movie_release_year=entity.movie_release_year,
                content_provider=entity.content_provider,
                is_mature=entity.is_mature,
                is_subbed=entity.is_subbed,
                is_dubbed=entity.is_dubbed
            )

        return map(map_to, entities)

    async def all_movies(self) -> Iterable[Movie]:
        movies = self._local_source.fetch_movie_list()
        self._logger.debug("Movie collection: %s", len(movies))
        return self._from_entity(movies)


class EpisodeRepository(IRepository):
    _remote_source: CollectionEndpoint
    _local_source: EpisodeDao

    def __init__(
            self,
            remote_source: Consumer,
            local_source: Thingy,
            logging_client: LoggingUtil,
            cache_log_client: CacheLogUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._cache_log_client = cache_log_client
        self._authentication = authentication_repository

    def __make_request(
            self,
            season: Season,
            signing_policies: List[SigningPolicyEntity]
    ) -> Optional[Dict]:
        try:
            return self._remote_source.get_episodes_for_season(
                season_id=season.id,
                policy=signing_policies[0].value,
                signature=signing_policies[1].value,
                key_pair=signing_policies[2].value
            )
        except JSONDecodeError as e:
            self._logger.error(f"Request failed with reason: {e.doc}", exc_info=e)
            return None

    async def episode(self, season: Season) -> None:
        key = self._local_source.get_collection_name()
        if self._cache_log_client.is_cache_expired(key, season.id):
            signing_policies = await self._authentication.signing_policies()
            response = self.__make_request(season, signing_policies)
            result = self._local_source.save_or_update(response)
            self._cache_log_client.save_or_update(key, season.id)

    @staticmethod
    def _from_entity(entities: List[EpisodeEntity]) -> Iterable[Episode]:
        def map_to(entity: EpisodeEntity) -> Episode:
            return Episode(
                id=entity.id,
                channel_id=entity.channel_id,
                title=entity.title,
                series_id=entity.series_id,
                season_id=entity.season_id,
                season_number=entity.season_number,
                episode=entity.episode,
                episode_number=entity.episode_number,
                is_mature=entity.is_mature,
                episode_air_date=entity.episode_air_date,
                is_subbed=entity.is_subbed,
                is_dubbed=entity.is_dubbed,
                media_type=entity.media_type,
                duration_ms=entity.duration_ms
            )

        return map(map_to, entities)

    async def all_episodes(self) -> Iterable[Episode]:
        episodes = self._local_source.fetch_episode_list()
        self._logger.debug("Episode collection: %s", len(episodes))
        return self._from_entity(episodes)
