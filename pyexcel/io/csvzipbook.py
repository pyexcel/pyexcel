"""
    pyexcel.io.csvzipbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level csv file format handler.

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import os
import zipfile
from .csvbook import CSVBook, CSVWriter
from .._compact import StringIO


class CSVZipBook(CSVBook):
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, filename,
                 file_content=None,
                 encoding="utf-8",
                 **keywords):
        with zipfile.ZipFile(filename) as myzip:
            names = myzip.namelist()
            io = StringIO(myzip.read(names[0]))
            CSVBook.__init__(self, None, io.getvalue(), encoding=encoding, **keywords)


class CSVZipWriter(CSVWriter):
    """
    csv file writer

    if there is multiple sheets for csv file, it simpily writes
    multiple csv files
    """
    def __init__(self, filename, **keywords):
        self.zipfile = filename
        io = StringIO()
        CSVWriter.__init__(self, io, **keywords)

    def close(self):
        """
        This call close the file handle
        """
        with zipfile.ZipFile(self.zipfile, 'w') as myzip:
            names = os.path.split(self.zipfile)
            filename = names[-1]
            myzip.writestr(filename.replace("csvz", "csv"), self.file.getvalue())
