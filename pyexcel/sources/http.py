"""
    pyexcel.sources.http
    ~~~~~~~~~~~~~~~~~~~

    Representation of http sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from .base import ReadOnlySource, one_sheet_tuple
from ..constants import KEYWORD_URL
from pyexcel_io import get_data
from .._compact import request, PY2


FILE_TYPE_MIME_TABLE = {
    "text/csv": "csv",
    "text/tab-separated-values": "tsv",
    "application/vnd.oasis.opendocument.spreadsheet": "ods",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-excel.sheet.macroenabled.12": "xlsm"
}


def get_file_type_from_url(url):
    extension = url.split('.')
    return extension[-1]


class HttpBookSource(ReadOnlySource):
    """
    Multiple sheet data source via http protocol
    """
    fields = [KEYWORD_URL]
    targets = ('book',)
    actions = ('read',)

    def __init__(self, url=None, **keywords):
        self.url = url
        self.keywords = keywords

    def get_data(self):
        f = request.urlopen(self.url)
        info = f.info()
        if PY2:
            mime_type = info.type
        else:
            mime_type = info.get_content_type()
        file_type = FILE_TYPE_MIME_TABLE.get(mime_type, None)
        if file_type is None:
            file_type = get_file_type_from_url(self.url)
        content = f.read()
        sheets = get_data(content,
                          file_type=file_type,
                          **self.keywords)
        return sheets, KEYWORD_URL, None


class HttpSheetSource(HttpBookSource):
    """
    Single sheet data source via http protocol
    """

    fields = [KEYWORD_URL]
    targets = ('sheet',)

    def __init__(self, url=None, **keywords):
        self.url = url
        self.keywords = keywords

    def get_data(self):
        sheets, unused1, unused2 = HttpBookSource.get_data(self)
        return one_sheet_tuple(sheets.items())


sources = (HttpBookSource, HttpSheetSource)