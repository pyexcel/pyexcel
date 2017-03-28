from pyexcel._compact import with_metaclass
from pyexcel.internal.parser_meta import MetaForParserRegistryOnly


class Parser(with_metaclass(MetaForParserRegistryOnly, object)):
    file_types = []

    def __init__(self, file_type):
        self._file_type = file_type

    def parse_file(self, file_name, **keywords):
        raise NotImplementedError("parse_file is not implemented")

    def parse_file_stream(self, file_stream, **keywords):
        raise NotImplementedError("parse_file_stream is not implemented")

    def parse_file_content(self, file_content, **keywords):
        raise NotImplementedError("parse_file_content is not implemented")
