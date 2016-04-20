"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from .base import ReadOnlySource, one_sheet_tuple
from .file import FileSource, SheetSource, BookSource
from pyexcel_io import get_data
from pyexcel_io.manager import RWManager
from ..constants import (
    KEYWORD_FILE_TYPE,
    KEYWORD_RECORDS,
    KEYWORD_ADICT,
    KEYWORD_ARRAY,
    KEYWORD_MEMORY,
    KEYWORD_BOOKDICT,
    DEFAULT_SHEET_NAME
)
from .._compact import OrderedDict

from .base import ReadOnlySource, one_sheet_tuple
from .file import IOSource, SheetSource, BookSource


class ReadOnlySheetSource(SheetSource):
    """Pick up 'file_type' and read a sheet from memory"""
    fields = [KEYWORD_FILE_TYPE]
    targets = ('sheet',)
    actions = ('read',)

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
            sheets = get_data(self.file_stream,
                              file_type=self.file_type,
                              **self.keywords)
        else:
            sheets = get_data(self.file_content,
                              file_type=self.file_type,
                              **self.keywords)
        return one_sheet_tuple(sheets.items())

    def write_data(self, content):
        """Disable write"""
        raise Exception("ReadOnlySource does not write")


class WriteOnlySheetSource(SheetSource):
    fields = [KEYWORD_FILE_TYPE]
    targets = ('sheet',)
    actions = ('write',)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream is None:
            self.content = RWManager.get_io(file_type)
        else:
            self.content = file_stream
        self.file_name = (file_type, self.content)
        self.keywords = keywords

    def get_data(self):
        raise Exception("WriteOnlySource does not read" )


class RecordsSource(ReadOnlySource):
    """
    A list of dictionaries as data source

    The dictionaries should have identical fields.
    """
    fields = [KEYWORD_RECORDS]
    targets = ('sheet',)
    actions = ('read',)

    def __init__(self, records):
        self.records = records

    def get_data(self):
        from ..utils import yield_from_records
        return DEFAULT_SHEET_NAME, yield_from_records(self.records)


class DictSource(ReadOnlySource):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [KEYWORD_ADICT]
    targets = ('sheet',)
    actions = ('read',)

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from ..utils import yield_dict_to_array
        return DEFAULT_SHEET_NAME, yield_dict_to_array(self.adict,
                                                       self.with_keys)


class ArraySource(ReadOnlySource):
    """
    A two dimensional array as sheet source
    """
    fields = [KEYWORD_ARRAY]
    targets = ('sheet',)
    actions = ('read',)

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return DEFAULT_SHEET_NAME, self.array


class ReadOnlyBookSource(ReadOnlySource, IOSource):
    """
    Multiple sheet data source via memory
    """
    fields = [KEYWORD_FILE_TYPE]
    targets = ('book',)
    actions = ('read',)

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
            sheets = get_data(self.file_stream,
                              file_type=self.file_type,
                              **self.keywords)
        else:
            sheets = get_data(self.file_content,
                              file_type=self.file_type,
                              **self.keywords)
        return sheets, KEYWORD_MEMORY, None


class BookDictSource(ReadOnlySource):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [KEYWORD_BOOKDICT]
    targets = ('book',)
    actions = ('read',)

    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        the_dict = self.bookdict
        if not isinstance(self.bookdict, OrderedDict):
            from ..utils import convert_dict_to_ordered_dict
            the_dict = convert_dict_to_ordered_dict(self.bookdict)
        return the_dict, KEYWORD_BOOKDICT, None


class WriteOnlyBookSource(BookSource):
    """
    Multiple sheet data source for writting back to memory
    """
    fields = [KEYWORD_FILE_TYPE]
    targets = ('book',)
    actions = ('write',)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream is None:
            self.content = RWManager.get_io(file_type)
        else:
            self.content = file_stream
        self.file_name = (file_type, self.content)
        self.keywords = keywords


sources = (
    ReadOnlySheetSource,
    DictSource,
    RecordsSource,
    ArraySource,
    WriteOnlySheetSource,
    ReadOnlyBookSource,
    BookDictSource,
    WriteOnlyBookSource
)

