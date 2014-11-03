
"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support styling, charts.

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""

from .readers import Reader, BookReader, Book
from .writers import Writer, BookWriter
from .readers import (SeriesReader,
                      ColumnSeriesReader,
                      PlainReader,
                      FilterableReader)
from .utils import to_dict, to_array, to_records
from .formatters import (ColumnFormatter,
                         RowFormatter,
                         SheetFormatter,
                         NamedColumnFormatter,
                         NamedRowFormatter)
from .filters import (ColumnIndexFilter,
                      RowIndexFilter,
                      SingleColumnFilter,
                      SingleRowFilter)
from . import cookbook

__VERSION__ = '0.0.7'
