"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from .base import ReadOnlySource, one_sheet_tuple
from .file import SheetSource, BookSource
from pyexcel_io import load_data, get_io
from ..constants import (
    KEYWORD_FILE_TYPE,
    KEYWORD_RECORDS,
    KEYWORD_ADICT,
    KEYWORD_ARRAY,
    KEYWORD_MEMORY,
    KEYWORD_BOOKDICT,
    DEFAULT_SHEET_NAME
)


class ReadOnlySheetSource(SheetSource):
    """Pick up 'file_type' and read a sheet from memory"""
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self,
                 file_content=None,
                 file_type=None,
                 file_stream=None,
                 **keywords):
        self.file_type = file_type
        self.file_stream = file_stream
        self.file_content = file_content
        self.keywords = keywords

    def get_data(self):
        if self.file_stream is not None:
            sheets = load_data(self.file_stream,
                               file_type=self.file_type,
                               **self.keywords)
        else:
            sheets = load_data(self.file_content,
                               file_type=self.file_type,
                               **self.keywords)
        return one_sheet_tuple(sheets.items())

    def write_data(self, content):
        """Disable write"""
        pass


class WriteOnlySheetSource(SheetSource):
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, **keywords):
        self.content = get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords

    def get_data(self):
        return None


class RecrodsSource(ReadOnlySource):
    """
    A list of dictionaries as data source

    The dictionaries should have identical fields.
    """
    fields = [KEYWORD_RECORDS]

    def __init__(self, records):
        self.records = records

    def get_data(self):
        from ..utils import from_records
        return DEFAULT_SHEET_NAME, from_records(self.records)


class DictSource(ReadOnlySource):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [KEYWORD_ADICT]

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from ..utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return DEFAULT_SHEET_NAME, tmp_array


class ArraySource(ReadOnlySource):
    """
    A two dimensional array as sheet source
    """
    fields = [KEYWORD_ARRAY]

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return DEFAULT_SHEET_NAME, self.array


class ReadOnlyBookSource(ReadOnlySource):
    """
    Multiple sheet data source via memory
    """
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self,
                 file_content=None,
                 file_type=None,
                 file_stream=None,
                 **keywords):
        self.file_type = file_type
        self.file_content = file_content
        self.file_stream = file_stream
        self.keywords = keywords

    def get_data(self):
        if self.file_stream is not None:
            sheets = load_data(self.file_stream,
                               file_type=self.file_type,
                               **self.keywords)
        else:
            sheets = load_data(self.file_content,
                               file_type=self.file_type,
                               **self.keywords)
        return sheets, KEYWORD_MEMORY, None


class BookDictSource(ReadOnlySource):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [KEYWORD_BOOKDICT]

    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        return self.bookdict, KEYWORD_BOOKDICT, None


class WriteOnlyBookSource(BookSource):
    """
    Multiple sheet data source for writting back to memory
    """
    fields = [KEYWORD_FILE_TYPE]

    def __init__(self, file_type=None, **keywords):
        self.content = get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords
