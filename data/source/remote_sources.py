from uplink import get, timeout, retry, ratelimit, Consumer, Query, Path
from requests import Response


@timeout(25)
@retry(max_attempts=5)
@ratelimit(calls=15, period=900)
class AuthenticationEndpoint(Consumer):

    @get("index")
    def get_authorization_token(self) -> Response:
        pass


@timeout(25)
@retry(max_attempts=5)
@ratelimit(calls=15, period=900)
class DiscoverEndpoint(Consumer):

    @get("browse/index")
    def get_index(
            self,
            service: Query('channel_id'),
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id'),
    ) -> Response:
        pass

    @get("browse")
    def get_catalogue(
            self,
            service: Query('channel_id'),
            sort_by: Query,
            n: Query,
            start: Query,
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id'),
    ) -> Response:
        pass

    @get("browse")
    def get_catalogue_by_prefix(
            self,
            service: Query('channel_id'),
            sort_by: Query,
            count: Query('n'),
            query: Query('q'),
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id')
    ) -> Response:
        pass


@timeout(25)
@retry(max_attempts=5)
@ratelimit(calls=15, period=900)
class CollectionEndpoint(Consumer):

    @get("seasons")
    def get_seasons_for_series_id(
            self,
            series_id: Query,
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id')
    ) -> Response:
        pass

    @get("series/{series_id}")
    def get_series_by_id(
            self,
            series_id: Path,
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id')
    ) -> Response:
        pass

    @get("movie_listings/{movie_id}")
    def get_movie_by_id(
            self,
            movie_id: Path,
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id')
    ) -> Response:
        pass

    @get("episodes")
    def get_episodes_for_season(
            self,
            season_id: Query,
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id')
    ) -> Response:
        pass

    @get("movies")
    def get_episodes_for_movie(
            self,
            movie_listing_id: Query,
            policy: Query('Policy'),
            signature: Query('Signature'),
            key_pair: Query('Key-Pair-Id')
    ) -> Response:
        pass
