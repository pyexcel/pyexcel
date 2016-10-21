# flake8: noqa
import logging


from .factory import renderer_registry
from . import _texttable, _excel


log = logging.getLogger(__name__)

try:
    import pyexcel_text as text
except ImportError as e:
    log.error("Failed to import pyexcel_text due to %s", exc_info=True)
    pass


def get_renderer(file_type):
    renderer_class = renderer_registry.get(file_type)
    return renderer_class(file_type)


def get_all_file_types():
    return renderer_registry.keys()