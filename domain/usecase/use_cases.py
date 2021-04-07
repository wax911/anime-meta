from abc import ABC

from data import LoggingUtil
from ..repository import CommonRepository


class CommonUseCase(ABC):

    def __init__(self, repository: CommonRepository, logging_client: LoggingUtil) -> None:
        self._repository = repository
        self._logger = logging_client.get_default_logger(__name__)
