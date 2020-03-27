import os
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Union

import yaml
import logging

from pathlib import Path
from logging import Formatter, StreamHandler, Logger


class FileSystem:

    @staticmethod
    def __get_base_dir():
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '..', '..')

    @staticmethod
    def get_input_directory():
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'config')

    @staticmethod
    def get_output_directory():
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'config')

    @staticmethod
    def get_file_contents(file_name):
        input_dir = FileSystem.get_input_directory()
        with open(os.path.join(input_dir, file_name)) as file:
            input_data = yaml.safe_load(file)
        return input_data

    @staticmethod
    def create_directory(directory_path):
        creation_path = os.path.join(FileSystem.get_output_directory(), directory_path)
        if not os.path.exists(creation_path):
            path = Path(creation_path)
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_file(directory_path, filename, contents) -> str:
        creation_path = os.path.join(FileSystem.get_output_directory(), directory_path)
        if not os.path.exists(creation_path):
            path = Path(creation_path)
            path.mkdir(parents=True, exist_ok=True)
        with open(os.path.join(creation_path, filename), "a+") as writer:
            writer.write(contents)
        return os.path.join(directory_path, filename)


class Logging(Logger):
    __FORMATTER = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"

    def __init__(
            self,
            name: str,
            log_file_name: str = 'anitrend.api',
            log_format: str = __FORMATTER,
            level: Union[int, str] = logging.DEBUG,
            *args,
            **kwargs
     ) -> None:
        super().__init__(name, level)
        self.formatter = Formatter(log_format)
        self.file_name = log_file_name
        self.addHandler(self.__get_stream_handler())
        self.addHandler(self.__get_file_handler())

    def __get_log_file(self) -> str:
        file_name = f'{self.file_name}.log'
        current_directory = os.path.abspath(os.path.dirname(__file__))
        directory_path = os.path.join(current_directory, '..', '..', 'logs')
        return FileSystem.create_file(directory_path, file_name, '')

    def __get_file_handler(self) -> TimedRotatingFileHandler:
        handler = TimedRotatingFileHandler(
            filename=self.__get_log_file(),
            when='midnight',
            backupCount=5
        )
        handler.setFormatter(self.formatter)
        return handler

    def __get_stream_handler(self) -> StreamHandler:
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        return handler
