import logging
from pyexcel._compact import with_metaclass

log = logging.getLogger(__name__)
parser_registry = {}


def _register_parser(parser_cls):
    __file_types = []
    for file_type in parser_cls.file_types:
        __file_types.append(file_type)
        parser_registry[file_type] = parser_cls
    log.debug("%s: %s" % (",".join(__file_types), parser_cls))

class MetaForParserRegistryOnly(type):
    def __init__(cls, name, bases, nmspc):
        super(MetaForParserRegistryOnly, cls).__init__(
            name, bases, nmspc)
        _register_parser(cls)


class Parser(with_metaclass(MetaForParserRegistryOnly, object)):
    file_types = []

    def __init__(self, file_type):
        self._file_type = file_type

    def parse_file(self, file_name, **keywords):
        pass

    def parse_file_stream(self, file_stream, **keywords):
        pass

    def parse_file_content(self, file_content, **keywords):
        pass
