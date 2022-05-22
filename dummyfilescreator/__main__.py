#! /usr/bin/env python3
import sys
from .dfc_ui import DFCUi
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = DFCUi()
    app.exec_()


if __name__ == "__main__":
    main()
