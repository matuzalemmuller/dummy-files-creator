# Building the Windows executable

## Prerequisites

* [Python 3.6 or later](https://www.python.org/downloads/release/python-360/) & [PyInstaller](https://pypi.org/project/pyinstaller/)

## Instructions

For the standalone executable, run:

```
pyinstaller windows-onefile.spec
```

For the build with multiple files, run:

```
pyinstaller windows-dir.spec
```
