import csv
import hashlib
import os
import sys
import unittest
from .common_lib import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")
from dummyfilescreator.files_creator import FilesCreator


class TestFileHash(unittest.TestCase):
    def match_file_hash_with_log(self):
        try:
            with open(f"{TEST_DATA_DIR}/dummy-files-creator.csv", mode="r") as file:
                log_entry = next(csv.reader(file))
                file_path = log_entry[2]
                file_hash = log_entry[3]
                if os.path.exists(file_path):
                    with open(file_path, "rb") as fout:
                        bytes = fout.read()
                        hash_result = hashlib.md5(bytes).hexdigest()
                        return file_hash == hash_result
                else:
                    return False
        except IOError as error:
            print(f"error: {error}")
            return False

    def test_file_hash(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        self.assertTrue(self.match_file_hash_with_log())
        self.assertTrue(delete_data_folder())
