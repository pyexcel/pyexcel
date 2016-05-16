"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import save_data, RWManager
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

    def write_data(self, sheet):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(self.file_name,
                  data,
                  **self.keywords)


class BookSource(SheetSource):
    """Pick up 'file_name' field and do multiple sheet based read and write
    """
    targets = (params.BOOK,)

    def write_data(self, book):
        book_dict = book.to_dict()
        save_data(self.file_name,
                  book_dict,
                  **self.keywords)


class WriteOnlyMemorySourceMixin(object):
    def __init__(self, file_type=None, file_stream=None, **keywords):
        if file_stream:
            self.stream = file_stream
        else:
            self.stream = RWManager.get_io(file_type)
        self.file_type = file_type
        self.keywords = keywords


class WriteOnlySheetSource(WriteOnlyMemorySourceMixin, SheetSource):
    fields = [params.FILE_TYPE]
    actions = (params.WRITE_ACTION,)

    def __init__(self, file_type=None, file_stream=None, **keywords):
        WriteOnlyMemorySourceMixin.__init__(self, file_type=file_type,
                                       file_stream=file_stream, **keywords)

    def write_data(self, sheet):
        sheet_name = DEFAULT_SHEET_NAME
        if sheet.name:
            sheet_name = sheet.name
        data = {sheet_name: sheet.to_array()}
        save_data(self.stream,
                  data,
                  file_type=self.file_type,
                  **self.keywords)


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

    def write_data(self, book):
        book_dict = book.to_dict()
        save_data(self.stream,
                  book_dict,
                  file_type=self.file_type,
                  **self.keywords)


sources = (
    WriteOnlySheetSource,
    WriteOnlyBookSource,
    SheetSource,
    BookSource
)
