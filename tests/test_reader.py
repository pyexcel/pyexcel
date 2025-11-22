import pytest
import pyexcel as p

from .base import (
    PyexcelBase,
    clean_up_files,
    create_generic_file,
    create_sample_file1,
)
from .nose_tools import eq_, raises


@pytest.mark.parametrize((), [])
class TestReader:
    @pytest.fixture
    def test_file(self) -> str:
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        testfile = "testcsv.csv"
        create_sample_file1(testfile)
        return testfile

    @raises(IndexError)
    def test_cell_value(self, test_file):
        r = p.Reader(test_file)
        value = r.cell_value(0, 1)
        assert value == "b"
        value = r.cell_value(100, 100)

    def test_row_range(self, test_file):
        r = p.Reader(test_file)
        row_range = r.row_range()
        assert len(row_range) == 3

    def test_column_range(self, test_file):
        r = p.Reader(test_file)
        column_range = r.column_range()
        assert len(column_range) == 4

    @raises(ValueError)
    def test_named_column_at(self, test_file):
        r = p.SeriesReader(test_file)
        data = r.named_column_at("a")
        assert ["e", "i"] == data
        r.named_column_at("A")

    def test_get_item_operator(self, test_file):
        r = p.Reader(test_file)
        value = r[0, 1]
        assert value == "b"

    @raises(IndexError)
    def test_row_at(self, test_file):
        r = p.Reader(test_file)
        value = r.row_at(2)
        assert value == ["i", "j", 1.1, 1]
        value = r.row_at(100)  # bang

    @raises(IndexError)
    def test_column_at(self, test_file):
        r = p.Reader(test_file)
        value = r.column_at(1)
        assert value == ["b", "f", "j"]
        value = r.column_at(100)  # bang

    @raises(p.exceptions.FileTypeNotSupported)
    def test_not_supported_file(self, test_file):
        p.Reader("test.sylk")

    @raises(IndexError)
    def test_out_of_index(self, test_file):
        r = p.Reader(test_file)
        r.row[10000]

    def test_contains(self, test_file):
        r = p.Reader(test_file)

        def f(row):
            return row[0] == "a" and row[1] == "b"

        assert r.contains(f) is True

    def tearDown(self, test_file):
        clean_up_files([test_file])


class TestCSVReader(PyexcelBase):
    """
    Test CSV reader
    """

    @pytest.fixture
    def test_file(self):
        test_file = "testcsv.csv"
        self._write_test_file(test_file)
        return test_file


def test_csv_reader_2():
    test_file = "testcsv.csv"
    create_sample_file1(test_file)

    r = p.Reader(test_file)
    result = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 1.1, 1]
    actual = list(r.enumerate())
    eq_(result, actual)
    clean_up_files([test_file])


def test_csv_reader_dialect():
    test_file = "testcsv.csv"
    table = []
    for i in [0, 4, 8]:
        array = [i + 1, i + 2, i + 3, i + 4]
        table.append(array)
    p.save_as(
        dest_file_name=test_file,
        dest_delimiter=":",
        array=table,
    )

    with open(test_file, encoding="utf-8") as test_file:
        content = "1:2:3:45:6:7:89:10:11:12"
        expected = ""
        for line in test_file:
            line = line.rstrip()
            expected += line
    eq_(expected, content)

    r = p.Reader(test_file, delimiter=":")
    content = list(r)
    assert content == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

    clean_up_files([test_file])


class TestXLSReader(PyexcelBase):
    def setUp(self, test_file):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        test_file = "test.xls"
        self._write_test_file(test_file)

    @raises(ValueError)
    def test_wrong_sheet(self, test_file):
        p.load(test_file, "Noexistent Sheet")

    def tearDown(self, test_file):
        clean_up_files([test_file])


@pytest.mark.parametrize((), [])
class TestXLSXReader(PyexcelBase):
    @pytest.fixture
    def test_file(self):
        test_file = "test.xlsx"
        self._write_test_file(test_file)
        return test_file


@pytest.mark.parametrize((), [])
class TestXLSMReader(PyexcelBase):
    @pytest.fixture
    def test_file(self):
        test_file = "test.xlsm"
        self._write_test_file(test_file)
        return test_file


class TestSeriesReader3:
    def setUp(self, test_file):
        test_file = "test.xlsx"
        self.content = [
            ["X", "Y", "Z"],
            [1, 11, 12],
            [2, 21, 22],
            [3, 31, 32],
            [4, 41, 42],
            [5, 51, 52],
        ]
        create_generic_file(test_file, self.content)

    def test_empty_series_reader(self, test_file):
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

    def tearDown(self, test_file):
        clean_up_files([test_file])


class TestSeriesReader4:
    def setUp(self, test_file):
        test_file = "test.xls"
        self.content = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        ]
        create_generic_file(test_file, self.content)

    def test_content_is_read(self, test_file):
        r = p.SeriesReader(test_file)
        actual = list(r.rows())
        assert self.content[1:] == actual

    def test_headers(self, test_file):
        r = p.SeriesReader(test_file)
        actual = r.colnames
        assert self.content[0] == actual

    def test_named_column_at(self, test_file):
        r = p.SeriesReader(test_file)
        result = r.named_column_at("X")
        actual = {"X": [1, 1, 1, 1, 1]}
        eq_(result, actual["X"])

    def test_get_item_operator(self, test_file):
        """
        Series Reader will skip first row because it has column header
        """
        r = p.SeriesReader(test_file)
        value = r[0, 1]
        assert value == 2

    def tearDown(self, test_file):
        clean_up_files([test_file])


class TestSeriesReader5:
    def setUp(self, test_file):
        test_file = "test.xls"
        self.content = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            ["X", "Y", "Z"],
            [1, 2, 3],
        ]
        create_generic_file(test_file, self.content)

    def test_content_is_read(self, test_file):
        r = p.SeriesReader(test_file, series=4)
        actual = list(r.rows())
        self.content.pop(4)
        eq_(self.content, actual)

    def test_headers(self, test_file):
        r = p.SeriesReader(test_file, series=4)
        actual = r.colnames
        eq_(self.content[4], actual)

    def test_named_column_at(self, test_file):
        r = p.SeriesReader(test_file, series=4)
        result = r.named_column_at("X")
        actual = {"X": [1, 1, 1, 1, 1]}
        eq_(result, actual["X"])

    def test_get_item_operator(self, test_file):
        r = p.SeriesReader(test_file, series=4)
        value = r[0, 1]
        assert value == 2

    def tearDown(self, test_file):
        clean_up_files([test_file])


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
