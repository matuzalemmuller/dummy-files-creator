import os
import uuid
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot


class FilesCreator(QObject):
    sig_step = pyqtSignal(str, int)
    sig_done = pyqtSignal()
    sig_abort = pyqtSignal(str)

    def __init__(self, path, number_files, size_files, size_unit):
        super().__init__()
        self._path = path
        self._number_files = int(number_files)
        self._size_files = int(size_files)
        self._size_unit = size_unit
        self.created_files = 0
        self.errorFlag = 0
        self.error = ""
        self.__abort = False
        self._running = False


    @pyqtSlot()
    def work(self):
        self._running = True
        prefix = 1024 ** self._size_unit
        file_size = self._size_files * prefix
        
        while self.created_files < self._number_files:
            if self.__abort == True:
                self._running = False
                return
            file_name = str(uuid.uuid4())
            try:
                with open(self._path+"/"+file_name, 'wb') as fout:
                    fout.write(os.urandom(file_size))
            except IOError as e:
                self.sig_abort.emit(str(e))
                return
            self.created_files+=1
            self.sig_step.emit(file_name, self.created_files)
        self.sig_done.emit()


    def abort(self):
        self.__abort = True