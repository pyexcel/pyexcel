"""
    pyexcel.internal
    ~~~~~~~~~~~~~~~~~~~

    Second level abstraction

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import types

from lml.manager import PluginManager

import pyexcel.constants as constants
import pyexcel.exceptions as exceptions


class PyexcelPluginManager(PluginManager):
    def __init__(self, name):
        PluginManager.__init__(self, name)
        self.loaded_registry = {}

    def load_me_later(self, plugin_meta, module_name):
        PluginManager.load_me_later(self, plugin_meta, module_name)
        if not isinstance(plugin_meta, dict):
            plugin = module_name.replace('_', '-')
            raise exceptions.UpgradePlugin(constants.MESSAGE_UPGRADE % plugin)
        library_import_path = "%s.%s" % (module_name, plugin_meta['submodule'])
        file_types = plugin_meta['file_types']
        if isinstance(file_types, types.FunctionType):
            file_types = file_types()
        for file_type in file_types:
            self.registry[file_type].append(
                (library_import_path, plugin_meta['submodule']))

    def load_me_now(self, key, **keywords):
        PluginManager.load_me_now(self, key, **keywords)
        __key = key.lower()
        if __key in self.registry:
            for path in self.registry[__key]:
                self.dynamic_load_library(path)
            # once loaded, forgot it
            self.registry.pop(__key)

    def get_a_plugin(self, file_type):
        __file_type = None
        if file_type:
            __file_type = file_type.lower()
        self.load_me_now(file_type)
        plugin_cls = self.loaded_registry.get(__file_type)
        if plugin_cls is None:
            raise Exception(
                "No %s is found for %s" % (self.name, file_type))
        return plugin_cls(__file_type)

    def get_all_file_types(self):
        file_types = (list(self.registry.keys()) +
                      list(self.loaded_registry.keys()))
        return file_types

    def register_a_plugin(self, plugin_cls):
        __file_types = []
        PluginManager.register_a_plugin(self, plugin_cls)
        for file_type in plugin_cls.file_types:
            __file_types.append(file_type)
            self.loaded_registry[file_type] = plugin_cls
