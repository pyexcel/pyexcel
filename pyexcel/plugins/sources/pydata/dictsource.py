"""
    pyexcel.plugins.sources.pydata.dictsource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Representation of dict sources

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
from pyexcel.constants import DEFAULT_SHEET_NAME
from pyexcel.source import AbstractSource, MemorySourceMixin
import pyexcel.constants as constants
from pyexcel.plugins.sources import params
from .common import _FakeIO, DictReader


class DictSource(AbstractSource, MemorySourceMixin):
    """
    A dictionary of one dimensional array as sheet source
    """
    fields = [params.ADICT]
    targets = (constants.SHEET, constants.BOOK)
    actions = (constants.READ_ACTION, constants.WRITE_ACTION)
    attributes = ["dict"]
    key = params.ADICT

    def __init__(self, adict, with_keys=True, sheet_name=DEFAULT_SHEET_NAME,
                 **keywords):
        self.__adict = adict
        self.__with_keys = with_keys
        self._content = _FakeIO()
        self.__sheet_name = sheet_name
        AbstractSource.__init__(self, **keywords)

    def get_data(self):
        dict_reader = DictReader(self.__adict, with_keys=self.__with_keys,
                                 **self._keywords)
        return {self.__sheet_name: dict_reader.to_array()}

    def get_source_info(self):
        return params.ADICT, None

    def write_data(self, sheet):
        self._content.setvalue(sheet.to_dict())
