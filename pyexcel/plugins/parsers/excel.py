"""
    pyexcel.plugins.parsers.excel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Parsing excel sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.parser import AbstractParser
from pyexcel_io import get_data, iget_data


class ExcelParser(AbstractParser):
    """get data from excel files"""
    def parse_file(self, file_name, on_demand=False, **keywords):
        if on_demand:
            sheets, reader = iget_data(file_name, **keywords)
            self._free_me_up_later(reader)
        else:
            sheets = get_data(file_name, **keywords)
        return sheets

    def parse_file_stream(self, file_stream, on_demand=False, **keywords):
        if on_demand:
            sheets, reader = iget_data(file_stream, file_type=self._file_type,
                                       **keywords)
            self._free_me_up_later(reader)
        else:
            sheets = get_data(
                file_stream, file_type=self._file_type, **keywords)
        return sheets

    def parse_file_content(self, file_content, on_demand=False, **keywords):
        if on_demand:
            sheets, reader = iget_data(
                file_content, file_type=self._file_type, **keywords)
            self._free_me_up_later(reader)
        else:
            sheets = get_data(
                file_content, file_type=self._file_type, **keywords)
        return sheets
