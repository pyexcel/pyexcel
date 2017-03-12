"""
    pyexcel.sources.file_source_input
    ~~~~~~~~~~~~~~~~~~~

    Representation of input file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import os

from pyexcel.sources import params
from pyexcel.sources.factory import FileSource, supported_read_file_types
import pyexcel.parsers as parsers


class InputSource(FileSource):
    """
    Get excel data from file source
    """
    @classmethod
    def can_i_handle(cls, action, file_type):
        __file_type = None
        if file_type:
            __file_type = file_type.lower()
        if action == params.READ_ACTION:
            status = __file_type in supported_read_file_types()
        else:
            status = False
        return status


class ReadExcelFromFile(InputSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (params.SHEET, params.BOOK)
    actions = (params.READ_ACTION,)

    def __init__(self, file_name=None, **keywords):
        self.__file_name = file_name

        file_type = self.__file_name.split('.')[-1]
        self.__parser = parsers.get_parser(file_type)
        self.__keywords = keywords

    def get_source_info(self):
        path, file_name = os.path.split(self.__file_name)
        return file_name, path

    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        sheets = self.__parser.parse_file(self.__file_name, **self.__keywords)
        return sheets


class ReadExcelFileMemory(InputSource):
    """Pick up 'file_type' and read a sheet from memory"""
    fields = [params.FILE_TYPE]
    targets = (params.SHEET, params.BOOK)
    actions = (params.READ_ACTION,)
    attributes = parsers.get_all_file_types()
    key = params.FILE_TYPE

    def __init__(self,
                 file_content=None,
                 file_type=None,
                 file_stream=None,
                 **keywords):
        self.__file_type = file_type
        self.__file_stream = file_stream
        self.__file_content = file_content
        self.__keywords = keywords
        self.__parser = parsers.get_parser(file_type)

    def get_data(self):
        if self.__file_stream is not None:
            sheets = self.__parser.parse_file_stream(
                self.__file_stream,
                **self.__keywords)
        else:
            sheets = self.__parser.parse_file_content(
                self.__file_content,
                **self.__keywords)
        return sheets

    def get_source_info(self):
        return params.MEMORY, None
