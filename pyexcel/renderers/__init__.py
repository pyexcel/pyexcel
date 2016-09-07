# flake8: noqa
from . import _texttable, _excel
from .factory import renderer_registry

try:
    import pyexcel_text as text
except ImportError as e:
    pass


def get_renderer(file_type):
    renderer_class = renderer_registry.get(file_type)
    return renderer_class(file_type)


def get_all_file_types():
    return renderer_registry.keys()