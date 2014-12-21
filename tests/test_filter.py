import os
import pyexcel as pe
from base import create_sample_file2_in_memory


class TestRareCases:
    def test_validate(self):
        ifr = pe.filters.IndexFilter(None)
        ifr.validate_filter(None)
        ifr.translate(1,2)
        assert 1==1

    def test_empty_column_filter(self):
        data = [
            [1,2,3]
        ]
        s = pe.sheets.FilterableSheet(data)
        s.add_filter(pe.filters.ColumnFilter([100]))
        result = pe.utils.to_array(s)
        assert data == result

    def test_empty_row_filter(self):
        data = [
            [1,2,3]
        ]
        s = pe.sheets.FilterableSheet(data)
        s.add_filter(pe.filters.RowFilter([100]))
        result = pe.utils.to_array(s)
        assert data == result

    def test_row_value_filter_with_series_reader(self):
        data = "Person,Age\nAdam,24\nBilly,23\nCeri,28\nDennis,25"
        r1 = pe.SeriesReader(("csv", data))
        filter_func = lambda row: row['Age'] == '23'
        r1.filter(pe.filters.SeriesRowValueFilter(filter_func).invert())
        assert r1.number_of_rows() == 1
        assert r1.row[0] == ['Billy', '23']


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
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.ColumnFilter([0, 2]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out last column and first column
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.ColumnFilter([0, 3]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 3, 6, 7, 10, 11]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out all
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.ColumnFilter([0, 1, 2, 3]))
        assert r.number_of_columns() == 0
        result = []
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_single_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.SingleColumnFilter(0))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 3
        result = [2, 3, 4, 6, 7, 8, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_single_column_filter_double_invert(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.SingleColumnFilter(0).invert().invert())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 3
        result = [2, 3, 4, 6, 7, 8, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_column_filter_with_invalid_indices(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.ColumnFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_column_index_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        test_func = lambda x: x in [0, 2]
        r.add_filter(pe.filters.ColumnIndexFilter(test_func))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # test removing the filter,  it prints the original one
        r.clear_filters()
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_even_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.EvenColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [1, 3, 5, 7, 9, 11]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_odd_column_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.OddColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.RowFilter([1]))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out last column and first column
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.RowFilter([0, 2]))
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out all
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.RowFilter([0, 1, 2]))
        assert r.number_of_rows() == 0
        result = []
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_single_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.SingleRowFilter(1))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        
    def test_row_filter_with_invalid_indices(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.RowFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_row_index_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        filter_func = lambda x: x in [1]
        r.add_filter(pe.filters.RowIndexFilter(filter_func))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # test removing the filter,  it prints the original one
        r.clear_filters()
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_even_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_odd_row_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        r.filter(pe.filters.OddRowFilter())
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_two_filters(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        f1 = pe.filters.OddRowFilter()
        f2 = pe.filters.OddColumnFilter()
        r.add_filter(f1)
        r.add_filter(f2)
        assert r.number_of_columns() == 2
        assert r.number_of_rows() == 1
        result = [6, 8]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        r.remove_filter(f1)
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_remove_filter(self):
        r = pe.load((self.file_type, self.testfile.getvalue()))
        f = pe.filters.OddRowFilter()
        r.add_filter(f)
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        r.remove_filter(f)
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual


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
        self.test_tuple = (self.file_type, self.testfile.getvalue())

    def test_use_filter_reader_without_filter(self):
        r = pe.load(self.test_tuple)
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_column_filter(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.ColumnFilter([0, 2]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out last column and first column
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.ColumnFilter([0, 3]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 3, 6, 7, 10, 11]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out all
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.ColumnFilter([0, 1, 2, 3]))
        assert r.number_of_columns() == 0
        result = []
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_column_filter_with_invalid_indices(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.ColumnFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_column_index_filter(self):
        r = pe.load(self.test_tuple)
        test_func = lambda x: x in [0, 2]
        r.add_filter(pe.filters.ColumnIndexFilter(test_func))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # test removing the filter,  it prints the original one
        r.clear_filters()
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_even_column_filter(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.EvenColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [1, 3, 5, 7, 9, 11]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_odd_column_filter(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.OddColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_row_filter(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.RowFilter([1]))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out last column and first column
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.RowFilter([0, 2]))
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # filter out all
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.RowFilter([0, 1, 2]))
        assert r.number_of_rows() == 0
        result = []
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_row_filter_with_invalid_indices(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.RowFilter([11, -1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_row_index_filter(self):
        r = pe.load(self.test_tuple)
        filter_func = lambda x: x in [1]
        r.add_filter(pe.filters.RowIndexFilter(filter_func))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual
        # test removing the filter,  it prints the original one
        r.clear_filters()
        result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_even_row_filter(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def test_odd_row_filter(self):
        r = pe.load(self.test_tuple)
        r.filter(pe.filters.OddRowFilter())
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5, 6, 7, 8]
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual


class TestComplexFilter:
    def setUp(self):
        """
        Make a test csv file as:

        1, 2, 3, 4
        5, 6, 7, 8
        9, 10, 11, 12
        """
        self.testfile1 = "testcsv1.csv"
        w = pe.Writer(self.testfile1)
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
        w.write_array(content)
        w.close()
        self.testfile2 = "testcsv2.csv"
        w = pe.Writer(self.testfile2)
        content = [
            [1, 'a', 'c'],
            [2, 'b', 'h'],
            [3, 'c', 'c'],
            [8, 'h', 'd']
        ]
        w.write_array(content)
        w.close()

    def test_row_value_filter(self):
        r1 = pe.load("testcsv1.csv")
        r2 = pe.load("testcsv2.csv")
        filter_func = lambda array: r2.contains((lambda row: array[0] == row[0] and array[1] == row[1]))
        r1.filter(pe.filters.RowValueFilter(filter_func).invert())
        result = ['1', 'a', '2', 'b', '3', 'c', '8', 'h']
        actual = pe.utils.to_array(r1.enumerate())
        assert result == actual

    def test_row_in_file_filter(self):
        r1 = pe.load("testcsv1.csv")
        r2 = pe.load("testcsv2.csv")
        r2.filter(pe.filters.ColumnFilter([2]))
        r1.filter(pe.filters.RowInFileFilter(r2))
        result = ['1', 'a', '2', 'b', '3', 'c', '8', 'h']
        actual = pe.utils.to_array(r1.enumerate())
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile1):
            os.unlink(self.testfile1)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)

class TestRegionFilter:
    def test_normal_usage(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7], #  0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
            ]
        s = pe.Sheet(data)
        s.filter(pe.filters.RegionFilter(slice(1,4,1), slice(1,5,1)))
        expected = [
            [22, 23, 24, 25],
            [32, 33, 34, 35],
            [42, 43, 44, 45]
        ]
        assert s.to_array() == expected

    def test_normal_usage2(self):
        data = [
            # 0 1  2  3  4 5   6
            [1, 2, 3, 4, 5, 6, 7], #  0
            [21, 22, 23, 24, 25, 26, 27],
            [31, 32, 33, 34, 35, 36, 37],
            [41, 42, 43, 44, 45, 46, 47],
            [51, 52, 53, 54, 55, 56, 57]  # 4
            ]
        s = pe.Sheet(data)
        s.add_filter(pe.filters.RegionFilter(slice(1,4,1), slice(1,5,1)))
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
        sheet.filter(pe.ColumnValueFilter(lambda column: column[1] == 1).invert())
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
        sheet.filter(pe.NamedRowValueFilter(lambda row: row['a'] == 3).invert())
        expected = [
            ['a', 'b', 'c', 'd', 'e'],
            [3, 4, 5, 6, 7]
        ]
        assert sheet.to_array() == expected


class TestNamedColumnValueFilter:
    def test_row_value_filter(self):
        data = [
            ['a', 1, 2, 3, 4, 1],
            ['b', 2, 3, 4, 5, 7],
            ['c', 3, 4, 5, 6, 7]
        ]
        sheet = pe.Sheet(data, name_rows_by_column=0)
        sheet.filter(pe.NamedColumnValueFilter(lambda column: column['a'] == 3).invert())
        expected = [
            ['a', 3],
            ['b', 4],
            ['c', 5]
        ]
        assert sheet.to_array() == expected

