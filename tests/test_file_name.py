import csv
import os
import unittest
from .common_lib import (
    create_data_folder,
    delete_data_folder,
    create_test_files,
    TEST_DATA_DIR,
)


class TestFileName(unittest.TestCase):

    def test_file_name(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        try:
            with open(
                f"{TEST_DATA_DIR}/dummy-files-creator.csv", mode="r", encoding="utf-8"
            ) as file:
                log_entry = next(csv.reader(file))
                file_path = log_entry[2]
                self.assertTrue(os.path.exists(file_path))
        except IOError as error:
            print(f"error: {error}")
        self.assertTrue(delete_data_folder())
