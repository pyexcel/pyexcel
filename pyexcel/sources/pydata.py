"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from .._compact import OrderedDict
from ..constants import DEFAULT_SHEET_NAME

from .base import ReadOnlySource
from . import params


class RecordsSource(ReadOnlySource):
    """
    A list of dictionaries as data source

    The dictionaries should have identical fields.
    """
    fields = [params.RECORDS]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

    def __init__(self, records):
        self.records = records

    def get_data(self):
        from ..utils import yield_from_records
        return DEFAULT_SHEET_NAME, yield_from_records(self.records)


class DictSource(ReadOnlySource):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [params.ADICT]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from ..utils import yield_dict_to_array
        return DEFAULT_SHEET_NAME, yield_dict_to_array(self.adict,
                                                       self.with_keys)


class ArraySource(ReadOnlySource):
    """
    A two dimensional array as sheet source
    """
    fields = [params.ARRAY]
    targets = (params.SHEET,)
    actions = (params.READ_ACTION,)

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return DEFAULT_SHEET_NAME, self.array


class BookDictSource(ReadOnlySource):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [params.BOOKDICT]
    targets = (params.BOOK,)
    actions = (params.READ_ACTION,)

    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        the_dict = self.bookdict
        if not isinstance(self.bookdict, OrderedDict):
            from ..utils import convert_dict_to_ordered_dict
            the_dict = convert_dict_to_ordered_dict(self.bookdict)
        return the_dict, params.BOOKDICT, None




sources = (
    DictSource,
    RecordsSource,
    ArraySource,
    BookDictSource,
)

