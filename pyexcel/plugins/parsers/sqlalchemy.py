"""
    pyexcel.plugin.parsers.sqlalchemy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into database datables

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel_io.database.exporters.sqlalchemy as sql
from pyexcel_io import get_data

from pyexcel.parser import DbParser


class SQLAlchemyExporter(DbParser):
    """export data via sqlalchmey"""
    def parse_db(self, argument,
                 export_columns_list=None, **keywords):
        session, tables = argument
        exporter = sql.SQLTableExporter(session)
        if export_columns_list is None:
            export_columns_list = [None] * len(tables)
        for table, export_columns in zip(tables, export_columns_list):
            adapter = sql.SQLTableExportAdapter(table, export_columns)
            exporter.append(adapter)
        sheets = get_data(exporter, streaming=True,
                          file_type=self._file_type, **keywords)
        return sheets
