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
    def __match_file_name_with_log(self):
        try:
            with open(
                f"{TEST_DATA_DIR}/dummy-files-creator.csv", mode="r", encoding="utf-8"
            ) as file:
                log_entry = next(csv.reader(file))
                file_path = log_entry[2]
                if os.path.exists(file_path):
                    return True
                else:
                    return False
        except IOError as error:
            print(f"error: {error}")
            return False

    def test_file_hash(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        self.assertTrue(self.__match_file_name_with_log())
        self.assertTrue(delete_data_folder())
