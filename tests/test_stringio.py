import os
import pyexcel as pe
from _compact import BytesIO, StringIO
from base import create_sample_file1
from nose.tools import raises


class TestIO:
    @raises(IOError)
    def test_wrong_io_input(self):
        pe.Reader(1000)

        
    def test_csv_stringio(self):
        csvfile = "cute.csv"
        create_sample_file1(csvfile)
        with open(csvfile, "r") as f:
            content = f.read()
            r = pe.load_from_memory("csv", content)
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', '1.1', '1']
            actual = pe.utils.to_array(r.enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_xls_stringio(self):
        csvfile = "cute.xls"
        create_sample_file1(csvfile)
        with open(csvfile, "rb") as f:
            content = f.read()
            r = pe.load_from_memory("xls", content)
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
            actual = pe.utils.to_array(r.enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_book_stringio(self):
        csvfile = "cute.xls"
        create_sample_file1(csvfile)
        with open(csvfile, "rb") as f:
            content = f.read()
            b = pe.load_book_from_memory("xls", content)
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
            actual = pe.utils.to_array(b[0].enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_csv_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = pe.save_as(dest_file_type="csv", array=data)
        r = pe.Reader(("csv", io.getvalue()))
        result=['1', '2', '3', '4', '5', '6']
        actual = pe.utils.to_array(r.enumerate())
        assert actual == result

    def test_csv_output_stringio2(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        r = pe.Sheet(data)
        io = StringIO()
        r.save_to_memory("csv", io)
        r = pe.load_from_memory("csv", io.getvalue())
        result=['1', '2', '3', '4', '5', '6']
        actual = pe.utils.to_array(r.enumerate())
        assert actual == result

    def test_csvz_stringio(self):
        csvfile = "cute.csvz"
        create_sample_file1(csvfile)
        with open(csvfile, "rb") as f:
            content = f.read()
            r = pe.load_from_memory("csvz", content)
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', '1.1', '1']
            actual = pe.utils.to_array(r.enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_csvz_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = pe.save_as(dest_file_type="csvz", array=data)
        r = pe.Reader(("csvz", io.getvalue()))
        result=['1', '2', '3', '4', '5', '6']
        actual = pe.utils.to_array(r.enumerate())
        assert actual == result

    def test_csvz_output_stringio2(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        r = pe.Sheet(data)
        io = BytesIO()
        r.save_to_memory("csvz", io)
        r = pe.load_from_memory("csvz", io.getvalue())
        result=['1', '2', '3', '4', '5', '6']
        actual = pe.utils.to_array(r.enumerate())
        assert actual == result

    def test_tsvz_stringio(self):
        csvfile = "cute.tsvz"
        create_sample_file1(csvfile)
        with open(csvfile, "rb") as f:
            content = f.read()
            r = pe.load_from_memory("tsvz", content)
            result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', '1.1', '1']
            actual = pe.utils.to_array(r.enumerate())
            assert result == actual
        if os.path.exists(csvfile):
            os.unlink(csvfile)

    def test_tsvz_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = pe.save_as(dest_file_type="tsvz", array=data)
        r = pe.Reader(("tsvz", io.getvalue()))
        result=['1', '2', '3', '4', '5', '6']
        actual = pe.utils.to_array(r.enumerate())
        assert actual == result

    def test_tsvz_output_stringio2(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        r = pe.Sheet(data)
        io = BytesIO()
        r.save_to_memory("tsvz", io)
        r = pe.load_from_memory("tsvz", io.getvalue())
        result=['1', '2', '3', '4', '5', '6']
        actual = pe.utils.to_array(r.enumerate())
        assert actual == result

    def test_xls_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = pe.save_as(dest_file_type="xls",array=data)
        r = pe.load_from_memory("xls", io.getvalue())
        result=[1, 2, 3, 4, 5, 6]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_xlsm_output_stringio(self):
        data = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        io = pe.save_as(dest_file_type="xlsm",array=data)
        r = pe.load_from_memory("xlsm", io.getvalue())
        result=[1, 2, 3, 4, 5, 6]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_book_output_stringio(self):
        data = {
            "Sheet 1": [
                [1, 2, 3],
                [4, 5, 6]
            ]
        }
        io = pe.save_book_as(dest_file_type="xlsm",bookdict=data)
        b = pe.load_book_from_memory("xlsm", io.getvalue())
        result=[1, 2, 3, 4, 5, 6]
        actual = pe.utils.to_array(b[0].enumerate())
        assert result == actual

    def test_book_save_to_stringio(self):
        data = {
            "Sheet 1": [
                [1, 2, 3],
                [4, 5, 6]
            ]
        }
        book = pe.Book(data)
        io = BytesIO()
        book.save_to_memory("xlsm", io)
        b = pe.load_book_from_memory("xlsm", io.getvalue())
        result=[1, 2, 3, 4, 5, 6]
        actual = pe.utils.to_array(b[0].enumerate())
        assert result == actual
