from unittest import TestCase
from core import FileSystem


class TestFileSystem(TestCase):

    def test_get_input_directory(self):
        directory_path = FileSystem.get_input_directory()
        self.assertIsNotNone(directory_path)

    def test_get_output_directory(self):
        directory_path = FileSystem.get_output_directory()
        self.assertIsNotNone(directory_path)

    def test_get_file_contents(self):
        file_name = 'configuration.yaml'
        output_contents = FileSystem.get_file_contents(file_name)
        self.assertIsNotNone(output_contents)
