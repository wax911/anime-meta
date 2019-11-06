from mongo_thingy import Thingy
from uplink import Consumer

from core.util import EventLogHelper


class CommonRepository(object):
    """

    """

    def __init__(self, remote_source: Consumer, local_source: Thingy) -> None:
        self._remote: Consumer = remote_source
        self._local: Thingy = local_source


class AuthenticationRepository(CommonRepository):
    """

    """
    pass


class IndexRepository(CommonRepository):
    """

    """
    pass


class PanelRepository(CommonRepository):
    """

    """
    pass


class SeasonsRepository(CommonRepository):
    """

    """
    pass


class SeriesRepository(CommonRepository):
    """

    """
    pass


class MovieRepository(CommonRepository):
    """

    """
    pass


class EpisodesRepository(CommonRepository):
    """

    """
    pass


class MovieEpisodesRepository(CommonRepository):
    """

    """
    pass
