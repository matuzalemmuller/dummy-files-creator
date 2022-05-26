#! /usr/bin/env python3
import sys
from .dfc_ui import DFCUi
from .dfc_cli import DFCCli
from PyQt5.QtWidgets import QApplication


def main():
    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        window = DFCUi()
        app.exec_()
    else:
        app = DFCCli()
        app.run()


if __name__ == "__main__":
    main()
