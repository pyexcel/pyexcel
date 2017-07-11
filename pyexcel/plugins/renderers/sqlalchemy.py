"""
    pyexcel.plugin.renderers.sqlalchemy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into database datables

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import save_data
import pyexcel_io.database.common as sql

from pyexcel._compact import OrderedDict
from pyexcel.internal.generators import SheetStream, BookStream
from pyexcel.renderer import DbRenderer


NO_COLUMN_NAMES = "Only sheet with column names is accepted"


class SQLAlchemyRenderer(DbRenderer):
    """Import data into database"""
    def render_sheet_to_stream(self, file_stream, sheet,
                               init=None, mapdict=None, **keywords):
        if isinstance(sheet, SheetStream):
            headers = next(sheet.payload)
        else:
            headers = sheet.colnames
        if len(headers) == 0:
            raise Exception(NO_COLUMN_NAMES)
        importer = sql.SQLTableImporter(file_stream[0])
        adapter = sql.SQLTableImportAdapter(file_stream[1])
        adapter.column_names = headers
        adapter.row_initializer = init
        adapter.column_name_mapping_dict = mapdict
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.get_internal_array()},
                  file_type=self._file_type, **keywords)

    def render_book_to_stream(self, file_stream, book,
                              inits=None, mapdicts=None, **keywords):
        session, tables = file_stream
        thebook = book
        if isinstance(book, BookStream):
            colnames_array = [next(sheet.payload) for sheet in book]
        else:
            for sheet in thebook:
                if len(sheet.colnames) == 0:
                    sheet.name_columns_by_row(0)
            colnames_array = [sheet.colnames for sheet in book]
        initializers = inits
        if initializers is None:
            initializers = [None] * len(tables)
        if mapdicts is None:
            mapdicts = [None] * len(tables)
        scattered = zip(tables, colnames_array, mapdicts, initializers)

        importer = sql.SQLTableImporter(session)
        for each_table in scattered:
            adapter = sql.SQLTableImportAdapter(each_table[0])
            adapter.column_names = each_table[1]
            adapter.column_name_mapping_dict = each_table[2]
            adapter.row_initializer = each_table[3]
            importer.append(adapter)
        to_store = OrderedDict()
        for sheet in thebook:
            # due book.to_dict() brings in column_names
            # which corrupts the data
            to_store[sheet.name] = sheet.get_internal_array()
        save_data(importer, to_store, file_type=self._file_type, **keywords)
