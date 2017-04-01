"""
    pyexcel.internal.source_meta
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Source registration and management

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import logging
from functools import partial
from itertools import product

from pyexcel_io.constants import DB_DJANGO, DB_SQL

from pyexcel.internal import preload_a_source, debug_registries
from pyexcel.internal.attributes import register_an_attribute
import pyexcel.constants as constants
import pyexcel.exceptions as exceptions


log = logging.getLogger(__name__)
# ignore the following attributes
NO_DOT_NOTATION = (DB_DJANGO, DB_SQL)
# registries
REGISTRY_KEY_FORMAT = "%s-%s"

SHEET_WRITE = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.WRITE_ACTION)
SHEET_READ = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.READ_ACTION)
BOOK_WRITE = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.WRITE_ACTION)
BOOK_READ = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.READ_ACTION)

REGISTRY = {
    SHEET_WRITE: [],
    BOOK_WRITE: [],
    BOOK_READ: [],
    SHEET_READ: []
}
KEYWORDS = {}


def register_class_meta(meta):
    debug_registry = "Source registry: "
    debug_attribute = "Instance attribute: "
    anything = False
    for target, action in product(meta["targets"], meta["actions"]):
        attributes = meta['attributes']
        if not isinstance(attributes, list):
            attributes = attributes()
        for attr in attributes:
            if attr in NO_DOT_NOTATION:
                continue
            register_an_attribute(target, action, attr)
            debug_attribute += "%s " % attr
            KEYWORDS[attr] = meta['key']
            anything = True
        debug_attribute += ", "
    if anything:
        log.debug(debug_attribute)
        log.debug(debug_registry)


def register_class(cls):
    debug_registry = "Source registry: "
    debug_attribute = "Instance attribute: "
    anything = False
    for target, action in product(cls.targets, cls.actions):
        key = REGISTRY_KEY_FORMAT % (target, action)
        REGISTRY[key].append(cls)
        debug_registry += "%s -> %s, " % (key, cls)
        debug_attribute += "%s -> " % key
        for attr in cls.attributes:
            if attr in NO_DOT_NOTATION:
                continue
            register_an_attribute(target, action, attr)
            debug_attribute += "%s " % attr
            KEYWORDS[attr] = cls.key
            anything = True
        debug_attribute += ", "
    if anything:
        log.debug(debug_registry)
        log.debug(debug_attribute)


class MetaForSourceRegistryOnly(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(MetaForSourceRegistryOnly, cls).__init__(
            name, bases, nmspc)
        register_class(cls)


def _get_generic_source(target, action, **keywords):
    preload_a_source(target, action, **keywords)
    key = REGISTRY_KEY_FORMAT % (target, action)
    for source in REGISTRY[key]:
        if source.is_my_business(action, **keywords):
            s = source(**keywords)
            log.info("Found %s for %s" % (s, key))
            return s

    _error_handler(target, action, **keywords)


def _error_handler(target, action, **keywords):
    if keywords:
        file_type = keywords.get('file_type', None)
        if file_type:
            raise exceptions.FileTypeNotSupported(
                constants.FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))
        else:
            debug_registries()
            debug_source_registries()
            msg = "Please check if there were typos in "
            msg += "function parameters: %s. Otherwise "
            msg += "unrecognized parameters were given."
            raise exceptions.UnknownParameters(msg % keywords)
    else:
        raise exceptions.UnknownParameters("No parameters found!")


get_source = partial(
    _get_generic_source, constants.SHEET, constants.READ_ACTION)

get_book_source = partial(
    _get_generic_source, constants.BOOK, constants.READ_ACTION)

get_writable_source = partial(
    _get_generic_source, constants.SHEET, constants.WRITE_ACTION)

get_writable_book_source = partial(
    _get_generic_source, constants.BOOK, constants.WRITE_ACTION)


def debug_source_registries():
    print("Source registry:")
    print(REGISTRY)


def get_keyword_for_parameter(key):
    return KEYWORDS.get(key, None)
