"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import load_data, get_io

from .._compact import OrderedDict
from ..constants import DEFAULT_SHEET_NAME

from .base import ReadOnlySource, one_sheet_tuple
from .file import IOSource, SheetSource, BookSource
from . import params


class ReadOnlySheetSource(SheetSource):
    """Pick up 'file_type' and read a sheet from memory"""
    fields = [params.FILE_TYPE]
    actions = (params.READ_ACTION,)

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
        raise Exception("ReadOnlySource does not write")


class WriteOnlySheetSource(SheetSource):
    fields = [params.FILE_TYPE]
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = get_io(file_type)
        self.file_name = (file_type, self.content)
        self.keywords = keywords

    def get_data(self):
        raise Exception("WriteOnlySource does not read" )


class RecordsSource(ReadOnlySource):
    """
    A list of dictionaries as data source

    The dictionaries should have identical fields.
    """
    fields = [params.RECORDS]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

    def __init__(self, records):
        self.records = records

    def get_data(self):
        from ..utils import yield_from_records
        return DEFAULT_SHEET_NAME, yield_from_records(self.records)


class DictSource(ReadOnlySource):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [params.ADICT]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

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
    fields = [params.ARRAY]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return DEFAULT_SHEET_NAME, self.array


class ReadOnlyBookSource(ReadOnlySource, IOSource):
    """
    Multiple sheet data source via memory
    """
    fields = [params.FILE_TYPE]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION,)

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
        return sheets, params.MEMORY, None


class BookDictSource(ReadOnlySource):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [params.BOOKDICT]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION,)

    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        the_dict = self.bookdict
        if not isinstance(self.bookdict, OrderedDict):
            from ..utils import convert_dict_to_ordered_dict
            the_dict = convert_dict_to_ordered_dict(self.bookdict)
        return the_dict, params.BOOKDICT, None


class WriteOnlyBookSource(BookSource):
    """
    Multiple sheet data source for writting back to memory
    """
    fields = [params.FILE_TYPE]
    targets = (params.BOOK,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = get_io(file_type)
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
