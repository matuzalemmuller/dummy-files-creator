import unittest
from .test_file_creation import TestFileCreation
from .test_log_creation import TestLogCreation
from .test_file_name import TestFileName
from .test_file_hash import TestFileHash

if __name__ == "__main__":
    tests = unittest.TestSuite()
    tests.addTest(TestFileCreation('test_file_creation'))
    tests.addTest(TestLogCreation('test_log_creation'))
    tests.addTest(TestFileName('test_file_name'))
    tests.addTest(TestFileHash('test_file_hash'))
    unittest.TextTestRunner().run(tests)
