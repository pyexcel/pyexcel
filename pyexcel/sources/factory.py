from pyexcel._compact import PY2, is_string
from pyexcel.params import FILE_NAME, FILE_TYPE, SOURCE


class SourceMeta(type):
    """sole class registry"""
    def __init__(cls, name, bases, nmspc):
        super(SourceMeta, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = {
                "input-read": [],
                "sheet-write": [],
                "book-write": [],
                "book-read": [],
                "sheet-read": []
            }
            cls.attribute_registry = {
                "input-read": [],
                "sheet-read": [],
                "sheet-write": [],
                "book-read": [],
                "book-write": []
            }
        for target in cls.targets:
            for action in cls.actions:
                key = "%s-%s" % (target, action)
                cls.registry[key].append(cls)
                for attr in cls.attributes:
                    cls.attribute_registry[key].append(attr)


class Source(object):
    """ A command source for get_sheet, get_book, save_as and save_book_as

    This can be used to extend the function parameters once the custom
    class inherit this and register it with corresponding source registry
    """
    __metaclass__ = SourceMeta
    fields = [SOURCE]
    attributes = []
    targets = []
    actions = []

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
        """This function does nothing """
        raise Exception("ReadOnlySource does not write")

    def get_data(self):
        """This function does nothing"""
        raise Exception("WriteOnlySource does not read")


class FileSource(Source):
    """
    Write into presentational file
    """
    @classmethod
    def is_my_business(cls, action, **keywords):
        status = super(FileSource, cls).is_my_business(
            action, **keywords)
        if status:
            file_name = keywords.get(FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = file_name.split(".")[-1]
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(FILE_TYPE)

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
