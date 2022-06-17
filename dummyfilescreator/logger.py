"""Author: Matuzalem (Mat) Muller.

License: GPLv3
"""
import csv
import datetime
import io
import logging
from logging.handlers import RotatingFileHandler
import uuid

FILE_SIZE = 0
HASH = 0


class CsvFormatter(logging.Formatter):
    """Formats log entry as csv."""

    def __init__(self):
        """Create csv write for log formatting."""
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        """Return log record in csv format."""
        self.writer.writerow(
            [datetime.datetime.now(), record.file_size, record.msg, record.hash]
        )
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


class CustomFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Custom filter to save file size and hash to log file."""

    def filter(self, record):
        """Include file size and hash in the log record."""
        record.file_size = FILE_SIZE
        record.hash = HASH
        return True


class Logger:  # pylint: disable=too-few-public-methods
    """Logger class, to be used by classes that want to save log entries to file."""

    def __init__(self, log_path, error_function=None):
        """Create log file and set up logger formatter and filter."""
        self.error_function = error_function
        self.logger = logging.getLogger(str(uuid.uuid4()))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addFilter(CustomFilter())

        try:
            log_handler = RotatingFileHandler(
                log_path,
                mode="a",
                delay=0,
            )
            csv_format = CsvFormatter()
            log_handler.setFormatter(csv_format)
            self.logger.addHandler(log_handler)
        except IOError as error:
            raise error

    def log(self, f_path, f_size, f_hash=None):
        """Save log record to log file."""
        global FILE_SIZE  # pylint: disable=global-statement
        FILE_SIZE = f_size
        global HASH  # pylint: disable=global-statement
        HASH = f_hash
        try:
            self.logger.info(f_path)
        except IOError as error:
            raise error
