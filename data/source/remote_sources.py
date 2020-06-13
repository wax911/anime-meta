from marshmallow import EXCLUDE
from uplink import get, timeout, retry, ratelimit, Consumer, Query, Path

from data.model import SigningPolicyContainerSchema, IndexContainerSchema, CollectionContainerSchema, \
    MovieSchema, SeriesSchema, EpisodeContainerSchema, SeasonContainerSchema

__TIME_OUT__: int = 25
__MAX_ATTEMPTS__: int = 5
__RATE_LIMIT_CALLS__: int = 5
__RATE_LIMIT_PERIOD_CALLS__: int = 10


@timeout(
    seconds=__TIME_OUT__
)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class AuthenticationEndpoint(Consumer):

    @get("index")
    def get_authorization_token(self) -> SigningPolicyContainerSchema(unknown=EXCLUDE):
        """

        :return: signing policy container
        """
        pass


@timeout(
    seconds=__TIME_OUT__
)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.status(401) | retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class DiscoverEndpoint(Consumer):

    @get("browse/index")
    def get_index(
            self,
            channel_id: Query(name='channel_id', type=str),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> IndexContainerSchema(unknown=EXCLUDE):
        """

        :param channel_id:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass

    @get("browse")
    def get_catalogue(
            self,
            channel_id: Query(name='channel_id', type=str),
            sort_by: Query(name='sort_by', type=str),
            count: Query(name='n', type=int),
            start: Query(name='start', type=int),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> CollectionContainerSchema(unknown=EXCLUDE):
        """

        :param channel_id:
        :param sort_by:
        :param count:
        :param start:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass

    @get("browse")
    def get_catalogue_by_prefix(
            self,
            channel_id: Query(name='channel_id', type=str),
            sort_by: Query(name='sort_by', type=str),
            count: Query(name='n', type=int),
            query: Query(name='q', type=str),
            start: Query(name='start', type=int),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> CollectionContainerSchema(unknown=EXCLUDE):
        """

        :param channel_id:
        :param sort_by:
        :param count:
        :param query:
        :param start:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass


@timeout(
    seconds=__TIME_OUT__
)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.status(401) | retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class CollectionEndpoint(Consumer):

    @get("seasons")
    def get_seasons_for_series_id(
            self,
            series_id: Query(name='series_id', type=str),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> SeasonContainerSchema(unknown=EXCLUDE):
        """

        :param series_id:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass

    @get("episodes")
    def get_episodes_for_season(
            self,
            season_id: Query(name='season_id', type=str),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> EpisodeContainerSchema(unknown=EXCLUDE):
        """

        :param season_id:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass

    @get("movies")
    def get_episodes_for_movie(
            self,
            movie_listing_id: Query(name='movie_listing_id', type=str),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> EpisodeContainerSchema(unknown=EXCLUDE):
        """

        :param movie_listing_id:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass


@timeout(
    seconds=__TIME_OUT__
)
@retry(
    max_attempts=__MAX_ATTEMPTS__,
    when=retry.when.status(401) | retry.when.raises(Exception),
    stop=retry.stop.after_attempt(__MAX_ATTEMPTS__) | retry.stop.after_delay(__RATE_LIMIT_PERIOD_CALLS__),
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@ratelimit(
    calls=__RATE_LIMIT_CALLS__,
    period=__RATE_LIMIT_PERIOD_CALLS__
)
class DetailEndpoint(Consumer):

    @get("series/{series_id}")
    def get_series_by_id(
            self,
            series_id: Path(name='series_id', type=str),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> SeriesSchema(unknown=EXCLUDE):
        """

        :param series_id:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass

    @get("movie_listings/{movie_id}")
    def get_movie_by_id(
            self,
            movie_id: Path(name='movie_id', type=str),
            policy: Query(name='Policy', type=str),
            signature: Query(name='Signature', type=str),
            key_pair: Query(name='Key-Pair-Id', type=str)
    ) -> MovieSchema(unknown=EXCLUDE):
        """

        :param movie_id:
        :param policy:
        :param signature:
        :param key_pair:
        :return:
        """
        pass
