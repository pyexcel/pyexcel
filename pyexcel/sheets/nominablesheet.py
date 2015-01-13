"""
    pyexcel.sheets.nominablesheet
    ~~~~~~~~~~~~~~~~~~~

    Building on top of filterablesheet, adding named columns and rows support

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .matrix import Row, Column, Matrix
from .formattablesheet import FormattableSheet
from .filterablesheet import FilterableSheet
from ..formatters import (
    ColumnFormatter,
    RowFormatter,
    NamedColumnFormatter,
    NamedRowFormatter)
from .._compact import is_string, OrderedDict, PY2, is_array_type
from ..filters import ColumnIndexFilter, RowIndexFilter
from ..iterators import ColumnIndexIterator, RowIndexIterator
from ..presentation import outsource
from ..texttable import Texttable


def names_to_indices(names, series):
    if isinstance(names, str):
        indices = series.index(names)
    elif (isinstance(names, list) and
          isinstance(names[0], str)):
        # translate each row name to index
        indices = [series.index(astr) for astr in names]
    else:
        return names
    return indices


def make_names_unique(alist):
    duplicates = {}
    new_names = []
    for item in alist:
        if item in duplicates:
            duplicates[item] = duplicates[item] + 1
            new_names.append("%s-%d" % (item, duplicates[item]))
        else:
            duplicates[item] = 0
            new_names.append(str(item))
    return new_names


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

    this is added to overcome doctest's inability to handle
    python 3's unicode::

        >>> r.format(str, lambda v: str(v))
        >>> print(pe.utils.to_array(r))
        [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['1.1', '2.2', '3.3'], ['4.4', '5.5', '6.6'], ['7.7', '8.8', '9.9']]

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
            Sheet Name: pyexcel
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
            Sheet Name: pyexcel
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
            Sheet Name: pyexcel
            +---+---+
            | a | 1 |
            +---+---+
            | b | 1 |
            +---+---+

        """
        if is_array_type(names, str):
            indices = names_to_indices(names, self.ref.rownames)
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
            Sheet Name: pyexcel
            +---+---+
            | c | 1 |
            +---+---+

        """
        if is_string(type(column_name)):
            self.ref.delete_named_row_at(column_name)
        elif isinstance(column_name, tuple) and is_array_type(list(column_name), str):
            indices = names_to_indices(list(column_name), self.ref.rownames)
            Row.__delitem__(self, indices)
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

    def format(self,
               row_index=None, format=None, custom_converter=None,
               format_specs=None, on_demand=False):
        """Format a row
        """
        def handle_one_formatter(rows, aformat, aconverter, on_demand):
            new_indices = rows
            if len(self.ref.rownames) > 0:
                new_indices = names_to_indices(rows, self.ref.rownames)
            formatter = RowFormatter(new_indices, aformat, aconverter)
            if on_demand:
                self.ref.add_formatter(formatter)
            else:
                self.ref.apply_formatter(formatter)
        if row_index is not None:
            handle_one_formatter(row_index, format,
                                 custom_converter, on_demand)
        elif format_specs:
            for spec in format_specs:
                if len(spec) == 3:
                    handle_one_formatter(spec[0], spec[1],
                                         spec[2], on_demand)
                else:
                    handle_one_formatter(spec[0], spec[1],
                                         None, on_demand)


class NamedColumn(Column):
    """Series Sheet would have Named Column instead of Column

    example::

        import pyexcel as pe

        r = pe.SeriesReader("example.csv")
        print(r.column["column 1"])

    """
    def select(self, names):
        """Delete columns other than specified
        
        Examples:
     
            >>> import pyexcel as pe
            >>> data = [[1,2,3,4,5,6,7,9]]
            >>> sheet = pe.Sheet(data)
            >>> sheet
            Sheet Name: pyexcel
            +---+---+---+---+---+---+---+---+
            | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 9 |
            +---+---+---+---+---+---+---+---+
            >>> sheet.column.select([1,2,3,5])
            >>> sheet
            Sheet Name: pyexcel
            +---+---+---+---+
            | 2 | 3 | 4 | 6 |
            +---+---+---+---+
            >>> data = [
            ...     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            ...     [1,2,3,4,5,6,7,9],
            ... ]
            >>> sheet = pe.Sheet(data, name_columns_by_row=0)
            >>> sheet
            Sheet Name: pyexcel
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
            Sheet Name: pyexcel
            +---+---+---+---+
            | a | c | e | h |
            +===+===+===+===+
            | 1 | 3 | 5 | 9 |
            +---+---+---+---+

        """
        if is_array_type(names, str):
            indices = names_to_indices(names, self.ref.colnames)
            Column.select(self, indices)
        else:
            Column.select(self, names)

    def __delitem__(self, str_or_aslice):
        """

        Example::

            >>> import pyexcel as pe
            >>> data = [
            ...     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            ...     [1,2,3,4,5,6,7,9],
            ... ]
            >>> sheet = pe.Sheet(data, name_columns_by_row=0)
            >>> sheet
            Sheet Name: pyexcel
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
            Sheet Name: pyexcel
            +---+---+---+---+
            | b | d | f | g |
            +===+===+===+===+
            | 2 | 4 | 6 | 7 |
            +---+---+---+---+

        """
        if is_string(type(str_or_aslice)):
            self.ref.delete_named_column_at(str_or_aslice)
        elif isinstance(str_or_aslice, tuple) and is_array_type(list(str_or_aslice), str):
            indices = names_to_indices(list(str_or_aslice), self.ref.colnames)
            Column.__delitem__(self, indices)
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

    def format(self,
               column_index=None, format=None, custom_converter=None,
               format_specs=None, on_demand=False):
        """Format a column
        """
        def handle_one_formatter(columns, aformat, aconverter, on_demand):
            new_indices = columns
            if len(self.ref.colnames) > 0:
                new_indices = names_to_indices(columns, self.ref.colnames)
            formatter = ColumnFormatter(new_indices, aformat, aconverter)
            if on_demand:
                self.ref.add_formatter(formatter)
            else:
                self.ref.apply_formatter(formatter)
        if column_index is not None:
            handle_one_formatter(column_index, format,
                                 custom_converter, on_demand)
        elif format_specs:
            for spec in format_specs:
                if len(spec) == 3:
                    handle_one_formatter(spec[0], spec[1],
                                         spec[2], on_demand)
                else:
                    handle_one_formatter(spec[0], spec[1],
                                         None, on_demand)


class NominableSheet(FilterableSheet):
    """Allow dictionary group of the content
    """
    def __init__(self, sheet=None, name="pyexcel",
                 name_columns_by_row=-1,
                 name_rows_by_column=-1,
                 colnames=None,
                 rownames=None):
        """Constructor

        :param sheet: two dimensional array
        :param name: this becomes the sheet name.
        :param name_columns_by_row: use a row to name all columns
        :param name_rows_by_column: use a column to name all rows
        :param colnames: use an external list of strings to name the columns
        :param rownames: use an external list of strings to name the rows
        """
        # this get rid of phatom data by not specifying sheet
        if sheet is None:
            sheet = []
        FilterableSheet.__init__(self, sheet)
        self.name = name
        self._column_names = []
        self._row_names = []
        self.named_row = NamedRow(self)
        self.named_column = NamedColumn(self)
        if name_columns_by_row != -1:
            if colnames:
                raise NotImplementedError(
                    "Confused! What do you want to put as column names")
            self.name_columns_by_row(name_columns_by_row)
        else:
            if colnames:
                self._column_names = colnames
        if name_rows_by_column != -1:
            if rownames:
                raise NotImplementedError(
                    "Confused! What do you want to put as column names")
            self.name_rows_by_column(name_rows_by_column)
        else:
            if rownames:
                self._row_names = rownames

    @property
    def row(self):
        """Row representation. see :class:`NamedRow`

        examples::

            >>> import pyexcel as pe
            >>> data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            >>> sheet = pe.Sheet(data)
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
        """Column representation. see :class:`NamedColumn`"""
        return self.named_column

    @column.setter
    def column(self, value):
        # dummy setter to enable self.column += ..
        pass

    def name_columns_by_row(self, row_index):
        """Use the elements of a specified row to represent individual columns

        The specified row will be deleted from the data
        :param int row_index: the index of the row that has the column names
        """
        self.row_index = row_index
        self._column_names = make_names_unique(self.row_at(row_index))
        del self.row[row_index]

    def name_rows_by_column(self, column_index):
        """Use the elements of a specified column to represent individual rows

        The specified column will be deleted from the data
        :param int column_index: the index of the column that has the row names
        """
        self.column_index = column_index
        self._row_names = make_names_unique(self.column_at(column_index))
        del self.column[column_index]

    @property
    def colnames(self):
        """Return column names"""
        if len(self._filters) != 0:
            column_filters = [f for f in self._filters
                              if isinstance(f, ColumnIndexFilter)]
            if len(column_filters) != 0:
                indices = range(0, len(self._column_names))
                for f in column_filters:
                    indices = [i for i in indices if i not in f.indices]
                return [self._column_names[i] for i in indices]
            else:
                return self._column_names
        else:
            return self._column_names

    @colnames.setter
    def colnames(self, value):
        """Set column names"""
        self._column_names = make_names_unique(value)

    @property
    def rownames(self):
        """Return row names"""
        if len(self._filters) != 0:
            row_filters = [f for f in self._filters
                           if isinstance(f, RowIndexFilter)]
            if len(row_filters) != 0:
                indices = range(0, len(self._row_names))
                for f in row_filters:
                    indices = [i for i in indices if i not in f.indices]
                return [self._row_names[i] for i in indices]
            else:
                return self._row_names
        else:
            return self._row_names

    @rownames.setter
    def rownames(self, value):
        """Set row names"""
        self._row_names = make_names_unique(value)

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
        FilterableSheet.delete_columns(self, column_indices)
        if len(self._column_names) > 0:
            new_series = [self._column_names[i]
                          for i in range(0, len(self._column_names))
                          if i not in column_indices]
            self._column_names = new_series

    def delete_rows(self, row_indices):
        """Delete one or more rows

        :param list row_indices: a list of row indices
        """
        FilterableSheet.delete_rows(self, row_indices)
        if len(self._row_names) > 0:
            new_series = [self._row_names[i]
                          for i in range(0, len(self._row_names))
                          if i not in row_indices]
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
            index = self.colnames.index(name)
            self.colnames.pop(index)
            FilterableSheet.delete_columns(self, [index])

    def named_row_at(self, name):
        """Get a row by its name """
        index = name
        # if is_string(type(index)):
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
            FilterableSheet.delete_rows(self, [index])

    def apply_formatter(self, aformatter):
        """Apply the formatter immediately.

        :param Formatter aformatter: a custom formatter
        """
        aformatter = self._translate_named_formatter(aformatter)
        FormattableSheet.apply_formatter(self, aformatter)

    def _translate_named_formatter(self, aformatter):
        if isinstance(aformatter, NamedColumnFormatter):
            series = self.colnames
        elif isinstance(aformatter, NamedRowFormatter):
            series = self.rownames
        else:
            series = None
        if series:
            indices = names_to_indices(aformatter.indices, series)
            aformatter.update_index(indices)
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
        FormattableSheet.add_formatter(self, aformatter)

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
            FilterableSheet.extend_rows(self, incoming_data)
        elif len(self.rownames) > 0:
            raise TypeError("Please give a ordered list")
        else:
            FilterableSheet.extend_rows(self, rows)

    def extend_columns_with_rows(self, rows):
        """Put rows on the right most side of the data"""
        if len(self.colnames) > 0:
            headers = rows.pop(self.row_index)
            self._column_names += headers
        FilterableSheet.extend_columns_with_rows(self, rows)

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
            FilterableSheet.extend_columns(self, incoming_data)
        elif len(self.colnames) > 0:
            raise TypeError("Please give a ordered list")
        else:
            FilterableSheet.extend_columns(self, columns)

    def __iter__(self):
        if len(self._column_names) > 0:
            return ColumnIndexIterator(self)
        elif len(self._row_names) > 0:
            return RowIndexIterator(self)
        else:
            return FilterableSheet.__iter__(self)

    def to_array(self):
        """Returns an array after filtering"""
        from ..utils import to_array
        ret = []
        ret += to_array(self.rows())
        if len(self.rownames) > 0:
            ret = map(lambda value: [value[0]] + value[1],
                      zip(self.rownames, ret))
            if not PY2:
                ret = list(ret)
        if len(self.colnames) > 0:
            if len(self.rownames) > 0:
                ret.insert(0, [""] + self.colnames)
            else:
                ret.insert(0, self.colnames)
        return ret

    def to_records(self, custom_headers=None):
        """Returns the content as an array of dictionaries

        """
        from ..utils import to_records
        return to_records(self, custom_headers)

    def to_dict(self, row=False):
        """Returns a dictionary"""
        from ..utils import to_dict
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

    def __border__(self):
        if len(self.colnames) > 0:
            return ['-', '|', '+', '=']
        else:
            return ['-', '|', '+', '-']

    @outsource
    def __str__(self):
        from ..formatters import to_format
        ret = "Sheet Name: %s\n" % self.name
        if len(self.colnames) > 0:
            table = Texttable(max_width=0)
            table.set_chars(self.__border__())
            data = self.to_array()
            new_data = []
            for sub_array in data:
                new_array = []
                for item in sub_array:
                    if item == "":
                        new_array.append(" ")
                    else:
                        new_array.append(to_format(str,item))
                new_data.append(new_array)
            table.add_rows(new_data)
            return ret+table.draw()
        else:
            return ret+FilterableSheet.__str__(self)
