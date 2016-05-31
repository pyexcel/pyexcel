from ._compact import PY2, is_string
from .params import FILE_NAME, FILE_TYPE, SOURCE


class SourceFactory:
    """
    The factory method to support multiple datasources in getters and savers
    """
    sources = {
        "input-read": [],
        "sheet-write": [],
        "book-write": [],
        "book-read": [],
        "sheet-read": []
    }

    @classmethod
    def register_sources(self, sources):
        for source in sources:
            for target in source.targets:
                for action in source.actions:
                    self.register_a_source(target, action, source)

    @classmethod
    def register_a_source(self, target, action, source):
        key = "%s-%s" % (target, action)
        self.sources[key].append(source)

    @classmethod
    def _get_generic_source(self, target, action, **keywords):
        key = "%s-%s" % (target, action)
        for source in self.sources[key]:
            if source.is_my_business(action, **keywords):
                s = source(**keywords)
                return s
        return None

    @classmethod
    def get_source(self, **keywords):
        source = self._get_generic_source(
            'input',
            'read',
            **keywords)
        if source is None:
            source = self._get_generic_source(
                'sheet',
                'read',
                **keywords)
        if source is None:
            raise NotImplementedError("No source found for %s" % keywords)
        else:
            return source

    @classmethod
    def get_book_source(self, **keywords):
        source = self._get_generic_source(
            'input',
            'read',
            **keywords)
        if source is None:
            source = self._get_generic_source(
                'book',
                'read',
                **keywords)
        if source is None:
            raise NotImplementedError("No source found for %s" % keywords)
        else:
            return source

    @classmethod
    def get_writeable_source(self, **keywords):
        source = self._get_generic_source(
            'sheet',
            'write',
            **keywords)
        if source is None:
            raise NotImplementedError("No source found for %s" % keywords)
        else:
            return source

    @classmethod
    def get_writeable_book_source(self, **keywords):
        source = self._get_generic_source(
            'book',
            'write',
            **keywords)
        if source is None:
            raise NotImplementedError("No source found for %s" % keywords)
        else:
            return source


class Source(object):
    """ A command source for get_sheet, get_book, save_as and save_book_as

    This can be used to extend the function parameters once the custom
    class inherit this and register it with corresponding source registry
    """
    fields = [SOURCE]

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


class ReadOnlySource(Source):
    """Read Only Data Source"""
    def write_data(self, content):
        """This function does nothing """
        raise Exception("ReadOnlySource does not write")


class WriteOnlySource(Source):
    """Write Only Data Source"""

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
