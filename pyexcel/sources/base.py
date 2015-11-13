"""
    pyexcel.sources.base
    ~~~~~~~~~~~~~~~~~~~

    Representation of excel data sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from ..constants import (
    MESSAGE_UNKNOWN_IO_OPERATION,
    KEYWORD_SOURCE, KEYWORD_FILE_NAME, KEYWORD_FILE_TYPE)
from .._compact import PY2, is_string
from pyexcel_io import AVAILABLE_READERS, AVAILABLE_WRITERS


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


class Source:
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


class FileSource(Source):
    @classmethod
    def is_my_business(cls, action, **keywords):
        statuses = [_has_field(field, keywords) for field in cls.fields]
        results = filter(lambda status: status is False, statuses)
        if not PY2:
            results = list(results)
        status = len(results) == 0
        if status:
            file_name = keywords.get(KEYWORD_FILE_NAME, None)
            if file_name:
                if is_string(type(file_name)):
                    file_type = file_name.split(".")[-1]
                else:
                    raise IOError("Wrong file name")
            else:
                file_type = keywords.get(KEYWORD_FILE_TYPE)
            if action == 'read':
                status = file_type in AVAILABLE_READERS
            elif action == 'write':
                status = file_type in AVAILABLE_WRITERS
            else:
                raise Exception(MESSAGE_UNKNOWN_IO_OPERATION)
        return status


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


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    if len(items[0][1]) == 0:
        return None, None
    else:
        return items[0][0], items[0][1]
