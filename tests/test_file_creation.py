import os
import sys
import unittest
from .common_lib import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")
from dummyfilescreator.files_creator import FilesCreator


class TestFileCreation(unittest.TestCase):
    def test_log_creation(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        self.assertEqual(number_files_created(), 1)
        self.assertTrue(delete_data_folder())
