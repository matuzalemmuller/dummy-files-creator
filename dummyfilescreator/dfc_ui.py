#!/usr/bin/env python3
"""Author: Matuzalem (Mat) Muller.

License: GPLv3
"""
import sys
import threading
import time
from PyQt5.QtCore import (  # pylint: disable=no-name-in-module
    pyqtSignal,
    pyqtSlot,
    QRegExp,
    Qt,
)
from PyQt5.QtGui import QIcon, QRegExpValidator  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import (  # pylint: disable=no-name-in-module
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)
from .files_creator import FilesCreator
from .qt_about_window import UiAbout
from .qt_main_window import UiMainWindow
from . import qt_icon  # pylint: disable=unused-import


class About(QDialog):
    """Displays About window."""

    __slots__ = "__about_window"

    def __init__(self):
        """Import Qt resource for icon and display the QDialog."""
        super().__init__()
        self.__about_window = UiAbout()
        self.__about_window.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.exec_()
        self.activateWindow()


class DFCUi(QMainWindow):
    """Launch application window."""

    __slots__ = ("__main_window", "__creator_thread", "__update_thread")

    signal_update_progress = pyqtSignal(int, str, int)
    signal_error = pyqtSignal(str)
    signal_complete = pyqtSignal()

    def __init__(self):
        """Import Qt resource for icon and window UI, connect signals and display window."""
        super().__init__()
        self.__main_window = UiMainWindow()
        self.__main_window.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.__creator_thread = None
        self.__update_thread = None
        # Initialize UI elements
        self.__set_number_validator()
        self.__set_connect()
        self.__enable_create_button()
        self.__change_ui("enabled")
        self.show()

    def __about_action(self):
        About()

    def __set_connect(self):
        self.__main_window.button_browse_files.clicked.connect(
            self.__click_button_browse_files
        )
        self.__main_window.button_browse_log.clicked.connect(
            self.__click_button_browse_log
        )
        self.__main_window.text_path.textChanged.connect(self.__enable_create_button)
        self.__main_window.text_n_files.textChanged.connect(self.__enable_create_button)
        self.__main_window.text_size_files.textChanged.connect(
            self.__enable_create_button
        )
        self.__main_window.text_chunk_size.textChanged.connect(
            self.__enable_create_button
        )
        self.__main_window.text_logfilepath.textChanged.connect(
            self.__enable_create_button
        )
        self.__main_window.checkbox_savelog.stateChanged.connect(
            self.__enable_create_button
        )
        self.__main_window.button_create_stop.clicked.connect(
            self.__click_button_create_stop
        )
        self.__main_window.button_close_quit.clicked.connect(
            self.__click_button_close_quit
        )
        self.__main_window.checkbox_savelog.stateChanged.connect(
            self.__hide_widget_log_options
        )
        self.__main_window.action_about.triggered.connect(self.__about_action)
        self.__main_window.text_path.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.__main_window.text_n_files.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.__main_window.text_size_files.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.__main_window.text_chunk_size.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.signal_update_progress.connect(self.__update_progress_bar)
        self.signal_complete.connect(self.__display_success_message)
        self.signal_error.connect(self.__display_error_message)

    def __set_number_validator(self):
        number_regex = QRegExp("[0-9]+")
        number_validator = QRegExpValidator(number_regex)
        self.__main_window.text_n_files.setValidator(number_validator)
        self.__main_window.text_size_files.setValidator(number_validator)
        self.__main_window.text_chunk_size.setValidator(number_validator)

    def __enable_create_button(self):
        if (
            len(self.__main_window.text_path.text()) > 0
            and len(self.__main_window.text_n_files.text()) > 0
            and len(self.__main_window.text_size_files.text()) > 0
            and len(self.__main_window.text_chunk_size.text()) > 0
            and (
                self.__main_window.checkbox_savelog.isChecked()
                and len(self.__main_window.text_logfilepath.text()) > 0
                or not (self.__main_window.checkbox_savelog.isChecked())
            )
        ):
            self.__main_window.button_create_stop.setDisabled(False)
        else:
            self.__main_window.button_create_stop.setDisabled(True)

    @pyqtSlot(int, str, int)
    def __update_progress_bar(
        self,
        created_files: int,
        file_name: str = None,
        current_chunk: int = None,
    ):
        self.__main_window.label_progress.setText(
            f"{created_files}/{self.__main_window.text_n_files.text()}"
        )
        self.__main_window.progress_bar.setValue(created_files)
        if self.__main_window.checkbox_verbose.isChecked():
            self.__main_window.label_verbose_information.setText(
                f"Creating {file_name}"
            )
            self.__main_window.progress_bar_verbose.setValue(current_chunk)

    @pyqtSlot(str)
    def __display_error_message(self, error_message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setWindowIcon(QIcon(":/icon.png"))
        msg.setText("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDetailedText(error_message)
        msg.exec_()
        self.__change_ui("enabled")

    @pyqtSlot()
    def __display_success_message(self):
        self.__change_ui(state="enabled")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setWindowIcon(QIcon(":/icon.png"))
        msg.setText("Success")
        msg.setInformativeText("Files created!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def emit_error_window(self, error_message: str):
        """Emit signal to display message when an error happens during file creation.

        The signal invokes the method self.__display_error_message
        This function is necessary because files_creator does not emit signals
        and it cannot draw/modify the QMainWindow from this class.
        """
        self.signal_error.emit(error_message)
        self.__creator_thread = None
        self.__update_thread = None

    def __update_ui_progress(self):
        while self.__creator_thread.is_alive():
            self.signal_update_progress.emit(
                self.__creator_thread.n_created - 1,
                self.__creator_thread.file_name,
                self.__creator_thread.chunk_n,
            )
            time.sleep(0.1)
        if self.__creator_thread.complete:
            self.signal_complete.emit()
        self.__creator_thread = None
        self.__update_thread = None

    def __hide_widget_log_options(self):
        if self.__main_window.checkbox_savelog.isChecked():
            self.__main_window.widget_log.show()
        else:
            self.__main_window.widget_log.hide()

    def __click_button_browse_files(self):
        dialog = QFileDialog()
        path = f"{QFileDialog.getExistingDirectory(dialog, 'Select Directory')}"
        self.__main_window.text_path.setText(path)

    def __click_button_browse_log(self):
        dialog = QFileDialog()
        path = f"{QFileDialog.getExistingDirectory(dialog, 'Select Directory')}"
        self.__main_window.text_logfilepath.setText(path)

    def __click_button_close_quit(self):
        if self.__main_window.button_close_quit.text() == "Quit":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Quit")
            msg.setText("Are you sure you want to quit?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            quit_code = msg.exec_()
            if quit_code == QMessageBox.Yes:
                self.__creator_thread.kill()
                sys.exit(0)
        else:
            sys.exit(0)

    def __click_button_create_stop(self):  # pylint: disable=too-many-branches
        if (
            len(self.__main_window.text_path.text()) <= 0
            or len(self.__main_window.text_n_files.text()) <= 0
            or len(self.__main_window.text_size_files.text()) <= 0
            or len(self.__main_window.text_chunk_size.text()) <= 0
        ):
            return
        if (
            self.__main_window.checkbox_savelog.isChecked()
            and len(self.__main_window.text_logfilepath.text()) <= 0
        ):
            return
        if self.__main_window.button_create_stop.text() == "Create":
            size_file = int(self.__main_window.text_size_files.text())
            chunk_size = int(self.__main_window.text_chunk_size.text())
            if self.__main_window.text_path.text()[-1] == "/":
                path = self.__main_window.text_path.text()[:-1]
            elif self.__main_window.text_path.text()[-1] == "\\":
                path = self.__main_window.text_path.text()[:-1]
            else:
                path = self.__main_window.text_path.text()
            if self.__main_window.checkbox_savelog.isChecked():
                if self.__main_window.text_logfilepath.text()[-1] == "/":
                    log_path = self.__main_window.text_logfilepath.text()[:-1]
                elif self.__main_window.text_logfilepath.text()[-1] == "\\":
                    log_path = self.__main_window.text_logfilepath.text()[:-1]
                else:
                    log_path = self.__main_window.text_logfilepath.text()
            else:
                log_path = None
            try:
                print(log_path)
                self.__creator_thread = FilesCreator(
                    folder_path=path,
                    number_files=int(self.__main_window.text_n_files.text()),
                    size_file=size_file,
                    size_unit=self.__main_window.combo_file_unit.currentText(),
                    chunk_size=chunk_size,
                    chunk_unit=self.__main_window.combo_chunk_unit.currentText(),
                    log_path=log_path,
                    log_hash=self.__main_window.checkbox_md5hash.isChecked(),
                    error_function=self.emit_error_window,
                )

                self.__main_window.progress_bar.setMaximum(
                    int(self.__main_window.text_n_files.text())
                )
                self.__main_window.progress_bar_verbose.setMaximum(
                    self.__creator_thread.number_of_chunks
                )
                self.__main_window.label_progress.setText(
                    f"0/{self.__main_window.text_n_files.text()}"
                )

                self.__update_thread = threading.Thread(
                    target=self.__update_ui_progress
                )
                self.__creator_thread.start()
                self.__update_thread.start()
            except IOError as error:
                print(f"UI: Error starting FilesCreator thread: {error}")
                return
            self.__change_ui(state="disabled")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Confirmation")
            msg.setText("Are you sure?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            cancel_code = msg.exec_()
            if cancel_code == QMessageBox.Yes:
                self.__creator_thread.kill()
                self.__change_ui(state="enabled")

    def __change_ui(self, state: str):  # pylint: disable=too-many-statements
        if state == "disabled":
            self.__main_window.label_path.setDisabled(True)
            self.__main_window.label_n_files.setDisabled(True)
            self.__main_window.label_size_files.setDisabled(True)
            self.__main_window.label_logfilepath.setDisabled(True)
            self.__main_window.label_verbose_information.setDisabled(True)
            self.__main_window.text_path.setDisabled(True)
            self.__main_window.text_n_files.setDisabled(True)
            self.__main_window.text_size_files.setDisabled(True)
            self.__main_window.text_chunk_size.setDisabled(True)
            self.__main_window.text_logfilepath.setDisabled(True)
            self.__main_window.button_browse_files.setDisabled(True)
            self.__main_window.button_browse_log.setDisabled(True)
            self.__main_window.checkbox_verbose.setDisabled(True)
            self.__main_window.checkbox_savelog.setDisabled(True)
            self.__main_window.checkbox_md5hash.setDisabled(True)
            self.__main_window.combo_file_unit.setDisabled(True)
            self.__main_window.combo_chunk_unit.setDisabled(True)
            self.__main_window.button_create_stop.setText("Stop")
            self.__main_window.button_close_quit.setText("Quit")
            self.__main_window.widget_progress_bar.show()
            if self.__main_window.checkbox_verbose.isChecked():
                self.__main_window.widget_verbose.show()
            if self.__main_window.checkbox_savelog.isChecked():
                self.__main_window.widget_log.show()
            else:
                self.__main_window.widget_log.hide()
        else:
            self.__main_window.label_path.setDisabled(False)
            self.__main_window.label_n_files.setDisabled(False)
            self.__main_window.label_size_files.setDisabled(False)
            self.__main_window.label_logfilepath.setDisabled(False)
            self.__main_window.label_verbose_information.setDisabled(False)
            self.__main_window.text_path.setDisabled(False)
            self.__main_window.text_n_files.setDisabled(False)
            self.__main_window.text_size_files.setDisabled(False)
            self.__main_window.text_chunk_size.setDisabled(False)
            self.__main_window.text_logfilepath.setDisabled(False)
            self.__main_window.button_browse_files.setDisabled(False)
            self.__main_window.button_browse_log.setDisabled(False)
            self.__main_window.checkbox_verbose.setDisabled(False)
            self.__main_window.checkbox_savelog.setDisabled(False)
            self.__main_window.checkbox_md5hash.setDisabled(False)
            self.__main_window.combo_file_unit.setDisabled(False)
            self.__main_window.combo_chunk_unit.setDisabled(False)
            self.__main_window.button_create_stop.setText("Create")
            self.__main_window.button_close_quit.setText("Close")
            self.__main_window.progress_bar.setValue(0)
            self.__main_window.progress_bar_verbose.setValue(0)
            self.__main_window.label_progress.setText("0/0")
            self.__main_window.widget_progress_bar.hide()
            self.__main_window.widget_verbose.hide()
            if self.__main_window.checkbox_savelog.isChecked():
                self.__main_window.widget_log.show()
            else:
                self.__main_window.widget_log.hide()


def main():
    """Entrypoint in case this file is executed directly."""
    app = QApplication(sys.argv)
    window = DFCUi()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
