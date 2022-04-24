import os
import math
import uuid

# Exceptions:
# * Ao criar os arquivos (automatico)
# * Ao criar o arquivo de log (automatico)
# * Ao validar as unidades

class FilesCreator:
    def create_files(
        self,
        path: str,
        number_files: int,
        size_file: int,
        size_unit: str,
        chunk_size: int,
        chunk_unit: str,
    ):
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
        file_size_bytes = math.ceil(size_file * (1024**size_mult))
        chunk_size_bytes = math.ceil(chunk_size * (1024**chunk_mult))

        # If the chunk size is too large, use the file size instead
        if file_size_bytes < chunk_size_bytes:
            chunk_size_bytes = file_size_bytes
            number_of_chunks = 1
        else:
            number_of_chunks = math.ceil(file_size_bytes / chunk_size_bytes)

        print("file_size_bytes: " + str(file_size_bytes))
        print("chunk_size_bytes: " + str(chunk_size_bytes))
        print("number_of_chunks: " + str(number_of_chunks))

        created_files = 0
        while created_files < number_files:
            file_name = str(uuid.uuid4()) + ".dummy"
            try:
                with open(path + "/" + file_name, "wb") as fout:
                    for iter in range(number_of_chunks):
                        fout.write(os.urandom(chunk_size_bytes))
            except IOError as e:
                print(e)
                return
            created_files += 1

        return True
