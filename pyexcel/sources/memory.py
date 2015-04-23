"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from .base import ReadOnlySource, _get_io
from .file import SheetSource, BookSource
from ..io import load_data
from ..constants import (
    KEYWORD_CONTENT,
    KEYWORD_FILE_TYPE,
    KEYWORD_RECORDS,
    KEYWORD_ADICT,
    KEYWORD_ARRAY,
    KEYWORD_MEMORY,
    KEYWORD_BOOKDICT,
    DEFAULT_SHEET_NAME
)


class ReadOnlySheetSource(SheetSource):
    fields = [KEYWORD_CONTENT, KEYWORD_FILE_TYPE]

    def __init__(self, content=None, file_type=None, **keywords):
        SheetSource.__init__(self,
                             file_name=(file_type, content),
                             **keywords)
    def write_data(self, content):
        pass


class WriteOnlySheetSource(SheetSource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, **keywords):
        self.content = _get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords

    def get_data(self):
        return None


class RecrodsSource(ReadOnlySource):
    fields= [KEYWORD_RECORDS]
    def __init__(self, records):
        self.records = records

    def get_data(self):
        from ..utils import from_records
        return DEFAULT_SHEET_NAME, from_records(self.records)


class DictSource(ReadOnlySource):
    fields = [KEYWORD_ADICT]

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from ..utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return DEFAULT_SHEET_NAME, tmp_array


class ArraySource(ReadOnlySource):
    fields = [KEYWORD_ARRAY]

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return DEFAULT_SHEET_NAME, self.array


class ReadOnlyBookSource(ReadOnlySource):
    fields = [KEYWORD_FILE_TYPE, KEYWORD_CONTENT]
    
    def __init__(self, file_type, content, **keywords):
        self.file_type = file_type
        self.content = content
        self.keywords = keywords

    def get_data(self):
        book = load_data((self.file_type, self.content), **self.keywords)
        return book.sheets(), KEYWORD_MEMORY, None


class BookDictSource(ReadOnlySource):
    fields = [KEYWORD_BOOKDICT]
    
    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        return self.bookdict, KEYWORD_BOOKDICT, None


class WriteOnlyBookSource(BookSource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, **keywords):
        self.content = _get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords

