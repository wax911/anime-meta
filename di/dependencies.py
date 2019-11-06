import dependency_injector.containers as containers
import dependency_injector.providers as providers

from data import NetworkUtil, DatabaseUtil
from data.source import AuthenticationEndpoint, DiscoverEndpoint, CollectionEndpoint


class UtilityClientScopeProvider(containers.DeclarativeContainer):
    """IoC container of utilities providers."""
    database_client = providers.Singleton(DatabaseUtil)
    network_client = providers.Singleton(NetworkUtil)


class LocalSourceProvider(containers.DeclarativeContainer):
    """IoC container of local sources providers."""
    pass


class RemoteSourceProvider(containers.DeclarativeContainer):
    """IoC container of remote sources providers."""

    authentication_endpoint = providers.Singleton(
        AuthenticationEndpoint,
        base_url=NetworkUtil.get_authentication_url(),
        client=UtilityClientScopeProvider.network_client().create_session()
    )
    discover_endpoint = providers.Singleton(
        DiscoverEndpoint,
        base_url=NetworkUtil.get_discover_url(),
        client=UtilityClientScopeProvider.network_client().create_session()
    )
    collection_endpoint = providers.Singleton(
        CollectionEndpoint,
        base_url=NetworkUtil.get_collection_url(),
        client=UtilityClientScopeProvider.network_client().create_session()
    )


class RepositoryProvider(containers.DeclarativeContainer):
    """IoC container of repository providers."""
    pass


class UseCaseProvider(containers.DeclarativeContainer):
    """IoC container of repository providers."""
    pass


