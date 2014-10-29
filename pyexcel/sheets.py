"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import six
import uuid
from .iterators import Matrix, SeriesColumnIterator, Column
from .formatters import ColumnFormatter, RowFormatter, SheetFormatter
from .filters import (RowIndexFilter,
                     ColumnIndexFilter,
                     RowFilter)


def is_string(atype):
    """find out if a type is str or not"""
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


class NamedColumn(Column):
    """Series Sheet would have Named Column instead of Column

    example::

        import pyexcel as pe

        r = pe.SeriesReader("example.csv")
        print(r.column["column 1"])
    
    """
    def __delitem__(self, str_or_aslice):
        if is_string(type(str_or_aslice)):
            self.ref.delete_named_column_at(str_or_aslice)
        else:
            Column.__delitem__(self, str_or_aslice)

    def __setitem__(self, str_or_aslice, c):
        if is_string(type(str_or_aslice)):
            self.ref.set_named_column_at(str_or_aslice, c)
        else:
            Column.__setitem__(self, str_or_aslice)

    def __getitem__(self, str_or_aslice):
        if is_string(type(str_or_aslice)):
            return self.ref.named_column_at(str_or_aslice)
        else:
            return Column.__getitem__(self, str_or_aslice)


class PlainSheet(Matrix):
    """
    A represetation of Matrix that accept custom formatters
    """
    def __init__(self, array):
        """Constructor"""
        Matrix.__init__(self, array)
        self._formatters = []

    def format(self, aformatter):
        """Shorthand for apply_formatter"""
        self.apply_formatter(aformatter)

    def apply_formatter(self, aformatter):
        """Apply the formatter immediately. No return ticket
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
        """
        self._formatters.append(aformatter)

    def remove_formatter(self, aformatter):
        """Remove a formatter

        :param Formatter aformatter: a custom formatter
        """
        self._formatters.remove(aformatter)

    def clear_formatters(self):
        """Clear all formatters"""
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
            raise TypeError
        c = Book()
        c.load_from_sheets(content)
        return c

    def __iadd__(self, other):
        """Overload += sign

        :return: self
        """
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
                raise TypeError
        else:
            raise TypeError
        return self


class MultipleFilterableSheet(PlainSheet):
    """
    A represetation of Matrix that can be filtered
    by as many filters as it is applied
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
        """Apply a filter

        :param Filter afilter: a custom filter
        """
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
        """Apply the filter with immediate effect"""
        if isinstance(afilter, ColumnIndexFilter):
            self._apply_column_filters(afilter)
        elif isinstance(afilter, RowIndexFilter):
            self._apply_row_filters(afilter)
        else:
            raise NotImplementedError("IndexFilter is not supported")

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


class Sheet(MultipleFilterableSheet):
    """
    A represetation of Matrix that can be formatted, filtered and
    support dictionary.

    This class is used in collaboration with Book to represent
    multi-sheet book.
    """
    def __init__(self, sheet, name):
        MultipleFilterableSheet.__init__(self, sheet)
        self.column_filters = []
        self.row_filters = []
        self.headers = None
        self.signature_filter = None
        self.name = name
        self.named_column = NamedColumn(self)

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

    def is_series(self):
        return self.signature_filter is not None

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
        """Re-apply filters

        It is called when some data is updated
        """
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
        Returns the first row as headers
        
        :returns: column headers
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
        return column_array

    def set_named_column_at(self, name, column_array):
        """
        Take the first row as column names

        Given name to identify the column index, set the column to
        the given array except the column name.
        """
        if self.signature_filter:
            self._headers()
            index = self.headers.index(name)
            self.set_column_at(index, column_array)
        else:
            headers = self.row_at(0)
            index = headers.index(name)
            self.set_column_at(index, column_array, 1)

    def delete_named_column_at(self, name):
        """
        Take the first row as column names

        Given name to identify the column index, set the column to
        the given array except the column name.
        """
        if self.signature_filter:
            self._headers()
            index = self.headers.index(name)
        else:
            headers = self.row_at(0)
            index = headers.index(name)
        self.delete_columns([index])

    def delete_rows(self, row_indices):
        """delete rows by specified row indices

        delete_rows method is overriden because absolute row index 0
        in SeriesReader is series row. We need to apply the translation
        for row 0
        """
        indices_to_delete = row_indices
        if self.signature_filter is not None:
            new_indices = []
            for row_index in row_indices:
                new_row_index, ignored_column = self.signature_filter.translate(
                    row_index, 0
                )
                new_indices.append(new_row_index)
            indices_to_delete = new_indices
        MultipleFilterableSheet.delete_rows(self, indices_to_delete)

    def apply_formatter(self, aformatter):
        aformatter = self._translate_named_formatter(aformatter)
        PlainSheet.apply_formatter(self, aformatter)

    def _translate_named_formatter(self, aformatter):
        if self.signature_filter is None:
            return aformatter
        series = self.series()
        if isinstance(aformatter, SheetFormatter) is False:
            if isinstance(aformatter.indices, str):
                new_indices = series.index(aformatter.indices)
                aformatter.update_index(new_indices)
            elif (isinstance(aformatter.indices, list) and
                  isinstance(aformatter.indices[0], str)):
                # translate each column name to index
                aformatter.indices = map(lambda astr: series.index(astr),
                                         aformatter.indices)
                aformatter.update_index(new_indices)
        return aformatter

    def add_formatter(self, aformatter):
        """Add a lazy formatter. 

        The formatter takes effect on the fly when a cell value is read
        This is cost effective when you have a big data table
        and you use only a few columns or rows. If you have farily modest
        data table, you can choose apply_formatter() too.

        :param Formatter aformatter: a custom formatter
        """
        aformatter = self._translate_named_formatter(aformatter)
        PlainSheet.add_formatter(self, aformatter)
        
    def __iter__(self):
        """Overload the iterator signature"""
        if self.signature_filter:
            return SeriesColumnIterator(self)
        else:
            return MultipleFilterableSheet.__iter__(self)

    @property
    def column(self):
        return self.named_column

    @column.setter
    def column(self, value):
        # dummy setter to enable self.column += ..
        pass
