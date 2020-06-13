from typing import Iterable

from data.repository import AuthenticationRepository, IndexRepository, PanelRepository, SeasonRepository, \
    SeriesRepository, MovieRepository, EpisodeRepository
from domain.entity import Index, Panel, Season, Series
from domain.usecase import CommonUseCase
from domain.model import LoginQuery


class AuthenticationUseCase(CommonUseCase):
    """
    User and system authentication use case
    """
    _repository: AuthenticationRepository

    def login(self, credentials: LoginQuery) -> None:
        pass


class IndexUseCase(CommonUseCase):
    """
    Indexed use case of available items on a given service
    """
    _repository: IndexRepository

    async def index_panel(self, service: str) -> Iterable[Index]:
        return await self._repository.index(service)


class PanelUseCase(CommonUseCase):
    """
    Panel use case of all indexed items
    """
    _repository: PanelRepository

    async def panels(self, service: str, index_collection: Iterable[Index]) -> Iterable[Panel]:
        for index in index_collection:
            self._logger.info(f'Searching for collection panel using: {index}')
            await self._repository.panel(service, index)
        return await self._repository.all_panels()


class SeasonUseCase(CommonUseCase):
    """
    Season use case for a given series
    """
    _repository: SeasonRepository

    async def seasons(self, series_collection: Iterable[Series]) -> Iterable[Season]:
        for item in series_collection:
            self._logger.info(f'Searching seasons for series: {item.id} -> {item.title}')
            await self._repository.seasons(item)
        return await self._repository.all_seasons()


class SeriesUseCase(CommonUseCase):
    """
    Series use case for a panel
    """
    _repository: SeriesRepository

    @staticmethod
    def __filter_only_series_types(panel_collection: Iterable[Panel]) -> Iterable[Panel]:
        return filter(
            lambda panel: panel.type == 'series',
            panel_collection
        )

    async def series(self, panel_collection: Iterable[Panel]) -> Iterable[Series]:
        panels = self.__filter_only_series_types(panel_collection)
        for item in panels:
            self._logger.info(f'Searching series for using: {item}')
            await self._repository.series(item)
        return await self._repository.all_series()


class MovieUseCase(CommonUseCase):
    """
    Movie use case for a panel
    """
    _repository: MovieRepository

    @staticmethod
    def __filter_only_movie_types(panel_collection: Iterable[Panel]) -> Iterable[Panel]:
        return filter(
            lambda panel: panel.type == 'movie_listing',
            panel_collection
        )

    async def movies(self, panel_collection: Iterable[Panel]) -> None:
        panels = self.__filter_only_movie_types(panel_collection)
        for item in panels:
            self._logger.info(f'Searching for movie using: {item}')
            await self._repository.movie(item)


class EpisodeUseCase(CommonUseCase):
    """
    Episode use case for given season
    """
    _repository: EpisodeRepository

    async def episodes(self, season_collection: Iterable[Season]) -> None:
        for item in season_collection:
            self._logger.info(f'Searching for episodes for season {item.season_number}: {item.series_id}')
            await self._repository.episode(item)
