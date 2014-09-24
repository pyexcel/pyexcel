"""
    pyexcel.formatters
    ~~~~~~~~~~~~~~~~~~~

    These utilities help format the content

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import datetime
import xlrd
import types


DATE_FORMAT = "d"
FLOAT_FORMAT = "f"
INT_FORMAT = "i"
UNICODE_FORMAT = "u"
STRING_FORMAT = "s"
BOOLEAN_FORMAT = "b"
EMPTY = "e"


XLS_FORMAT_CONVERSION = {
    xlrd.XL_CELL_TEXT: STRING_FORMAT,
    xlrd.XL_CELL_EMPTY: EMPTY,
    xlrd.XL_CELL_DATE: DATE_FORMAT,
    xlrd.XL_CELL_NUMBER: FLOAT_FORMAT,
    xlrd.XL_CELL_DATE: FLOAT_FORMAT,
    xlrd.XL_CELL_BOOLEAN: INT_FORMAT,
    xlrd.XL_CELL_BLANK: EMPTY,
    xlrd.XL_CELL_ERROR: EMPTY
}


def string_to_format(value, FORMAT):
    if FORMAT == FLOAT_FORMAT:
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

def float_to_format(value, FORMAT):
    if FORMAT == INT_FORMAT:
        try:
            ret = int(value)
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


def int_to_format(value, FORMAT):
    if FORMAT == FLOAT_FORMAT:
        ret = float(value)
    elif FORMAT == STRING_FORMAT:
        try:
            ret = str(value)
        except:
            ret = "N/A"
    else:
        ret = value
    return ret


def date_to_format(value, FORMAT):
    if FORMAT == DATE_FORMAT:
        ret = value
    elif FORMAT == STRING_FORMAT:
        ret = value.isoformat()
    else:
        ret = value
    return ret


def boolean_to_format(value, FORMAT):
    if FORMAT == FLOAT_FORMAT:
        ret = float(value)
    elif FORMAT == STRING_FORMAT:
        if value == 1:
            ret = "True"
        else:
            ret = "False"
    else:
        ret = value
    return ret

    
def empty_to_format(value, FORMAT):
    if FORMAT == DATE_FORMAT:
        ret = None
    elif FORMAT == FLOAT_FORMAT:
        ret = 0.0
    elif FORMAT == INT_FORMAT:
        ret = 0
    elif FORMAT == STRING_FORMAT:
        ret = ""
    else:
        ret = value
    return ret


CONVERSION_FUNCTIONS = {
    STRING_FORMAT: string_to_format,
    FLOAT_FORMAT: float_to_format,
    INT_FORMAT: int_to_format,
    DATE_FORMAT: date_to_format,
    BOOLEAN_FORMAT: boolean_to_format,
    EMPTY: empty_to_format
}


def to_format(from_type, to_type, value):
    func = CONVERSION_FUNCTIONS[from_type]
    return func(value, to_type)


class Formatter:
    """Generic formatter

    Formatter starts when the quanlifying functions returns true
    cell's row, column and value are fed to the quanlifying functions
    """
    def __init__(self, quanlify_func, FORMAT):
        self.quanlify_func = quanlify_func
        self.desired_format = FORMAT

    def is_my_business(self, row, column, value):
        return self.quanlify_func(row, column, value)

    def do_format(self, value, ctype):
        if type(self.desired_format) == types.FunctionType:
            return self.desired_format(value, ctype)
        else:
            return to_format(ctype, self.desired_format, value)


class ColumnFormatter(Formatter):
    def __init__(self, column_index, FORMAT):
        func = lambda r, c, v: c == column_index
        Formatter.__init__(self, func, FORMAT)
