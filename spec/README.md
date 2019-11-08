## Using PyInstaller to generate the packages

Install the dependencies:

```
pip3 install -r ../requirements.txt
```

> Note that all commands must be run inside the `spec` folder due to the folder paths used.

### Windows

Having Python 3.7.0 (or later) and PyInstaller installed, you can create the `.exe` package:

```
pyinstaller --clean --windowed --onefile windows.spec
```

### macOS

Having Python 3.7.0 (or later) and PyInstaller, you can create the portable version of the app:

```
pyinstaller --clean --windowed --onefile macos.spec
```