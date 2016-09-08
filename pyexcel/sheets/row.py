from pyexcel.sheets.filters import RowFilter
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
        self.ref.filter(RowFilter(indices).invert())

    def __delitem__(self, aslice):
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
        if isinstance(aslice, slice):
            my_range = utils.analyse_slice(aslice,
                                           self.ref.number_of_rows())
            self.ref.delete_rows(my_range)
        elif isinstance(aslice, tuple):
            self.ref.filter(RowFilter(list(aslice)))
        elif isinstance(aslice, list):
            self.ref.filter(RowFilter(aslice))
        else:
            self.ref.delete_rows([aslice])

    def __setitem__(self, aslice, c):
        """Override the operator to set items"""
        if isinstance(aslice, slice):
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
        if isinstance(aslice, slice):
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
        if isinstance(other, list):
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


class NamedRow(Row):
    """Series Sheet would have Named Row instead of Row

    Here is an example to merge sheets. Suppose we have the
    following three files::

        >>> import pyexcel as pe
        >>> data = [[1,2,3],[4,5,6],[7,8,9]]
        >>> s = pe.Sheet(data)
        >>> s.save_as("1.csv")
        >>> data2 = [['a','b','c'],['d','e','f'],['g','h','i']]
        >>> s2 = pe.Sheet(data2)
        >>> s2.save_as("2.csv")
        >>> data3=[[1.1, 2.2, 3.3],[4.4, 5.5, 6.6],[7.7, 8.8, 9.9]]
        >>> s3=pe.Sheet(data3)
        >>> s3.save_as("3.csv")


        >>> merged = pe.Sheet()
        >>> for file in ["1.csv", "2.csv", "3.csv"]:
        ...     r = pe.get_sheet(file_name=file)
        ...     merged.row += r
        >>> merged.save_as("merged.csv")

    Now let's verify what we had::

        >>> sheet = pe.get_sheet(file_name="merged.csv")

    this is added to overcome doctest's inability to handle
    python 3's unicode::

        >>> sheet.format(lambda v: str(v))
        >>> sheet
        merged.csv:
        +-----+-----+-----+
        | 1   | 2   | 3   |
        +-----+-----+-----+
        | 4   | 5   | 6   |
        +-----+-----+-----+
        | 7   | 8   | 9   |
        +-----+-----+-----+
        | a   | b   | c   |
        +-----+-----+-----+
        | d   | e   | f   |
        +-----+-----+-----+
        | g   | h   | i   |
        +-----+-----+-----+
        | 1.1 | 2.2 | 3.3 |
        +-----+-----+-----+
        | 4.4 | 5.5 | 6.6 |
        +-----+-----+-----+
        | 7.7 | 8.8 | 9.9 |
        +-----+-----+-----+

    .. testcleanup::
        >>> import os
        >>> os.unlink("1.csv")
        >>> os.unlink("2.csv")
        >>> os.unlink("3.csv")
        >>> os.unlink("merged.csv")

    """
    def select(self, names):
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
            >>> data = [
            ...     ['a', 1],
            ...     ['b', 1],
            ...     ['c', 1]
            ... ]
            >>> sheet = pe.Sheet(data, name_rows_by_column=0)
            >>> sheet.row.select(['a', 'b'])
            >>> sheet
            pyexcel sheet:
            +---+---+
            | a | 1 |
            +---+---+
            | b | 1 |
            +---+---+

        """
        if compact.is_array_type(names, str):
            indices = utils.names_to_indices(names, self.ref.rownames)
            Row.select(self, indices)
        else:
            Row.select(self, names)

    def __delitem__(self, column_name):
        """

        Examples::

            >>> import pyexcel as pe
            >>> data = [
            ...     ['a', 1],
            ...     ['b', 1],
            ...     ['c', 1]
            ... ]
            >>> sheet = pe.Sheet(data, name_rows_by_column=0)
            >>> del sheet.row['a', 'b']
            >>> sheet
            pyexcel sheet:
            +---+---+
            | c | 1 |
            +---+---+

        """
        if compact.is_string(type(column_name)):
            self.ref.delete_named_row_at(column_name)
        elif compact.is_tuple_consists_of_strings(column_name):
            indices = utils.names_to_indices(list(column_name),
                                             self.ref.rownames)
            Row.__delitem__(self, indices)
        else:
            Row.__delitem__(self, column_name)

    def __setitem__(self, str_or_aslice, c):
        if compact.is_string(type(str_or_aslice)):
            self.ref.set_named_row_at(str_or_aslice, c)
        else:
            Row.__setitem__(self, str_or_aslice, c)

    def __getitem__(self, str_or_aslice):
        if compact.is_string(type(str_or_aslice)):
            return self.ref.named_row_at(str_or_aslice)
        else:
            return Row.__getitem__(self, str_or_aslice)

    def __iadd__(self, other):
        """Overload += sign

        :param list other: the row header must be the first element.
        :return: self
        """
        if isinstance(other, compact.OrderedDict):
            self.ref.extend_rows(other)
        else:
            Row.__iadd__(self, other)
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
