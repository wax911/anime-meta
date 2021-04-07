import dependency_injector.containers as containers
import dependency_injector.providers as providers

from data import NetworkUtil, DatabaseUtil, LoggingUtil, TimeUtil
from data.mapper import SigningPolicyMapper, IndexMapper, PanelMapper, SeasonMapper, \
    SeriesMapper, MovieMapper, EpisodeMapper
from data.source import AuthenticationEndpoint, DiscoverEndpoint, CollectionEndpoint, DetailEndpoint
from data.source.local_sources import IndexDao, PanelDao, SeriesDao, SeasonDao, EpisodeDao, \
    MovieDao, AuthenticationDao, CacheLogDao

from data.repository import AuthenticationRepository, EpisodeRepository, IndexRepository, \
    MovieRepository, PanelRepository, SeasonRepository, SeriesRepository
from data.type_registry import CacheLogEntityCodec, SigningPolicyEntityCodec, IndexEntityCodec, PanelEntityCodec, \
    SeasonEntityCodec, SeriesEntityCodec, EpisodeEntityCodec, MovieEntityCodec, ImageEntityCodec, \
    ImageContainerEntityCodec, SearchMetaEntityCodec, AdBreakEntityCodec, SeriesPanelEntityCodec, MoviePanelEntityCodec

from data.usecase import AuthenticationUseCase, EpisodeUseCase, IndexUseCase, \
    MovieUseCase, PanelUseCase, SeasonUseCase, SeriesUseCase

from data.source import CacheLogUtil


class UtilityClientScopeProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""

    database_client = providers.Singleton(DatabaseUtil)
    time_zone_client = providers.Singleton(TimeUtil)
    logging_client = providers.Singleton(LoggingUtil)
    network_client = providers.Singleton(NetworkUtil)


class MapperScopeProvider(containers.DeclarativeContainer):
    """IoC container of mapper providers."""
    singing_policy_mapper = providers.Factory(
        SigningPolicyMapper,
        logging_client=UtilityClientScopeProvider.logging_client(),
        time_zone_client=UtilityClientScopeProvider.time_zone_client()
    )
    index_mapper = providers.Factory(
        IndexMapper,
        logging_client=UtilityClientScopeProvider.logging_client()
    )
    panel_mapper = providers.Factory(
        PanelMapper,
        logging_client=UtilityClientScopeProvider.logging_client()
    )
    seasons_mapper = providers.Factory(
        SeasonMapper,
        logging_client=UtilityClientScopeProvider.logging_client()
    )
    series_mapper = providers.Factory(
        SeriesMapper,
        logging_client=UtilityClientScopeProvider.logging_client()
    )
    movies_mapper = providers.Factory(
        MovieMapper,
        logging_client=UtilityClientScopeProvider.logging_client()
    )
    episodes_mapper = providers.Factory(
        EpisodeMapper,
        logging_client=UtilityClientScopeProvider.logging_client()
    )


class LocalSourceProvider:
    """Container of local sources providers."""

    cache_collection = providers.Singleton(
        CacheLogDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            CacheLogEntityCodec()
        ]
    )
    auth_collection = providers.Singleton(
        AuthenticationDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            SigningPolicyEntityCodec()
        ],
        mapper=MapperScopeProvider.singing_policy_mapper()
    )
    index_collection = providers.Singleton(
        IndexDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            IndexEntityCodec()
        ],
        mapper=MapperScopeProvider.index_mapper()
    )
    panel_collection = providers.Singleton(
        PanelDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            ImageContainerEntityCodec(),
            ImageEntityCodec(),
            MoviePanelEntityCodec(),
            SeriesPanelEntityCodec(),
            SearchMetaEntityCodec()
        ],
        mapper=MapperScopeProvider.panel_mapper()
    )
    series_collection = providers.Singleton(
        SeriesDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            ImageContainerEntityCodec(),
            ImageEntityCodec()
        ],
        mapper=MapperScopeProvider.series_mapper()
    )
    season_collection = providers.Singleton(
        SeasonDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            ImageContainerEntityCodec(),
            ImageEntityCodec()
        ],
        mapper=MapperScopeProvider.seasons_mapper()
    )
    episode_collection = providers.Singleton(
        EpisodeDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            ImageContainerEntityCodec(),
            ImageEntityCodec(),
            AdBreakEntityCodec()
        ],
        mapper=MapperScopeProvider.episodes_mapper()
    )
    movie_collection = providers.Singleton(
        MovieDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client(),
        type_codecs=[
            ImageContainerEntityCodec(),
            ImageEntityCodec()
        ],
        mapper=MapperScopeProvider.movies_mapper()
    )


class SourceUtilityProvider(containers.DeclarativeContainer):
    """IoC container for cache utility"""

    cache_client = providers.Factory(
        CacheLogUtil,
        local_source=LocalSourceProvider.cache_collection(),
        logging_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client()
    )


class RemoteSourceProvider(containers.DeclarativeContainer):
    """IoC container of remote sources providers."""
    __network_client = UtilityClientScopeProvider.network_client()
    __session_client = __network_client.create_session()

    authentication_endpoint = providers.Singleton(
        AuthenticationEndpoint,
        base_url=__network_client.get_authentication_url(),
        client=__session_client
    )
    discover_endpoint = providers.Singleton(
        DiscoverEndpoint,
        base_url=__network_client.get_discover_url(),
        client=__session_client
    )
    collection_endpoint = providers.Singleton(
        CollectionEndpoint,
        base_url=__network_client.get_collection_url(),
        client=__session_client
    )
    detail_endpoint = providers.Singleton(
        DetailEndpoint,
        base_url=__network_client.get_collection_url(),
        client=__session_client
    )


class RepositoryProvider(containers.DeclarativeContainer):
    """IoC container of repository providers."""

    authentication_repository = providers.Factory(
        AuthenticationRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.authentication_endpoint,
        local_source=LocalSourceProvider.auth_collection()
    )
    episodes_repository = providers.Factory(
        EpisodeRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.episode_collection(),
        cache_log_client=SourceUtilityProvider.cache_client,
        authentication_repository=authentication_repository()
    )
    index_repository = providers.Factory(
        IndexRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.discover_endpoint,
        local_source=LocalSourceProvider.index_collection(),
        cache_log_client=SourceUtilityProvider.cache_client,
        authentication_repository=authentication_repository()
    )
    movie_repository = providers.Factory(
        MovieRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.detail_endpoint,
        local_source=LocalSourceProvider.movie_collection(),
        cache_log_client=SourceUtilityProvider.cache_client,
        authentication_repository=authentication_repository()
    )
    panel_repository = providers.Factory(
        PanelRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.discover_endpoint,
        local_source=LocalSourceProvider.panel_collection(),
        cache_log_client=SourceUtilityProvider.cache_client,
        authentication_repository=authentication_repository()
    )
    seasons_repository = providers.Factory(
        SeasonRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.season_collection(),
        cache_log_client=SourceUtilityProvider.cache_client,
        authentication_repository=authentication_repository()
    )
    series_repository = providers.Factory(
        SeriesRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.detail_endpoint,
        local_source=LocalSourceProvider.series_collection(),
        cache_log_client=SourceUtilityProvider.cache_client,
        authentication_repository=authentication_repository()
    )


class UseCaseProvider(containers.DeclarativeContainer):
    """IoC container of repository providers."""

    authentication_use_case = providers.Factory(
        AuthenticationUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.authentication_repository
    )
    episodes_use_case = providers.Factory(
        EpisodeUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.episodes_repository
    )
    index_use_case = providers.Factory(
        IndexUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.index_repository
    )
    movie_use_case = providers.Factory(
        MovieUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.movie_repository
    )
    panel_use_case = providers.Factory(
        PanelUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.panel_repository
    )
    seasons_use_case = providers.Factory(
        SeasonUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.seasons_repository
    )
    series_use_case = providers.Factory(
        SeriesUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.series_repository
    )
