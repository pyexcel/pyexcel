"""
    pyexcel.plugins.sources.output_to_memory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of output file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel.internal.renderer_meta as renderers
import pyexcel.constants as constants
from .file_sources import OutputSource
from . import params


class WriteSheetToMemory(OutputSource):
    fields = [params.FILE_TYPE]
    targets = (constants.SHEET,)
    actions = (constants.WRITE_ACTION,)
    attributes = renderers.get_all_file_types()

    def __init__(self, file_type=None, file_stream=None, **keywords):
        self._keywords = keywords

        self._renderer = renderers.get_renderer(file_type)
        if file_stream:
            self._content = file_stream
        else:
            self._content = self._renderer.get_io()
        self.attributes = renderers.get_all_file_types()

    def write_data(self, sheet):
        self._renderer.render_sheet_to_stream(self._content,
                                              sheet, **self._keywords)

    def get_internal_stream(self):
        return self._content


class WriteBookToMemory(WriteSheetToMemory):
    """
    Multiple sheet data source for writting back to memory
    """
    targets = (constants.BOOK,)

    def write_data(self, book):
        self._renderer.render_book_to_stream(self._content, book,
                                             **self._keywords)
