from dataclasses import dataclass


@dataclass()
class Oauth:
    key: str
    secret: str


@dataclass()
class Authentication:
    client: str
    apiKey: str
    hostName: str
    collection: str
    authenticator: str
    oauth: Oauth
