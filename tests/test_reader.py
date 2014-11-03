import pyexcel as pe
from base import PyexcelBase, clean_up_files
from base import create_sample_file1
from _compact import BytesIO
from nose.tools import raises


class TestReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testfile = "testcsv.csv"
        create_sample_file1(self.testfile)

    def test_is_series(self):
        r = pe.Reader(self.testfile)
        assert r.is_series() is False
        
    def test_cell_value(self):
        r = pe.Reader(self.testfile)
        value = r.cell_value(100,100)
        assert value == None
        value = r.cell_value(0, 1)
        assert value == 'b'

    def test_row_range(self):
        r = pe.Reader(self.testfile)
        row_range = r.row_range()
        assert len(row_range) == 3

    def test_column_range(self):
        r = pe.Reader(self.testfile)
        column_range = r.column_range()
        assert len(column_range) == 4

    @raises(ValueError)
    def test_named_column_at(self):
        r = pe.SeriesReader(self.testfile)
        data = r.named_column_at('a')
        assert ['e', 'i'] == data
        r.named_column_at("A")

    def test_get_item_operator(self):
        r = pe.Reader(self.testfile)
        value = r[0,1]
        assert value == 'b'

    def test_row_at(self):
        r = pe.Reader(self.testfile)
        value = r.row_at(100)
        assert value == None
        value = r.row_at(2)
        assert value == ['i', 'j', "1.1", "1"]

    def test_column_at(self):
        r = pe.Reader(self.testfile)
        value = r.column_at(100)
        assert value == None
        value = r.column_at(1)
        assert value == ['b','f','j']

    @raises(NotImplementedError)
    def test_not_supported_file(self):
        pe.Reader("test.sylk")
        assert 0==1

    @raises(IndexError)
    def test_out_of_index(self):
        r = pe.Reader(self.testfile)
        r.row[10000]

    def test_contains(self):
        r = pe.Reader(self.testfile)
        f = lambda row: row[0]=='a' and row[1] == 'b'
        assert r.contains(f) == True

    def tearDown(self):
        clean_up_files([self.testfile])


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
        clean_up_files([self.testfile])


class TestCSVReader2:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,k,l
        """
        self.testfile = "testcsv.csv"
        create_sample_file1(self.testfile)

    def test_data_types(self):
        r = pe.Reader(self.testfile)
        result=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', '1.1', '1']
        actual = pe.utils.to_array(r.enumerate())
        assert result == actual

    def tearDown(self):
        clean_up_files([self.testfile])


class TestCSVReaderDialect:
    def create_sample_file(self, file):
        """
        1,2,3,4
        5,6,7,8
        9,10,11,12
        """    
        w = pe.Writer(file, delimiter=":")
        table = []
        for i in [0, 4, 8]:
            array = [i+1, i+2, i+3, i+4]
            table.append(array)
        w.write_array(table)
        w.close()
        
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,k,l
        """
        self.testfile = "testcsv.csv"
        self.create_sample_file(self.testfile)
    
    def test_delimiter(self):
        f = open(self.testfile)
        content = '1:2:3:45:6:7:89:10:11:12'
        expected = ''
        for l in f:
            l = l.rstrip()
            expected += l
        assert expected == content

    def test_read_delimiter(self):
        r = pe.Reader(self.testfile, delimiter=":")
        content = pe.utils.to_array(r)
        assert content == [["1", "2", "3", "4"], ["5", "6", "7", "8"], ["9", "10", "11", "12"]]
        
    def tearDown(self):
        clean_up_files([self.testfile])


class TestXLSReader(PyexcelBase):
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
        clean_up_files([self.testfile])


class TestXLSXReader(PyexcelBase):
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
        clean_up_files([self.testfile])


class TestXLSMReader(PyexcelBase):
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
        clean_up_files([self.testfile])


class TestSeriesReader3:
    def setUp(self):
        self.testfile = "test.xlsx"
        self.content = [
            ["X", "Y", "Z"],
            [1, 11, 12],
            [2, 21, 22],
            [3, 31, 32],
            [4, 41, 42],
            [5, 51, 52]
        ]
        w = pe.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_empty_series_reader(self):
        r = pe.SeriesReader()
        assert r.name == "memory"
        test_data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column 1", "Column 2", "Column 3"]
        ]
        r.column += test_data
        actual = pe.to_array(r)
        assert test_data == actual
        r.declare_index(2)
        assert r.row_series == test_data[2]
        
    def test_row_filter(self):
        r = pe.SeriesReader(self.testfile)
        r.add_filter(pe.filters.RowFilter([1]))
        actual = pe.utils.to_dict(r)
        result = {
            "X": [1, 3, 4, 5],
            "Y": [11, 31, 41, 51],
            "Z": [12, 32, 42, 52]
        }
        assert result == actual

    def test_odd_row_filter(self):
        r = pe.SeriesReader(self.testfile)
        f = pe.filters.OddRowFilter()
        r.add_filter(f)
        actual = pe.utils.to_dict(r)
        result = {
            "X": [2, 4],
            "Y": [21, 41],
            "Z": [22, 42]
        }
        assert result == actual
        r.remove_filter(f)
        actual = pe.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_even_row_filter(self):
        r = pe.SeriesReader(self.testfile)
        r.add_filter(pe.filters.EvenRowFilter())
        actual = pe.utils.to_dict(r)
        result = {
            "X": [1, 3, 5],
            "Y": [11, 31, 51],
            "Z": [12, 32, 52]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pe.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_orthogonality(self):
        r = pe.SeriesReader(self.testfile)
        r.add_filter(pe.filters.EvenRowFilter())
        r.add_filter(pe.filters.OddColumnFilter())
        actual = pe.to_dict(r)
        result = {
            "Y": [11, 31, 51]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pe.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_orthogonality2(self):
        r = pe.SeriesReader(self.testfile)
        r.add_filter(pe.filters.OddColumnFilter())
        r.add_filter(pe.filters.EvenRowFilter())
        actual = pe.utils.to_dict(r)
        result = {
            "Y": [11, 31, 51]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pe.utils.to_array(r)
        result = [{'X': [1, 2, 3, 4, 5]}, {'Y': [11, 21, 31, 41, 51]}, {'Z': [12, 22, 32, 42, 52]}]
        assert actual == result

    def test_series_column_iterator(self):
        r = pe.SeriesReader(self.testfile)
        sci = pe.iterators.ColumnIndexIterator(r)
        actual = pe.utils.to_array(sci)
        result = [{'X': [1, 2, 3, 4, 5]}, {'Y': [11, 21, 31, 41, 51]}, {'Z': [12, 22, 32, 42, 52]}]
        assert actual == result

    def tearDown(self):
        clean_up_files([self.testfile])


class TestSeriesReader4:
    def setUp(self):
        self.testfile = "test.xls"
        self.content = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]
        ]
        w = pe.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_content_is_read(self):
        r = pe.SeriesReader(self.testfile)
        actual = pe.utils.to_array(r.rows())
        assert self.content[1:] == actual

    def test_headers(self):
        r = pe.SeriesReader(self.testfile)
        actual = r.row_series
        assert self.content[0] == actual

    def test_named_column_at(self):
        r = pe.SeriesReader(self.testfile)
        result = r.named_column_at("X")
        actual = {"X":[1, 1, 1, 1, 1]}
        assert result == actual["X"]

    def test_column_filter(self):
        r = pe.SeriesReader(self.testfile)
        filter = pe.filters.ColumnFilter([1])
        r.add_filter(filter)
        actual = pe.utils.to_dict(r)
        result = {
            "X": [1, 1, 1, 1, 1],
            "Z": [3, 3, 3, 3, 3]
        }
        assert "Y" not in actual
        assert result == actual
        # test removing the filter, it prints the original one
        r.remove_filter(filter)
        actual = pe.utils.to_array(r.rows())
        assert actual == self.content[1:]

    def test_get_item_operator(self):
        """
        Series Reader will skip first row because it has column header
        """
        r = pe.SeriesReader(self.testfile)
        value = r[0,1]
        assert value == 2

    def tearDown(self):
        clean_up_files([self.testfile])


class TestSeriesReader5:
    def setUp(self):
        self.testfile = "test.xls"
        self.content = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            ["X", "Y", "Z"],
            [1, 2, 3]
        ]
        w = pe.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_content_is_read(self):
        r = pe.SeriesReader(self.testfile, series=4)
        actual = pe.utils.to_array(r.rows())
        self.content.pop(4)
        assert self.content == actual

    def test_headers(self):
        r = pe.SeriesReader(self.testfile, series=4)
        actual = r.row_series
        assert self.content[4] == actual

    def test_named_column_at(self):
        r = pe.SeriesReader(self.testfile, series=4)
        result = r.named_column_at("X")
        actual = {"X":[1, 1, 1, 1, 1]}
        assert result == actual["X"]

    def test_column_filter(self):
        r = pe.SeriesReader(self.testfile, series=4)
        filter = pe.filters.ColumnFilter([1])
        r.add_filter(filter)
        actual = pe.utils.to_dict(r)
        result = {
            "X": [1, 1, 1, 1, 1],
            "Z": [3, 3, 3, 3, 3]
        }
        assert "Y" not in actual
        assert result == actual
        # test removing the filter, it prints the original one
        r.remove_filter(filter)
        actual = pe.utils.to_array(r.rows())
        self.content.pop(4)
        assert actual == self.content

    def test_get_item_operator(self):
        """
        Series Reader will skip first row because it has column header
        """
        r = pe.SeriesReader(self.testfile, series_row=4)
        value = r[0,1]
        assert value == 2

    def tearDown(self):
        clean_up_files([self.testfile])


class TestColumnSeriesReader:
    def setUp(self):
        file_type = "xlsx"
        io = BytesIO()
        self.content = [
            ["X", "Y", "Z"],
            [1, 11, 12],
            [2, 21, 22],
            [3, 31, 32],
            [4, 41, 42],
            [5, 51, 52]
        ]
        w = pe.Writer((file_type, io))
        w.write_columns(self.content)
        w.close()
        self.test_tuple = (file_type, io.getvalue())

    def test_row_filter(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        r.add_filter(pe.filters.SingleRowFilter(1))
        actual = pe.utils.to_dict(r)
        result = {
            "X": [1, 2, 3, 4, 5],
            "Z": [12, 22, 32, 42, 52]
        }
        assert result == actual

    def test_column_filter(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        r.add_filter(pe.filters.SingleColumnFilter(0))
        actual = pe.utils.to_dict(r)
        result = {
            "X": [2, 3, 4, 5],
            "Y": [21, 31, 41, 51],
            "Z": [22, 32, 42, 52]
        }
        assert result == actual
        assert r.column_series == ["X", "Y", "Z"]

    def test_odd_row_filter(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        f = pe.filters.OddRowFilter()
        r.add_filter(f)
        actual = pe.utils.to_dict(r)
        result = {
            "Y": [11, 21, 31, 41, 51]
        }
        assert result == actual
        r.remove_filter(f)
        actual = pe.utils.to_array(r.rows())
        assert actual == pe.iterators.transpose(self.content[1:])

    def test_even_row_filter(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        r.add_filter(pe.filters.EvenRowFilter())
        actual = pe.utils.to_dict(r)
        result = {
            "X": [1, 2, 3, 4, 5],
            "Z": [12, 22, 32, 42, 52]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pe.utils.to_array(r.rows())
        assert actual == pe.iterators.transpose(self.content[1:])

    def test_orthogonality(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        r.add_filter(pe.filters.EvenRowFilter())
        r.add_filter(pe.filters.OddColumnFilter())
        actual = pe.to_dict(r)
        result = {
            "X": [2, 4],
            "Z": [22, 42]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pe.utils.to_array(r.rows())
        assert actual == pe.iterators.transpose(self.content[1:])

    def test_orthogonality2(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        r.add_filter(pe.filters.OddColumnFilter())
        r.add_filter(pe.filters.EvenRowFilter())
        actual = pe.utils.to_dict(r)
        result = {
            "X": [2, 4],
            "Z": [22, 42]
        }
        assert result == actual
        # test removing the filter, it prints the original one
        r.clear_filters()
        actual = pe.utils.to_array(r)
        result = [{'X': [1, 2, 3, 4, 5]}, {'Y': [11, 21, 31, 41, 51]}, {'Z': [12, 22, 32, 42, 52]}]
        assert actual == result

    def test_series_column_iterator(self):
        r = pe.ColumnSeriesReader(self.test_tuple)
        sri = pe.iterators.RowIndexIterator(r)
        actual = pe.utils.to_array(sri)
        result = [{'X': [1, 2, 3, 4, 5]}, {'Y': [11, 21, 31, 41, 51]}, {'Z': [12, 22, 32, 42, 52]}]
        assert actual == result
