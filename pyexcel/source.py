"""
    pyexcel.source
    ~~~~~~~~~~~~~~~~~~~

    Representation of incoming data source

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import os
from .io import load_file
from ._compact import PY2
from .sheets import Sheet
from .book import Book


def has_field(field, keywords):
    return field in keywords and keywords[field]


class DataSource:
    field = []
    optional_fields = {}

    def get_data(self):
        return []

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


class SingleSheetFile(DataSource):
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


class SingleSheetRecrodsSource(DataSource):
    fields= ['records']
    def __init__(self, records):
        self.records = records

    def get_data(self):
        from .utils import from_records
        return 'pyexcel_sheet1', from_records(self.records)


class SingleSheetDictSource(DataSource):
    fields = ['adict']

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from .utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return 'pyexcel_sheet1', tmp_array


class SingleSheetArraySource(DataSource):
    fields = ['array']

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return 'pyexcel_sheet1', self.array


class SingleSheetQuerySetSource(DataSource):
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


class SingleSheetDatabaseSourceMixin(DataSource):
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


SOURCES = [
    SingleSheetFile,
    SingleSheetRecrodsSource,
    SingleSheetDictSource,
    SingleSheetSQLAlchemySource,
    SingleSheetDjangoSource,
    SingleSheetQuerySetSource,
    SingleSheetFileInMemory,
    SingleSheetArraySource
]

#### BOOK #########
class BookFile(DataSource):
    fields = ['file_name']
    def __init__(self, file_name, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def get_data(self):
        book = load_file(self.file_name, **self.keywords)
        path, filename_alone = os.path.split(self.file_name)
        return book.sheets(), filename_alone, path

class BookInMemory(DataSource):
    fields = ['file_type', 'content']
    def __init__(self, file_type, content, **keywords):
        self.file_type = file_type
        self.content = content
        self.keywords = keywords

    def get_data(self):
        book = load_file((self.file_type, self.content), **self.keywords)
        return book.sheets(), 'memory', None

class BookInDict(DataSource):
    fields = ['bookdict']
    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        return self.bookdict, 'bookdict', None

class BookFromSQLTables(DataSource):
    fields = ['session', 'tables']
    def __init__(self, session, tables, **keywords):
        self.session = session
        self.tables = tables
        self.keywords = keywords

    def get_data(self):
        book = load_file('sql', session=self.session, tables=self.tables)
        return book.sheets(), 'sql', None
        
class BookFromDjangoModels(DataSource):
    fields = ['models']
    def __init__(self, models, **keywords):
        self.models = models
        self.keywords = keywords

    def get_data(self):
        book = load_file('django', models=self.models)
        return book.sheets(), 'django', None


BOOK_SOURCES = [
    BookFile,
    BookInMemory,
    BookInDict,
    BookFromSQLTables,
    BookFromDjangoModels
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
    loading from file          file_name, sheet_name, keywords
    loading from memory        file_type, content, sheet_name, keywords
    loading from sql           session ,table
    loading from sql in django django model
    loading from query sets    any query sets(sqlalchemy or django)
    loading from dictionary    adict, with_keys
    loading from records       records
    loading from array         array
    ========================== =========================================

    see also :ref:`a-list-of-data-structures`
    """
    sheet = None
    sheet_params = {}
    for field in ['name_columns_by_row', 'name_rows_by_column', 'colnames', 'rownames', 'transpose_before', 'transpose_after']:
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
    """
    source = SourceFactory.get_book_source(**keywords)
    if source is not None:
        sheets, filename, path = source.get_data()
        book = Book(sheets, filename=filename, path=path)
        return book
    return None
