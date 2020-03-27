import dependency_injector.containers as containers
import dependency_injector.providers as providers

from data import NetworkUtil, DatabaseUtil, LoggingUtil, TimeUtil
from data.source import AuthenticationEndpoint, DiscoverEndpoint, CollectionEndpoint
from data.source.local_sources import IndexDao, PanelDao, SeriesDao, SeasonDao, EpisodeDao, MovieDao, AuthenticationDao

from data.repository import AuthenticationRepository, EpisodesRepository, IndexRepository, \
    MovieEpisodesRepository, MovieRepository, PanelRepository, SeasonsRepository, SeriesRepository

from data.usecase import AuthenticationUseCase, EpisodesUseCase, IndexUseCase, MovieEpisodesUseCase, \
    MovieUseCase, PanelUseCase, SeasonsUseCase, SeriesUseCase


class UtilityClientScopeProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""

    database_client = providers.Singleton(DatabaseUtil)
    time_zone_client = providers.Singleton(TimeUtil)
    logging_client = providers.Singleton(LoggingUtil)
    network_client = providers.Singleton(NetworkUtil)


class LocalSourceProvider:
    """Container of local sources providers."""

    auth_collection = providers.Singleton(
        AuthenticationDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )
    index_collection = providers.Singleton(
        IndexDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )
    panel_collection = providers.Singleton(
        PanelDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )
    series_collection = providers.Singleton(
        SeriesDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )
    season_collection = providers.Singleton(
        SeasonDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )
    episode_collection = providers.Singleton(
        EpisodeDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )
    movie_collection = providers.Singleton(
        MovieDao,
        logger_client=UtilityClientScopeProvider.logging_client(),
        timezone_client=UtilityClientScopeProvider.time_zone_client(),
        database_client=UtilityClientScopeProvider.database_client()
    )


class RemoteSourceProvider(containers.DeclarativeContainer):
    """IoC container of remote sources providers."""
    __session_client = UtilityClientScopeProvider.network_client().create_session()

    authentication_endpoint = providers.Singleton(
        AuthenticationEndpoint,
        base_url=NetworkUtil.get_authentication_url(),
        client=__session_client
    )
    discover_endpoint = providers.Singleton(
        DiscoverEndpoint,
        base_url=NetworkUtil.get_discover_url(),
        client=__session_client
    )
    collection_endpoint = providers.Singleton(
        CollectionEndpoint,
        base_url=NetworkUtil.get_collection_url(),
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
        EpisodesRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.episode_collection()
    )
    index_repository = providers.Factory(
        IndexRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.discover_endpoint,
        local_source=LocalSourceProvider.index_collection(),
        authentication_repository=authentication_repository()
    )
    movie_episodes_repository = providers.Factory(
        MovieEpisodesRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.episode_collection()
    )
    movie_repository = providers.Factory(
        MovieRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.movie_collection()
    )
    panel_repository = providers.Factory(
        PanelRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.discover_endpoint,
        local_source=LocalSourceProvider.panel_collection()
    )
    seasons_repository = providers.Factory(
        SeasonsRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.season_collection()
    )
    series_repository = providers.Factory(
        SeriesRepository,
        logging_client=UtilityClientScopeProvider.logging_client(),
        remote_source=RemoteSourceProvider.collection_endpoint,
        local_source=LocalSourceProvider.series_collection()
    )


class UseCaseProvider(containers.DeclarativeContainer):
    """IoC container of repository providers."""

    authentication_use_case = providers.Factory(
        AuthenticationUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.authentication_repository
    )
    episodes_use_case = providers.Factory(
        EpisodesUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.episodes_repository
    )
    index_use_case = providers.Factory(
        IndexUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.index_repository
    )
    movie_episodes_use_case = providers.Factory(
        MovieEpisodesUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.movie_episodes_repository
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
        SeasonsUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.seasons_repository
    )
    series_use_case = providers.Factory(
        SeriesUseCase,
        logging_client=UtilityClientScopeProvider.logging_client(),
        repository=RepositoryProvider.series_repository
    )
