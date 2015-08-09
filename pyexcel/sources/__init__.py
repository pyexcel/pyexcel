"""
    pyexcel.sources
    ~~~~~~~~~~~~~~~~~~~

    Representation of excel data sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import re
from .base import ReadOnlySource, WriteOnlySource
from ..sheets import VALID_SHEET_PARAMETERS, Sheet
from ..book import Book
from ..constants import (
    KEYWORD_STARTS_WITH_DEST,
    MESSAGE_DEPRECATED_02,
    DEPRECATED_KEYWORD_OUT_FILE,
    DEPRECATED_KEYWORD_CONTENT,
    KEYWORD_FILE_CONTENT,
    KEYWORD_FILE_NAME,
    KEYWORD_FILE_TYPE,
    MESSAGE_ERROR_02
)
from .file import (
    SheetSource,
    BookSource
)
from .memory import (
    ReadOnlySheetSource,
    WriteOnlySheetSource,
    DictSource,
    RecrodsSource,
    ArraySource,
    ReadOnlyBookSource,
    BookDictSource,
    WriteOnlyBookSource
)
from .database import (
    SheetSQLAlchemySource,
    SheetDjangoSource,
    SheetQuerySetSource,
    BookSQLSource,
    BookDjangoSource
)
from .http import HttpBookSource, HttpSheetSource

SOURCES = [
    ReadOnlySource,
    SheetSource,
    ReadOnlySheetSource,
    SheetSQLAlchemySource,
    SheetDjangoSource,
    RecrodsSource,
    DictSource,
    SheetQuerySetSource,
    ArraySource,
    HttpSheetSource
]

DEST_SOURCES = [
    WriteOnlySource,
    SheetSource,
    WriteOnlySheetSource,
    SheetSQLAlchemySource,
    SheetDjangoSource
]

BOOK_SOURCES = [
    ReadOnlySource,
    BookSource,
    ReadOnlyBookSource,
    BookSQLSource,
    BookDjangoSource,
    BookDictSource,
    HttpBookSource
]

DEST_BOOK_SOURCES = [
    WriteOnlySource,
    BookSource,
    WriteOnlyBookSource,
    BookDjangoSource,
    BookSQLSource
]


class SourceFactory:
    """
    The factory method to support multiple datasources in getters and savers
    """
    @classmethod
    def get_generic_source(self, registry, **keywords):
        for source in registry:
            if source.is_my_business(**keywords):
                s = source(**keywords)
                return s
        return None

    @classmethod
    def get_source(self, **keywords):
        return self.get_generic_source(SOURCES, **keywords)

    @classmethod
    def get_book_source(self, **keywords):
        return self.get_generic_source(BOOK_SOURCES, **keywords)

    @classmethod
    def get_writeable_source(self, **keywords):
        return self.get_generic_source(DEST_SOURCES, **keywords)

    @classmethod
    def get_writeable_book_source(self, **keywords):
        return self.get_generic_source(DEST_BOOK_SOURCES, **keywords)


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
    sheet = None
    sheet_params = {}
    for field in VALID_SHEET_PARAMETERS:
        if field in keywords:
            sheet_params[field] = keywords.pop(field)
    if DEPRECATED_KEYWORD_CONTENT in keywords:
        print(MESSAGE_DEPRECATED_02)
        keywords[KEYWORD_FILE_CONTENT] = keywords.pop(
            DEPRECATED_KEYWORD_CONTENT)
    source = SourceFactory.get_source(**keywords)
    if source is not None:
        sheet_name, data = source.get_data()
        sheet = Sheet(data, sheet_name, **sheet_params)
        return sheet
    else:
        return None


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

    ========================== ============================================
    source                     parameters
    ========================== ============================================
    loading from file          file_name, keywords
    loading from memory        file_type, content, keywords
    loading from sql           session, tables
    loading from django models models
    loading from dictionary    bookdict
    ========================== ============================================

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    if DEPRECATED_KEYWORD_CONTENT in keywords:
        print(MESSAGE_DEPRECATED_02)
        keywords[KEYWORD_FILE_CONTENT] = keywords.pop(
            DEPRECATED_KEYWORD_CONTENT)
    source = SourceFactory.get_book_source(**keywords)
    if source is not None:
        sheets, filename, path = source.get_data()
        book = Book(sheets, filename=filename, path=path)
        return book
    return None


def split_keywords(**keywords):
    dest_keywords = {}
    source_keywords = {}
    for key in keywords.keys():
        result = re.match(KEYWORD_STARTS_WITH_DEST, key)
        if result:
            dest_keywords[result.group(1)] = keywords[key]
        else:
            source_keywords[key] = keywords[key]
    if DEPRECATED_KEYWORD_OUT_FILE in keywords:
        print(MESSAGE_DEPRECATED_02)
        dest_keywords[KEYWORD_FILE_NAME] = keywords.pop(
            DEPRECATED_KEYWORD_OUT_FILE)
    if DEPRECATED_KEYWORD_CONTENT in keywords:
        print(MESSAGE_DEPRECATED_02)
        dest_keywords[KEYWORD_FILE_CONTENT] = keywords.pop(
            DEPRECATED_KEYWORD_CONTENT)
    return dest_keywords, source_keywords


def save_as(**keywords):
    """Save a sheet from a data srouce to another one

    :param dest_file_name: another file name. **out_file** is deprecated
                           though is still accepted.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_table: the target destination table
    :param dest_model: the target django model
    :param dest_mapdict: a mapping dictionary, see :meth:`~pyexcel.Sheet.save_to_memory`
    :param dest_initializer: a custom initializer function for table or model
    :param dest_mapdict: nominate headers
    :param dest_batch_size: object creation batch size. Django specific
    :param keywords: additional keywords can be found at :meth:`pyexcel.get_sheet`
    :returns: IO stream if saving to memory. None otherwise

    ========================== =============================================================================
    Saving to source           parameters
    ========================== =============================================================================
    file                       dest_file_name, dest_sheet_name, keywords with prefix 'dest'
    memory                     dest_file_type, dest_content, dest_sheet_name, keywords with prefix 'dest'
    sql                        dest_session, table, dest_initializer, dest_mapdict
    django model               dest_model, dest_initializer, dest_mapdict, dest_batch_size
    ========================== =============================================================================
    """
    dest_keywords, source_keywords = split_keywords(**keywords)
    dest_source = SourceFactory.get_writeable_source(**dest_keywords)
    if dest_source is not None:
        sheet = get_sheet(**source_keywords)
        sheet.save_to(dest_source)
        if KEYWORD_FILE_TYPE in dest_source.fields:
            dest_source.content.seek(0)            
            return dest_source.content
    else:
        raise ValueError(MESSAGE_ERROR_02)


def save_book_as(**keywords):
    """Save a book from a data source to another one

    :param dest_file_name: another file name. **out_file** is deprecated though is still accepted.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_tables: the list of target destination tables
    :param dest_models: the list of target destination django models
    :param dest_mapdicts: a list of mapping dictionaries
    :param dest_initializers: table initialization fuctions
    :param dest_mapdicts: to nominate a model or table fields. Optional
    :param dest_batch_size: batch creation size. Optional
    :param keywords: additional keywords can be found at :meth:`pyexcel.get_sheet`
    :returns: IO stream if saving to memory. None otherwise

    ========================== =============================================================================
    Saving to source           parameters
    ========================== =============================================================================
    file                       dest_file_name, dest_sheet_name, keywords with prefix 'dest'
    memory                     dest_file_type, dest_content, dest_sheet_name, keywords with prefix 'dest'
    sql                        dest_session, dest_tables, dest_table_init_func, dest_mapdict
    django model               dest_models, dest_initializers, dest_mapdict, dest_batch_size
    ========================== =============================================================================
    """
    dest_keywords, source_keywords = split_keywords(**keywords)
    dest_source = SourceFactory.get_writeable_book_source(**dest_keywords)
    if dest_source is not None:
        book = get_book(**source_keywords)
        book.save_to(dest_source)
        if KEYWORD_FILE_TYPE in dest_source.fields:
            dest_source.content.seek(0)
            return dest_source.content
    else:
        raise ValueError(MESSAGE_ERROR_02)
