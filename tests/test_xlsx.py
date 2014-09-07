import os
import pyexcel
from base import PyexcelXlsBase


class TestXLSXReader(PyexcelXlsBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.xlsx"
        self._write_test_file(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
