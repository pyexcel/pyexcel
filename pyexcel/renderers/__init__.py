# flake8: noqa
import logging


from .factory import renderer_registry, soft_renderer_registry, pre_register, preload_a_renderer
from . import _texttable, _excel, _database
from pkgutil import iter_modules

log = logging.getLogger(__name__)


black_list = ['pyexcel_io', 'pyexcel_webio',
              'pyexcel_xlsx', 'pyexcel_xls',
              'pyexcel_ods3', 'pyexcel_ods',
              'pyexcel_odsr', 'pyexcel_xlsxw']


for _, module_name, ispkg in iter_modules():
    if module_name in black_list:
        continue

    if ispkg and module_name.startswith('pyexcel_'):
        try:
            plugin = __import__(module_name)
            if hasattr(plugin, '__pyexcel_renderer_plugins__'):
                for meta in plugin.__pyexcel_renderer_plugins__:
                    #__import__("%s.%s" % (module_name, p))
                    pre_register(meta, module_name)
        except Exception as e:
            log.info("Failed to import %s due to %s" % (module_name, str(e)),
                     exc_info=True)
            continue


def get_renderer(file_type):
    __file_type = None
    if file_type:
        __file_type = file_type.lower()
    preload_a_renderer(file_type)
    renderer_class = renderer_registry.get(__file_type)
    if renderer_class is None:
        raise Exception("No renderer found for %s" % file_type)
    return renderer_class(__file_type)


def get_all_file_types():
    return renderer_registry.keys() + soft_renderer_registry.keys()