"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Core functionality of pyexcel, data model

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .sheet import Sheet, NominableSheet, load, load_from_memory, Reader, SeriesReader, ColumnSeriesReader, PlainReader, FilterableReader
from .formattablesheet import FormattableSheet
from .filterablesheet import FilterableSheet
from .matrix import Matrix, transpose