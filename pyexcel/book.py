"""
    pyexcel.book
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014-2017 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
import sys
from pyexcel.sheets import Sheet
import pyexcel._compact as compact
from pyexcel.sources import BookMeta, save_book, StreamAttribute


LOCAL_UUID = 0


class Book(compact.with_metaclass(BookMeta, object)):
    """
    Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets=None, filename="memory", path=None):
        """
        Book constructor

        Selecting a specific book according to filename extension
        :param OrderedDict/dict sheets: a dictionary of data
        :param str filename: the physical file
        :param str path: the relative path or absolute path
        :param set keywords: additional parameters to be passed on
        """
        self.init(sheets=sheets, filename=filename, path=path)

    def init(self, sheets=None, filename="memory", path=None):
        self.__path = path
        self._filename = filename
        self.__name_array = []
        self.load_from_sheets(sheets)

    @property
    def stream(self):
        """Return a stream in which the book content is properly encoded

        Example::

            >>> import pyexcel as p
            >>> b = p.get_book(bookdict={"A": [[1]]})
            >>> csv_stream = b.stream.texttable
            >>> print(csv_stream.getvalue())
            A:
            +---+
            | 1 |
            +---+

        Where b.stream.xls.getvalue() is equivalent to b.xls. In some situation
        b.stream.xls is prefered than b.xls.

        """
        return StreamAttribute(self)

    def load_from_sheets(self, sheets):
        """
        Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is
                            a list of lists
        """
        self.__sheets = compact.OrderedDict()
        if sheets is None:
            return
        keys = sheets.keys()
        if not isinstance(sheets, compact.OrderedDict):
            # if the end user does not care about the order
            # we put alphatical order
            keys = sorted(keys)
        for name in keys:
            sheet = Sheet(sheets[name], name)
            # this sheets keep sheet order
            self.__sheets.update({name: sheet})
            # this provide the convenience of access the sheet
            self.__dict__[name] = sheet
        self.__name_array = list(self.__sheets.keys())

    def __iter__(self):
        return compact.SheetIterator(self)

    def number_of_sheets(self):
        """
        Return the number of sheets
        """
        return len(self.__name_array)

    def sheet_names(self):
        """
        Return all sheet names
        """
        return self.__name_array

    def sheet_by_name(self, name):
        """
        Get the sheet with the specified name
        """
        return self.__sheets[name]

    def sheet_by_index(self, index):
        """
        Get the sheet with the specified index
        """
        if index < len(self.__name_array):
            sheet_name = self.__name_array[index]
            return self.sheet_by_name(sheet_name)

    def remove_sheet(self, sheet):
        """
        Remove a sheet
        """
        if isinstance(sheet, int):
            if sheet < len(self.__name_array):
                sheet_name = self.__name_array[sheet]
                del self.__sheets[sheet_name]
                self.__name_array = list(self.__sheets.keys())
            else:
                raise IndexError
        elif isinstance(sheet, str):
            if sheet in self.__name_array:
                del self.__sheets[sheet]
                self.__name_array = list(self.__sheets.keys())
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
        content = {}
        current_dict = self.to_dict()
        for k in current_dict.keys():
            new_key = k
            if len(current_dict.keys()) == 1:
                new_key = "%s_%s" % (self._filename, k)
            content[new_key] = current_dict[k]
        if isinstance(other, Book):
            other_dict = other.to_dict()
            for l in other_dict.keys():
                new_key = l
                if len(other_dict.keys()) == 1:
                    new_key = other._filename
                if new_key in content:
                    uid = local_uuid()
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = other_dict[l]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = local_uuid()
                new_key = "%s_%s" % (other.name, uid)
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
                    new_key = other._filename
                if new_key in self.__name_array:
                    uid = local_uuid()
                    new_key = "%s_%s" % (name, uid)
                self.__sheets[new_key] = Sheet(other[name].array,
                                               new_key)
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in self.__name_array:
                uid = local_uuid()
                new_key = "%s_%s" % (other.name, uid)
            self.__sheets[new_key] = Sheet(other.to_array(), new_key)
        else:
            raise TypeError
        self.__name_array = list(self.__sheets.keys())
        return self

    def to_dict(self):
        """Convert the book to a dictionary"""
        the_dict = compact.OrderedDict()
        for sheet in self:
            the_dict.update({sheet.name: sheet.array})
        return the_dict

    def __repr__(self):
        if compact.PY2:
            default_encoding = sys.getdefaultencoding()
            if default_encoding == "ascii":
                result = self.texttable
                return result.encode('utf-8')

        return self.texttable

    def __str__(self):
        return self.__repr__()

    def save_as(self, filename):
        """
        Save the content to a new file

        :param filename: a file path
        """
        return save_book(self, file_name=filename)

    def save_to_memory(self, file_type, stream=None, **keywords):
        """
        Save the content to a memory stream

        :param file_type: what format the stream is in
        :param stream: a memory stream.  Note in Python 3, for csv and tsv
                       format, please pass an instance of StringIO. For xls,
                       xlsx, and ods, an instance of BytesIO.
        """
        get_method = getattr(self, "get_%s_stream" % file_type)
        stream = get_method(file_stream=stream, **keywords)
        return stream

    def save_to_django_models(self, models,
                              initializers=None, mapdicts=None,
                              batch_size=None):
        """
        Save to database table through django model

        :param models: a list of database models, that is accepted by
                       :meth:`Sheet.save_to_django_model`. The sequence
                       of tables matters when there is dependencies in
                       between the tables. For example, **Car** is made
                       by **Car Maker**. **Car Maker** table should be
                       specified before **Car** table.
        :param initializers: a list of intialization functions for your
                             tables and the sequence should match tables,
        :param mapdicts: custom map dictionary for your data columns
                         and the sequence should match tables
        """
        save_book(self,
                  models=models,
                  initializers=initializers,
                  mapdicts=mapdicts,
                  batch_size=batch_size)

    def save_to_database(self, session, tables,
                         initializers=None, mapdicts=None,
                         auto_commit=True):
        """
        Save data in sheets to database tables

        :param session: database session
        :param tables: a list of database tables, that is accepted by
                       :meth:`Sheet.save_to_database`. The sequence of tables
                       matters when there is dependencies in between the
                       tables. For example, **Car** is made by **Car Maker**.
                       **Car Maker** table should
                       be specified before **Car** table.
        :param initializers: a list of intialization functions for your
                             tables and the sequence should match tables,
        :param mapdicts: custom map dictionary for your data columns
                         and the sequence should match tables
        :param auto_commit: by default, data is committed.

        """
        save_book(self,
                  session=session,
                  tables=tables,
                  initializers=initializers,
                  mapdicts=mapdicts,
                  auto_commit=auto_commit)


def to_book(bookstream):
    return Book(bookstream.to_dict(),
                filename=bookstream.filename,
                path=bookstream.path)


def local_uuid():
    global LOCAL_UUID
    LOCAL_UUID = LOCAL_UUID + 1
    return LOCAL_UUID
