"""
    pyexcel.sources.database
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of database sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import get_data
from pyexcel_io.constants import DB_SQL, DB_DJANGO
import pyexcel_io.database.sql as sql
import pyexcel_io.database.django as django
from pyexcel_io.database.querysets import QuerysetsReader

from pyexcel._compact import PY2
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.sources.factory import Source
import pyexcel.renderers as renderers
from . import params


NO_COLUMN_NAMES = "Only sheet with column names is accepted"


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
        render = renderers.get_renderer(DB_SQL)
        if params.INITIALIZER in self.__keywords:
            init_func = self.__keywords.pop(params.INITIALIZER)
        else:
            init_func = None
        if params.MAPDICT in self.__keywords:
            map_dict = self.__keywords.pop(params.MAPDICT)
        else:
            map_dict = None

        render.render_sheet_to_stream(
            (self.__session, self.__table),
            sheet,
            init=init_func,
            mapdict=map_dict,
            **self.__keywords)


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
        render = renderers.get_renderer(DB_DJANGO)
        if params.INITIALIZER in self.__keywords:
            init_func = self.__keywords.pop(params.INITIALIZER)
        else:
            init_func = None
        if params.MAPDICT in self.__keywords:
            map_dict = self.__keywords.pop(params.MAPDICT)
        else:
            map_dict = None

        render.render_sheet_to_stream(
            self.__model,
            sheet,
            init=init_func,
            mapdict=map_dict,
            **self.__keywords)


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

    def write_data(self, book):
        render = renderers.get_renderer(DB_SQL)
        if params.INITIALIZERS in self.__keywords:
            init_funcs = self.__keywords.pop(params.INITIALIZERS)
        else:
            init_funcs = None
        if params.MAPDICTS in self.__keywords:
            map_dicts = self.__keywords.pop(params.MAPDICTS)
        else:
            map_dicts = None

        render.render_book_to_stream(
            (self.__session, self.__tables),
            book,
            inits=init_funcs,
            mapdicts=map_dicts,
            **self.__keywords)


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

    def write_data(self, book):
        render = renderers.get_renderer(DB_DJANGO)
        if params.INITIALIZERS in self.__keywords:
            init_funcs = self.__keywords.pop(params.INITIALIZERS)
        else:
            init_funcs = None
        if params.MAPDICTS in self.__keywords:
            map_dicts = self.__keywords.pop(params.MAPDICTS)
        else:
            map_dicts = None
        render.render_book_to_stream(
            self.__models,
            book,
            inits=init_funcs,
            mapdicts=map_dicts,
            **self.__keywords)


def _set_dictionary_key(adict, sheet_name):
    if PY2:
        (old_sheet_name, array) = adict.items()[0]
    else:
        (old_sheet_name, array) = list(adict.items())[0]
    adict[sheet_name] = array
    adict.pop(old_sheet_name)
