"""
    pyexcel.internal.source_plugin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Second level abstraction

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from itertools import product
from collections import defaultdict

from lml.manager import PluginManager

import pyexcel_io.constants as io_constants

import pyexcel.constants as constants
import pyexcel.exceptions as exceptions
from pyexcel.internal.attributes import register_an_attribute


REGISTRY_KEY_FORMAT = "%s-%s"
# ignore the following attributes
NO_DOT_NOTATION = (io_constants.DB_DJANGO, io_constants.DB_SQL)

SHEET_WRITE = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.WRITE_ACTION)
SHEET_READ = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.READ_ACTION)
BOOK_WRITE = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.WRITE_ACTION)
BOOK_READ = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.READ_ACTION)


class SourcePluginManager(PluginManager):
    def __init__(self):
        PluginManager.__init__(self, 'source')
        self.registry = defaultdict(list)
        self.loaded_registry = {
            SHEET_WRITE: [],
            BOOK_WRITE: [],
            BOOK_READ: [],
            SHEET_READ: []
        }
        self.keywords = {}

    def load_me_later(self, plugin_meta, module_name):
        PluginManager.load_me_later(self, plugin_meta, module_name)
        if not isinstance(plugin_meta, dict):
            plugin = module_name.replace('_', '-')
            raise exceptions.UpgradePlugin(constants.MESSAGE_UPGRADE % plugin)
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
        PluginManager.load_me_now(self, key, **keywords)
        selected_source = None
        action = key.split('-')[-1]
        for source in self.registry[key]:
            if match_potential_source(source, action, **keywords):
                self.dynamic_load_library(source['path'])
                selected_source = source
                break

        if selected_source:
            self.registry[key].remove(selected_source)

    def dynamic_load_library(self, library_import_path):
        return PluginManager.dynamic_load_library(self, [library_import_path])

    def register_class_meta(self, meta):
        self._register_a_plugin(
            meta["targets"], meta["actions"],
            meta["attributes"], meta.get('key'))

    def register_a_plugin(self, plugin_cls):
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
        key = "%s-%s" % (target, action)
        self.load_me_now(key, **keywords)
        key = REGISTRY_KEY_FORMAT % (target, action)
        for source_cls in self.loaded_registry[key]:
            if source_cls.is_my_business(action, **keywords):
                s = source_cls(**keywords)
                self._logger.info("Found %s for %s" % (s, key))
                return s

        _error_handler(target, action, **keywords)

    def get_source(self, **keywords):
        return self.get_a_plugin(
            constants.SHEET, constants.READ_ACTION, **keywords)

    def get_book_source(self, **keywords):
        return self.get_a_plugin(
            constants.BOOK, constants.READ_ACTION, **keywords)

    def get_writable_source(self, **keywords):
        return self.get_a_plugin(
            constants.SHEET, constants.WRITE_ACTION, **keywords)

    def get_writable_book_source(self, **keywords):
        return self.get_a_plugin(
            constants.BOOK, constants.WRITE_ACTION, **keywords)

    def get_keyword_for_parameter(self, key):
        return self.keywords.get(key, None)


def _error_handler(target, action, **keywords):
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


def match_potential_source(source_meta, action, **keywords):
    """
    If all required keys are present, this source is activated
    """
    statuses = [_has_field(field, keywords) for field in source_meta['fields']]
    results = [status for status in statuses if status is False]
    return len(results) == 0


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None
