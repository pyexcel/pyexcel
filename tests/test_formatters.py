import datetime
from unittest import TestCase
import pyexcel as pe
from base import clean_up_files
from nose.tools import raises


class TestToFormatFunction:
    def test_none_2_str(self):
        value = None
        n_value = pe.formatters.to_format(str, value)
        assert n_value == ""

    def test_string_2_float(self):
        value = "11.11"
        n_value = pe.formatters.to_format(
            float, value)
        assert n_value == 11.11
        value = "abc"
        n_value = pe.formatters.to_format(
            float, value)
        assert n_value == value

    def test_string_to_string(self):
        value = "string"
        n_value = pe.formatters.to_format(
            str, value)
        assert n_value == value

    def test_string_2_int_format(self):
        value = "11"
        n_value = pe.formatters.to_format(
            int, value)
        assert n_value == 11
        value = "11.11111"
        n_value = pe.formatters.to_format(
            int,
            value)
        assert n_value == 11
        value = "abc"
        n_value = pe.formatters.to_format(
            int, value)
        assert n_value == value

    def test_float_2_string_format(self):
        value = 1.0
        n_value = pe.formatters.to_format(
            str, value)
        assert n_value == "1.0"

    def test_float_2_int_format(self):
        value = 1.1111
        n_value = pe.formatters.to_format(
            int, value)
        assert type(n_value) == int
        assert n_value == 1

    def test_float_2_date_format(self):
        value = 1.1111
        n_value = pe.formatters.to_format(
            datetime.datetime, value)
        assert type(n_value) == float
        assert n_value == value

    def test_int_2_string_format(self):
        value = 11
        n_value = pe.formatters.to_format(
            str, value)
        assert n_value == "11"

    def test_int_2_float_format(self):
        value = 11
        n_value = pe.formatters.to_format(
            float,
            value)
        assert type(n_value) == float
        assert n_value == value

    def test_int_2_date(self):
        value = 11
        n_value = pe.formatters.to_format(
            datetime.datetime,
            value)
        assert type(n_value) == int
        assert n_value == value

    def test_date_conversion(self):
        d = datetime.datetime.now()
        new_d = pe.formatters.to_format(
            datetime.datetime,
            d
        )
        assert d == new_d
        new_d = pe.formatters.to_format(
            str,
            d
        )
        assert d.strftime("%d/%m/%y") == new_d
        new_d = pe.formatters.to_format(
            bool,
            d
        )
        assert d == new_d
        t = datetime.time(11,11,11)
        new_t = pe.formatters.to_format(
            datetime.datetime,
            t
        )
        assert t == new_t
        new_t = pe.formatters.to_format(
            str,
            t
        )
        assert t.strftime("%H:%M:%S") == new_t
        new_t = pe.formatters.to_format(
            bool,
            t
        )
        assert t == new_t
        bad = "bad"
        new_d = pe.formatters.to_format(
            str,
            bad
        )
        assert bad == new_d

    def test_boolean_2_date(self):
        value = True
        n_value = pe.formatters.to_format(
            datetime.datetime,
            value)
        assert type(n_value) == bool
        assert n_value == value

    def test_boolean_2_float(self):
        value = True
        n_value = pe.formatters.to_format(
            float,
            value)
        assert n_value == 1

    def test_boolean_2_string(self):
        value = True
        n_value = pe.formatters.to_format(
            str,
            value)
        assert n_value == "true"
        value = False
        n_value = pe.formatters.to_format(
            str,
            value)
        assert n_value == "false"

    def test_empty_to_supported_types(self):
        value = ""
        n_value = pe.formatters.to_format(
            float,
            value)
        assert type(n_value) == float
        assert n_value == 0
        value = ""
        n_value = pe.formatters.to_format(
            int,
            value)
        assert type(n_value) == int
        assert n_value == 0
        value = ""
        n_value = pe.formatters.to_format(
            datetime.datetime,
            value)
        assert n_value == ""

    def test_date_format(self):
        d = "11-Jan-14"
        n_d = pe.formatters.to_format(
            datetime.datetime,
            d)
        assert d == n_d


class TestColumnFormatter(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "6": ["2", "3", "4", "5", "6", "7", "8", "9"]
        }
        self.io = pe.save_as(dest_file_type="xls", adict=self.data)
        self.test_tuple = ("xls", self.io.getvalue())

    def test_general_usage(self):
        r = pe.Reader(self.test_tuple)
        r.add_formatter(pe.formatters.ColumnFormatter(
            0,
            str))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])

    def test_column_format_general_usage(self):
        """Test column format function"""
        r = pe.Reader(self.test_tuple)
        r.column.format(
            0,
            str)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data["2"])
            
    def test_column_format_general_usage2(self):
        """Test column format function on demand"""
        r = pe.Reader(self.test_tuple)
        r.column.format(
            0,
            str,
            on_demand=True)
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['2'])

    def test_column_format_specs(self):
        r = pe.Reader(self.test_tuple)
        r.column.format(format_specs=[[0, str], [[2,3,4], float]])
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['2'])
        c1 = r.column_at(3)[1:]
        self.assertEqual(c1, self.data['3'])

    def test_column_format_specs_on_demand(self):
        r = pe.Reader(self.test_tuple)
        r.column.format(format_specs=[[0, lambda v: int(v)+1], [[2,3,4], float]])
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['5'])
        c1 = r.column_at(3)[1:]
        self.assertEqual(c1, self.data['3'])

    def test_one_formatter_for_two_columns(self):
        r = pe.Reader(self.test_tuple)
        r.add_formatter(pe.formatters.ColumnFormatter(
            [0,5],
            str))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['2'])
        c1 = r.column_at(5)[1:]
        self.assertEqual(c1, self.data['6'])

    @raises(NotImplementedError)
    def test_invalid_input(self):
        pe.formatters.ColumnFormatter("world", str)

    @raises(IndexError)
    def test_invalid_input2(self):
        """Empty list"""
        pe.formatters.ColumnFormatter([], str)

    @raises(IndexError)
    def test_float_in_list(self):
        pe.formatters.ColumnFormatter([1, 1.1], str)

    def test_two_formatters(self):
        r = pe.Reader(self.test_tuple)
        r.add_formatter(pe.formatters.ColumnFormatter(
            0,
            str))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['2'])
        r.add_formatter(pe.formatters.ColumnFormatter(
            0,
            int))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['1'])

    def test_custom_func(self):
        r = pe.Reader(self.test_tuple)
        f = lambda x: int(x) + 1
        r.add_formatter(pe.formatters.ColumnFormatter(
            0,
            f))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['5'])

    def test_custom_func_with_a_general_converter(self):
        r = pe.Reader(self.test_tuple)
        f = lambda x: int(x) + 1
        r.add_formatter(pe.formatters.ColumnFormatter(
            0,
            f))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['5'])
        r.add_formatter(pe.formatters.ColumnFormatter(
            0,
            str))
        c1 = r.column_at(0)[1:]
        self.assertEqual(c1, self.data['6'])

    @raises(NotImplementedError)
    def test_named_formatter(self):
        """Test wrong data type to update_index"""
        nrf = pe.formatters.NamedColumnFormatter("abc", str)
        nrf.update_index("abc")
        

class TestRowFormatter(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "6": ["2", "3", "4", "5", "6", "7", "8", "9"]
        }
        self.testfile = "test.xls"
        pe.save_as(dest_file_name=self.testfile, adict=self.data)

    def test_general_usage(self):
        """format a row 
        """
        r = pe.Reader(self.testfile)
        r.add_formatter(pe.formatters.RowFormatter(
            1,
            str))
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_general_usage2(self):
        """format a row 
        """
        r = pe.Reader(self.testfile)
        r.row.format(
            1,
            str)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_general_usage3(self):
        """format a row 
        """
        r = pe.Reader(self.testfile)
        r.row.format(
            1,
            str, on_demand=True)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)

    def test_one_formatter_for_two_rows(self):
        """format more than one row
        """
        r = pe.Reader(self.testfile)
        r.add_formatter(pe.formatters.RowFormatter(
            [1,2],
            str))
        c1 = r.row_at(2)
        c2 = ["2", "2", "2.2", "2.2", "3", "3"]
        self.assertEqual(c1, c2)
        c1 = r.row_at(1)
        c2 = ['1', "1", '1.1', "1.1", '2', "2"]
        self.assertEqual(c1, c2)

    @raises(NotImplementedError)
    def test_unacceptable_index(self):
        pe.formatters.RowFormatter(
            "hello", str)

    @raises(IndexError)
    def test_empty_list_as_input(self):
        pe.formatters.RowFormatter(
            [], str
        )

    @raises(IndexError)
    def test_float_in_row_formatter(self):
        pe.formatters.RowFormatter([1, 1.1], str)

    def test_remove_formatter(self):
        r = pe.Reader(self.testfile)
        ft = pe.formatters.RowFormatter(
            1,
            str)
        r.add_formatter(ft)
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        self.assertEqual(c1, c2)
        r.remove_formatter(ft)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)

    def test_two_formatters(self):
        r = pe.Reader(self.testfile)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)
        r.add_formatter(pe.formatters.RowFormatter(
            1,
            int))
        r.add_formatter(pe.formatters.RowFormatter(
            1,
            str))
        c1 = r.row_at(1)
        c2 = ['1', '1', '1', '1', '2', '2']
        self.assertEqual(c1, c2)

    def test_two_formatters_with_row_fomat(self):
        r = pe.Reader(self.testfile)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)
        r.row.format(format_specs=[[1, int],[1,str]])
        c1 = r.row_at(1)
        c2 = ['1', '1', '1', '1', '2', '2']
        self.assertEqual(c1, c2)

    def test_two_formatters_with_row_fomat_custom_func(self):
        r = pe.Reader(self.testfile)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)
        r.row.format(format_specs=[[1, lambda v: float(v)+1],[1,str]])
        c1 = r.row_at(1)
        c2 = ['2.0', '2.0', '2.1', '2.1', '3.0', '3.0']
        self.assertEqual(c1, c2)

    def test_custom_func(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.RowFormatter(
            1,
            f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        self.assertEqual(c1, c2)

    def test_custom_func_with_a_general_converter(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.RowFormatter(
            1,
            f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        self.assertEqual(c1, c2)
        r.add_formatter(pe.formatters.RowFormatter(
            1,
            str))
        c1 = r.row_at(1)
        c2 = ["2.0", "2.0", "2.1", "2.1", "3.0", "3.0"]
        self.assertEqual(c1, c2)

    def test_remove_formatter2(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        ft = pe.formatters.RowFormatter(1, f)
        r.add_formatter(ft)
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        self.assertEqual(c1, c2)
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        self.assertEqual(c1, c2)
        r.remove_formatter(ft)
        c1 = r.row_at(1)
        c2 = [1, "1", 1.1, "1.1", 2, "2"]
        self.assertEqual(c1, c2)

    @raises(NotImplementedError)
    def test_named_formatter(self):
        """Test wrong data type to update_index"""
        nrf = pe.formatters.NamedRowFormatter("abc", str)
        nrf.update_index("abc")
        
    def tearDown(self):
        clean_up_files([self.testfile])


class TestSheetFormatter(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "7": [1, '',]
        }
        self.testfile = "test.xls"
        pe.save_as(dest_file_name=self.testfile, adict=self.data)

    def test_general_usage(self):
        r = pe.SeriesReader(self.testfile)
        r.add_formatter(pe.formatters.SheetFormatter(
            str))
        data = [
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"]
        ]
        c1 = r.column_at(0)
        self.assertEqual(c1, data[0])
        c1 = r.column_at(1)
        self.assertEqual(c1, data[1])

    def test_two_formatters(self):
        r = pe.Reader(self.testfile)
        r.add_formatter(pe.formatters.SheetFormatter(str))
        r.add_formatter(pe.formatters.SheetFormatter(int))
        c1 = r.row_at(0)
        c2 = [1, 3, 5, 7]
        self.assertEqual(c1, c2)

    def test_custom_func(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(float))
        r.add_formatter(pe.formatters.SheetFormatter(f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0, 2.0]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4, 1.0]
        self.assertEqual(c1, c2)

    def test_custom_func2(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.format(float)
        r.map(f)
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0, 2.0]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4, 1.0]
        self.assertEqual(c1, c2)

    def test_custom_func_with_a_general_converter(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(float))
        r.add_formatter(pe.formatters.SheetFormatter(f))
        r.add_formatter(pe.formatters.SheetFormatter(str))
        c1 = r.row_at(1)
        c2 = ["2.0", "2.1", "3.0", "2.0"]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = ["3.0", "3.2", "4.0", "1.0"]
        self.assertEqual(c1, c2)

    @raises(TypeError)
    def test_custom_func_with_a_general_converter2(self):
        """Before float type operation, please convert
        the sheet to float first, otherwise, TypeError
        """
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(f))
        r.row_at(2) # bang

    def test_clear_formatters(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(f))
        r.add_formatter(pe.formatters.SheetFormatter(str))
        r.clear_formatters()
        r.name_columns_by_row(0)
        mydata = r.to_dict()
        self.assertEqual(mydata['1'], self.data['1'])
        self.assertEqual(mydata['3'], self.data['3'])
        self.assertEqual(mydata['5'], self.data['5'])

    def tearDown(self):
        clean_up_files([self.testfile])


class TestSheetFormatterInXLS(TestCase):
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
        }
        self.testfile = "test.xls"
        pe.save_as(dest_file_name=self.testfile, adict=self.data)

    def test_general_usage(self):
        r = pe.SeriesReader(self.testfile)
        r.add_formatter(pe.formatters.SheetFormatter(str))
        self.data = [
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"],
            ["2", "3", "4", "5", "6", "7", "8", "9"]
        ]
        c1 = r.column_at(0)
        self.assertEqual(c1, self.data[0])
        c1 = r.column_at(1)
        self.assertEqual(c1, self.data[1])

    def test_two_formatters(self):
        r = pe.Reader(self.testfile)
        r.add_formatter(pe.formatters.SheetFormatter(str))
        r.add_formatter(pe.formatters.SheetFormatter(int))
        c1 = r.row_at(0)
        c2 = [1, 3, 5]
        self.assertEqual(c1, c2)

    def test_custom_func(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4]
        self.assertEqual(c1, c2)

    def test_custom_func_with_a_general_converter(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(f))
        r.add_formatter(pe.formatters.SheetFormatter(str))
        c1 = r.row_at(1)
        c2 = ["2.0", "2.1", "3.0"]
        self.assertEqual(c1, c2)
        c1 = r.row_at(2)
        c2 = ["3.0", "3.2", "4.0"]
        self.assertEqual(c1, c2)

    def test_clear_formatters(self):
        r = pe.Reader(self.testfile)
        f = lambda x: float(x) + 1
        r.add_formatter(pe.formatters.SheetFormatter(f))
        r.add_formatter(pe.formatters.SheetFormatter(str))
        r.clear_formatters()
        r.name_columns_by_row(0)
        mydata = r.to_dict()
        self.assertEqual(mydata['1'], self.data['1'])
        self.assertEqual(mydata['3'], self.data['3'])
        self.assertEqual(mydata['5'], self.data['5'])

    def tearDown(self):
        clean_up_files([self.testfile])
