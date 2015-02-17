"""
    pyexcel.io.csvzipbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014-2015 by C. W.
    :license: GPL v3
"""
import zipfile
import csv
from pyexcel_io import BookReader, BookWriter
from .csvbook import (
    CSVinMemoryReader,
    NamedContent,
    CSVSheetWriter,
    DEFAULT_SHEETNAME
)
from .._compact import BytesIO, StringIO


class CSVZipBook(BookReader):
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, filename,
                 file_content=None,
                 load_sheet_with_name=None,
                 load_sheet_at_index=None,
                 **keywords):
        BookReader.__init__(self, filename,
                            file_content=file_content,
                            load_sheet_with_name=load_sheet_with_name,
                            load_sheet_at_index=load_sheet_at_index,
                            **keywords)
        self.native_book.close()

    def load_from_memory(self, file_content, **keywords):
        io = BytesIO(file_content)
        return zipfile.ZipFile(io, 'r')

    def load_from_file(self, filename, **keywords):
        return zipfile.ZipFile(filename, 'r')

    def sheetIterator(self):
        if self.sheet_name:
            return [sheet for sheet in self.native_book.namelist() if self._get_sheet_name(sheet) == self.sheet_name]
        else:
            return self.native_book.namelist()

    def _get_sheet_name(self, filename):
        name_len = len(filename) - 4
        return filename[:name_len]

    def getSheet(self, native_sheet):
        return CSVinMemoryReader(
            NamedContent(self._get_sheet_name(native_sheet),
                         self.native_book.read(native_sheet)),
            **self.keywords)


class CSVZipSheetWriter(CSVSheetWriter):
    def __init__(self, zipfile, sheetname, file_extension, **keywords):
        self.file_extension = file_extension
        keywords['single_sheet_in_book'] = False
        CSVSheetWriter.__init__(self, zipfile, sheetname, **keywords)

    def set_sheet_name(self, name):
        self.content = StringIO()
        self.writer = csv.writer(self.content, **self.keywords)

    def close(self):
        file_name = "%s.%s" % (self.native_sheet, self.file_extension)
        self.native_book.writestr(file_name, self.content.getvalue())
        self.content.close()


class CSVZipWriter(BookWriter):
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, filename, **keywords):
        BookWriter.__init__(self, filename, **keywords)
        self.myzip = zipfile.ZipFile(self.file, 'w')
        if 'dialect' in keywords:
            self.file_extension = "tsv"
        else:
            self.file_extension = "csv"

    def create_sheet(self, name):
        given_name = name
        if given_name is None:
            given_name = DEFAULT_SHEETNAME
        return CSVZipSheetWriter(self.myzip,
                                 given_name,
                                 self.file_extension,
                                 **self.keywords)

    def close(self):
        """
        This call close the file handle
        """
        self.myzip.close()
