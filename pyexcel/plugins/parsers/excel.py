"""
    pyexcel.plugins.parsers.excel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parsing excel sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.parser import Parser
from pyexcel_io import get_data, manager
from pyexcel_io.utils import AVAILABLE_READERS
from pyexcel_io.constants import DB_SQL, DB_DJANGO


def get_excel_formats():
    all_formats = set(list(manager.reader_factories.keys()) +
                      list(AVAILABLE_READERS.keys()))
    all_formats = all_formats.difference(set([DB_SQL, DB_DJANGO]))
    return all_formats


class ExcelParser(Parser):
    file_types = get_excel_formats()

    def parse_file(self, file_name, **keywords):
        sheets = get_data(file_name, streaming=True, **keywords)
        return sheets

    def parse_file_stream(self, file_stream, **keywords):
        sheets = get_data(file_stream, file_type=self._file_type,
                          streaming=True, **keywords)
        return sheets

    def parse_file_content(self, file_content, **keywords):
        sheets = get_data(file_content, file_type=self._file_type,
                          streaming=True, **keywords)
        return sheets
