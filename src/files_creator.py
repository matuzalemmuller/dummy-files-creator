from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
import os
import math
import uuid
import time

# Exceptions:
# * Ao criar os arquivos (automatico)
# * Ao criar o arquivo de log (automatico)
# * Ao validar as unidades


class FilesCreator(QObject):
    update_progress = pyqtSignal(int, int, str, int, int)

    def __init__(self,
        folder_path: str,
        number_files: int,
        size_file: int,
        size_unit: str,
        chunk_size: int,
        chunk_unit: str,
        debug: bool = None,
        log_path: str = None,
    ):
        super().__init__()
        self.folder_path = folder_path
        self.number_files = number_files
        self.debug = debug
        # self.log_path = log_path

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
            self.number_of_chunks = math.ceil(self.file_size_bytes / self.chunk_size_bytes)

    @pyqtSlot()
    def create_files(self):
        for n_created in range(1, self.number_files+1):
            file_name = str(uuid.uuid4()) + ".dummy"
            try:
                with open(self.folder_path + "/" + file_name, "wb") as fout:
                    if self.debug:
                        for chunk_n in range(1, self.number_of_chunks+1):
                            if self.abort == True:
                                os.remove(self.folder_path + "/" + file_name)
                                return
                            fout.write(os.urandom(self.chunk_size_bytes))
                            self.update_progress.emit(
                                n_created,
                                self.number_files,
                                file_name,
                                chunk_n,
                                self.number_of_chunks,
                            )
                    else:
                        for chunk_n in range(self.number_of_chunks):
                            if self.abort == True:
                                os.remove(self.folder_path + "/" + file_name)
                                return
                            fout.write(os.urandom(self.chunk_size_bytes))
            except IOError as e:
                print(e)
                return
            time.sleep(1)
        self.update_progress.emit(n_created, self.number_files, file_name, 1, 1)
        return True

    def abort(self):
        self.abort = True
