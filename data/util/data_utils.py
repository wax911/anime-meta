from datetime import datetime, tzinfo
import logging
from logging import Logger
from typing import Dict

import pytz
from pytz import BaseTzInfo
from requests_oauthlib import OAuth1Session

from core.util.file_system import FileSystem, Logging

from domain.model import Configuration, Oauth, Header


class LoggingUtil:

    def __init__(self) -> None:
        self._attachment = FileSystem.get_file_contents('configuration.yaml')

    def get_default_logger(self, name: str) -> Logger:
        logging.setLoggerClass(Logging)
        logger = logging.getLogger(name)
        logger.setLevel(self._attachment['log_level'])
        return logger


class BaseUtil(object):

    def __init__(self) -> None:
        self._logger = LoggingUtil().get_default_logger(__name__)
        self._configuration = self.__build_configuration(
            FileSystem.get_file_contents('configuration.yaml')
        )

    @staticmethod
    def __build_configuration(attachment: Dict) -> Configuration:
        return Configuration(
            client=attachment['client'],
            api_key=attachment['api_key'],
            base_url=attachment['base_url'],
            host_name=attachment['host_name'],
            authenticator=attachment['authenticator'],
            oauth=Oauth(
                key=attachment['oauth']['key'],
                secret=attachment['oauth']['secret']
            ),
            time_zone=attachment['time_zone'],
            log_level=attachment['log_level'],
            headers=Header(
                user_agent=attachment['header']['user_agent'],
                accept_encoding=attachment['header']['accept_encoding'],
                accept=attachment['header']['accept'],
                accept_language=attachment['header']['accept_language']
            )
        )


class DatabaseUtil(BaseUtil):

    def create_connection_string(self) -> str:
        __schema = 'mongodb://'
        __client = self._configuration.client
        __authenticator = self._configuration.authenticator
        __api_key = self._configuration.api_key
        __host_name = self._configuration.host_name
        return f'{__schema}{__client}:{__api_key}@{__host_name}/{__authenticator}'

    def disconnect(self) -> None:
        from data.source.local_sources import Dao
        Dao.close_database(self._logger)


class TimeUtil(BaseUtil):
    TIME_FORMAT_TEMPLATE = '%Y-%m-%dT%H:%M:%S%z'

    @staticmethod
    def default_timezone() -> BaseTzInfo:
        return pytz.utc

    def __get_current_tz(self) -> tzinfo:
        timezone = self._configuration.time_zone
        return pytz.timezone(timezone)

    def as_local_time(self, time_unit: str, time_unit_format: str = TIME_FORMAT_TEMPLATE) -> datetime:
        tz = self.__get_current_tz()
        current_time_unit = datetime.strptime(time_unit, time_unit_format)
        local_time = current_time_unit.astimezone(tz)
        self._logger.debug(
            f'Converted `{time_unit}` to local time of `{local_time}` using time format: `{time_unit_format}`'
        )
        return local_time

    def get_current_time_formatted(self, time_format: str = TIME_FORMAT_TEMPLATE) -> str:
        current_time = datetime.now(tz=self.__get_current_tz())
        return current_time.strftime(time_format)

    def get_current_time(self) -> datetime:
        current_time = datetime.now(tz=self.__get_current_tz())
        return current_time

    @staticmethod
    def from_date_time_to_time_stamp(time_unit: datetime) -> int:
        return int(time_unit.timestamp())

    def get_current_timestamp(self) -> int:
        current_date_time = self.get_current_time()
        current_time_stamp = self.from_date_time_to_time_stamp(current_date_time)
        return current_time_stamp


class NetworkUtil(BaseUtil):

    def create_session(self) -> OAuth1Session:
        session = OAuth1Session(
            client_key=self._configuration.oauth.key,
            client_secret=self._configuration.oauth.secret
        )
        session.headers = self.__get_request_headers(self._configuration.headers)
        return session

    @staticmethod
    def __get_request_headers(header: Header) -> Dict:
        return {
            'User-Agent': header.user_agent,
            'Accept-Encoding': header.accept_encoding,
            'Accept': header.accept,
            'Accept-Language': header.accept_language,
        }

    def get_authentication_url(self) -> str:
        return self._configuration.base_url + '/core/'

    def get_discover_url(self) -> str:
        return self._configuration.base_url + '/disc/public/v1/US/M2/-/-/'

    def get_collection_url(self) -> str:
        return self._configuration.base_url + '/cms/v2/US/M2/-/'
