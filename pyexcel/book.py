"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .iterators import SheetIterator
from .sheets import Sheet
from .utils import to_dict, local_uuid
from ._compact import OrderedDict
from .presentation import outsource


class BookStream(object):
    """Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets=None, filename="memory", path=None):
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
        if sheets:
            self.sheets = sheets
        else:
            self.sheets = {}
        self.name_array = list(self.sheets.keys())

    def save_to(self, source):
        """Save to a writeable data source"""
        from .sources import BookDjangoSource, BookSQLSource
        if isinstance(source, BookDjangoSource) or isinstance(source, BookSQLSource):
            book = Book(self.sheets,
                        filename=self.filename,
                        path=self.path)
            source.write_data(book)
        else:
            source.write_data(self)

    def to_dict(self):
        """
        Get book data structure as a dictionary
        """
        return self.sheets

    def __iter__(self):
        return SheetIterator(self)

    def number_of_sheets(self):
        """Return the number of sheets"""
        return len(self.name_array)

    def __getitem__(self, index):
        if index < len(self.name_array):
            sheet_name = self.name_array[index]
            return self.sheets[sheet_name]


class Book(object):
    """Read an excel book that has one or more sheets

    For csv file, there will be just one sheet
    """
    def __init__(self, sheets=None, filename="memory", path=None):
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
        current_dict = to_dict(self)
        for k in current_dict.keys():
            new_key = k
            if len(current_dict.keys()) == 1:
                new_key = "%s_%s" % (self.filename, k)
            content[new_key] = current_dict[k]
        if isinstance(other, Book):
            other_dict = to_dict(other)
            for l in other_dict.keys():
                new_key = l
                if len(other_dict.keys()) == 1:
                    new_key = other.filename
                if new_key in content:
                    uid = local_uuid()
                    new_key = "%s_%s" % (l, uid)
                content[new_key] = other_dict[l]
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in content:
                uid = local_uuid()
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
                    uid = local_uuid()
                    new_key = "%s_%s" % (name, uid)
                self.sheets[new_key] = self.get_sheet(other[name].to_array(),
                                                      new_key)
        elif isinstance(other, Sheet):
            new_key = other.name
            if new_key in self.name_array:
                uid = local_uuid()
                new_key = "%s_%s" % (other.name, uid)
            self.sheets[new_key] = self.get_sheet(other.to_array(), new_key)
        else:
            raise TypeError
        self.name_array = list(self.sheets.keys())
        return self

    def save_to(self, source):
        """Save to a writeable data source"""
        source.write_data(self)

    def save_as(self, filename):
        """Save the content to a new file

        :param str filename: a file path
        """
        from .sources import BookSource
        out_source = BookSource(file_name=filename)
        self.save_to(out_source)

    def save_to_memory(self, file_type, stream, **keywords):
        """Save the content to a memory stream

        :param file_type: what format the stream is in
        :param stream: a memory stream.  Note in Python 3, for csv and tsv
                       format, please pass an instance of StringIO. For xls,
                       xlsx, and ods, an instance of BytesIO.
        """
        self.save_as((file_type, stream), **keywords)

    def save_to_django_models(self, models,
                              initializers=None, mapdicts=None, batch_size=None):
        """Save to database table through django model

        :param models: a list of database models, that is accepted by
                       :meth:`Sheet.save_to_django_model`. The sequence of tables
                       matters when there is dependencies in between the tables.
                       For example, **Car** is made by **Car Maker**. **Car Maker**
                       table should be specified before **Car** table.
        :param initializers: a list of intialization functions for your talbes and
                             the sequence should match tables,
        :param mapdicts: custom map dictionary for your data columns and the sequence should
                   match tables
        """
        from .sources import BookDjangoSource
        out_source = BookDjangoSource(
            models=models,
            initializers=initializers,
            mapdicts=mapdicts,
            batch_size=batch_size
        )
        self.save_to(out_source)

    def save_to_database(self, session, tables,
                         initializers=None, mapdicts=None,
                         auto_commit=True):
        """Save data in sheets to database tables

        :param session: database session
        :param tables: a list of database tables, that is accepted by
                       :meth:`Sheet.save_to_database`. The sequence of tables matters
                       when there is dependencies in between the tables. For example,
                       **Car** is made by **Car Maker**. **Car Maker** table should
                       be specified before **Car** table.
        :param initializers: a list of intialization functions for your tables and
                             the sequence should match tables,
        :param mapdicts: custom map dictionary for your data columns and the sequence should
                   match tables
        :param auto_commit: by default, data is committed.

        """
        from .sources import BookSQLSource
        out_source = BookSQLSource(
            session=session,
            tables=tables,
            initializers=initializers,
            mapdicts=mapdicts,
            auto_commit=auto_commit
        )
        self.save_to(out_source)

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
