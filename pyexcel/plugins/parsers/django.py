"""
    pyexcel.plugin.parsers.django
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into database datables

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel_io.database.exporters.django as django
from pyexcel_io import get_data

from pyexcel.parser import DbParser


class DjangoExporter(DbParser):
    """Export data from django model"""
    def parse_db(self, argument,
                 export_columns_list=None, **keywords):
        models = argument
        exporter = django.DjangoModelExporter()
        if export_columns_list is None:
            export_columns_list = [None] * len(models)
        for model, export_columns in zip(models, export_columns_list):
            adapter = django.DjangoModelExportAdapter(model, export_columns)
            exporter.append(adapter)
        sheets = get_data(exporter, streaming=True,
                          file_type=self._file_type, **keywords)
        return sheets
