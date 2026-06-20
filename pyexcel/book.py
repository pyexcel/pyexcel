"""
pyexcel.book
~~~~~~~~~~~~~~~~~~~

Excel book

:copyright: (c) 2014-2026 by C Wang
:license: New BSD License, see LICENSE for more details
"""

from pyexcel.sheet import Sheet
from pyexcel._compact import OrderedDict
from pyexcel.internal.meta import BookMeta
from pyexcel.internal.common import SheetIterator

LOCAL_UUID = 0


class Book(BookMeta):
    """
    Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """

    def __init__(self, sheets=None, filename="memory", path=None):
        """
        Book constructor

        Selecting a specific book according to filename extension

        :param sheets: a dictionary of data
        :param filename: the physical file
        :param path: the relative path or absolute path
        :param keywords: additional parameters to be passed on
        """
        self.filename = None
        self.__path = None
        self.__sheets = OrderedDict()
        self.init(sheets=sheets, filename=filename, path=path)

    def init(self, sheets=None, filename="memory", path=None):
        """independent function so that it could be called multiple times"""
        self.__path = path
        self.filename = filename
        self.load_from_sheets(sheets)

    def load_from_sheets(self, sheets):
        """
        Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is
                            a list of lists
        """
        if sheets is None:
            return
        for name in sheets.keys():
            value = sheets[name]
            if isinstance(value, Sheet):
                sheet = value
                sheet.name = name
            else:
                # array
                sheet = Sheet(value, name)
            # this sheets keep sheet order
            self.__sheets.update({name: sheet})
            # this provide the convenience of access the sheet
            self.__dict__[name.replace(" ", "_")] = sheet

    def __iter__(self):
        return SheetIterator(self)

    def __len__(self):
        return len(self.__sheets)

    def sort_sheets(self, key=None, reverse=False):
        sorted_sheet_names = sorted(
            self.__sheets.keys(), key=key, reverse=reverse
        )
        self.__sheets = OrderedDict(
            (sheet_name, self.__sheets[sheet_name])
            for sheet_name in sorted_sheet_names
        )

    def number_of_sheets(self):
        """
        Return the number of sheets
        """
        return len(self.__sheets)

    def sheet_names(self):
        """
        Return all sheet names
        """
        return list(self.__sheets.keys())

    def sheet_by_name(self, name):
        """
        Get the sheet with the specified name
        """
        return self.__sheets[name]

    def sheet_by_index(self, index):
        """
        Get the sheet with the specified index
        """
        sheet_names = self.sheet_names()
        if index < len(sheet_names):
            sheet_name = sheet_names[index]
            return self.sheet_by_name(sheet_name)

    def remove_sheet(self, sheet):
        """
        Remove a sheet
        """
        if isinstance(sheet, int):
            sheet_names = self.sheet_names()
            if sheet < len(sheet_names):
                sheet_name = sheet_names[sheet]
                del self.__sheets[sheet_name]
            else:
                raise IndexError
        elif isinstance(sheet, str):
            if sheet in self.__sheets:
                del self.__sheets[sheet]
            else:
                raise KeyError
        else:
            raise TypeError

    def __getitem__(self, key):
        """Override operator[]"""
        if isinstance(key, int):
            return self.sheet_by_index(key)
        return self.sheet_by_name(key)

    def __delitem__(self, other):
        """
        Override del book[index]
        """
        self.remove_sheet(other)
        return self

    def __add__(self, other):
        """
        Override operator +

        example::

            book3 = book1 + book2
            book3 = book1 + book2["Sheet 1"]

        """
        content = OrderedDict()
        current_dict = self.to_dict()
        if len(current_dict) == 1:
            for single_key in current_dict.keys():
                new_key = f"{self.filename}_{single_key}"
                content[new_key] = current_dict[single_key]
        else:
            content.update(current_dict)
        if isinstance(other, Book):
            other_dict = other.to_dict()
            for key in other_dict.keys():
                if len(other_dict.keys()) == 1:
                    new_key = f"{other.filename}_{key}"
                else:
                    new_key = key
                if new_key in content:
                    uid = local_uuid()
                    new_key = f"{key}_{uid}"
                content[new_key] = other_dict[key]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = local_uuid()
                new_key = f"{other.name}_{uid}"
            content[new_key] = other.array
        else:
            raise TypeError
        output = Book()
        output.load_from_sheets(content)
        return output

    def __iadd__(self, other):
        """
        Operator overloading +=

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
                if new_key in self.__sheets:
                    uid = local_uuid()
                    new_key = f"{name}_{uid}"
                self.__sheets[new_key] = Sheet(other[name].array, new_key)
        elif isinstance(other, Sheet):
            self._add_a_sheet(other)
        else:
            raise TypeError
        return self

    def _add_a_sheet(self, sheet):
        """
        Add a sheet to the book

        :param sheet: an instance of Sheet
        """
        new_key = sheet.name
        if new_key in self.__sheets:
            uid = local_uuid()
            new_key = f"{sheet.name}_{uid}"
        self.__sheets[new_key] = Sheet(sheet.array, new_key)

    def to_dict(self):
        """Convert the book to a dictionary"""
        the_dict = OrderedDict()
        for sheet in self:
            the_dict.update({sheet.name: sheet.array})
        return the_dict


def to_book(bookstream):
    """Convert a bookstream to Book"""
    if isinstance(bookstream, Book):
        return bookstream
    return Book(
        bookstream.to_dict(),
        filename=bookstream.filename,
        path=bookstream.path,
    )


def local_uuid():
    """create home made uuid"""
    global LOCAL_UUID
    LOCAL_UUID = LOCAL_UUID + 1
    return LOCAL_UUID
