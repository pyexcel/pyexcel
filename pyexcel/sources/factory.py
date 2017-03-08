"""
    pyexcel.sources.factory
    ~~~~~~~~~~~~~~~~~~~

    Data source registration

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import logging
from functools import partial
from itertools import product

from pyexcel_io.constants import DB_SQL, DB_DJANGO
from pyexcel_io.utils import AVAILABLE_READERS
from pyexcel_io import manager

import pyexcel.renderers as renderers
from pyexcel._compact import is_string, with_metaclass
from . import params


log = logging.getLogger(__name__)
# ignore the following attributes
NO_DOT_NOTATION = (DB_DJANGO, DB_SQL)
# registries
REGISTRY_KEY_FORMAT = "%s-%s"
FILE_TYPE_NOT_SUPPORTED_FMT = "File type '%s' is not supported for %s."

SHEET_WRITE = REGISTRY_KEY_FORMAT % (params.SHEET, params.WRITE_ACTION)
SHEET_READ = REGISTRY_KEY_FORMAT % (params.SHEET, params.READ_ACTION)
BOOK_WRITE = REGISTRY_KEY_FORMAT % (params.BOOK, params.WRITE_ACTION)
BOOK_READ = REGISTRY_KEY_FORMAT % (params.BOOK, params.READ_ACTION)

registry = {
    SHEET_WRITE: [],
    BOOK_WRITE: [],
    BOOK_READ: [],
    SHEET_READ: []
}
attribute_registry = {
    params.SHEET: {
        params.READ_ACTION: set(),
        params.WRITE_ACTION: set(),
        params.RW_ACTION: set()
    },
    params.BOOK: {
        params.READ_ACTION: set(),
        params.WRITE_ACTION: set(),
        params.RW_ACTION: set()
    }
}
keywords = {}


class UnknownParameters(Exception):
    pass


class FileTypeNotSupported(Exception):
    pass


def register_an_attribute(target, action, attr):
    if attr in attribute_registry[target][params.RW_ACTION]:
        # No registration required
        return
    attribute_registry[target][action].add(attr)
    intersection = (attr in attribute_registry[target][params.READ_ACTION]
                    and
                    attr in attribute_registry[target][params.WRITE_ACTION])
    if intersection:
        attribute_registry[target][params.RW_ACTION].add(attr)
        attribute_registry[target][params.READ_ACTION].remove(attr)
        attribute_registry[target][params.WRITE_ACTION].remove(attr)


def register_class(cls):
    debug_registry = "Source registry: "
    debug_attribute = "Instance attribute: "
    for target, action in product(cls.targets, cls.actions):
        key = REGISTRY_KEY_FORMAT % (target, action)
        registry[key].append(cls)
        debug_registry += "%s -> %s, " % (key, cls)
        for attr in cls.attributes:
            if attr in NO_DOT_NOTATION:
                continue
            register_an_attribute(target, action, attr)
            debug_attribute += "%s -> %s, " % (key, attr)
            keywords[attr] = cls.key
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
    fields = [params.SOURCE]
    attributes = []
    targets = []
    actions = []
    key = params.SOURCE

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


class FileSource(Source):
    """
    Write into presentational file
    """
    @classmethod
    def is_my_business(cls, action, **keywords):
        status = super(FileSource, cls).is_my_business(
            action, **keywords)
        if status:
            file_name = keywords.get(params.FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = _find_file_type_from_file_name(file_name,
                                                               action)
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(params.FILE_TYPE)

            if cls.can_i_handle(action, file_type):
                status = True
            else:
                status = False
        return status

    @classmethod
    def can_i_handle(cls, action, file_type):
        return False


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


def get_book_rw_attributes():
    return attribute_registry[params.BOOK][params.RW_ACTION]


def get_book_w_attributes():
    return attribute_registry[params.BOOK][params.WRITE_ACTION]


def get_book_r_attributes():
    return attribute_registry[params.BOOK][params.READ_ACTION]


def get_sheet_rw_attributes():
    return attribute_registry[params.SHEET][params.RW_ACTION]


def get_sheet_w_attributes():
    return attribute_registry[params.SHEET][params.WRITE_ACTION]


def get_sheet_r_attributes():
    return attribute_registry[params.SHEET][params.READ_ACTION]


def _get_generic_source(target, action, **keywords):
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
                FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))
        else:
            msg = "Please check if there were typos in "
            msg += "function parameters: %s. Otherwise "
            msg += "unrecognized parameters were given."
            raise UnknownParameters(msg % keywords)
    else:
        raise UnknownParameters("No parameters found!")


def _find_file_type_from_file_name(file_name, action):
    if action == 'read':
        list_of_file_types = supported_read_file_types()
    else:
        list_of_file_types = supported_write_file_types()
    file_types = []
    lowercase_file_name = file_name.lower()
    for a_supported_type in list_of_file_types:
        if lowercase_file_name.endswith(a_supported_type):
            file_types.append(a_supported_type)
    if len(file_types) > 1:
        file_types = sorted(file_types, key=lambda x: len(x))
        file_type = file_types[-1]
    elif len(file_types) == 1:
        file_type = file_types[0]
    else:
        file_type = lowercase_file_name.split('.')[-1]
        raise FileTypeNotSupported(
            FILE_TYPE_NOT_SUPPORTED_FMT % (file_type, action))

    return file_type


def supported_read_file_types():
    return set(list(manager.reader_factories.keys()) +
               list(AVAILABLE_READERS.keys()))


def supported_write_file_types():
    return renderers.get_all_file_types()


get_source = partial(
    _get_generic_source, params.SHEET, params.READ_ACTION)

get_book_source = partial(
    _get_generic_source, params.BOOK, params.READ_ACTION)

get_writable_source = partial(
    _get_generic_source, params.SHEET, params.WRITE_ACTION)

get_writable_book_source = partial(
    _get_generic_source, params.BOOK, params.WRITE_ACTION)
