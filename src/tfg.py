import sys
from about import About
from files_creator import FilesCreator
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMenuBar

#------------------------------------------------------------------------------#

class MyWindow(QWidget):
    sig_abort_workers = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Files Generator")
        self.setWindowIcon(QtGui.QIcon('../icon/icon.png'))
        QThread.currentThread().setObjectName('main')
        self.__threads = []
        self._files_created = []
        self._create_ui()


    def _create_ui(self):
        self._window_layout = QGridLayout()
        self._window_layout.setContentsMargins(0,0,0,0)

        self._menu_bar = QMenuBar()
        self._window_layout.addWidget(self._menu_bar)
        self._help_item = self._menu_bar.addMenu('Help')
        self._about_action = QAction("Help", self._menu_bar)
        self._about_action.triggered.connect(self._about_clicked)
        self._help_item.addAction(self._about_action)

        self._options_layout = QGridLayout()
        self._options_layout.setAlignment(QtCore.Qt.AlignCenter)
        self._options_widget = QWidget()
        self._options_widget.setLayout(self._options_layout)

        self._path_label = QLabel()
        self._path_label.setText("Path")
        self._path_label.setAlignment(QtCore.Qt.AlignCenter)

        self._path_textbox = QLineEdit()
        self._path_textbox.resize(320,20)
        self._path_textbox.setMinimumWidth(320)

        self._browse_button = QPushButton("Browse")
        self._browse_button.setFixedWidth(80)
        self._browse_button.clicked.connect(self._browse_clicked)

        self._options_layout.addWidget(self._path_label, 1, 1)
        self._options_layout.addWidget(self._path_textbox, 1, 2)
        self._options_layout.addWidget(self._browse_button, 1, 3,
                                      QtCore.Qt.AlignCenter)

        self._number_files_label = QLabel()
        self._number_files_label.setText("Number of Files")
        self._number_files_label.setAlignment(QtCore.Qt.AlignCenter)

        self._number_validator=QtCore.QRegExp("[0-9]+")
        self._validator = QtGui.QRegExpValidator(self._number_validator)

        self._number_files_textbox = QLineEdit()
        self._number_files_textbox.resize(320,20)
        self._number_files_textbox.setMinimumWidth(320)
        self._number_files_textbox.setValidator(self._validator)

        self._options_layout.addWidget(self._number_files_label, 2, 1)
        self._options_layout.addWidget(self._number_files_textbox, 2, 2)

        self._size_files_label = QLabel()
        self._size_files_label.setText("Size of File(s)")
        self._size_files_label.setAlignment(QtCore.Qt.AlignCenter)

        self._size_files_textbox = QLineEdit()
        self._size_files_textbox.resize(320,20)
        self._size_files_textbox.setMinimumWidth(320)
        self._size_files_textbox.setValidator(self._validator)

        self._radio_button_layout = QHBoxLayout()
        self._radio_button_layout.setSpacing(5)
        self._radio_widget = QWidget() 
        self._radio_widget.setLayout(self._radio_button_layout)
        self._kb_button = QRadioButton("KB")
        self._kb_button.setChecked(False)
        self._mb_button = QRadioButton("MB")
        self._mb_button.setChecked(True)
        self._gb_button = QRadioButton("GB")
        self._gb_button.setChecked(False)

        self._radio_button_layout.addWidget(self._kb_button, 1)
        self._radio_button_layout.addWidget(self._mb_button, 2)
        self._radio_button_layout.addWidget(self._gb_button, 3)

        self._options_layout.addWidget(self._size_files_label, 3, 1)
        self._options_layout.addWidget(self._size_files_textbox, 3, 2)
        self._options_layout.addWidget(self._radio_widget, 3, 3,
                                      QtCore.Qt.AlignLeft)

        self._create_close_layout = QHBoxLayout()
        self._create_close_widget = QWidget() 
        self._create_close_widget.setLayout(self._create_close_layout)

        self._create_button = QPushButton("Create")
        self._create_button.setFixedWidth(80)
        self._create_button.clicked.connect(self._create_clicked)

        self._close_button = QPushButton("Close")
        self._close_button.setFixedWidth(80)
        self._close_button.clicked.connect(self._close_clicked)

        self._create_close_layout.addWidget(self._create_button, 1)
        self._create_close_layout.addWidget(self._close_button, 1)

        self._options_layout.addWidget(self._create_close_widget, 4, 2)

        self._window_layout.addWidget(self._options_widget)
        self._window_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.progress_bar = QProgressBar()
        self.progress_bar.setContentsMargins(0,0,0,0)
        self.progress_label = QLabel()
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_label.setContentsMargins(0,0,0,0)

        self.setLayout(self._window_layout)


    def _about_clicked(self):
        About()


    def _browse_clicked(self):
        dialog = QFileDialog()
        path = str(QFileDialog.getExistingDirectory(dialog,
                                                         "Select Directory"))
        self._path_textbox.setText(path)    
   

    def _create_clicked(self):
        if self._path_textbox.text() == "" or \
        self._number_files_textbox.text() == "" or \
        self._size_files_textbox.text() == "":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("You must fill all options to "\
                                       "create files")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        elif int(self._number_files_textbox.text()) == 0 or \
        int(self._size_files_textbox.text()) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Number of files/File size cannot be zero")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            if self._kb_button.isChecked(): size_unit = 1
            elif self._mb_button.isChecked(): size_unit = 2
            else: size_unit = 3
            self.Files = FilesCreator(self._path_textbox.text(),
                                            self._number_files_textbox.text(),
                                            self._size_files_textbox.text(),
                                            size_unit)
            self.thread = QThread()
            self.__threads.append((self.thread, self.Files))
            self.Files.moveToThread(self.thread)
            self.Files.sig_step.connect(self._step)
            self.Files.sig_done.connect(self._done)  
            self.Files.sig_abort.connect(self._abort)
            self.thread.started.connect(self.Files.work)
            self.thread.start()
            self._change_layout('Running')


    def _close_clicked(self):
        if self._close_button.text() == "Quit":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Quit")
            msg.setText("Are you sure you want to quit?\n" + \
                        "It may take a few moments to exit the app.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            quit_code = msg.exec_()
            if quit_code == QMessageBox.Yes:
                sys.exit(0)
        else:
            sys.exit(0)


    def _cancel_clicked(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Confirmation")
        msg.setText("Are you sure?\nThe current file will still be created " + \
                    "before the program closes.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        cancel_code = msg.exec_()
        if cancel_code == QMessageBox.Yes:
            self.Files.abort()
            self._change_layout('Stopped')


    def _change_layout(self, status):
        if status == 'Running':
            disabled_style = "background-color: rgb(210,210,210); border: gray"
            self._path_textbox.setStyleSheet(disabled_style)
            self._number_files_textbox.setStyleSheet(disabled_style)
            self._size_files_textbox.setStyleSheet(disabled_style)
            self._path_textbox.setDisabled(True)
            self._number_files_textbox.setDisabled(True)
            self._size_files_textbox.setDisabled(True)
            self._kb_button.setDisabled(True)
            self._mb_button.setDisabled(True)
            self._gb_button.setDisabled(True)
            self._create_button.setText("Cancel")
            self._create_button.clicked.disconnect()
            self._create_button.clicked.connect(self._cancel_clicked)
            self._close_button.setText("Quit")
            self._close_button.clicked.disconnect()
            self._close_button.clicked.connect(self._close_clicked)
            self.progress_bar.setContentsMargins(0,0,0,0)
            self.progress_bar.setValue(0)
            self.progress_label.setText("0/" + \
                                        str(self.Files._number_files))

            self._window_layout.addWidget(self.progress_label)
            self._window_layout.addWidget(self.progress_bar)
            self.repaint()
        else:
            self._path_textbox.setStyleSheet("")
            self._number_files_textbox.setStyleSheet("")
            self._size_files_textbox.setStyleSheet("")
            self._path_textbox.setDisabled(False)
            self._number_files_textbox.setDisabled(False)
            self._size_files_textbox.setDisabled(False)
            self._kb_button.setDisabled(False)
            self._mb_button.setDisabled(False)
            self._gb_button.setDisabled(False)
            self._create_button.setText("Create")
            self._create_button.clicked.disconnect()
            self._create_button.clicked.connect(self._create_clicked)
            self._close_button.setText("Close")
            self._close_button.clicked.disconnect()
            self._close_button.clicked.connect(self._close_clicked)

            self._window_layout.removeWidget(self.progress_label)
            self._window_layout.removeWidget(self.progress_bar)
            self.repaint()


    @pyqtSlot(str)
    def _abort(self, error: str):
        print(error)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Error. See details for more information.")
        msg.setDetailedText(error)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self._change_layout('Stopped')


    @pyqtSlot()
    def _done(self):
        self._change_layout('Stopped')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Info")
        msg.setInformativeText("Files created!")
        detailed_text = ""
        for i in range(0,len(self._files_created)):
            detailed_text = detailed_text + self._files_created[i] + "\n"
        msg.setDetailedText(detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    @pyqtSlot(str, int)
    def _step(self, file_name: str, number_files: int):
        self.progress_label.setText(str(self.Files.created_files) + "/" + \
                                    str(int(self._number_files_textbox.text())))
        value = number_files * 100 / int(self._number_files_textbox.text())
        self.progress_bar.setValue(value)
        self._files_created.append(file_name)

#------------------------------------------------------------------------------#

if __name__ == "__main__":
    app = QApplication([])

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())