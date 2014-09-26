import pyexcel
import os
import datetime


class TestToFormatFunction:
    def test_string_2_float(self):
        value = "11.11"
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.FLOAT_FORMAT, value)
        assert n_value == 11.11
        value = "abc"
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.FLOAT_FORMAT, value)
        assert n_value == "N/A"

    def test_string_to_string(self):
        value = "string"
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.STRING_FORMAT, value)
        assert n_value == value

    def test_string_2_int_format(self):
        value = "11"
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.INT_FORMAT, value)
        assert n_value == 11
        value = "11.11111"
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.INT_FORMAT,
            value)
        assert n_value == 11
        value = "abc"
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.INT_FORMAT, value)
        assert n_value == "N/A"

    def test_float_2_string_format(self):
        value = 1.0
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.FLOAT_FORMAT,
            pyexcel.formatters.STRING_FORMAT, value)
        assert n_value == "1.0"

    def test_float_2_int_format(self):
        value = 1.1111
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.FLOAT_FORMAT,
            pyexcel.formatters.INT_FORMAT, value)
        assert type(n_value) == int
        assert n_value == 1
        value = "1.1"
        try:
            n_value = pyexcel.formatters.to_format(
                pyexcel.formatters.FLOAT_FORMAT,
                pyexcel.formatters.INT_FORMAT, value)
            assert 1==2
        except:
            assert 1 == 1

    def test_float_2_date_format(self):
        value = 1.1111
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.FLOAT_FORMAT,
            pyexcel.formatters.DATE_FORMAT, value)
        assert type(n_value) == float
        assert n_value == value

    def test_int_2_string_format(self):
        value = 11
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.INT_FORMAT,
            pyexcel.formatters.STRING_FORMAT, value)
        assert n_value == "11"

    def test_int_2_float_format(self):
        value = 11
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.INT_FORMAT,
            pyexcel.formatters.FLOAT_FORMAT,
            value)
        assert type(n_value) == float
        assert n_value == value

    def test_int_2_date(self):
        value = 11
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.INT_FORMAT,
            pyexcel.formatters.DATE_FORMAT,
            value)
        assert type(n_value) == int
        assert n_value == value

    def test_date_conversion(self):
        d = datetime.datetime.now()
        new_d = pyexcel.formatters.to_format(
            pyexcel.formatters.DATE_FORMAT,
            pyexcel.formatters.DATE_FORMAT,
            d
        )
        assert d == new_d
        new_d = pyexcel.formatters.to_format(
            pyexcel.formatters.DATE_FORMAT,
            pyexcel.formatters.STRING_FORMAT,
            d
        )
        assert d.isoformat() == new_d
        new_d = pyexcel.formatters.to_format(
            pyexcel.formatters.DATE_FORMAT,
            pyexcel.formatters.BOOLEAN_FORMAT,
            d
        )
        assert d == new_d

    def test_boolean_2_date(self):
        value = True
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.BOOLEAN_FORMAT,
            pyexcel.formatters.DATE_FORMAT,
            value)
        assert type(n_value) == bool
        assert n_value == value

    def test_boolean_2_float(self):
        value = True
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.BOOLEAN_FORMAT,
            pyexcel.formatters.FLOAT_FORMAT,
            value)
        assert n_value == 1

    def test_boolean_2_string(self):
        value = True
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.BOOLEAN_FORMAT,
            pyexcel.formatters.STRING_FORMAT,
            value)
        assert n_value == "True"
        value = False
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.BOOLEAN_FORMAT,
            pyexcel.formatters.STRING_FORMAT,
            value)
        assert n_value == "False"

    def test_empty_to_supported_types(self):
        value = ""
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.EMPTY,
            pyexcel.formatters.FLOAT_FORMAT,
            value)
        assert type(n_value) == float
        assert n_value == 0
        value = ""
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.EMPTY,
            pyexcel.formatters.INT_FORMAT,
            value)
        assert type(n_value) == int
        assert n_value == 0
        value = ""
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.EMPTY,
            pyexcel.formatters.DATE_FORMAT,
            value)
        assert n_value == ""

    def test_date_format(self):
        d = "11-Jan-14"
        n_d = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.DATE_FORMAT,
            d)
        assert d == n_d


class TestColumnFormatter:
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "6": ["2", "3", "4", "5", "6", "7", "8", "9"]
        }
        self.testfile = "test.csv"
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.data)
        w.close()

    def test_general_usage(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.column_at(0)[1:]
        c2 = self.data["2"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_two_formatters(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.column_at(0)[1:]
        c2 = self.data["2"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            pyexcel.formatters.INT_FORMAT))
        c1 = r.column_at(0)[1:]
        c2 = self.data["1"]
        for i in range(0, len(c1)):
            assert type(c1[i]) == int
            assert c1[i] == c2[i]

    def test_custom_func(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: int(x) + 1
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            pyexcel.formatters.INT_FORMAT,
            f))
        c1 = r.column_at(0)[1:]
        c2 = self.data["5"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_custom_func_with_a_general_converter(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: int(x) + 1
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            pyexcel.formatters.INT_FORMAT,
            f))
        c1 = r.column_at(0)[1:]
        c2 = self.data["5"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.column_at(0)[1:]
        c2 = self.data["6"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestRowFormatter:
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
            "6": ["2", "3", "4", "5", "6", "7", "8", "9"]
        }
        self.testfile = "test.csv"
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.data)
        w.close()

    def test_general_usage(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.row_at(1)
        print c1
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_remove_formatter(self):
        r = pyexcel.Reader(self.testfile)
        ft = pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.STRING_FORMAT)
        r.add_formatter(ft)
        c1 = r.row_at(1)
        print c1
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.remove_formatter(ft)
        c1 = r.row_at(1)
        c2 = [1, 1, 1.1, 1.1, 2, 2]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_two_formatters(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.row_at(1)
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.INT_FORMAT))
        c1 = r.row_at(1)
        c2 = [1, 1, 1, 1, 2, 2]
        for i in range(0, len(c1)):
            assert type(c1[i]) == int
            assert c1[i] == c2[i]

    def test_custom_func(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        c1 = r.row_at(1)
        print c1
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_custom_func_with_a_general_converter(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        print c1
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.row_at(1)
        print c1
        c2 = ["2.0", "2.0", "2.1", "2.1", "3.0", "3.0"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_remove_formatter2(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        ft = pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.FLOAT_FORMAT,
            f)
        r.add_formatter(ft)
        c1 = r.row_at(1)
        c2 = [2.0, 2.0, 2.1, 2.1, 3.0, 3.0]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.add_formatter(pyexcel.formatters.RowFormatter(
            1,
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.row_at(1)
        print c1
        c2 = ["2.0", "2.0", "2.1", "2.1", "3.0", "3.0"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        r.remove_formatter(ft)
        c1 = r.row_at(1)
        print c1
        c2 = ["1", "1", "1.1", "1.1", "2", "2"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]


    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestSheetFormatter:
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
        }
        self.testfile = "test.csv"
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.data)
        w.close()

    def test_general_usage(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        self.data = [
            ["1", "2", "3", "4", "5", "6", "7", "8"],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"],
            ["2", "3", "4", "5", "6", "7", "8", "9"]
        ]
        c1 = r.column_at(0)
        for i in range(0, len(c1)):
            assert c1[i] == self.data[0][i]
        c1 = r.column_at(1)
        for i in range(0, len(c1)):
            assert c1[i] == self.data[1][i]

    def test_two_formatters(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.INT_FORMAT))
        c1 = r.row_at(0)
        c2 = [1, 3, 5]
        print c1
        for i in range(0, len(c1)):
            assert type(c1[i]) == int
            assert c1[i] == c2[i]

    def test_custom_func(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_custom_func_with_a_general_converter(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.row_at(1)
        c2 = ["2.0", "2.1", "3.0"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        c1 = r.row_at(2)
        c2 = ["3.0", "3.2", "4.0"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_clear_formatters(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        r.clear_formatters()
        mydata = pyexcel.utils.to_dict(r.become_series())
        assert mydata[1] == self.data['1']
        assert mydata[3] == self.data['3']
        assert mydata[5] == self.data['5']

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestSheetFormatterInXLS:
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
        }
        self.testfile = "test.xls"
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.data)
        w.close()

    def test_general_usage(self):
        r = pyexcel.SeriesReader(self.testfile)
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        self.data = [
            ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0"],
            ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7.7", "8.8"],
            ["2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]
        ]
        c1 = r.column_at(0)
        for i in range(0, len(c1)):
            assert c1[i] == self.data[0][i]
        c1 = r.column_at(1)
        for i in range(0, len(c1)):
            assert c1[i] == self.data[1][i]

    def test_two_formatters(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.INT_FORMAT))
        c1 = r.row_at(0)
        c2 = [1, 3, 5]
        print c1
        for i in range(0, len(c1)):
            assert type(c1[i]) == int
            assert c1[i] == c2[i]

    def test_custom_func(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        c1 = r.row_at(1)
        c2 = [2.0, 2.1, 3.0]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        c1 = r.row_at(2)
        c2 = [3, 3.2, 4]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_custom_func_with_a_general_converter(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        c1 = r.row_at(1)
        c2 = ["2.0", "2.1", "3.0"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]
        c1 = r.row_at(2)
        c2 = ["3.0", "3.2", "4.0"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def test_clear_formatters(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: float(x) + 1
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.FLOAT_FORMAT,
            f))
        r.add_formatter(pyexcel.formatters.SheetFormatter(
            pyexcel.formatters.STRING_FORMAT))
        r.clear_formatters()
        mydata = pyexcel.utils.to_dict(r.become_series())
        print mydata
        assert mydata['1'] == self.data['1']
        assert mydata['3'] == self.data['3']
        assert mydata['5'] == self.data['5']

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
