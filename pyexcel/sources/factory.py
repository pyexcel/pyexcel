from functools import partial

from pyexcel._compact import PY2, is_string, with_metaclass
from . import params

# ignore the following attributes
NO_DOT_NOTATION = ('django', 'sql')
# registries
REGISTRY_KEY_FORMAT = "%s-%s"

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
    SHEET_WRITE: [],
    BOOK_WRITE: [],
    BOOK_READ: [],
    SHEET_READ: []
}
keywords = {}


def register_class(cls):
    for target in cls.targets:
        for action in cls.actions:
            key = REGISTRY_KEY_FORMAT % (target, action)
            registry[key].append(cls)
            for attr in cls.attributes:
                if attr in NO_DOT_NOTATION:
                    continue
                attribute_registry[key].append(attr)
                keywords[attr] = cls.key


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
        self.source = source
        self.keywords = keywords

    def get_source_info(self):
        return (None, None)

    @classmethod
    def is_my_business(cls, action, **keywords):
        """
        If all required keys are present, this source is activated
        """
        statuses = [_has_field(field, keywords) for field in cls.fields]
        results = filter(lambda status: status is False, statuses)
        if not PY2:
            results = list(results)
        return len(results) == 0

    def write_data(self, content):
        raise NotImplementedError("")

    def get_data(self):
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
                    file_type = file_name.split(".")[-1]
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
    return set(attribute_registry[BOOK_READ]).intersection(
        set(attribute_registry[BOOK_WRITE]))


def get_book_w_attributes():
    return set(attribute_registry[BOOK_WRITE]).difference(
        set(attribute_registry[BOOK_READ]))


def get_book_r_attributes():
    return set(attribute_registry[BOOK_READ]).difference(
        set(attribute_registry[BOOK_WRITE]))


def get_sheet_rw_attributes():
    return set(attribute_registry[SHEET_READ]).intersection(
        set(attribute_registry[SHEET_WRITE]))


def get_sheet_w_attributes():
    return set(attribute_registry[SHEET_WRITE]).difference(
        set(attribute_registry[SHEET_READ]))


def get_sheet_r_attributes():
    return set(attribute_registry[SHEET_READ]).difference(
        set(attribute_registry[SHEET_WRITE]))


def _get_generic_source(target, action, **keywords):
    key = REGISTRY_KEY_FORMAT % (target, action)
    for source in registry[key]:
        if source.is_my_business(action, **keywords):
            s = source(**keywords)
            return s
    raise NotImplementedError("No source found for %s" % keywords)


get_source = partial(_get_generic_source,
                     params.SHEET, params.READ_ACTION)

get_book_source = partial(_get_generic_source,
                          params.BOOK, params.READ_ACTION)

get_writable_source = partial(_get_generic_source,
                              params.SHEET, params.WRITE_ACTION)

get_writable_book_source = partial(_get_generic_source,
                                   params.BOOK, params.WRITE_ACTION)
