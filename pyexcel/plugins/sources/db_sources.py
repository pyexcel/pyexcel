"""
    pyexcel.plugins.sources.db_sources
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Generic database sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel.constants as constants
from pyexcel.source import Source
import pyexcel.internal.renderer_meta as renderers
import pyexcel.internal.parser_meta as parsers
from pyexcel._compact import PY2
from . import params

NO_COLUMN_NAMES = "Only sheet with column names is accepted"


class SheetDbSource(Source):
    """
    SQLAlchemy channeled sql database as data source
    """
    targets = (constants.SHEET,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)
    attributes = []

    def __init__(self, db_type, export_columns=None,
                 sheet_name=None, **keywords):
        self._db_type = db_type
        self.__export_columns = export_columns
        self.__sheet_name = sheet_name
        Source.__init__(self, **keywords)

    def get_data(self):
        parser = parsers.get_parser(self._db_type)
        export_params = self.get_export_params()
        data = parser.parse_file_stream(
            export_params,
            export_columns_list=[self.__export_columns],
            **self._keywords)
        if self.__sheet_name is not None:
            _set_dictionary_key(data, self.__sheet_name)
        return data

    def get_export_params(self):
        pass

    def write_data(self, sheet):
        render = renderers.get_renderer(self._db_type)
        init_func, map_dict = transcode_sheet_db_keywords(
            self._keywords)
        import_params = self.get_import_params()
        render.render_sheet_to_stream(
            import_params,
            sheet,
            init=init_func,
            mapdict=map_dict,
            **self._keywords)

    def get_import_params(self):
        pass


class BookDbSource(Source):
    """
    multiple Django table as data source
    """
    targets = (constants.BOOK,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)

    def __init__(self, db_type, **keywords):
        self.__db_type = db_type
        Source.__init__(self, **keywords)

    def get_data(self):
        parser = parsers.get_parser(self.__db_type)
        export_params = self.get_params()
        data = parser.parse_file_stream(export_params,
                                        **self._keywords)
        return data

    def get_params(self):
        pass

    def get_source_info(self):
        return self.__db_type, None

    def write_data(self, book):
        render = renderers.get_renderer(self.__db_type)
        init_funcs, map_dicts = transcode_book_db_keywords(
            self._keywords)

        import_params = self.get_params()
        render.render_book_to_stream(
            import_params,
            book,
            inits=init_funcs,
            mapdicts=map_dicts,
            **self._keywords)


def _set_dictionary_key(adict, sheet_name):
    if PY2:
        (old_sheet_name, array) = adict.items()[0]
    else:
        (old_sheet_name, array) = list(adict.items())[0]
    adict[sheet_name] = array
    adict.pop(old_sheet_name)


def transcode_sheet_db_keywords(keywords):
    if params.INITIALIZER in keywords:
        init_func = keywords.pop(params.INITIALIZER)
    else:
        init_func = None
    if params.MAPDICT in keywords:
        map_dict = keywords.pop(params.MAPDICT)
    else:
        map_dict = None

    return init_func, map_dict


def transcode_book_db_keywords(keywords):
    if params.INITIALIZERS in keywords:
        init_funcs = keywords.pop(params.INITIALIZERS)
    else:
        init_funcs = None
    if params.MAPDICTS in keywords:
        map_dicts = keywords.pop(params.MAPDICTS)
    else:
        map_dicts = None

    return init_funcs, map_dicts
