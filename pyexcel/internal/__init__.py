import logging

from pkgutil import iter_modules
from collections import defaultdict
import pyexcel.plugins.parsers as parsers
import pyexcel.plugins.renderers as renderers
from pyexcel.internal.generators import SheetStream, BookStream  # noqa


log = logging.getLogger(__name__)

soft_renderer_registry = defaultdict(list)
soft_parser_registry = defaultdict(list)

UPGRADE_MESSAGE = "Please upgrade the plugin '%s' according to \
plugin compactibility table."


class UpgradePlugin(Exception):
    pass


def pre_register(registry, library_meta, module_name):
    if not isinstance(library_meta, dict):
        plugin = module_name.replace('_', '-')
        raise UpgradePlugin(UPGRADE_MESSAGE % plugin)
    library_import_path = "%s.%s" % (module_name, library_meta['submodule'])
    for file_type in library_meta['file_types']:
        registry[file_type].append(
            (library_import_path, library_meta['submodule']))
    log.debug("pre-register :" + ','.join(library_meta['file_types']))


def dynamic_load_library(library_import_path):
    __import__(library_import_path[0])


def preload_a_plugin(registry, file_type):
    __file_type = file_type.lower()
    if __file_type in registry:
        debug_path = []
        for path in registry[__file_type]:
            dynamic_load_library(path)
            debug_path.append(path)
        log.debug("preload :" + __file_type + ":" + ','.join(path))
        # once loaded, forgot it
        registry.pop(__file_type)


black_list = ['pyexcel_io', 'pyexcel_webio',
              'pyexcel_xlsx', 'pyexcel_xls',
              'pyexcel_ods3', 'pyexcel_ods',
              'pyexcel_odsr', 'pyexcel_xlsxw']


def register_plugins(plugin_metas, module_name):
    for meta in plugin_metas:
        if meta['plugin_type'] == 'renderer':
            pre_register(soft_renderer_registry, meta, module_name)
        elif meta['plugin_type'] == 'parser':
            pre_register(soft_parser_registry, meta, module_name)


for _, module_name, ispkg in iter_modules():
    if module_name in black_list:
        continue

    if ispkg and module_name.startswith('pyexcel_'):
        try:
            plugin = __import__(module_name)
            if hasattr(plugin, '__pyexcel_plugins__'):
                register_plugins(plugin.__pyexcel_plugins__, module_name)
        except Exception as e:
            log.info("Failed to import %s due to %s" % (module_name, str(e)),
                     exc_info=True)
            continue


register_plugins(renderers.__pyexcel_plugins__, renderers.__name__)
register_plugins(parsers.__pyexcel_plugins__, parsers.__name__)
