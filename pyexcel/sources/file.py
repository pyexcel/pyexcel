"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import os
from .base import Source, one_sheet_tuple
from ..constants import KEYWORD_FILE_NAME
from ..io import load_file


class SingleSheetFileSource(Source):
    fields = [KEYWORD_FILE_NAME]

    def __init__(self, file_name=None, **keywords):
        self.file_name = file_name
        self.keywords = keywords
        
    def get_data(self):
        """
        Return a dictionary with only one key and one value
        """
        io_book = load_file(self.file_name, **self.keywords)
        sheets = io_book.sheets()
        return one_sheet_tuple(sheets.items())

    def write_data(self, sheet):
        from ..writers import Writer
        w = Writer(self.file_name, sheet_name=sheet.name, **self.keywords)
        w.write_reader(sheet)
        w.close()

        
class BookSource(SingleSheetFileSource):
    def get_data(self):
        book = load_file(self.file_name, **self.keywords)
        path, filename_alone = os.path.split(self.file_name)
        return book.sheets(), filename_alone, path

    def write_data(self, book):
        from ..writers import BookWriter
        writer = BookWriter(self.file_name, **self.keywords)
        writer.write_book_reader(book)
        writer.close()

