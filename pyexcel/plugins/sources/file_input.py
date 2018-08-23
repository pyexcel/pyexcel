"""
    pyexcel.plugins.sources.file_input
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of input file sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import os

from pyexcel.internal import PARSER
from pyexcel.source import AbstractSource


# pylint: disable=W0223
class ReadExcelFromFile(AbstractSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    def __init__(self, file_name=None, parser_library=None,
                 file_type=None, **keywords):
        self.__file_name = file_name

        if file_type is None:
            file_type = self.__file_name.split('.')[-1]
            keywords['file_type'] = file_type
        self.__parser = PARSER.get_a_plugin(file_type, parser_library)
        AbstractSource.__init__(self, **keywords)

    def get_source_info(self):
        path, file_name = os.path.split(self.__file_name)
        return file_name, path

    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        sheets = self.__parser.parse_file(self.__file_name, **self._keywords)
        return sheets
