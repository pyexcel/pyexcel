"""
    pyexcel.book
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import pyexcel.utils as utils
from pyexcel.sheets.iterators import SheetIterator
from pyexcel.sheets import Sheet
from pyexcel._compact import OrderedDict
from pyexcel.sources import BookMixin


class Book(BookMixin):
    """Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets=None, filename="memory", path=None):
        """Book constructor

        Selecting a specific book according to filename extension
        :param OrderedDict/dict sheets: a dictionary of data
        :param str filename: the physical file
        :param str path: the relative path or absolute path
        :param set keywords: additional parameters to be passed on
        """
        self.init_attributes()
        self.init(sheets=sheets, filename=filename, path=path)

    def init(self, sheets=None, filename="memory", path=None):
        self.path = path
        self.filename = filename
        self.name_array = []
        self.load_from_sheets(sheets)

    def load_from_sheets(self, sheets):
        """Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is
        a list of lists
        """
        self.sheets = OrderedDict()
        if sheets is None:
            return
        keys = sheets.keys()
        if not isinstance(sheets, OrderedDict):
            # if the end user does not care about the order
            # we put alphatical order
            keys = sorted(keys)
        for name in keys:
            sheet = self.get_sheet(sheets[name], name)
            # this sheets keep sheet order
            self.sheets.update({name: sheet})
            # this provide the convenience of access the sheet
            self.__dict__[name] = sheet
        self.name_array = list(self.sheets.keys())

    def get_sheet(self, array, name):
        """Create a sheet from a list of lists"""
        return Sheet(array, name)

    def __iter__(self):
        return SheetIterator(self)

    def number_of_sheets(self):
        """Return the number of sheets"""
        return len(self.name_array)

    def sheet_names(self):
        """Return all sheet names"""
        return self.name_array

    def sheet_by_name(self, name):
        """Get the sheet with the specified name"""
        return self.sheets[name]

    def sheet_by_index(self, index):
        """Get the sheet with the specified index"""
        if index < len(self.name_array):
            sheet_name = self.name_array[index]
            return self.sheets[sheet_name]

    def remove_sheet(self, sheet):
        """Remove a sheet"""
        if isinstance(sheet, int):
            if sheet < len(self.name_array):
                sheet_name = self.name_array[sheet]
                del self.sheets[sheet_name]
                self.name_array = list(self.sheets.keys())
            else:
                raise IndexError
        elif isinstance(sheet, str):
            if sheet in self.name_array:
                del self.sheets[sheet]
                self.name_array = list(self.sheets.keys())
            else:
                raise KeyError
        else:
            raise TypeError

    def __getitem__(self, key):
        """Override operator[]"""
        if isinstance(key, int):
            return self.sheet_by_index(key)
        else:
            return self.sheet_by_name(key)

    def __delitem__(self, other):
        """Override del book[index]"""
        self.remove_sheet(other)
        return self

    def __add__(self, other):
        """Override operator +

        example::

            book3 = book1 + book2
            book3 = book1 + book2["Sheet 1"]

        """
        content = {}
        current_dict = utils.to_dict(self)
        for k in current_dict.keys():
            new_key = k
            if len(current_dict.keys()) == 1:
                new_key = "%s_%s" % (self.filename, k)
            content[new_key] = current_dict[k]
        if isinstance(other, Book):
            other_dict = utils.to_dict(other)
            for l in other_dict.keys():
                new_key = l
                if len(other_dict.keys()) == 1:
                    new_key = other.filename
                if new_key in content:
                    uid = utils.local_uuid()
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = other_dict[l]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = utils.local_uuid()
                new_key = "%s_%s" % (other.name, uid)
            content[new_key] = other.to_array()
        else:
            raise TypeError
        output = Book()
        output.load_from_sheets(content)
        return output

    def __iadd__(self, other):
        """Operator overloading +=

        example::

            book += book2
            book += book2["Sheet1"]

        """
        if isinstance(other, Book):
            names = other.sheet_names()
            for name in names:
                new_key = name
                if len(names) == 1:
                    new_key = other.filename
                if new_key in self.name_array:
                    uid = utils.local_uuid()
                    new_key = "%s_%s" % (name, uid)
                self.sheets[new_key] = self.get_sheet(other[name].to_array(),
                                                      new_key)
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in self.name_array:
                uid = utils.local_uuid()
                new_key = "%s_%s" % (other.name, uid)
            self.sheets[new_key] = self.get_sheet(other.to_array(), new_key)
        else:
            raise TypeError
        self.name_array = list(self.sheets.keys())
        return self

    def to_dict(self):
        """Convert the book to a dictionary"""
        from .utils import to_dict
        return to_dict(self)

    def __repr__(self):
        return self.texttable

    def __str__(self):
        return self.texttable


def to_book(bookstream):
    return Book(bookstream.to_dict(),
                filename=bookstream.filename,
                path=bookstream.path)
