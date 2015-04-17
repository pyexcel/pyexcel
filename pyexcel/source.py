"""
    pyexcel.source
    ~~~~~~~~~~~~~~~~~~~

    Representation of excel data sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import os
import re
from .io import load_file, FILE_FORMAT_DJANGO, FILE_FORMAT_SQL, FILE_FORMAT_CSV, FILE_FORMAT_TSV
from ._compact import PY2, BytesIO, StringIO
from .sheets import Sheet, VALID_SHEET_PARAMETERS
from .book import Book
from .constants import DEFAULT_SHEET_NAME, MESSAGE_DEPRECATED_02, MESSAGE_ERROR_02


KEYWORD_MEMORY = 'memory'
KEYWORD_SOURCE = 'source'
KEYWORD_FILE_TYPE = 'file_type'
KEYWORD_FILE_NAME = 'file_name'
KEYWORD_SESSION = 'session'
KEYWORD_TABLE = 'table'
KEYWORD_MODEL = 'model'
KEYWORD_TABLES = 'tables'
KEYWORD_MODELS = 'models'
KEYWORD_CONTENT = 'content'
KEYWORD_ADICT = 'adict'
KEYWORD_RECORDS = 'records'
KEYWORD_ARRAY = 'array'
KEYWORD_COLUMN_NAMES = 'column_names'
KEYWORD_QUERY_SETS = 'query_sets'
KEYWORD_OUT_FILE = 'out_file'
KEYWORD_BOOKDICT = 'bookdict'
KEYWORD_MAPDICT = 'mapdict'
KEYWORD_MAPDICTS = 'mapdicts'
KEYWORD_INITIALIZER = 'initializer'
KEYWORD_INITIALIZERS = 'initializers'
KEYWORD_BATCH_SIZE = 'batch_size'

KEYWORD_STARTS_WITH_DEST = '^dest_(.*)'


def has_field(field, keywords):
    return field in keywords and keywords[field] is not None


def _get_io(file_type):
    if file_type in [FILE_FORMAT_CSV, FILE_FORMAT_TSV]:
        return StringIO()
    else:
        return BytesIO()

class Pluggible:
    fields = []

    @classmethod
    def is_my_business(self, **keywords):
        """
        If all required keys are present, this source is OK
        """
        statuses = [has_field(field, keywords) for field in self.fields]
        results = filter(lambda status: status==False, statuses)
        if not PY2:
            results = list(results)
        return len(results) == 0
        

def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    if len(items[0][1]) == 0:
        return None, None
    else:
        return items[0][0], items[0][1]


class ReadableSource(Pluggible):
    fields = [KEYWORD_SOURCE]

    def __init__(self, source=None, **keywords):
        self.source = source

    def get_data(self):
        return self.source.get_data()

        
class WriteableSource(Pluggible):
    fields = [KEYWORD_SOURCE]
    def __init__(self, source=None, **keywords):
        self.source = source
        
    def write_data(self, content):
        self.source.write_data(content)


class SingleSheetFileSource(ReadableSource, WriteableSource):
    fields = [KEYWORD_FILE_NAME]

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        
    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        io_book = load_file(self.file_name, **self.keywords)
        sheets = io_book.sheets()
        return one_sheet_tuple(sheets.items())

    def write_data(self, sheet):
        from .writers import Writer
        w = Writer(self.file_name, sheet_name=sheet.name, **self.keywords)
        w.write_reader(sheet)
        w.close()


class SingleSheetFileInMemorySource(SingleSheetFileSource):
    fields = [KEYWORD_CONTENT, KEYWORD_FILE_TYPE]

    def __init__(self, content=None, file_type=None, **keywords):
        SingleSheetFileSource.__init__(self, file_name=(file_type, content),**keywords)


class SingleSheetRecrodsSource(ReadableSource):
    fields= [KEYWORD_RECORDS]
    def __init__(self, records):
        self.records = records

    def get_data(self):
        from .utils import from_records
        return DEFAULT_SHEET_NAME, from_records(self.records)


class SingleSheetDictSource(ReadableSource):
    fields = [KEYWORD_ADICT]

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from .utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return DEFAULT_SHEET_NAME, tmp_array


class SingleSheetArraySource(ReadableSource):
    fields = [KEYWORD_ARRAY]

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return DEFAULT_SHEET_NAME, self.array


class SingleSheetQuerySetSource(ReadableSource):
    fields = [KEYWORD_COLUMN_NAMES, KEYWORD_QUERY_SETS]

    def __init__(self, column_names, query_sets, sheet_name=None):
        self.sheet_name = sheet_name
        if self.sheet_name is None:
            self.sheet_name = DEFAULT_SHEET_NAME
        self.column_names = column_names
        self.query_sets = query_sets

    def get_data(self):
        from .utils import from_query_sets
        return self.sheet_name, from_query_sets(self.column_names, self.query_sets)


class SingleSheetDatabaseSourceMixin(ReadableSource):
    def get_sql_book():
        pass
        
    def get_data(self):
        sql_book = self.get_sql_book()
        sheets = sql_book.sheets()
        return one_sheet_tuple(sheets.items())


class SingleSheetSQLAlchemySource(SingleSheetDatabaseSourceMixin, WriteableSource):
    fields = [KEYWORD_SESSION, KEYWORD_TABLE]

    def __init__(self, session, table, **keywords):
        self.session = session
        self.table = table
        self.keywords = keywords

    def get_sql_book(self):
        return load_file(FILE_FORMAT_SQL, session=self.session, tables=[self.table])

    def write_data(self, sheet):
        from .writers import Writer
        if(len(sheet.colnames)) == 0:
            sheet.name_columns_by_row(0)
        w = Writer(
            FILE_FORMAT_SQL,
            sheet_name=sheet.name,
            session=self.session,
            tables={
                sheet.name: (self.table,
                             sheet.colnames,
                             self.keywords.get(KEYWORD_MAPDICT, None),
                             self.keywords.get(KEYWORD_INITIALIZER, None)
                         )
            }
        )
        w.write_array(sheet.array)
        w.close()

class SingleSheetDjangoSource(SingleSheetDatabaseSourceMixin, WriteableSource):
    fields = [KEYWORD_MODEL]

    def __init__(self, model=None, **keywords):
        self.model = model
        self.keywords = keywords

    def get_sql_book(self):
        return load_file(FILE_FORMAT_DJANGO, models=[self.model])

    def write_data(self, sheet):
        from .writers import Writer
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(0)
        w = Writer(
            FILE_FORMAT_DJANGO,
            sheet_name=sheet.name,
            models={
                sheet.name:(
                    self.model,
                    sheet.colnames,
                    self.keywords.get(KEYWORD_MAPDICT, None),
                    self.keywords.get(KEYWORD_INITIALIZER, None)
                )
            },
            batch_size=self.keywords.get(KEYWORD_BATCH_SIZE, None)
        )
        w.write_array(sheet.array)
        w.close()

class BookInMemory(ReadableSource):
    fields = [KEYWORD_FILE_TYPE, KEYWORD_CONTENT]
    
    def __init__(self, file_type, content, **keywords):
        self.file_type = file_type
        self.content = content
        self.keywords = keywords

    def get_data(self):
        book = load_file((self.file_type, self.content), **self.keywords)
        return book.sheets(), KEYWORD_MEMORY, None


class BookInDict(ReadableSource):
    fields = [KEYWORD_BOOKDICT]
    
    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        return self.bookdict, KEYWORD_BOOKDICT, None


class BookSQLSource(ReadableSource, WriteableSource):
    fields = [KEYWORD_SESSION, KEYWORD_TABLES]
    
    def __init__(self, session, tables, **keywords):
        self.session = session
        self.tables = tables
        self.keywords = keywords

    def get_data(self):
        book = load_file(FILE_FORMAT_SQL, session=self.session, tables=self.tables)
        return book.sheets(), FILE_FORMAT_SQL, None
        
    def write_data(self, book):
        from .writers import BookWriter
        initializers = self.keywords.get(KEYWORD_INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(self.tables)
        mapdicts = self.keywords.get(KEYWORD_MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(self.tables)
        for sheet in book:
            if len(sheet.colnames)  == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.tables, colnames_array, mapdicts, initializers)
        table_dict = dict(zip(book.name_array, x))
        w = BookWriter(FILE_FORMAT_SQL, session=self.session, tables=table_dict)
        w.write_book_reader_to_db(book)
        w.close()


class BookDjangoSource(ReadableSource, WriteableSource):
    fields = [KEYWORD_MODELS]
    
    def __init__(self, models, **keywords):
        self.models = models
        self.keywords = keywords

    def get_data(self):
        book = load_file(FILE_FORMAT_DJANGO, models=self.models)
        return book.sheets(), FILE_FORMAT_DJANGO, None

    def write_data(self, book):
        from .writers import BookWriter
        batch_size = self.keywords.get(KEYWORD_BATCH_SIZE, None)
        initializers = self.keywords.get(KEYWORD_INITIALIZERS, None)
        if initializers is None:
            initializers= [None] * len(self.models)
        mapdicts = self.keywords.get(KEYWORD_MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(self.models)
        for sheet in book:
            if len(sheet.colnames)  == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.models, colnames_array, initializers, mapdicts)
        table_dict = dict(zip(book.name_array, x))
        w = BookWriter(FILE_FORMAT_DJANGO, models=table_dict, batch_size=batch_size)
        w.write_book_reader_to_db(book)
        w.close()


class SingleSheetOutMemory(SingleSheetFileInMemorySource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, **keywords):
        self.content = _get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords


class BookSource(SingleSheetFileSource):
    def get_data(self):
        book = load_file(self.file_name, **self.keywords)
        path, filename_alone = os.path.split(self.file_name)
        return book.sheets(), filename_alone, path

    def write_data(self, book):
        from .writers import BookWriter
        writer = BookWriter(self.file_name, **self.keywords)
        writer.write_book_reader(book)
        writer.close()


class BookSourceInMemory(BookSource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, **keywords):
        self.content = _get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords


SOURCES = [
    ReadableSource,
    SingleSheetFileSource,
    SingleSheetFileInMemorySource,
    SingleSheetRecrodsSource,
    SingleSheetDictSource,
    SingleSheetSQLAlchemySource,
    SingleSheetDjangoSource,
    SingleSheetQuerySetSource,
    SingleSheetArraySource
]


BOOK_SOURCES = [
    ReadableSource,
    BookSource,
    BookInMemory,
    BookInDict,
    BookSQLSource,
    BookDjangoSource
]

DEST_SOURCES = [
    WriteableSource,
    SingleSheetFileSource,
    SingleSheetOutMemory,
    SingleSheetSQLAlchemySource,
    SingleSheetDjangoSource
]

DEST_BOOK_SOURCES = [
    WriteableSource,
    BookSource,
    BookSourceInMemory,
    BookDjangoSource,
    BookSQLSource
]


class SourceFactory:
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
    :param content: the file content
    :param file_type: the file type in *content*
    :param session: database session
    :param table: database table
    :param model: a django model
    :param adict: a dictionary of one dimensional arrays
    :param with_keys: load with previous dictionary's keys, default is True
    :param records: a list of dictionaries that have the same keys
    :param array: a two dimensional array, a list of lists
    :param keywords: additional parameters, see :meth:`Sheet.__init__`
    :param sheet_name: sheet name. if sheet_name is not given, the default sheet
                       at index 0 is loaded

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
    :param content: the file content
    :param file_type: the file type in *content*
    :param session: database session
    :param tables: a list of database table
    :param models: a list of django models
    :param bookdict: a dictionary of two dimensional arrays
    see also :ref:`a-list-of-data-structures`

    Here is a table of parameters:

    ========================== ============================================
    source                     parameters
    ========================== ============================================
    loading from file          file_name, keywords
    loading from memory        file_type, content, keywords
    loading from sql           session, tables
    loading from django modles models
    loading from dictionary    bookdict
    ========================== ============================================

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
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
            dest_keywords[result.group(1)]= keywords[key]
        else:
            source_keywords[key] = keywords[key]
    if KEYWORD_OUT_FILE in keywords:
        print(MESSAGE_DEPRECATED_02)
        dest_keywords[KEYWORD_FILE_NAME] = keywords.pop(KEYWORD_OUT_FILE)
    return dest_keywords, source_keywords


def save_as(**keywords):
    """Save a sheet from a data srouce to another one

    :param dest_file_name: another file name. **out_file** is deprecated though is still accepted.
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
    file                       dest_file_name, dest_sheet_name, keywords with prefix 'dest_'
    memory                     dest_file_type, dest_content, dest_sheet_name, keywords with prefix 'dest_'
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
    file                       dest_file_name, dest_sheet_name, keywords with prefix 'dest_'
    memory                     dest_file_type, dest_content, dest_sheet_name, keywords with prefix 'dest_'
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
            return dest_source.content
    else:
        raise ValueError(MESSAGE_ERROR_02)
