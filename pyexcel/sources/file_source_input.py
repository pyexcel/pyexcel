"""
    pyexcel.sources.file
    ~~~~~~~~~~~~~~~~~~~

    Representation of file sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
import os

from pyexcel_io import get_data, RWManager
from pyexcel_io.utils import AVAILABLE_READERS

from pyexcel import params
from .factory import FileSource


class InputSource(FileSource):
    """
    Get excel data from file source
    """
    attributes = ["xls", "xlsx", "ods", "csv", "csvz", "tsv", "tsvz"]

    @classmethod
    def can_i_handle(cls, action, file_type):
        if action == params.READ_ACTION:
            status = (file_type in RWManager.reader_factories or
                      file_type in AVAILABLE_READERS)
        else:
            status = False
        return status


class ExcelSource(InputSource):
    """Pick up 'file_name' field and do single sheet based read and write
    """
    fields = [params.FILE_NAME]
    targets = (params.INPUT,)
    actions = (params.READ_ACTION,)

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
        sheets = get_data(self.file_name, streaming=True, **self.keywords)
        return sheets


class ExcelMemorySource(InputSource):
    """Pick up 'file_type' and read a sheet from memory"""
    fields = [params.FILE_TYPE]
    targets = (params.SHEET, params.BOOK)
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
            sheets = get_data(self.file_stream,
                              file_type=self.file_type,
                              streaming=True,
                              **self.keywords)
        else:
            sheets = get_data(self.file_content,
                              file_type=self.file_type,
                              streaming=True,
                              **self.keywords)
        return sheets

    def get_source_info(self):
        return params.MEMORY, None


sources = (ExcelSource, ExcelMemorySource)
