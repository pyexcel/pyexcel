"""
    pyexcel.plugin.parsers.django
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into database datables

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.parser import Parser
from pyexcel_io.constants import DB_DJANGO
import pyexcel_io.database.django as django
from pyexcel_io import get_data


class DjangoExporter(Parser):
    file_types = [DB_DJANGO]

    def parse_file_stream(self, file_stream,
                          export_columns_list=None, **keywords):
        models = file_stream
        exporter = django.DjangoModelExporter()
        if export_columns_list is None:
            export_columns_list = [None] * len(models)
        for model, export_columns in zip(models, export_columns_list):
            adapter = django.DjangoModelExportAdapter(model, export_columns)
            exporter.append(adapter)
        sheets = get_data(exporter, streaming=True,
                          file_type=self._file_type, **keywords)
        return sheets
