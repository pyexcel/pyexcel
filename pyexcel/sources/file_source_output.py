"""
    pyexcel.sources.file_source_output
    ~~~~~~~~~~~~~~~~~~~

    Representation of output file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel.renderers as renderers
from pyexcel.sources.factory import (
    FileSource, supported_write_file_types,
    _find_file_type_from_file_name)
from pyexcel.sources import params


class OutputSource(FileSource):
    """
    Get excel data from file source
    """
    attributes = supported_write_file_types()
    key = params.FILE_TYPE

    @classmethod
    def can_i_handle(cls, action, file_type):
        if action == params.WRITE_ACTION:
            status = file_type.lower() in tuple(
                renderers.get_all_file_types())
        else:
            status = False
        return status


class WriteSheetToFile(OutputSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_name=None, **keywords):
        self._keywords = keywords
        self._file_name = file_name

        self.__file_type = _find_file_type_from_file_name(file_name, 'write')
        self._renderer = renderers.get_renderer(self.__file_type)

    def write_data(self, sheet):
        self._renderer.render_sheet_to_file(self._file_name,
                                            sheet, **self._keywords)


class WriteBookToFile(WriteSheetToFile):
    """Pick up 'file_name' field and do multiple sheet based read and write
    """
    targets = (params.BOOK,)

    def write_data(self, book):
        self._renderer.render_book_to_file(self._file_name, book,
                                           **self._keywords)


class WriteSheetToMemory(OutputSource):
    fields = [params.FILE_TYPE]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)

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
    targets = (params.BOOK,)

    def write_data(self, book):
        self._renderer.render_book_to_stream(self._content, book,
                                             **self._keywords)
