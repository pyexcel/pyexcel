from . import _shared as utils
from .formatters import RowFormatter
import pyexcel._compact as compact


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
        >>> m = pe.sheets.Matrix(data)
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
        self.ref = matrix

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
        to_remove = []
        for index in self.ref.row_range():
            if index not in indices:
                to_remove.append(index)
        self.ref.filter(row_indices=to_remove)

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
            self.ref.delete_named_row_at(locator)
        elif compact.is_tuple_consists_of_strings(locator):
            indices = utils.names_to_indices(list(locator),
                                             self.ref.rownames)
            self.ref.delete_rows(indices)
        elif isinstance(locator, slice):
            my_range = utils.analyse_slice(locator,
                                           self.ref.number_of_rows())
            self.ref.delete_rows(my_range)
        elif isinstance(locator, tuple):
            self.ref.filter(row_indices=(list(locator)))
        elif isinstance(locator, list):
            self.ref.filter(row_indices=locator)
        else:
            self.ref.delete_rows([locator])

    def __setitem__(self, aslice, c):
        """Override the operator to set items"""
        if compact.is_string(type(aslice)):
            self.ref.set_named_row_at(aslice, c)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.ref.number_of_rows())
            for i in my_range:
                self.ref.set_row_at(i, c)
        else:
            self.ref.set_row_at(aslice, c)

    def __getitem__(self, aslice):
        """By default, this class recognize from top to bottom
        from left to right"""
        index = aslice
        if compact.is_string(type(aslice)):
            return self.ref.named_row_at(aslice)
        elif isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.ref.number_of_rows())
            results = []
            for i in my_range:
                results.append(self.ref.row_at(i))
            return results
        if index in self.ref.row_range():
            return self.ref.row_at(index)
        else:
            raise IndexError

    def __iadd__(self, other):
        """Overload += sign

        :return: self
        """
        if isinstance(other, compact.OrderedDict):
            self.ref.extend_rows(other)
        elif isinstance(other, list):
            self.ref.extend_rows(other)
        elif hasattr(other, '_array'):
            self.ref.extend_rows(other._array)
        else:
            raise TypeError
        return self

    def __add__(self, other):
        """Overload += sign

        :return: self
        """
        self.__iadd__(other)
        return self.ref

    def format(self,
               row_index=None, formatter=None,
               format_specs=None, on_demand=False):
        """Format a row
        """
        def handle_one_formatter(rows, theformatter, on_demand):
            new_indices = rows
            if len(self.ref.rownames) > 0:
                new_indices = utils.names_to_indices(rows, self.ref.rownames)
            aformatter = RowFormatter(new_indices, theformatter)
            if on_demand:
                self.ref.add_formatter(aformatter)
            else:
                self.ref.apply_formatter(aformatter)
        if row_index is not None:
            handle_one_formatter(row_index, formatter, on_demand)
        elif format_specs:
            for spec in format_specs:
                if len(spec) == 3:
                    handle_one_formatter(spec[0], spec[1],
                                         on_demand)
                else:
                    handle_one_formatter(spec[0], spec[1],
                                         on_demand)
