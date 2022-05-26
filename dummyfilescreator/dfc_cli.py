import argparse
import sys
from .files_creator import FilesCreator
from tqdm import tqdm


class DFCCli:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--output", "-o", required=True, help="Location where files will be created"
        )
        parser.add_argument(
            "--n-files", "-n", required=True, help="Number of files to be created"
        )
        parser.add_argument(
            "--size", "-fs", required=True, help="Size of files to be created"
        )
        parser.add_argument(
            "--unit",
            "-fu",
            required=True,
            help="Size unit. Accepted values: KiB, MiB, GiB",
        )
        parser.add_argument("--chunk-size", "-cs", required=False, help="Chunk size")
        parser.add_argument(
            "--chunk-unit",
            "-cu",
            required=False,
            help="Chunk size unit. Accepted values: KiB, MiB, GiB",
        )
        parser.add_argument("--debug", "-d", required=False)
        parser.add_argument("--log", "-l", required=False)
        parser.add_argument("--hash", "-ha", required=False)

        args = vars(parser.parse_args())

        self.folder_path = str(args["output"])
        self.number_files = int(args["n_files"])
        self.size_file = int(args["size"])
        if args["unit"] == "KiB" or args["unit"] == "MiB" or args["unit"] == "GiB":
            self.size_unit = str(args["unit"])
        else:
            print(
                "Error: Acceptable values for --file-unit/-fu are 'KiB', 'MiB', and 'GiB'"
            )
            sys.exit(1)

        if args["chunk_size"] != None and args["chunk_unit"] != None:
            if (
                args["chunk_unit"] == "KiB"
                or args["chunk_unit"] == "MiB"
                or args["chunk_unit"] == "GiB"
            ):
                self.chunk_size = int(args["chunk_size"])
                self.chunk_unit = str(args["chunk_unit"])
            else:
                print(
                    "Error: Acceptable values for --chunk-unit/-cu are 'KiB', 'MiB', and 'GiB'"
                )
                sys.exit(1)
        else:
            self.chunk_size = 1024
            self.chunk_unit = "KiB"

        if args["debug"] != None:
            self.debug = bool(args["debug"])
        else:
            self.debug = None
        if args["log"] != None:
            self.log_path = str(args["log"])
        else:
            self.log_path = None
        if args["hash"] != None:
            self.log_hash = str(args["hash"])
        else:
            self.log_hash = None

        self.files_creator = None

        self.pbar_total = tqdm(range(self.number_files), unit=" files")

        if self.debug:
            self.pbar_file = tqdm(range(100), unit=" chunks")

    def print_progress(
        self,
        n_created: int,
        number_files: int,
        file_name: str,
        chunk_n: int,
        number_of_chunks: int,
    ):
        self.pbar_total.n = n_created
        self.pbar_total.refresh()
        if self.debug:
            debug_percent = int(chunk_n * 100 / number_of_chunks)
            self.pbar_file.n = debug_percent
            self.pbar_file.set_description("%s" % file_name)
            self.pbar_file.refresh()

    def error_function(self, error_message: str):
        print(error_message)
        sys.exit(1)

    def run(self):
        try:
            self.files_creator = FilesCreator(
                folder_path=self.folder_path,
                number_files=self.number_files,
                size_file=self.size_file,
                size_unit=self.size_unit,
                chunk_size=self.chunk_size,
                chunk_unit=self.chunk_unit,
                debug=self.debug,
                log_path=self.log_path,
                log_hash=self.log_hash,
                update_function=self.print_progress,
                error_function=self.error_function,
            )
            self.files_creator.start()
        except IOError as e:
            print("CLI: Error starting FilesCreator thread: " + str(e))
            sys.exit(1)
