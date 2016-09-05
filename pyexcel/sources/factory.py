from six import with_metaclass
from pyexcel._compact import PY2, is_string
from . import params


registry = {
    "input-read": [],
    "input-write": [],
    "sheet-write": [],
    "book-write": [],
    "book-read": [],
    "sheet-read": []
}
attribute_registry = {
    "input-read": [],
    "input-write": [],
    "sheet-read": [],
    "sheet-write": [],
    "book-read": [],
    "book-write": []
}
keywords = {}


def register_class(cls):
    for target in cls.targets:
        for action in cls.actions:
            key = "%s-%s" % (target, action)
            registry[key].append(cls)
            for attr in cls.attributes:
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
    return set(attribute_registry["book-read"]).intersection(
        set(attribute_registry["book-write"]))


def get_book_w_attributes():
    return set(attribute_registry["book-write"]).difference(
        set(attribute_registry["book-read"]))


def get_sheet_rw_attributes():
    return set(attribute_registry["sheet-read"]).intersection(
        set(attribute_registry["sheet-write"]))


def get_sheet_w_attributes():
    return set(attribute_registry["sheet-write"]).difference(
        set(attribute_registry["sheet-read"]))


def _get_generic_source(target, action, **keywords):
    key = "%s-%s" % (target, action)
    for source in registry[key]:
        if source.is_my_business(action, **keywords):
            s = source(**keywords)
            return s
    return None


def get_source(**keywords):
    source = _get_generic_source(
        'input',
        'read',
        **keywords)
    if source is None:
        source = _get_generic_source(
            'sheet',
            'read',
            **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_book_source(**keywords):
    source = _get_generic_source(
        'input',
        'read',
        **keywords)
    if source is None:
        source = _get_generic_source(
            'book',
            'read',
            **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_writable_source(**keywords):
    source = _get_generic_source(
        'sheet',
        'write',
        **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source


def get_writable_book_source(**keywords):
    source = _get_generic_source(
        'book',
        'write',
        **keywords)
    if source is None:
        raise NotImplementedError("No source found for %s" % keywords)
    else:
        return source
