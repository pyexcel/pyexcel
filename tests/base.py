import os
import json

import pyexcel as pe

import unittest
from nose.tools import eq_, raises


def clean_up_files(file_list):
    for f in file_list:
        if os.path.exists(f):
            os.unlink(f)


def to_json(iterator):
    array = list(iterator)
    return json.dumps(array)


def create_generic_file(filename, array_content):
    pe.save_as(dest_file_name=filename, array=array_content)


def create_sample_file1(filename):
    data = [["a", "b", "c", "d"], ["e", "f", "g", "h"], ["i", "j", 1.1, 1]]
    create_generic_file(filename, data)


def create_sample_file1_series(filename):
    data = [
        ["c1", "c2", "c3", "c4"],
        ["a", "b", "c", "d"],
        ["e", "f", "g", "h"],
        ["i", "j", 1.1, 1],
    ]
    create_generic_file(filename, data)


def create_sample_file2(filename):
    """
    1,2,3,4
    5,6,7,8
    9,10,11,12
    """
    table = []
    for i in [0, 4, 8]:
        array = [i + 1, i + 2, i + 3, i + 4]
        table.append(array)
    create_generic_file(filename, table)


def create_sample_file2_in_memory(file_type):
    """
    1,2,3,4
    5,6,7,8
    9,10,11,12
    """
    table = []
    for i in [0, 4, 8]:
        array = [i + 1, i + 2, i + 3, i + 4]
        table.append(array)
    io = pe.save_as(dest_file_type=file_type, array=table)
    return io


class PyexcelSheetBase(unittest.TestCase):
    filename = "fixtures/non-uniform-rows.csv"

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), self.filename)
        self.sheet = pe.get_sheet(file_name=filename)


class PyexcelBase:
    def _write_test_file(self, filename):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.rows = 3
        table = []
        for i in range(0, self.rows):
            row = i + 1
            array = [row] * 4
            table.append(array)
        create_generic_file(filename, table)

    def test_number_of_rows(self):
        r = pe.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pe.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert row == r.cell_value(i, 1)
        for i in r.row_range():
            assert i + 1 == r.cell_value(i, 1)
        assert 3 == r.cell_value(2, 3)

    def test_row_range(self):
        r = pe.Reader(self.testfile)
        assert self.rows == len(r.row_range())

    def test_number_of_columns(self):
        r = pe.Reader(self.testfile)
        assert 4 == r.number_of_columns()

    @raises(ValueError)
    def test_slice(self):
        r = pe.Reader(self.testfile)
        content1 = [[1, 1, 1, 1]]
        assert content1 == r.row[0:1]
        content2 = [[1, 1, 1, 1], [2, 2, 2, 2]]
        assert content2 == r.row[0:2]
        assert content2 == r.row[:2]
        content3 = [[2, 2, 2, 2], [3, 3, 3, 3]]
        assert content3 == r.row[1:]
        content4 = [[1, 1, 1, 1], [2, 2, 2, 2]]
        assert content4 == r.row[0:2:1]
        content5 = [1, 1, 1, 1]
        assert [content5] == r.row[0:0]
        r.row[2:1]  # bang


class PyexcelMultipleSheetBase:
    def _write_test_file(self, filename):
        pe.save_book_as(dest_file_name=filename, bookdict=self.content)

    def _clean_up(self):
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

    def test_sheet_names(self):
        r = pe.BookReader(self.testfile)
        expected = ["Sheet1", "Sheet2", "Sheet3"]
        sheet_names = r.sheet_names()
        assert sheet_names == expected

    def test_reading_through_sheets(self):
        b = pe.BookReader(self.testfile)
        data = list(b["Sheet1"].rows())
        expected = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
        assert data == expected
        data = list(b["Sheet2"].rows())
        expected = [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]
        assert data == expected
        data = list(b["Sheet3"].rows())
        expected = [[u"X", u"Y", u"Z"], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected
        sheet3 = b["Sheet3"]
        sheet3.name_columns_by_row(0)
        data = list(sheet3.rows())
        expected = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        assert data == expected

    def test_iterate_through_sheets(self):
        b = pe.get_book(file_name=self.testfile)
        for s in b:
            data = s.array
            assert self.content[s.name] == data
        si = pe.internal.common.SheetIterator(b)
        for s in si:
            data = s.array
            assert self.content[s.name] == data

    def test_write_a_book_reader(self):
        b = pe.get_book(file_name=self.testfile)
        b.save_as(self.testfile2)
        x = pe.get_book(file_name=self.testfile2)
        for s in x:
            data = s.array
            assert self.content[s.name] == data

    def test_random_access_operator(self):
        r = pe.get_book(file_name=self.testfile)
        value = r["Sheet1"].row[0][1]
        assert value == 1
        value = r["Sheet3"].row[0][1]
        assert value == "Y"
        r["Sheet3"].name_columns_by_row(0)
        value = r["Sheet3"].row[0][1]
        assert value == 4


class PyexcelIteratorBase:
    @raises(IndexError)
    def test_random_access(self):
        self.iteratable.cell_value(100, 100)

    def test_set_value(self):
        self.iteratable.cell_value(0, 0, 1)
        assert self.iteratable.cell_value(0, 0) == 1

    def test_horizontal_iterator(self):
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(self.iteratable.enumerate())
        eq_(result, actual)

    def test_row_iterator(self):
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = to_one_dimensional_array(self.iteratable.rows())
        eq_(result, actual)

    def test_row_iterator_2_dimensions(self):
        result = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        actual = list(self.iteratable.rows())
        eq_(result, actual)

    def test_horizontal_reverse_iterator(self):
        result = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        actual = list(self.iteratable.reverse())
        eq_(result, actual)

    def test_row_reverse_iterator(self):
        result = [9, 10, 11, 12, 5, 6, 7, 8, 1, 2, 3, 4]
        actual = to_one_dimensional_array(self.iteratable.rrows())
        eq_(result, actual)

    def test_row_reverse_iterator_2_dimensions(self):
        result = [[9, 10, 11, 12], [5, 6, 7, 8], [1, 2, 3, 4]]
        actual = list(self.iteratable.rrows())
        eq_(result, actual)

    def test_vertical_iterator(self):
        result = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
        actual = list(self.iteratable.vertical())
        eq_(result, actual)

    def test_column_iterator(self):
        result = [1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12]
        actual = to_one_dimensional_array(self.iteratable.columns())
        eq_(result, actual)

    def test_column_iterator_2_dimensions(self):
        result = [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
        actual = list(self.iteratable.columns())
        eq_(result, actual)

    def test_vertical_reverse_iterator(self):
        result = [12, 8, 4, 11, 7, 3, 10, 6, 2, 9, 5, 1]
        actual = list(self.iteratable.rvertical())
        eq_(result, actual)

    def test_column_reverse_iterator(self):
        result = [4, 8, 12, 3, 7, 11, 2, 6, 10, 1, 5, 9]
        actual = to_one_dimensional_array(self.iteratable.rcolumns())
        eq_(result, actual)

    def test_column_reverse_iterator_2_dimensions(self):
        result = [[4, 8, 12], [3, 7, 11], [2, 6, 10], [1, 5, 9]]
        actual = list(self.iteratable.rcolumns())
        eq_(result, actual)


class PyexcelSheetRWBase:
    @raises(TypeError)
    def test_extend_rows(self):
        r2 = self.testclass(self.testfile)
        content = [
            ["r", "s", "t", "o"],
            [1, 2, 3, 4],
            [True],
            [1.1, 2.2, 3.3, 4.4, 5.5],
        ]
        r2.row += content
        assert r2.row[3] == ["r", "s", "t", "o", ""]
        assert r2.row[4] == [1, 2, 3, 4, ""]
        assert r2.row[5] == [True, "", "", "", ""]
        assert r2.row[6] == [1.1, 2.2, 3.3, 4.4, 5.5]
        r2.row += 12  # bang


def to_one_dimensional_array(iterator):
    """convert a reader to one dimensional array"""
    array = []
    for i in iterator:
        if type(i) == list:
            array += i
        else:
            array.append(i)
    return array
