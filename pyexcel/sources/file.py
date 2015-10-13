"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
import os
from .base import FileSource, one_sheet_tuple
from ..constants import KEYWORD_FILE_NAME
from pyexcel_io import load_data, get_writer


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
        sheets = load_data(self.file_name, **self.keywords)
        return one_sheet_tuple(sheets.items())

    def write_data(self, sheet):
        if isinstance(self.file_name, tuple):
            writer = get_writer(self.file_name[1],
                                     self.file_name[0],
                                     single_sheet_in_book=True,
                                     **self.keywords)
        else:
            writer = get_writer(self.file_name,
                                single_sheet_in_book=True,
                                **self.keywords)

        raw_sheet = writer.create_sheet(sheet.name)
        data_table = sheet.to_array()
        rows = len(data_table)
        columns = len(data_table[0])
        raw_sheet.set_size((rows, columns))
        raw_sheet.write_array(data_table)
        raw_sheet.close()
        writer.close()


class BookSource(SheetSource):
    """Pick up 'file_name' field and do multiple sheet based read and write
    """
    def get_data(self):
        sheets = load_data(self.file_name, **self.keywords)
        path, filename_alone = os.path.split(self.file_name)
        return sheets, filename_alone, path

    def write_data(self, book):
        if isinstance(self.file_name, tuple):
            writer = get_writer(self.file_name[1],
                                     self.file_name[0],
                                     **self.keywords)
        else:
            writer = get_writer(self.file_name,
                                **self.keywords)

        writer.write(book.to_dict())
        writer.close()
