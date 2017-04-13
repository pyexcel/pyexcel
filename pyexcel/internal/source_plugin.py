"""
    pyexcel.internal.source_plugin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Second level abstraction

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from itertools import product
from collections import defaultdict

import pyexcel_io.constants as io_constants

import pyexcel.constants as constants
import pyexcel.exceptions as exceptions
from pyexcel.internal.attributes import register_an_attribute
from pyexcel.internal.common import PyexcelPluginManager


REGISTRY_KEY_FORMAT = "%s-%s"
# ignore the following attributes
NO_DOT_NOTATION = (io_constants.DB_DJANGO, io_constants.DB_SQL)

SHEET_WRITE = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.WRITE_ACTION)
SHEET_READ = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.READ_ACTION)
BOOK_WRITE = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.WRITE_ACTION)
BOOK_READ = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.READ_ACTION)


class SourcePluginManager(PyexcelPluginManager):
    """Data source plugin loader"""

    def __init__(self):
        PyexcelPluginManager.__init__(self, 'source')
        self.registry = defaultdict(list)
        self.loaded_registry = {
            SHEET_WRITE: [],
            BOOK_WRITE: [],
            BOOK_READ: [],
            SHEET_READ: []
        }
        self.keywords = {}

    def load_me_later(self, plugin_meta, module_name):
        """map each source with its loading requirements"""
        PyexcelPluginManager.load_me_later(self, plugin_meta, module_name)
        self.register_class_meta(plugin_meta)
        library_import_path = "%s.%s" % (module_name, plugin_meta['submodule'])
        target_action_list = product(
            plugin_meta['targets'], plugin_meta['actions'])
        for target, action in target_action_list:
            key = "%s-%s" % (target, action)
            self.registry[key].append(dict(
                fields=plugin_meta['fields'],
                path=library_import_path,
                submodule=plugin_meta['submodule']
            ))

    def load_me_now(self, key, **keywords):
        """get source module into memory for use"""
        PyexcelPluginManager.load_me_now(self, key, **keywords)
        selected_source = None
        for source in self.registry[key]:
            if match_potential_source(source, **keywords):
                self.dynamic_load_library(source['path'])
                selected_source = source
                break

        if selected_source:
            self.registry[key].remove(selected_source)

    def dynamic_load_library(self, library_import_path):
        """custom import a module
        """
        return PyexcelPluginManager.dynamic_load_library(
            self, [library_import_path])

    def register_class_meta(self, meta):
        """register sheet and book attributes even though
        the plugins will be loaded later

        If this is missing, dot attribute will get
        triggered.
        """
        self._register_a_plugin(
            meta["targets"], meta["actions"],
            meta["attributes"], meta.get('key'))

    def register_a_plugin(self, plugin_cls):
        """register a source plugin after it is imported"""
        PyexcelPluginManager.register_a_plugin(self, plugin_cls)
        self._register_a_plugin(plugin_cls.targets,
                                plugin_cls.actions,
                                plugin_cls.attributes,
                                plugin_cls.key)
        for target, action in product(plugin_cls.targets, plugin_cls.actions):
            key = REGISTRY_KEY_FORMAT % (target, action)
            self.loaded_registry[key].append(plugin_cls)

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

    def get_a_plugin(self, target, action, **keywords):
        """obtain a source plugin for pyexcel signature functions"""
        key = "%s-%s" % (target, action)
        self.load_me_now(key, **keywords)
        key = REGISTRY_KEY_FORMAT % (target, action)
        for source_cls in self.loaded_registry[key]:
            if source_cls.is_my_business(action, **keywords):
                source_instance = source_cls(**keywords)
                self._logger.info(
                    "Found %s for %s" % (str(source_instance), key))
                return source_instance

        _error_handler(action, **keywords)

    def get_source(self, **keywords):
        """obtain a sheet read source plugin for pyexcel signature functions"""
        return self.get_a_plugin(
            constants.SHEET, constants.READ_ACTION, **keywords)

    def get_book_source(self, **keywords):
        """obtain a book read source plugin for pyexcel signature functions"""
        return self.get_a_plugin(
            constants.BOOK, constants.READ_ACTION, **keywords)

    def get_writable_source(self, **keywords):
        """obtain a sheet write source plugin for pyexcel signature functions
        """
        return self.get_a_plugin(
            constants.SHEET, constants.WRITE_ACTION, **keywords)

    def get_writable_book_source(self, **keywords):
        """obtain a book write source plugin for pyexcel signature functions"""
        return self.get_a_plugin(
            constants.BOOK, constants.WRITE_ACTION, **keywords)

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


def match_potential_source(source_meta, **keywords):
    """
    If all required keys are present, this source is activated
    """
    statuses = [_has_field(field, keywords) for field in source_meta['fields']]
    results = [status for status in statuses if status is False]
    return len(results) == 0


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None
