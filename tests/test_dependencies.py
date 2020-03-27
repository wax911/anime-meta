from unittest import TestCase
from di import UtilityClientScopeProvider, \
    RepositoryProvider, \
    LocalSourceProvider, \
    RemoteSourceProvider, \
    UseCaseProvider


class Test(TestCase):

    def test_utility_client_scope_provider(self):
        network_utility = UtilityClientScopeProvider.network_client()
        self.assertIsNotNone(network_utility)
        database_utility = UtilityClientScopeProvider.database_client()
        self.assertIsNotNone(database_utility)
        logging_utility = UtilityClientScopeProvider.logging_client()
        self.assertIsNotNone(logging_utility)
        time_zone_utility = UtilityClientScopeProvider.time_zone_client()
        self.assertIsNotNone(time_zone_utility)

    def test_local_source_provider(self):
        index_collection = LocalSourceProvider.index_collection()
        self.assertIsNotNone(index_collection)
        panel_collection = LocalSourceProvider.panel_collection()
        self.assertIsNotNone(panel_collection)
        series_collection = LocalSourceProvider.series_collection()
        self.assertIsNotNone(series_collection)
        seasons_collection = LocalSourceProvider.season_collection()
        self.assertIsNotNone(seasons_collection)
        episodes_collection = LocalSourceProvider.episode_collection()
        self.assertIsNotNone(episodes_collection)
        movie_collection = LocalSourceProvider.movie_collection()
        self.assertIsNotNone(movie_collection)

    def test_remote_source_provider(self):
        authentication_endpoint = RemoteSourceProvider.authentication_endpoint()
        self.assertIsNotNone(authentication_endpoint)
        collection_endpoint = RemoteSourceProvider.collection_endpoint()
        self.assertIsNotNone(collection_endpoint)
        discover_endpoint = RemoteSourceProvider.discover_endpoint()
        self.assertIsNotNone(discover_endpoint)

    def test_repository_provider(self):
        authentication_repository = RepositoryProvider.authentication_repository()
        self.assertIsNotNone(authentication_repository)
        episodes_repository = RepositoryProvider.episodes_repository()
        self.assertIsNotNone(episodes_repository)
        index_repository = RepositoryProvider.index_repository()
        self.assertIsNotNone(index_repository)
        movie_episodes_repository = RepositoryProvider.movie_episodes_repository()
        self.assertIsNotNone(movie_episodes_repository)
        movie_repository = RepositoryProvider.movie_repository()
        self.assertIsNotNone(movie_repository)
        panel_repository = RepositoryProvider.panel_repository()
        self.assertIsNotNone(panel_repository)
        seasons_repository = RepositoryProvider.seasons_repository()
        self.assertIsNotNone(seasons_repository)
        series_repository = RepositoryProvider.series_repository()
        self.assertIsNotNone(series_repository)

    def test_use_case_provider(self):
        authentication_use_case = UseCaseProvider.authentication_use_case()
        self.assertIsNotNone(authentication_use_case)
        episodes_use_case = UseCaseProvider.episodes_use_case()
        self.assertIsNotNone(episodes_use_case)
        index_use_case = UseCaseProvider.index_use_case()
        self.assertIsNotNone(index_use_case)
        movie_episodes_use_case = UseCaseProvider.movie_episodes_use_case()
        self.assertIsNotNone(movie_episodes_use_case)
        movie_use_case = UseCaseProvider.movie_use_case()
        self.assertIsNotNone(movie_use_case)
        panel_use_case = UseCaseProvider.panel_use_case()
        self.assertIsNotNone(panel_use_case)
        seasons_use_case = UseCaseProvider.seasons_use_case()
        self.assertIsNotNone(seasons_use_case)
        series_use_case = UseCaseProvider.series_use_case()
        self.assertIsNotNone(series_use_case)
