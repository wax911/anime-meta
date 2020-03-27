from typing import List, Any

from domain.entity import SigningPolicy
from domain.model import LoginQuery
from domain.repository import CommonRepository
from .. import LoggingUtil
from ..source import AuthenticationEndpoint, AuthenticationDao, DiscoverEndpoint, IndexDao


class AuthenticationRepository(CommonRepository):
    """

    """

    def __init__(
            self,
            remote_source: AuthenticationEndpoint,
            local_source: AuthenticationDao,
            logging_client: LoggingUtil,
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)

    async def signing_policies(self) -> List[SigningPolicy]:
        if not self._local_source.contains_valid_sessions():
            response = self._remote_source.get_authorization_token()
            signing_policies = self._local_source.save_new_policy(response)
            return signing_policies

        self._logger.info("Skipping CMS authentication")
        return self._local_source.fetch_policy_matching('public')

    async def login(self, credentials: LoginQuery):
        pass


class IndexRepository(CommonRepository):
    """

    """

    def __init__(
            self,
            remote_source: DiscoverEndpoint,
            local_source: IndexDao,
            logging_client: LoggingUtil,
            authentication_repository: AuthenticationRepository
    ) -> None:
        super().__init__(remote_source, local_source, logging_client)
        self._authentication = authentication_repository

    async def index_panel(self, service: str) -> Any:
        signing_policies = await self._authentication.signing_policies()
        response = self._remote_source.get_index(
            service=service,
            policy=signing_policies[0].value,
            signature=signing_policies[1].value,
            key_pair=signing_policies[2].value
        )
        self._logger.debug("Index collection: %s", response)


class PanelRepository(CommonRepository):
    """

    """

    async def get(self) -> Any:
        pass


class SeasonsRepository(CommonRepository):
    """

    """

    async def get(self) -> Any:
        pass


class SeriesRepository(CommonRepository):
    """

    """

    async def get(self) -> Any:
        pass


class MovieRepository(CommonRepository):
    """

    """

    async def get(self) -> Any:
        pass


class EpisodesRepository(CommonRepository):
    """

    """

    async def get(self) -> Any:
        pass


class MovieEpisodesRepository(CommonRepository):
    """

    """

    async def get(self) -> Any:
        pass
