from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel_io import save_data
import pyexcel_io.manager as manager
from pyexcel_io.utils import AVAILABLE_WRITERS
from pyexcel_io.constants import DB_SQL, DB_DJANGO

from pyexcel.renderers import Renderer


def get_excel_formats():
    all_formats = set(tuple(AVAILABLE_WRITERS.keys()) +
                      tuple(manager.get_writers()))
    all_formats = all_formats.difference(set([DB_SQL, DB_DJANGO]))
    return all_formats


class ExcelRenderer(Renderer):

    file_types = get_excel_formats()

    def get_io(self):
        return manager.get_io(self._file_type)

    def render_sheet_to_file(self, file_name, sheet, **keywords):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(file_name, data, **keywords)

    def render_book_to_file(self, file_name, book, **keywords):
        save_data(file_name, book.to_dict(), **keywords)

    def render_sheet_to_stream(self, file_stream, sheet, **keywords):
        self.render_sheet_to_file(
            file_stream, sheet, file_type=self._file_type, **keywords)

    def render_book_to_stream(self, file_stream, book, **keywords):
        self.render_book_to_file(
            file_stream, book, file_type=self._file_type, **keywords)
