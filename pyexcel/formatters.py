"""
    pyexcel.formatters
    ~~~~~~~~~~~~~~~~~~~

    These utilities help format the content

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import six
import types
import datetime


def string_to_format(value, FORMAT):
    if FORMAT == float:
        try:
            ret = float(value)
        except ValueError:
            ret = "N/A"
    elif FORMAT == int:
        try:
            ret = float(value)
            ret = int(ret)
        except ValueError:
            ret = "N/A"
    else:
        ret = value

    return ret


def float_to_format(value, FORMAT):
    if FORMAT == int:
        ret = int(value)
    elif FORMAT == str:
        ret = str(value)
    else:
        ret = value

    return ret


def int_to_format(value, FORMAT):
    if FORMAT == float:
        ret = float(value)
    elif FORMAT == str:
        ret = str(value)
    else:
        ret = value
    return ret


def date_to_format(value, FORMAT):
    if FORMAT == datetime.datetime:
        ret = value
    elif FORMAT == str:
        if isinstance(value, datetime.date):
            ret = value.strftime("%d/%m/%y")
        elif isinstance(value, datetime.datetime):
            ret = value.strftime("%d/%m/%y")
        elif isinstance(value, datetime.time):
            ret = value.strftime("%H:%M:%S")
        else:
            ret = value
    else:
        ret = value
    return ret


def boolean_to_format(value, FORMAT):
    if FORMAT == float:
        ret = float(value)
    elif FORMAT == str:
        if value == 1:
            ret = "True"
        else:
            ret = "False"
    else:
        ret = value
    return ret


def empty_to_format(value, FORMAT):
    if FORMAT == float:
        ret = 0.0
    elif FORMAT == int:
        ret = 0
    else:
        ret = ""
    return ret


CONVERSION_FUNCTIONS = {
    str: string_to_format,
    float: float_to_format,
    int: int_to_format,
    datetime.datetime: date_to_format,
    bool: boolean_to_format,
    None: empty_to_format,
}

if six.PY2:
    CONVERSION_FUNCTIONS[unicode] = string_to_format


def to_format(from_type, to_type, value):
    """Wrapper utility function for format different formats"""
    func = CONVERSION_FUNCTIONS[from_type]
    return func(value, to_type)


class Formatter:
    """Generic formatter

    Formatter starts when the quanlifying functions returns true
    cell's row, column and value are fed to the quanlifying functions
    """
    def __init__(self, quanlify_func, FORMAT, custom_converter=None):
        self.quanlify_func = quanlify_func
        self.desired_format = FORMAT
        self.converter = custom_converter

    def is_my_business(self, row, column, value):
        return self.quanlify_func(row, column, value)

    def do_format(self, value, ctype):
        if self.converter is not None and isinstance(self.converter, types.FunctionType):
            return self.converter(value, ctype)
        else:
            return to_format(ctype, self.desired_format, value)


class ColumnFormatter(Formatter):
    """Column Formatter"""
    def __init__(self, column_index, FORMAT, custom_converter=None):
        func = lambda r, c, v: c == column_index
        Formatter.__init__(self, func, FORMAT, custom_converter)


class RowFormatter(Formatter):
    def __init__(self, row_index, FORMAT, custom_converter=None):
        func = lambda r, c, v: r == row_index
        Formatter.__init__(self, func, FORMAT, custom_converter)


class SheetFormatter(Formatter):
    """
    Apply the formatter to all cells in the sheet
    """
    def __init__(self, FORMAT, custom_converter=None):
        Formatter.__init__(self, None, FORMAT, custom_converter)

    def is_my_business(self, row, column, value):
        return True
