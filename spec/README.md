## Using PyInstaller to generate the packages

See [this guide](../src/README.md) to learn the prerequisites to run the python code.

To generate the packages, you must install `pyinstaller` using `pip`:

```
pip3 install pyinstaller
```

> Note that all commands must be run inside the `spec` folder due to the folder paths used.

### Windows

Having Python 3 and PyInstaller installed, you can create the `.exe` package:

```
pyinstaller --clean --windowed --hidden-import tkinter --onefile tfg_windows.spec
```

### Linux

Having Python 3 and PyInstaller installed, you can create the portable version of the app:

```
pyinstaller --clean --windowed --hidden-import tkinter --onefile tfg_linux.spec
```


### masOS

Having Python 3 and PyInstaller installed, you can create the portable version of the app:

```
pyinstaller --clean --windowed --hidden-import tkinter --onefile tfg_macos.spec
```

After creating the `.pkg` file and the folder with all the libraries, it may be necessary to import the `tk` framework inside the app. This happens because PyInstaller may fail importing the `tk` libraries, so that must be done manually. The steps on how to import the framework are outlined below:

* Create folders inside the `Test Files Generator.app` package and the `test-files-generator-darwin` folder for `tk` and `tcl`:

```
mkdir dist/Test\ Files\ Generator.app/Contents/MacOS/tk
mkdir dist/Test\ Files\ Generator.app/Contents/MacOS/tcl
```
```
mkdir dist/test-files-generator-darwin/tk
mkdir dist/test-files-generator-darwin/tcl
```

* Copy the frameworks inside the folders (replace `<version>` by the version of Tcl installed in your Mac):

```
cp  /System/Library/Frameworks/Tk.framework/Tk \
    dist/Test\ Files\ Generator.app/Contents/MacOS/tk

cp  /System/Library/Frameworks/Tcl.framework/Versions/<version>/Tcl \
    dist/Test\ Files\ Generator.app/Contents/MacOS/tcl
```
```
cp  /System/Library/Frameworks/Tk.framework/Tk \
    dist/test-files-generator-darwin/Contents/MacOS/tk

cp  /System/Library/Frameworks/Tcl.framework/Versions/<version>/Tcl \
    dist/test-files-generator-darwin/Contents/MacOS/tcl
```

You should now be able to run the `Test Files Generator.app` application and the `test-files-generator-darwin` executable.