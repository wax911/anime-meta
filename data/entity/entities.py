from abc import ABC
from dataclasses import dataclass
from typing import Optional, List, Union, Iterable


class Entity(ABC):
    """
    Base entity type that can be iterated upon
    """

    def __iter__(self) -> Iterable:
        """
        Provides iterable for creating documents. N.B we will only provide iterables
         for top level objects and let [type_registry] handle sub type conversions
        :return:
        """
        pass


@dataclass()
class CacheLogEntity(Entity):
    collection: str
    time_stamp: int
    item_id: Optional[str]

    def __iter__(self) -> Iterable:
        yield 'collection', self.collection
        yield 'time_stamp', self.time_stamp
        yield 'item_id', self.item_id


@dataclass()
class SigningPolicyEntity(Entity):
    name: str
    path: str
    value: str
    expires: int

    def __iter__(self) -> Iterable:
        yield 'name', self.name
        yield 'path', self.path
        yield 'value', self.value
        yield 'expires', self.expires


@dataclass()
class IndexEntity(Entity):
    prefix: str
    offset: int
    count: int

    def __iter__(self) -> Iterable:
        yield 'prefix', self.prefix
        yield 'offset', self.offset
        yield 'count', self.count


@dataclass()
class SeriesPanelEntity(Entity):
    episode_count: int
    season_count: int
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    is_simulcast: bool
    maturity_ratings: List[str]
    last_public_season_number: int
    last_public_episode_number: Optional[int]


@dataclass()
class MoviePanelEntity(Entity):
    duration_ms: int
    movie_release_year: int
    is_premium_only: bool
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    available_offline: bool
    maturity_ratings: List[str]


@dataclass()
class SearchMetaEntity(Entity):
    score: int
    rank: int
    popularity_score: float


@dataclass()
class ImageEntity(Entity):
    width: int
    height: int
    type: str
    source: str


@dataclass()
class ImageContainerEntity(Entity):
    poster_tall: Optional[List[ImageEntity]]
    poster_wide: Optional[List[ImageEntity]]
    thumbnail: Optional[List[ImageEntity]]


@dataclass()
class PanelEntity(Entity):
    id: str
    external_id: str
    channel_id: str
    title: str
    description: str
    type: str
    slug: str
    images: Optional[ImageContainerEntity]
    movie_listing_metadata: Optional[MoviePanelEntity]
    series_metadata: Optional[SeriesPanelEntity]
    locale: str
    search_metadata: Optional[SearchMetaEntity]
    last_public: Optional[str]
    new: bool

    def __iter__(self) -> Iterable:
        yield 'id', self.id
        yield 'external_id', self.external_id
        yield 'channel_id', self.channel_id
        yield 'title', self.title
        yield 'description', self.description
        yield 'type', self.type
        yield 'slug', self.slug
        yield 'images', self.images
        yield 'movie_listing_metadata', self.movie_listing_metadata
        yield 'series_metadata', self.series_metadata
        yield 'locale', self.locale
        yield 'search_metadata', self.search_metadata
        yield 'last_public', self.last_public
        yield 'new', self.new


@dataclass()
class AdBreakEntity(Entity):
    type: str
    offset_ms: int


@dataclass()
class EpisodeEntity(Entity):
    id: str
    channel_id: str
    series_id: str
    series_title: str
    season_id: str
    season_title: str
    season_number: int
    episode: str
    episode_number: Optional[int]
    sequence_number: Union[int, float]
    production_episode_id: str
    title: str
    description: str
    next_episode_id: Optional[str]
    next_episode_title: Optional[str]
    hd_flag: bool
    is_mature: bool
    mature_blocked: bool
    episode_air_date: str
    is_subbed: bool
    is_dubbed: bool
    is_clip: bool
    season_tags: List[str]
    available_offline: bool
    media_type: str
    slug: str
    images: Optional[ImageContainerEntity]
    duration_ms: Optional[int]
    ad_breaks: Optional[List[AdBreakEntity]]
    is_premium_only: bool
    listing_id: str

    def __iter__(self) -> Iterable:
        yield 'id', self.id
        yield 'channel_id', self.channel_id
        yield 'series_id', self.series_id
        yield 'series_title', self.series_title
        yield 'season_id', self.season_id
        yield 'season_title', self.season_title
        yield 'season_number', self.season_number
        yield 'episode', self.episode
        yield 'episode_number', self.episode_number
        yield 'sequence_number', self.sequence_number
        yield 'production_episode_id', self.production_episode_id
        yield 'title', self.title
        yield 'description', self.description
        yield 'next_episode_id', self.next_episode_id
        yield 'next_episode_title', self.next_episode_title
        yield 'hd_flag', self.hd_flag
        yield 'is_mature', self.is_mature
        yield 'mature_blocked', self.mature_blocked
        yield 'episode_air_date', self.episode_air_date
        yield 'is_subbed', self.is_subbed
        yield 'is_dubbed', self.is_dubbed
        yield 'is_clip', self.is_clip
        yield 'season_tags', self.season_tags
        yield 'available_offline', self.available_offline
        yield 'media_type', self.media_type
        yield 'slug', self.slug
        yield 'images', self.images
        yield 'duration_ms', self.duration_ms
        yield 'ad_breaks', self.ad_breaks
        yield 'is_premium_only', self.is_premium_only
        yield 'listing_id', self.listing_id


@dataclass()
class SeasonEntity(Entity):
    id: str
    channel_id: str
    title: str
    series_id: str
    season_number: int
    is_complete: bool
    description: str
    keywords: List[str]
    season_tags: List[str]
    images: Optional[ImageContainerEntity]
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    is_simulcast: bool

    def __iter__(self) -> Iterable:
        yield 'id', self.id
        yield 'channel_id', self.channel_id
        yield 'title', self.title
        yield 'series_id', self.series_id
        yield 'season_number', self.season_number
        yield 'is_complete', self.is_complete
        yield 'description', self.description
        yield 'keywords', self.keywords
        yield 'season_tags', self.season_tags
        yield 'images', self.images
        yield 'is_mature', self.is_mature
        yield 'mature_blocked', self.mature_blocked
        yield 'is_subbed', self.is_subbed
        yield 'is_dubbed', self.is_dubbed
        yield 'is_simulcast', self.is_simulcast


@dataclass()
class SeriesEntity(Entity):
    id: str
    channel_id: str
    title: str
    slug: str
    description: str
    keywords: List[str]
    season_tags: List[str]
    images: Optional[ImageContainerEntity]
    maturity_ratings: List[str]
    episode_count: int
    season_count: int
    media_count: int
    content_provider: str
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    is_simulcast: bool

    def __iter__(self) -> Iterable:
        yield 'id', self.id
        yield 'channel_id', self.channel_id
        yield 'title', self.title
        yield 'slug', self.slug
        yield 'description', self.description
        yield 'keywords', self.keywords
        yield 'season_tags', self.season_tags
        yield 'images', self.images
        yield 'maturity_ratings', self.maturity_ratings
        yield 'episode_count', self.episode_count
        yield 'season_count', self.season_count
        yield 'media_count', self.media_count
        yield 'content_provider', self.content_provider
        yield 'is_mature', self.is_mature
        yield 'mature_blocked', self.mature_blocked
        yield 'is_subbed', self.is_subbed
        yield 'is_dubbed', self.is_dubbed
        yield 'is_simulcast', self.is_simulcast


@dataclass()
class MovieEntity(Entity):
    id: str
    channel_id: str
    title: str
    slug: str
    description: str
    keywords: List[str]
    images: Optional[ImageContainerEntity]
    maturity_ratings: List[str]
    season_tags: List[str]
    hd_flag: bool
    is_premium_only: bool
    is_mature: bool
    mature_blocked: bool
    movie_release_year: int
    content_provider: str
    is_subbed: bool
    is_dubbed: bool
    available_offline: bool

    def __iter__(self) -> Iterable:
        yield 'id', self.id
        yield 'channel_id', self.channel_id
        yield 'title', self.title
        yield 'slug', self.slug
        yield 'description', self.description
        yield 'keywords', self.keywords
        yield 'images', self.images
        yield 'maturity_ratings', self.maturity_ratings
        yield 'season_tags', self.season_tags
        yield 'hd_flag', self.hd_flag
        yield 'is_premium_only', self.is_premium_only
        yield 'is_mature', self.is_mature
        yield 'mature_blocked', self.mature_blocked
        yield 'movie_release_year', self.movie_release_year
        yield 'content_provider', self.content_provider
        yield 'is_subbed', self.is_subbed
        yield 'is_dubbed', self.is_dubbed
        yield 'available_offline', self.available_offline


