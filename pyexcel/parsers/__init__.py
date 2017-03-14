from .factory import parser_registry
from pyexcel.internal import soft_parser_registry, preload_a_plugin
from . import _excel  # noqa
from . import _database  # noqa


def get_parser(file_type):
    __file_type = None
    if file_type:
        __file_type = file_type.lower()
    preload_a_plugin(soft_parser_registry, file_type)
    parser_class = parser_registry.get(__file_type)
    if parser_class is None:
        raise Exception("No parser is found for %s" % file_type)
    return parser_class(__file_type)


def get_all_file_types():
    return parser_registry.keys() + soft_parser_registry.keys()
