from pyexcel.parsers.factory import Parser
from pyexcel_io import get_data, manager
from pyexcel_io.utils import AVAILABLE_READERS


class ExcelParser(Parser):
    file_types = (list(manager.reader_factories.keys()) +
                  list(AVAILABLE_READERS.keys()))

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
