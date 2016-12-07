"""
    pyexcel.sources.pydata
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import OrderedDict
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.sources import params
from pyexcel.sources.factory import Source
from pyexcel._compact import zip_longest, PY2


class _FakeIO:
    def __init__(self):
        self.__value = None

    def setvalue(self, value):
        self.__value = value

    def getvalue(self):
        return self.__value


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

    def __init__(self, records):
        self.__records = records
        self.__content = _FakeIO()

    def get_data(self):
        return {DEFAULT_SHEET_NAME: yield_from_records(self.__records)}

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

    def __init__(self, adict, with_keys=True):
        self.__adict = adict
        self.__with_keys = with_keys
        self.__content = _FakeIO()

    def get_data(self):
        return {DEFAULT_SHEET_NAME: yield_dict_to_array(
            self.__adict, self.__with_keys)}

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

    def __init__(self, array):
        self.__array = array
        self.__content = _FakeIO()

    def get_data(self):
        return {DEFAULT_SHEET_NAME: self.__array}

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

    def __init__(self, bookdict, **keywords):
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


def yield_from_records(records):
    """Reverse function of to_records
    """
    if len(records) < 1:
        yield []
    else:
        first_record = records[0]
        if isinstance(first_record, OrderedDict):
            keys = first_record.keys()
        else:
            keys = sorted(first_record.keys())
        yield list(keys)
        for r in records:
            row = []
            for k in keys:
                row.append(r[k])
            yield row


def yield_dict_to_array(the_dict, with_keys=True):
    """Convert a dictionary of columns to an array

    The example dict is::

        {
            "Column 1": [1, 2, 3],
            "Column 2": [5, 6, 7, 8],
            "Column 3": [9, 10, 11, 12, 13],
        }

    The output will be::

        [
            ["Column 1", "Column 2", "Column 3"],
            [1, 5, 9],
            [2, 6, 10],
            [3, 7, 11],
            ['', 8, 12],
            ['', '', 13]
        ]

    :param dict the_dict: the dictionary to be converted.
    :param bool with_keys: to write the keys as the first row or not
    """
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    if not isinstance(the_dict, OrderedDict):
        keys = sorted(keys)
    if with_keys:
        yield keys
    sorted_values = (the_dict[key] for key in keys)
    for row in zip_longest(*sorted_values, fillvalue=''):
        yield list(row)


def convert_dict_to_ordered_dict(the_dict):
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    keys = sorted(keys)
    ret = OrderedDict()
    for key in keys:
        ret[key] = the_dict[key]
    return ret
