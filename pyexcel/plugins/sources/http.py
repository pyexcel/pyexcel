"""
    pyexcel.source.http
    ~~~~~~~~~~~~~~~~~~~

    Representation of http sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import request, PY2

from pyexcel.source import Source
import pyexcel.constants as constants
import pyexcel.internal.parser_meta as parsers

from . import params

_xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

FILE_TYPE_MIME_TABLE = {
    "text/csv": "csv",
    "text/tab-separated-values": "tsv",
    "application/vnd.oasis.opendocument.spreadsheet": "ods",
    "application/vnd.ms-excel": "xls",
    _xlsx: "xlsx",
    "application/vnd.ms-excel.sheet.macroenabled.12": "xlsm"
}


class HttpSource(Source):
    """
    Multiple sheet data source via http protocol
    """
    fields = [params.URL]
    targets = (constants.SHEET, constants.BOOK)
    actions = (constants.READ_ACTION,)
    attributes = [params.URL]
    key = params.URL

    def __init__(self, url=None, **keywords):
        self.__url = url
        self.__keywords = keywords

    def get_data(self):
        f = request.urlopen(self.__url)
        info = f.info()
        if PY2:
            mime_type = info.type
        else:
            mime_type = info.get_content_type()
        file_type = FILE_TYPE_MIME_TABLE.get(mime_type, None)
        if file_type is None:
            file_type = _get_file_type_from_url(self.__url)
        parser = parsers.get_parser(file_type)
        content = f.read()
        sheets = parser.parse_file_content(content,
                                           **self.__keywords)
        return sheets

    def get_source_info(self):
        return self.__url, None


def _get_file_type_from_url(url):
    extension = url.split('.')
    return extension[-1]
