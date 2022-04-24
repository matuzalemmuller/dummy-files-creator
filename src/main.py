#!/usr/bin/env python3

from files_creator import FilesCreator

def main():
    f = FilesCreator()
    f.create_files(path="/home/matuzalem/dev/dummy-files-creator/dist",
             number_files=10,
             size_file=200,
             size_unit="KiB",
             chunk_size=1024,
             chunk_unit="KiB")

if __name__ == "__main__":
    main()
