import os
from unittest import TestCase
import pyexcel as pe
from base import create_sample_file2_in_memory
from nose.tools import eq_


class TestRareCases(TestCase):
    def test_empty_column_filter(self):
        data = [
            [1, 2, 3]
        ]
        s = pe.Sheet(data)
        s.add_filter(pe.sheets.filters.ColumnFilter([100]))
        result = s.array
        self.assertEqual(data, result)

    def test_empty_row_filter(self):
        data = [
            [1, 2, 3]
        ]
        s = pe.Sheet(data)
        s.add_filter(pe.sheets.filters.RowFilter([100]))
        result = s.array
        self.assertEqual(data, result)

    def test_row_value_filter_with_series_reader(self):
        data = "Person,Age\nAdam,24\nBilly,23\nCeri,28\nDennis,25"
        r1 = pe.SeriesReader(("csv", data))

        def filter_func(row): return row['Age'] == 23
        r1.filter(pe.sheets.filters.SeriesRowValueFilter(filter_func).invert())
        self.assertEqual(r1.number_of_rows(), 1)
        self.assertEqual(r1.row[0], ['Billy', 23])


class TestFilterWithFilterableReader:
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.file_type = "xlsm"
        self.testfile = create_sample_file2_in_memory(self.file_type)

    def test_use_filter_reader_without_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.ColumnFilter([0, 2]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out last column and first column
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.ColumnFilter([0, 3]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 3, 6, 7, 10, 11]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out all
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.ColumnFilter([0, 1, 2, 3]))
        assert r.number_of_columns() == 0
        result = []
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_single_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.SingleColumnFilter(0))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 3
        result = [2, 3, 4, 6, 7, 8, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_single_column_filter_double_invert(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.SingleColumnFilter(0).invert().invert())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 3
        result = [2, 3, 4, 6, 7, 8, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_column_filter_with_invalid_indices(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.ColumnFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_column_index_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))

        def test_func(x): return x in [0, 2]
        r.add_filter(pe.sheets.filters.ColumnIndexFilter(test_func))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_even_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.EvenColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [1, 3, 5, 7, 9, 11]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_odd_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.OddColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.RowFilter([1]))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out last column and first column
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.RowFilter([0, 2]))
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out all
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.RowFilter([0, 1, 2]))
        assert r.number_of_rows() == 0
        result = []
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_single_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.SingleRowFilter(1))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_row_filter_with_invalid_indices(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.RowFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_row_index_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))

        def filter_func(x): return x in [1]
        r.add_filter(pe.sheets.filters.RowIndexFilter(filter_func))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_even_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_odd_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.sheets.filters.OddRowFilter())
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_two_filters(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        f1 = pe.sheets.filters.OddRowFilter()
        f2 = pe.sheets.filters.OddColumnFilter()
        r.add_filter(f1)
        r.add_filter(f2)
        assert r.number_of_columns() == 2
        assert r.number_of_rows() == 1
        result = [6, 8]
        actual = list(r.enumerate())
        eq_(result, actual)


class TestFilterWithReader:
    def setUp(self):
        """
        Make a test csv file as:

        1, 2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.file_type = "xlsx"
        self.testfile = create_sample_file2_in_memory(self.file_type)

    def test_use_filter_reader_without_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_column_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.ColumnFilter([0, 2]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out last column and first column
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.ColumnFilter([0, 3]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 3, 6, 7, 10, 11]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out all
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.ColumnFilter([0, 1, 2, 3]))
        assert r.number_of_columns() == 0
        result = []
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_column_filter_with_invalid_indices(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.ColumnFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_column_index_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)

        def test_func(x): return x in [0, 2]
        r.add_filter(pe.sheets.filters.ColumnIndexFilter(test_func))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_even_column_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.EvenColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [1, 3, 5, 7, 9, 11]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_odd_column_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.OddColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_row_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.RowFilter([1]))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out last column and first column
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.RowFilter([0, 2]))
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = list(r.enumerate())
        eq_(result, actual)
        # filter out all
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.RowFilter([0, 1, 2]))
        assert r.number_of_rows() == 0
        result = []
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_row_filter_with_invalid_indices(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.RowFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_row_index_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)

        def filter_func(x): return x in [1]
        r.add_filter(pe.sheets.filters.RowIndexFilter(filter_func))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_even_row_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = list(r.enumerate())
        eq_(result, actual)

    def test_odd_row_filter(self):
        r = pe.get_sheet(file_type=self.file_type, file_stream=self.testfile)
        r.filter(pe.sheets.filters.OddRowFilter())
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = list(r.enumerate())
        eq_(result, actual)


class TestComplexFilter(TestCase):
    def setUp(self):
        """
        Make a test csv file as:

        1, 2, 3, 4
        5, 6, 7, 8
        9, 10, 11, 12
        """
        self.testfile1 = "testcsv1.csv"
        content = [
            [1, 'a'],
            [2, 'b'],
            [3, 'c'],
            [4, 'd'],
            [5, 'e'],
            [6, 'f'],
            [7, 'g'],
            [8, 'h']
        ]
        pe.save_as(dest_file_name=self.testfile1,
                   array=content)
        self.testfile2 = "testcsv2.csv"
        content = [
            [1, 'a', 'c'],
            [2, 'b', 'h'],
            [3, 'c', 'c'],
            [8, 'h', 'd']
        ]
        pe.save_as(dest_file_name=self.testfile2,
                   array=content)

    def test_row_value_filter(self):
        r1 = pe.load("testcsv1.csv")
        r2 = pe.load("testcsv2.csv")

        def filter_func(array):
            def func(row): return array[0] == row[0] and array[1] == row[1]
            return r2.contains(func)
        r1.filter(pe.sheets.filters.RowValueFilter(filter_func).invert())
        result = [1, 'a', 2, 'b', 3, 'c', 8, 'h']
        actual = list(r1.enumerate())
        self.assertEqual(result, actual)

    def test_row_in_file_filter(self):
        r1 = pe.load("testcsv1.csv")
        r2 = pe.load("testcsv2.csv")
        r2.filter(pe.sheets.filters.ColumnFilter([2]))
        r1.filter(pe.sheets.filters.RowInFileFilter(r2))
        result = [1, 'a', 2, 'b', 3, 'c', 8, 'h']
        actual = list(r1.enumerate())
        self.assertEqual(result, actual)

    def tearDown(self):
        if os.path.exists(self.testfile1):
            os.unlink(self.testfile1)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestRegionFilter:
    def test_normal_usage(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
            ]
        s = pe.Sheet(data)
        s.filter(pe.sheets.filters.RegionFilter(
            slice(1, 4, 1), slice(1, 5, 1)))
        expected = [
            [22, 23, 24, 25],
            [32, 33, 34, 35],
            [42, 43, 44, 45]
        ]
        assert s.to_array() == expected

    def test_normal_usage2(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7],  # 0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
            ]
        s = pe.Sheet(data)
        s.add_filter(pe.sheets.filters.RegionFilter(
            slice(1, 4, 1), slice(1, 5, 1)))
        expected = [
            [22, 23, 24, 25],
            [32, 33, 34, 35],
            [42, 43, 44, 45]
        ]
        assert s.to_array() == expected


class TestColumnValueFilter:
    def test_row_value_filter(self):
        data = [
            ['a', 'b', 'c', 'd', 'e'],
            [1, 2, 3, 4, 1]
        ]
        sheet = pe.Sheet(data)

        def func(column): return column[1] == 1
        sheet.filter(pe.ColumnValueFilter(func).invert())
        expected = [
            ['a', 'e'],
            [1, 1]
        ]
        assert sheet.to_array() == expected


class TestNamedRowValueFilter:
    def test_row_value_filter(self):
        data = [
            ['a', 'b', 'c', 'd', 'e'],
            [1, 2, 3, 4, 1],
            [2, 3, 4, 5, 7],
            [3, 4, 5, 6, 7]
        ]
        sheet = pe.Sheet(data, name_columns_by_row=0)

        def func(row): return row['a'] == 3
        sheet.filter(pe.NamedRowValueFilter(func).invert())
        expected = [
            ['a', 'b', 'c', 'd', 'e'],
            [3, 4, 5, 6, 7]
        ]
        assert sheet.to_array() == expected


class TestNamedColumnValueFilter(TestCase):
    def test_row_value_filter(self):
        data = [
            ['a', 1, 2, 3, 4, 1],
            ['b', 2, 3, 4, 5, 7],
            ['c', 3, 4, 5, 6, 7]
        ]
        sheet = pe.Sheet(data, name_rows_by_column=0)

        def func(column): return column['a'] == 3
        sheet.filter(pe.NamedColumnValueFilter(func).invert())
        expected = [
            ['a', 3],
            ['b', 4],
            ['c', 5]
        ]
        self.assertEqual(sheet.to_array(), expected)
