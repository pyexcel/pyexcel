"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support formulas, styles and charts.

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .book import Book
from .sheets import (
    Sheet,
    transpose)
from .utils import (
    to_dict,
    to_array,
    to_records,
    dict_to_array,
    from_records)
from .formatters import (
    ColumnFormatter,
    RowFormatter,
    SheetFormatter,
    NamedColumnFormatter,
    NamedRowFormatter)
from .filters import (
    ColumnIndexFilter,
    ColumnFilter,
    RowFilter,
    EvenColumnFilter,
    OddColumnFilter,
    EvenRowFilter,
    OddRowFilter,
    RowIndexFilter,
    SingleColumnFilter,
    RowValueFilter,
    NamedRowValueFilter,
    ColumnValueFilter,
    NamedColumnValueFilter,
    SingleRowFilter)
from .cookbook import (
    merge_csv_to_a_book,
    merge_all_to_a_book,
    split_a_book,
    extract_a_sheet_from_a_book)
from .core import (
    get_array,
    get_dict,
    get_records,
    get_book_dict,
    get_sheet,
    get_book,
    save_as,
    save_book_as)
from .deprecated import (
    load_book,
    load_book_from_memory,
    load_book_from_sql,
    load,
    load_from_memory,
    load_from_dict,
    load_from_sql,
    load_from_records,
    Reader,
    SeriesReader,
    ColumnSeriesReader,
    BookReader,
    Writer,
    BookWriter
)

from pyexcel_io.manager import RWManager
import pyexcel.sources.file_source_output as outfiles
all_types = RWManager.file_types + outfiles.file_types

for file_type in all_types:
    Sheet.register_presentation(file_type)
    Book.register_presentation(file_type)
