import os
import json
import logging
from typing import Any
from pathlib import Path
from datetime import datetime


class InputOutputHelper:

    @staticmethod
    def __get_base_dir():
        current_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(current_path, '..')

    @staticmethod
    def get_input_directory():
        base_dir = InputOutputHelper.__get_base_dir()
        return os.path.join(base_dir, 'auth')

    @staticmethod
    def get_output_directory():
        base_dir = InputOutputHelper.__get_base_dir()
        return os.path.join(base_dir, 'auth')

    @staticmethod
    def get_file_contents(file_name):
        input_dir = InputOutputHelper.get_input_directory()
        with open(os.path.join(input_dir, file_name)) as file:
            input_data = json.loads(file.read())
        return input_data

    @staticmethod
    def create_directory(directory_path):
        creation_path = os.path.join(InputOutputHelper.get_output_directory(), directory_path)
        if not os.path.exists(creation_path):
            path = Path(creation_path)
            path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def create_file(directory_path, filename, contents) -> str:
        creation_path = os.path.join(InputOutputHelper.get_output_directory(), directory_path)
        if not os.path.exists(creation_path):
            path = Path(creation_path)
            path.mkdir(parents=True, exist_ok=True)
        with open(os.path.join(creation_path, filename), "a+") as writer:
            writer.write(contents)
        return os.path.join(directory_path, filename)


class EventLogHelper:

    @staticmethod
    def __get_current_date_time() -> Any:
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def __get_log_file(postfix: str) -> str:
        file_name = f'{EventLogHelper.__get_current_date_time()} - {postfix}.log'
        current_directory = os.path.abspath(os.path.dirname(__file__))
        directory_path = os.path.join(current_directory, '..', '..', 'logs')
        return InputOutputHelper.create_file(directory_path, file_name, '')

    @staticmethod
    def log_info(message: Any):
        logging.basicConfig(filename=EventLogHelper.__get_log_file("INFO"),
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info(f"{message}")

    @staticmethod
    def log_warning(message: Any):
        logging.basicConfig(filename=EventLogHelper.__get_log_file("WARNING"),
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.WARNING)
        logger = logging.getLogger(__name__)
        logger.warning(f"{message}")

    @staticmethod
    def log_error(message: Any):
        logging.basicConfig(filename=EventLogHelper.__get_log_file("ERROR"),
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(f"{message}")

    @staticmethod
    def log_critical(message: Any):
        logging.basicConfig(filename=EventLogHelper.__get_log_file("CRITICAL"),
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.CRITICAL)
        logger = logging.getLogger(__name__)
        logger.critical(f"{message}")
