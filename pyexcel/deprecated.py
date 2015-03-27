"""
    pyexcel.deprecated
    ~~~~~~~~~~~~~~~~~~~

    List of apis that become deprecated but was kept for backward compatibility

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from .source import load, load_book


def Reader(file=None, sheetname=None, **keywords):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next

    use as class would fail though
    changed since 0.0.7
    """
    print("Deprecated. Please use class Sheet instead")
    return load(file, sheetname=sheetname, **keywords)


def SeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has column headers in a selected row

    use as class would fail
    changed since 0.0.7
    """
    print("Deprecated. Please use class Sheet(..., name_columns_by_row=0,..) instead")
    return load(file, sheetname=sheetname, name_columns_by_row=series, **keywords)


def ColumnSeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has row headers in a selected column

    use as class would fail
    changed since 0.0.7
    """
    print("Deprecated. Please use class Sheet(..., name_rows_by_column=0..) instead")
    return load(file, sheetname=sheetname, name_rows_by_column=series, **keywords)


def BookReader(file, **keywords):
    """For backward compatibility
    """
    print("Deprecated. Please use class Book instead")
    return load_book(file, **keywords)
