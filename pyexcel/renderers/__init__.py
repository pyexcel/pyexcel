# flake8: noqa
import logging


from .factory import renderer_registry
from . import _texttable, _excel
from pkgutil import iter_modules


log = logging.getLogger(__name__)


black_list = ['pyexcel_io', 'pyexcel_webio',
              'pyexcel_xlsx',
              'pyexcel_ods3', 'pyexcel_ods',
              'pyexcel_odsr', 'pyexcel_xlsxw']

for _, module_name, ispkg in iter_modules():
    if module_name in black_list:
        continue

    if ispkg and module_name.startswith('pyexcel_'):
        try:
            plugin = __import__(module_name)
            if hasattr(plugin, '__pyexcel_renderer_plugins__'):
                for p in plugin.__pyexcel_renderer_plugins__:
                    __import__("%s.%s" % (module_name, p))
        except ImportError as e:
            log.info("Failed to import %s due to %s" % (module_name, str(e)),
                     exc_info=True)
            continue


def get_renderer(file_type):
    __file_type = None
    if file_type:
        __file_type = file_type.lower()
    renderer_class = renderer_registry.get(__file_type)
    return renderer_class(__file_type)


def get_all_file_types():
    return renderer_registry.keys()