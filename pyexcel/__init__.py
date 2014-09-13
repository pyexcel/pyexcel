"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support styling, charts.

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""

from .readers import Reader
from .writers import Writer
from .readers import FilterableReader, StaticSeriesReader
from .readers import ColumnFilterableSeriesReader, SeriesReader
import cookbook