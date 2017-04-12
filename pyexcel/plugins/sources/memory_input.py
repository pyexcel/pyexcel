"""
    pyexcel.plugins.sources.memory_input
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of input file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import pyexcel.constants as constants
from pyexcel.internal import PARSER
from . import params
from .file_sources import InputSource


class ReadExcelFileMemory(InputSource):
    """Pick up 'file_type' and read a sheet from memory"""
    fields = [params.FILE_TYPE]
    targets = (constants.SHEET, constants.BOOK)
    actions = (constants.READ_ACTION,)
    attributes = PARSER.get_all_file_types()
    key = params.FILE_TYPE

    def __init__(self,
                 file_content=None,
                 file_type=None,
                 file_stream=None,
                 **keywords):
        self.__file_type = file_type
        self.__file_stream = file_stream
        self.__file_content = file_content
        self.__parser = PARSER.get_a_plugin(file_type)
        InputSource.__init__(self, **keywords)

    def get_data(self):
        if self.__file_stream is not None:
            sheets = self.__parser.parse_file_stream(
                self.__file_stream,
                **self._keywords)
        else:
            sheets = self.__parser.parse_file_content(
                self.__file_content,
                **self._keywords)
        return sheets

    def get_source_info(self):
        return params.MEMORY, None
