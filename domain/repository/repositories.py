from mongo_thingy import Thingy
from uplink import Consumer
from abc import ABC, abstractmethod

from data import LoggingUtil


class CommonRepository(ABC):
    """
    Abstract repository
    """

    def __init__(self, remote_source: Consumer, local_source: Thingy, logging_client: LoggingUtil) -> None:
        """

        :param remote_source: consumer for remote api
        :param local_source:
        :param logging_client:
        """
        self._remote_source = remote_source
        self._local_source = local_source
        self._logger = logging_client.get_default_logger(__name__)
