"""
    pyexcel.internal
    ~~~~~~~~~~~~~~~~~~~

    Second level abstraction

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import types

from pyexcel.internal.common import PyexcelPluginManager


class IOPluginManager(PyexcelPluginManager):
    """Generic plugin manager for renderer and parser
    """
    def __init__(self, name):
        PyexcelPluginManager.__init__(self, name)
        self.loaded_registry = {}

    def load_me_later(self, plugin_meta, module_name):
        """map each file type against its supporting module
        """
        PyexcelPluginManager.load_me_later(self, plugin_meta, module_name)
        library_import_path = "%s.%s" % (module_name, plugin_meta['submodule'])
        file_types = plugin_meta['file_types']
        if isinstance(file_types, types.FunctionType):
            file_types = file_types()
        for file_type in file_types:
            self.registry[file_type].append(
                (library_import_path, plugin_meta['submodule']))

    def load_me_now(self, key, **keywords):
        """load the corresponding supporting module for each file type
        """
        PyexcelPluginManager.load_me_now(self, key, **keywords)
        __key = key.lower()
        if __key in self.registry:
            for path in self.registry[__key]:
                self.dynamic_load_library(path)
            # once loaded, forgot it
            self.registry.pop(__key)

    def get_a_plugin(self, file_type):
        """get a plugin to handle the file type
        """
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
        """get all supported file types
        """
        file_types = (list(self.registry.keys()) +
                      list(self.loaded_registry.keys()))
        return file_types

    def register_a_plugin(self, plugin_cls):
        """register loaded plugin classes"""
        __file_types = []
        PyexcelPluginManager.register_a_plugin(self, plugin_cls)
        for file_type in plugin_cls.file_types:
            __file_types.append(file_type)
            self.loaded_registry[file_type] = plugin_cls
