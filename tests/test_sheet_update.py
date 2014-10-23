import pyexcel
import os
from base import (create_sample_file1,
                  create_sample_file1_series,
                  create_sample_file2,
                  PyexcelSheetRWBase)


class TestReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        create_sample_file1(self.testfile)

    def test_set_named_column_at(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.set_named_column_at('b', [11, 1])
        assert r.column_at(1) == [11, 1]
        r2 = pyexcel.Reader(self.testfile)
        r2.set_named_column_at('b', [11, 1])
        assert r2.column_at(1) == ['b', 11, 1]

    def test_update_a_cell_with_a_filter(self):
        """
        Filter the sheet first and then update the filtered now

        with the filter, you can set its value. then clear
        the filters, the value stays with the cell. so if you want
        to save the change with original data, please clear the filter
        first
        """
        r = pyexcel.FilterableReader(self.testfile)
        r.filter(pyexcel.filters.ColumnFilter([0, 2]))
        r.cell_value(2, 1, "k")
        assert r[2,1] == "k"
        r.clear_filters()
        assert r[2,3] == "k"

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestPlainReader(PyexcelSheetRWBase):
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testclass = pyexcel.PlainReader
        self.testfile = "testcsv.csv"
        self.rows = 3
        create_sample_file1(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestReader2(PyexcelSheetRWBase):
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testclass = pyexcel.Reader
        self.testfile = "testcsv.csv"
        create_sample_file1(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
            
class TestSeriesReader(PyexcelSheetRWBase):
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testclass = pyexcel.SeriesReader
        self.testfile = "testcsv.csv"
        create_sample_file1_series(self.testfile)

    def test_extend_columns(self):
        r = self.testclass(self.testfile)
        columns = [
            ['p', 'a', 'd'],
            ['c1', 'c2', 'c3'],
            ['x1', 'x2', 'x4']]
        r.extend_columns(columns)
        assert r.row[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r.row[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r.row[2] == ['i', 'j', 1.1, 1, '', '', '']
        r2 = self.testclass(self.testfile)
        columns2 = [
            ['p', 'a', 'd'],
            ['c1', 'c2', 'c3'],
            ['x1', 'x2', 'x4'],
            ['y1', 'y2'],
            ['z1']]
        r2.extend_columns(columns2)
        assert r2.row[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r2.row[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r2.row[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r2.row[3] == ['', '', '', '', 'z1', '', '']

    def test_add_as_columns(self):
        # test += operator
        columns2 = [
            [1,2,3],  # padded to make the rest of the test the same
            ['c1', 'c2', 'c3'],
            ['x1', 'x2', 'x4'],
            ['y1', 'y2'],
            ['z1']]
        r3 = self.testclass(self.testfile)
        r3 += pyexcel.sheets.AS_COLUMNS(columns2)
        assert r3.row[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r3.row[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r3.row[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r3.row[3] == ['', '', '', '', 'z1', '', '']
        r4 = self.testclass(self.testfile)
        sheet = pyexcel.sheets.Sheet(columns2, "test")
        r4 += pyexcel.sheets.AS_COLUMNS(sheet)
        assert r4.row[0] == ['a', 'b', 'c', 'd', 'c1', 'c2', 'c3']
        assert r4.row[1] == ['e', 'f', 'g', 'h', 'x1', 'x2', 'x4']
        assert r4.row[2] == ['i', 'j', 1.1, 1, 'y1', 'y2', '']
        assert r4.row[3] == ['', '', '', '', 'z1', '', '']

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestReaderWithFilter:
    def setUp(self):
        """
        Make a test csv file as:

        1, 2, 3, 4
        5, 6, 7, 8
        9, 10,11,12
        """
        self.testfile = "test.csv"
        create_sample_file2(self.testfile)

    def test_add_rows_even_row_filter(self):
        r = pyexcel.Reader(self.testfile)
        r.filter(pyexcel.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        content = [['r', 's', 't', 'o'],  # 4
                   [1, 2, 3, 4],  # 5
                   [True],  # 6
                   [1.1, 2.2, 3.3, 4.4, 5.5]]  # 7
        r.extend_rows(content)
        assert r.row[3] == content[3]

    def test_add_rows_even_row_filter2(self):
        r = pyexcel.readers.FilterableReader(self.testfile)
        r.filter(pyexcel.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        content = [['r', 's', 't', 'o'],  # 4
                   [1, 2, 3, 4],  # 5
                   [True],  # 6
                   [1.1, 2.2, 3.3, 4.4, 5.5]]  # 7
        r.extend_rows(content)
        assert r.row[3] == content[3]

    def test_delete_rows_even_row_filter(self):
        r = pyexcel.Reader(self.testfile)
        r.filter(pyexcel.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        del r.row[0]
        result = [5, 6, 7, 8]
        actual = pyexcel.utils.to_array(r.enumerate())

    def test_add_rows_odd_column_filter(self):
        r = pyexcel.Reader(self.testfile)
        r.filter(pyexcel.filters.OddColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        #             5     6    7
        columns = [['c1', 'c2', 'c3'],
                   ['x1', 'x2', 'x4']]
        r.extend_columns(columns)
        assert r.row[0] == [2, 4, 'c2']
        assert r.row[1] == [6, 8, 'x2']
        assert r.row[2] == [10, 12, '']

    def test_delete_rows_odd_column_filter(self):
        r = pyexcel.Reader(self.testfile)
        r.filter(pyexcel.filters.OddColumnFilter())
        assert r.number_of_rows() == 3
        assert r.number_of_columns() == 2
        result = [2, 4, 6, 8, 10, 12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        #             5     6    7
        r.delete_columns([0])
        result = [3, 7, 11]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
