"""
pyexcel.plugin.renderers.excel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Export data into excel files

:copyright: (c) 2015-2025 by Onni Software Ltd.
:license: New BSD License
"""

from pyexcel._compact import get_string_file_name
from pyexcel.renderer import AbstractRenderer
from pyexcel.constants import DEFAULT_SHEET_NAME

from pyexcel_io import manager, save_data


class ExcelRenderer(AbstractRenderer):
    """Output data into excel format"""

    def get_io(self):
        return manager.get_io(self._file_type)

    def render_sheet_to_file(self, file_name, sheet, **keywords):
        file_name = get_string_file_name(file_name)
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(file_name, data, **keywords)

    def render_book_to_file(self, file_name, book, **keywords):
        file_name = get_string_file_name(file_name)
        save_data(file_name, book.to_dict(), **keywords)

    def render_sheet_to_stream(self, file_stream, sheet, **keywords):
        self.render_sheet_to_file(
            file_stream,
            sheet,
            file_type=self._file_type,
            **keywords,
        )

    def render_book_to_stream(self, file_stream, book, **keywords):
        self.render_book_to_file(
            file_stream,
            book,
            file_type=self._file_type,
            **keywords,
        )
