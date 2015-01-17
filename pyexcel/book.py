"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import os
import uuid
from .iterators import SheetIterator
from .sheets import Sheet, load_from_sql
from .utils import to_dict
from .io import load_file
from ._compact import OrderedDict
from .presentation import outsource


def load_book(file, **keywords):
    """Load content from physical file

    :param str file: the file name
    :param any keywords: additional parameters
    """
    path, filename = os.path.split(file)
    book = load_file(file, **keywords)
    sheets = book.sheets()
    return Book(sheets, filename, path, **keywords)


def load_book_from_memory(file_type, file_content, **keywords):
    """Load content from memory content

    :param tuple the_tuple: first element should be file extension,
    second element should be file content
    :param any keywords: additional parameters
    """
    book = load_file((file_type, file_content), **keywords)
    sheets = book.sheets()
    return Book(sheets, **keywords)


def load_book_from_sql(session, tables):
    """Get an instance of :class:`Book` from a list of tables
    """
    book = Book()
    for table in tables:
        sheet = load_from_sql(session, table)
        book += sheet
    return book


def get_book(file_name=None, content=None, file_type=None, session=None, tables=None, bookdict=None, **keywords):
    """Get an instance of :class:`Book` from an excel source

    :param file_name: a file with supported file extension
    :param content: the file content
    :param file_type: the file type in *content*
    :param session: database session
    :param table: database table
    :param bookdict: a dictionary of two dimensional arrays
    see also :ref:`a-list-of-data-structures`
    """
    book = None
    if file_name:
        book = load_book(file_name, **keywords)
    elif content and file_type:
        book = load_book_from_memory(file_type, content, **keywords)
    elif session and tables:
        book = load_book_from_sql(session, tables)
    elif bookdict:
        book = Book(bookdict)
    return book
    

class Book(object):
    """Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets={}, filename="memory", path=None, **keywords):
        """Book constructor

        Selecting a specific book according to filename extension
        :param OrderedDict/dict sheets: a dictionary of data
        :param str filename: the physical file
        :param str path: the relative path or abosolute path
        :param set keywords: additional parameters to be passed on
        """
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
        keys = sheets.keys()
        if not isinstance(sheets, OrderedDict):
            # if the end user does not care about the order
            # we put alphatical order
            keys = sorted(keys)
        for name in keys:
            self.sheets.update({name: self.get_sheet(sheets[name], name)})
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
        if type(key) == int:
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

    def save_as(self, filename):
        """Save the content to a new file

        :param str filename: a file path
        """
        from .writers import BookWriter
        writer = BookWriter(filename)
        writer.write_book_reader(self)
        writer.close()

    def save_to_memory(self, file_type, stream):
        """Save the content to a memory stream

        :param iostream stream: a memory stream
        """
        from .writers import BookWriter
        writer = BookWriter((file_type, stream))
        writer.write_book_reader(self)
        writer.close()

    def save_to_database(self, session, tables, mapdicts=None):
        for i in range(0, self.number_of_sheets()):
            sheet = self.sheet_by_index(i)
            if len(sheet.colnames) == 0 and len(sheet.rownames) == 0:
                sheet.name_colmns_by_row(0)
            if mapdicts and i < len(mapdicts):
                sheet.save_to_database(session, tables[i], mapdicts[i])
            else:
                sheet.save_to_database(session, tables[i], None)

    def to_dict(self):
        """Convert the book to a dictionary"""
        from .utils import to_dict
        return to_dict(self)

    def __repr__(self):
        return self.__str__()

    @outsource
    def __str__(self):
        ret = ""
        for sheet in self.sheets:
            ret += str(self.sheets[sheet])
            ret += "\n"
        return ret.strip('\n')


def BookReader(file, **keywords):
    """For backward compatibility
    """
    return load_book(file, **keywords)
