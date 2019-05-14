import sys
import os
import uuid
import threading

class filesCreator():
    def __init__(self, path, number_files, size_files, size_unit):
        self._path = path
        self._number_files = number_files
        self._size_files = size_files
        self._size_unit = size_unit
        self.created_files = 0
        self.errorFlag = 0
        self.error = ""
        self._stop_event = 0
        self._running = False

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def is_running(self):
        return self._running

    def run(self):
        self._running = True
        prefix = 1024 ** self._size_unit
        file_size = int(self._size_files) * prefix
        
        while self.created_files < int(self._number_files):
            if self._stop_event == 1:
                self._running = False
                return

            file_name = str(uuid.uuid4())
            try:
                with open(self._path+"/"+file_name, 'wb') as fout:
                    fout.write(os.urandom(file_size))
            except IOError as e:
                self.error = e
                self.errorFlag = 1
                sys.exit(1)
            self.created_files+=1
    
    def stop(self):
        self._stop_event = 1