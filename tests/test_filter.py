import os
import pyexcel


class TestFilter:
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
        
    def test_use_filter_reader_without_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual

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
        
    def test_even_column_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.EvenColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [1,3,5,7,9,11]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        
    def test_odd_column_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.OddColumnFilter())
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
        
    def test_even_row_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1,2,3,4,9,10,11,12]
        actual = pyexcel.utils.to_array(r)
        assert result == actual
        
    def test_odd_row_filter(self):
        r = pyexcel.FilterReader(self.testfile)
        r.filter(pyexcel.filters.OddRowFilter())
        assert r.number_of_rows() == 1
        assert r.number_of_columns() == 4
        result = [5,6,7,8]
        actual = pyexcel.utils.to_array(r)
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

class TestComplexFilter:
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile1 = "testcsv1.csv"
        w = pyexcel.Writer(self.testfile1)
        content = [
            [1,'a'],
            [2,'b'],
            [3,'c'],
            [4,'d'],
            [5,'e'],
            [6,'f'],
            [7,'g'],
            [8,'h']
        ]
        w.write_table(content)
        w.close()
        self.testfile2 = "testcsv2.csv"
        w = pyexcel.Writer(self.testfile2)
        content = [
            [1,'a','c'],
            [2,'b','h'],
            [3,'c','c'],
            [8,'h','d']
        ]
        w.write_table(content)
        w.close()

    def test_row_value_filter(self):
        r1 = pyexcel.FilterReader("testcsv1.csv")
        r2 = pyexcel.Reader("testcsv2.csv")
        filter_func = lambda array: r2.contains((lambda row: array[0] == row[0] and array[1] == row[1]))
        r1.filter(pyexcel.filters.RowValueFilter(filter_func))
        result = [1, 'a', 2, 'b', 3, 'c', 8, 'h']
        actual = pyexcel.utils.to_array(r1)
        assert result == actual

    def test_row_in_file_filter(self):
        r1 = pyexcel.FilterReader("testcsv1.csv")
        r2 = pyexcel.FilterReader("testcsv2.csv")
        r2.filter(pyexcel.filters.ColumnFilter([2]))
        r1.filter(pyexcel.filters.RowInFileFilter(r2))
        result = [1, 'a', 2, 'b', 3, 'c', 8, 'h']
        actual = pyexcel.utils.to_array(r1)
        assert result == actual        
        
    def tearDown(self):
        if os.path.exists(self.testfile1):
            os.unlink(self.testfile1)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestHeaderFilter:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = [
            ["X", "Y", "Z"],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3]
        ]
        w = pyexcel.Writer(self.testfile)
        w.write_table(self.content)
        w.close()

    def test_content_is_read(self):
        r = pyexcel.HatReader(self.testfile)
        actual = pyexcel.utils.to_array(r.rows())
        assert self.content[1:] == actual

    def test_headers(self):
        r = pyexcel.HatReader(self.testfile)
        actual = r.hat()
        assert self.content[0] == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        