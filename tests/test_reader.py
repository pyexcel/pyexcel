import pyexcel
from base import PyexcelBase
from base import PyexcelXlsBase
import os


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
        w = pyexcel.Writer(self.testfile)
        data=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        value = r.cell_value(100,100)
        assert value == None
        value = r.cell_value(0, 1)
        assert value == 'b'

    def test_row_range(self):
        r = pyexcel.Reader(self.testfile)
        row_range = r.row_range()
        assert row_range == range(0,3)

    def test_column_range(self):
        r = pyexcel.Reader(self.testfile)
        column_range = r.column_range()
        assert column_range == range(0,4)

    def test_named_column_at(self):
        r = pyexcel.Reader(self.testfile)
        result = r.named_column_at("A")
        assert result == {}

    def test_get_item_operator(self):
        r = pyexcel.Reader(self.testfile)
        value = r[0][1]
        assert value == 'b'

    def test_row_at(self):
        r = pyexcel.Reader(self.testfile)
        value = r.row_at(100)
        assert value == None
        value = r.row_at(2)
        assert value == ['i', 'j', 1.1, 1]

    def test_column_at(self):
        r = pyexcel.Reader(self.testfile)
        value = r.column_at(100)
        assert value == None
        value = r.column_at(1)
        assert value == ['b','f','j']

    def test_not_supported_file(self):
        try:
            r = pyexcel.Reader("test.sylk")
            assert 0==1
        except NotImplementedError:
            assert 1==1

    def test_out_of_index(self):
        r = pyexcel.Reader(self.testfile)
        try:
            r[10000]
            assert 1!=1
        except IndexError:
            assert 1==1

    def test_contains(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda row: row[0]=='a' and row[1] == 'b'
        assert r.contains(f) == True

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestCSVReader(PyexcelBase):
    """
    Test CSV reader
    """
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "testcsv.csv"
        self._write_test_file(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestCSVReader2:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,k,l
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        w = pyexcel.Writer(self.testfile)
        data=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

    def test_data_types(self):
        r = pyexcel.Reader(self.testfile)
        result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 1.1, 1]
        actual = pyexcel.utils.to_array(r.enumerate())
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestODSReader(PyexcelBase):
    def setUp(self):
        """
        Declare the test xls file.

        It is pre-made as csv file:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.ods"
        self._write_test_file(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestXLSReader(PyexcelXlsBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.xls"
        self._write_test_file(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestXLSXReader(PyexcelXlsBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.xlsx"
        self._write_test_file(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestXLSMReader(PyexcelXlsBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.xlsm"
        self._write_test_file(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestSeriesReader3:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = [
            ["X", "Y", "Z"],
            [1, 1, 1],
            [2, 2, 2],
            [3, 3, 3],
            [4, 4, 4],
            [5, 5, 5]
        ]
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_row_filter(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.add_filter(pyexcel.filters.RowFilter([1]))
        actual = pyexcel.utils.to_dict(r)
        result = {
            "X": [1, 3, 4, 5],
            "Y": [1, 3, 4, 5],
            "Z": [1, 3, 4, 5]
        }
        print actual
        assert result == actual

    def test_odd_row_filter(self):
        r = pyexcel.SeriesReader(self.testfile)
        f = pyexcel.filters.OddRowFilter()
        r.add_filter(f)
        actual = pyexcel.utils.to_dict(r)
        result = {
            "X": [2, 4],
            "Y": [2, 4],
            "Z": [2, 4]
        }
        print actual
        assert result == actual
        r.remove_filter(f)
        actual = pyexcel.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_even_row_filter(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.add_filter(pyexcel.filters.EvenRowFilter())
        actual = pyexcel.utils.to_dict(r)
        result = {
            "X": [1, 3, 5],
            "Y": [1, 3, 5],
            "Z": [1, 3, 5]
        }
        print actual
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pyexcel.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_orthogonality(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.add_filter(pyexcel.filters.EvenRowFilter())
        r.add_filter(pyexcel.filters.OddColumnFilter())
        actual = pyexcel.utils.to_dict(r)
        result = {
            "Y": [1, 3, 5]
        }
        print actual
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pyexcel.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_orthogonality2(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.add_filter(pyexcel.filters.OddColumnFilter())
        r.add_filter(pyexcel.filters.EvenRowFilter())
        actual = pyexcel.utils.to_dict(r)
        result = {
            "Y": [1, 3, 5]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pyexcel.utils.to_array(r)
        print actual
        result = [{'X': [1, 2, 3, 4, 5]}, {'Y': [1, 2, 3, 4, 5]}, {'Z': [1, 2, 3, 4, 5]}]
        assert actual == result

    def test_series_column_iterator(self):
        r = pyexcel.SeriesReader(self.testfile)
        sci = pyexcel.iterators.SeriesColumnIterator(r)
        actual = pyexcel.utils.to_array(sci)
        result = [{'X': [1, 2, 3, 4, 5]}, {'Y': [1, 2, 3, 4, 5]}, {'Z': [1, 2, 3, 4, 5]}]
        assert actual == result

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestSeriesReader4:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]
        ]
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_content_is_read(self):
        r = pyexcel.SeriesReader(self.testfile)
        actual = pyexcel.utils.to_array(r.rows())
        print actual
        assert self.content[1:] == actual

    def test_headers(self):
        r = pyexcel.SeriesReader(self.testfile)
        actual = r.series()
        assert self.content[0] == actual

    def test_named_column_at(self):
        r = pyexcel.SeriesReader(self.testfile)
        result = r.named_column_at("X")
        actual = {"X":[1, 1, 1, 1, 1]}
        assert result == actual

    def test_column_filter(self):
        r = pyexcel.SeriesReader(self.testfile)
        filter = pyexcel.filters.ColumnFilter([1])
        r.add_filter(filter)
        actual = pyexcel.utils.to_dict(r)
        result = {
            "X": [1, 1, 1, 1, 1],
            "Z": [3, 3, 3, 3, 3]
        }
        assert "Y" not in actual
        assert result == actual
        # test removing the filter, it prints the original one
        r.remove_filter(filter)
        actual = pyexcel.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_get_item_operator(self):
        """
        Series Reader will skip first row because it has column header
        """
        r = pyexcel.SeriesReader(self.testfile)
        value = r[0][1]
        assert value == 2

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
