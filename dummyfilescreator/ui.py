#! /usr/bin/env python3
import sys
from .files_creator import FilesCreator
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow, QMessageBox


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("./lib/qt/About.ui", self)  # Load the .ui file
        self.exec_()
        self.activateWindow()


class Ui(QMainWindow):
    signal_update_progress = pyqtSignal(int, int, str, int, int)
    signal_error = pyqtSignal(str)
    signal_complete = pyqtSignal()

    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("./lib/qt/MainWindow.ui", self)  # Load the .ui file
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
        self.button_browse_files.clicked.connect(self.__click_button_browse_files)
        self.button_browse_log.clicked.connect(self.__click_button_browse_log)
        self.text_path.textChanged.connect(self.__enable_create_button)
        self.text_n_files.textChanged.connect(self.__enable_create_button)
        self.text_size_files.textChanged.connect(self.__enable_create_button)
        self.text_chunk_size.textChanged.connect(self.__enable_create_button)
        self.button_create_stop.clicked.connect(self.__click_button_create_stop)
        self.button_close_quit.clicked.connect(self.__click_button_close_quit)
        self.checkbox_savelog.stateChanged.connect(self.__hide_widget_log_options)
        self.action_about.triggered.connect(self.__about_action)
        self.text_path.returnPressed.connect(self.__click_button_create_stop)
        self.text_n_files.returnPressed.connect(self.__click_button_create_stop)
        self.text_size_files.returnPressed.connect(self.__click_button_create_stop)
        self.text_chunk_size.returnPressed.connect(self.__click_button_create_stop)
        self.signal_update_progress.connect(self.__update_progress_bar)
        self.signal_complete.connect(self.__display_success_message)
        self.signal_error.connect(self.__display_error_message)

    def __set_number_validator(self):
        number_regex = QRegExp("[0-9]+")
        number_validator = QRegExpValidator(number_regex)
        self.text_n_files.setValidator(number_validator)
        self.text_size_files.setValidator(number_validator)
        self.text_chunk_size.setValidator(number_validator)

    def __enable_create_button(self):
        if (
            len(self.text_path.text()) > 0
            and len(self.text_n_files.text()) > 0
            and len(self.text_size_files.text()) > 0
            and len(self.text_chunk_size.text()) > 0
        ):
            self.button_create_stop.setDisabled(False)
        else:
            self.button_create_stop.setDisabled(True)

    @pyqtSlot(int, int, str, int, int)
    def __update_progress_bar(
        self,
        created_files: int,
        total_files: int,
        file_name: str = None,
        current_chunk: int = None,
        total_chunks: int = None,
    ):
        progress_bar_text = str(created_files) + "/" + str(total_files)
        progress_bar_percent = int(created_files * 100 / total_files)
        self.label_progress.setText(progress_bar_text)
        self.progress_bar.setValue(progress_bar_percent)
        if self.checkbox_debug.isChecked():
            debug_bar = "Creating " + file_name
            debug_percent = int(current_chunk * 100 / total_chunks)
            self.label_debug_information.setText(debug_bar)
            self.progress_bar_debug.setValue(debug_percent)

    @pyqtSlot(str)
    def __display_error_message(self, error_message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
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

    def emit_error_window(self, error_message):
        self.signal_error.emit(error_message)

    def emit_display_success_message(self):
        self.signal_complete.emit()

    def __hide_widget_log_options(self):
        if self.checkbox_savelog.isChecked():
            self.widget_log.show()
        else:
            self.widget_log.hide()

    def __click_button_browse_files(self):
        dialog = QFileDialog()
        path = str(QFileDialog.getExistingDirectory(dialog, "Select Directory"))
        self.text_path.setText(path)

    def __click_button_browse_log(self):
        dialog = QFileDialog()
        path = str(QFileDialog.getExistingDirectory(dialog, "Select Directory"))
        self.text_logfilepath.setText(path)

    def __click_button_close_quit(self):
        if self.button_close_quit.text() == "Quit":
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
            len(self.text_path.text()) <= 0
            or len(self.text_n_files.text()) <= 0
            or len(self.text_size_files.text()) <= 0
            or len(self.text_chunk_size.text()) <= 0
        ):
            return
        elif (
            self.checkbox_savelog.isChecked() and len(self.text_logfilepath.text()) <= 0
        ):
            return
        elif self.button_create_stop.text() == "Create":
            folder_path = self.text_path.text()
            number_files = int(self.text_n_files.text())
            size_file = int(self.text_size_files.text())
            size_unit = self.combo_file_unit.currentText()
            chunk_size = int(self.text_chunk_size.text())
            chunk_unit = self.combo_chunk_unit.currentText()
            debug = self.checkbox_debug.isChecked()
            log_hash = self.checkbox_md5hash.isChecked()
            if self.checkbox_savelog.isChecked():
                log_path = self.text_logfilepath.text()
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
                self.__creator_thread.start()
            except IOError as e:
                print("UI: Error starting FilesCreator thread: " + str(e))
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
            self.label_path.setDisabled(True)
            self.label_n_files.setDisabled(True)
            self.label_size_files.setDisabled(True)
            self.label_logfilepath.setDisabled(True)
            self.label_debug_information.setDisabled(True)
            self.text_path.setDisabled(True)
            self.text_n_files.setDisabled(True)
            self.text_size_files.setDisabled(True)
            self.text_chunk_size.setDisabled(True)
            self.text_logfilepath.setDisabled(True)
            self.button_browse_files.setDisabled(True)
            self.button_browse_log.setDisabled(True)
            self.checkbox_debug.setDisabled(True)
            self.checkbox_savelog.setDisabled(True)
            self.checkbox_md5hash.setDisabled(True)
            self.combo_file_unit.setDisabled(True)
            self.combo_chunk_unit.setDisabled(True)
            self.button_create_stop.setText("Stop")
            self.button_close_quit.setText("Quit")
            self.widget_progress_bar.show()
            if self.checkbox_debug.isChecked():
                self.widget_debug.show()
            if self.checkbox_savelog.isChecked():
                self.widget_log.show()
            else:
                self.widget_log.hide()
        else:
            self.label_path.setDisabled(False)
            self.label_n_files.setDisabled(False)
            self.label_size_files.setDisabled(False)
            self.label_logfilepath.setDisabled(False)
            self.label_debug_information.setDisabled(False)
            self.text_path.setDisabled(False)
            self.text_n_files.setDisabled(False)
            self.text_size_files.setDisabled(False)
            self.text_chunk_size.setDisabled(False)
            self.text_logfilepath.setDisabled(False)
            self.button_browse_files.setDisabled(False)
            self.button_browse_log.setDisabled(False)
            self.checkbox_debug.setDisabled(False)
            self.checkbox_savelog.setDisabled(False)
            self.checkbox_md5hash.setDisabled(False)
            self.combo_file_unit.setDisabled(False)
            self.combo_chunk_unit.setDisabled(False)
            self.button_create_stop.setText("Create")
            self.button_close_quit.setText("Close")
            self.progress_bar.setValue(0)
            self.progress_bar_debug.setValue(0)
            self.label_progress.setText("0/0")
            self.widget_progress_bar.hide()
            self.widget_debug.hide()
            if self.checkbox_savelog.isChecked():
                self.widget_log.show()
            else:
                self.widget_log.hide()
        return

def main():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


if __name__ == "__main__":
    main()
