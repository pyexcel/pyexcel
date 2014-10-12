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


class TestXLSHatWriter(PyexcelHatWriterBase):
    def setUp(self):
        self.testfile="test.xls"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestWriteReader:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = {
            "X": [1, 2, 3, 4, 5],
            "Y": [6, 7, 8, 9, 10],
            "Z": [11, 12, 13, 14, 15],
        }
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        self.testfile2 = "test.xlsm"

    def test_content_is_read(self):
        r = pyexcel.SeriesReader(self.testfile)
        content = pyexcel.utils.to_dict(r)
        print(content)
        assert content == self.content

    def test_write_simple_reader(self):
        r = pyexcel.Reader(self.testfile)
        w = pyexcel.Writer(self.testfile2)
        w.write_reader(r)
        w.close()
        r2 = pyexcel.SeriesReader(self.testfile2)
        content = pyexcel.utils.to_dict(r2)
        assert content == self.content

    def test_write_series_reader(self):
        r = pyexcel.SeriesReader(self.testfile)
        w = pyexcel.Writer(self.testfile2)
        w.write_reader(r)
        w.close()
        r2 = pyexcel.SeriesReader(self.testfile2)
        content = pyexcel.utils.to_dict(r2)
        print(content)
        assert content == self.content

    def test_write_simple_reader(self):
        try:
            w = pyexcel.Writer(self.testfile2)
            w.write_reader("abc")
            w.close()
            assert 1==2
        except TypeError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestBookWriter:
    def setUp(self):
        self.content = {
            'Sheet 2':
            [
                ['X', 'Y', 'Z'],
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]
            ],
            'Sheet 3':
            [
                ['O', 'P', 'Q'],
                [3.0, 2.0, 1.0],
                [4.0, 3.0, 2.0]
            ],
            'Sheet 1':
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ]
        }
        self.testfile = "test.xls"
        self.testfile2 = "test.xlsx"
        w = pyexcel.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()


    def test_write_book_reader(self):
        reader = pyexcel.BookReader(self.testfile)
        writer = pyexcel.BookWriter(self.testfile2)
        writer.write_book_reader(reader)
        writer.close()
        reader2 = pyexcel.BookReader(self.testfile2)
        data = pyexcel.utils.to_dict(reader2)
        assert data == self.content

    def test_not_supported_file(self):
        try:
            pyexcel.BookWriter("bad.format")
        except NotImplementedError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestCSVBookWriter:
    def setUp(self):
        self.content = {
            'Sheet 2':
            [
                ['X', 'Y', 'Z'],
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]
            ],
            'Sheet 3':
            [
                ['O', 'P', 'Q'],
                [3.0, 2.0, 1.0],
                [4.0, 3.0, 2.0]
            ],
            'Sheet 1':
            [
                [1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]
            ]
        }
        self.testfile = "test.xls"
        self.testfile2 = "test.csv"
        w = pyexcel.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()

    def test_write_book_reader(self):
        reader = pyexcel.BookReader(self.testfile)
        writer = pyexcel.BookWriter(self.testfile2)
        writer.write_book_reader(reader)
        writer.close()
        sheet1 = "test_Sheet 1.csv"
        reader1 = pyexcel.Reader(sheet1)
        data = pyexcel.utils.to_array(reader1)
        assert data == self.content["Sheet 1"]
        sheet2 = "test_Sheet 2.csv"
        reader2 = pyexcel.Reader(sheet2)
        data = pyexcel.utils.to_array(reader2)
        assert data == self.content["Sheet 2"]
        sheet3 = "test_Sheet 3.csv"
        reader3 = pyexcel.Reader(sheet3)
        data = pyexcel.utils.to_array(reader3)
        assert data == self.content["Sheet 3"]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists("test_Sheet 1.csv"):
            os.unlink("test_Sheet 1.csv")
        if os.path.exists("test_Sheet 2.csv"):
            os.unlink("test_Sheet 2.csv")
        if os.path.exists("test_Sheet 3.csv"):
            os.unlink("test_Sheet 3.csv")
