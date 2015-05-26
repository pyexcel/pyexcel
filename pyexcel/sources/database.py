"""
    pyexcel.sources.database
    ~~~~~~~~~~~~~~~~~~~

    Representation of database sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from .base import ReadOnlySource, Source, one_sheet_tuple
from pyexcel_io import DB_SQL, DB_DJANGO, load_data
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


class SheetQuerySetSource(ReadOnlySource):
    fields = [KEYWORD_COLUMN_NAMES, KEYWORD_QUERY_SETS]

    def __init__(self, column_names, query_sets, sheet_name=None):
        self.sheet_name = sheet_name
        if self.sheet_name is None:
            self.sheet_name = DEFAULT_SHEET_NAME
        self.column_names = column_names
        self.query_sets = query_sets

    def get_data(self):
        from ..utils import from_query_sets
        return (self.sheet_name,
                from_query_sets(self.column_names, self.query_sets))


class SheetDatabaseSourceMixin(Source):
    def get_sql_book():
        pass

    def get_writer(self, sheet):
        pass

    def get_data(self):
        sheets = self.get_sql_book()
        return one_sheet_tuple(sheets.items())

    def write_data(self, sheet):
        if(len(sheet.colnames)) == 0:
            sheet.name_columns_by_row(0)
        w = self.get_writer(sheet)
        w.write_array(sheet.array)
        w.close()


class SheetSQLAlchemySource(SheetDatabaseSourceMixin):
    fields = [KEYWORD_SESSION, KEYWORD_TABLE]

    def __init__(self, session, table, **keywords):
        self.session = session
        self.table = table
        self.keywords = keywords

    def get_sql_book(self):
        return load_data(DB_SQL,
                         session=self.session,
                         tables=[self.table])

    def get_writer(self, sheet):
        from ..writers import Writer
        tables = {
            sheet.name: (
                self.table,
                sheet.colnames,
                self.keywords.get(KEYWORD_MAPDICT, None),
                self.keywords.get(KEYWORD_INITIALIZER, None)
            )
        }
        w = Writer(
            DB_SQL,
            sheet_name=sheet.name,
            session=self.session,
            tables=tables
        )
        return w


class SheetDjangoSource(SheetDatabaseSourceMixin):
    fields = [KEYWORD_MODEL]

    def __init__(self, model=None, **keywords):
        self.model = model
        self.keywords = keywords

    def get_sql_book(self):
        return load_data(DB_DJANGO, models=[self.model])

    def get_writer(self, sheet):
        from ..writers import Writer
        models = {
            sheet.name: (
                self.model,
                sheet.colnames,
                self.keywords.get(KEYWORD_MAPDICT, None),
                self.keywords.get(KEYWORD_INITIALIZER, None)
            )
        }
        w = Writer(
            DB_DJANGO,
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
        sheets = load_data(DB_SQL, session=self.session, tables=self.tables)
        return sheets, DB_SQL, None

    def write_data(self, book):
        from ..writers import BookWriter
        initializers = self.keywords.get(KEYWORD_INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(self.tables)
        mapdicts = self.keywords.get(KEYWORD_MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(self.tables)
        for sheet in book:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.tables, colnames_array, mapdicts, initializers)
        table_dict = dict(zip(book.name_array, x))
        w = BookWriter(DB_SQL, session=self.session, tables=table_dict)
        w.write_book_reader_to_db(book)
        w.close()


class BookDjangoSource(Source):
    fields = [KEYWORD_MODELS]

    def __init__(self, models, **keywords):
        self.models = models
        self.keywords = keywords

    def get_data(self):
        sheets = load_data(DB_DJANGO, models=self.models)
        return sheets, DB_DJANGO, None

    def write_data(self, book):
        from ..writers import BookWriter
        batch_size = self.keywords.get(KEYWORD_BATCH_SIZE, None)
        initializers = self.keywords.get(KEYWORD_INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(self.models)
        mapdicts = self.keywords.get(KEYWORD_MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(self.models)
        for sheet in book:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.models, colnames_array, mapdicts, initializers)
        table_dict = dict(zip(book.name_array, x))
        w = BookWriter(DB_DJANGO, models=table_dict, batch_size=batch_size)
        w.write_book_reader_to_db(book)
        w.close()
