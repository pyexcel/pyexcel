"""
    pyexcel.sources.file_source_input
    ~~~~~~~~~~~~~~~~~~~

    Representation of input file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import os

from . import params
from pyexcel.sources.factory import InputSource
import pyexcel.parsers as parsers


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
