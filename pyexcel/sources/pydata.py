"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import OrderedDict
from pyexcel.constants import DEFAULT_SHEET_NAME

from pyexcel.sources.base import ReadOnlySource
from pyexcel.sources import params


class RecordsSource(ReadOnlySource):
    """
    A list of dictionaries as data source

    The dictionaries should have identical fields.
    """
    fields = [params.RECORDS]
    targets = (params.INPUT,)
    actions = (params.READ_ACTION,)

    def __init__(self, records):
        self.records = records

    def get_data(self):
        from pyexcel.utils import yield_from_records
        return {DEFAULT_SHEET_NAME: yield_from_records(self.records)}

    def get_source_info(self):
        return params.RECORDS, None


class DictSource(ReadOnlySource):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [params.ADICT]
    targets = (params.INPUT,)
    actions = (params.READ_ACTION,)

    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self):
        from pyexcel.utils import yield_dict_to_array
        return {DEFAULT_SHEET_NAME: yield_dict_to_array(self.adict,
                                                       self.with_keys)}

    def get_source_info(self):
        return params.ADICT, None


class ArraySource(ReadOnlySource):
    """
    A two dimensional array as sheet source
    """
    fields = [params.ARRAY]
    targets = (params.INPUT,)
    actions = (params.READ_ACTION,)

    def __init__(self, array):
        self.array = array

    def get_data(self):
        return {DEFAULT_SHEET_NAME: self.array}

    def get_source_info(self):
        return params.ARRAY, None


class BookDictSource(ReadOnlySource):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [params.BOOKDICT]
    targets = (params.INPUT,)
    actions = (params.READ_ACTION,)

    def __init__(self, bookdict, **keywords):
        self.bookdict = bookdict

    def get_data(self):
        the_dict = self.bookdict
        if not isinstance(self.bookdict, OrderedDict):
            from pyexcel.utils import convert_dict_to_ordered_dict
            the_dict = convert_dict_to_ordered_dict(self.bookdict)
        return the_dict

    def get_source_info(self):
        return params.BOOKDICT, None



sources = (
    DictSource,
    RecordsSource,
    ArraySource,
    BookDictSource,
)

