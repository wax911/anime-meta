from dataclasses import dataclass
from itertools import chain
from typing import Optional, Dict
from requests import Response


@dataclass()
class ResponseWrapper:
    body: Optional[Dict]
    href: Optional[str]
    links: Optional[Dict]
    actions: Optional[Dict]
    class_attr: Optional[str]
    response_code: int

    def __init__(self, response: Response) -> None:
        self.body = self.__flatten_types(response.json())
        self.href = self.body['__href__']
        self.links = self.body['__links__']
        self.actions = self.body['__actions__']
        self.class_attr = self.body['__class__']
        self.response_code = response.status_code

    def __repr__(self) -> str:
        return u'<VRVResponse: {}>'.format(self.class_attr)

    @staticmethod
    def __flatten_types(json: Dict) -> Dict:
        # Images seem to be nested lists which is redundant so we're going to flatten the list
        # Also reducing the nesting depth level
        if 'images' in json:
            images = json['images']
            if 'poster_tall' in images:
                poster_tall = list(chain.from_iterable(images['poster_tall']))
                json['poster_tall'] = poster_tall
            if 'poster_wide' in images:
                poster_wide = list(chain.from_iterable(images['poster_wide']))
                json['poster_wide'] = poster_wide
            if 'thumbnail' in images:
                thumbnail = list(chain.from_iterable(images['thumbnail']))
                json['thumbnail'] = thumbnail
            del json['images']
        return json
