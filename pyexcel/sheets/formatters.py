"""
    pyexcel.formatters
    ~~~~~~~~~~~~~~~~~~~

    These utilities help format the content

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import types
import datetime
from pyexcel._compact import is_array_type, PY2
from pyexcel.constants import (
    MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST,
    MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE,
    MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE
)


def string_to_format(value, target_format):
    """Convert string to specified format"""
    if target_format == float:
        try:
            ret = float(value)
        except ValueError:
            ret = value
    elif target_format == int:
        try:
            ret = float(value)
            ret = int(ret)
        except ValueError:
            ret = value
    else:
        ret = value

    return ret


def float_to_format(value, target_format):
    """Convert float to specified format"""
    if target_format == int:
        ret = int(value)
    elif target_format == str:
        ret = str(value)
    else:
        ret = value

    return ret


def int_to_format(value, target_format):
    """Convert int to specified format"""
    if target_format == float:
        ret = float(value)
    elif target_format == str:
        ret = str(value)
    else:
        ret = value
    return ret


def date_to_format(value, target_format):
    """Convert date to specified format"""
    if target_format == str:
        if isinstance(value, datetime.date):
            ret = value.strftime("%d/%m/%y")
        elif isinstance(value, datetime.datetime):
            ret = value.strftime("%d/%m/%y")
        elif isinstance(value, datetime.time):
            ret = value.strftime("%H:%M:%S")
    else:
        ret = value
    return ret


def boolean_to_format(value, target_format):
    """Convert bool to specified format"""
    if target_format == float:
        ret = float(value)
    elif target_format == str:
        if value == 1:
            ret = "true"
        else:
            ret = "false"
    else:
        ret = value
    return ret


def empty_to_format(value, target_format):
    """Convert empty value to specified format"""
    if target_format == float:
        ret = 0.0
    elif target_format == int:
        ret = 0
    else:
        ret = ""
    return ret


CONVERSION_FUNCTIONS = {
    str: string_to_format,
    float: float_to_format,
    int: int_to_format,
    datetime.datetime: date_to_format,
    datetime.time: date_to_format,
    datetime.date: date_to_format,
    bool: boolean_to_format,
    None: empty_to_format,
}

if PY2:
    CONVERSION_FUNCTIONS[unicode] = string_to_format
    CONVERSION_FUNCTIONS[long] = float_to_format


def to_format(to_type, value):
    """Wrapper utility function for format different formats

    :param type from_type: a python type
    :param type to_type: a python type
    :param value value: a python value
    """
    if value is not None:
        if value == "":
            from_type = None
        else:
            from_type = type(value)
    else:
        from_type = None
    func = CONVERSION_FUNCTIONS[from_type]
    return func(value, to_type)


class Formatter(object):
    """Generic formatter

    Formatter starts when the quanlifying functions returns true
    cell's row, column and value are fed to the quanlifying functions
    """
    def __init__(self, quanlify_func, formatter, custom_converter=None):
        self.quanlify_func = quanlify_func
        self.formatter = formatter
        self.converter = custom_converter

    def is_my_business(self, row, column, value):
        """Check should this formatter be active for cell at (row, column) with value

        :param int row: the row index of current cell
        :param int column: the column index of current cell
        :param any value: the value of current cell
        :returns: True or False
            * True if the cell qualitifies
            * False if the cell does not

        """
        return self.quanlify_func(row, column, value)

    def do_format(self, value):
        new_value = value
        if value == "":
            new_value = None
        if isinstance(self.formatter, types.FunctionType):
            return self.formatter(new_value)
        else:
            return to_format(self.formatter, new_value)


class ColumnFormatter(Formatter):
    """Apply formatting on columns"""

    def __init__(self, column_index, formatter):
        """Constructor
        :param column_index: to which column or what
                             columns to apply the formatter
        :param formatter: the target format, or a custom
                          functional formatter
        """
        self.indices = column_index
        if isinstance(column_index, int):
            def func(r, c, v): return c == column_index
        elif isinstance(column_index, list):
            if len(column_index) == 0:
                raise IndexError(MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST)
            if is_array_type(column_index, int):
                def func(r, c, v): return c in column_index
            else:
                raise IndexError(MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE)
        else:
            raise NotImplementedError(
                "%s is not supported" % type(column_index))
        Formatter.__init__(self, func, formatter)


class NamedColumnFormatter(ColumnFormatter):
    """Apply formatting using named columns"""

    def __init__(self, column_index, formatter):
        """Constructor
        :param column_index: to which column or what
                             columns to apply the formatter
        :param formatter: the target format, or a custom
                          functional formatter
        """
        self.indices = column_index
        if isinstance(column_index, str):
            def func(r, c, v): return c == column_index
        elif isinstance(column_index, list):
            if len(column_index) == 0:
                raise IndexError(MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST)
            if is_array_type(column_index, str):
                def func(r, c, v): return c in column_index
            else:
                raise IndexError(MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE)
        else:
            raise NotImplementedError(
                "%s is not supported" % type(column_index))
        Formatter.__init__(self, func, formatter)

    def update_index(self, new_indices):
        self.indices = new_indices
        if isinstance(new_indices, int):
            def func(r, c, v): return c == new_indices
            self.quanlify_func = func
        elif isinstance(new_indices, list):
            def func(r, c, v): return c in new_indices
            self.quanlify_func = func
        else:
            raise NotImplementedError(
                "%s is not supported" % type(new_indices))


class RowFormatter(Formatter):
    """Row Formatter"""

    def __init__(self, row_index, formatter):
        """Constructor
        :param row_index: to which row or what
                             rows to apply the formatter
        :param formatter: the target format, or a custom
                          functional formatter
        """
        self.indices = row_index
        if isinstance(row_index, int):
            def func(r, c, v): return r == row_index
        elif isinstance(row_index, list):
            if len(row_index) == 0:
                raise IndexError(MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST)
            if is_array_type(row_index, int):
                def func(r, c, v): return r in row_index
            else:
                raise IndexError(MESSAGE_DATA_ERROR_COLUMN_LIST_INTEGER_TYPE)
        else:
            raise NotImplementedError(
                "%s is not supported" % type(row_index))
        Formatter.__init__(self, func, formatter)


class NamedRowFormatter(RowFormatter):
    """Formatting rows using named rows"""

    def __init__(self, row_index, formatter):
        """Constructor
        :param row_index: to which row or what
                             rows to apply the formatter
        :param formatter: the target format, or a custom
                          functional formatter
        """
        self.indices = row_index
        if isinstance(row_index, str):
            def func(r, c, v): return r == row_index
        elif isinstance(row_index, list):
            if len(row_index) == 0:
                raise IndexError(MESSAGE_DATA_ERROR_EMPTY_COLUMN_LIST)
            if is_array_type(row_index, str):
                def func(r, c, v): return r in row_index
            else:
                raise IndexError(MESSAGE_DATA_ERROR_COLUMN_LIST_STRING_TYPE)
        else:
            raise NotImplementedError(
                "%s is not supported" % type(row_index))
        Formatter.__init__(self, func, formatter)

    def update_index(self, new_indices):
        if isinstance(new_indices, int):
            def func(r, c, v): return r == new_indices
            self.quanlify_func = func
        elif isinstance(new_indices, list):
            def func(r, c, v): return r in new_indices
            self.quanlify_func = func
        else:
            raise NotImplementedError(
                "%s is not supported" % type(new_indices))


class SheetFormatter(Formatter):
    """
    Apply the formatter to all cells in the sheet
    """
    def __init__(self, formatter):
        Formatter.__init__(self, None, formatter)

    def is_my_business(self, row, column, value):
        return True
