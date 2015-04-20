"""
    pyexcel.sources.database
    ~~~~~~~~~~~~~~~~~~~

    Representation of database sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import datetime
from .base import ReadOnlySource, Source, one_sheet_tuple
from ..io import FILE_FORMAT_SQL, FILE_FORMAT_DJANGO, load_file
from ..constants import (
    KEYWORD_TABLES,
    KEYWORD_MODELS,
    KEYWORD_INITIALIZERS,
    KEYWORD_MAPDICTS,
    KEYWORD_COLUMN_NAMES,
    KEYWORD_BATCH_SIZE,
    KEYWORD_QUERY_SETS,
    KEYWORD_SESSION,
    KEYWORD_TABLE,
    KEYWORD_MAPDICT,
    KEYWORD_INITIALIZER,
    KEYWORD_MODEL,
    DEFAULT_SHEET_NAME
)


def from_query_sets(column_names, query_sets):
    array = []
    array.append(column_names)
    for o in query_sets:
        new_array = []
        for column in column_names:
            value = getattr(o, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        array.append(new_array)
    return array
        
from pyexcel_io import (BookReaderBase, SheetReaderBase, BookWriter, SheetWriter)
from .._compact import OrderedDict
from ..constants import MESSAGE_INVALID_PARAMETERS


class SQLTableReader(SheetReaderBase):
    """Read a table
    """
    def __init__(self, session, table):
        self.session = session
        self.table = table

    @property
    def name(self):
        return getattr(self.table, '__tablename__', None)

    def to_array(self):
        from ..utils import from_query_sets
        objects = self.session.query(self.table).all()
        if len(objects) == 0:
            return []
        else:
            column_names = sorted([column for column in objects[0].__dict__
                                   if column != '_sa_instance_state'])
            
            return from_query_sets(column_names, objects)


class SQLBookReader(BookReaderBase):
    """Read a list of tables
    """
    def __init__(self, session=None, tables=None):
        self.my_sheets = OrderedDict()
        for table in tables:
            sqltablereader = SQLTableReader(session, table)
            self.my_sheets[sqltablereader.name]=sqltablereader.to_array()
            
    def sheets(self):
        return self.my_sheets

        
class SQLTableWriter(SheetWriter):
    """Write to a table
    """
    def __init__(self, session, table_params):
        self.session = session
        self.table = None
        self.initializer = None
        self.mapdict = None
        self.column_names = None
        if len(table_params) == 4:
            self.table, self.column_names, self.mapdict, self.initializer = table_params
        else:
            raise ValueError(MESSAGE_INVALID_PARAMETERS)

        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None

    def set_sheet_name(self, name):
        pass

    def write_row(self, array):
        row = dict(zip(self.column_names, array))
        if self.initializer:
            o = self.initializer(row)
        else:
            o = self.table()
            for name in self.column_names:
                if self.mapdict is not None:
                    key = self.mapdict[name]
                else:
                    key = name
                setattr(o, key, row[name])
        self.session.add(o)

    def write_array(self, table):
        SheetWriter.write_array(self, table)
        self.session.commit()

        
class SQLBookWriter(BookWriter):
    """Write to alist of tables
    """
    def __init__(self, file, session=None, tables=None, **keywords):
        BookWriter.__init__(self, file, **keywords)
        self.session = session
        self.tables = tables

    def create_sheet(self, name):
        table_params = self.tables[name]
        return SQLTableWriter(self.session, table_params)

    def close(self):
        pass

class DjangoModelReader(SheetReaderBase):
    """Read from django model
    """
    def __init__(self, model):
        self.model = model

    @property
    def name(self):
        return self.model._meta.model_name

    def to_array(self):
        from ..utils import from_query_sets
        objects = self.model.objects.all()
        if len(objects) == 0:
            return []
        else:
            column_names = sorted([field.attname for field in self.model._meta.concrete_fields])
            return from_query_sets(column_names, objects)


class DjangoBookReader(BookReaderBase):
    """Read from a list of django models
    """
    def __init__(self, models):
        self.my_sheets = OrderedDict()
        for model in models:
            djangomodelreader = DjangoModelReader(model)
            self.my_sheets[djangomodelreader.name]=djangomodelreader.to_array()
            
    def sheets(self):
        return self.my_sheets


class DjangoModelWriter(SheetWriter):
    def __init__(self, model, batch_size=None):
        self.batch_size = batch_size
        self.mymodel = None
        self.column_names = None
        self.mapdict = None
        self.initializer = None

        self.mymodel, self.column_names, self.mapdict, self.initializer = model

        if self.initializer is None:
            self.initializer = lambda row: row
        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None
        elif isinstance(self.mapdict, dict):
            self.column_names = [self.mapdict[name] for name in self.column_names]

        self.objs = []

    def set_sheet_name(self, name):
        pass
        
    def write_row(self, array):
        self.objs.append(self.mymodel(**dict(zip(self.column_names, self.initializer(array)))))

    def close(self):
        self.mymodel.objects.bulk_create(self.objs, batch_size=self.batch_size)


class DjangoBookWriter(BookWriter):
    """Write to alist of tables
    """
    def __init__(self, file, models=None, batch_size=None, **keywords):
        BookWriter.__init__(self, file, **keywords)
        self.models = models
        self.batch_size = batch_size

    def create_sheet(self, name):
        model_params = self.models[name]
        return DjangoModelWriter(model_params, batch_size=self.batch_size)

    def close(self):
        pass

class SingleSheetQuerySetSource(ReadOnlySource):
    fields = [KEYWORD_COLUMN_NAMES, KEYWORD_QUERY_SETS]

    def __init__(self, column_names, query_sets, sheet_name=None):
        self.sheet_name = sheet_name
        if self.sheet_name is None:
            self.sheet_name = DEFAULT_SHEET_NAME
        self.column_names = column_names
        self.query_sets = query_sets

    def get_data(self):
        return self.sheet_name, from_query_sets(self.column_names, self.query_sets)


class SingleSheetDatabaseSourceMixin(Source):
    def get_sql_book():
        pass

    def get_writer(self, sheet):
        pass
        
    def get_data(self):
        sql_book = self.get_sql_book()
        sheets = sql_book.sheets()
        return one_sheet_tuple(sheets.items())

    def write_data(self, sheet):
        if(len(sheet.colnames)) == 0:
            sheet.name_columns_by_row(0)
        w = self.get_writer(sheet)
        w.write_array(sheet.array)
        w.close()


class SingleSheetSQLAlchemySource(SingleSheetDatabaseSourceMixin):
    fields = [KEYWORD_SESSION, KEYWORD_TABLE]

    def __init__(self, session, table, **keywords):
        self.session = session
        self.table = table
        self.keywords = keywords

    def get_sql_book(self):
        return load_file(FILE_FORMAT_SQL,
                         session=self.session,
                         tables=[self.table])

    def get_writer(self, sheet):
        from ..writers import Writer
        tables = {
            sheet.name: (self.table,
                         sheet.colnames,
                         self.keywords.get(KEYWORD_MAPDICT, None),
                         self.keywords.get(KEYWORD_INITIALIZER, None)
                     )
        }
        w = Writer(
            FILE_FORMAT_SQL,
            sheet_name=sheet.name,
            session=self.session,
            tables=tables
        )
        return w


class SingleSheetDjangoSource(SingleSheetDatabaseSourceMixin):
    fields = [KEYWORD_MODEL]

    def __init__(self, model=None, **keywords):
        self.model = model
        self.keywords = keywords

    def get_sql_book(self):
        return load_file(FILE_FORMAT_DJANGO, models=[self.model])

    def get_writer(self, sheet):
        from ..writers import Writer
        models = {
            sheet.name:(
                self.model,
                sheet.colnames,
                self.keywords.get(KEYWORD_MAPDICT, None),
                self.keywords.get(KEYWORD_INITIALIZER, None)
            )
        }
        w = Writer(
            FILE_FORMAT_DJANGO,
            sheet_name=sheet.name,
            models=models,
            batch_size=self.keywords.get(KEYWORD_BATCH_SIZE, None)
        )
        return w

class BookSQLSource(Source):
    fields = [KEYWORD_SESSION, KEYWORD_TABLES]
    
    def __init__(self, session, tables, **keywords):
        self.session = session
        self.tables = tables
        self.keywords = keywords

    def get_data(self):
        book = load_file(FILE_FORMAT_SQL, session=self.session, tables=self.tables)
        return book.sheets(), FILE_FORMAT_SQL, None
        
    def write_data(self, book):
        from ..writers import BookWriter
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


class BookDjangoSource(Source):
    fields = [KEYWORD_MODELS]
    
    def __init__(self, models, **keywords):
        self.models = models
        self.keywords = keywords

    def get_data(self):
        book = load_file(FILE_FORMAT_DJANGO, models=self.models)
        return book.sheets(), FILE_FORMAT_DJANGO, None

    def write_data(self, book):
        from ..writers import BookWriter
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
