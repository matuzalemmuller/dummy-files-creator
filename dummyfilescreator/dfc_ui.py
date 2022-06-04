#! /usr/bin/env python3
import math
import sys
from . import qt_icon
from .files_creator import FilesCreator
from .qt_main_window import UiMainWindow
from .qt_about_window import UiAbout
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRegExp, Qt
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QMessageBox


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.about_window = UiAbout()
        self.about_window.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.exec_()
        self.activateWindow()


class DFCUi(QMainWindow):
    signal_update_progress = pyqtSignal(int, int, str, int, int)
    signal_error = pyqtSignal(str)
    signal_complete = pyqtSignal()

    def __init__(self):
        super(DFCUi, self).__init__()
        self.main_window = UiMainWindow()
        self.main_window.setupUi(self)
        self.setWindowIcon(QIcon(":/icon.png"))
        self.__creator_thread = None
        # Initialize UI elements
        self.__set_number_validator()
        self.__set_connect()
        self.__enable_create_button()
        self.__change_ui("enabled")
        self.show()  # Show the GUI

    def __about_action(self):
        About()

    def __set_connect(self):
        self.main_window.button_browse_files.clicked.connect(
            self.__click_button_browse_files
        )
        self.main_window.button_browse_log.clicked.connect(
            self.__click_button_browse_log
        )
        self.main_window.text_path.textChanged.connect(self.__enable_create_button)
        self.main_window.text_n_files.textChanged.connect(self.__enable_create_button)
        self.main_window.text_size_files.textChanged.connect(
            self.__enable_create_button
        )
        self.main_window.text_chunk_size.textChanged.connect(
            self.__enable_create_button
        )
        self.main_window.text_logfilepath.textChanged.connect(
            self.__enable_create_button
        )
        self.main_window.checkbox_savelog.stateChanged.connect(
            self.__enable_create_button
        )
        self.main_window.button_create_stop.clicked.connect(
            self.__click_button_create_stop
        )
        self.main_window.button_close_quit.clicked.connect(
            self.__click_button_close_quit
        )
        self.main_window.checkbox_savelog.stateChanged.connect(
            self.__hide_widget_log_options
        )
        self.main_window.action_about.triggered.connect(self.__about_action)
        self.main_window.text_path.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.main_window.text_n_files.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.main_window.text_size_files.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.main_window.text_chunk_size.returnPressed.connect(
            self.__click_button_create_stop
        )
        self.signal_update_progress.connect(self.__update_progress_bar)
        self.signal_complete.connect(self.__display_success_message)
        self.signal_error.connect(self.__display_error_message)

    def __set_number_validator(self):
        number_regex = QRegExp("[0-9]+")
        number_validator = QRegExpValidator(number_regex)
        self.main_window.text_n_files.setValidator(number_validator)
        self.main_window.text_size_files.setValidator(number_validator)
        self.main_window.text_chunk_size.setValidator(number_validator)

    def __enable_create_button(self):
        if (
            len(self.main_window.text_path.text()) > 0
            and len(self.main_window.text_n_files.text()) > 0
            and len(self.main_window.text_size_files.text()) > 0
            and len(self.main_window.text_chunk_size.text()) > 0
            and (
                self.main_window.checkbox_savelog.isChecked()
                and len(self.main_window.text_logfilepath.text()) > 0
                or not (self.main_window.checkbox_savelog.isChecked())
            )
        ):
            self.main_window.button_create_stop.setDisabled(False)
        else:
            self.main_window.button_create_stop.setDisabled(True)

    @pyqtSlot(int, int, str, int, int)
    def __update_progress_bar(
        self,
        created_files: int,
        total_files: int,
        file_name: str = None,
        current_chunk: int = None,
        total_chunks: int = None,
    ):
        created_files -= 1
        self.main_window.label_progress.setText(
            f"{created_files}/{total_files}"
        )
        self.main_window.progress_bar.setValue(created_files)
        if self.main_window.checkbox_debug.isChecked():
            self.main_window.label_debug_information.setText(f"Creating {file_name}")
            self.main_window.progress_bar_debug.setValue(current_chunk)

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

    def emit_progress_bar_update(
        self,
        n_created: int,
        number_files: int,
        file_name: str,
        chunk_n: int,
        number_of_chunks: int,
    ):
        self.signal_update_progress.emit(
            n_created, number_files, file_name, chunk_n, number_of_chunks
        )

    def emit_error_window(self, error_message: str):
        self.signal_error.emit(error_message)

    def emit_display_success_message(self):
        self.signal_complete.emit()

    def __hide_widget_log_options(self):
        if self.main_window.checkbox_savelog.isChecked():
            self.main_window.widget_log.show()
        else:
            self.main_window.widget_log.hide()

    def __click_button_browse_files(self):
        dialog = QFileDialog()
        path = f"{QFileDialog.getExistingDirectory(dialog, 'Select Directory')}"
        self.main_window.text_path.setText(path)

    def __click_button_browse_log(self):
        dialog = QFileDialog()
        path = f"{QFileDialog.getExistingDirectory(dialog, 'Select Directory')}"
        self.main_window.text_logfilepath.setText(path)

    def __click_button_close_quit(self):
        if self.main_window.button_close_quit.text() == "Quit":
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

    def __click_button_create_stop(self):
        if (
            len(self.main_window.text_path.text()) <= 0
            or len(self.main_window.text_n_files.text()) <= 0
            or len(self.main_window.text_size_files.text()) <= 0
            or len(self.main_window.text_chunk_size.text()) <= 0
        ):
            return
        elif (
            self.main_window.checkbox_savelog.isChecked()
            and len(self.main_window.text_logfilepath.text()) <= 0
        ):
            return
        elif self.main_window.button_create_stop.text() == "Create":
            folder_path = self.main_window.text_path.text()
            number_files = int(self.main_window.text_n_files.text())
            size_file = int(self.main_window.text_size_files.text())
            size_unit = self.main_window.combo_file_unit.currentText()
            chunk_size = int(self.main_window.text_chunk_size.text())
            chunk_unit = self.main_window.combo_chunk_unit.currentText()
            debug = self.main_window.checkbox_debug.isChecked()
            log_hash = self.main_window.checkbox_md5hash.isChecked()
            if self.main_window.checkbox_savelog.isChecked():
                log_path = self.main_window.text_logfilepath.text()
            else:
                log_path = None
            try:
                self.__creator_thread = FilesCreator(
                    folder_path=folder_path,
                    number_files=number_files,
                    size_file=size_file,
                    size_unit=size_unit,
                    chunk_size=chunk_size,
                    chunk_unit=chunk_unit,
                    debug=debug,
                    log_path=log_path,
                    log_hash=log_hash,
                    update_function=self.emit_progress_bar_update,
                    complete_function=self.emit_display_success_message,
                    error_function=self.emit_error_window,
                )

                if size_unit == "KiB":
                    size_mult = 1
                elif size_unit == "MiB":
                    size_mult = 2
                elif size_unit == "GiB":
                    size_mult = 3

                if chunk_unit == "KiB":
                    chunk_mult = 1
                elif chunk_unit == "MiB":
                    chunk_mult = 2
                elif chunk_unit == "GiB":
                    chunk_mult = 3

                file_size_bytes = math.ceil(size_file * (1024**size_mult))
                chunk_size_bytes = math.ceil(chunk_size * (1024**chunk_mult))

                # If the chunk size is too large, use the file size instead
                if file_size_bytes < chunk_size_bytes:
                    chunk_size_bytes = file_size_bytes
                    number_of_chunks = 1
                else:
                    number_of_chunks = math.ceil(file_size_bytes / chunk_size_bytes)

                self.main_window.progress_bar.setMaximum(number_files)
                self.main_window.progress_bar_debug.setMaximum(number_of_chunks)

                self.__creator_thread.start()
            except IOError as e:
                print(f"UI: Error starting FilesCreator thread: {e}")
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

    def __change_ui(self, state: str):
        if state == "disabled":
            self.main_window.label_path.setDisabled(True)
            self.main_window.label_n_files.setDisabled(True)
            self.main_window.label_size_files.setDisabled(True)
            self.main_window.label_logfilepath.setDisabled(True)
            self.main_window.label_debug_information.setDisabled(True)
            self.main_window.text_path.setDisabled(True)
            self.main_window.text_n_files.setDisabled(True)
            self.main_window.text_size_files.setDisabled(True)
            self.main_window.text_chunk_size.setDisabled(True)
            self.main_window.text_logfilepath.setDisabled(True)
            self.main_window.button_browse_files.setDisabled(True)
            self.main_window.button_browse_log.setDisabled(True)
            self.main_window.checkbox_debug.setDisabled(True)
            self.main_window.checkbox_savelog.setDisabled(True)
            self.main_window.checkbox_md5hash.setDisabled(True)
            self.main_window.combo_file_unit.setDisabled(True)
            self.main_window.combo_chunk_unit.setDisabled(True)
            self.main_window.button_create_stop.setText("Stop")
            self.main_window.button_close_quit.setText("Quit")
            self.main_window.widget_progress_bar.show()
            if self.main_window.checkbox_debug.isChecked():
                self.main_window.widget_debug.show()
            if self.main_window.checkbox_savelog.isChecked():
                self.main_window.widget_log.show()
            else:
                self.main_window.widget_log.hide()
        else:
            self.main_window.label_path.setDisabled(False)
            self.main_window.label_n_files.setDisabled(False)
            self.main_window.label_size_files.setDisabled(False)
            self.main_window.label_logfilepath.setDisabled(False)
            self.main_window.label_debug_information.setDisabled(False)
            self.main_window.text_path.setDisabled(False)
            self.main_window.text_n_files.setDisabled(False)
            self.main_window.text_size_files.setDisabled(False)
            self.main_window.text_chunk_size.setDisabled(False)
            self.main_window.text_logfilepath.setDisabled(False)
            self.main_window.button_browse_files.setDisabled(False)
            self.main_window.button_browse_log.setDisabled(False)
            self.main_window.checkbox_debug.setDisabled(False)
            self.main_window.checkbox_savelog.setDisabled(False)
            self.main_window.checkbox_md5hash.setDisabled(False)
            self.main_window.combo_file_unit.setDisabled(False)
            self.main_window.combo_chunk_unit.setDisabled(False)
            self.main_window.button_create_stop.setText("Create")
            self.main_window.button_close_quit.setText("Close")
            self.main_window.progress_bar.setValue(0)
            self.main_window.progress_bar_debug.setValue(0)
            self.main_window.label_progress.setText("0/0")
            self.main_window.widget_progress_bar.hide()
            self.main_window.widget_debug.hide()
            if self.main_window.checkbox_savelog.isChecked():
                self.main_window.widget_log.show()
            else:
                self.main_window.widget_log.hide()
        return


def main():
    app = QApplication(sys.argv)
    window = DFCUi()
    app.exec_()


if __name__ == "__main__":
    main()
