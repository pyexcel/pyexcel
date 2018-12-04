import os
import sys

from base import create_sample_file1
from _compact import BytesIO

import pyexcel as pe
from nose.tools import eq_, raises


def do_read_stringio(file_name):
    create_sample_file1(file_name)
    file_type = file_name.split(".")[-1]
    open_flag = "rb"
    if file_type in ["csv", "tsv"]:
        open_flag = "r"
    with open(file_name, open_flag) as f:
        content = f.read()
        r = pe.get_sheet(file_type=file_type, file_content=content)
        result = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 1.1, 1]
        actual = list(r.enumerate())
        eq_(result, actual)
    if os.path.exists(file_name):
        os.unlink(file_name)


def do_book_read_stringio(file_name):
    create_sample_file1(file_name)
    file_type = file_name.split(".")[-1]
    open_flag = "rb"
    if file_type in ["csv", "tsv"]:
        open_flag = "r"
    with open(file_name, open_flag) as f:
        content = f.read()
        b = pe.get_book(file_type=file_type, file_content=content)
        result = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 1.1, 1]
        actual = list(b[0].enumerate())
        eq_(result, actual)
    if os.path.exists(file_name):
        os.unlink(file_name)


def do_write_stringio(file_type):
    data = [[1, 2, 3], [4, 5, 6]]
    io = pe.save_as(dest_file_type=file_type, array=data)
    r = pe.get_sheet(file_type=file_type, file_content=io.getvalue())
    result = [1, 2, 3, 4, 5, 6]
    actual = list(r.enumerate())
    eq_(result, actual)


def do_write_stringio2(file_type):
    data = [[1, 2, 3], [4, 5, 6]]
    r = pe.Sheet(data)
    getter = getattr(r, "get_" + file_type)
    content = getter()
    r = pe.load_from_memory(file_type, content)
    result = [1, 2, 3, 4, 5, 6]
    actual = list(r.enumerate())
    eq_(result, actual)


class TestIO:
    @raises(IOError)
    def test_wrong_io_input(self):
        pe.Reader(1000)

    def test_csv_stringio(self):
        do_read_stringio("cute.csv")

    def test_xls_stringio(self):
        do_read_stringio("cute.xls")

    def test_book_stringio(self):
        do_book_read_stringio("cute-book.xls")

    def test_csv_output_stringio(self):
        do_write_stringio("csv")

    def test_csv_output_stringio2(self):
        do_write_stringio2("csv")

    def test_csvz_stringio(self):
        do_read_stringio("cute.csvz")

    def test_csvz_output_stringio(self):
        do_write_stringio("csvz")

    def test_csvz_output_stringio2(self):
        do_write_stringio2("csvz")

    def test_tsvz_stringio(self):
        do_read_stringio("tsvz")

    def test_tsvz_output_stringio(self):
        do_write_stringio("tsvz")

    def test_tsvz_output_stringio2(self):
        do_write_stringio2("tsvz")

    def test_xls_output_stringio(self):
        do_write_stringio2("xls")

    def test_xlsm_output_stringio(self):
        do_write_stringio2("xlsm")

    def test_book_output_stringio(self):
        data = {"Sheet 1": [[1, 2, 3], [4, 5, 6]]}
        io = pe.save_book_as(dest_file_type="xlsm", bookdict=data)
        b = pe.load_book_from_memory("xlsm", io.getvalue())
        result = [1, 2, 3, 4, 5, 6]
        actual = list(b[0].enumerate())
        eq_(result, actual)

    def test_book_save_to_stringio(self):
        data = {"Sheet 1": [[1, 2, 3], [4, 5, 6]]}
        book = pe.Book(data)
        io = BytesIO()
        book.save_to_memory("xlsm", io)
        b = pe.load_book_from_memory("xlsm", io.getvalue())
        result = [1, 2, 3, 4, 5, 6]
        actual = list(b[0].enumerate())
        eq_(result, actual)


def test_save_sheet_to_sys_stdout():
    data = [[1]]
    sheet = pe.Sheet(data)
    stream = sheet.save_to_memory("csv", sys.stdout)
    eq_(stream.getvalue(), "1\r\n")


def test_save_book_to_sys_stdout():
    data = {"sheet": [[1]]}
    book = pe.Book(data)
    stream = book.save_to_memory("csv", sys.stdout)
    eq_(stream.getvalue(), "1\r\n")
