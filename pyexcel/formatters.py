"""
    pyexcel.formatters
    ~~~~~~~~~~~~~~~~~~~

    Format the data types

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import datetime


DATE_FORMAT = "d"
FLOAT_FORMAT = "f"
INT_FORMAT = "i"
UNICODE_FORMAT = "u"
STRING_FORMAT = "s"


def doformat(FORMAT, value):
    if FORMAT == DATE_FORMAT:
        ret = datetime.parse_datetime(value)
    elif FORMAT == FLOAT_FORMAT:
        try:
            ret = float(value)
        except ValueError:
            ret = "N/A"
    elif FORMAT == INT_FORMAT:
        try:
            ret = float(value)
            ret = int(ret)
        except ValueError:
            ret = "N/A"
    elif FORMAT == STRING_FORMAT:
        try:
            ret = str(value)
        except:
            ret = "N/A"
    else:
        ret = value

    return ret


class Formatter:
    """Generic formatter

    Formatter starts when the quanlifying functions returns true
    cell's row, column and value are fed to the quanlifying functions
    """
    def __init__(self, quanlify_func, FORMAT):
        self.quanlify_func = quanlify_func
        self.format = FORMAT

    def is_my_business(self, row, column, value):
        return self.quanlify_func(row, column, value)

    def format(self, value):
        return doformat(value)


class ColumnFormatter(Formatter):
    def __init__(self, column_index, FORMAT):
        func = lambda r, c, v: c == column_index
        Formatter.__init__(self, func, FORMAT)
