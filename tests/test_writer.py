import os
from base import PyexcelWriterBase, PyexcelHatWriterBase
import pyexcel


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

class TestODSHatWriter(PyexcelHatWriterBase):
    def setUp(self):
        self.testfile="test.ods"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestWriteReader:
    def setUp(self):
        self.testfile = "test.ods"
        self.content = {
            "X": [1,2,3,4,5],
            "Y": [6,7,8,9,10],
            "Z": [11,12,13,14,15],
        }
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        self.testfile2 = "test.xlsm"

    def test_write_simple_reader(self):
        r = pyexcel.Reader(self.testfile)
        w = pyexcel.Writer(self.testfile2)
        w.write_reader(r)
        w.close()
        r2 = pyexcel.SeriesReader(self.testfile2)
        content = pyexcel.utils.to_dict(r2)
        print content
        assert content == self.content

    def test_write_series_reader(self):
        r = pyexcel.SeriesReader(self.testfile)
        w = pyexcel.Writer(self.testfile2)
        w.write_reader(r)
        w.close()
        r2 = pyexcel.SeriesReader(self.testfile2)
        content = pyexcel.utils.to_dict(r2)
        print content
        assert content == self.content

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
