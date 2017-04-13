"""
    pyexcel.parser
    ~~~~~~~~~~~~~~~~~~~

    Extract tabular data from external file, stream or content

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from lml.manager import Plugin, with_metaclass


class Parser(with_metaclass(Plugin, object)):
    """
    Parsing data from tabular data such as excel file
    """
    plugin_type = 'parser'
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


class DbParser(Parser):
    """
    Change interface for db parser
    """
    def parse_file(self, file_name, **keywords):
        raise Exception("parse_file is not supported")

    def parse_file_stream(self, file_stream, **keywords):
        return self.parse_db(file_stream, **keywords)

    def parse_file_content(self, file_content, **keywords):
        raise Exception("parse_file_content is not supported")

    def parse_db(self, argument, **keywords):
        """
        Parse data from database
        """
        raise NotImplementedError("parse_db is not implemented")
