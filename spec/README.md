## Using PyInstaller to generate the packages

See [this guide](../src/README.md) to learn the prerequisites to run the python code.

To generate the packages, you must install `pyinstaller` using `pip`:

```
pip3 install pyinstaller
```

> Note that all commands must be run inside the `spec` folder due to the folder paths used.

### Windows

Having Python 3.7.0 (or later) and PyInstaller installed, you can create the `.exe` package:

```
pyinstaller --clean --windowed --onefile tfg_windows.spec
```

### Linux

Having Python 3.7.0 (or later) and PyInstaller, you can create the portable version of the app:

```
pyinstaller --clean --windowed tfg_linux.spec
```


### masOS

Having Python 3.7.0 (or later) and PyInstaller, you can create the portable version of the app:

```
pyinstaller --clean --windowed --onefile tfg_macos.spec
```