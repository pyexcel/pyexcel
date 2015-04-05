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
    SingleSheetFile,
    SingleSheetRecrodsSource,
    SingleSheetDictSource,
    SingleSheetQuerySetSource,
    SingleSheetSQLAlchemySource,
    SingleSheetDjangoSource,
    get_sheet,
    get_book,
    save_as
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
from ._compact import BytesIO, StringIO


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

def save_book_to_database(session, tables, **keywords):
    """Save a book to database

    :param session: the database session
    :param tables: a list of database tables
    :param mapdicts: a list of mapping dictionaries
    see also :meth:`~pyexcel.Book.save_to_database`
    """
    book = get_book(**keywords)
    book.save_to_database(session, tables)
    return None


def save_book_to_django_models(dest_models, **keywords):
    """Save a book to database

    :param session: the database session
    :param tables: a list of database tables
    :param mapdicts: a list of mapping dictionaries
    see also :meth:`~pyexcel.Book.save_to_database`
    """
    book = get_book(**keywords)
    book.save_to_django_models(dest_models)
    return None


def _get_io(file_type):
    if file_type in ['csv', 'tsv']:
        return StringIO()
    else:
        return BytesIO()


def save_book_to_memory(dest_file_type, **keywords):
    """Save a sheet of an excel source to memory

    :param file_type: indicate the file type
    :param keywords: see :meth:`~pyexcel.get_book`
    :returns: IO stream
    """
    io = _get_io(dest_file_type)
    book = get_book(**keywords)
    book.save_to_memory(dest_file_type, io)
    io.seek(0)
    return io


def save_book_as(out_file=None, dest_file_type=None,
                 dest_session=None, dest_tables=None,
                 dest_models=None,
                 **keywords):
    """Save a copy of an excel source

    :param out_file: another file name.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_tables: the list of target destination tables
    :param dest_models: the list of target destination django models
    :param mapdicts: a list of mapping dictionaries, see :methd:`~pyexcel.Book.save_to_memory`
    :param keywords: see :meth:`~pyexcel.get_book`
    :returns: IO stream if saving to memory. None otherwise
    """
    if out_file:
        book = get_book(**keywords)
        book.save_as(out_file)
        return None
    elif dest_file_type:
        return save_book_to_memory(dest_file_type, **keywords)
    elif dest_session and dest_tables:
        return save_book_to_database(dest_session, dest_tables, **keywords)
    elif dest_models:
        return save_book_to_django_models(dest_models, **keywords)
    raise ValueError("No valid parameters found!")


__VERSION__ = '0.1.5'
