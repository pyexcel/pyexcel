"""
    pyexcel.sources.memory
    ~~~~~~~~~~~~~~~~~~~

    Representation of memory sources

    :copyright: (c) 2015-2016 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import OrderedDict
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.sources import params
from pyexcel.sources.factory import Source


class _FakeIO:
    def __init__(self):
        self.value = None

    def setvalue(self, value):
        self.value = value

    def getvalue(self):
        return self.value


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
        self.records = records
        self.content = _FakeIO()

    def get_data(self):
        from pyexcel.utils import yield_from_records
        return {DEFAULT_SHEET_NAME: yield_from_records(self.records)}

    def get_source_info(self):
        return params.RECORDS, None

    def write_data(self, sheet):
        self.content.setvalue(sheet.to_records())


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
        self.adict = adict
        self.with_keys = with_keys
        self.content = _FakeIO()

    def get_data(self):
        from pyexcel.utils import yield_dict_to_array
        return {DEFAULT_SHEET_NAME: yield_dict_to_array(
            self.adict, self.with_keys)}

    def get_source_info(self):
        return params.ADICT, None

    def write_data(self, sheet):
        self.content.setvalue(sheet.to_dict())


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
        self.array = array
        self.content = _FakeIO()

    def get_data(self):
        return {DEFAULT_SHEET_NAME: self.array}

    def get_source_info(self):
        return params.ARRAY, None

    def write_data(self, sheet):
        self.content.setvalue(sheet.to_array())


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
        self.bookdict = bookdict
        self.content = _FakeIO()

    def get_data(self):
        the_dict = self.bookdict
        if not isinstance(self.bookdict, OrderedDict):
            from pyexcel.utils import convert_dict_to_ordered_dict
            the_dict = convert_dict_to_ordered_dict(self.bookdict)
        return the_dict

    def get_source_info(self):
        return params.BOOKDICT, None

    def write_data(self, book):
        self.content.setvalue(book.to_dict())
