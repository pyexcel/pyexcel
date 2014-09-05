import unittest
import os
import pyexcel


class TestFilter(unittest.TestCase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        w = pyexcel.Writer(self.testfile)
        for i in [0,4,8]:
            array = [i+1, i+2, i+3, i+4]
            w.write_row(array)
        w.close()

    def test_column_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([0,2]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2,4,6,8,10,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        # filter out last column and first column
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([0,3]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2,3,6,7,10,11]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        # filter out all
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([0,1,2,3]))
        assert r.number_of_columns() == 0
        result = []
        actual = pyexcel.utils.to_array(r)
        assert result == actual
    
    def test_column_filter_with_invalid_indices(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([11,-1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        
    def test_column_index_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        test_func = lambda x: x in [0,2]
        r.filter(pyexcel.filters.ColumnIndexFilter(test_func))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2,4,6,8,10,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        
    def test_row_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.RowFilter([1]))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1,2,3,4,9,10,11,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        # filter out last column and first column
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.RowFilter([0,2]))
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5,6,7,8]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        # filter out all
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.RowFilter([0,1,2]))
        assert r.number_of_rows() == 0
        result = []
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        
    def test_row_filter_with_invalid_indices(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.RowFilter([11,-1]))
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 4
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        
    def test_row_index_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        filter_func = lambda x: x in [1]
        r.filter(pyexcel.filters.RowIndexFilter(filter_func))
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1,2,3,4,9,10,11,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
