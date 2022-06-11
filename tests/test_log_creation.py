import os
import sys
import unittest
from .common_lib import *


class TestLogCreation(unittest.TestCase):
    def test_log_creation(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        self.assertTrue(log_file_exists())
        self.assertTrue(delete_data_folder())
