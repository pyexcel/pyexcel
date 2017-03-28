"""
    pyexcel.plugins.sources.pydata
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel_io.sheet import SheetReader

from pyexcel._compact import OrderedDict
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.sources.factory import Source
from pyexcel._compact import zip_longest, PY2
import pyexcel.constants as constants
from . import params


class _FakeIO:
    def __init__(self):
        self.__value = None

    def setvalue(self, value):
        self.__value = value

    def getvalue(self):
        return self.__value


class ArrayReader(SheetReader):

    def row_iterator(self):
        for row in self._native_sheet:
            yield row

    def column_iterator(self, row):
        for cell in row:
            yield cell


class RecordsReader(ArrayReader):

    def row_iterator(self):
        headers = []
        for index, row in enumerate(self._native_sheet):
            if index == 0:
                if isinstance(row, OrderedDict):
                    headers = row.keys()
                else:
                    headers = sorted(row.keys())
                yield list(headers)

            values = []
            for k in headers:
                values.append(row[k])
            yield values


class DictReader(ArrayReader):

    def row_iterator(self):
        keys = self._native_sheet.keys()
        if not PY2:
            keys = list(keys)
        if not isinstance(self._native_sheet, OrderedDict):
            keys = sorted(keys)
        if self._keywords.get('with_keys', True):
            yield keys

        if isinstance(self._native_sheet[keys[0]], list):
            sorted_values = (self._native_sheet[key] for key in keys)
            for row in zip_longest(
                    *sorted_values,
                    fillvalue=constants.DEFAULT_NA):
                yield row
        else:
            row = [self._native_sheet[key] for key in keys]
            yield row


class RecordsSource(Source):
    """
    A list of dictionaries as data source

    The dictionaries should have identical fields.
    """
    fields = [params.RECORDS]
    targets = (params.SHEET, params.BOOK)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = [params.RECORDS]
    key = params.RECORDS

    def __init__(self, records, sheet_name=DEFAULT_SHEET_NAME, **keywords):
        self.__records = records
        self.__content = _FakeIO()
        self.__sheet_name = sheet_name
        self.__keywords = keywords

    def get_data(self):
        records_reader = RecordsReader(self.__records, **self.__keywords)
        return {self.__sheet_name: records_reader.to_array()}

    def get_source_info(self):
        return params.RECORDS, None

    def write_data(self, sheet):
        self.__content.setvalue(sheet.to_records())

    def get_internal_stream(self):
        return self.__content


class DictSource(Source):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [params.ADICT]
    targets = (params.SHEET, params.BOOK)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = ["dict"]
    key = params.ADICT

    def __init__(self, adict, with_keys=True, sheet_name=DEFAULT_SHEET_NAME,
                 **keywords):
        self.__adict = adict
        self.__with_keys = with_keys
        self.__content = _FakeIO()
        self.__sheet_name = sheet_name
        self.__keywords = keywords

    def get_data(self):
        dict_reader = DictReader(self.__adict, with_keys=self.__with_keys,
                                 **self.__keywords)
        return {self.__sheet_name: dict_reader.to_array()}

    def get_source_info(self):
        return params.ADICT, None

    def write_data(self, sheet):
        self.__content.setvalue(sheet.to_dict())

    def get_internal_stream(self):
        return self.__content


class ArraySource(Source):
    """
    A two dimensional array as sheet source
    """
    fields = [params.ARRAY]
    targets = (params.SHEET, params.BOOK)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = ["array"]
    key = params.ARRAY

    def __init__(self, array, sheet_name=DEFAULT_SHEET_NAME,
                 **keywords):
        self.__array = array
        self.__content = _FakeIO()
        self.__sheet_name = sheet_name
        self.__keywords = keywords

    def get_data(self):
        array_reader = ArrayReader(self.__array, **self.__keywords)
        return {self.__sheet_name: array_reader.to_array()}

    def get_source_info(self):
        return params.ARRAY, None

    def write_data(self, sheet):
        self.__content.setvalue(sheet.to_array())

    def get_internal_stream(self):
        return self.__content


class BookDictSource(Source):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [params.BOOKDICT]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION, params.WRITE_ACTION)
    attributes = [params.BOOKDICT]
    key = params.BOOKDICT

    def __init__(self, bookdict):
        self.__bookdict = bookdict
        self.__content = _FakeIO()

    def get_data(self):
        the_dict = self.__bookdict
        if not isinstance(self.__bookdict, OrderedDict):
            the_dict = convert_dict_to_ordered_dict(self.__bookdict)
        return the_dict

    def get_source_info(self):
        return params.BOOKDICT, None

    def write_data(self, book):
        self.__content.setvalue(book.to_dict())

    def get_internal_stream(self):
        return self.__content


def convert_dict_to_ordered_dict(the_dict):
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    keys = sorted(keys)
    ret = OrderedDict()
    for key in keys:
        ret[key] = the_dict[key]
    return ret
