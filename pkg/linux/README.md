# Building the linux package

## Prerequisites

*   A linux-based OS with dpkg or rpm-based package manager
*   [Python 3.6 or later](https://www.python.org/downloads/release/python-360/) & [PyInstaller](https://pypi.org/project/pyinstaller/)
*   The requirements at the root of the repository ([`requirements.txt`](../../requirements.txt))
*   [Ruby 2.7](https://www.ruby-lang.org/en/) & [fpm](https://fpm.readthedocs.io/en/latest/index.html)

## Instructions

Run `python3 build_package.py`, and the `.deb`/`.rpm` package will be generated in this folder.

*   dpkg-based systems will generate the `.deb` packages, and systems with the `rpm` package manager will create the `.rpm` packages.
