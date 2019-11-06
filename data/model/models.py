from dataclasses import dataclass
from typing import Optional
from requests import Response


@dataclass()
class Parameters:
    service: Optional[str]
    username: Optional[str]
    password: Optional[str]


@dataclass()
class ResponseWrapper:
    body: Optional[dict]
    href: Optional[str]
    links: Optional[str]
    actions: Optional[str]
    class_attr: Optional[str]
    response_code: int

    def __init__(self, response: Response) -> None:
        self.body = response.json()
        self.href = self.body['__href__']
        self.links = self.body['__links__']
        self.actions = self.body['__actions__']
        self.class_attr = self.body['__class__']
        self.response_code = response.status_code

    def __repr__(self) -> str:
        return u'<VRVResponse: {}>'.format(self.class_attr)



