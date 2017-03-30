"""
    pyexcel.plugins.sources.sqlalchemy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of sqlalchemy sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.constants import DB_SQL
from pyexcel.source import Source
import pyexcel.internal.renderer_meta as renderers
import pyexcel.internal.parser_meta as parsers
import pyexcel.constants as constants
from . import params
from ._shared import _set_dictionary_key


class SheetSQLAlchemySource(Source):
    """
    SQLAlchemy channeled sql database as data source
    """
    fields = [params.SESSION, params.TABLE]
    targets = (constants.SHEET,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)
    attributes = []

    def __init__(self, session, table, export_columns=None,
                 sheet_name=None, **keywords):
        self.__session = session
        self.__table = table
        self.__export_columns = export_columns
        self.__sheet_name = sheet_name
        Source.__init__(self, **keywords)

    def get_data(self):
        parser = parsers.get_parser(DB_SQL)
        data = parser.parse_file_stream(
            (self.__session, [self.__table]),
            export_columns_list=[self.__export_columns],
            **self._keywords)
        if self.__sheet_name is not None:
            _set_dictionary_key(data, self.__sheet_name)
        return data

    def write_data(self, sheet):
        render = renderers.get_renderer(DB_SQL)
        if params.INITIALIZER in self._keywords:
            init_func = self._keywords.pop(params.INITIALIZER)
        else:
            init_func = None
        if params.MAPDICT in self._keywords:
            map_dict = self._keywords.pop(params.MAPDICT)
        else:
            map_dict = None

        render.render_sheet_to_stream(
            (self.__session, self.__table),
            sheet,
            init=init_func,
            mapdict=map_dict,
            **self._keywords)


class BookSQLSource(Source):
    """
    SQLAlchemy bridged multiple table data source
    """
    fields = [params.SESSION, params.TABLES]
    targets = (constants.BOOK,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)
    attributes = []

    def __init__(self, session, tables, **keywords):
        self.__session = session
        self.__tables = tables
        Source.__init__(self, **keywords)

    def get_data(self):
        parser = parsers.get_parser(DB_SQL)
        data = parser.parse_file_stream(
            (self.__session, self.__tables),
            **self._keywords)
        return data

    def get_source_info(self):
        return DB_SQL, None

    def write_data(self, book):
        render = renderers.get_renderer(DB_SQL)
        if params.INITIALIZERS in self._keywords:
            init_funcs = self._keywords.pop(params.INITIALIZERS)
        else:
            init_funcs = None
        if params.MAPDICTS in self._keywords:
            map_dicts = self._keywords.pop(params.MAPDICTS)
        else:
            map_dicts = None

        render.render_book_to_stream(
            (self.__session, self.__tables),
            book,
            inits=init_funcs,
            mapdicts=map_dicts,
            **self._keywords)
