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
from ._compact import BytesIO


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
    return book.to_dict()


def save_to_memory(file_type, **keywords):
    """Save a sheet of an excel source separately

    :param file_type: indicate the file type
    :param keywords: see :meth:`~pyexcel.get_sheet`
    :returns: IO stream
    """
    io = BytesIO()
    sheet = get_sheet(**keywords)
    sheet.save_to_memory(file_type, io)
    io.seek(0)
    return io


def save_book_to_memory(file_type, **keywords):
    """Save a sheet of an excel source to memory

    :param file_type: indicate the file type
    :param keywords: see :meth:`~pyexcel.get_book`
    :returns: IO stream
    """
    io = BytesIO()
    book = get_book(**keywords)
    book.save_to_memory(file_type, io)
    io.seek(0)
    return io


def save_as(out_file=None, file_type=None, **keywords):
    """Save a sheet of an excel source separately

    :param out_file: another file name.
    :param file_type: this is needed if you want to save to memory
    :param keywords: see :meth:`~pyexcel.get_sheet`
    :returns: None if saving to file, IO stream if saving to memory
    """
    if out_file:
        sheet = get_sheet(**keywords)
        sheet.save_as(out_file)
        return None
    elif file_type:
        return save_to_memory(file_type, **keywords)


def save_book_as(out_file=None, file_type=None, **keywords):
    """Save a copy of an excel source

    :param out_file: another file name.
    :param file_type: this is needed if you want to save to memory
    :param keywords: see :meth:`~pyexcel.get_book`
    :returns: None if saving to file, IO stream if saving to memory
    """
    if out_file:
        book = get_book(**keywords)
        book.save_as(out_file)
        return None
    elif file_type:
        return save_book_to_memory(file_type, **keywords)


__VERSION__ = '0.1.2'
