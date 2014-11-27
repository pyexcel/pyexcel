"""
    pyexcel.sheets.filterablesheet
    ~~~~~~~~~~~~~~~~~~~

    Building on top of formattablesheet, adding filtering feature

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import copy
from .matrix import Matrix
from .formattablesheet import FormattableSheet
from ..filters import ColumnIndexFilter, RowIndexFilter, RegionFilter


class FilterableSheet(FormattableSheet):
    """
    A represetation of Matrix that can be filtered
    by as many filters as it is applied
    """
    def __init__(self, sheet):
        FormattableSheet.__init__(self, sheet)
        self._filters = []

    def _number_of_rows(self):
        return len(self.array)

    def _number_of_columns(self):
        if self._number_of_rows() > 0:
            return len(self.array[0])
        else:
            return 0

    def number_of_rows(self):
        """
        Number of rows in the data sheet
        """
        number_of_rows = self._number_of_rows()
        if len(self._filters) != 0:
            new_rows = number_of_rows
            for f in self._filters:
                new_rows = new_rows - f.rows()
            return new_rows
        else:
            return number_of_rows

    def number_of_columns(self):
        """
        Number of columns in the data sheet
        """
        number_of_columns = self._number_of_columns()
        if len(self._filters) != 0:
            new_cols = number_of_columns
            for f in self._filters:
                new_cols = new_cols - f.columns()
            return new_cols
        else:
            return number_of_columns

    def cell_value(self, row, column, new_value=None):
        """
        Random access to the data cells
        """
        if row in self.row_range() and column in self.column_range():
            if len(self._filters) != 0:
                new_row = row
                new_column = column
                number_of_filters = len(self._filters)
                for i in range(number_of_filters-1, -1, -1):
                    new_row, new_column = self._filters[i].translate(
                        new_row,
                        new_column)
                return self._cell_value(new_row, new_column, new_value)
            else:
                return self._cell_value(row, column, new_value)
        else:
            return None

    def add_filter(self, afilter):
        """Apply a filter

        :param Filter afilter: a custom filter
        """
        afilter.validate_filter(self)
        self._filters.append(afilter)

    def remove_filter(self, afilter):
        """Remove a named filter

        have to remove all filters in order to re-validate the
        rest of the filters
        """
        self._filters.remove(afilter)
        local_filters = self._filters
        self._filters = []
        for f in local_filters:
            f.validate_filter(self)
            self._filters.append(f)

    def clear_filters(self):
        """Clears all filters"""
        self._filters = []

    def filter(self, afilter):
        """Apply the filter with immediate effect"""
        if isinstance(afilter, ColumnIndexFilter):
            self._apply_column_filters(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self._apply_row_filters(afilter)
        else:
            afilter.validate_filter(self)
            decending_list = sorted(afilter.row_indices, reverse=True)
            for i in decending_list:
                del self.row[i]
            decending_list = sorted(afilter.column_indices, reverse=True)
            for i in decending_list:
                del self.column[i]

    def _apply_row_filters(self, afilter):
        afilter.validate_filter(self)
        decending_list = sorted(afilter.indices, reverse=True)
        for i in decending_list:
            del self.row[i]

    def _apply_column_filters(self, afilter):
        """Private method to apply column filter"""
        afilter.validate_filter(self)
        decending_list = sorted(afilter.indices, reverse=True)
        for i in decending_list:
            del self.column[i]

    def validate_filters(self):
        """Re-apply filters

        It is called when some data is updated
        """
        local_filters = self._filters
        self._filters = []
        for filter in local_filters:
            filter.validate_filter(self)
            self._filters.append(filter)

    def freeze_filters(self):
        """Apply all filters and delete them"""
        local_filters = self._filters
        self._filters = []
        for f in local_filters:
            self.filter(f)

    def _lift_filters(func):
        """
        disable filters, do something and enable fitlers
        """
        def wrapper(self, *args):
            local_filters = []
            # if filter exist
            if len(self._filters) > 0:
                local_filters = self._filters
                self._filters = []
            func(self, *args)
            #if filter exist
            if len(local_filters) > 0:
                self._filters = local_filters
                self.validate_filters()
        return wrapper

    @_lift_filters
    def extend_rows(self, rows):
        """expected the rows to be off the same length

        :param list rows: a list of arrays
        """
        Matrix.extend_rows(self, rows)

    @_lift_filters
    def delete_rows(self, row_indices):
        """delete rows

        :param list row_indices: a list of row indices to be removed
        """
        Matrix.delete_rows(self, row_indices)

    @_lift_filters
    def extend_columns(self, columns):
        """expected the rows to be of the same length

        :param list columns: a list of arrays
        """
        Matrix.extend_columns(self, columns)

    @_lift_filters
    def delete_columns(self, column_indices):
        """delete rows

        :param list row_indices: a list of column indices to be removed
        """
        Matrix.delete_columns(self, column_indices)

    def region(self, topleft_corner, bottomright_corner):
        """Get a rectangle shaped data out

        :param slice topleft_corner: the top left corner of the rectangle
        :param slice bottomright_corner: the bottom right corner of the rectangle

        example::

            >>> import pyexcel as pe
            >>> data = [
            ...     # 0 1  2  3  4 5   6
            ...     [1, 2, 3, 4, 5, 6, 7], #  0
            ...     [21, 22, 23, 24, 25, 26, 27],
            ...     [31, 32, 33, 34, 35, 36, 37],
            ...     [41, 42, 43, 44, 45, 46, 47],
            ...     [51, 52, 53, 54, 55, 56, 57]  # 4
            ... ]
            >>> s = pe.Sheet(data)
            >>> data = s.cut([1, 1], [4, 5])
            >>> s2 = pe.Sheet(data) #  let's present the result
            >>> s2
            Sheet Name: pyexcel
            +----+----+----+----+
            | 22 | 23 | 24 | 25 |
            +----+----+----+----+
            | 32 | 33 | 34 | 35 |
            +----+----+----+----+
            | 42 | 43 | 44 | 45 |
            +----+----+----+----+
        """
        row_slice = slice(topleft_corner[0], bottomright_corner[0], 1)
        column_slice = slice(topleft_corner[1], bottomright_corner[1], 1)
        f = RegionFilter(row_slice, column_slice)
        self.add_filter(f)
        ret_data = copy.deepcopy(self.to_array())
        self.remove_filter(f)
        return ret_data

    def cut(self, topleft_corner, bottomright_corner):
        """Get a rectangle shaped data out and clear them in position

        :param slice topleft_corner: the top left corner of the rectangle
        :param slice bottomright_corner: the bottom right corner of the rectangle

        example::

            >>> import pyexcel as pe
            >>> data = [
            ...     # 0 1  2  3  4 5   6
            ...     [1, 2, 3, 4, 5, 6, 7], #  0
            ...     [21, 22, 23, 24, 25, 26, 27],
            ...     [31, 32, 33, 34, 35, 36, 37],
            ...     [41, 42, 43, 44, 45, 46, 47],
            ...     [51, 52, 53, 54, 55, 56, 57]  # 4
            ... ]
            >>> s = pe.Sheet(data)
            >>> s
            Sheet Name: pyexcel
            +----+----+----+----+----+----+----+
            | 1  | 2  | 3  | 4  | 5  | 6  | 7  |
            +----+----+----+----+----+----+----+
            | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
            +----+----+----+----+----+----+----+
            | 31 | 32 | 33 | 34 | 35 | 36 | 37 |
            +----+----+----+----+----+----+----+
            | 41 | 42 | 43 | 44 | 45 | 46 | 47 |
            +----+----+----+----+----+----+----+
            | 51 | 52 | 53 | 54 | 55 | 56 | 57 |
            +----+----+----+----+----+----+----+
            >>> # cut  1<= row < 4, 1<= column < 5
            >>> data = s.cut([1, 1], [4, 5])
            >>> s
            Sheet Name: pyexcel
            +----+----+----+----+----+----+----+
            | 1  | 2  | 3  | 4  | 5  | 6  | 7  |
            +----+----+----+----+----+----+----+
            | 21 |    |    |    |    | 26 | 27 |
            +----+----+----+----+----+----+----+
            | 31 |    |    |    |    | 36 | 37 |
            +----+----+----+----+----+----+----+
            | 41 |    |    |    |    | 46 | 47 |
            +----+----+----+----+----+----+----+
            | 51 | 52 | 53 | 54 | 55 | 56 | 57 |
            +----+----+----+----+----+----+----+

        """
        row_slice = slice(topleft_corner[0], bottomright_corner[0], 1)
        column_slice = slice(topleft_corner[1], bottomright_corner[1], 1)
        f = RegionFilter(row_slice, column_slice)
        self.add_filter(f)
        ret_data = copy.deepcopy(self.to_array())
        for r in self.row_range():
            for c in self.column_range():
                self.cell_value(r, c, '')
        self.remove_filter(f)
        return ret_data

    def paste(self, topleft_corner):
        """Paste a rectangle shaped data after a position

        :param slice topleft_corner: the top left corner of the rectangle
        """
        pass
