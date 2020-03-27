from abc import ABC

from data import LoggingUtil
from domain.model import Parameters


class CorePresenter(ABC):

    def __init__(self) -> None:
        super().__init__()


class CoreInteractor(ABC):

    def __init__(self, parameters: Parameters, __logging_client: LoggingUtil) -> None:
        self._parameters = parameters
        self._logger = __logging_client.get_default_logger(__name__)
