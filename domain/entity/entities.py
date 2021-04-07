from dataclasses import dataclass
from typing import List, Optional, Union


class Item:
    pass


@dataclass
class Index(Item):
    prefix: str
    offset: int
    count: int


@dataclass
class EntityItem(Item):
    id: str
    channel_id: str
    title: str


@dataclass
class Panel(EntityItem):
    external_id: str
    type: str
    locale: str
    last_public: Optional[str]
    new: bool


@dataclass
class Season(EntityItem):
    series_id: str
    season_number: int
    is_mature: bool
    is_subbed: bool
    is_dubbed: bool


@dataclass
class Series(EntityItem):
    slug: Optional[str]
    maturity_ratings: List[str]
    episode_count: int
    season_count: int
    media_count: int
    content_provider: str
    is_mature: bool
    is_subbed: bool
    is_dubbed: bool


@dataclass
class Movie(EntityItem):
    slug: Optional[str]
    maturity_ratings: List[str]
    movie_release_year: int
    content_provider: str
    is_mature: bool
    is_subbed: bool
    is_dubbed: bool


@dataclass
class Episode(EntityItem):
    series_id: str
    season_id: str
    season_number: int
    episode: str
    episode_number: Optional[int]
    is_mature: bool
    episode_air_date: Optional[str]
    is_subbed: bool
    is_dubbed: bool
    media_type: str
    duration_ms: Optional[int]
