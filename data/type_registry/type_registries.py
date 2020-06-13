from abc import ABC, abstractproperty
from typing import Dict, Optional
from bson.codec_options import TypeCodec
from dacite import from_dict, Config
from marshmallow import Schema

from data.entity import Entity, CacheLogEntity, IndexEntity, SigningPolicyEntity, SeriesPanelEntity, \
    MoviePanelEntity, SearchMetaEntity, ImageEntity, ImageContainerEntity, PanelEntity, AdBreakEntity, \
    EpisodeEntity, SeasonEntity, SeriesEntity, MovieEntity

from data.model import SigningPolicySchema, IndexSchema, SeriesPanelMetaSchema, MoviePanelMetaSchema, \
    SearchMetaSchema, ImageSchema, ImageContainerSchema, PanelSchema, AdBreakSchema, EpisodeSchema, \
    SeasonSchema, SeriesSchema, MovieSchema


class CoreEntityCodec(TypeCodec, ABC):
    """Base entity codec"""
    _config: Optional[Config] = None

    def transform_python(self, value: Entity) -> Dict:
        """Convert the given Python object into something serializable."""
        if self._schema_type():
            _schema_type: type = self._schema_type()
            _schema: Schema = _schema_type()
            _dict = _schema.dump(value)
            return _dict

        return dict(value)

    def transform_bson(self, value: Dict) -> Entity:
        """Convert the given BSON value into our own type."""
        return from_dict(
            data_class=self.python_type,
            config=self._config,
            data=value
        )

    @property
    def bson_type(self) -> type:
        """The BSON type to be converted into our own type."""
        return dict

    @abstractproperty
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        pass


class CacheLogEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return None

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return CacheLogEntity


class SigningPolicyEntityCodec(CoreEntityCodec):

    def __init__(self) -> None:
        self._config = Config()

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return SigningPolicySchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return SigningPolicyEntity


class IndexEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return IndexSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return IndexEntity


class SeriesPanelEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return SeriesPanelMetaSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return SeriesPanelEntity


class MoviePanelEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return MoviePanelMetaSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return MoviePanelEntity


class SearchMetaEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return SearchMetaSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return SearchMetaEntity


class ImageEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return ImageSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return ImageEntity


class ImageContainerEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return ImageContainerSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return ImageContainerEntity


class PanelEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return PanelSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return PanelEntity


class AdBreakEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return AdBreakSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return AdBreakEntity


class EpisodeEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return EpisodeSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return EpisodeEntity


class SeasonEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return SeasonSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return SeasonEntity


class SeriesEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return SeriesSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return SeriesEntity


class MovieEntityCodec(CoreEntityCodec):

    @property
    def _schema_type(self) -> Optional[type]:
        """The schema type to be used to convert value objects to `bson_type`"""
        return MovieSchema

    @property
    def python_type(self) -> type:
        """The Python type to be converted into something serializable."""
        return MovieEntity
