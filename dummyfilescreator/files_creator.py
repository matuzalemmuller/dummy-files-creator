import hashlib
import math
import os
import threading
import uuid
from .logger import Logger

# import time # used for debugging


class FilesCreator(threading.Thread):
    __slots__ = (
        "folder_path",
        "number_files",
        "verbose",
        "log_path",
        "log_hash",
        "complete_function",
        "update_function",
        "error_function",
        "abort",
        "file_size_bytes",
        "chunk_size_bytes",
        "number_of_chunks",
        "readable_size",
        "logger",
    )

    def __init__(
        self,
        folder_path: str,
        number_files: int,
        size_file: int,
        size_unit: str,
        chunk_size: int,
        chunk_unit: str,
        verbose: bool = None,
        log_path: str = None,
        log_hash: bool = None,
        complete_function=None,
        update_function=None,
        error_function=None,
    ):
        super().__init__()
        self.folder_path = folder_path
        self.number_files = number_files
        self.verbose = verbose
        self.log_path = log_path
        self.log_hash = log_hash
        self.complete_function = complete_function
        self.update_function = update_function
        self.error_function = error_function
        self.abort = False

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
        self.file_size_bytes = math.ceil(size_file * (1024**size_mult))
        self.chunk_size_bytes = math.ceil(chunk_size * (1024**chunk_mult))

        # If the chunk size is too large, use the file size instead
        if self.file_size_bytes < self.chunk_size_bytes:
            self.chunk_size_bytes = self.file_size_bytes
            self.number_of_chunks = 1
        else:
            self.number_of_chunks = math.ceil(
                self.file_size_bytes / self.chunk_size_bytes
            )

        if self.log_path:
            self.readable_size = f"{size_file}{size_unit}"
            if self.log_path[-1] != "/":
                self.log_path = f"{self.log_path}/dummy-files-creator.csv"
            else:
                self.log_path = f"{self.log_path}/dummy-files-creator.csv"
            try:
                self.logger = Logger(self.log_path, self.error_function)
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error saving log file: {e}")
                raise e

    def __write_log(self, msg: str):
        try:
            with open(msg, "rb") as fout:
                if self.log_hash:
                    bytes = fout.read()
                    hash_result = hashlib.md5(bytes).hexdigest()
                    self.logger.log(msg, self.readable_size, hash_result)
                else:
                    self.logger.log(msg, self.readable_size, "")
        except IOError as e:
            if self.error_function:
                self.error_function(f"Error saving log: {e}")
            return False

        return True

    def __create_files(self):
        for _ in range(1, self.number_files + 1):
            file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.folder_path}/{file_name}"
            try:
                with open(file_path, "wb") as fout:
                    for _ in range(self.number_of_chunks):
                        if self.abort == True:
                            os.remove(file_path)
                            return False
                        fout.write(os.urandom(self.chunk_size_bytes))
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error creating file: {e}")
                return False
            if self.abort == True:
                return False

        if self.complete_function:
            self.complete_function()

        return True

    def __create_files_with_log(self):
        for _ in range(1, self.number_files + 1):
            file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.folder_path}/{file_name}"
            try:
                with open(file_path, "wb") as fout:
                    for _ in range(self.number_of_chunks):
                        if self.abort == True:
                            os.remove(file_path)
                            return False
                        fout.write(os.urandom(self.chunk_size_bytes))
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error creating file: {e}")
                return False
            if not self.__write_log(file_path):
                return False
            if self.abort == True:
                return False

        if self.complete_function:
            self.complete_function()

        return True

    def __create_files_with_progress(self):
        for n_created in range(1, self.number_files + 1):
            file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.folder_path}/{file_name}"
            try:
                with open(file_path, "wb") as fout:
                    for _ in range(self.number_of_chunks):
                        if self.abort == True:
                            os.remove(file_path)
                            return False
                        fout.write(os.urandom(self.chunk_size_bytes))
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error creating file: {e}")
                return False
            if self.abort == True:
                return False
            else:
                self.update_function(n_created, self.number_files, file_name, 1, 1)

        if self.complete_function:
            self.complete_function()

        return True

    def __create_files_with_progress_and_log(self):
        for n_created in range(1, self.number_files + 1):
            file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.folder_path}/{file_name}"
            try:
                with open(file_path, "wb") as fout:
                    for _ in range(self.number_of_chunks):
                        if self.abort == True:
                            os.remove(file_path)
                            return False
                        fout.write(os.urandom(self.chunk_size_bytes))
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error creating file: {e}")
                return False
            if not self.__write_log(file_path):
                return False
            if self.abort == True:
                return False
            else:
                self.update_function(n_created, self.number_files, file_name, 1, 1)

        if self.complete_function:
            self.complete_function()

        return True

    def __create_files_with_verbose(self):
        for n_created in range(1, self.number_files + 1):
            file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.folder_path}/{file_name}"
            try:
                with open(file_path, "wb") as fout:
                    for chunk_n in range(1, self.number_of_chunks + 1):
                        if self.abort == True:
                            os.remove(file_path)
                            return False
                        fout.write(os.urandom(self.chunk_size_bytes))
                        self.update_function(
                            n_created,
                            self.number_files,
                            file_name,
                            chunk_n,
                            self.number_of_chunks,
                        )
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error creating file: {e}")
                return False

            if self.abort == True:
                return False
            else:
                self.update_function(n_created, self.number_files, file_name, 1, 1)

        if self.complete_function:
            self.complete_function()

        return True

    def __create_files_with_verbose_and_log(self):
        for n_created in range(1, self.number_files + 1):
            file_name = f"{uuid.uuid4()}.dummy"
            file_path = f"{self.folder_path}/{file_name}"
            try:
                with open(file_path, "wb") as fout:
                    for chunk_n in range(1, self.number_of_chunks + 1):
                        if self.abort == True:
                            os.remove(file_path)
                            return False
                        fout.write(os.urandom(self.chunk_size_bytes))
                        self.update_function(
                            n_created,
                            self.number_files,
                            file_name,
                            chunk_n,
                            self.number_of_chunks,
                        )
            except IOError as e:
                if self.error_function:
                    self.error_function(f"Error creating file: {e}")
                return False
            if not self.__write_log(file_path):
                return False
            if self.abort == True:
                return False
            else:
                self.update_function(n_created, self.number_files, file_name, 1, 1)

        if self.complete_function:
            self.complete_function()

        return True

    def run(self):
        if self.update_function:
            if self.verbose:
                if self.log_path:
                    return self.__create_files_with_verbose_and_log()
                else:
                    return self.__create_files_with_verbose()
            else:
                if self.log_path:
                    return self.__create_files_with_progress_and_log()
                else:
                    return self.__create_files_with_progress()
        else:
            if self.log_path:
                return self.__create_files_with_log()
            else:
                return self.__create_files()

    def kill(self):
        self.abort = True
