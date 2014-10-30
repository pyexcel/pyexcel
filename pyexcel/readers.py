"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from .iterators import SheetIterator
from .sheets import PlainSheet, MultipleFilterableSheet, RowSeriesSheet, is_string, Sheet
from .utils import to_dict
from .io import load_file
import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
import os
import uuid


class Book:
    """
    Read an excel book that has mutliple sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, filename=None, **keywords):
        """
        Book constructor

        Selecting a specific book according to filename extension
        """
        self.path = ""
        self.filename = "memory"
        self.name_array = []
        self.sheets = {}
        if is_string(type(filename)):
            if filename and os.path.exists(filename):
                self.load_from(filename, **keywords)
        elif isinstance(filename, tuple):
            self.load_from_memory(filename, **keywords)

    def load_from(self, file, **keywords):
        """Load content from physical file

        :param str file: the file name
        :param any keywords: additional parameters
        """
        path, filename = os.path.split(file)
        self.path = path
        self.filename = filename
        book = load_file(file, **keywords)
        sheets = book.sheets()
        self.load_from_sheets(sheets)

    def load_from_memory(self, the_tuple, **keywords):
        """Load content from memory content

        :param tuple the_tuple: first element should be file extension,
        second element should be file content
        :param any keywords: additional parameters
        """
        book = load_file(the_tuple, **keywords)
        sheets = book.sheets()
        self.load_from_sheets(sheets)

    def load_from_sheets(self, sheets):
        """Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is
        a list of lists
        """
        self.sheets = OrderedDict()
        for name in sheets.keys():
            self.sheets[name] = self.get_sheet(sheets[name], name)
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
        if type(key) == int:
            return self.sheet_by_index(key)
        else:
            return self.sheet_by_name(key)

    def __delitem__(self, other):
        self.remove_sheet(other)
        return self

    def __add__(self, other):
        """Operator overloading

        example::

            book3 = book1 + book2
            book3 = book1 + book2["Sheet 1"]

        """
        content = {}
        a = to_dict(self)
        for k in a.keys():
            new_key = k
            if len(a.keys()) == 1:
                new_key = "%s_%s" % (self.filename, k)
            content[new_key] = a[k]
        if isinstance(other, Book):
            b = to_dict(other)
            for l in b.keys():
                new_key = l
                if len(b.keys()) == 1:
                    new_key = other.filename
                if new_key in content:
                    uid = uuid.uuid4().hex
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = b[l]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = uuid.uuid4().hex
                new_key = "%s_%s" % (other.name, uid)
            content[new_key] = other.array
        else:
            raise TypeError
        c = Book()
        c.load_from_sheets(content)
        return c

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
                    uid = uuid.uuid4().hex
                    new_key = "%s_%s" % (name, uid)
                self.sheets[new_key] = self.get_sheet(other[name].array,
                                                      new_key)
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in self.name_array:
                uid = uuid.uuid4().hex
                new_key = "%s_%s" % (other.name, uid)
            self.sheets[new_key] = self.get_sheet(other.array, new_key)
        else:
            raise TypeError
        self.name_array = list(self.sheets.keys())
        return self


class BookReader(Book):
    """
    For backward compatibility
    """
    pass


class Reader(Sheet):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next
    """

    def __init__(self, file=None, sheet=None, **keywords):
        if file:
            self.load_file(file, sheet, **keywords)
        else:
            Sheet.__init__(self, [], "memory")

    def load_file(self, file, sheet=None, **keywords):
        """
        Load only one sheet from the file

        :param str file: the file name
        :param str sheet: the sheet to be used as the default sheet
        """
        book = load_file(file, **keywords)
        sheets = book.sheets()
        if sheet:
            Sheet.__init__(self, sheets[sheet], sheet)
        else:
            keys = sorted(list(sheets.keys()))
            Sheet.__init__(self, sheets[keys[0]], keys[0])


class SeriesReader(RowSeriesSheet):
    """
    A single sheet excel file reader and it has column headers
    """
    def __init__(self, file=None, sheet=None, series=0, **keywords):
        if file:
            self.load_file(file, sheet, series, **keywords)
        else:
            RowSeriesSheet.__init__(self, [], "memory", 0)

    def load_file(self, file, sheet=None, series=0, **keywords):
        """
        Load only one sheet from the file

        :param str file: the file name
        :param str sheet: the sheet to be used as the default sheet
        """
        book = load_file(file, **keywords)
        sheets = book.sheets()
        if sheet:
            RowSeriesSheet.__init__(self, sheets[sheet], sheet, series)
        else:
            keys = list(sheets.keys())
            RowSeriesSheet.__init__(self, sheets[keys[0]], keys[0], series)


class PlainReader(PlainSheet):
    """
    PlainReader exists for speed over Reader and also for testing purposes
    """
    def __init__(self, file, sheet=None, **keywords):
        book = load_file(file, **keywords)
        sheets = book.sheets()
        if sheet:
            PlainSheet.__init__(self, sheets[sheet])
        else:
            keys = list(sheets.keys())
            PlainSheet.__init__(self, sheets[keys[0]])


class FilterableReader(MultipleFilterableSheet):
    """
    FiltableReader lets you use filters at the sequence of your choice
    """
    def __init__(self, file, sheet=None, **keywords):
        book = load_file(file, **keywords)
        sheets = book.sheets()
        if sheet:
            MultipleFilterableSheet.__init__(self, sheets[sheet])
        else:
            keys = list(sheets.keys())
            MultipleFilterableSheet.__init__(self, sheets[keys[0]])
