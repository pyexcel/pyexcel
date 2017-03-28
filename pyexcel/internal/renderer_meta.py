import logging

from pyexcel.internal import soft_renderer_registry, preload_a_plugin
from pyexcel._compact import PY2


log = logging.getLogger(__name__)
renderer_registry = {}


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


def _register_renderer(renderer_cls):
    __file_types = []
    for file_type in set(renderer_cls.file_types):
        __file_types.append(file_type)
        renderer_registry[file_type] = renderer_cls
    log.debug("%s: %s" % (",".join(__file_types), renderer_cls))


class MetaForRendererRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForRendererRegistryOnly, cls).__init__(
            name, bases, nmspc)
        _register_renderer(cls)
