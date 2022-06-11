#! /usr/bin/env python3
import sys


def main():
    if len(sys.argv) == 1:
        from .dfc_ui import DFCUi
        from PyQt5.QtWidgets import QApplication

        app = QApplication(sys.argv)
        window = DFCUi()
        app.exec_()
    else:
        from .dfc_cli import DFCCli

        app = DFCCli()
        app.run()


if __name__ == "__main__":
    main()
