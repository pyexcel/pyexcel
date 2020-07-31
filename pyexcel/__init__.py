"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support formulas, styles and charts.

    :copyright: (c) 2014-2019 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .__version__ import __author__, __version__
from .book import Book

# flake8: noqa
from .cookbook import (
    extract_a_sheet_from_a_book,
    merge_all_to_a_book,
    merge_csv_to_a_book,
    split_a_book,
)
from .core import (
    get_array,
    get_book,
    get_book_dict,
    get_dict,
    get_records,
    get_sheet,
    iget_array,
    iget_book,
    iget_records,
    isave_as,
    isave_book_as,
    save_as,
    save_book_as,
)
from .deprecated import (
    BookReader,
    ColumnSeriesReader,
    Reader,
    SeriesReader,
    load,
    load_book,
    load_book_from_memory,
    load_from_dict,
    load_from_memory,
    load_from_records,
)
from .internal.garbagecollector import free_resources
from .sheet import Sheet
