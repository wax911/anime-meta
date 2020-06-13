import typing
from itertools import chain
from typing import Optional

from dacite import from_dict
from marshmallow import Schema, fields, RAISE, EXCLUDE, post_load, types
from marshmallow.error_store import ErrorStore
from marshmallow.fields import String, Integer, Float, Boolean, List
from marshmallow.schema import _T as T

from .models import SigningPolicyModel, EpisodeModel, SeasonModel, SeriesModel, IndexModel, PanelModel, MovieModel, \
    ImageContainerModel, AdBreakModel, SearchMetaModel, ImageModel, SeriesPanelModel, MoviePanelModel


class TypedSchema(Schema):

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None, type_inference: Optional[type] = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown)
        self._type_inference = type_inference

    @post_load()
    def _on_post_load(self, data, many, **kwargs) -> typing.Any:
        if self._type_inference is None:
            return data
        # noinspection PyTypeChecker
        obj = from_dict(self._type_inference, data)
        return obj


class CoreSchema(TypedSchema):
    """
    Base type schema
    """
    __class__: String = fields.Str(load_only=True)
    __href__: String = fields.Str(load_only=True)
    __resource_key__: String = fields.Str(allow_none=True, load_only=True)

    @staticmethod
    def __modify_image_body(
            data: typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[typing.Mapping[str, typing.Any]]]
    ) -> typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[typing.Mapping[str, typing.Any]]]:
        # Images seem to be nested lists which is redundant so we're going to flatten the list
        if 'images' in data:
            images = data['images']
            if 'poster_tall' in images:
                poster_tall = list(chain.from_iterable(images['poster_tall']))
                data['images']['poster_tall'] = poster_tall
            if 'poster_wide' in images:
                poster_wide = list(chain.from_iterable(images['poster_wide']))
                data['images']['poster_wide'] = poster_wide
            if 'thumbnail' in images:
                thumbnail = list(chain.from_iterable(images['thumbnail']))
                data['images']['thumbnail'] = thumbnail
        return data

    def _deserialize(
            self,
            data: typing.Union[
                typing.Mapping[str, typing.Any],
                typing.Iterable[typing.Mapping[str, typing.Any]],
            ], *,
            error_store: ErrorStore,
            many: bool = False,
            partial=False,
            unknown=RAISE,
            index=None
    ) -> typing.Union[T, typing.List[T]]:
        return super()._deserialize(
            self.__modify_image_body(data),
            error_store=error_store,
            many=many,
            partial=partial,
            unknown=unknown,
            index=index
        )


class SigningPolicySchema(TypedSchema):
    name: String = fields.Str(load_only=True)
    path: String = fields.Str(load_only=True)
    value: String = fields.Str(load_only=True)
    expires: String = fields.Str(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=SigningPolicyModel)


class SigningPolicyContainerSchema(CoreSchema):
    signing_policies: List = fields.List(
        fields.Nested(
            nested=SigningPolicySchema,
            load_only=True
        )
    )


class IndexSchema(TypedSchema):
    prefix: String = fields.Str(load_only=True)
    offset: Integer = fields.Int(load_only=True)
    count: Integer = fields.Int(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=IndexModel)


class IndexContainerSchema(CoreSchema):
    total_count: Integer = fields.Int(load_only=True)
    num_items: Integer = fields.Int(load_only=True)
    items = fields.List(
        fields.Nested(
            nested=IndexSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )


class SeriesPanelMetaSchema(TypedSchema):
    episode_count: Integer = fields.Int(load_only=True)
    season_count: Integer = fields.Int(load_only=True)
    is_mature: Boolean = fields.Bool(load_only=True)
    mature_blocked: Boolean = fields.Bool(load_only=True)
    is_subbed: Boolean = fields.Bool(load_only=True)
    is_dubbed: Boolean = fields.Bool(load_only=True)
    is_simulcast: Boolean = fields.Bool(load_only=True)
    maturity_ratings: List = fields.List(fields.Str(load_only=True))
    last_public_season_number: Integer = fields.Int(load_only=True)
    last_public_episode_number: Integer = fields.Int(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=SeriesPanelModel)


class MoviePanelMetaSchema(TypedSchema):
    duration_ms: Integer = fields.Int(load_only=True)
    movie_release_year: Integer = fields.Int(load_only=True)
    is_premium_only: Boolean = fields.Bool(load_only=True)
    is_mature: Boolean = fields.Bool(load_only=True)
    mature_blocked: Boolean = fields.Bool(load_only=True)
    is_subbed: Boolean = fields.Bool(load_only=True)
    is_dubbed: Boolean = fields.Bool(load_only=True)
    available_offline: Boolean = fields.Bool(load_only=True)
    maturity_ratings: List = fields.List(fields.Str(load_only=True))

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=MoviePanelModel)


class SearchMetaSchema(TypedSchema):
    score: Integer = fields.Int(load_only=True)
    rank: Integer = fields.Int(load_only=True)
    popularity_score: Float = fields.Float(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=SearchMetaModel)


class ImageSchema(TypedSchema):
    width: Integer = fields.Int(load_only=True)
    height: Integer = fields.Int(load_only=True)
    type: String = fields.Str(load_only=True)
    source: String = fields.Str(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=ImageModel)


class ImageContainerSchema(TypedSchema):
    poster_tall: List = fields.List(
        fields.Nested(
            nested=ImageSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )
    poster_wide: List = fields.List(
        fields.Nested(
            nested=ImageSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )
    thumbnail: List = fields.List(
        fields.Nested(
            nested=ImageSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=ImageContainerModel)


class PanelSchema(CoreSchema):
    id: String = fields.Str(load_only=True)
    external_id: String = fields.Str(load_only=True)
    channel_id: String = fields.Str(load_only=True)
    title: String = fields.Str(load_only=True)
    description: String = fields.Str(load_only=True)
    type: String = fields.Str(load_only=True)
    slug: String = fields.Str(load_only=True)
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    movie_listing_metadata = fields.Nested(
        nested=MoviePanelMetaSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    series_metadata = fields.Nested(
        nested=SeriesPanelMetaSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    locale: String = fields.Str(load_only=True)
    search_metadata = fields.Nested(
        nested=SearchMetaSchema,
        unknown=EXCLUDE,
        load_only=True
    )
    last_public: String = fields.Str(load_only=True, allow_none=True)
    new: Boolean = fields.Bool(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=PanelModel)


class CollectionContainerSchema(CoreSchema):
    total: Integer = fields.Int(load_only=True)
    items: List = fields.List(
        fields.Nested(
            nested=PanelSchema,
            unknown=EXCLUDE,
            load_only=True
        )
    )


class AdBreakSchema(TypedSchema):
    type: String = fields.Str(load_only=True)
    offset_ms: Integer = fields.Int(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=AdBreakModel)


class EpisodeSchema(CoreSchema):
    id: String = fields.Str(load_only=True)
    channel_id: String = fields.Str(load_only=True)
    series_id: String = fields.Str(load_only=True)
    series_title: String = fields.Str(load_only=True)
    season_id: String = fields.Str(load_only=True)
    season_title: String = fields.Str(load_only=True)
    season_number: Integer = fields.Int(load_only=True)
    episode: String = fields.Str(load_only=True)
    episode_number: Integer = fields.Int(load_only=True)
    sequence_number: Integer = fields.Int(load_only=True, strict=False)
    production_episode_id: String = fields.Str(load_only=True)
    title: String = fields.Str(load_only=True)
    description: String = fields.Str(load_only=True)
    next_episode_id: String = fields.Str(load_only=True, allow_none=True)
    next_episode_title: String = fields.Str(load_only=True, allow_none=True)
    hd_flag: Boolean = fields.Bool(load_only=True)
    is_mature: Boolean = fields.Bool(load_only=True)
    mature_blocked: Boolean = fields.Bool(load_only=True)
    episode_air_date: String = fields.Str(load_only=True)
    is_subbed: Boolean = fields.Bool(load_only=True)
    is_dubbed: Boolean = fields.Bool(load_only=True)
    is_clip: Boolean = fields.Bool(load_only=True)
    season_tags: List = fields.List(fields.Str(load_only=True))
    available_offline: Boolean = fields.Bool(load_only=True)
    media_type: String = fields.Str(load_only=True)
    slug: String = fields.Str(load_only=True)
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    duration_ms: Integer = fields.Int(load_only=True)
    ad_breaks = fields.List(
        fields.Nested(
            nested=AdBreakSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )
    is_premium_only: Boolean = fields.Bool(load_only=True)
    listing_id: String = fields.Str(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=EpisodeModel)


class EpisodeContainerSchema(CoreSchema):
    total: Integer = fields.Int(load_only=True)
    items: List = fields.List(
        fields.Nested(
            nested=EpisodeSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )


class SeasonSchema(CoreSchema):
    id: String = fields.Str(load_only=True)
    channel_id: String = fields.Str(load_only=True)
    title: String = fields.Str(load_only=True)
    series_id: String = fields.Str(load_only=True)
    season_number: Integer = fields.Int(load_only=True)
    is_complete: Boolean = fields.Bool(load_only=True)
    description: String = fields.Str(load_only=True)
    keywords: List = fields.List(fields.Str(load_only=True))
    season_tags: List = fields.List(fields.Str(load_only=True))
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    is_mature: Boolean = fields.Bool(load_only=True)
    mature_blocked: Boolean = fields.Bool(load_only=True)
    is_subbed: Boolean = fields.Bool(load_only=True)
    is_dubbed: Boolean = fields.Bool(load_only=True)
    is_simulcast: Boolean = fields.Bool(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=SeasonModel)


class SeasonContainerSchema(CoreSchema):
    total: Integer = fields.Int(load_only=True)
    items: List = fields.List(
        fields.Nested(
            nested=SeasonSchema,
            allow_none=True,
            unknown=EXCLUDE,
            load_only=True
        )
    )


class SeriesSchema(CoreSchema):
    id: String = fields.Str(load_only=True)
    channel_id: String = fields.Str(load_only=True)
    title: String = fields.Str(load_only=True)
    slug: String = fields.Str(load_only=True)
    description: String = fields.Str(load_only=True)
    keywords: List = fields.List(fields.Str(load_only=True))
    season_tags: List = fields.List(fields.Str(load_only=True))
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    maturity_ratings: List = fields.List(fields.Str(load_only=True))
    episode_count: Integer = fields.Int(load_only=True)
    season_count: Integer = fields.Int(load_only=True)
    media_count: Integer = fields.Int(load_only=True)
    content_provider: String = fields.Str(load_only=True)
    is_mature: Boolean = fields.Bool(load_only=True)
    mature_blocked: Boolean = fields.Bool(load_only=True)
    is_subbed: Boolean = fields.Bool(load_only=True)
    is_dubbed: Boolean = fields.Bool(load_only=True)
    is_simulcast: Boolean = fields.Bool(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=SeriesModel)


class MovieSchema(CoreSchema):
    id: String = fields.Str(load_only=True)
    channel_id: String = fields.Str(load_only=True)
    title: String = fields.Str(load_only=True)
    slug: String = fields.Str(load_only=True)
    description: String = fields.Str(load_only=True)
    keywords: List = fields.List(fields.Str(load_only=True))
    images = fields.Nested(
        nested=ImageContainerSchema,
        allow_none=True,
        unknown=EXCLUDE,
        load_only=True
    )
    maturity_ratings: List = fields.List(fields.Str(load_only=True))
    season_tags: List = fields.List(fields.Str(load_only=True))
    hd_flag: Boolean = fields.Bool(load_only=True)
    is_premium_only: Boolean = fields.Bool(load_only=True)
    is_mature: Boolean = fields.Bool(load_only=True)
    mature_blocked: Boolean = fields.Bool(load_only=True)
    movie_release_year: Integer = fields.Int(load_only=True)
    content_provider: String = fields.Str(load_only=True)
    is_subbed: Boolean = fields.Bool(load_only=True)
    is_dubbed: Boolean = fields.Bool(load_only=True)
    available_offline: Boolean = fields.Bool(load_only=True)

    def __init__(self, *, only: types.StrSequenceOrSet = None, exclude: types.StrSequenceOrSet = (), many: bool = False,
                 context: typing.Dict = None, load_only: types.StrSequenceOrSet = (),
                 dump_only: types.StrSequenceOrSet = (), partial: typing.Union[bool, types.StrSequenceOrSet] = False,
                 unknown: str = None):
        super().__init__(only=only, exclude=exclude, many=many, context=context, load_only=load_only,
                         dump_only=dump_only, partial=partial, unknown=unknown, type_inference=MovieModel)
