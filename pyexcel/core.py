"""
    pyexcel.core
    ~~~~~~~~~~~~~~~~~~~

    A list of pyexcel signature functions

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
import re

from .sheets import VALID_SHEET_PARAMETERS, Sheet
from .book import Book
from .generators import BookStream, SheetStream
import pyexcel.sources as sources

from ._compact import PY2
from pyexcel_io.manager import RWManager


STARTS_WITH_DEST = '^dest_(.*)'


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
    ========================== =========================================

    see also :ref:`a-list-of-data-structures`
    """
    sheet_params = {}
    for field in VALID_SHEET_PARAMETERS:
        if field in keywords:
            sheet_params[field] = keywords.pop(field)
    named_content = get_sheet_stream(**keywords)
    sheet = Sheet(named_content.payload, named_content.name, **sheet_params)
    return sheet


def get_sheet_stream(**keywords):
    source = sources.get_source(**keywords)
    sheets = source.get_data()
    sheet_name, data = one_sheet_tuple(sheets.items())
    return SheetStream(sheet_name, data)


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
    ========================== ===============================

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    book_stream = get_book_stream(**keywords)
    book = Book(book_stream.to_dict(),
                filename=book_stream.filename,
                path=book_stream.path)
    return book


def get_book_stream(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    source = sources.get_book_source(**keywords)
    sheets = source.get_data()
    filename, path = source.get_source_info()
    book = BookStream(sheets, filename=filename, path=path)
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
    sql               dest_session, table,
                      dest_initializer, dest_mapdict
    django model      dest_model, dest_initializer,
                      dest_mapdict, dest_batch_size
    ================= =============================================
    """
    dest_keywords, source_keywords = _split_keywords(**keywords)
    dest_source = sources.get_writable_source(**dest_keywords)
    sheet_params = {}
    for field in VALID_SHEET_PARAMETERS:
        if field in source_keywords:
            sheet_params[field] = source_keywords.pop(field)
    sheet = get_sheet_stream(**source_keywords)
    if sheet_params != {}:
        sheet = Sheet(sheet.payload, sheet.name,
                      **sheet_params)
    sheet.save_to(dest_source)
    if hasattr(dest_source, 'content'):
        _try_put_file_read_pointer_to_its_begining(dest_source.content)
        return dest_source.content


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
                     :meth:`pyexcel.get_sheet`
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
    dest_source = sources.get_writable_book_source(**dest_keywords)
    book = get_book_stream(**source_keywords)
    book.save_to(dest_source)
    if hasattr(dest_source, 'content'):
        _try_put_file_read_pointer_to_its_begining(dest_source.content)
        return dest_source.content


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
    io_type = RWManager.get_io_type(file_type)
    if io_type is None:
        io_type = "string"
    return io_type


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    return items[0][0], items[0][1]


def _try_put_file_read_pointer_to_its_begining(a_stream):
    if PY2:
        try:
            a_stream.seek(0)
        except IOError:
            pass
    else:
        import io
        try:
            a_stream.seek(0)
        except io.UnsupportedOperation:
            pass


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
