from dataclasses import dataclass
from typing import List, Optional, Union


class Model:
    """Base class for network models"""
    pass


@dataclass()
class SigningPolicyModel(Model):
    name: str
    path: str
    value: str
    expires: str


@dataclass()
class IndexModel(Model):
    prefix: str
    offset: int
    count: int


@dataclass()
class SeriesPanelModel(Model):
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
class MoviePanelModel(Model):
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
class SearchMetaModel(Model):
    score: int
    rank: int
    popularity_score: float


@dataclass()
class ImageModel(Model):
    width: int
    height: int
    type: str
    source: str


@dataclass()
class ImageContainerModel(Model):
    poster_tall: Optional[List[ImageModel]]
    poster_wide: Optional[List[ImageModel]]
    thumbnail: Optional[List[ImageModel]]


@dataclass()
class PanelModel(Model):
    id: str
    external_id: str
    channel_id: str
    title: str
    description: str
    type: str
    slug: str
    images: Optional[ImageContainerModel]
    movie_listing_metadata: Optional[MoviePanelModel]
    series_metadata: Optional[SeriesPanelModel]
    locale: str
    search_metadata: Optional[SearchMetaModel]
    last_public: Optional[str]
    new: bool


@dataclass()
class AdBreakModel(Model):
    type: str
    offset_ms: int


@dataclass()
class EpisodeModel(Model):
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
    images: Optional[ImageContainerModel]
    duration_ms: int
    ad_breaks: Optional[List[AdBreakModel]]
    is_premium_only: bool
    listing_id: str


@dataclass()
class SeasonModel(Model):
    id: str
    channel_id: str
    title: str
    series_id: str
    season_number: int
    is_complete: bool
    description: str
    keywords: List[str]
    season_tags: List[str]
    images: Optional[ImageContainerModel]
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    is_simulcast: bool


@dataclass()
class SeriesModel(Model):
    id: str
    channel_id: str
    title: str
    slug: str
    description: str
    keywords: List[str]
    season_tags: List[str]
    images: Optional[ImageContainerModel]
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
class MovieModel(Model):
    id: str
    channel_id: str
    title: str
    slug: str
    description: str
    keywords: List[str]
    images: Optional[ImageContainerModel]
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
