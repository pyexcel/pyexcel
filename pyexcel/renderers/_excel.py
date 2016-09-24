from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel_io import save_data, RWManager
from pyexcel_io.utils import AVAILABLE_WRITERS

from .factory import Renderer


class ExcelRenderer(Renderer):

    file_types = (tuple(AVAILABLE_WRITERS) +
                  tuple(RWManager.writer_factories.keys()))

    def get_io(self):
        return RWManager.get_io(self.file_type)

    def render_sheet_to_file(self, file_name, sheet, **keywords):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(file_name,
                  data,
                  **keywords)

    def render_book_to_file(self, file_name, book, **keywords):
        save_data(file_name, book.to_dict(), **keywords)

    def render_sheet_to_stream(self, file_stream, sheet, **keywords):
        self.render_sheet_to_file(file_stream, sheet,
                                  file_type=self.file_type, **keywords)

    def render_book_to_stream(self, file_stream, book, **keywords):
        self.render_book_to_file(file_stream, book,
                                 file_type=self.file_type, **keywords)
