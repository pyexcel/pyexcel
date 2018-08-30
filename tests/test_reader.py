import pyexcel as p
from base import PyexcelBase, clean_up_files
from base import create_sample_file1
from base import create_generic_file
from nose.tools import raises, eq_


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

    @raises(IndexError)
    def test_cell_value(self):
        r = p.Reader(self.testfile)
        value = r.cell_value(0, 1)
        assert value == "b"
        value = r.cell_value(100, 100)

    def test_row_range(self):
        r = p.Reader(self.testfile)
        row_range = r.row_range()
        assert len(row_range) == 3

    def test_column_range(self):
        r = p.Reader(self.testfile)
        column_range = r.column_range()
        assert len(column_range) == 4

    @raises(ValueError)
    def test_named_column_at(self):
        r = p.SeriesReader(self.testfile)
        data = r.named_column_at("a")
        assert ["e", "i"] == data
        r.named_column_at("A")

    def test_get_item_operator(self):
        r = p.Reader(self.testfile)
        value = r[0, 1]
        assert value == "b"

    @raises(IndexError)
    def test_row_at(self):
        r = p.Reader(self.testfile)
        value = r.row_at(2)
        assert value == ["i", "j", 1.1, 1]
        value = r.row_at(100)  # bang

    @raises(IndexError)
    def test_column_at(self):
        r = p.Reader(self.testfile)
        value = r.column_at(1)
        assert value == ["b", "f", "j"]
        value = r.column_at(100)  # bang

    @raises(p.exceptions.FileTypeNotSupported)
    def test_not_supported_file(self):
        p.Reader("test.sylk")

    @raises(IndexError)
    def test_out_of_index(self):
        r = p.Reader(self.testfile)
        r.row[10000]

    def test_contains(self):
        r = p.Reader(self.testfile)

        def f(row):
            return row[0] == "a" and row[1] == "b"

        assert r.contains(f) is True

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
        r = p.Reader(self.testfile)
        result = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 1.1, 1]
        actual = list(r.enumerate())
        eq_(result, actual)

    def tearDown(self):
        clean_up_files([self.testfile])


class TestCSVReaderDialect:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,k,l
        """
        self.testfile = "testcsv.csv"
        table = []
        for i in [0, 4, 8]:
            array = [i + 1, i + 2, i + 3, i + 4]
            table.append(array)
        p.save_as(
            dest_file_name=self.testfile, dest_delimiter=":", array=table
        )

    def test_delimiter(self):
        with open(self.testfile) as test_file:
            content = "1:2:3:45:6:7:89:10:11:12"
            expected = ""
            for line in test_file:
                line = line.rstrip()
                expected += line
            eq_(expected, content)

    def test_read_delimiter(self):
        r = p.Reader(self.testfile, delimiter=":")
        content = list(r)
        assert content == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

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

    @raises(ValueError)
    def test_wrong_sheet(self):
        p.load(self.testfile, "Noexistent Sheet")

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
            [5, 51, 52],
        ]
        create_generic_file(self.testfile, self.content)

    def test_empty_series_reader(self):
        # debug this further
        s = p.Sheet()  # seriesreader is gone since v0.0.7
        assert s.name == "pyexcel sheet"
        test_data = [
            [1, 2, 3],
            [4, 5, 6],
            ["Column 1", "Column 2", "Column 3"],
        ]
        s.column += p.internal.sheets.transpose(test_data)
        actual = s.array
        assert test_data == actual
        s.name_columns_by_row(2)
        assert s.colnames == test_data[2]

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
            [1, 2, 3],
        ]
        create_generic_file(self.testfile, self.content)

    def test_content_is_read(self):
        r = p.SeriesReader(self.testfile)
        actual = list(r.rows())
        assert self.content[1:] == actual

    def test_headers(self):
        r = p.SeriesReader(self.testfile)
        actual = r.colnames
        assert self.content[0] == actual

    def test_named_column_at(self):
        r = p.SeriesReader(self.testfile)
        result = r.named_column_at("X")
        actual = {"X": [1, 1, 1, 1, 1]}
        eq_(result, actual["X"])

    def test_get_item_operator(self):
        """
        Series Reader will skip first row because it has column header
        """
        r = p.SeriesReader(self.testfile)
        value = r[0, 1]
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
            [1, 2, 3],
        ]
        create_generic_file(self.testfile, self.content)

    def test_content_is_read(self):
        r = p.SeriesReader(self.testfile, series=4)
        actual = list(r.rows())
        self.content.pop(4)
        eq_(self.content, actual)

    def test_headers(self):
        r = p.SeriesReader(self.testfile, series=4)
        actual = r.colnames
        eq_(self.content[4], actual)

    def test_named_column_at(self):
        r = p.SeriesReader(self.testfile, series=4)
        result = r.named_column_at("X")
        actual = {"X": [1, 1, 1, 1, 1]}
        eq_(result, actual["X"])

    def test_get_item_operator(self):
        r = p.SeriesReader(self.testfile, series=4)
        value = r[0, 1]
        assert value == 2

    def tearDown(self):
        clean_up_files([self.testfile])


def test_cell_value_boundary():
    data = [[0, 1], [10, 11]]
    sheet = p.Sheet(data)
    value = sheet.cell_value(1, 1)
    eq_(value, 11)


@raises(IndexError)
def test_cell_value_outside_boundary():
    data = [[0, 1], [10, 11]]
    sheet = p.Sheet(data)
    sheet.cell_value(1, 2)
