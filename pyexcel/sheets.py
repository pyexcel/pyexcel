"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import six
import uuid
from .iterators import Matrix, ColumnIndexIterator, RowIndexIterator, Column, Row
from .formatters import ColumnFormatter, RowFormatter, NamedColumnFormatter, NamedRowFormatter
from .filters import (RowIndexFilter,
                      ColumnIndexFilter)
from ._compact import OrderedDict


def is_string(atype):
    """find out if a type is str or not"""
    if atype == str:
            return True
    elif six.PY2:
        if atype == unicode:
            return True
    return False


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
        ...     r = pe.load(file)
        ...     merged.row += r
        >>> merged.save_as("merged.csv")

    Now let's verify what we had::

        >>> r=pe.Reader("merged.csv")
    
    this is added to overcome doctest's inability to handle python 3's unicode::
    
        >>> r.format(pe.formatters.SheetFormatter(str, lambda v: str(v))) 
        >>> print(pe.utils.to_array(r))
        [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['1.1', '2.2', '3.3'], ['4.4', '5.5', '6.6'], ['7.7', '8.8', '9.9']]
    
    .. testcleanup::
        >>> import os
        >>> os.unlink("1.csv")
        >>> os.unlink("2.csv")
        >>> os.unlink("3.csv")
        >>> os.unlink("merged.csv")

    """
    def __delitem__(self, column_name):
        if is_string(type(column_name)):
            self.ref.delete_named_row_at(column_name)
        else:
            Row.__delitem__(self, column_name)

    def __setitem__(self, str_or_aslice, c):
        if is_string(type(str_or_aslice)):
            self.ref.set_named_row_at(str_or_aslice, c)
        else:
            Row.__setitem__(self, str_or_aslice, c)

    def __getitem__(self, str_or_aslice):
        if is_string(type(str_or_aslice)):
            return self.ref.named_row_at(str_or_aslice)
        else:
            return Row.__getitem__(self, str_or_aslice)

    def __iadd__(self, other):
        """Overload += sign

        :param list other: the row header must be the first element.
        :return: self
        """
        if isinstance(other, OrderedDict):
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

    def format(self, row_index=None, format=None, custom_converter=None, format_specs=None, on_demand=False):
        def handle_one_formatter(rows, aformat, aconverter, on_demand):
            formatter = RowFormatter(rows, aformat, aconverter)
            if on_demand:
                self.ref.add_formatter(formatter)
            else:
                self.ref.apply_formatter(formatter)
        if row_index:
            handle_one_formatter(row_index, format, custom_converter, on_demand)
        elif format_specs:
            for spec in format_specs:
                if len(spec) == 3:
                    handle_one_formatter(spec[0], spec[1], spec[2], on_demand)
                else:
                    handle_one_formatter(spec[0], spec[1], None, on_demand)
                
        
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
            Column.__setitem__(self, str_or_aslice, c)

    def __getitem__(self, str_or_aslice):
        if is_string(type(str_or_aslice)):
            return self.ref.named_column_at(str_or_aslice)
        else:
            return Column.__getitem__(self, str_or_aslice)

    def __iadd__(self, other):
        """Overload += sign

        :param list other: the column header must be the first element.
        :return: self
        """
        if isinstance(other, OrderedDict):
            self.ref.extend_columns(other)
        else:
            Column.__iadd__(self, other)
        return self

    def __add__(self, other):
        """Overload += sign

        :return: self
        """
        self.__iadd__(other)
        return self.ref

    def format(self, column_index=None, format=None, custom_converter=None, format_specs=None, on_demand=False):
        def handle_one_formatter(columns, aformat, aconverter, on_demand):
            formatter = ColumnFormatter(columns, aformat, aconverter)
            if on_demand:
                self.ref.add_formatter(formatter)
            else:
                self.ref.apply_formatter(formatter)
        if column_index:
            handle_one_formatter(column_index, format, custom_converter, on_demand)
        elif format_specs:
            for spec in format_specs:
                if len(spec) == 3:
                    handle_one_formatter(spec[0], spec[1], spec[2], on_demand)
                else:
                    handle_one_formatter(spec[0], spec[1], None, on_demand)


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
        raise NotImplementedError("Depreciated!Not supported any more. Please .row or .column to extendsheet")


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


class IndexSheet(MultipleFilterableSheet):
    """Allow dictionary group of the content
    """
    def __init__(self, sheet=None, name="pyexcel", name_columns_by_row=-1, name_rows_by_column=-1):
        # this get rid of phatom data by not specifying sheet
        if sheet is None:
            sheet = []
        MultipleFilterableSheet.__init__(self, sheet)
        self.name = name
        self._column_names = []
        self._row_names = []
        self.named_row = NamedRow(self)
        self.named_column = NamedColumn(self)
        if name_columns_by_row != -1:
            self.name_columns_by_row(name_columns_by_row)
        if name_rows_by_column != -1:
            self.name_rows_by_column(name_rows_by_column)

    @property
    def row(self):
        """Row representation.

        examples::

            >>> import pyexcel as pe
            >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            >>> sheet = Sheet(data)
            >>> sheet.row[1]
            [4, 5, 6]
            >>> sheet.row[0:3]
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            >>> sheet.row += [11, 12, 13]
            >>> sheet.row[3]
            [11, 12, 13]
            >>> sheet.row[0:4] = [0, 0, 0] # set all to zero
            >>> sheet.row[3]
            [0, 0, 0]
            >>> sheet.row[0] = ['a', 'b', 'c'] # set one row
            >>> sheet.row[0]
            ['a', 'b', 'c']
            >>> del sheet.row[0] # delete first row
            >>> sheet.row[0] # now, second row becomes the first
            [0, 0, 0]
            >>> del sheet.row[0:]
            >>> sheet.row[0]  # nothing left
            Traceback (most recent call last):
                ...
            IndexError
        """
        return self.named_row

    @row.setter
    def row(self, value):
        # dummy setter to enable self.row += ..
        pass

    @property
    def column(self):
        """Column representation, giving random access to columns"""
        return self.named_column

    @column.setter
    def column(self, value):
        # dummy setter to enable self.column += ..
        pass

    def index_by_row(self, row_index):
        self.name_columns_by_row(row_index)

    def name_columns_by_row(self, row_index):
        """Use the elements of a specified row to represent individual columns"""
        self.row_index = row_index
        self._column_names = self.row_at(row_index)
        del self.row[row_index]

    def index_by_column(self, column_index):
        self.name_rows_by_column(column_index)
        
    def name_rows_by_column(self, column_index):
        """Use the elements of a specified column to represent individual rows"""
        self.column_index = column_index
        self._row_names = self.column_at(column_index)
        del self.column[column_index]

    @property
    def colnames(self):
        """Row names"""
        if len(self._filters) != 0:
            column_filters = [ f for f in self._filters if isinstance(f, ColumnIndexFilter)]
            if len(column_filters) != 0:
                indices = range(0, len(self._column_names))
                for f in column_filters:
                    indices = [i for i in indices if i not in f.indices]
                return [self._column_names[i] for i in indices]
            else:
                return self._column_names
        else:
            return self._column_names

    @property
    def rownames(self):
        """Column names"""
        if len(self._filters) != 0:
            row_filters = [ f for f in self._filters if isinstance(f, RowIndexFilter)]
            if len(row_filters) != 0:
                indices = range(0, len(self._row_names))
                for f in row_filters:
                    indices = [i for i in indices if i not in f.indices]
                return [self._row_names[i] for i in indices]
            else:
                return self._row_names
        else:
            return self._row_names

    def named_column_at(self, name):
        """Get a column by its name """
        index = name
        if is_string(type(index)):
            index = self.colnames.index(name)
        column_array = self.column_at(index)
        return column_array

    def set_named_column_at(self, name, column_array):
        """
        Take the first row as column names

        Given name to identify the column index, set the column to
        the given array except the column name.
        """
        index = name
        if is_string(type(index)):
            index = self.colnames.index(name)
        self.set_column_at(index, column_array)

    def delete_columns(self, column_indices):
        """Delete one or more columns

        :param list column_indices: a list of column indices
        """
        MultipleFilterableSheet.delete_columns(self, column_indices)
        if len(self._column_names) > 0:
            new_series = [ self._column_names[i] for i in range(0, len(self._column_names)) if i not in column_indices ]
            self._column_names = new_series

    def delete_rows(self, row_indices):
        """Delete one or more rows

        :param list row_indices: a list of row indices
        """
        MultipleFilterableSheet.delete_rows(self, row_indices)
        if len(self._row_names) > 0:
            new_series = [ self._row_names[i] for i in range(0, len(self._row_names)) if i not in row_indices ]
            self._row_names = new_series

    def delete_named_column_at(self, name):
        """Works only after you named columns by a row

        Given name to identify the column index, set the column to
        the given array except the column name.
        :param str name: a column name
        """
        if isinstance(name, int):
            if len(self.rownames) > 0:
                self.rownames.pop(name)
            self.delete_columns([name])
        else:
            index = self.rownames.index(name)
            self.rownames.pop(index)
            self.delete_columns([index])

    def named_row_at(self, name):
        """Get a row by its name """
        index = name
        if is_string(type(index)):
            index = self.rownames.index(name)
        row_array = self.row_at(index)
        return row_array

    def set_named_row_at(self, name, row_array):
        """
        Take the first column as row names

        Given name to identify the row index, set the row to
        the given array except the row name.
        """
        index = name
        if is_string(type(index)):
            index = self.rownames.index(name)
        self.set_row_at(index, row_array)

    def delete_named_row_at(self, name):
        """Take the first column as row names

        Given name to identify the row index, set the row to
        the given array except the row name.
        """
        if isinstance(name, int):
            if len(self.rownames) > 0:
                self.rownames.pop(name)
            self.delete_rows([name])
        else:
            index = self.rownames.index(name)
            self.rownames.pop(index)
            self.delete_rows([index])

    def apply_formatter(self, aformatter):
        """Apply the formatter immediately.
        
        :param Formatter aformatter: a custom formatter
        """
        aformatter = self._translate_named_formatter(aformatter)
        PlainSheet.apply_formatter(self, aformatter)

    def _translate_named_formatter(self, aformatter):
        if isinstance(aformatter, NamedColumnFormatter):
            series = self.colnames
        elif isinstance(aformatter, NamedRowFormatter):
            series = self.rownames
        else:
            series = None
        if series:
            if isinstance(aformatter.indices, str):
                new_indices = series.index(aformatter.indices)
                aformatter.update_index(new_indices)
            elif (isinstance(aformatter.indices, list) and
                  isinstance(aformatter.indices[0], str)):
                # translate each row name to index
                new_indices = [ series.index(astr) for astr in aformatter.indices]
                aformatter.update_index(new_indices)
        return aformatter

    def add_formatter(self, aformatter):
        """Add a lazy formatter.

        The formatter takes effect on the fly when a cell value is read
        This is cost effective when you have a big data table
        and you use only a few rows or columns. If you have farily modest
        data table, you can choose apply_formatter() too.

        :param Formatter aformatter: a custom formatter
        """
        aformatter = self._translate_named_formatter(aformatter)
        PlainSheet.add_formatter(self, aformatter)

    def extend_rows(self, rows):
        """Take ordereddict to extend named rows

        :param ordereddist/list rows: a list of rows.
        """
        incoming_data = []
        if isinstance(rows, OrderedDict):
            keys = rows.keys()
            for k in keys:
                self.rownames.append(k)
                incoming_data.append(rows[k])
            MultipleFilterableSheet.extend_rows(self, incoming_data)
        elif len(self.rownames) > 0:
            raise TypeError("Please give a ordered list")
        else:
            MultipleFilterableSheet.extend_rows(self, rows)

    def extend_columns(self, columns):
        """Take ordereddict to extend named columns

        :param ordereddist/list columns: a list of columns
        """
        incoming_data = []
        if isinstance(columns, OrderedDict):
            keys = columns.keys()
            for k in keys:
                self.colnames.append(k)
                incoming_data.append(columns[k])
            MultipleFilterableSheet.extend_columns(self, incoming_data)
        elif len(self.colnames) > 0:
            raise TypeError("Please give a ordered list")
        else:
            MultipleFilterableSheet.extend_columns(self, columns)

    def __iter__(self):
        if len(self._column_names) > 0:
            return ColumnIndexIterator(self)
        elif len(self._row_names) > 0:
            return RowIndexIterator(self)
        else:
            return MultipleFilterableSheet.__iter__(self)

    def to_records(self):
        """Returns the content as an array of dictionaries

        """
        from .utils import to_records
        return to_records(self)

    def to_dict(self, row=False):
        """Returns a dictionary"""
        from .utils import to_dict
        if row:
            return to_dict(RowIndexIterator(self))
        else:
            return to_dict(ColumnIndexIterator(self))

    def __getitem__(self, aset):
        if isinstance(aset, tuple):
            if isinstance(aset[0], str):
                row = self.rownames.index(aset[0])
            else:
                row = aset[0]

            if isinstance(aset[1], str):
                column = self.colnames.index(aset[1])
            else:
                column = aset[1]
            return self.cell_value(row, column)
        else:
            return Matrix.__getitem__(self, aset)

class Sheet(IndexSheet):
    """Two dimensional data container for filtering, formatting and custom iteration

    :class:`Sheet` is a container for a two dimensional array, where individual
    cell can be any Python types. Other than numbers, value of thsee
    types: string, date, time and boolean can be mixed in the array. This
    differs from Numpy's matrix where each cell are of the same number type.

    In order to prepare two dimensional data for your computation, formatting
    functions help convert array cells to required types. Formatting can be
    applied not only to the whole sheet but also to selected rows or columns.
    Custom conversion function can be passed to these formatting functions. For
    example, to remove extra spaces surrounding the content of a cell, a custom
    function is required.

    Filtering functions are used to reduce the information contained in the
    array. 
    """
    def become_series(self, series=0):
        return IndexSheet(self.array, self.name, series)

    def is_series(self):
        """Keep backward compactibility"""
        return False

    def save_as(self, filename):
        """Save the content to a named file"""
        from .writers import Writer
        w = Writer(filename)
        w.write_reader(self)
        w.close()

    def save_to_memory(self, file_type, stream):
        """Save the content to memory

        :param str file_type: any value of 'csv', 'xls', 'xlsm', 'xlsx' and 'ods'
        :param iostream stream: the memory stream to be written to 
        """
        self.save_as((file_type, stream))