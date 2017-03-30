import logging

from pkgutil import iter_modules
from collections import defaultdict
from pyexcel.internal.generators import SheetStream, BookStream  # noqa
from itertools import product


log = logging.getLogger(__name__)

soft_renderer_registry = defaultdict(list)
soft_parser_registry = defaultdict(list)
soft_source_registry = defaultdict(list)

UPGRADE_MESSAGE = "Please upgrade the plugin '%s' according to \
plugin compactibility table."


def debug_registries():
    print("Unloaded renderers:")
    print(soft_renderer_registry)
    print("Unloaded parsers:")
    print(soft_parser_registry)
    print("Unloaded sources:")
    print(soft_source_registry)


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


def pre_register_source(registry, meta, module_name):
    from .source_meta import register_class_meta
    if not isinstance(meta, dict):
        plugin = module_name.replace('_', '-')
        raise UpgradePlugin(UPGRADE_MESSAGE % plugin)
    register_class_meta(meta)
    library_import_path = "%s.%s" % (module_name, meta['submodule'])
    for target, action in product(meta['targets'], meta['actions']):
        key = "%s-%s" % (target, action)
        registry[key].append(dict(
            fields=meta['fields'],
            path=library_import_path,
            submodule=meta['submodule']
        ))
    log.debug("pre-register source:" + library_import_path)


def dynamic_load_library(library_import_path):
    __import__(library_import_path)


def preload_a_plugin(registry, file_type):
    __file_type = file_type.lower()
    if __file_type in registry:
        debug_path = []
        for path in registry[__file_type]:
            dynamic_load_library(path[0])
            debug_path.append(path)
        log.debug("preload :" + __file_type + ":" + ','.join(path))
        # once loaded, forgot it
        registry.pop(__file_type)


def preload_a_source(target, action, **keywords):
    key = "%s-%s" % (target, action)
    selected_source = None
    for source in soft_source_registry[key]:
        if match_potential_source(source, action, **keywords):
            dynamic_load_library(source['path'])
            selected_source = source
            break

    if selected_source:
        soft_source_registry[key].remove(selected_source)
        log.debug("preload source: %s - %s" % (key, selected_source['path']))


def match_potential_source(source_meta, action, **keywords):
    """
    If all required keys are present, this source is activated
    """
    statuses = [_has_field(field, keywords) for field in source_meta['fields']]
    results = [status for status in statuses if status is False]
    return len(results) == 0


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


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
        elif meta['plugin_type'] == 'source':
            pre_register_source(soft_source_registry, meta, module_name)


def auto_load_plugins():
    for _, module_name, ispkg in iter_modules():
        if module_name in black_list:
            continue

        if ispkg and module_name.startswith('pyexcel_'):
            try:
                pyexcel_plugin = __import__(module_name)
                if hasattr(pyexcel_plugin, '__pyexcel_plugins__'):
                    register_plugins(pyexcel_plugin.__pyexcel_plugins__,
                                     module_name)
            except Exception as e:
                log.info(
                    "Failed to import %s due to %s" % (module_name, str(e)),
                    exc_info=True)
                continue


auto_load_plugins()

import pyexcel.plugins.parsers as parsers  # noqa
import pyexcel.plugins.renderers as renderers  # noqa
import pyexcel.plugins.sources as sources  # noqa

register_plugins(renderers.__pyexcel_plugins__, renderers.__name__)
register_plugins(parsers.__pyexcel_plugins__, parsers.__name__)
register_plugins(sources.__pyexcel_plugins__, sources.__name__)
