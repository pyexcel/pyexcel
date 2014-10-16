"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import six
import uuid
from .iterators import Matrix, SeriesColumnIterator
from .filters import (RowIndexFilter,
                     ColumnIndexFilter,
                     RowFilter)

def is_string(atype):
    if atype == str:
            return True
    elif six.PY2:
        if atype == unicode:
            return True
    return False

class AS_COLUMNS(object):
    """Indicate direction is by columns"""
    def __init__(self, payload):
        self.payload = payload


class PlainSheet(Matrix):
    """
    xls sheet

    Currently only support first sheet in the file
    """
    def __init__(self, array):
        Matrix.__init__(self, array)
        self._formatters = []

    def add_formatter(self, aformatter):
        self._formatters.append(aformatter)

    def remove_formatter(self, aformatter):
        self._formatters.remove(aformatter)

    def clear_formatters(self):
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
            value_type = type(value)
            if len(self._formatters) > 0:
                previous_type = value_type
                for f in self._formatters:
                    if f.is_my_business(row, column, value):
                        value = f.do_format(value, previous_type)
                        previous_type = f.desired_format
            else:
                if is_string(value_type):
                    try:
                        value = float(value)
                    except ValueError:
                        pass
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
        from .readers import Book
        from .utils import to_dict
        content = {}
        content[self.name] = self.array
        if isinstance(other, Book):
            b = to_dict(other)
            for l in b.keys():
                new_key = l
                if len(b.keys()) == 1:
                    new_key = other.filename
                if new_key in content:
                    uid = uuid.uuid4().hex
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = b[l]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = uuid.uuid4().hex
                new_key = "%s_%s" % (other.name, uid)
            content[new_key] = other.array
        else:
            raise ValueError
        c = Book()
        c.load_from_sheets(content)
        return c

    def __iadd__(self, other):
        if isinstance(other, list):
            self.extend_rows(other)
        elif isinstance(other, Sheet):
            self.extend_rows(other.array)
        elif isinstance(other, AS_COLUMNS):
            new_other = other.payload
            if isinstance(new_other, list):
                self.extend_columns(new_other)
            elif isinstance(new_other, Sheet):
                self.extend_columns(new_other.array)
            else:
                raise ValueError
        else:
            raise ValueError
        return self


class MultipleFilterableSheet(PlainSheet):
    """
    Sheet that can be applied one filter
    """
    def __init__(self, sheet):
        PlainSheet.__init__(self, sheet)
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
        """Apply a filter"""
        afilter.validate_filter(self)
        self._filters.append(afilter)
        return self

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
        """This is short hand for add_filter"""
        self.add_filter(afilter)

    def validate_filters(self):
        local_filters = self._filters
        self._filters = []
        for filter in local_filters:
            filter.validate_filter(self)
            self._filters.append(filter)

    def extend_rows(self, rows):
        """expected the rows to be off the same length

        too expensive to do so
        """
        Matrix.extend_rows(self, rows)
        self.validate_filters()

    def delete_rows(self, row_indices):
        """delete rows

        too expensive to do so
        """
        Matrix.delete_rows(self, row_indices)
        self.validate_filters()

    def extend_columns(self, columns):
        """expected the rows to be off the same length

        too expensive to do so
        """
        Matrix.extend_columns(self, columns)
        self.validate_filters()

    def delete_columns(self, column_indices):
        """delete rows

        too expensive to do so
        """
        Matrix.delete_columns(self, column_indices)
        self.validate_filters()


class Sheet(MultipleFilterableSheet):
    def __init__(self, sheet, name):
        MultipleFilterableSheet.__init__(self, sheet)
        self.column_filters = []
        self.row_filters = []
        self.headers = None
        self.signature_filter = None
        self.name = name

    def become_series(self):
        """
        Evolve this sheet to a SeriesReader
        """
        self.signature_filter = RowFilter([0])
        self.validate_filters()
        return self

    def become_sheet(self):
        """
        Evolve back to plain sheet reader
        """
        self.signature_filter = None
        self.validate_filters()
        return self

    def add_filter(self, afilter):
        """
        Apply a filter
        """
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.append(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.append(afilter)
        self.validate_filters()

    def clear_filters(self):
        """
        Clear all filters
        """
        self.column_filters = []
        self.row_filters = []
        self.validate_filters()

    def remove_filter(self, afilter):
        """
        Remove a named custom filter
        """
        if isinstance(afilter, ColumnIndexFilter):
            self.column_filters.remove(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self.row_filters.remove(afilter)
        self.validate_filters()

    def validate_filters(self):
        if self.signature_filter:
            local_filters = (self.column_filters +
                             [self.signature_filter] +
                             self.row_filters)
        else:
            local_filters = self.column_filters + self.row_filters
        self._filters = []
        for filter in local_filters:
            filter.validate_filter(self)
            self._filters.append(filter)

    def _headers(self):
        self.headers = []
        for i in self.column_range():
            new_row = 0
            new_column = i
            number_of_column_filters = len(self.column_filters)
            for x in range(number_of_column_filters-1, -1, -1):
                new_row, new_column = self.column_filters[x].translate(
                    new_row,
                    new_column)
            self.headers.append(self._cell_value(0, new_column))

    def series(self):
        """
        Return column headers
        """
        if self.signature_filter:
            self._headers()
            return self.headers
        else:
            return []

    def named_column_at(self, name):
        """Get a column by its name """
        if self.signature_filter:
            self._headers()
            index = self.headers.index(name)
            column_array = self.column_at(index)
        else:
            headers = self.row_at(0)
            index = headers.index(name)
            column_array = self.column_at(index)[1:]
        return {name: column_array}

    def set_named_column_at(self, name, column_array):
        if self.signature_filter:
            self._headers()
            index = self.headers.index(name)
            self.set_column_at(index, column_array)
        else:
            headers = self.row_at(0)
            index = headers.index(name)
            self.set_column_at(index, column_array, 1)


    def __iter__(self):
        if self.signature_filter:
            return SeriesColumnIterator(self)
        else:
            return MultipleFilterableSheet.__iter__(self)
