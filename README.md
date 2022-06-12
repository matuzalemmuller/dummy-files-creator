# Dummy Files Creator

![Unit tests](https://github.com/matuzalemmuller/dummy-files-creator/actions/workflows/unit-tests.yml/badge.svg)

Application to generate dummy files with random content and different checksums. **All sizes are considered as corresponding powers of 2<sup>10</sup> [(KiB, MiB, GiB)](https://en.wikipedia.org/wiki/Orders_of_magnitude_(data))**.

See the project in [GitHub](https://github.com/matuzalemmuller/dummy-files-creator) and [PyPi](https://pypi.org/project/dummyfilescreator/).

## Installation

### Cross-platform

Install the package via pip:

```
pip3 install dummyfilescreator
```

### Windows

Download the latest release from the [releases page](https://github.com/matuzalemmuller/dummy-files-creator/releases).
* The build tagged as `dir` has all dlls and the `dummyfilescreator.exe` executable and is faster to start.
* The build tagged as `one-file` has a single executable, [but it takes longer to start](https://pyinstaller.org/en/stable/operating-mode.html#bundling-to-one-file).

### Linux

Download the `.deb` and `.rpm` packages from the [releases page](https://github.com/matuzalemmuller/dummy-files-creator/releases).

### macOS

Download the latest `.dmg` file from the [releases page](https://github.com/matuzalemmuller/dummy-files-creator/releases). Note that at the moment there are no `arm`-compatible packages due to the lack of devices to build the app. Contributions are welcome.
