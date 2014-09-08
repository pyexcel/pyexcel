import os
from base import PyexcelWriterBase


class TestCSVnXLSMWriter(PyexcelWriterBase):
    def setUp(self):
        self.testfile="test.csv"
        self.testfile2="test.xlsm"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)

class TestXLSnXLSXWriter(PyexcelWriterBase):
    def setUp(self):
        self.testfile="test.xls"
        self.testfile2="test.xlsx"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)

class TestODSnCSVWriter(PyexcelWriterBase):
    def setUp(self):
        self.testfile="test.ods"
        self.testfile2="test.csv"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
