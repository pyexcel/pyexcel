"""
    pyexcel.plugin.renderers.django
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into django models

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import save_data
import pyexcel_io.database.common as django

from pyexcel._compact import OrderedDict
from pyexcel.internal.generators import BookStream
from pyexcel.renderer import DbRenderer


NO_COLUMN_NAMES = "Only sheet with column names is accepted"


class DjangoRenderer(DbRenderer):
    """Import data into database"""
    def render_sheet_to_stream(self, model, sheet, init=None, mapdict=None,
                               **keywords):
        headers = sheet.colnames
        if len(headers) == 0:
            raise Exception(NO_COLUMN_NAMES)
        importer = django.DjangoModelImporter()
        adapter = django.DjangoModelImportAdapter(model)
        adapter.column_names = headers
        adapter.column_name_mapping_dict = mapdict
        adapter.row_initializer = init
        importer.append(adapter)
        save_data(importer, {adapter.get_name(): sheet.get_internal_array()},
                  file_type=self._file_type, **keywords)

    def render_book_to_stream(self, models, thebook,
                              inits=None, mapdicts=None,
                              batch_size=None, **keywords):
        from pyexcel.book import to_book
        book = thebook
        if isinstance(thebook, BookStream):
            book = to_book(thebook)
        new_models = [model for model in models if model is not None]
        initializers = inits
        if initializers is None:
            initializers = [None] * len(new_models)
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
        save_data(importer, to_store, file_type=self._file_type,
                  batch_size=batch_size, **keywords)
