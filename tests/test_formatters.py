import datetime
from unittest import TestCase

from base import clean_up_files
from pyexcel import SeriesReader, save_as, get_sheet
from pyexcel.internal.sheets import formatters


def increase_func(x):
    return int(x) + 1


def increase_float_func(x):
    return float(x) + 1


class TestToFormatFunction:
    def test_none_2_str(self):
        value = None
        n_value = formatters.to_format(str, value)
        assert n_value == ""

    def test_string_2_float(self):
        value = "11.11"
        n_value = formatters.to_format(float, value)
        assert n_value == 11.11
        value = "abc"
        n_value = formatters.to_format(float, value)
        assert n_value == value

    def test_string_to_string(self):
        value = "string"
        n_value = formatters.to_format(str, value)
        assert n_value == value

    def test_string_2_int_format(self):
        value = "11"
        n_value = formatters.to_format(int, value)
        assert n_value == 11
        value = "11.11111"
        n_value = formatters.to_format(int, value)
        assert n_value == 11
        value = "abc"
        n_value = formatters.to_format(int, value)
        assert n_value == value

    def test_float_2_string_format(self):
        value = 1.0
        n_value = formatters.to_format(str, value)
        assert n_value == "1.0"

    def test_float_2_int_format(self):
        value = 1.1111
        n_value = formatters.to_format(int, value)
        assert type(n_value) == int
        assert n_value == 1

    def test_float_2_date_format(self):
        value = 1.1111
        n_value = formatters.to_format(datetime.datetime, value)
        assert type(n_value) == float
        assert n_value == value

    def test_int_2_string_format(self):
        value = 11
        n_value = formatters.to_format(str, value)
        assert n_value == "11"

    def test_int_2_float_format(self):
        value = 11
        n_value = formatters.to_format(float, value)
        assert type(n_value) == float
        assert n_value == value

    def test_int_2_date(self):
        value = 11
        n_value = formatters.to_format(datetime.datetime, value)
        assert type(n_value) == int
        assert n_value == value

    def test_date_conversion(self):
        d = datetime.datetime.now()
        new_d = formatters.to_format(datetime.datetime, d)
        assert d == new_d
        new_d = formatters.to_format(str, d)
        assert d.strftime("%d/%m/%y") == new_d
        new_d = formatters.to_format(bool, d)
        assert d == new_d
        t = datetime.time(11, 11, 11)
        new_t = formatters.to_format(datetime.datetime, t)
        assert t == new_t
        new_t = formatters.to_format(str, t)
        assert t.strftime("%H:%M:%S") == new_t
        new_t = formatters.to_format(bool, t)
        assert t == new_t
        bad = "bad"
        new_d = formatters.to_format(str, bad)
        assert bad == new_d

    def test_boolean_2_date(self):
        value = True
        n_value = formatters.to_format(datetime.datetime, value)
        assert type(n_value) == bool
        assert n_value == value

    def test_boolean_2_float(self):
        value = True
        n_value = formatters.to_format(float, value)
        assert n_value == 1

    def test_boolean_2_string(self):
        value = True
        n_value = formatters.to_format(str, value)
        assert n_value == "true"
        value = False
        n_value = formatters.to_format(str, value)
        assert n_value == "false"

    def test_empty_to_supported_types(self):
        value = ""
        n_value = formatters.to_format(float, value)
        assert type(n_value) == float
        assert n_value == 0
        value = ""
        n_value = formatters.to_format(int, value)
        assert type(n_value) == int
        assert n_value == 0
        value = ""
        n_value = formatters.to_format(datetime.datetime, value)
        assert n_value == ""

    def test_date_format(self):
        d = "11-Jan-14"
        n_d = formatters.to_format(datetime.datetime, d)
        assert d == n_d


class TestColumnFormatter(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "6": ["2", "3", "4", "5", "6", "7", "8", "9"],
        }
        self.io = save_as(dest_file_type="xls", adict=self.data)

    def test_general_usage(self):
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(0, str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])

    def test_column_format_general_usage(self):
        """Test column format function"""
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(0, str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])

    def test_column_format_general_usage2(self):
        """Test column format function on demand"""
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(0, str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])

    def test_column_format_specs(self):
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(format_specs=[[0, str], [[2, 3, 4], float]])
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])
        c1 = r.column_at(3)[1:]
        self.assertEqual(c1, self.data["3"])

    def test_one_formatter_for_two_columns(self):
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format([0, 5], str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])
        c1 = r.column_at(5)[1:]
        self.assertEqual(c1, self.data["6"])

    def test_two_formatters(self):
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(0, str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])
        r.column.format(0, int)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["1"])

    def test_custom_func(self):
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(0, increase_func)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["5"])

    def test_custom_func_with_a_general_converter(self):
        r = get_sheet(file_stream=self.io, file_type="xls")
        r.column.format(0, increase_func)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["5"])
        r.column.format(0, str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["6"])


class TestRowFormatter(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "6": ["2", "3", "4", "5", "6", "7", "8", "9"],
        }
        self.testfile = "test.xls"
        save_as(dest_file_name=self.testfile, adict=self.data)

    def test_general_usage(self):
        """format a row"""
        r = get_sheet(file_name=self.testfile)
        r.row.format(1, str)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_general_usage2(self):
        """format a row"""
        r = get_sheet(file_name=self.testfile)
        r.row.format(1, str)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_one_formatter_for_two_rows(self):
        """format more than one row"""
        r = get_sheet(file_name=self.testfile)
        r.row.format([1, 2], str)
        c1 = r.row_at(2)
        c2 = ["2", "2", "2.2", "2.2", "3", "3"]
        self.assertEqual(c1, c2)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_two_formatters(self):
        r = get_sheet(file_name=self.testfile)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)
        r.row.format(1, int)
        r.row.format(1, str)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1", "1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_two_formatters_with_row_fomat(self):
        r = get_sheet(file_name=self.testfile)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)
        r.row.format(format_specs=[[1, int], [1, str]])
        c1 = r.row_at(1)
        c2 = ["1", "1", "1", "1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_two_formatters_with_row_fomat_custom_func(self):
        r = get_sheet(file_name=self.testfile)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)
        r.row.format(format_specs=[[1, increase_float_func], [1, str]])
        c1 = r.row_at(1)
        c2 = ["2.0", "2.0", "2.1", "2.1", "3.0", "3.0"]
        self.assertEqual(c1, c2)

    def test_custom_func(self):
        r = get_sheet(file_name=self.testfile)
        r.row.format(1, increase_float_func)
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        self.assertEqual(c1, c2)

    def test_custom_func_with_a_general_converter(self):
        r = get_sheet(file_name=self.testfile)
        r.row.format(1, increase_float_func)
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        self.assertEqual(c1, c2)
        r.row.format(1, str)
        c1 = r.row_at(1)
        c2 = ["2.0", "2.0", "2.1", "2.1", "3.0", "3.0"]
        self.assertEqual(c1, c2)

    def tearDown(self):
        clean_up_files([self.testfile])


class TestSheetFormatter(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "7": [1, ""],
        }
        self.testfile = "test.xls"
        save_as(dest_file_name=self.testfile, adict=self.data)

    def test_general_usage(self):
        r = SeriesReader(file_name=self.testfile)
        r.format(str)
        data = [
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"],
        ]
        c1 = r.column_at(0)
        self.assertEqual(c1, data[0])
        c1 = r.column_at(1)
        self.assertEqual(c1, data[1])

    def test_two_formatters(self):
        r = get_sheet(file_name=self.testfile)
        r.format(str)
        r.format(int)
        c1 = r.row_at(0)
        c2 = [1, 3, 5, 7]
        self.assertEqual(c1, c2)

    def test_custom_func(self):
        r = get_sheet(file_name=self.testfile)
        r.format(float)
        r.map(increase_float_func)
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0, 2.0]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4, 1.0]
        self.assertEqual(c1, c2)

    def test_custom_func2(self):
        r = get_sheet(file_name=self.testfile)
        r.format(float)
        r.map(increase_float_func)
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0, 2.0]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4, 1.0]
        self.assertEqual(c1, c2)

    def test_custom_func_with_a_general_converter(self):
        r = get_sheet(file_name=self.testfile)
        r.format(float)
        r.map(increase_float_func)
        r.format(str)
        c1 = r.row_at(1)
        c2 = ["2.0", "2.1", "3.0", "2.0"]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = ["3.0", "3.2", "4.0", "1.0"]
        self.assertEqual(c1, c2)

    def tearDown(self):
        clean_up_files([self.testfile])
