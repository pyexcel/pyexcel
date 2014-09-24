import pyexcel
import os
import datetime


class TestFormatFunction:
    def _test_date_format(self):
        d = "11-Jan-14"
        n_d = pyexcel.formatters.doformat(
            pyexcel.formatters.DATE_FORMAT,
            d)
        assert isinstance(n_d, datetime.datetime)

    def test_string_format(self):
        value = 11
        n_value = pyexcel.formatters.doformat(
            pyexcel.formatters.STRING_FORMAT, value)
        assert n_value == "11"

    def test_int_format(self):
        value = "11"
        n_value = pyexcel.formatters.doformat(
            pyexcel.formatters.INT_FORMAT, value)
        assert n_value == 11
        value = "11.11111"
        n_value = pyexcel.formatters.doformat(
            pyexcel.formatters.INT_FORMAT,
            value)
        assert n_value == 11
        value = "abc"
        n_value = pyexcel.formatters.doformat(
            pyexcel.formatters.INT_FORMAT, value)
        assert n_value == "N/A"


class TestColumnFormatter:
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
        }
        self.testfile = "test.xlsx"
        w = pyexcel.Writer(self.testfile)
        w.write_dict(self.data)
        w.close()
        
    def _test_general_usage(self):
        r = pyexcel.Reader(self.testfile)
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            1,
            pyexcel.formatters.STRING_FORMAT))
        print r.column_at(0)
        print self.data["2"]
        assert r.column_at(0)[1:] == self.data["2"]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

        