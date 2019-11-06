from uplink import get, headers, params, timeout, retry, ratelimit, Consumer, Query, Path
from ..util import NetworkUtil
from requests import Response


@timeout(25)
@retry(max_attempts=5)
@ratelimit(calls=15, period=900)
@headers(NetworkUtil.get_request_headers())
class AuthenticationEndpoint(Consumer):

    @get("index")
    def get_authorization_token(self) -> Response:
        pass


@timeout(25)
@retry(max_attempts=5)
@ratelimit(calls=15, period=900)
@headers(NetworkUtil.get_request_headers())
class DiscoverEndpoint(Consumer):

    @get("browse/index")
    def get_index(self, channel_id: Query) -> Response:
        pass

    @get("browse")
    def get_catalogue(self, channel_id: Query, sort_by: Query, n: Query, start: Query) -> Response:
        pass

    @get("browse")
    def get_catalogue_by_prefix(self, channel_id: Query, sort_by: Query, n: Query, q: Query) -> Response:
        pass


@timeout(25)
@retry(max_attempts=5)
@ratelimit(calls=15, period=900)
@headers(NetworkUtil.get_request_headers())
class CollectionEndpoint(Consumer):

    @get("seasons")
    def get_seasons_for_series_id(self, series_id: Query) -> Response:
        pass

    @get("series/{series_id}")
    def get_series_by_id(self, series_id: Path) -> Response:
        pass

    @get("movie_listings/{movie_id}")
    def get_movie_by_id(self, movie_id: Path) -> Response:
        pass

    @get("episodes")
    def get_episodes_for_season(self, season_id: Query) -> Response:
        pass

    @get("movies")
    def get_episodes_for_movie(self, movie_listing_id: Query) -> Response:
        pass
