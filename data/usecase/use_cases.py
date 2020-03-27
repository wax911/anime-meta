from typing import List

from domain.entity import SigningPolicy
from domain.usecase import CommonUseCase
from domain.model import LoginQuery


class AuthenticationUseCase(CommonUseCase):
    """
    User and system authentication use case
    """

    def login(self, credentials: LoginQuery) -> None:
        pass

    async def signing_policies(self) -> List[SigningPolicy]:
        return await self._repository.signing_policies()


class IndexUseCase(CommonUseCase):
    """

    """

    async def index_panel(self, service: str):
        return await self._repository.index_panel(service)


class PanelUseCase(CommonUseCase):
    """

    """
    pass


class SeasonsUseCase(CommonUseCase):
    """

    """
    pass


class SeriesUseCase(CommonUseCase):
    """

    """
    pass


class MovieUseCase(CommonUseCase):
    """

    """
    pass


class EpisodesUseCase(CommonUseCase):
    """

    """
    pass


class MovieEpisodesUseCase(CommonUseCase):
    """

    """
    pass
