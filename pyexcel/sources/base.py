"""
    pyexcel.sources.base
    ~~~~~~~~~~~~~~~~~~~

    Representation of excel data sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from ..constants import KEYWORD_SOURCE
from ..io import FILE_FORMAT_CSV, FILE_FORMAT_TSV
from .._compact import PY2, BytesIO, StringIO


def _has_field(field, keywords):
    return field in keywords and keywords[field] is not None


class Source:
    fields = [KEYWORD_SOURCE]
    def __init__(self, source=None, **keywords):
        self.source = source
        self.keywords = keywords

    @classmethod
    def is_my_business(self, **keywords):
        """
        If all required keys are present, this source is OK
        """
        statuses = [_has_field(field, keywords) for field in self.fields]
        results = filter(lambda status: status==False, statuses)
        if not PY2:
            results = list(results)
        return len(results) == 0
        

class ReadOnlySource(Source):

    def write_data(self, content):
        pass


class WriteOnlySource(Source):
        
    def get_data(self):
        return None


def _get_io(file_type):
    if file_type in [FILE_FORMAT_CSV, FILE_FORMAT_TSV]:
        return StringIO()
    else:
        return BytesIO()


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    if len(items[0][1]) == 0:
        return None, None
    else:
        return items[0][0], items[0][1]
