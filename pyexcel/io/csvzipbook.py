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
from .._compact import BytesIO, StringIO


class CSVZipBook(CSVBook):
    """
    CSVBook reader

    It simply return one sheet
    """
    def __init__(self, filename,
                 file_content=None,
                 encoding="utf-8",
                 **keywords):
        if filename:
            the_file = filename
        else:
            the_file = BytesIO(file_content)
        myzip = zipfile.ZipFile(the_file, 'r')
        names = myzip.namelist()
        io = StringIO(myzip.read(names[0]).decode(encoding))
        CSVBook.__init__(self, None, io.getvalue(), encoding=encoding, **keywords)
        myzip.close()


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
        myzip = zipfile.ZipFile(self.zipfile, 'w')
        if isinstance(self.zipfile, BytesIO):
            filename = "pyexcel"
        else:
            names = os.path.split(self.zipfile)
            filename = names[-1]
            filename = filename.replace("csvz", "csv")
        myzip.writestr(filename, self.file.getvalue())
        myzip.close()

