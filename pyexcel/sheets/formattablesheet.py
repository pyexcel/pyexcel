"""
    pyexcel.sheets.formattablesheet
    ~~~~~~~~~~~~~~~~~~~

    Building on top of Matrix, adding formatting feature

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .matrix import Matrix
from ..formatters import (
    ColumnFormatter,
    RowFormatter,
    SheetFormatter
)
from ..constants import MESSAGE_NOT_IMPLEMENTED_01


class FormattableSheet(Matrix):
    """
    A represetation of Matrix that accept custom formatters
    """
    def __init__(self, array):
        """Constructor

        """
        Matrix.__init__(self, array)
        self._formatters = []

    def format(self, formatter, on_demand=False):
        """Apply a formatting action for the whole sheet

        Example::

            >>> import pyexcel as pe
            >>> # Given a dictinoary as the following
            >>> data = {
            ...     "1": [1, 2, 3, 4, 5, 6, 7, 8],
            ...     "3": [1.25, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ...     "5": [2, 3, 4, 5, 6, 7, 8, 9],
            ...     "7": [1, '',]
            ...     }
            >>> sheet = pe.get_sheet(adict=data)
            >>> sheet.row[1]
            [1, 1.25, 2, 1]
            >>> sheet.format(str)
            >>> sheet.row[1]
            ['1', '1.25', '2', '1']
            >>> sheet.format(int)
            >>> sheet.row[1]
            [1, 1, 2, 1]

        """
        sf = SheetFormatter(formatter)
        if on_demand:
            self.add_formatter(sf)
        else:
            self.apply_formatter(sf)

    def map(self, custom_function):
        """Execute a function across all cells of the sheet

        Example::

            >>> import pyexcel as pe
            >>> # Given a dictinoary as the following
            >>> data = {
            ...     "1": [1, 2, 3, 4, 5, 6, 7, 8],
            ...     "3": [1.25, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ...     "5": [2, 3, 4, 5, 6, 7, 8, 9],
            ...     "7": [1, '',]
            ...     }
            >>> sheet = pe.get_sheet(adict=data)
            >>> sheet.row[1]
            [1, 1.25, 2, 1]
            >>> sheet.map(lambda value: (float(value) if value != None else 0)+1 )
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]

        """
        sf = SheetFormatter(custom_function)
        self.apply_formatter(sf)

    def apply_formatter(self, aformatter):
        """Apply the formatter immediately. No return ticket

        Example::

            >>> import pyexcel as pe
            >>> # Given a dictinoary as the following
            >>> data = {
            ...     "1": [1, 2, 3, 4, 5, 6, 7, 8],
            ...     "3": [1.25, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ...     "5": [2, 3, 4, 5, 6, 7, 8, 9],
            ...     "7": [1, '',]
            ...     }
            >>> sheet = pe.get_sheet(adict=data)
            >>> sheet.row[1]
            [1, 1.25, 2, 1]
            >>> aformatter = pe.SheetFormatter(lambda value: (float(value) if value != None else 0)+1 )
            >>> sheet.apply_formatter(aformatter)
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]
            >>> sheet.clear_formatters() # no return ticket
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]

        """
        if isinstance(aformatter, ColumnFormatter):
            self._apply_column_formatter(aformatter)
        elif isinstance(aformatter, RowFormatter):
            self._apply_row_formatter(aformatter)
        else:
            # to do don't use add_formatter'
            self.add_formatter(aformatter)
            self.freeze_formatters()

    def _apply_column_formatter(self, column_formatter):
        def filter_indices(column_index):
            return column_formatter.is_my_business(-1, column_index, -1)
        applicables = [i for i in self.column_range() if filter_indices(i)]
        # set the values
        for rindex in self.row_range():
            for cindex in applicables:
                value = self.cell_value(rindex, cindex)
                value = column_formatter.do_format(value)
                self.cell_value(rindex, cindex, value)

    def _apply_row_formatter(self, row_formatter):
        def filter_indices(row_index):
            return row_formatter.is_my_business(row_index, -1, -1)
        applicables = [i for i in self.row_range() if filter_indices(i)]
        # set the values
        for rindex in applicables:
            for cindex in self.column_range():
                value = self.cell_value(rindex, cindex)
                value = row_formatter.do_format(value)
                self.cell_value(rindex, cindex, value)

    def add_formatter(self, aformatter):
        """Add a lazy formatter.

        The formatter takes effect on the fly when a cell value is read
        This is cost effective when you have a big data table
        and you use only a few columns or rows. If you have farily modest
        data table, you can choose apply_formatter() too.

        :param Formatter aformatter: a custom formatter

        Example::

            >>> import pyexcel as pe
            >>> # Given a dictinoary as the following
            >>> data = {
            ...     "1": [1, 2, 3, 4, 5, 6, 7, 8],
            ...     "3": [1.25, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ...     "5": [2, 3, 4, 5, 6, 7, 8, 9],
            ...     "7": [1, '',]
            ...     }
            >>> sheet = pe.get_sheet(adict=data)
            >>> sheet.row[1]
            [1, 1.25, 2, 1]
            >>> aformatter = pe.SheetFormatter(lambda value: (float(value) if value != None else 0)+1 )
            >>> sheet.add_formatter(aformatter)
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]
            >>> sheet.clear_formatters()
            >>> sheet.row[1]
            [1, 1.25, 2, 1]
            >>> aformatter = pe.SheetFormatter(lambda value: (float(value) if value != None else 0)+1 )
            >>> sheet.apply_formatter(aformatter)
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]
            >>> sheet.clear_formatters() # no return ticket
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]

        """
        self._formatters.append(aformatter)

    def remove_formatter(self, aformatter):
        """Remove a formatter

        :param Formatter aformatter: a custom formatter
        """
        self._formatters.remove(aformatter)

    def clear_formatters(self):
        """Clear all formatters

        Example::

            >>> import pyexcel as pe
            >>> # Given a dictinoary as the following
            >>> data = {
            ...     "1": [1, 2, 3, 4, 5, 6, 7, 8],
            ...     "3": [1.25, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8],
            ...     "5": [2, 3, 4, 5, 6, 7, 8, 9],
            ...     "7": [1, '',]
            ...     }
            >>> sheet = pe.get_sheet(adict=data)
            >>> sheet.row[1]
            [1, 1.25, 2, 1]
            >>> aformatter = pe.SheetFormatter(lambda value: (float(value) if value != None else 0)+1)
            >>> sheet.add_formatter(aformatter)
            >>> sheet.row[1]
            [2.0, 2.25, 3.0, 2.0]
            >>> sheet.clear_formatters()
            >>> sheet.row[1]
            [1, 1.25, 2, 1]


        """
        self._formatters = []

    def freeze_formatters(self):
        """Apply all added formatters and clear them

        The tradeoff here is when you extend the sheet, you won't
        get the effect of previously applied formatters because they
        are applied and gone.
        """
        if len(self._formatters) < 1:
            return
        # set the values
        for rindex in self.row_range():
            for cindex in self.column_range():
                value = self.cell_value(rindex, cindex)
                self.cell_value(rindex, cindex, value)
        # clear formatters
        self._formatters = []

    def _cell_value(self, row, column, new_value=None):
        """
        Random access to the xls cells
        """
        if new_value is None:
            try:
                value = self.array[row][column]
            except IndexError:
                value = ""
            if len(self._formatters) > 0:
                for f in self._formatters:
                    if f.is_my_business(row, column, value):
                        value = f.do_format(value)
            return value
        else:
            self.array[row][column] = new_value
            return new_value

    def cell_value(self, row, column, new_value=None):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            # apply formatting
            return self._cell_value(row, column, new_value)
        else:
            return None

    def __add__(self, other):
        """Overload the + sign

        :returns: a new book
        """
        from ..book import Book
        from ..utils import to_dict, local_uuid
        content = {}
        content[self.name] = self.array
        if isinstance(other, Book):
            b = to_dict(other)
            for l in b.keys():
                new_key = l
                if len(b.keys()) == 1:
                    new_key = other.filename
                if new_key in content:
                    uid = local_uuid()
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = b[l]
        elif isinstance(other, Matrix):
            new_key = other.name
            if new_key in content:
                uid = local_uuid()
                new_key = "%s_%s" % (other.name, uid)
            content[new_key] = other.array
        else:
            raise TypeError
        c = Book()
        c.load_from_sheets(content)
        return c

    def __iadd__(self, other):
        """Overload += sign

        :return: self
        """
        raise NotImplementedError(MESSAGE_NOT_IMPLEMENTED_01)
