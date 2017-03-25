import types
from functools import partial

from . import _shared as utils
import pyexcel._compact as compact
from .formatters import to_format


class Row:
    """Represent row of a matrix

    .. table:: "example.csv"

        = = =
        1 2 3
        4 5 6
        7 8 9
        = = =

    Above column manipulation can be performed on rows similarly. This section
    will not repeat the same example but show some advance usages.


        >>> import pyexcel as pe
        >>> data = [[1,2,3], [4,5,6], [7,8,9]]
        >>> m = pe.internal.sheets.Matrix(data)
        >>> m.row[0:2]
        [[1, 2, 3], [4, 5, 6]]
        >>> m.row[0:3] = [0, 0, 0]
        >>> m.row[2]
        [0, 0, 0]
        >>> del m.row[0:2]
        >>> m.row[0]
        [0, 0, 0]

    """
    def __init__(self, matrix):
        self.__ref = matrix

    def select(self, indices):
        """Delete row indices other than specified

        Examples:

            >>> import pyexcel as pe
            >>> data = [[1],[2],[3],[4],[5],[6],[7],[9]]
            >>> sheet = pe.Sheet(data)
            >>> sheet
            pyexcel sheet:
            +---+
            | 1 |
            +---+
            | 2 |
            +---+
            | 3 |
            +---+
            | 4 |
            +---+
            | 5 |
            +---+
            | 6 |
            +---+
            | 7 |
            +---+
            | 9 |
            +---+
            >>> sheet.row.select([1,2,3,5])
            >>> sheet
            pyexcel sheet:
            +---+
            | 2 |
            +---+
            | 3 |
            +---+
            | 4 |
            +---+
            | 6 |
            +---+

        """
        new_indices = []
        if compact.is_array_type(indices, str):
            new_indices = utils.names_to_indices(indices,
                                                 self.__ref.rownames)
        else:
            new_indices = indices
        to_remove = []
        for index in self.__ref.row_range():
            if index not in new_indices:
                to_remove.append(index)
        self.__ref.filter(row_indices=to_remove)

    def __delitem__(self, locator):
        """Override the operator to delete items

        Examples:

            >>> import pyexcel as pe
            >>> data = [[1],[2],[3],[4],[5],[6],[7],[9]]
            >>> sheet = pe.Sheet(data)
            >>> sheet
            pyexcel sheet:
            +---+
            | 1 |
            +---+
            | 2 |
            +---+
            | 3 |
            +---+
            | 4 |
            +---+
            | 5 |
            +---+
            | 6 |
            +---+
            | 7 |
            +---+
            | 9 |
            +---+
            >>> del sheet.row[1,2,3,5]
            >>> sheet
            pyexcel sheet:
            +---+
            | 1 |
            +---+
            | 5 |
            +---+
            | 7 |
            +---+
            | 9 |
            +---+

        """
        if compact.is_string(type(locator)):
            self.__ref.delete_named_row_at(locator)
        elif compact.is_tuple_consists_of_strings(locator):
            indices = utils.names_to_indices(list(locator),
                                             self.__ref.rownames)
            self.__ref.delete_rows(indices)
        elif isinstance(locator, slice):
            my_range = utils.analyse_slice(locator,
                                           self.__ref.number_of_rows())
            self.__ref.delete_rows(my_range)
        elif isinstance(locator, tuple):
            self.__ref.filter(row_indices=(list(locator)))
        elif isinstance(locator, list):
            self.__ref.filter(row_indices=locator)
        elif isinstance(locator, types.LambdaType):
            self._delete_rows_by_content(locator)
        elif isinstance(locator, types.FunctionType):
            self._delete_rows_by_content(locator)
        else:
            self.__ref.delete_rows([locator])

    def _delete_rows_by_content(self, locator):
        to_remove = []
        for index, row in enumerate(self.__ref.rows()):
            if locator(index, row):
                to_remove.append(index)
        if len(to_remove) > 0:
            self.__ref.delete_rows(to_remove)

    def __setitem__(self, aslice, c):
        """Override the operator to set items"""
        if compact.is_string(type(aslice)):
            self.__ref.set_named_row_at(aslice, c)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.__ref.number_of_rows())
            for i in my_range:
                self.__ref.set_row_at(i, c)
        else:
            self.__ref.set_row_at(aslice, c)

    def __getitem__(self, aslice):
        """By default, this class recognize from top to bottom
        from left to right"""
        index = aslice
        if compact.is_string(type(aslice)):
            return self.__ref.named_row_at(aslice)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.__ref.number_of_rows())
            results = []
            for i in my_range:
                results.append(self.__ref.row_at(i))
            return results
        if index in self.__ref.row_range():
            return self.__ref.row_at(index)
        else:
            raise IndexError

    def __iadd__(self, other):
        """Overload += sign

        :return: self
        """
        if isinstance(other, compact.OrderedDict):
            self.__ref.extend_rows(other)
        elif isinstance(other, list):
            self.__ref.extend_rows(other)
        elif hasattr(other, 'get_internal_array'):
            self.__ref.extend_rows(other.get_internal_array())
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
               row_index=None, formatter=None,
               format_specs=None):
        """Format a row
        """
        def handle_one_formatter(rows, theformatter):
            new_indices = rows
            if len(self.__ref.rownames) > 0:
                new_indices = utils.names_to_indices(rows, self.__ref.rownames)

            converter = None
            if isinstance(theformatter, types.FunctionType):
                converter = theformatter
            else:
                converter = partial(to_format, theformatter)

            if isinstance(new_indices, list):
                for rindex in self.__ref.row_range():
                    if rindex in new_indices:
                        for column in self.__ref.column_range():
                            value = self.__ref.cell_value(rindex, column)
                            value = converter(value)
                            self.__ref.cell_value(rindex, column, value)
            else:
                for column in self.__ref.column_range():
                    value = self.__ref.cell_value(new_indices, column)
                    value = converter(value)
                    self.__ref.cell_value(new_indices, column, value)

        if row_index is not None:
            handle_one_formatter(row_index, formatter)
        elif format_specs:
            for spec in format_specs:
                handle_one_formatter(spec[0], spec[1])
