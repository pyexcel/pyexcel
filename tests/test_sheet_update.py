import pyexcel
import os
import datetime
from base import create_sample_file1, PyexcelSheetRWBase


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

    def test_update_a_cell(self):
        r = pyexcel.readers.PlainReader(self.testfile)
        r.cell_value(0, 0, 'k')
        assert r[0][0] == 'k'
        d = datetime.date(2014, 10, 1)
        r.cell_value(0, 1, d)
        assert isinstance(r[0][1], datetime.date) is True
        assert r[0][1].strftime("%d/%m/%y") == "01/10/14"

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
        assert r[2][1] == "k"
        r.clear_filters()
        assert r[2][3] == "k"

    def test_set_column_at(self):
        r = pyexcel.PlainReader(self.testfile)
        try:
            r.set_column_at(1, [11, 1], 1000)
            assert 1 == 2
        except ValueError:
            assert 1 == 1

    def test_set_item(self):
        r = pyexcel.Reader(self.testfile)
        content = ['r', 's', 't', 'o']
        r[1] = content
        assert r[1] == ['r', 's', 't', 'o']
        content2 = [1, 2, 3, 4]
        r[1:] = content2
        assert r[2] == [1, 2, 3, 4]
        content3 = [True, False, True, False]
        r[0:0] = content3
        assert r[0] == [True, False, True, False]
        r[0:2:1] = [1, 1, 1, 1]
        assert r[0] == [1, 1, 1, 1]
        assert r[1] == [1, 1, 1, 1]
        assert r[2] == [1, 2, 3, 4]
        try:
            r[2:1] = ['e', 'r', 'r', 'o']
            assert 1 == 2
        except ValueError:
            assert 1 == 1

    def test_delete_item(self):
        r = pyexcel.readers.PlainReader(self.testfile)
        content = ['i', 'j', 1.1, 1]
        assert r[2] == content
        del r[0]
        assert r[1] == content
        r2 = pyexcel.readers.PlainReader(self.testfile)
        del r2[1:]
        assert r2.number_of_rows() == 1
        r3 = pyexcel.readers.PlainReader(self.testfile)
        del r3[0:0]
        assert r3[1] == content
        assert r3.number_of_rows() == 2
        try:
            del r[2:1]
            assert 1 == 2
        except ValueError:
            assert 1 == 1

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
        w = pyexcel.Writer(self.testfile)
        data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

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
        self.rows = 3
        w = pyexcel.Writer(self.testfile)
        data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

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
        w = pyexcel.Writer(self.testfile)
        for i in [0, 4, 8]:
            array = [i+1, i+2, i+3, i+4]
            w.write_row(array)
        w.close()

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
        assert r[3] == content[3]

    def test_delete_rows_even_row_filter(self):
        r = pyexcel.Reader(self.testfile)
        r.filter(pyexcel.filters.EvenRowFilter())
        assert r.number_of_rows() == 2
        assert r.number_of_columns() == 4
        result = [1, 2, 3, 4, 9, 10, 11, 12]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual
        del r[0]
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
        assert r[0] == [2, 4, 'c2']
        assert r[1] == [6, 8, 'x2']
        assert r[2] == [10, 12, '']

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
