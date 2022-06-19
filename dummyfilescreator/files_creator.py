"""Author: Matuzalem (Mat) Muller.

License: GPLv3
"""
import hashlib
import math
import os
import threading
import uuid
from .logger import Logger


class FilesCreator(threading.Thread):  # pylint: disable=too-many-instance-attributes
    """Creates files."""

    __slots__ = (
        "__folder_path",
        "__number_files",
        "__log_path",
        "__log_hash",
        "__error_function",
        "__abort",
        "__chunk_size_bytes",
        "__readable_size",
        "__logger",
        "number_of_chunks",
        "n_created",
        "file_name",
        "chunk_n",
        "complete",
    )

    def __init__(  # pylint: disable=too-many-arguments, too-many-locals, too-many-branches
        self,
        folder_path: str,
        number_files: int,
        size_file: int,
        size_unit: str,
        chunk_size: int,
        chunk_unit: str,
        log_path: str = None,
        log_hash: bool = None,
        error_function=None,
    ):
        """Save parameters to internal atributes and computes how many chunks should be created per file."""  # pylint: disable=line-too-long
        super().__init__()
        self.__folder_path = folder_path
        self.__number_files = number_files
        self.__log_path = log_path
        self.__log_hash = log_hash
        self.__error_function = error_function
        self.__abort = False

        if size_unit == "KiB":
            size_mult = 1
        elif size_unit == "MiB":
            size_mult = 2
        elif size_unit == "GiB":
            size_mult = 3

        if chunk_unit == "KiB":
            chunk_mult = 1
        elif chunk_unit == "MiB":
            chunk_mult = 2
        elif chunk_unit == "GiB":
            chunk_mult = 3

        # Converts both values to bytes
        file_size_bytes = math.ceil(size_file * (1024**size_mult))
        self.__chunk_size_bytes = math.ceil(chunk_size * (1024**chunk_mult))

        # If the chunk size is too large, use the file size instead
        if file_size_bytes < self.__chunk_size_bytes:
            self.__chunk_size_bytes = file_size_bytes
            self.number_of_chunks = 1
        else:
            self.number_of_chunks = math.ceil(file_size_bytes / self.__chunk_size_bytes)

        if self.__log_path:
            self.__readable_size = f"{size_file}{size_unit}"
            if self.__log_path[-1] != "/":
                self.__log_path = f"{self.__log_path}/dummy-files-creator.csv"
            else:
                self.__log_path = f"{self.__log_path}/dummy-files-creator.csv"
            try:
                self.__logger = Logger(self.__log_path, self.__error_function)
            except IOError as error:
                if self.__error_function:
                    self.__error_function(f"Error saving log file: {error}")
                raise error

        self.n_created = 0
        self.file_name = ""
        self.chunk_n = 0
        self.complete = False

    def __write_log(self, file_path):
        try:
            with open(file_path, "rb") as fout:
                if self.__log_hash:
                    f_bytes = fout.read()
                    hash_result = hashlib.md5(f_bytes).hexdigest()
                    self.__logger.log(file_path, self.__readable_size, hash_result)
                else:
                    self.__logger.log(file_path, self.__readable_size, "")
            return True
        except IOError as error:
            if self.__error_function:
                self.__error_function(f"Error saving log: {error}")
            return False

    def __create_file(self, file_path):
        try:
            with open(file_path, "ab") as fout:
                for self.chunk_n in range(1, self.number_of_chunks + 1):
                    if self.__abort is True:
                        os.remove(file_path)
                        return False
                    fout.write(os.urandom(self.__chunk_size_bytes))
        except IOError as error:
            if self.__error_function:
                self.__error_function(f"Error creating file: {error}")
            return False
        return True

    def run(self):
        """Start file creation."""
        for self.n_created in range(1, self.__number_files + 1):
            self.file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.__folder_path}/{self.file_name}"
            if not self.__create_file(file_path):
                return False
            if self.__log_path:
                if not self.__write_log(file_path):
                    return False
            if self.__abort is True:
                return False
        self.complete = True
        return True

    def kill(self):
        """Set the abort flag to true, which will stop the thread execution loop."""
        self.__abort = True
