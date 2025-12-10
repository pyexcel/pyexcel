"""
pyexcel.internal.plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~

Renderer and parser plugin manager

:copyright: (c) 2015-2025 by Onni Software Ltd.
:license: New BSD License
"""

from lml.plugin import PluginManager


class IOPluginManager(PluginManager):
    """Generic plugin manager for renderer and parser"""

    def get_a_plugin(self, key, library=None):
        """get a plugin to handle the file type"""
        file_type = None
        if key:
            file_type = key.lower()
        plugin_cls = self.load_me_now(file_type, library=library)

        return plugin_cls(file_type)

    def get_all_file_types(self):
        """get all supported file types"""
        file_types = list(self.registry.keys())
        return file_types


RENDERER = IOPluginManager("renderer")
PARSER = IOPluginManager("parser")
