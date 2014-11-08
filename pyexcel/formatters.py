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
from ._compact import is_array_type


def string_to_format(value, FORMAT):
    """Convert string to specified format"""
    if FORMAT == float:
        try:
            ret = float(value)
        except ValueError:
            ret = value
    elif FORMAT == int:
        try:
            ret = float(value)
            ret = int(ret)
        except ValueError:
            ret = value
    else:
        ret = value

    return ret


def float_to_format(value, FORMAT):
    """Convert float to specified format"""
    if FORMAT == int:
        ret = int(value)
    elif FORMAT == str:
        ret = str(value)
    else:
        ret = value

    return ret


def int_to_format(value, FORMAT):
    """Convert int to specified format"""
    if FORMAT == float:
        ret = float(value)
    elif FORMAT == str:
        ret = str(value)
    else:
        ret = value
    return ret


def date_to_format(value, FORMAT):
    """Convert date to specified format"""
    if FORMAT == str:
        if isinstance(value, datetime.date):
            ret = value.strftime("%d/%m/%y")
        elif isinstance(value, datetime.datetime):
            ret = value.strftime("%d/%m/%y")
        elif isinstance(value, datetime.time):
            ret = value.strftime("%H:%M:%S")
    else:
        ret = value
    return ret


def boolean_to_format(value, FORMAT):
    """Convert bool to specified format"""
    if FORMAT == float:
        ret = float(value)
    elif FORMAT == str:
        if value == 1:
            ret = "true"
        else:
            ret = "false"
    else:
        ret = value
    return ret


def empty_to_format(value, FORMAT):
    """Convert empty value to specified format"""
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
    datetime.time: date_to_format,
    datetime.date: date_to_format,
    bool: boolean_to_format,
    None: empty_to_format,
}

if six.PY2:
    CONVERSION_FUNCTIONS[unicode] = string_to_format


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
        if self.converter is not None and isinstance(self.converter, types.FunctionType):
            return self.converter(new_value)
        else:
            return to_format(self.desired_format, new_value)


class ColumnFormatter(Formatter):
    """Apply formatting on columns"""
    def __init__(self, column_index, FORMAT, custom_converter=None):
        """
        Constructor
        
        :param int or list column_index: to which column or what columns
        to apply the formatter
        :param type FORMAT: the target format
        :param func custom_converter: the custom functional formatter
        """
        self.indices = column_index
        if isinstance(column_index, int):
            func = lambda r, c, v: c == column_index
        elif isinstance(column_index, list):
            if len(column_index) == 0:
                raise IndexError("column list is empty. do not waste resurce")
            if is_array_type(column_index, int):
                func = lambda r, c, v: c in column_index
            else:
                raise IndexError("column list should be a list of integers")
        else:
            raise NotImplementedError("%s is not supported" % type(column_index))
        Formatter.__init__(self, func, FORMAT, custom_converter)


class NamedColumnFormatter(ColumnFormatter):
    """Apply formatting using named columns"""
    def __init__(self, column_index, FORMAT, custom_converter=None):
        """
        Constructor
        
        :param int or list column_index: to which column or what columns
        to apply the formatter
        :param type FORMAT: the target format
        :param func custom_converter: the custom functional formatter
        """
        self.indices = column_index
        if isinstance(column_index, str):
            func = lambda r, c, v: c == column_index
        elif isinstance(column_index, list):
            if len(column_index) == 0:
                raise IndexError("column list is empty. do not waste resurce")
            if is_array_type(column_index, str):
                func = lambda r, c, v: c in column_index
            else:
                raise IndexError("column list should be a list of strings")
        else:
            raise NotImplementedError("%s is not supported" % type(column_index))
        Formatter.__init__(self, func, FORMAT, custom_converter)

    def update_index(self, new_indices):
        self.indices = new_indices
        if isinstance(new_indices, int):
            self.quanlify_func = lambda r, c, v: c == new_indices
        elif isinstance(new_indices, list):
            self.quanlify_func = lambda r, c, v: c in new_indices
        else:
            raise NotImplementedError("%s is not supported" % type(new_indices))

class RowFormatter(Formatter):
    """Row Formatter"""    
    def __init__(self, row_index, FORMAT, custom_converter=None):
        """
        Constructor

        :param int or list row_index: to which row or what rows to apply the
        formatter
        :param type FORMAT: the target format
        :param func custom_converter: the custom functional formatter
        """
        self.indices = row_index
        if isinstance(row_index, int):
            func = lambda r, c, v: r == row_index
        elif isinstance(row_index, list):
            if len(row_index) == 0:
                raise IndexError("row list is empty. do not waste resurce")
            if is_array_type(row_index, int):
                func = lambda r, c, v: r in row_index
            else:
                raise IndexError("row list should be a list of integers")
        else:
            raise NotImplementedError("%s is not supported" % type(row_index))
        Formatter.__init__(self, func, FORMAT, custom_converter)


class NamedRowFormatter(RowFormatter):
    """Formatting rows using named rows"""    
    def __init__(self, row_index, FORMAT, custom_converter=None):
        """
        Constructor

        :param int or list row_index: to which row or what rows to apply the
        formatter
        :param type FORMAT: the target format
        :param func custom_converter: the custom functional formatter
        """
        self.indices = row_index
        if isinstance(row_index, str):
            func = lambda r, c, v: r == row_index
        elif isinstance(row_index, list):
            if len(row_index) == 0:
                raise IndexError("row list is empty. do not waste resurce")
            if is_array_type(row_index, str):
                func = lambda r, c, v: r in row_index
            else:
                raise IndexError("row list should be a list of strings")
        else:
            raise NotImplementedError("%s is not supported" % type(row_index))
        Formatter.__init__(self, func, FORMAT, custom_converter)
            
    def update_index(self, new_indices):
        if isinstance(new_indices, int):
            self.quanlify_func = lambda r, c, v: r == new_indices
        elif isinstance(new_indices, list):
            self.quanlify_func = lambda r, c, v: r in new_indices
        else:
            raise NotImplementedError("%s is not supported" % type(new_indices))
            

class SheetFormatter(Formatter):
    """Apply the formatter to all cells in the sheet
    """
    def __init__(self, FORMAT, custom_converter=None):
        Formatter.__init__(self, None, FORMAT, custom_converter)

    def is_my_business(self, row, column, value):
        return True
