"""
    pyexcel.sheets.nominablesheet
    ~~~~~~~~~~~~~~~~~~~

    Building on top of formattablesheet, adding named columns and rows support

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .matrix import Matrix
from .formatters import (
    NamedColumnFormatter,
    NamedRowFormatter)
import pyexcel._compact as compact
from .iterators import (
    ColumnIndexIterator,
    RowIndexIterator,
    NamedRowIterator,
    NamedColumnIterator
)
from ..constants import (
    MESSAGE_NOT_IMPLEMENTED_02,
    MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED,
    DEFAULT_NAME)
from pyexcel.sources import SheetMixin
from .row import NamedRow
from .column import NamedColumn
from . import _shared as utils


def make_names_unique(alist):
    duplicates = {}
    new_names = []
    for item in alist:
        if not compact.is_string(type(item)):
            item = str(item)
        if item in duplicates:
            duplicates[item] = duplicates[item] + 1
            new_names.append("%s-%d" % (item, duplicates[item]))
        else:
            duplicates[item] = 0
            new_names.append(item)
    return new_names


class Sheet(Matrix, SheetMixin):
    """Two dimensional data container for filtering, formatting and iteration

    :class:`Sheet` is a container for a two dimensional array, where individual
    cell can be any Python types. Other than numbers, value of these
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
    def __init__(self, sheet=None, name=DEFAULT_NAME,
                 name_columns_by_row=-1,
                 name_rows_by_column=-1,
                 colnames=None,
                 rownames=None,
                 transpose_before=False,
                 transpose_after=False):
        """Constructor

        :param sheet: two dimensional array
        :param name: this becomes the sheet name.
        :param name_columns_by_row: use a row to name all columns
        :param name_rows_by_column: use a column to name all rows
        :param colnames: use an external list of strings to name the columns
        :param rownames: use an external list of strings to name the rows
        """
        self.init_attributes()
        self.init(
            sheet=sheet,
            name=name,
            name_columns_by_row=name_columns_by_row,
            name_rows_by_column=name_rows_by_column,
            colnames=colnames,
            rownames=rownames,
            transpose_before=transpose_before,
            transpose_after=transpose_after
        )

    def init(self, sheet=None, name=DEFAULT_NAME,
             name_columns_by_row=-1,
             name_rows_by_column=-1,
             colnames=None,
             rownames=None,
             transpose_before=False,
             transpose_after=False):
        # this get rid of phatom data by not specifying sheet
        if sheet is None:
            sheet = []
        Matrix.__init__(self, sheet)
        if transpose_before:
            self.transpose()
        self.name = name
        self._column_names = []
        self._row_names = []
        self.named_row = NamedRow(self)
        self.named_column = NamedColumn(self)
        if name_columns_by_row != -1:
            if colnames:
                raise NotImplementedError(MESSAGE_NOT_IMPLEMENTED_02)
            self.name_columns_by_row(name_columns_by_row)
        else:
            if colnames:
                self._column_names = colnames
        if name_rows_by_column != -1:
            if rownames:
                raise NotImplementedError(MESSAGE_NOT_IMPLEMENTED_02)
            self.name_rows_by_column(name_rows_by_column)
        else:
            if rownames:
                self._row_names = rownames
        if transpose_after:
            self.transpose()

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
        return self._column_names

    @colnames.setter
    def colnames(self, value):
        """Set column names"""
        self._column_names = make_names_unique(value)

    @property
    def rownames(self):
        """Return row names"""
        return self._row_names

    @rownames.setter
    def rownames(self, value):
        """Set row names"""
        self._row_names = make_names_unique(value)

    def named_column_at(self, name):
        """Get a column by its name """
        index = name
        if compact.is_string(type(index)):
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
        if compact.is_string(type(index)):
            index = self.colnames.index(name)
        self.set_column_at(index, column_array)

    def delete_columns(self, column_indices):
        """Delete one or more columns

        :param list column_indices: a list of column indices
        """
        Matrix.delete_columns(self, column_indices)
        if len(self._column_names) > 0:
            new_series = [self._column_names[i]
                          for i in range(0, len(self._column_names))
                          if i not in column_indices]
            self._column_names = new_series

    def delete_rows(self, row_indices):
        """Delete one or more rows

        :param list row_indices: a list of row indices
        """
        Matrix.delete_rows(self, row_indices)
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
            Matrix.delete_columns(self, [index])

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
        if compact.is_string(type(index)):
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
            Matrix.delete_rows(self, [index])

    def apply_formatter(self, aformatter):
        """Apply the formatter immediately.

        :param Formatter aformatter: a custom formatter
        """
        aformatter = self._translate_named_formatter(aformatter)
        Matrix.apply_formatter(self, aformatter)

    def _translate_named_formatter(self, aformatter):
        if isinstance(aformatter, NamedColumnFormatter):
            series = self.colnames
        elif isinstance(aformatter, NamedRowFormatter):
            series = self.rownames
        else:
            series = None
        if series:
            indices = utils.names_to_indices(aformatter.indices,
                                             series)
            aformatter.update_index(indices)
        return aformatter

    def extend_rows(self, rows):
        """Take ordereddict to extend named rows

        :param ordereddist/list rows: a list of rows.
        """
        incoming_data = []
        if isinstance(rows, compact.OrderedDict):
            keys = rows.keys()
            for k in keys:
                self.rownames.append(k)
                incoming_data.append(rows[k])
            Matrix.extend_rows(self, incoming_data)
        elif len(self.rownames) > 0:
            raise TypeError(MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED)
        else:
            Matrix.extend_rows(self, rows)

    def extend_columns_with_rows(self, rows):
        """Put rows on the right most side of the data"""
        if len(self.colnames) > 0:
            headers = rows.pop(self.row_index)
            self._column_names += headers
        Matrix.extend_columns_with_rows(self, rows)

    def extend_columns(self, columns):
        """Take ordereddict to extend named columns

        :param ordereddist/list columns: a list of columns
        """
        incoming_data = []
        if isinstance(columns, compact.OrderedDict):
            keys = columns.keys()
            for k in keys:
                self.colnames.append(k)
                incoming_data.append(columns[k])
            Matrix.extend_columns(self, incoming_data)
        elif len(self.colnames) > 0:
            raise TypeError(MESSAGE_DATA_ERROR_ORDEREDDICT_IS_EXPECTED)
        else:
            Matrix.extend_columns(self, columns)

    def __iter__(self):
        if len(self._column_names) > 0:
            return ColumnIndexIterator(self)
        elif len(self._row_names) > 0:
            return RowIndexIterator(self)
        else:
            return Matrix.__iter__(self)

    def to_array(self):
        """Returns an array after filtering"""
        from ..utils import to_array
        ret = []
        ret += to_array(self.rows())
        if len(self.rownames) > 0:
            ret = map(lambda value: [value[0]] + value[1],
                      zip(self.rownames, ret))
            if not compact.PY2:
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

    def __setitem__(self, aset, c):
        if isinstance(aset, tuple):
            if isinstance(aset[0], str):
                row = self.rownames.index(aset[0])
            else:
                row = aset[0]

            if isinstance(aset[1], str):
                column = self.colnames.index(aset[1])
            else:
                column = aset[1]
            self.cell_value(row, column, c)
        else:
            Matrix.__setitem__(self, aset, c)

    def named_rows(self):
        return NamedRowIterator(self)

    def named_columns(self):
        return NamedColumnIterator(self)

    class _RepresentedString:
        def __init__(self, text):
            self.text = text

        def __repr__(self):
            return self.text

        def __str__(self):
            return self.text

    def __repr__(self):
        return self.texttable

    def __str__(self):
        return self.texttable

    @property
    def content(self):
        """
        Plain representation without headers
        """
        content = self.get_texttable(write_title=False)
        return self._RepresentedString(content)
