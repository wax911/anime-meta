from asyncio import run

from app.contract import CoreInteractor


class ServiceInteractor(CoreInteractor):

    async def __start_discovery(self):
        self._logger.info(f'Fetching index for service: {self._parameters.service}')
        index = await self._index_use_case.index_panel(self._parameters.service)
        self._logger.info(f'Fetching panels for index')
        panels = await self._panel_use_case.panels(self._parameters.service, index)
        self._logger.info(f'Fetching series for panels')
        series = await self._series_use_case.series(panels)
        self._logger.info(f'Fetching seasons for series')
        seasons = await self._season_use_case.seasons(series)
        self._logger.info(f'Fetching movies for panels')
        await self._movie_use_case.movies(panels)
        self._logger.info(f'Fetching episodes for seasons')
        await self._episode_use_case.episodes(seasons)

    async def __on_start(self):
        self._logger.info('Starting discovery task..')
        await self.__start_discovery()

    def start_service(self):
        self._logger.info('Starting service coroutine..')
        run(self.__on_start())
