"""
    pyexcel.sources.database
    ~~~~~~~~~~~~~~~~~~~

    Representation of database sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import get_data, save_data
from pyexcel_io.constants import DB_SQL, DB_DJANGO
import pyexcel_io.database.sql as sql
import pyexcel_io.database.django as django
from pyexcel_io.database.querysets import QuerysetsReader

from pyexcel._compact import OrderedDict
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.generators import BookStream
from pyexcel.sources.factory import Source
from . import params


class SheetQuerySetSource(Source):
    """
    Database query set as data source

    SQLAlchemy and Django query sets are supported
    """
    fields = [params.COLUMN_NAMES, params.QUERY_SETS]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)
    attributes = []

    def __init__(self, column_names, query_sets,
                 sheet_name=None, row_renderer=None,
                 start_row=0, row_limit=-1,
                 start_column=None, column_limit=None,
                 skip_row_func=None, skip_column_func=None):
        self.__sheet_name = sheet_name
        if self.__sheet_name is None:
            self.__sheet_name = DEFAULT_SHEET_NAME
        self.__column_names = column_names
        self.__query_sets = query_sets
        self.__row_renderer = row_renderer
        self.__start_row = start_row
        self.__row_limit = row_limit
        self.__skip_row_func = skip_row_func

        if start_column is None:
            print("start_column is ignored")
        if column_limit is None:
            print("column_limit is ignored")
        if skip_column_func is None:
            print("skip_column_func is ignored")

    def get_data(self):
        params = dict(
            row_renderer=self.__row_renderer,
            start_row=self.__start_row,
            row_limit=self.__row_limit
        )
        if self.__skip_row_func is not None:
            params['skip_row_func'] = self.__skip_row_func
        reader = QuerysetsReader(
            self.__query_sets, self.__column_names, **params)
        data = reader.to_array()
        return {self.__sheet_name: data}


class SheetSQLAlchemySource(Source):
    """
    SQLAlchemy channeled sql database as data source
    """
    fields = [params.SESSION, params.TABLE]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = []

    def __init__(self, session, table, export_columns=None,
                 sheet_name=None, **keywords):
        self.__session = session
        self.__table = table
        self.__export_columns = export_columns
        self.__sheet_name = sheet_name
        self.__keywords = keywords

    def get_data(self):
        exporter = sql.SQLTableExporter(self.__session)
        adapter = sql.SQLTableExportAdapter(
            self.__table, self.__export_columns)
        exporter.append(adapter)
        data = get_data(exporter, file_type=DB_SQL)
        if self.__sheet_name is not None:
            _set_dictionary_key(data, self.__sheet_name)
        return data

    def write_data(self, sheet):
        headers = sheet.colnames
        if len(headers) == 0:
            headers = sheet.rownames
        importer = sql.SQLTableImporter(self.__session)
        adapter = sql.SQLTableImportAdapter(self.__table)
        adapter.column_names = headers
        adapter.row_initializer = self.__keywords.get(params.INITIALIZER, None)
        adapter.column_name_mapping_dict = self.__keywords.get(
            params.MAPDICT, None)
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.get_internal_array()},
                  file_type=DB_SQL, **self.__keywords)


class SheetDjangoSource(Source):
    """
    Django model as data source
    """
    fields = [params.MODEL]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = []

    def __init__(self, model=None, export_columns=None, sheet_name=None,
                 **keywords):
        self.__model = model
        self.__export_columns = export_columns
        self.__sheet_name = sheet_name
        self.__keywords = keywords

    def get_data(self):
        exporter = django.DjangoModelExporter()
        adapter = django.DjangoModelExportAdapter(
            self.__model, self.__export_columns)
        exporter.append(adapter)
        data = get_data(exporter, file_type=DB_DJANGO, **self.__keywords)
        if self.__sheet_name is not None:
            _set_dictionary_key(data, self.__sheet_name)
        return data

    def write_data(self, sheet):
        headers = sheet.colnames
        if len(headers) == 0:
            headers = sheet.rownames
        importer = django.DjangoModelImporter()
        adapter = django.DjangoModelImportAdapter(self.__model)
        adapter.column_names = headers
        adapter.column_name_mapping_dict = self.__keywords.get(
            params.MAPDICT, None)
        adapter.row_initializer = self.__keywords.get(params.INITIALIZER, None)
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.get_internal_array()},
                  file_type=DB_DJANGO, **self.__keywords)


class BookSQLSource(Source):
    """
    SQLAlchemy bridged multiple table data source
    """
    fields = [params.SESSION, params.TABLES]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = []

    def __init__(self, session, tables, **keywords):
        self.__session = session
        self.__tables = tables
        self.__keywords = keywords

    def get_data(self):
        exporter = sql.SQLTableExporter(self.__session)
        for table in self.__tables:
            adapter = sql.SQLTableExportAdapter(table)
            exporter.append(adapter)
        data = get_data(exporter, file_type=DB_SQL, **self.__keywords)
        return data

    def get_source_info(self):
        return DB_SQL, None

    def write_data(self, thebook):
        from pyexcel.book import to_book
        book = thebook
        if isinstance(thebook, BookStream):
            book = to_book(thebook)
        initializers = self.__keywords.get(params.INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(self.__tables)
        mapdicts = self.__keywords.get(params.MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(self.__tables)
        for sheet in book:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        scattered = zip(self.__tables, colnames_array, mapdicts, initializers)

        importer = sql.SQLTableImporter(self.__session)
        for each_table in scattered:
            adapter = sql.SQLTableImportAdapter(each_table[0])
            adapter.column_names = each_table[1]
            adapter.column_name_mapping_dict = each_table[2]
            adapter.row_initializer = each_table[3]
            importer.append(adapter)
        to_store = OrderedDict()
        for sheet_name in book.sheet_names():
            # due book.to_dict() brings in column_names
            # which corrupts the data
            to_store[sheet_name] = book[sheet_name].get_internal_array()
        save_data(importer, to_store, file_type=DB_SQL, **self.__keywords)


class BookDjangoSource(Source):
    """
    multiple Django table as data source
    """
    fields = [params.MODELS]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, models, **keywords):
        self.__models = models
        self.__keywords = keywords

    def get_data(self):
        exporter = django.DjangoModelExporter()
        for model in self.__models:
            adapter = django.DjangoModelExportAdapter(model)
            exporter.append(adapter)
        data = get_data(exporter, file_type=DB_DJANGO, **self.__keywords)
        return data

    def get_source_info(self):
        return DB_DJANGO, None

    def write_data(self, thebook):
        from pyexcel.book import to_book
        book = thebook
        if isinstance(thebook, BookStream):
            book = to_book(thebook)
        new_models = [model for model in self.__models if model is not None]
        batch_size = self.__keywords.get(params.BATCH_SIZE, None)
        initializers = self.__keywords.get(params.INITIALIZERS, None)
        if initializers is None:
            initializers = [None] * len(new_models)
        mapdicts = self.__keywords.get(params.MAPDICTS, None)
        if mapdicts is None:
            mapdicts = [None] * len(new_models)
        for sheet in book:
            if len(sheet.colnames) == 0:
                sheet.name_columns_by_row(0)
        colnames_array = [sheet.colnames for sheet in book]
        scattered = zip(new_models, colnames_array, mapdicts, initializers)

        importer = django.DjangoModelImporter()
        for each_model in scattered:
            adapter = django.DjangoModelImportAdapter(each_model[0])
            adapter.column_names = each_model[1]
            adapter.column_name_mapping_dict = each_model[2]
            adapter.row_initializer = each_model[3]
            importer.append(adapter)
        to_store = OrderedDict()
        for sheet_name in book.sheet_names():
            # due book.to_dict() brings in column_names
            # which corrupts the data
            to_store[sheet_name] = book[sheet_name].get_internal_array()
        save_data(importer, to_store, file_type=DB_DJANGO,
                  batch_size=batch_size)


def _set_dictionary_key(adict, sheet_name):
    (old_sheet_name, array), = adict
    adict[sheet_name] = array
    adict.pop(old_sheet_name)
            