import logging
from logging.handlers import RotatingFileHandler
import csv
import io


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow([record.levelname, record.msg, record.file_size])
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
    def __init__(self, log_path):
        csv_format = CsvFormatter()

        self.logger = logging.getLogger("root")

        self.logger.setLevel(logging.DEBUG)
        self.logger.addFilter(CustomFilter())

        log_handler = RotatingFileHandler(
            log_path,
            mode="a",
            encoding=None,
            delay=0,
        )
        log_handler.setFormatter(csv_format)
        self.logger.addHandler(log_handler)

    def log(self, f_path, f_size):
        global file_size
        file_size = f_size
        self.logger.debug(f_path)
