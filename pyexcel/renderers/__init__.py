# flake8: noqa
from . import _texttable, _excel
try:
    import pyexcel_text as text
except ImportError as e:
    print("Failed to import pyexcel_text due to %s" % e)
    pass
from .factory import renderer_registry


def get_renderer(file_type):
    renderer_class = renderer_registry.get(file_type)
    return renderer_class(file_type)


def get_all_file_types():
    return renderer_registry.keys()