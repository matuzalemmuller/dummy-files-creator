import csv
import hashlib
import os
import unittest
from .common_lib import (
    create_data_folder,
    delete_data_folder,
    create_test_files,
    TEST_DATA_DIR,
)


class TestFileHash(unittest.TestCase):

    def test_file_hash(self):
        self.assertTrue(create_data_folder())
        self.assertTrue(create_test_files(1))
        try:
            with open(
                f"{TEST_DATA_DIR}/dummy-files-creator.csv", mode="r", encoding="utf-8"
            ) as file:
                log_entry = next(csv.reader(file))
                file_path = log_entry[2]
                file_hash = log_entry[3]
                if os.path.exists(file_path):
                    with open(file_path, "rb") as fout:
                        f_bytes = fout.read()
                        hash_result = hashlib.md5(f_bytes).hexdigest()
                        self.assertEqual(file_hash, hash_result)
        except IOError as error:
            print(f"error: {error}")
        self.assertTrue(delete_data_folder())
