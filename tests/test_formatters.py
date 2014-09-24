import pyexcel
import os


class TestFormatFunction:
    def test_date_format(self):
        d = "11-Jan-14"
        n_d = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.DATE_FORMAT,
            d)
        assert d == n_d

    def test_string_format(self):
        value = 11
        n_value = pyexcel.formatters.to_format(
            pyexcel.formatters.STRING_FORMAT,
            pyexcel.formatters.STRING_FORMAT, value)
        assert n_value == "11"

    def test_int_format(self):
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


class TestColumnFormatter:
    def setUp(self):
        self.data = {
            "1": [1, 2, 3, 4, 5, 6, 7, 8],
            "2": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "3": [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            "4": ["1.1", "2.2", "3.3", "4.4", "5.5", "6.6", "7,7", "8.8"],
            "5": [2, 3, 4, 5, 6, 7, 8, 9],
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
            
    def test_custom_func(self):
        r = pyexcel.Reader(self.testfile)
        f = lambda x, t: int(x) + 1
        r.add_formatter(pyexcel.formatters.ColumnFormatter(
            0,
            f))
        c1 = r.column_at(0)[1:]
        c2 = self.data["5"]
        for i in range(0, len(c1)):
            assert c1[i] == c2[i]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

        