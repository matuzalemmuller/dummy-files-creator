import hashlib
import math
import os
import threading
import time
import uuid
from .logger import Logger


class FilesCreator(threading.Thread):
    def __init__(
        self,
        folder_path: str,
        number_files: int,
        size_file: int,
        size_unit: str,
        chunk_size: int,
        chunk_unit: str,
        debug: bool = None,
        log_path: str = None,
        log_hash: bool = None,
        complete_function=None,
        update_function=None,
        error_function=None,
    ):
        super().__init__()
        self.folder_path = folder_path
        self.number_files = number_files
        self.debug = debug
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
            size_mult = 2
        else:
            return False

        if chunk_unit == "KiB":
            chunk_mult = 1
        elif chunk_unit == "MiB":
            chunk_mult = 2
        elif chunk_unit == "GiB":
            chunk_mult = 3
        else:
            return False

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
            self.readable_size = str(size_file) + size_unit
            if self.log_path[-1] != "/":
                self.log_path = self.log_path + "/dummy-files-creator.csv"
            else:
                self.log_path = self.log_path + "dummy-files-creator.csv"
            try:
                self.logger = Logger(self.log_path, self.error_function)
            except IOError as e:
                print("FilesCreator: Error creating Logger: " + str(e))
                self.error_function("Error saving log file: " + str(e))
                raise e

    def run(self):
        for n_created in range(1, self.number_files + 1):
            file_name = str(uuid.uuid4()) + ".dummy"
            file_path = self.folder_path + "/" + file_name
            try:
                with open(file_path, "wb") as fout:
                    if self.debug:
                        for chunk_n in range(1, self.number_of_chunks + 1):
                            if self.abort == True:
                                os.remove(file_path)
                                return False
                            fout.write(os.urandom(self.chunk_size_bytes))
                            if self.update_function:
                                self.update_function(
                                    n_created,
                                    self.number_files,
                                    file_name,
                                    chunk_n,
                                    self.number_of_chunks,
                                )
                    else:
                        for chunk_n in range(self.number_of_chunks):
                            if self.abort == True:
                                os.remove(file_path)
                                return False
                            fout.write(os.urandom(self.chunk_size_bytes))
            except IOError as e:
                print(e)
                if self.error_function:
                    self.error_function("Error creating file: " + str(e))
                return False
            if self.log_path:
                try:
                    with open(file_path, "rb") as fout:
                        if self.log_hash:
                            bytes = fout.read()
                            hash_result = hashlib.md5(bytes).hexdigest()
                            self.logger.log(file_path, self.readable_size, hash_result)
                        else:
                            self.logger.log(file_path, self.readable_size, "")
                except IOError as e:
                    print("Files Creator: error logging entry: " + str(e))
                    self.error_function("Error saving log: " + str(e))
                    return False
            time.sleep(1)
            if self.abort == True:
                return False
            else:
                if self.update_function:
                    self.update_function(n_created, self.number_files, file_name, 1, 1)

        if self.complete_function:
            self.complete_function()

        return True

    def kill(self):
        self.abort = True
