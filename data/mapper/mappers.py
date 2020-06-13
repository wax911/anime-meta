from abc import ABC
from logging import Logger
from typing import Dict, List, Optional, Union, Any

from dacite import from_dict

from data import TimeUtil, LoggingUtil
from data.entity import SigningPolicyEntity, Entity, IndexEntity, PanelEntity, SeasonEntity, EpisodeEntity, \
    SeriesEntity, MovieEntity
from data.model import Model, SigningPolicyModel, IndexModel, PanelModel, PanelSchema, SeasonSchema, SeasonModel, \
    EpisodeModel, EpisodeSchema, SeriesModel, SeriesSchema, MovieModel, MovieSchema


class CoreMapper(ABC):
    _response_key: Optional[str]
    _logger: Logger

    def __init__(
            self,
            response_key: Optional[str],
            logging_client: LoggingUtil
    ) -> None:
        """

        :param response_key:
        :param logging_client:
        """
        self._response_key = response_key
        self._logger = logging_client.get_default_logger(__name__)

    @classmethod
    def _map_to_dict(cls, model: Model) -> Dict:
        pass

    @classmethod
    def _map_to_entity(cls, model: Model) -> Entity:
        pass

    def to_model(self, response: Union[Dict, Model]) -> Union[Any, Model, List[Model]]:
        if isinstance(response, dict) and self._response_key:
            return response[self._response_key]
        return response

    def to_entity(self, model: Union[Model, List[Model]]) -> Union[Entity, List[Entity]]:
        pass


class SigningPolicyMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil, time_zone_client: TimeUtil) -> None:
        super().__init__('signing_policies', logging_client)
        self.time_util = time_zone_client

    def _map_to_entity(self, model: SigningPolicyModel) -> SigningPolicyEntity:
        expires_date_time = self.time_util.as_local_time(model.expires)
        expire_time_stamp = self.time_util.from_date_time_to_time_stamp(expires_date_time)
        return SigningPolicyEntity(
            name=model.name,
            path=model.path,
            value=model.value,
            expires=expire_time_stamp
        )

    def to_entity(self, model: List[SigningPolicyModel]) -> List[SigningPolicyEntity]:
        entities = map(self._map_to_entity, model)
        return list(entities)


class IndexMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil) -> None:
        super().__init__('items', logging_client)

    @classmethod
    def _map_to_entity(cls, model: IndexModel) -> IndexEntity:
        return IndexEntity(
            prefix=model.prefix,
            offset=model.offset,
            count=model.count
        )

    def to_entity(self, model: List[IndexModel]) -> List[IndexEntity]:
        entities = map(self._map_to_entity, model)
        return list(entities)


class PanelMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil) -> None:
        super().__init__('items', logging_client)

    @classmethod
    def _map_to_dict(cls, model: Model) -> Dict:
        schema = PanelSchema()
        return schema.dump(model)

    @classmethod
    def _map_to_entity(cls, model: PanelModel) -> PanelEntity:
        data: Dict = cls._map_to_dict(model)
        return from_dict(PanelEntity, data)

    def to_entity(self, model: List[PanelModel]) -> List[PanelEntity]:
        entities = map(self._map_to_entity, model)
        return list(entities)


class SeasonMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil) -> None:
        super().__init__('items', logging_client)

    @classmethod
    def _map_to_dict(cls, model: Model) -> Dict:
        schema = SeasonSchema()
        return schema.dump(model)

    @classmethod
    def _map_to_entity(cls, model: SeasonModel) -> SeasonEntity:
        data = cls._map_to_dict(model)
        return from_dict(SeasonEntity, data)

    def to_entity(self, model: List[SeasonModel]) -> List[SeasonEntity]:
        entities = map(self._map_to_entity, model)
        return list(entities)


class EpisodeMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil) -> None:
        super().__init__('items', logging_client)

    @classmethod
    def _map_to_dict(cls, model: Model) -> Dict:
        schema = EpisodeSchema()
        return schema.dump(model)

    @classmethod
    def _map_to_entity(cls, model: EpisodeModel) -> EpisodeEntity:
        data = cls._map_to_dict(model)
        return from_dict(EpisodeEntity, data)

    def to_entity(self, model: List[EpisodeModel]) -> List[EpisodeEntity]:
        entities = map(self._map_to_entity, model)
        return list(entities)


class SeriesMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil) -> None:
        super().__init__(None, logging_client)

    @classmethod
    def _map_to_dict(cls, model: Model) -> Dict:
        schema = SeriesSchema()
        return schema.dump(model)

    @classmethod
    def _map_to_entity(cls, model: SeriesModel) -> SeriesEntity:
        data = cls._map_to_dict(model)
        return from_dict(SeriesEntity, data)

    def to_entity(self, model: SeriesModel) -> SeriesEntity:
        entity = self._map_to_entity(model)
        return entity


class MovieMapper(CoreMapper):

    def __init__(self, logging_client: LoggingUtil) -> None:
        super().__init__(None, logging_client)

    @classmethod
    def _map_to_dict(cls, model: Model) -> Dict:
        schema = MovieSchema()
        return schema.dump(model)

    @classmethod
    def _map_to_entity(cls, model: MovieModel) -> MovieEntity:
        data = cls._map_to_dict(model)
        return from_dict(MovieEntity, data)

    def to_entity(self, model: MovieModel) -> MovieEntity:
        entity = self._map_to_entity(model)
        return entity
