from abc import ABC
from dataclasses import dataclass
from typing import Optional, List, Union


class Entity(ABC):
    """
    Base entity type that can be iterated upon
    """

    def __iter__(self):
        pass


@dataclass()
class CacheLogEntity(Entity):
    collection: str
    time_stamp: int
    item_id: Optional[str]

    def __iter__(self):
        yield 'collection', self.collection
        yield 'time_stamp', self.time_stamp
        yield 'item_id', self.item_id


@dataclass()
class SigningPolicyEntity(Entity):
    name: str
    path: str
    value: str
    expires: int


@dataclass()
class IndexEntity(Entity):
    prefix: str
    offset: int
    count: int


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
    last_public_episode_number: int


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
    episode_number: int
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
    duration_ms: int
    ad_breaks: Optional[List[AdBreakEntity]]
    is_premium_only: bool
    listing_id: str


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
