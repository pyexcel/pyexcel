"""
    pyexcel.sources.base
    ~~~~~~~~~~~~~~~~~~~

    Representation of excel data sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from ..constants import KEYWORD_SOURCE
from .._compact import PY2
from .._compact import is_string
from ..constants import KEYWORD_FILE_NAME, KEYWORD_FILE_TYPE



def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


class Source(object):
    """ A command source for get_sheet, get_book, save_as and save_book_as

    This can be used to extend the function parameters once the custom
    class inherit this and register it with corresponding source registry
    """
    fields = [KEYWORD_SOURCE]

    def __init__(self, source=None, **keywords):
        self.source = source
        self.keywords = keywords

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
        pass


class WriteOnlySource(Source):
    """Write Only Data Source"""

    def get_data(self):
        """This function does nothing"""
        return None


class FileSource(Source):
    """
    Write into presentational file
    """
    @classmethod
    def is_my_business(cls, action, **keywords):
        status = super(FileSource, cls).is_my_business(
            action, **keywords)
        if status:
            file_name = keywords.get(KEYWORD_FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = file_name.split(".")[-1]
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(KEYWORD_FILE_TYPE)

            if cls.can_i_handle(action, file_type):
                status = True
            else:
                status = False
        return status

    @classmethod
    def can_i_handle(cls, action, file_type):
        return False


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    return items[0][0], items[0][1]
