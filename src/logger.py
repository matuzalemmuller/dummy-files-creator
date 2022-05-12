import csv
import datetime
import io
import logging
from logging.handlers import RotatingFileHandler
import uuid


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow([datetime.datetime.now(), record.msg, record.file_size])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


class CustomFilter(logging.Filter):
    def filter(self, record):
        global file_size
        record.file_size = file_size
        return True


class Logger:
    def __init__(self, log_path, error_function=None):
        self.error_function = error_function
        self.logger = logging.getLogger(str(uuid.uuid4()))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addFilter(CustomFilter())

        log_handler = RotatingFileHandler(
            log_path,
            mode="w",
            delay=0,
        )
        csv_format = CsvFormatter()
        log_handler.setFormatter(csv_format)
        self.logger.addHandler(log_handler)

    def log(self, f_path, f_size):
        global file_size
        file_size = f_size
        self.logger.info(f_path)
