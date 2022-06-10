import glob
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")
from dummyfilescreator.files_creator import FilesCreator

ROOT_DIR = os.getcwd()
TEST_DATA_DIR = f"{ROOT_DIR}/tests/data"


def create_data_folder():
    if not delete_data_folder():
        return False

    try:
        os.makedirs(TEST_DATA_DIR)
    except OSError as error:
        print(f"error: {error}")
        return False

    return True


def delete_data_folder():
    if os.path.isdir(TEST_DATA_DIR):
        try:
            shutil.rmtree(TEST_DATA_DIR)
        except (shutil.Error, OSError) as error:
            print(f"error: {error}")
            return False

    return True


def create_test_files(number_files: int):
    files_creator = FilesCreator(
        folder_path=TEST_DATA_DIR,
        number_files=number_files,
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


def number_files_created():
    try:
        return len(glob.glob(f"{TEST_DATA_DIR}/*.dummy"))
    except IOError as error:
        print(f"error: {error}")
        return -1


def get_names_files_created():
    try:
        return glob.glob(f"{TEST_DATA_DIR}/*.dummy")
    except IOError as error:
        print(f"error: {error}")
        return False


def log_file_exists():
    if os.path.exists(f"{TEST_DATA_DIR}/dummy-files-creator.csv"):
        return True
    return False
