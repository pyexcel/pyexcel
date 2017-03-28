"""
    pyexcel.plugins.sources.django
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of django sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.constants import DB_DJANGO

from pyexcel.source import Source
import pyexcel.internal.renderer_meta as renderers
import pyexcel.internal.parser_meta as parsers
import pyexcel.constants as constants
from . import params
from ._shared import _set_dictionary_key


NO_COLUMN_NAMES = "Only sheet with column names is accepted"


class SheetDjangoSource(Source):
    """
    Django model as data source
    """
    fields = [params.MODEL]
    targets = (constants.SHEET,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)
    attributes = []

    def __init__(self, model=None, export_columns=None, sheet_name=None,
                 **keywords):
        self.__model = model
        self.__export_columns = export_columns
        self.__sheet_name = sheet_name
        self.__keywords = keywords

    def get_data(self):
        parser = parsers.get_parser(DB_DJANGO)
        data = parser.parse_file_stream(
            [self.__model],
            export_columns_list=[self.__export_columns],
            **self.__keywords)
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


class BookDjangoSource(Source):
    """
    multiple Django table as data source
    """
    fields = [params.MODELS]
    targets = (constants.BOOK,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)

    def __init__(self, models, **keywords):
        self.__models = models
        self.__keywords = keywords

    def get_data(self):
        parser = parsers.get_parser(DB_DJANGO)
        data = parser.parse_file_stream(self.__models,
                                        **self.__keywords)
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
