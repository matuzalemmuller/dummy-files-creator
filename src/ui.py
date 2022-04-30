from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
from files_creator import FilesCreator


class About(QtWidgets.QDialog):
    def __init__(self):
        super(About, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("../lib/qt/About.ui", self)  # Load the .ui file
        self.exec_()
        self.activateWindow()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("../lib/qt/MainWindow.ui", self)  # Load the .ui file
        self.setWindowIcon(QtGui.QIcon("../icon.png"))
        # Initialize UI elements
        self.creating_files = False  # Files are not being created
        self.__set_validator()
        self.__set_connect()
        self.__switch_log_options()
        self.__switch_progress_bar()
        self.__toggle_create_stop()
        self.show()  # Show the GUI

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

    def __about_action(self):
        About()

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

    # Set validator for number-exclusive fields
    def __set_validator(self):
        number_regex = QtCore.QRegExp("[0-9]+")
        number_validator = QtGui.QRegExpValidator(number_regex)
        self.text_n_files.setValidator(number_validator)
        self.text_size_files.setValidator(number_validator)
        self.text_chunk_size.setValidator(number_validator)

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

    # Action to button Stop
    def _cancel_creation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        cancel_code = msg.exec_()
        if cancel_code == QMessageBox.Yes:
            self._change_layout("Stopped")

    # Open native folder dialog to select where test files will be created
    def __browse_files(self):
        dialog = QtWidgets.QFileDialog()
        path = str(
            QtWidgets.QFileDialog.getExistingDirectory(dialog, "Select Directory")
        )
        self.text_path.setText(path)

    # Open native folder dialog to select where log file will be saved
    def __browse_log(self):
        dialog = QtWidgets.QFileDialog()
        path = str(
            QtWidgets.QFileDialog.getExistingDirectory(dialog, "Select Directory")
        )
        self.text_logfilepath.setText(path)

    # Show/hide log folder text field
    def __switch_log_options(self):
        if self.checkbox_savelog.isChecked():
            self.widget_log.show()
        else:
            self.widget_log.hide()

    # Show/hide file creation progress bar
    def __switch_progress_bar(self):
        if self.creating_files:
            self.widget_progress_bar.show()
        else:
            self.widget_progress_bar.hide()

    # Steps taken when clicking on Create/Stop
    def __create_stop_clicked(self):
        if self.button_create_stop.text() == "Create":
            self.__change_ui(state="disabled")
            f = FilesCreator()
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
            self.__change_ui(state="enabled")

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
        return


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
