"""
    pyexcel.internal.source_plugin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Second level abstraction

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from itertools import product

import pyexcel_io.constants as io_constants

import pyexcel.constants as constants
import pyexcel.exceptions as exceptions
from pyexcel.internal.attributes import register_an_attribute
from lml.plugin import PluginManager, Plugin


REGISTRY_KEY_FORMAT = "%s-%s"
# ignore the following attributes
NO_DOT_NOTATION = (io_constants.DB_DJANGO, io_constants.DB_SQL)

SHEET_WRITE = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.WRITE_ACTION)
SHEET_READ = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.READ_ACTION)
BOOK_WRITE = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.WRITE_ACTION)
BOOK_READ = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.READ_ACTION)


class SourcePluginManager(PluginManager):
    """Data source plugin loader"""

    def __init__(self):
        PluginManager.__init__(self, 'source')
        self.keywords = {}

    def load_me_later(self, plugin_info):
        PluginManager.load_me_later(self, plugin_info)
        self.register_class_meta(plugin_info)

    def load_me_now(self, key, action=None, **keywords):
        """get source module into memory for use"""
        self._logger.debug("load me now:" + key)
        plugin = None
        for source in self.registry[key]:
            if source.is_my_business(action, **keywords):
                if isinstance(source, Plugin):
                    plugin = source
                else:
                    cls = self.dynamic_load_library(source)
                    plugin = cls
                break
        else:
            # nothing is found
            _error_handler(action, **keywords)
        return plugin

    def register_class_meta(self, meta):
        """register sheet and book attributes even though
        the plugins will be loaded later

        If this is missing, dot attribute will get
        triggered.
        """
        self._register_a_plugin(
            meta.targets, meta.actions,
            meta.attributes, meta.key)

    def register_a_plugin(self, plugin_cls, plugin_info):
        """ for dynamically loaded plugin """
        PluginManager.register_a_plugin(self, plugin_cls)
        self._register_a_plugin(plugin_info.targets,
                                plugin_info.actions,
                                plugin_info.attributes,
                                plugin_info.key)
        for key in plugin_info.keywords():
            self._logger.debug(key)
            self.registry[key].append(plugin_cls)

    def _register_a_plugin(self, targets, actions, attributes, key):
        debug_registry = "Source registry: "
        debug_attribute = "Instance attribute: "
        anything = False
        for target, action in product(targets, actions):
            if not isinstance(attributes, list):
                attributes = attributes()
            for attr in attributes:
                if attr in NO_DOT_NOTATION:
                    continue
                register_an_attribute(target, action, attr)
                debug_attribute += "%s " % attr
                self.keywords[attr] = key
                anything = True
            debug_attribute += ", "
        if anything:
            self._logger.debug(debug_attribute)
            self._logger.debug(debug_registry)

    def get_a_plugin(self, target=None, action=None, **keywords):
        """obtain a source plugin for pyexcel signature functions"""
        PluginManager.get_a_plugin(self, target=target,
                                   action=action, **keywords)
        key = REGISTRY_KEY_FORMAT % (target, action)
        source_cls = self.load_me_now(key, action=action, **keywords)
        source_instance = source_cls(**keywords)
        return source_instance

    def get_source(self, **keywords):
        """obtain a sheet read source plugin for pyexcel signature functions"""
        return self.get_a_plugin(
            target=constants.SHEET,
            action=constants.READ_ACTION,
            **keywords)

    def get_book_source(self, **keywords):
        """obtain a book read source plugin for pyexcel signature functions"""
        return self.get_a_plugin(
            target=constants.BOOK,
            action=constants.READ_ACTION,
            **keywords)

    def get_writable_source(self, **keywords):
        """obtain a sheet write source plugin for pyexcel signature functions
        """
        return self.get_a_plugin(
            target=constants.SHEET,
            action=constants.WRITE_ACTION,
            **keywords)

    def get_writable_book_source(self, **keywords):
        """obtain a book write source plugin for pyexcel signature functions"""
        return self.get_a_plugin(
            target=constants.BOOK,
            action=constants.WRITE_ACTION,
            **keywords)

    def get_keyword_for_parameter(self, key):
        """custom keyword for an attribute"""
        return self.keywords.get(key, None)


def _error_handler(action, **keywords):
    if keywords:
        file_type = keywords.get('file_type', None)
        if file_type:
            raise exceptions.FileTypeNotSupported(
                constants.FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))
        else:
            msg = "Please check if there were typos in "
            msg += "function parameters: %s. Otherwise "
            msg += "unrecognized parameters were given."
            raise exceptions.UnknownParameters(msg % keywords)
    else:
        raise exceptions.UnknownParameters("No parameters found!")


SOURCE = SourcePluginManager()
