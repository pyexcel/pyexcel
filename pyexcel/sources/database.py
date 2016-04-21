"""
    pyexcel.sources.database
    ~~~~~~~~~~~~~~~~~~~

    Representation of database sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import DB_SQL, DB_DJANGO, load_data, get_writer

from .._compact import OrderedDict
from ..constants import DEFAULT_SHEET_NAME

from .base import ReadOnlySource, Source, one_sheet_tuple
from . import params


class SheetQuerySetSource(ReadOnlySource):
    """
    Database query set as data source

    SQLAlchemy and Django query sets are supported
    """
    fields = [params.COLUMN_NAMES, params.QUERY_SETS]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

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
    """
    Generic database source

    It does the general data import and export.

    Please note that name_columns_by_row, or name_rows_by_column
    should be specified prior to writing
    """
    def get_sql_book():
        pass

    def get_writer(self, sheet):
        pass

    def get_data(self):
        sheets = self.get_sql_book()
        return one_sheet_tuple(sheets.items())

    def write_data(self, sheet):
        w = self.get_writer(sheet)
        raw_sheet = w.create_sheet(sheet.name)
        raw_sheet.write_array(sheet.array)
        raw_sheet.close()
        w.close()


class SheetSQLAlchemySource(SheetDatabaseSourceMixin):
    """
    SQLAlchemy channeled sql database as data source
    """
    fields = [params.SESSION, params.TABLE]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, session, table, **keywords):
        self.session = session
        self.table = table
        self.keywords = keywords

    def get_sql_book(self):
        return load_data(DB_SQL,
                         session=self.session,
                         tables=[self.table])

    def get_writer(self, sheet):
        headers = sheet.colnames
        if len(headers) == 0:
            headers = sheet.rownames
        tables = {
            sheet.name: (
                self.table,
                headers,
                self.keywords.get(params.MAPDICT, None),
                self.keywords.get(params.INITIALIZER, None)
            )
        }
        w = get_writer(
            DB_SQL,
            single_sheet_in_book=True,
            session=self.session,
            tables=tables,
            **self.keywords
        )
        return w


class SheetDjangoSource(SheetDatabaseSourceMixin):
    """
    Django model as data source
    """
    fields = [params.MODEL]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, model=None, **keywords):
        self.model = model
        self.keywords = keywords

    def get_sql_book(self):
        return load_data(DB_DJANGO, models=[self.model])

    def get_writer(self, sheet):
        headers = sheet.colnames
        if len(headers) == 0:
            headers = sheet.rownames
        models = {
            sheet.name: (
                self.model,
                headers,
                self.keywords.get(params.MAPDICT, None),
                self.keywords.get(params.INITIALIZER, None)
            )
        }
        w = get_writer(
            DB_DJANGO,
            single_sheet_in_book=True,
            models=models,
            batch_size=self.keywords.get(params.BATCH_SIZE, None)
        )
        return w


def _write_book(writer, book):
    the_dict = OrderedDict()
    keys = book.sheet_names()
    for name in keys:
        the_dict.update({name: book[name].array})
    writer.write(the_dict)
    writer.close()


class BookSQLSource(Source):
    """
    SQLAlchemy bridged multiple table data source
    """
    fields = [params.SESSION, params.TABLES]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, session, tables, **keywords):
        self.session = session
        self.tables = tables
        self.keywords = keywords

    def get_data(self):
        sheets = load_data(DB_SQL,
                           session=self.session,
                           tables=self.tables)
        return sheets, DB_SQL, None

    def write_data(self, book):
        initializers = self.keywords.get(params.INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(self.tables)
        mapdicts = self.keywords.get(params.MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(self.tables)
        for sheet in book:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(self.tables, colnames_array, mapdicts, initializers)
        table_dict = dict(zip(book.name_array, x))
        writer = get_writer(DB_SQL,
                            session=self.session,
                            tables=table_dict,
                            **self.keywords)
        _write_book(writer, book)


class BookDjangoSource(Source):
    """
    multiple Django table as data source
    """
    fields = [params.MODELS]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, models, **keywords):
        self.models = models
        self.keywords = keywords

    def get_data(self):
        sheets = load_data(DB_DJANGO, models=self.models)
        return sheets, DB_DJANGO, None

    def write_data(self, book):
        new_models = [model for model in self.models if model is not None]
        batch_size = self.keywords.get(params.BATCH_SIZE, None)
        initializers = self.keywords.get(params.INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(new_models)
        mapdicts = self.keywords.get(params.MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(new_models)
        for sheet in book:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        x = zip(new_models, colnames_array, mapdicts, initializers)
        table_dict = dict(zip(book.name_array, x))
        writer = get_writer(DB_DJANGO,
                            models=table_dict,
                            batch_size=batch_size)
        _write_book(writer, book)


sources = (
    SheetSQLAlchemySource, SheetDjangoSource, SheetQuerySetSource,
    BookDjangoSource, BookSQLSource
)

