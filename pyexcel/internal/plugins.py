"""
    pyexcel.internal.plugins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Renderer and parser plugin manager

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from lml.plugin import PluginManager


class IOPluginManager(PluginManager):
    """Generic plugin manager for renderer and parser
    """
    def __init__(self, name):
        PluginManager.__init__(self, name)

    def get_a_plugin(self, file_type=None, library=None):
        """get a plugin to handle the file type
        """
        PluginManager.get_a_plugin(
            self, file_type=file_type, library=library)
        __file_type = None
        if file_type:
            __file_type = file_type.lower()
        plugin_cls = self.load_me_now(file_type, library=library)

        return plugin_cls(__file_type)

    def get_all_file_types(self):
        """get all supported file types
        """
        file_types = list(self.registry.keys())
        return file_types


RENDERER = IOPluginManager('renderer')
PARSER = IOPluginManager('parser')
