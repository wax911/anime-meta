from typing import Dict, List

from dacite import from_dict
from requests import Response

from data import TimeUtil
from domain.model import ResponseWrapper
from domain.entity import SigningPolicy


class ResponseMapper:

    @staticmethod
    def from_response(response: Response) -> ResponseWrapper:
        # _logger.debug(
        #     "Response status: `%s %s` | headers: %s",
        #     response.reason, response.status_code, response.headers
        # )
        response_wrapper = ResponseWrapper(response)
        return response_wrapper


class SigningPolicyMapper:

    @staticmethod
    def map_from_response(response: Response, time_zone_client: TimeUtil) -> List[SigningPolicy]:
        wrapper = ResponseMapper.from_response(response)
        raw_json: [dict] = wrapper.body['signing_policies']
        signing_policies = list()
        for entry in raw_json:
            expires_date_time = time_zone_client.as_local_time(entry['expires'])
            expire_time_stamp = time_zone_client.from_date_time_to_time_stamp(expires_date_time)
            policy = SigningPolicy(
                name=entry['name'],
                path=entry['path'],
                value=entry['value'],
                expires=expire_time_stamp
            )
            signing_policies.append(policy)
        return signing_policies

    @staticmethod
    def map_from_dict(models: List[Dict]) -> List[SigningPolicy]:
        entities = list()
        for model in models:
            entity = from_dict(SigningPolicy, model)
            entities.append(entity)
        return entities

    @staticmethod
    def map_to_dict(entities: List[SigningPolicy]) -> List[Dict]:
        models = list()
        for entity in entities:
            model = dict(entity)
            models.append(model)
        return models
