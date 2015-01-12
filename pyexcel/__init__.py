"""
    pyexcel
    ~~~~~~~~~~~~~~~~~~~

    **pyexcel** is a wrapper library to read, manipulate and
    write data in different excel formats: csv, ods, xls, xlsx
    and xlsm. It does not support styling, charts.

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .book import (
    BookReader,
    Book,
    get_book,
    load_book,
    load_book_from_memory)
from .writers import Writer, BookWriter
from .sheets import (
    Sheet,
    load,
    transpose,
    Reader,
    SeriesReader,
    ColumnSeriesReader,
    get_sheet,
    load_from_dict,
    load_from_records,
    load_from_memory,
    load_from_sql)
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

from _compact import BytesIO


def get_array(file_name, **keywords):
    sheet = get_sheet(file_name, **keywords)
    if sheet:
        return sheet.to_array()
    else:
        return None


def get_dict(file_name, **keywords):
    sheet = get_sheet(file_name, **keywords)
    if sheet:
        return sheet.to_dict()
    else:
        return None


def get_records(file_name, **keywords):
    sheet = get_sheet(file_name, **keywords)
    if sheet:
        return sheet.to_records()
    else:
        return None


def get_book_dict(file_name, **keywords):
    book = get_book(file_name, **keywords)
    return book.to_dict()


def save_as(file_name, out_file=None, **keywords):
    sheet = get_sheet(file_name, **keywords)
    sheet.save_as(out_file)


def save_book_as(file_name, out_file=None, **keywords):
    book = get_book(file_name, **keywords)
    book.save_as(out_file)


def save_to_memory(file_name, file_type, **keywords):
    io = BytesIO()
    sheet = get_sheet(file_name, **keywords)
    sheet.save_to_memory(file_type, io)
    io.seek(0)
    return sheet


def save_book_to_memory(file_name, file_type, **keywords):
    io = BytesIO()
    book = get_book(file_name, **keywords)
    book.save_to_memory(file_type, io)
    io.seek(0)
    return book


__VERSION__ = '0.1.2'
