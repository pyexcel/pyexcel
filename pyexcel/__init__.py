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
from .sheet import Sheet
from .internal.garbagecollector import free_resources
from .deprecated import (
    load_book,
    load_book_from_memory,
    load,
    load_from_memory,
    load_from_dict,
    load_from_records,
    Reader,
    SeriesReader,
    ColumnSeriesReader,
    BookReader
)
