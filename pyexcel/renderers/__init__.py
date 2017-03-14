from .factory import renderer_registry
from pyexcel.internal import soft_renderer_registry, preload_a_plugin
from . import _texttable, _excel, _database  # noqa
from pyexcel._compact import PY2


def get_renderer(file_type):
    __file_type = None
    if file_type:
        __file_type = file_type.lower()
    preload_a_plugin(soft_renderer_registry, file_type)
    renderer_class = renderer_registry.get(__file_type)
    if renderer_class is None:
        raise Exception("No renderer found for %s" % file_type)
    return renderer_class(__file_type)


def get_all_file_types():
    if PY2:
        file_types = renderer_registry.keys() + soft_renderer_registry.keys()
    else:
        file_types = (list(renderer_registry.keys()) +
                      list(soft_renderer_registry.keys()))
    return file_types
