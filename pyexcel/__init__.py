"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support formulas, styles and charts.

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
# flake8: noqa
import logging
from ._compact import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

from .cookbook import (
    merge_csv_to_a_book,
    merge_all_to_a_book,
    split_a_book,
    extract_a_sheet_from_a_book)
from .core import (
    get_array,
    iget_array,
    get_dict,
    get_records,
    iget_records,
    get_book_dict,
    get_sheet,
    get_book,
    save_as,
    isave_as,
    save_book_as,
    isave_book_as)
from .book import Book
from .sheets import Sheet
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
