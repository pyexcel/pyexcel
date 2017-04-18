"""
    pyexcel.plugins.parsers.excel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parsing excel sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.parser import AbstractParser
from pyexcel_io import get_data
from pyexcel_io.plugins import readers


class ExcelParser(AbstractParser):
    """get data from excel files"""
    file_types = readers.get_all_formats()

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
