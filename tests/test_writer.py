import os
from base import PyexcelWriterBase, PyexcelHatWriterBase, clean_up_files
import pyexcel as pe


class TestCSVnXLSMWriter(PyexcelWriterBase):
    def setUp(self):
        self.testfile="test.csv"
        self.testfile2="test.xlsm"

    def tearDown(self):
        file_list = [self.testfile, self.testfile2]
        clean_up_files(file_list)

class TestXLSnXLSXWriter(PyexcelWriterBase):
    def setUp(self):
        self.testfile="test.xls"
        self.testfile2="test.xlsx"

    def tearDown(self):
        file_list = [self.testfile, self.testfile2]
        clean_up_files(file_list)


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
            "X": ["1", "2", "3", "4", "5"],
            "Y": ["6", "7", "8", "9", "10"],
            "Z": ["11", "12", "13", "14", "15"]
        }
        w = pe.Writer(self.testfile)
        w.write_dict(self.content)
        w.close()
        self.testfile2 = "test.xlsm"

    def test_content_is_read(self):
        r = pe.SeriesReader(self.testfile)
        content = pe.utils.to_dict(r)
        print(content)
        assert content == self.content

    def test_write_simple_reader(self):
        r = pe.Reader(self.testfile)
        w = pe.Writer(self.testfile2)
        w.write_reader(r)
        w.close()
        r2 = pe.SeriesReader(self.testfile2)
        content = pe.utils.to_dict(r2)
        assert content == self.content

    def test_write_series_reader(self):
        r = pe.SeriesReader(self.testfile)
        w = pe.Writer(self.testfile2)
        w.write_reader(r)
        w.close()
        r2 = pe.SeriesReader(self.testfile2)
        content = pe.utils.to_dict(r2)
        assert content == self.content

    def test_write_simple_reader_error(self):
        try:
            w = pe.Writer(self.testfile2)
            w.write_reader("abc")  # boom
            assert 1==2
        except TypeError:
            assert 1==1

    def tearDown(self):
        file_list = [self.testfile, self.testfile2]
        clean_up_files(file_list)


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
        w = pe.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()


    def test_write_book_reader(self):
        reader = pe.BookReader(self.testfile)
        writer = pe.BookWriter(self.testfile2)
        writer.write_book_reader(reader)
        writer.close()
        reader2 = pe.BookReader(self.testfile2)
        data = pe.utils.to_dict(reader2)
        assert data == self.content

    def test_not_supported_file(self):
        try:
            pe.BookWriter("bad.format")
        except NotImplementedError:
            assert 1==1

    def tearDown(self):
        file_list = [self.testfile, self.testfile2]
        clean_up_files(file_list)


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
        w = pe.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()

    def test_write_book_reader(self):
        reader = pe.BookReader(self.testfile)
        writer = pe.BookWriter(self.testfile2)
        writer.write_book_reader(reader)
        writer.close()
        sheet1 = "test_Sheet 1.csv"
        reader1 = pe.Reader(sheet1)
        reader1.apply_formatter(pe.formatters.SheetFormatter(float))
        data = pe.utils.to_array(reader1)
        assert data == self.content["Sheet 1"]
        sheet2 = "test_Sheet 2.csv"
        reader2 = pe.Reader(sheet2)
        reader2.apply_formatter(pe.formatters.SheetFormatter(float))
        data = pe.utils.to_array(reader2)
        assert data == self.content["Sheet 2"]
        sheet3 = "test_Sheet 3.csv"
        reader3 = pe.Reader(sheet3)
        reader3.apply_formatter(pe.formatters.SheetFormatter(float))
        data = pe.utils.to_array(reader3)
        assert data == self.content["Sheet 3"]

    def tearDown(self):
        file_list = [
            self.testfile,
            "test_Sheet 1.csv",
            "test_Sheet 2.csv",
            "test_Sheet 3.csv"
        ]
        clean_up_files(file_list)
