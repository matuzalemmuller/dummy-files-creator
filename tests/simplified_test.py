#! /usr/bin/env python3
import unittest
import shutil
import os
import sys
import csv
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dummyfilescreator.files_creator import FilesCreator

ROOT_DIR = os.getcwd()
TEST_DATA_DIR = f"{ROOT_DIR}/tests/data"

class Test(unittest.TestCase):

    def create_data_folder(self):
        try:
            os.makedirs(TEST_DATA_DIR)
        except OSError as error:
            print(f"error: {error}")
            return False

        return True


    def delete_data_folder(self):
        if os.path.isdir(TEST_DATA_DIR):
            try:
                shutil.rmtree(TEST_DATA_DIR)
            except (shutil.Error, OSError) as error:
                print(f"error: {error}")
                return False

        return True


    def create_test_data(self):
        files_creator = FilesCreator(
            folder_path=TEST_DATA_DIR,
            number_files=1,
            size_file=1,
            size_unit="MiB",
            log_path=TEST_DATA_DIR,
            log_hash=True,
            chunk_size=1024,
            chunk_unit="KiB",
        )
        files_creator.start()
        files_creator.join()

        return True


    def check_file_hash(self):
        try:
            with open(f"{TEST_DATA_DIR}/dummy-files-creator.csv", mode="r") as file:
                log_entry = next(csv.reader(file))
                file_path = log_entry[2]
                file_hash = log_entry[3]
                if os.path.exists(file_path):
                    with open(file_path, "rb") as fout:
                        bytes = fout.read()
                        hash_result = hashlib.md5(bytes).hexdigest()
                        assert (
                            file_hash == hash_result
                        ), f"Saved hash: {file_hash}, calculated hash: {hash_result}"
                else:
                    return False
        except IOError as error:
            print(f"error: {error}")
            return False

        return True

    def test_file_hash(self):
        if not self.delete_data_folder():
            sys.exit(1)

        if not self.create_data_folder():
            sys.exit(1)

        if not self.create_test_data():
            sys.exit(1)

        if not self.check_file_hash():
            sys.exit(1)

        if not self.delete_data_folder():
            sys.exit(1)

if __name__ == "__main__":
    unittest.main()
