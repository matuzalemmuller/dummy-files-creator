from PyQt5 import uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow
from files_creator import FilesCreator
import sys


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("../lib/qt/About.ui", self)  # Load the .ui file
        self.exec_()
        self.activateWindow()


class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("../lib/qt/MainWindow.ui", self)  # Load the .ui file
        # Initialize UI elements
        self.__creating_files = False  # Files are not being created
        self.__created_files = 0
        self.__total_files = 0
        self.__set_validator()
        self.__set_connect()
        self.__switch_log_options()
        self.__toggle_create_stop()
        self.__change_ui("enabled")
        self.show()  # Show the GUI

    def __about_action(self):
        About()

    # Connects Qt elements to action methods
    def __set_connect(self):
        self.button_browse_files.clicked.connect(self.__browse_files)
        self.button_browse_log.clicked.connect(self.__browse_log)
        self.text_path.textChanged.connect(self.__toggle_create_stop)
        self.text_n_files.textChanged.connect(self.__toggle_create_stop)
        self.text_size_files.textChanged.connect(self.__toggle_create_stop)
        self.text_chunk_size.textChanged.connect(self.__toggle_create_stop)
        self.button_create_stop.clicked.connect(self.__create_stop_clicked)
        self.button_close_quit.clicked.connect(self.__close_app)
        self.checkbox_savelog.stateChanged.connect(self.__switch_log_options)
        self.action_about.triggered.connect(self.__about_action)

    # Set validator for number-exclusive fields
    def __set_validator(self):
        number_regex = QRegExp("[0-9]+")
        number_validator = QRegExpValidator(number_regex)
        self.text_n_files.setValidator(number_validator)
        self.text_size_files.setValidator(number_validator)
        self.text_chunk_size.setValidator(number_validator)

    # Enables create button when all fields have values
    def __toggle_create_stop(self):
        if (
            len(self.text_path.text()) > 0
            and len(self.text_n_files.text()) > 0
            and len(self.text_size_files.text()) > 0
            and len(self.text_chunk_size.text()) > 0
        ):
            self.button_create_stop.setDisabled(False)
        else:
            self.button_create_stop.setDisabled(True)

    # Open native folder dialog to select where test files will be created
    def __browse_files(self):
        dialog = QFileDialog()
        path = str(QFileDialog.getExistingDirectory(dialog, "Select Directory"))
        self.text_path.setText(path)

    # Show/hide log folder text field
    def __switch_log_options(self):
        if self.checkbox_savelog.isChecked():
            self.widget_log.show()
        else:
            self.widget_log.hide()

    # Open native folder dialog to select where log file will be saved
    def __browse_log(self):
        dialog = QFileDialog()
        path = str(QFileDialog.getExistingDirectory(dialog, "Select Directory"))
        self.text_logfilepath.setText(path)

    # Action to button Stop
    def __cancel_creation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        cancel_code = msg.exec_()
        if cancel_code == QMessageBox.Yes:
            self._change_layout("Stopped")

    # Action to button Close/Quit
    def __close_app(self):
        if self.button_close_quit.text() == "Quit":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Quit")
            msg.setText("Are you sure you want to quit?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            quit_code = msg.exec_()
            if quit_code == QMessageBox.Yes:
                sys.exit(0)
        else:
            sys.exit(0)

    # Steps taken when clicking on Create/Stop
    def __create_stop_clicked(self):
        if self.button_create_stop.text() == "Create":
            self.__total_files = int(self.text_n_files.text())
            self.__created_files = 0
            self.__change_ui(state="disabled")
            # for i in range(self.__total_files):
            #     self.__created_files += 1
            #     self.__update_progress_bar()
            #     time.sleep(1)
            # self.__change_ui(state="enabled")
            # f = FilesCreator()
            # files_created = 0
            # while files_created < int(self.text_n_files.text()):
            #     f.create_files(path=self.text_path.text(),
            #         size_file=int(self.text_size_files.text()),
            #         size_unit=self.combo_file_unit.currentText(),
            #         chunk_size=int(self.text_chunk_size.text()),
            #         chunk_unit=self.combo_chunk_unit.currentText()
            #     )
            #     files_created += 1
        else:
            self.__total_files = 0
            self.__created_files = 0
            # self.__cancel_creation()
            self.__change_ui(state="enabled")

    def __update_progress_bar(self):
        progress_bar_text = str(self.__created_files) + "/" + str(self.__total_files)
        progress_bar_percent = int(self.__created_files * 100 / self.__total_files)
        self.label_progress.setText(progress_bar_text)
        self.progress_bar.setValue(progress_bar_percent)

    # Enables/disables fields when app is starts running or turns idle
    def __change_ui(self, state: str):
        if state == "disabled":
            self.label_path.setDisabled(True)
            self.label_n_files.setDisabled(True)
            self.label_size_files.setDisabled(True)
            self.label_logfilepath.setDisabled(True)
            self.text_path.setDisabled(True)
            self.text_n_files.setDisabled(True)
            self.text_size_files.setDisabled(True)
            self.text_chunk_size.setDisabled(True)
            self.text_logfilepath.setDisabled(True)
            self.button_browse_files.setDisabled(True)
            self.button_browse_log.setDisabled(True)
            self.checkbox_debug.setDisabled(True)
            self.checkbox_savelog.setDisabled(True)
            self.combo_file_unit.setDisabled(True)
            self.combo_chunk_unit.setDisabled(True)
            self.button_create_stop.setText("Stop")
            self.button_close_quit.setText("Quit")
            self.widget_progress_bar.show()
            if self.checkbox_debug.isChecked():
                self.widget_debug.show()
        else:
            self.label_path.setDisabled(False)
            self.label_n_files.setDisabled(False)
            self.label_size_files.setDisabled(False)
            self.label_logfilepath.setDisabled(False)
            self.text_path.setDisabled(False)
            self.text_n_files.setDisabled(False)
            self.text_size_files.setDisabled(False)
            self.text_chunk_size.setDisabled(False)
            self.text_logfilepath.setDisabled(False)
            self.button_browse_files.setDisabled(False)
            self.button_browse_log.setDisabled(False)
            self.checkbox_debug.setDisabled(False)
            self.checkbox_savelog.setDisabled(False)
            self.combo_file_unit.setDisabled(False)
            self.combo_chunk_unit.setDisabled(False)
            self.button_create_stop.setText("Create")
            self.button_close_quit.setText("Close")
            self.widget_progress_bar.hide()
            self.widget_debug.hide()
        return


def main():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()


if __name__ == "__main__":
    main()
