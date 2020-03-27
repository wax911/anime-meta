from asyncio import run

from app.contract import CoreInteractor
from data.usecase import IndexUseCase
from di import UseCaseProvider


class ServiceInteractor(CoreInteractor):

    async def __create_index(self):
        index_use_case: IndexUseCase = UseCaseProvider.index_use_case()
        result = await index_use_case.index_panel(self._parameters.service)
        self._logger.info("")

    async def __on_start(self):
        await self.__create_index()

    def start_service(self):
        run(self.__on_start())
