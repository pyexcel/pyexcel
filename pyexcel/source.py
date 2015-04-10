"""
    pyexcel.source
    ~~~~~~~~~~~~~~~~~~~

    Representation of incoming data source

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import os
import re
from .io import load_file
from ._compact import PY2, BytesIO, StringIO
from .sheets import Sheet
from .book import Book


def has_field(field, keywords):
    return field in keywords and keywords[field]


def _get_io(file_type):
    if file_type in ['csv', 'tsv']:
        return StringIO()
    else:
        return BytesIO()

class Pluggible:
    field = []

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
    fields = ['source']

    def __init__(self, source=None, **keywords):
        self.source = source

    def get_data(self):
        return self.source.get_data()

        
class SingleSheetFile(ReadableSource):
    fields = ['file_name']

    def __init__(self, file_name=None, sheet_name=None, sheet_index=None, **keywords):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.sheet_index = sheet_index
        self.keywords = keywords
        
    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        if self.sheet_name:
            io_book = load_file(self.file_name, sheet_name=self.sheet_name, **self.keywords)
            sheets = io_book.sheets()
        else:
            if self.sheet_index:
                sheet_index = self.sheet_index
            else:
                sheet_index = 0
            io_book = load_file(self.file_name, sheet_index=sheet_index, **self.keywords)
            sheets = io_book.sheets()
        return one_sheet_tuple(sheets.items())


class SingleSheetFileInMemory(SingleSheetFile):
    fields = ['content', 'file_type']

    def __init__(self, content=None, file_type=None, **keywords):
        SingleSheetFile.__init__(self, file_name=(file_type, content),**keywords)


class SingleSheetRecrodsSource(ReadableSource):
    fields= ['records']
    def __init__(self, records):
        self.records = records

    def get_data(self):
        from .utils import from_records
        return 'pyexcel_sheet1', from_records(self.records)


class SingleSheetDictSource(ReadableSource):
    fields = ['adict']

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from .utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return 'pyexcel_sheet1', tmp_array


class SingleSheetArraySource(ReadableSource):
    fields = ['array']

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return 'pyexcel_sheet1', self.array


class SingleSheetQuerySetSource(ReadableSource):
    fields = ['column_names', 'query_sets']

    def __init__(self, column_names, query_sets, sheet_name=None):
        self.sheet_name = sheet_name
        if self.sheet_name is None:
            self.sheet_name = 'pyexcel_sheet1'
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


class SingleSheetSQLAlchemySource(SingleSheetDatabaseSourceMixin):
    fields = ['session', 'table']

    def __init__(self, session, table):
        self.session = session
        self.table = table

    def get_sql_book(self):
        return load_file('sql', session=self.session, tables=[self.table])


class SingleSheetDjangoSource(SingleSheetDatabaseSourceMixin):
    fields = ['model']

    def __init__(self, model):
        self.model = model

    def get_sql_book(self):
        return load_file('django', models=[self.model])


class BookFile(ReadableSource):
    fields = ['file_name']
    
    def __init__(self, file_name, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def get_data(self):
        book = load_file(self.file_name, **self.keywords)
        path, filename_alone = os.path.split(self.file_name)
        return book.sheets(), filename_alone, path


class BookInMemory(ReadableSource):
    fields = ['file_type', 'content']
    
    def __init__(self, file_type, content, **keywords):
        self.file_type = file_type
        self.content = content
        self.keywords = keywords

    def get_data(self):
        book = load_file((self.file_type, self.content), **self.keywords)
        return book.sheets(), 'memory', None


class BookInDict(ReadableSource):
    fields = ['bookdict']
    
    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        return self.bookdict, 'bookdict', None

class BookFromSQLTables(ReadableSource):
    fields = ['session', 'tables']
    
    def __init__(self, session, tables, **keywords):
        self.session = session
        self.tables = tables
        self.keywords = keywords

    def get_data(self):
        book = load_file('sql', session=self.session, tables=self.tables)
        return book.sheets(), 'sql', None
        
class BookFromDjangoModels(ReadableSource):
    fields = ['models']
    
    def __init__(self, models, **keywords):
        self.models = models
        self.keywords = keywords

    def get_data(self):
        book = load_file('django', models=self.models)
        return book.sheets(), 'django', None


class WriteableSource(Pluggible):
    fields = ['source']
    def __init__(self, source=None, **keywords):
        self.source = source
        
    def write_data(self, content):
        self.source.write_data(content)


class SingleSheetOutFile(WriteableSource):
    fields = ['file_name']

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        
    def write_data(self, sheet):
        from .writers import Writer
        w = Writer(self.file_name, sheet_name=sheet.name, **self.keywords)
        w.write_reader(sheet)
        w.close()

class SingleSheetOutMemory(SingleSheetOutFile):
    fields = ['file_type']

    def __init__(self, file_type=None, **keywords):
        self.content = _get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords


class SingleSheetOutSQLTable(WriteableSource):
    fields = ['session', 'table']

    def __init__(self, session=None, table=None, **keywords):
        self.session = session
        self.table = table
        self.keywords = keywords

    def write_data(self, sheet):
        from .writers import Writer
        if(len(sheet.colnames)) == 0:
            sheet.name_columns_by_row(0)
        w = Writer(
            'sql',
            sheet_name=sheet.name,
            session=self.session,
            tables={
                sheet.name: (self.table,
                             sheet.colnames,
                             self.keywords.get('table_init_func', None),
                             self.keywords.get('mapdict', None)
                         )
            }
        )
        w.write_array(sheet.array)
        w.close()


class SingleSheetOutDjangoModel(WriteableSource):
    fields = ['model']

    def __init__(self, model=None, **keywords):
        self.model = model 
        self.keywords = keywords

    def write_data(self, sheet):
        from .writers import Writer
        if len(sheet.colnames) == 0:
            sheet.name_columns_by_row(0)
        w = Writer(
            'django',
            sheet_name=sheet.name,
            models={
                sheet.name:(
                    self.model,
                    sheet.colnames,
                    self.keywords.get('mapdict', None),
                    self.keywords.get('data_wrapper', None)
                )
            },
            batch_size=self.keywords.get('batch_size', None)
        )
        w.write_array(sheet.array)
        w.close()


class BookSource(SingleSheetOutFile):
    def write_data(self, book):
        from .writers import BookWriter
        writer = BookWriter(self.file_name, **self.keywords)
        writer.write_book_reader(book)
        writer.close()


class BookSourceInMemory(BookSource):
    fields = ['file_type']

    def __init__(self, file_type=None, **keywords):
        self.content = _get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords


class BookOutSQLTables(WriteableSource):
    fields = ['session', 'tables']
    def __init__(self, session=None, tables=None, table_init_funcs=None, mapdicts=None):
        self.session = session
        self.tables = tables
        self.table_init_funcs = table_init_funcs
        if self.table_init_funcs is None:
            self.table_init_funcs = [None] * len(self.tables)
        self.mapdicts = mapdicts
        if self.mapdicts is None:
            self.mapdicts = [None] * len(self.tables)

    def write_data(self, book):
        from .writers import BookWriter
        for sheet in book:
            if len(sheet.colnames)  == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.tables, colnames_array, self.table_init_funcs,self. mapdicts)
        table_dict = dict(zip(book.name_array, x))
        w = BookWriter('sql', session=self.session, tables=table_dict)
        w.write_book_reader_to_db(book)
        w.close()
        
        
class BookOutDjangoModels(WriteableSource):
    fields = ['models']

    def __init__(self, models=None, data_wrappers=None, mapdicts=None, batch_size=None):
        self.models = models
        self.data_wrappers = data_wrappers
        self.batch_size = batch_size
        if self.data_wrappers is None:
            self.data_wrappers= [None] * len(models)
        self.mapdicts = mapdicts
        if self.mapdicts is None:
            self.mapdicts = [None] * len(models)

    def write_data(self, book):
        from .writers import BookWriter
        for sheet in book:
            if len(sheet.colnames)  == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.models, colnames_array, self.data_wrappers, self.mapdicts)
        table_dict = dict(zip(book.name_array, x))
        w = BookWriter('django', models=table_dict, batch_size=self.batch_size)
        w.write_book_reader_to_db(book)
        w.close()


SOURCES = [
    ReadableSource,
    SingleSheetFile,
    SingleSheetRecrodsSource,
    SingleSheetDictSource,
    SingleSheetSQLAlchemySource,
    SingleSheetDjangoSource,
    SingleSheetQuerySetSource,
    SingleSheetFileInMemory,
    SingleSheetArraySource
]


BOOK_SOURCES = [
    ReadableSource,
    BookFile,
    BookInMemory,
    BookInDict,
    BookFromSQLTables,
    BookFromDjangoModels
]

DEST_SOURCES = [
    SingleSheetOutFile,
    SingleSheetOutMemory,
    SingleSheetOutSQLTable,
    SingleSheetOutDjangoModel
]

DEST_BOOK_SOURCES = [
    BookSource,
    BookSourceInMemory,
    BookOutSQLTables,
    BookOutDjangoModels
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
    def get_writable_source(self, **keywords):
        return self.get_generic_source(DEST_SOURCES, **keywords)

    @classmethod
    def get_writable_book_source(self, **keywords):
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
    valid_sheet_params = ['name_columns_by_row',
                          'name_rows_by_column',
                          'colnames',
                          'rownames',
                          'transpose_before',
                          'transpose_after']
    for field in valid_sheet_params:
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


def save_as(**keywords):
    """Save a sheet from a data srouce to another one

    :param dest_file_name: another file name. **out_file** is deprecated though is still accepted.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_table: the target destination table
    :param dest_table_init_func: custom table initialization function
    :param dest_model: the target django model
    :param dest_mapdict: a mapping dictionary, see :meth:`~pyexcel.Sheet.save_to_memory`
    :param dest_data_wrapper: a custom django model initialization function
    :param dest_mapdict: nominate headers
    :param dest_batch_size: object creation batch size. Django specific
    :param keywords: additional keywords can be found at :meth:`pyexcel.get_sheet`
    :returns: IO stream if saving to memory. None otherwise

    ========================== =============================================================================
    Saving to source           parameters
    ========================== =============================================================================
    file                       dest_file_name, dest_sheet_name, keywords with prefix 'dest_'
    memory                     dest_file_type, dest_content, dest_sheet_name, keywords with prefix 'dest_'
    sql                        dest_session, table, dest_table_init_func, dest_mapdict
    django model               dest_model, dest_data_wrapper, dest_mapdict, dest_batch_size
    ========================== =============================================================================
    """
    dest_keywords = {}
    source_keywords = {}
    for key in keywords.keys():
        result = re.match('^dest_(.*)', key)
        if result:
            dest_keywords[result.group(1)]= keywords[key]
        else:
            source_keywords[key] = keywords[key]
    if 'out_file' in keywords:
        print('depreciated. please use dest_file_name')
        dest_keywords['file_name'] = keywords.pop('out_file')
    dest_source = SourceFactory.get_writable_source(**dest_keywords)
    if dest_source is not None:
        sheet = get_sheet(**source_keywords)
        sheet.save_to(dest_source)
        if 'file_type' in dest_source.fields:
            return dest_source.content
    else:
        raise ValueError("No valid parameters found!")


def save_book_as(**keywords):
    """Save a book from a data source to another one

    :param dest_file_name: another file name. **out_file** is deprecated though is still accepted.
    :param dest_file_type: this is needed if you want to save to memory
    :param dest_session: the target database session
    :param dest_tables: the list of target destination tables
    :param dest_models: the list of target destination django models
    :param dest_mapdicts: a list of mapping dictionaries
    :param dest_table_init_funcs: table initialization fuctions
    :param dest_data_wrappers: to initialize a model. Optional
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
    django model               dest_models, dest_data_wrappers, dest_mapdict, dest_batch_size
    ========================== =============================================================================
    """
    dest_keywords = {}
    source_keywords = {}
    for key in keywords.keys():
        result = re.match('^dest_(.*)', key)
        if result:
            dest_keywords[result.group(1)]= keywords[key]
        else:
            source_keywords[key] = keywords[key]
    if 'out_file' in keywords:
        print('depreciated. please use dest_file_name')
        dest_keywords['file_name'] = keywords.pop('out_file')
    dest_source = SourceFactory.get_writable_book_source(**dest_keywords)
    if dest_source is not None:
        book = get_book(**source_keywords)
        book.save_to(dest_source)
        if 'file_type' in dest_source.fields:
            return dest_source.content
    else:
        raise ValueError("No valid parameters found!")

