#! /usr/bin/env python3
import sys
from .ui import Ui
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == "__main__":
    main()
