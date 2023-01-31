#!/usr/bin/env python3
"""Author: Matuzalem (Mat) Muller.

License: GPLv3
"""
import argparse
import sys
import threading
import time
from tqdm import tqdm
from .files_creator import FilesCreator


class DFCCli:  # pylint: disable=too-many-instance-attributes
    """Class that provides CLI support."""

    __slots__ = (
        "__folder_path",
        "__number_files",
        "__size_file",
        "__size_unit",
        "__chunk_size",
        "__chunk_unit",
        "__verbose",
        "__progressbar",
        "__log_path",
        "__log_hash",
        "__pbar_total",
        "__pbar_file",
        "__files_creator",
        "__update_thread",
    )

    def __init__(self):  # pylint: disable=too-many-branches
        """Save arguments to internal atributes."""
        parser = argparse.ArgumentParser(
            description="""Application to generate dummy files. Run without arguments to start
            in GUI mode or include arguments to use CLI mode."""
        )
        parser.add_argument(
            "--output", "-o", required=True, help="Location where files will be created"
        )
        parser.add_argument(
            "--n-files",
            "-n",
            required=True,
            type=int,
            help="Number of files to be created",
        )
        parser.add_argument(
            "--size", "-fs", required=True, type=int, help="Size of files to be created"
        )
        parser.add_argument(
            "--unit",
            "-fu",
            required=True,
            help="Size unit. Accepted values: KiB, MiB, GiB",
        )
        parser.add_argument(
            "--chunk-size", "-cs", required=False, type=int, help="Chunk size"
        )
        parser.add_argument(
            "--chunk-unit",
            "-cu",
            required=False,
            help="Chunk size unit. Accepted values: KiB, MiB, GiB",
        )
        parser.add_argument(
            "--log", "-l", required=False, help="Saves log file. Affects performance"
        )
        parser.add_argument(
            "--hash",
            "-ha",
            action="store_true",
            required=False,
            help="Includes md5 hash in log file. Affects performance",
        )
        parser.add_argument(
            "--progressbar",
            "-p",
            action="store_true",
            required=False,
            help="Shows progress bar. Affects performance",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            required=False,
            help="Shows per-file progress bar. Affects performance",
        )
        args = vars(parser.parse_args())

        output = f"{args['output']}"
        if output[-1] == "/":
            output = output[:-1]
        elif output[-1] == "\\":
            output = output[:-1]
        self.__folder_path = output

        if args["n_files"] <= 0:
            parser.error("argument --n_files/-n must be greater than 0")
        self.__number_files = args["n_files"]

        if args["size"] <= 0:
            parser.error("argument --size/-fs must be greater than 0")
        self.__size_file = args["size"]

        if args["unit"] == "KiB" or args["unit"] == "MiB" or args["unit"] == "GiB":
            self.__size_unit = f"{args['unit']}"
        else:
            print(
                "Error: Acceptable values for --file-unit/-fu are 'KiB', 'MiB', and 'GiB'"
            )
            sys.exit(1)

        if args["chunk_size"] is not None and args["chunk_unit"] is not None:
            if (
                args["chunk_unit"] == "KiB"
                or args["chunk_unit"] == "MiB"
                or args["chunk_unit"] == "GiB"
            ):
                if args["chunk_size"] <= 0:
                    parser.error("argument --chunk-size/-cs must be greater than 0")
                self.__chunk_size = args["chunk_size"]
                self.__chunk_unit = f"{args['chunk_unit']}"
            else:
                print(
                    "Error: Acceptable values for --chunk-unit/-cu are 'KiB', 'MiB', and 'GiB'"
                )
                sys.exit(1)
        else:
            self.__chunk_size = 1024
            self.__chunk_unit = "KiB"

        if args["verbose"] is not None:
            self.__verbose = bool(args["verbose"])
        else:
            self.__verbose = None

        if args["progressbar"] is not None:
            self.__progressbar = bool(args["progressbar"])
        else:
            self.__progressbar = None

        if args["log"] is not None:
            log = f"{args['log']}"
            if log[-1] == "/":
                log = log[:-1]
            elif log[-1] == "\\":
                log = log[:-1]
            self.__log_path = log
        else:
            self.__log_path = None

        if args["hash"] is not None:
            self.__log_hash = bool(args["hash"])
        else:
            self.__log_hash = None

        self.__files_creator = None
        self.__pbar_total = None
        self.__pbar_file = None
        self.__update_thread = None

    def error_function(self, error_message: str):
        """Display message when an error happens during file creation."""
        if self.__pbar_total is not None:
            self.__pbar_total.close()
        if self.__pbar_file is not None:
            self.__pbar_file.close()
        print("\r" + error_message)
        sys.exit(1)

    def __update_cli_progress(self):
        while self.__files_creator.is_alive():
            self.__pbar_total.n = self.__files_creator.n_created - 1
            self.__pbar_total.refresh()
            if self.__verbose:
                self.__pbar_file.n = self.__files_creator.chunk_n
                self.__pbar_file.set_description(f"{self.__files_creator.file_name}")
                self.__pbar_file.refresh()
            time.sleep(0.1)
        self.__pbar_total.close()
        if self.__pbar_file is not None:
            self.__pbar_file.close()
        print(f"\r{self.__number_files} file(s) created in {self.__folder_path}")
        if self.__log_path is not None:
            print(f"Log file saved to {self.__log_path}")

    def run(self):
        """Start the file creation process."""
        try:
            self.__files_creator = FilesCreator(
                folder_path=self.__folder_path,
                number_files=self.__number_files,
                size_file=self.__size_file,
                size_unit=self.__size_unit,
                chunk_size=self.__chunk_size,
                chunk_unit=self.__chunk_unit,
                log_path=self.__log_path,
                log_hash=self.__log_hash,
                error_function=self.error_function,
            )
            if self.__progressbar or self.__verbose:
                self.__pbar_total = tqdm(
                    range(self.__number_files), unit=" files", leave=False
                )
                if self.__verbose:
                    self.__pbar_file = tqdm(
                        range(self.__files_creator.number_of_chunks),
                        unit=" chunks",
                        leave=False,
                    )
            self.__files_creator.start()
            if self.__progressbar or self.__verbose:
                self.__update_thread = threading.Thread(
                    target=self.__update_cli_progress
                )
                self.__update_thread.start()
        except IOError as error:
            print(f"CLI: Error starting FilesCreator thread: {error}")
            sys.exit(1)


def main():
    """Entrypoint in case this file is executed directly."""
    app = DFCCli()
    app.run()


if __name__ == "__main__":
    main()
