"""
    pyexcel.core
    ~~~~~~~~~~~~~~~~~~~

    A list of pyexcel signature functions

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import re

import pyexcel_io.manager as manager

from pyexcel.sheets import Sheet
from pyexcel.book import Book
import pyexcel.sources as sources
import pyexcel.constants as constants
from pyexcel._compact import zip_longest


STARTS_WITH_DEST = '^dest_(.*)'
SAVE_AS_EXCEPTION = ("This function does not accept parameters for " +
                     "pyexce.Sheet. Please use pyexcel.save_as instead.")


def get_sheet(**keywords):
    """Get an instance of :class:`Sheet` from an excel source

    :param file_name: a file with supported file extension
    :param file_content: the file content
    :param file_stream: the file stream
    :param file_type: the file type in *content*
    :param session: database session
    :param table: database table
    :param model: a django model
    :param adict: a dictionary of one dimensional arrays
    :param url: a download http url for your excel file
    :param with_keys: load with previous dictionary's keys, default is True
    :param records: a list of dictionaries that have the same keys
    :param array: a two dimensional array, a list of lists
    :param keywords: additional parameters, see :meth:`Sheet.__init__`
    :param sheet_name: sheet name. if sheet_name is not given,
                       the default sheet at index 0 is loaded

    Not all parameters are needed. Here is a table

    ========================== =========================================
    source                     parameters
    ========================== =========================================
    loading from file          file_name, sheet_name, keywords
    loading from memory        file_type, content, sheet_name, keywords
    loading from sql           session, table
    loading from sql in django model
    loading from query sets    any query sets(sqlalchemy or django)
    loading from dictionary    adict, with_keys
    loading from records       records
    loading from array         array
    loading from an url        url
    ========================== =========================================

    see also :ref:`a-list-of-data-structures`
    """
    sheet_params = {}
    for field in constants.VALID_SHEET_PARAMETERS:
        if field in keywords:
            sheet_params[field] = keywords.pop(field)
    named_content = sources.get_sheet_stream(**keywords)
    sheet = Sheet(named_content.payload, named_content.name, **sheet_params)
    return sheet


def get_book(**keywords):
    """Get an instance of :class:`Book` from an excel source

    :param file_name: a file with supported file extension
    :param file_content: the file content
    :param file_stream: the file stream
    :param file_type: the file type in *content*
    :param session: database session
    :param tables: a list of database table
    :param models: a list of django models
    :param bookdict: a dictionary of two dimensional arrays
    :param url: a download http url for your excel file

    see also :ref:`a-list-of-data-structures`

    Here is a table of parameters:

    ========================== ===============================
    source                     parameters
    ========================== ===============================
    loading from file          file_name, keywords
    loading from memory        file_type, content, keywords
    loading from sql           session, tables
    loading from django models models
    loading from dictionary    bookdict
    loading from an url        url
    ========================== ===============================

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    book_stream = sources.get_book_stream(**keywords)
    book = Book(book_stream.to_dict(),
                filename=book_stream.filename,
                path=book_stream.path)
    return book


def save_as(**keywords):
    """Save a sheet from a data source to another one

    It accepts two sets of keywords. Why two sets? one set is
    source, the other set is destination. In order to distinguish
    the two sets, source set will be exactly the same
    as the ones for :meth:`pyexcel.get_sheet`; destination
    set are exactly the same as the ones for :class:`pyexcel.Sheet.save_as`
    but require a 'dest' prefix.

    :param keywords: additional keywords can be found at
                     :meth:`pyexcel.get_sheet`
    :param dest_file_name: another file name. **out_file** is deprecated
                           though is still accepted.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_table: the target destination table
    :param dest_model: the target django model
    :param dest_mapdict: a mapping dictionary,
                         see :meth:`pyexcel.Sheet.save_to_memory`
    :param dest_initializer: a custom initializer function for table or model
    :param dest_mapdict: nominate headers
    :param dest_batch_size: object creation batch size.
                            it is Django specific

    if csv file is destination format, python csv
    `fmtparams <https://docs.python.org/release/3.1.5/
    library/csv.html#dialects-and-formatting-parameters>`_
    are accepted

    for example: dest_lineterminator will replace default '\r\n'
    to the one you specified
    :returns: IO stream if saving to memory. None otherwise

    ================= =============================================
    Saving to source  parameters
    ================= =============================================
    file              dest_file_name, dest_sheet_name,
                      keywords with prefix 'dest'
    memory            dest_file_type, dest_content,
                      dest_sheet_name, keywords with prefix 'dest'
    sql               dest_session, dest_table,
                      dest_initializer, dest_mapdict
    django model      dest_model, dest_initializer,
                      dest_mapdict, dest_batch_size
    ================= =============================================

    In addition, this function use :class:`pyexcel.Sheet` to
    render the data which could have performance penalty. In exchange,
    parameters for :class:`pyexcel.Sheet` can be passed on, e.g.
    `name_columns_by_row`.

    """
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
    sheet_params = {}
    for field in constants.VALID_SHEET_PARAMETERS:
        if field in source_keywords:
            sheet_params[field] = source_keywords.pop(field)
    sheet = sources.get_sheet_stream(**source_keywords)
    if sheet_params != {}:
        raise Exception(SAVE_AS_EXCEPTION)
    return sources.save_sheet(sheet, **dest_keywords)


def save_book_as(**keywords):
    """Save a book from a data source to another one

    :param dest_file_name: another file name. **out_file** is
                           deprecated though is still accepted.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_tables: the list of target destination tables
    :param dest_models: the list of target destination django models
    :param dest_mapdicts: a list of mapping dictionaries
    :param dest_initializers: table initialization functions
    :param dest_mapdicts: to nominate a model or table fields. Optional
    :param dest_batch_size: batch creation size. Optional
    :param keywords: additional keywords can be found at
                     :meth:`pyexcel.get_book`
    :returns: IO stream if saving to memory. None otherwise

    ================ ============================================
    Saving to source parameters
    ================ ============================================
    file             dest_file_name, dest_sheet_name,
                     keywords with prefix 'dest'
    memory           dest_file_type, dest_content,
                     dest_sheet_name, keywords with prefix 'dest'
    sql              dest_session, dest_tables,
                     dest_table_init_func, dest_mapdict
    django model     dest_models, dest_initializers,
                     dest_mapdict, dest_batch_size
    ================ ============================================
    """
    dest_keywords, source_keywords = _split_keywords(**keywords)
    book = sources.get_book_stream(**source_keywords)
    return sources.save_book(book, **dest_keywords)


def get_array(**keywords):
    """Obtain an array from an excel source

    :param keywords: see :meth:`~pyexcel.get_sheet`
    """
    sheet = get_sheet(**keywords)
    return sheet.to_array()


def get_dict(name_columns_by_row=0, **keywords):
    """Obtain a dictionary from an excel source

    :param name_columns_by_row: specify a row to be a dictionary key.
                                It is default to 0 or first row.
    :param keywords: see :meth:`~pyexcel.get_sheet`

    If you would use a column index 0 instead, you should do::

        get_dict(name_columns_by_row=-1, name_rows_by_column=0)

    """
    sheet = get_sheet(name_columns_by_row=name_columns_by_row,
                      **keywords)
    return sheet.to_dict()


def get_records(name_columns_by_row=0, **keywords):
    """Obtain a list of records from an excel source

    :param name_columns_by_row: specify a row to be a dictionary key.
                                It is default to 0 or first row.
    :param keywords: see :meth:`~pyexcel.get_sheet`

    If you would use a column index 0 instead, you should do::

        get_records(name_columns_by_row=-1, name_rows_by_column=0)

    """
    sheet = get_sheet(name_columns_by_row=name_columns_by_row,
                      **keywords)
    return sheet.to_records()


def iget_array(**keywords):
    """Obtain a generator of an two dimensional array from an excel source

    It is similiar to :meth:`pyexcel.get_array` but it has less memory
    footprint.
    """
    sheet_stream = sources.get_sheet_stream(**keywords)
    return sheet_stream.payload


def iget_records(**keywords):
    """Obtain a generator of a list of records from an excel source

    It is similiar to :meth:`pyexcel.get_records` but it has less memory
    footprint but requires the headers to be in the first row. And the
    data matrix should be of equal length. It should consume less memory
    and should work well with large files.
    """
    sheet_stream = sources.get_sheet_stream(**keywords)
    headers = None
    for row_index, row in enumerate(sheet_stream.payload):
        if row_index == 0:
            headers = row
        else:
            yield dict(zip_longest(headers, row, fillvalue=''))


def get_book_dict(**keywords):
    """Obtain a dictionary of two dimensional arrays

    :param keywords: see :meth:`~pyexcel.get_book`
    """
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
    for key in keywords.keys():
        result = re.match(STARTS_WITH_DEST, key)
        if result:
            dest_keywords[result.group(1)] = keywords[key]
        else:
            source_keywords[key] = keywords[key]
    return dest_keywords, source_keywords
