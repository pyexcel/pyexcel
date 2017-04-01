"""
    pyexcel.parser
    ~~~~~~~~~~~~~~~~~~~

    Extract tabular data from external file, stream or content

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import with_metaclass
from pyexcel.internal.parser_meta import MetaForParserRegistryOnly


class Parser(with_metaclass(MetaForParserRegistryOnly, object)):
    """
    Parsing data from tabular data such as excel file
    """
    file_types = []

    def __init__(self, file_type):
        self._file_type = file_type

    def parse_file(self, file_name, **keywords):
        """
        Parse data from a physical file
        """
        raise NotImplementedError("parse_file is not implemented")

    def parse_file_stream(self, file_stream, **keywords):
        """
        Parse data from a file stream
        """
        raise NotImplementedError("parse_file_stream is not implemented")

    def parse_file_content(self, file_content, **keywords):
        """
        Parse data from a given file content
        """
        raise NotImplementedError("parse_file_content is not implemented")
