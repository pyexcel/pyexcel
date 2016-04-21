"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
import os

from pyexcel_io import load_data, save_data
from pyexcel_io import READERS, AVAILABLE_READERS, WRITERS, AVAILABLE_WRITERS

from ..constants import DEFAULT_SHEET_NAME
from . import params

from .base import FileSource, one_sheet_tuple


class IOSource(FileSource):
    """
    Get excel data from file source
    """
    @classmethod
    def can_i_handle(cls, action, file_type):
        if action == params.READ_ACTION:
            status = file_type in READERS or file_type in AVAILABLE_READERS 
        elif action == params.WRITE_ACTION:
            status = file_type in WRITERS or file_type in AVAILABLE_WRITERS
        else:
            status = False
        return status


class SheetSource(IOSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        sheets = load_data(self.file_name, **self.keywords)
        return one_sheet_tuple(sheets.items())

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
        sheets = load_data(self.file_name, **self.keywords)
        path, filename_alone = os.path.split(self.file_name)
        return sheets, filename_alone, path

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


sources = (SheetSource, BookSource)
