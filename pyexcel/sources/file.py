"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
import os
from .base import Source, one_sheet_tuple, _has_field
from ..constants import (
    DEFAULT_SHEET_NAME,
    KEYWORD_FILE_NAME,
    MESSAGE_UNKNOWN_IO_OPERATION,
    KEYWORD_FILE_TYPE)
from pyexcel_io import get_data, save_data
from pyexcel_io.book import AVAILABLE_READERS, AVAILABLE_WRITERS
from pyexcel_io.book import ReaderFactory, WriterFactory
from .._compact import PY2, is_string


class FileSource(Source):
    """
    Get excel data from file source
    """
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
                status = file_type in ReaderFactory.factories or file_type in AVAILABLE_READERS 
            elif action == 'write':
                status = file_type in WriterFactory.factories or file_type in AVAILABLE_WRITERS
            else:
                raise Exception(MESSAGE_UNKNOWN_IO_OPERATION)
        return status


class SheetSource(FileSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [KEYWORD_FILE_NAME]

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords

    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        sheets = get_data(self.file_name, **self.keywords)
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
    def get_data(self):
        sheets = get_data(self.file_name, **self.keywords)
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

