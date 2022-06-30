#!/usr/bin/env python3
"""Author: Matuzalem (Mat) Muller.

License: GPLv3
"""
import sys


def main():
    """Entrypoint.

    If no parameters are provided, start in GUI mode. Otherwise,
    run in CLI mode. The imports are done according to the execution mode: if
    CLI mode is used it is not necessary to import all the PyQt libraries.
    """
    if len(sys.argv) == 1:
        from .dfc_ui import DFCUi
        from PyQt5.QtWidgets import QApplication

        app = QApplication(sys.argv)
        window = DFCUi()
        window.show()
        app.exec_()
    else:
        from .dfc_cli import DFCCli

        app = DFCCli()
        app.run()


if __name__ == "__main__":
    main()
