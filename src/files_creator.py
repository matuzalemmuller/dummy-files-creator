import os
import math
import uuid
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot


class FilesCreator(QObject):
    sig_step_overall = pyqtSignal(str, int)
    sig_step_file = pyqtSignal(str, int, int)
    sig_done = pyqtSignal()
    sig_abort = pyqtSignal(str)

    def __init__(self, path, number_files, size_files, size_unit, chunksize,
                 chunksize_unit, debug):
        super().__init__()
        self._path = path
        self._number_files = int(number_files)
        self._file_size = int(size_files) * (1024 ** size_unit) #1073741824
        self._chunksize = int(chunksize) * (1024 ** chunksize_unit)
        self._debug = debug
        self.created_files = 0
        self.errorFlag = 0
        self.error = ""
        self.__abort = False
        self._running = False


    @pyqtSlot()
    def work(self):
        self._running = True

        chunks = math.ceil(self._file_size / self._chunksize)
        os_size = int(self._file_size * 1024 / chunks)

        if self._debug == True:
            while self.created_files < self._number_files:
                file_name = str(uuid.uuid4())
                try:
                    with open(self._path+"/"+file_name, "wb") as fout:
                        for iter in range(chunks):
                            fout.write(os.urandom(os_size))
                            self.sig_step_file.emit(file_name, iter, chunks)
                            if self.__abort == True:
                                self._running = False
                                os.remove(self._path+"/"+file_name)
                                return
                except IOError as e:
                    self.sig_abort.emit(str(e))
                    return
                self.created_files+=1
                self.sig_step_overall.emit(file_name, self.created_files)
        else:
            # "Repeats" code without debug check for better performance
            while self.created_files < self._number_files:
                file_name = str(uuid.uuid4())
                try:
                    with open(self._path+"/"+file_name, "wb") as fout:
                        for iter in range(chunks):
                            fout.write(os.urandom(os_size))                         
                            if self.__abort == True:
                                self._running = False
                                os.remove(self._path+"/"+file_name)
                                return
                except IOError as e:
                    self.sig_abort.emit(str(e))
                    return
                self.created_files+=1
                self.sig_step_overall.emit(file_name, self.created_files)            
        self.sig_done.emit()


    def abort(self):
        self.__abort = True