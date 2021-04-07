from typing import Dict
from unittest import TestCase

from marshmallow import EXCLUDE

from data.model.schemas import SigningPolicyContainerSchema, \
    IndexContainerSchema, CollectionContainerSchema, EpisodeContainerSchema, \
    SeasonContainerSchema, SeriesSchema, MovieSchema

from data.model.models import SigningPolicyModel, EpisodeModel, \
    SeasonModel, SeriesModel, IndexModel, PanelModel, MovieModel


def __load_sample_file__(file_name: str) -> dict:
    """
    Loads a file from the sample directory
    :param file_name: file name to load
    :return: contents as dict
    """
    import os
    import json
    current_path = os.path.abspath(os.path.dirname(__file__))
    samples_path = os.path.join(current_path, '..', 'samples')
    with open(os.path.join(samples_path, file_name)) as file:
        input_data = json.load(file)
    return input_data


class Test(TestCase):

    def test_signing_policy_response(self):
        json: Dict = __load_sample_file__('signing_policy.json')
        schema = SigningPolicyContainerSchema()
        result: Dict = schema.load(json, unknown=EXCLUDE)
        self.assertIn('signing_policies', result)
        item: SigningPolicyModel = result['signing_policies'][0]
        self.assertIsInstance(item, SigningPolicyModel)

    def test_index_response(self):
        json: Dict = __load_sample_file__('index.json')
        schema = IndexContainerSchema()
        result: Dict = schema.load(json, unknown=EXCLUDE)
        self.assertIn('items', result)
        item: IndexModel = result['items'][0]
        self.assertIsInstance(item, IndexModel)

    def test_collection_response(self):
        json: Dict = __load_sample_file__('collection.json')
        schema = CollectionContainerSchema()
        result: Dict = schema.load(json, unknown=EXCLUDE)
        self.assertIn('items', result)
        item: PanelModel = result['items'][0]
        self.assertIsInstance(item, PanelModel)

    def test_episode_response(self):
        json: Dict = __load_sample_file__('episodes.json')
        schema = EpisodeContainerSchema()
        result: Dict = schema.load(json, unknown=EXCLUDE)
        self.assertIn('items', result)
        item: EpisodeModel = result['items'][0]
        self.assertIsInstance(item, EpisodeModel)

    def test_season_response(self):
        json: Dict = __load_sample_file__('seasons.json')
        schema = SeasonContainerSchema()
        result: Dict = schema.load(json, unknown=EXCLUDE)
        self.assertIn('items', result)
        item: SeasonModel = result['items'][0]
        self.assertIsInstance(item, SeasonModel)

    def test_series_response(self):
        json: Dict = __load_sample_file__('series.json')
        schema = SeriesSchema()
        result: SeriesModel = schema.load(json, unknown=EXCLUDE)
        self.assertIsInstance(result, SeriesModel)

    def test_movie_response(self):
        json: Dict = __load_sample_file__('movie.json')
        schema = MovieSchema()
        result: MovieModel = schema.load(json, unknown=EXCLUDE)
        self.assertIsInstance(result, MovieModel)
