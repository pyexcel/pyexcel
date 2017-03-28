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
attribute_registry = {
    constants.SHEET: {
        constants.READ_ACTION: set(),
        constants.WRITE_ACTION: set(),
        constants.RW_ACTION: set()
    },
    constants.BOOK: {
        constants.READ_ACTION: set(),
        constants.WRITE_ACTION: set(),
        constants.RW_ACTION: set()
    }
}
keywords = {}


class UnknownParameters(Exception):
    pass


class FileTypeNotSupported(Exception):
    pass


def register_an_attribute(target, action, attr):
    if attr in attribute_registry[target][constants.RW_ACTION]:
        # No registration required
        return
    log.debug("%s-%s for %s" % (target, action, attr))
    attribute_registry[target][action].add(attr)
    intersection = (attr in attribute_registry[target][constants.READ_ACTION]
                    and
                    attr in attribute_registry[target][constants.WRITE_ACTION])
    if intersection:
        attribute_registry[target][constants.RW_ACTION].add(attr)
        attribute_registry[target][constants.READ_ACTION].remove(attr)
        attribute_registry[target][constants.WRITE_ACTION].remove(attr)


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


def get_book_rw_attributes():
    return attribute_registry[constants.BOOK][constants.RW_ACTION]


def get_book_w_attributes():
    return attribute_registry[constants.BOOK][constants.WRITE_ACTION]


def get_book_r_attributes():
    return attribute_registry[constants.BOOK][constants.READ_ACTION]


def get_sheet_rw_attributes():
    return attribute_registry[constants.SHEET][constants.RW_ACTION]


def get_sheet_w_attributes():
    return attribute_registry[constants.SHEET][constants.WRITE_ACTION]


def get_sheet_r_attributes():
    return attribute_registry[constants.SHEET][constants.READ_ACTION]


def debug_source_registries():
    print("Source registry:")
    print(registry)
    print("Attribute registry:")
    print(attribute_registry)
