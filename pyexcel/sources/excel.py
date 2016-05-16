"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
import os

from pyexcel_io import get_data, save_data, RWManager
from pyexcel_io.utils import AVAILABLE_WRITERS

from ..constants import DEFAULT_SHEET_NAME
from . import params

from .base import FileSource


class IOSource(FileSource):
    """
    Get excel data from file source
    """
    @classmethod
    def can_i_handle(cls, action, file_type):
        if action == params.WRITE_ACTION:
            status = file_type in RWManager.writer_factories or file_type in AVAILABLE_WRITERS
        else:
            status = False
        return status


class SheetSource(IOSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (params.SHEET,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def get_source_info(self):
        path, file_name = os.path.split(self.file_name)
        return file_name, path

    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        sheets = get_data(self.file_name, **self.keywords)
        return sheets

    def write_data(self, sheet):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        if isinstance(self.file_name, tuple):
            save_data(self.file_name[1],
                      data,
                      file_type=self.file_name[0],
                      **self.keywords)
        else:
            save_data(self.file_name,
                      data,
                      **self.keywords)


class BookSource(SheetSource):
    """Pick up 'file_name' field and do multiple sheet based read and write
    """
    targets = (params.BOOK,)

    def get_data(self):
        sheets = get_data(self.file_name, **self.keywords)
        return sheets

    def write_data(self, book):
        book_dict = book.to_dict()
        if isinstance(self.file_name, tuple):
            save_data(self.file_name[1],
                      book_dict,
                      file_type=self.file_name[0],
                      **self.keywords)
        else:
            save_data(self.file_name,
                      book_dict,
                      **self.keywords)


class WriteOnlyMemorySourceMixin(object):
    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream:
            self.content = file_stream
        else:
            self.content = RWManager.get_io(file_type)
        self.file_type = file_type
        self.keywords = keywords


class WriteOnlySheetSource(WriteOnlyMemorySourceMixin, SheetSource):
    fields = [params.FILE_TYPE]
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        WriteOnlyMemorySourceMixin.__init__(self, file_type=file_type,
                                       file_stream=file_stream, **keywords)
        self.file_name = (file_type, self.content)


class WriteOnlyBookSource(WriteOnlyMemorySourceMixin, BookSource):
    """
    Multiple sheet data source for writting back to memory
    """
    fields = [params.FILE_TYPE]
    targets = (params.BOOK,)
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        WriteOnlyMemorySourceMixin.__init__(self, file_type=file_type,
                                       file_stream=file_stream, **keywords)
        self.file_name = (file_type, self.content)


sources = (
    WriteOnlySheetSource,
    WriteOnlyBookSource,
    SheetSource,
    BookSource
)
