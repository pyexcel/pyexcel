"""
    pyexcel.internal
    ~~~~~~~~~~~~~~~~~~~

    Second level abstraction

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.internal.common import PyexcelPluginManager


class IOPluginManager(PyexcelPluginManager):
    """Generic plugin manager for renderer and parser
    """
    def __init__(self, name):
        PyexcelPluginManager.__init__(self, name)
        self.loaded_registry = {}

    def get_a_plugin(self, file_type=None):
        """get a plugin to handle the file type
        """
        PyexcelPluginManager.get_a_plugin(self, file_type=file_type)
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

    def register_a_plugin(self, plugin_cls, plugin_info):
        """register loaded plugin classes"""
        __file_types = []
        PyexcelPluginManager.register_a_plugin(self, plugin_cls)
        for file_type in plugin_info.keywords():
            __file_types.append(file_type)
            self.loaded_registry[file_type] = plugin_cls
