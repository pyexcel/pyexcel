"""
    pyexcel.internal.sheets.column
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Generic table column

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import types
from functools import partial

from . import _shared as utils
from .formatters import to_format
import pyexcel._compact as compact


class Column:
    """Represent columns of a matrix

    .. table:: "example.csv"

        = = =
        1 2 3
        4 5 6
        7 8 9
        = = =

    Let us manipulate the data columns on the above data matrix::

        >>> import pyexcel as pe
        >>> data = [[1,2,3], [4,5,6], [7,8,9]]
        >>> m = pe.internal.sheets.Matrix(data)
        >>> m.column[0]
        [1, 4, 7]
        >>> m.column[2] = [0, 0, 0]
        >>> m.column[2]
        [0, 0, 0]
        >>> del m.column[1]
        >>> m.column[1]
        [0, 0, 0]
        >>> m.column[2]
        Traceback (most recent call last):
            ...
        IndexError

    """
    def __init__(self, matrix):
        self.__ref = matrix

    def select(self, indices):
        """
        Examples:

            >>> import pyexcel as pe
            >>> data = [[1,2,3,4,5,6,7,9]]
            >>> sheet = pe.Sheet(data)
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+---+---+---+---+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
            +---+---+---+---+---+---+---+---+
            >>> sheet.column.select([1,2,3,5])
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+
            | 2 | 3 | 4 | 6 |
            +---+---+---+---+
            >>> data = [[1,2,3,4,5,6,7,9]]
            >>> sheet = pe.Sheet(data)
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+---+---+---+---+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
            +---+---+---+---+---+---+---+---+
            >>> sheet.column.select([1,2,3,5])
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+
            | 2 | 3 | 4 | 6 |
            +---+---+---+---+
            >>> data = [
            ...     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            ...     [1,2,3,4,5,6,7,9],
            ... ]
            >>> sheet = pe.Sheet(data, name_columns_by_row=0)
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+---+---+---+---+
            | a | b | c | d | e | f | g | h |
            +===+===+===+===+===+===+===+===+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
            +---+---+---+---+---+---+---+---+
            >>> del sheet.column['a', 'b', 'i', 'f'] # doctest:+ELLIPSIS
            Traceback (most recent call last):
                ...
            ValueError: ...
            >>> sheet.column.select(['a', 'c', 'e', 'h'])
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+
            | a | c | e | h |
            +===+===+===+===+
            | 1 | 3 | 5 | 9 |
            +---+---+---+---+
        """
        new_indices = []
        if compact.is_array_type(indices, str):
            new_indices = utils.names_to_indices(indices,
                                                 self.__ref.colnames)
        else:
            new_indices = indices
        to_remove = []
        for index in self.__ref.column_range():
            if index not in new_indices:
                to_remove.append(index)
        self.__ref.filter(column_indices=to_remove)

    def __delitem__(self, aslice):
        """Override the operator to delete items

        Examples:

            >>> import pyexcel as pe
            >>> data = [[1,2,3,4,5,6,7,9]]
            >>> sheet = pe.Sheet(data)
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+---+---+---+---+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
            +---+---+---+---+---+---+---+---+
            >>> del sheet.column[1,2,3,5]
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+
            | 1 | 5 | 7 | 9 |
            +---+---+---+---+
            >>> data = [
            ...     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            ...     [1,2,3,4,5,6,7,9],
            ... ]
            >>> sheet = pe.Sheet(data, name_columns_by_row=0)
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+---+---+---+---+
            | a | b | c | d | e | f | g | h |
            +===+===+===+===+===+===+===+===+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
            +---+---+---+---+---+---+---+---+
            >>> del sheet.column['a', 'b', 'i', 'f'] # doctest:+ELLIPSIS
            Traceback (most recent call last):
                ...
            ValueError: ...
            >>> del sheet.column['a', 'c', 'e', 'h']
            >>> sheet
            pyexcel sheet:
            +---+---+---+---+
            | b | d | f | g |
            +===+===+===+===+
            | 2 | 4 | 6 | 7 |
            +---+---+---+---+

        """
        is_sheet = (compact.is_string(type(aslice)) and
                    hasattr(self.__ref, 'delete_named_column_at'))
        if is_sheet:
            self.__ref.delete_named_column_at(aslice)
        elif compact.is_tuple_consists_of_strings(aslice):
            indices = utils.names_to_indices(list(aslice),
                                             self.__ref.colnames)
            self.__ref.delete_columns(indices)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.__ref.number_of_columns())
            self.__ref.delete_columns(my_range)
        elif isinstance(aslice, str):
            index = utils.excel_column_index(aslice)
            self.__ref.delete_columns([index])
        elif isinstance(aslice, tuple):
            indices = list(aslice)
            self.__ref.filter(column_indices=indices)
        elif isinstance(aslice, list):
            indices = aslice
            self.__ref.filter(column_indices=indices)
        elif isinstance(aslice, int):
            self.__ref.delete_columns([aslice])
        elif isinstance(aslice, types.LambdaType):
            self._delete_columns_by_content(aslice)
        elif isinstance(aslice, types.FunctionType):
            self._delete_columns_by_content(aslice)
        else:
            raise IndexError

    def _delete_columns_by_content(self, locator):
        to_remove = []
        for index, column in enumerate(self.__ref.columns()):
            if locator(index, column):
                to_remove.append(index)
        if len(to_remove) > 0:
            self.__ref.delete_columns(to_remove)

    def __setitem__(self, aslice, c):
        """Override the operator to set items"""
        is_sheet = (compact.is_string(type(aslice)) and
                    hasattr(self.__ref, 'set_named_column_at'))
        if is_sheet:
            self.__ref.set_named_column_at(aslice, c)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.__ref.number_of_columns())
            for i in my_range:
                self.__ref.set_column_at(i, c)
        elif isinstance(aslice, str):
            index = utils.excel_column_index(aslice)
            self.__ref.set_column_at(index, c)
        elif isinstance(aslice, int):
            self.__ref.set_column_at(aslice, c)
        else:
            raise IndexError

    def __getitem__(self, aslice):
        """By default, this class recognize from top to bottom
        from left to right"""
        index = aslice
        is_sheet = (compact.is_string(type(aslice)) and
                    hasattr(self.__ref, 'named_column_at'))
        if is_sheet:
            return self.__ref.named_column_at(aslice)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.__ref.number_of_columns())
            results = []
            for i in my_range:
                results.append(self.__ref.column_at(i))
            return results
        elif isinstance(aslice, str):
            index = utils.excel_column_index(aslice)
        if index in self.__ref.column_range():
            return self.__ref.column_at(index)
        else:
            raise IndexError

    def __iadd__(self, other):
        """Overload += sign

        :return: self
        """
        if isinstance(other, compact.OrderedDict):
            self.__ref.extend_columns(other)
        elif isinstance(other, list):
            self.__ref.extend_columns(other)
        elif hasattr(other, 'get_internal_array'):
            self.__ref.extend_columns_with_rows(other.get_internal_array())
        else:
            raise TypeError
        return self

    def __add__(self, other):
        """Overload += sign

        :return: self
        """
        self.__iadd__(other)
        return self.__ref

    def format(self,
               column_index=None, formatter=None,
               format_specs=None):
        """Format a column
        """
        def handle_one_formatter(columns, theformatter):
            new_indices = columns
            if len(self.__ref.colnames) > 0:
                new_indices = utils.names_to_indices(columns,
                                                     self.__ref.colnames)
            converter = None
            if isinstance(theformatter, types.FunctionType):
                converter = theformatter
            else:
                converter = partial(to_format, theformatter)

            if isinstance(new_indices, list):
                for rcolumn in self.__ref.column_range():
                    if rcolumn in new_indices:
                        for row in self.__ref.row_range():
                            value = self.__ref.cell_value(row, rcolumn)
                            value = converter(value)
                            self.__ref.cell_value(row, rcolumn, value)
            else:
                for row in self.__ref.row_range():
                    value = self.__ref.cell_value(row, new_indices)
                    value = converter(value)
                    self.__ref.cell_value(row, new_indices, value)

        if column_index is not None:
            handle_one_formatter(column_index, formatter)
        elif format_specs:
            for spec in format_specs:
                handle_one_formatter(spec[0], spec[1])
