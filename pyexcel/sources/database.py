"""
    pyexcel.sources.database
    ~~~~~~~~~~~~~~~~~~~

    Representation of database sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import get_data, save_data
from pyexcel_io.constants import DB_SQL, DB_DJANGO
from pyexcel_io.database.sql import SQLTableImporter, SQLTableImportAdapter
from pyexcel_io.database.sql import SQLTableExporter, SQLTableExportAdapter
from pyexcel_io.database.django import DjangoModelExporter, DjangoModelExportAdapter
from pyexcel_io.database.django import DjangoModelImporter, DjangoModelImportAdapter
from pyexcel_io.utils import from_query_sets

from pyexcel._compact import OrderedDict
from pyexcel.constants import DEFAULT_SHEET_NAME

from pyexcel.factory import ReadOnlySource, Source
from pyexcel import params


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
        return {self.sheet_name:
                from_query_sets(self.column_names, self.query_sets)}


class SheetSQLAlchemySource(Source):
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

    def get_data(self):
        exporter = SQLTableExporter(self.session)
        adapter = SQLTableExportAdapter(self.table)
        exporter.append(adapter)
        data = get_data(exporter, file_type=DB_SQL)
        return data

    def write_data(self, sheet):
        headers = sheet.colnames
        if len(headers) == 0:
            headers = sheet.rownames
        importer = SQLTableImporter(self.session)
        adapter = SQLTableImportAdapter(self.table)
        adapter.column_names = headers
        adapter.row_initializer = self.keywords.get(params.INITIALIZER, None)
        adapter.column_name_mapping_dict = self.keywords.get(params.MAPDICT, None)
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.array}, file_type=DB_SQL, **self.keywords)


class SheetDjangoSource(Source):
    """
    Django model as data source
    """
    fields = [params.MODEL]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, model=None, **keywords):
        self.model = model
        self.keywords = keywords

    def get_data(self):
        exporter = DjangoModelExporter()
        adapter = DjangoModelExportAdapter(self.model)
        exporter.append(adapter)
        data = get_data(exporter, file_type=DB_DJANGO, **self.keywords)
        return data

    def write_data(self, sheet):
        headers = sheet.colnames
        if len(headers) == 0:
            headers = sheet.rownames
        importer = DjangoModelImporter()
        adapter = DjangoModelImportAdapter(self.model)
        adapter.set_column_names(headers)
        adapter.set_column_name_mapping_dict(self.keywords.get(params.MAPDICT, None))
        adapter.set_row_initializer(self.keywords.get(params.INITIALIZER, None))
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.array}, file_type=DB_DJANGO, **self.keywords)


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
        exporter = SQLTableExporter(self.session)
        for table in self.tables:
            adapter = SQLTableExportAdapter(table)
            exporter.append(adapter)
        data = get_data(exporter, file_type=DB_SQL, **self.keywords)
        return data

    def get_source_info(self):
        return DB_SQL, None

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
        scattered = zip(self.tables, colnames_array, mapdicts, initializers)

        importer = SQLTableImporter(self.session)
        for each_table in scattered:
            adapter = SQLTableImportAdapter(each_table[0])
            adapter.column_names = each_table[1]
            adapter.column_name_mapping_dict = each_table[2]
            adapter.row_initializer = each_table[3]
            importer.append(adapter)
        to_store = OrderedDict()
        for sheet_name in book.sheet_names():
            # due book.to_dict() brings in column_names
            # which corrupts the data
            to_store[sheet_name] = book[sheet_name].array
        save_data(importer, to_store, file_type=DB_SQL, **self.keywords)


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
        exporter = DjangoModelExporter()
        for model in self.models:
            adapter = DjangoModelExportAdapter(model)
            exporter.append(adapter)
        data = get_data(exporter, file_type=DB_DJANGO, **self.keywords)
        return data

    def get_source_info(self):
        return DB_DJANGO, None

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
        scattered = zip(new_models, colnames_array, mapdicts, initializers)

        importer = DjangoModelImporter()
        for each_model in scattered:
            adapter = DjangoModelImportAdapter(each_model[0])
            adapter.set_column_names(each_model[1])
            adapter.set_column_name_mapping_dict(each_model[2])
            adapter.set_row_initializer(each_model[3])
            importer.append(adapter)
        to_store = OrderedDict()
        for sheet_name in book.sheet_names():
            # due book.to_dict() brings in column_names
            # which corrupts the data
            to_store[sheet_name] = book[sheet_name].array
        save_data(importer, to_store, file_type=DB_DJANGO,
                  batch_size=batch_size)


sources = (
    SheetSQLAlchemySource, SheetDjangoSource, SheetQuerySetSource,
    BookDjangoSource, BookSQLSource
)

