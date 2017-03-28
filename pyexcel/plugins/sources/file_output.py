"""
    pyexcel.plugins.sources.file_output
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of output file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel.renderers as renderers
from .file_sources import (
    OutputSource,
    _find_file_type_from_file_name)
import pyexcel.constants as constants
from . import params


class WriteSheetToFile(OutputSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (constants.SHEET,)
    actions = (constants.WRITE_ACTION,)

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
    targets = (constants.BOOK,)

    def write_data(self, book):
        self._renderer.render_book_to_file(self._file_name, book,
                                           **self._keywords)
