"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support styling, charts.

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .book import Book
from .writers import Writer, BookWriter
from .sheets import (
    Sheet,
    transpose)
from .utils import to_dict, to_array, to_records, dict_to_array, from_records
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
from .source import (
    SingleSheetRecrodsSource,
    SingleSheetDictSource,
    SingleSheetQuerySetSource,
    SingleSheetSQLAlchemySource,
    SingleSheetDjangoSource,
    get_sheet,
    get_book,
    save_as,
    save_book_as
)
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
    BookReader
)


def get_array(**keywords):
    """Obtain an array from an excel source

    :param keywords: see :meth:`~pyexcel.get_sheet`
    """
    sheet = get_sheet(**keywords)
    if sheet:
        return sheet.to_array()
    else:
        return None


def get_dict(name_columns_by_row=0, **keywords):
    """Obtain a dictionary from an excel source

    :param name_columns_by_row: specify a row to be a dictionary key. It is default to 0 or first row. If you would use a column index 0 instead, you should do::

        get_dict(name_columns_by_row=-1, name_rows_by_column=0)
    
    :param keywords: see :meth:`~pyexcel.get_sheet`
    """
    sheet = get_sheet(name_columns_by_row=name_columns_by_row,
                      **keywords)
    if sheet:
        return sheet.to_dict()
    else:
        return None


def get_records(name_columns_by_row=0, **keywords):
    """Obtain a list of records from an excel source

    :param name_columns_by_row: specify a row to be a dictionary key. It is default to 0 or first row. If you would use a column index 0 instead, you should do::

        get_dict(name_columns_by_row=-1, name_rows_by_column=0)
    
    :param keywords: see :meth:`~pyexcel.get_sheet`
    """
    sheet = get_sheet(name_columns_by_row=name_columns_by_row,
                      **keywords)
    if sheet:
        return sheet.to_records()
    else:
        return None


def get_book_dict(**keywords):
    """Obtain a dictionary of two dimensional arrays

    :param keywords: see :meth:`~pyexcel.get_book`
    """
    book = get_book(**keywords)
    if book:
        return book.to_dict()
    else:
        return None


__VERSION__ = '0.1.5'
