
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
from .readers import SeriesReader, PlainReader, FilterableReader
from .utils import to_dict, to_array, to_records
from . import formatters, cookbook

__VERSION__ = '0.0.7'
