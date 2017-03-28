"""
    pyexcel.sources.factory
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Data source registration

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import logging
from functools import partial
from itertools import product

from pyexcel_io.constants import DB_DJANGO, DB_SQL

from pyexcel._compact import with_metaclass
from pyexcel.internal import preload_a_source, debug_registries
from pyexcel.internal.attributes import register_an_attribute
import pyexcel.constants as constants


log = logging.getLogger(__name__)
# ignore the following attributes
NO_DOT_NOTATION = (DB_DJANGO, DB_SQL)
# registries
REGISTRY_KEY_FORMAT = "%s-%s"

SHEET_WRITE = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.WRITE_ACTION)
SHEET_READ = REGISTRY_KEY_FORMAT % (constants.SHEET, constants.READ_ACTION)
BOOK_WRITE = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.WRITE_ACTION)
BOOK_READ = REGISTRY_KEY_FORMAT % (constants.BOOK, constants.READ_ACTION)

registry = {
    SHEET_WRITE: [],
    BOOK_WRITE: [],
    BOOK_READ: [],
    SHEET_READ: []
}
keywords = {}


class UnknownParameters(Exception):
    pass


class FileTypeNotSupported(Exception):
    pass


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
            keywords[attr] = meta['key']
            anything = True
        debug_attribute += ", "
    if anything:
        log.debug("Preload class meta: ==>")
        log.debug(debug_attribute)
        log.debug(debug_registry)


def register_class(cls):
    debug_registry = "Source registry: "
    debug_attribute = "Instance attribute: "
    anything = False
    for target, action in product(cls.targets, cls.actions):
        key = REGISTRY_KEY_FORMAT % (target, action)
        registry[key].append(cls)
        debug_registry += "%s -> %s, " % (key, cls)
        debug_attribute += "%s -> " % key
        for attr in cls.attributes:
            if attr in NO_DOT_NOTATION:
                continue
            register_an_attribute(target, action, attr)
            debug_attribute += "%s " % attr
            keywords[attr] = cls.key
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


class Source(with_metaclass(MetaForSourceRegistryOnly, object)):
    """ A command source for get_sheet, get_book, save_as and save_book_as

    This can be used to extend the function parameters once the custom
    class inherit this and register it with corresponding source registry
    """
    fields = [constants.SOURCE]
    attributes = []
    targets = []
    actions = []
    key = constants.SOURCE

    def __init__(self, source=None, **keywords):
        self.__source = source
        self.__keywords = keywords

    def get_source_info(self):
        return (None, None)

    @classmethod
    def is_my_business(cls, action, **keywords):
        """
        If all required keys are present, this source is activated
        """
        statuses = [_has_field(field, keywords) for field in cls.fields]
        results = [status for status in statuses if status is False]
        return len(results) == 0

    def write_data(self, content):
        raise NotImplementedError("")

    def get_data(self):
        raise NotImplementedError("")

    def get_internal_stream(self):
        raise NotImplementedError("")


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


def _get_generic_source(target, action, **keywords):
    preload_a_source(target, action, **keywords)
    key = REGISTRY_KEY_FORMAT % (target, action)
    for source in registry[key]:
        if source.is_my_business(action, **keywords):
            s = source(**keywords)
            log.info("Found %s for %s" % (s, key))
            return s

    _error_handler(target, action, **keywords)


def _error_handler(target, action, **keywords):
    if keywords:
        file_type = keywords.get('file_type', None)
        if file_type:
            raise FileTypeNotSupported(
                constants.FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))
        else:
            debug_registries()
            debug_source_registries()
            msg = "Please check if there were typos in "
            msg += "function parameters: %s. Otherwise "
            msg += "unrecognized parameters were given."
            raise UnknownParameters(msg % keywords)
    else:
        raise UnknownParameters("No parameters found!")


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
    print(registry)

