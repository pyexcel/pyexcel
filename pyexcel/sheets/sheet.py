"""
    pyexcel.sheets.Sheet
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel.sheets.nominablesheet import NominableSheet
import pyexcel.constants as constants
from pyexcel.sources import SheetMixin


class Sheet(NominableSheet, SheetMixin):
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
    def __init__(self, sheet=None, name=constants.DEFAULT_NAME,
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
        NominableSheet.__init__(
            self,
            sheet=sheet,
            name=name,
            name_columns_by_row=name_columns_by_row,
            name_rows_by_column=name_rows_by_column,
            colnames=colnames,
            rownames=rownames,
            transpose_before=transpose_before,
            transpose_after=transpose_after
        )

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
