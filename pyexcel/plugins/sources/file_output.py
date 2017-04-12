"""
    pyexcel.plugins.sources.file_output
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of output file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.internal import RENDERER
from .file_sources import (
    OutputSource,
    _find_file_type_from_file_name)
import pyexcel.constants as constants
from . import params


# pylint: disable=W0223
class WriteSheetToFile(OutputSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (constants.SHEET,)
    actions = (constants.WRITE_ACTION,)

    def __init__(self, file_name=None, **keywords):
        OutputSource.__init__(self, **keywords)
        self._file_name = file_name

        self.__file_type = _find_file_type_from_file_name(file_name, 'write')
        self._renderer = RENDERER.get_a_plugin(self.__file_type)

    def write_data(self, sheet):
        self._renderer.render_sheet_to_file(self._file_name,
                                            sheet, **self._keywords)


# pylint: disable=W0223
class WriteBookToFile(WriteSheetToFile):
    """Pick up 'file_name' field and do multiple sheet based read and write
    """
    targets = (constants.BOOK,)

    def write_data(self, book):
        self._renderer.render_book_to_file(self._file_name, book,
                                           **self._keywords)
