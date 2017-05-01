"""
    pyexcel.core
    ~~~~~~~~~~~~~~~~~~~

    A list of pyexcel signature functions

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import re

import pyexcel_io.manager as manager

from pyexcel.sheet import Sheet
from pyexcel.book import Book, to_book
import pyexcel.internal.core as sources
import pyexcel.constants as constants
from pyexcel._compact import zip_longest, add_doc
import pyexcel.docs as docs


STARTS_WITH_DEST = '^dest_(.*)'
SAVE_AS_EXCEPTION = ("This function does not accept parameters for " +
                     "pyexce.Sheet. Please use pyexcel.save_as instead.")


@add_doc(docs.GET_SHEET_DOC)
def get_sheet(**keywords):
    sheet_params = {}
    for field in constants.VALID_SHEET_PARAMETERS:
        if field in keywords:
            sheet_params[field] = keywords.pop(field)
    named_content = sources.get_sheet_stream(**keywords)
    sheet = Sheet(named_content.payload, named_content.name, **sheet_params)
    return sheet


@add_doc(docs.GET_BOOK_DOC)
def get_book(**keywords):
    book_stream = sources.get_book_stream(**keywords)
    book = Book(book_stream.to_dict(),
                filename=book_stream.filename,
                path=book_stream.path)
    return book


@add_doc(docs.SAVE_AS_DOC)
def save_as(**keywords):
    dest_keywords, source_keywords = _split_keywords(**keywords)
    sheet_params = {}
    for field in constants.VALID_SHEET_PARAMETERS:
        if field in source_keywords:
            sheet_params[field] = source_keywords.pop(field)
    sheet_stream = sources.get_sheet_stream(**source_keywords)
    sheet = Sheet(sheet_stream.payload, sheet_stream.name,
                  **sheet_params)
    return sources.save_sheet(sheet, **dest_keywords)


def isave_as(**keywords):
    """Save a sheet from a data source to another one with less memory

    It is simliar to :meth:`pyexcel.save_as` except that it does
    not accept parameters for :class:`pyexcel.Sheet`. And it read
    when it writes.
    """

    dest_keywords, source_keywords = _split_keywords(**keywords)
    for field in constants.VALID_SHEET_PARAMETERS:
        if field in source_keywords:
            raise Exception(SAVE_AS_EXCEPTION)
    sheet = sources.get_sheet_stream(**source_keywords)
    return sources.save_sheet(sheet, **dest_keywords)


@add_doc(docs.SAVE_BOOK_AS_DOC)
def save_book_as(**keywords):
    dest_keywords, source_keywords = _split_keywords(**keywords)
    book = sources.get_book_stream(**source_keywords)
    book = to_book(book)
    return sources.save_book(book, **dest_keywords)


def isave_book_as(**keywords):
    """Save a book from a data source to another one

    It is simliar to :meth:`pyexcel.save_book_as` but it read
    when it writes. This function provide some speedup but
    the output data is made uniform.
    """
    dest_keywords, source_keywords = _split_keywords(**keywords)
    book = sources.get_book_stream(**source_keywords)
    return sources.save_book(book, **dest_keywords)


@add_doc(docs.GET_ARRAY_DOC)
def get_array(**keywords):
    sheet = get_sheet(**keywords)
    return sheet.to_array()


@add_doc(docs.GET_DICT_DOC)
def get_dict(name_columns_by_row=0, **keywords):
    sheet = get_sheet(name_columns_by_row=name_columns_by_row,
                      **keywords)
    return sheet.to_dict()


@add_doc(docs.GET_RECORDS_DOC)
def get_records(name_columns_by_row=0, **keywords):
    sheet = get_sheet(name_columns_by_row=name_columns_by_row,
                      **keywords)
    return sheet.to_records()


@add_doc(docs.IGET_ARRAY_DOC)
def iget_array(**keywords):
    sheet_stream = sources.get_sheet_stream(**keywords)
    return sheet_stream.payload


@add_doc(docs.IGET_RECORDS_DOC)
def iget_records(**keywords):
    sheet_stream = sources.get_sheet_stream(**keywords)
    headers = None
    for row_index, row in enumerate(sheet_stream.payload):
        if row_index == 0:
            headers = row
        else:
            yield dict(zip_longest(headers, row,
                                   fillvalue=constants.DEFAULT_NA))


@add_doc(docs.GET_BOOK_DICT_DOC)
def get_book_dict(**keywords):
    book = get_book(**keywords)
    return book.to_dict()


def get_io_type(file_type):
    """
    Return the io stream types, string or bytes
    """
    io_type = manager.get_io_type(file_type)
    if io_type is None:
        io_type = "string"
    return io_type


def _split_keywords(**keywords):
    dest_keywords = {}
    source_keywords = {}
    for key, value in keywords.items():
        result = re.match(STARTS_WITH_DEST, key)
        if result:
            dest_keywords[result.group(1)] = value
        else:
            source_keywords[key] = value
    return dest_keywords, source_keywords
