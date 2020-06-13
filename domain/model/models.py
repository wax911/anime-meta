from dataclasses import dataclass
from typing import Optional


@dataclass()
class Oauth:
    key: str
    secret: str


@dataclass()
class Configuration:
    client: str
    apiKey: str
    hostName: str
    authenticator: str
    oauth: Oauth
    timeZone: str
    logLevel: str


@dataclass()
class Parameters:
    service: Optional[str]
    credentials: Optional[str]


@dataclass
class LoginQuery:
    username: str
    password: str
