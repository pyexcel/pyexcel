"""
    pyexcel.sources.http
    ~~~~~~~~~~~~~~~~~~~

    Representation of http sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io import get_data
from pyexcel._compact import request, PY2

from pyexcel.sources.base import ReadOnlySource
from pyexcel.sources import params


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
    fields = [params.URL]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION,)

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
        return sheets

    def get_source_info(self):
        return self.url, None


class HttpSheetSource(HttpBookSource):
    """
    Single sheet data source via http protocol
    """

    fields = [params.URL]
    targets = (params.SHEET,)


sources = (HttpBookSource, HttpSheetSource)