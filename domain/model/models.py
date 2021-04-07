from dataclasses import dataclass
from typing import Optional


@dataclass()
class Oauth:
    key: str
    secret: str


@dataclass()
class Header:
    user_agent: str
    accept_encoding: str
    accept: str
    accept_language: str


@dataclass()
class Configuration:
    client: str
    api_key: str
    base_url: str
    host_name: str
    authenticator: str
    oauth: Oauth
    time_zone: str
    log_level: str
    headers: Header


@dataclass()
class Parameters:
    service: Optional[str]
    credentials: Optional[str]


@dataclass
class LoginQuery:
    username: str
    password: str
