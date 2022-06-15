import unittest
from .common_lib import (
    create_data_folder,
    delete_data_folder,
    create_test_files,
    number_files_created,
)


class TestFileCreation(unittest.TestCase):
    def test_file_creation(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        self.assertEqual(number_files_created(), 1)
        self.assertTrue(delete_data_folder())
