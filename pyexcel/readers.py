"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
from iterators import SheetIterator
from sheets import PlainSheet, MultipleFilterableSheet, Sheet
from utils import to_dict
from io import load_file
import os
import uuid


class Book:
    """
    Read an excel book that has mutliple sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, file=None):
        """
        Book constructor

        Selecting a specific book according to file extension
        """
        self.path = ""
        self.filename = "memory"
        self.name_array = []
        self.sheets = {}
        if file and os.path.exists(file):
            self.load_from(file)

    def load_from(self, file):
        path, filename = os.path.split(file)
        self.path = path
        self.filename = filename
        book = load_file(file)
        sheets = book.sheets()
        self.load_from_sheets(sheets)

    def load_from_sheets(self, sheets):
        self.sheets = {}
        for name in sheets.keys():
            self.sheets[name] = self.get_sheet(sheets[name], name)
        self.name_array = self.sheets.keys()

    def get_sheet(self, array, name):
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
                self.name_array = self.sheets.keys()
            else:
                raise IndexError
        elif isinstance(sheet, str):
            if sheet in self.name_array:
                del self.sheets[sheet]
                self.name_array = self.sheets.keys()
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

    def __setitem__(self, key):
        pass

    def __add__(self, other):
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
        self.name_array = self.sheets.keys()
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

    def __init__(self, file=None, sheet=None):
        if file:
            self.load_file(file, sheet)
        else:
            Sheet.__init__(self, [], "memory")

    def load_file(self, file, sheet):
        book = load_file(file)
        sheets = book.sheets()
        if sheet:
            Sheet.__init__(self, sheets[sheet], sheet)
        else:
            keys = sheets.keys()
            Sheet.__init__(self, sheets[keys[0]], keys[0])


class SeriesReader(Reader):
    """
    A single sheet excel file reader and it has column headers
    """

    def __init__(self, file, sheet=None):
        Reader.__init__(self, file, sheet)
        self.become_series()


class PlainReader(PlainSheet):
    """
    PlainReader exists for speed over Reader and also for testing purposes
    """
    def __init__(self, file, sheet=None):
        book = load_file(file)
        sheets = book.sheets()
        if sheet:
            PlainSheet.__init__(self, sheets[sheet])
        else:
            keys = sheets.keys()
            PlainSheet.__init__(self, sheets[keys[0]])


class FilterableReader(MultipleFilterableSheet):
    """
    FiltableReader lets you use filters at the sequence of your choice
    """
    def __init__(self, file, sheet=None):
        book = load_file(file)
        sheets = book.sheets()
        if sheet:
            MultipleFilterableSheet.__init__(self, sheets[sheet])
        else:
            keys = sheets.keys()
            MultipleFilterableSheet.__init__(self, sheets[keys[0]])
