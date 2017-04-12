"""
    pyexcel.plugins.sources.pydata.bookdictsource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of book dict source

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel._compact import OrderedDict, PY2
from pyexcel.source import Source, MemorySourceMixin
import pyexcel.constants as constants
from pyexcel.plugins.sources import params
from .common import _FakeIO


class BookDictSource(Source, MemorySourceMixin):
    """
    Multiple sheet data source via a dictionary of two dimensional arrays
    """
    fields = [params.BOOKDICT]
    targets = (constants.BOOK,)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)
    attributes = [params.BOOKDICT]
    key = params.BOOKDICT

    def __init__(self, bookdict, **keywords):
        self.__bookdict = bookdict
        self._content = _FakeIO()
        Source.__init__(self, **keywords)

    def get_data(self):
        the_dict = self.__bookdict
        if not isinstance(self.__bookdict, OrderedDict):
            the_dict = _convert_dict_to_ordered_dict(self.__bookdict)
        return the_dict

    def get_source_info(self):
        return params.BOOKDICT, None

    def write_data(self, book):
        self._content.setvalue(book.to_dict())


def _convert_dict_to_ordered_dict(the_dict):
    keys = the_dict.keys()
    if not PY2:
        keys = list(keys)
    keys = sorted(keys)
    ret = OrderedDict()
    for key in keys:
        ret[key] = the_dict[key]
    return ret
