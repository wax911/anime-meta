from logging import Logger

from app.usecase import ServiceInteractor
from data import DatabaseUtil, LoggingUtil
from domain.model import Parameters

from di import UtilityClientScopeProvider


class Main:
    """ Main application control center """
    __logging_client: LoggingUtil = UtilityClientScopeProvider.logging_client()
    __logger: Logger = __logging_client.get_default_logger(__name__)
    __database_client: DatabaseUtil = UtilityClientScopeProvider.database_client()

    def __init__(self, parameters: Parameters) -> None:
        self.__parameters = parameters

    def start(self) -> None:
        """
        Application starting point, check parameters and stars the application service
        :return:
        """
        try:
            ServiceInteractor(
                self.__parameters,
                self.__logging_client
            ).start_service()
        except Exception as error:
            self.__logger.error(
                f'Unhandled exception thrown from service: `{self.__parameters.service}`',
                exc_info=error
            )
        finally:
            self.__logger.info("Attempting to close database connection..")
            self.__database_client.disconnect()
