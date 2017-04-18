"""
    pyexcel.plugin.renderers.excel
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Export data into excel files

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import save_data
import pyexcel_io.manager as manager
from pyexcel_io.plugins import writers

from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.renderer import AbstractRenderer


class ExcelRenderer(AbstractRenderer):
    """Output data into excel format"""
    file_types = writers.get_all_formats()

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
