from abc import ABC

from data import LoggingUtil
from data.usecase import PanelUseCase, IndexUseCase, SeriesUseCase, MovieUseCase, SeasonUseCase, EpisodeUseCase
from di import UseCaseProvider
from domain.model import Parameters


class CoreInteractor(ABC):
    _index_use_case: IndexUseCase
    _panel_use_case: PanelUseCase
    _series_use_case: SeriesUseCase
    _movie_use_case: MovieUseCase
    _season_use_case: SeasonUseCase
    _episode_use_case: EpisodeUseCase

    def __init__(self, parameters: Parameters, __logging_client: LoggingUtil) -> None:
        self._parameters = parameters
        self._index_use_case = UseCaseProvider.index_use_case()
        self._panel_use_case = UseCaseProvider.panel_use_case()
        self._series_use_case = UseCaseProvider.series_use_case()
        self._movie_use_case = UseCaseProvider.movie_use_case()
        self._season_use_case = UseCaseProvider.seasons_use_case()
        self._episode_use_case = UseCaseProvider.episodes_use_case()
        self._logger = __logging_client.get_default_logger(__name__)
