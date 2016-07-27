"""
    pyexcel.readers
    ~~~~~~~~~~~~~~~~~~~

    Uniform interface for describing a excel book

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .iterators import SheetIterator
from .sheets import Sheet, SheetStream
from .utils import to_dict, local_uuid
from ._compact import OrderedDict
import pyexcel.params as params
from .constants import (
    MESSAGE_DEPRECATED_CONTENT,
    MESSAGE_ERROR_NO_HANDLER,
    _IO_FILE_TYPE_DOC_STRING,
    _OUT_FILE_TYPE_DOC_STRING
)
from .factory import SourceFactory


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
            self.load_from_sheets(sheets)
        else:
            self.sheets = {}

    def load_from_sheets(self, sheets):
        """Load content from existing sheets

        :param dict sheets: a dictionary of sheets. Each sheet is
        a list of lists
        """
        if sheets is None:
            return
        self.sheets = OrderedDict()
        keys = sheets.keys()
        if not isinstance(sheets, OrderedDict):
            # if the end user does not care about the order
            # we put alphatical order
            keys = sorted(keys)
        for name in keys:
            sheet = SheetStream(name, sheets[name])
            # this sheets keep sheet order
            self.sheets.update({name: sheet})
            # this provide the convenience of access the sheet
            self.__dict__[name] = sheet
        self.name_array = list(self.sheets.keys())

    def save_to(self, source):
        """Save to a writeable data source"""
        source.write_data(self)

    def to_book(self):
        return Book(self.to_dict(),
                    filename=self.filename,
                    path=self.path)

    def to_dict(self):
        """
        Get book data structure as a dictionary
        """
        the_dict = OrderedDict()
        for sheet in self:
            the_dict.update({sheet.name: sheet.payload})
        return the_dict

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
        self.init(sheets=sheets, filename=filename, path=path)

    def init(self, sheets=None, filename="memory", path=None):
        self.path = path
        self.filename = filename
        self.name_array = []
        self.load_from_sheets(sheets)

    @classmethod
    def register_presentation(cls, file_type):
        getter = presenter(file_type)
        file_type_property = property(
            getter,
            doc=_OUT_FILE_TYPE_DOC_STRING.format(file_type, "Book"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)

    @classmethod
    def register_io(cls, file_type):
        getter = presenter(file_type)
        setter = importer(file_type)
        file_type_property = property(
            getter, setter,
            doc=_IO_FILE_TYPE_DOC_STRING.format(file_type, "Book"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)
        setattr(cls, 'set_%s' % file_type, setter)

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
        from .factory import SourceFactory
        out_source = SourceFactory.get_writeable_book_source(
            file_name=filename)
        self.save_to(out_source)

    def save_to_memory(self, file_type, stream=None, **keywords):
        """Save the content to a memory stream

        :param file_type: what format the stream is in
        :param stream: a memory stream.  Note in Python 3, for csv and tsv
                       format, please pass an instance of StringIO. For xls,
                       xlsx, and ods, an instance of BytesIO.
        """
        from .factory import SourceFactory
        out_source = SourceFactory.get_writeable_book_source(
            file_type=file_type,
            file_stream=stream,
            **keywords)
        self.save_to(out_source)
        return out_source.content

    def save_to_django_models(self, models,
                              initializers=None, mapdicts=None,
                              batch_size=None):
        """Save to database table through django model

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
        from .factory import SourceFactory
        out_source = SourceFactory.get_writeable_book_source(
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
        from .factory import SourceFactory
        out_source = SourceFactory.get_writeable_book_source(
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
        return self.texttable

    def __str__(self):
        return self.texttable


def presenter(file_type=None):
    def custom_presenter(self, **keywords):
        from .factory import SourceFactory
        memory_source = SourceFactory.get_writeable_book_source(
            file_type=file_type,
            **keywords)
        self.save_to(memory_source)
        return memory_source.content.getvalue()
    return custom_presenter


def importer(file_type=None):
    def custom_importer(self, content, **keywords):
        sheets, filename, path = _get_book(
            file_type=file_type,
            file_content=content,
            **keywords)
        self.init(sheets=sheets, filename=filename, path=path)

    return custom_importer


def _get_book(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    if params.DEPRECATED_CONTENT in keywords:
        print(MESSAGE_DEPRECATED_CONTENT)
        keywords[params.FILE_CONTENT] = keywords.pop(
            params.DEPRECATED_CONTENT)
    source = SourceFactory.get_book_source(**keywords)
    if source is not None:
        sheets = source.get_data()
        filename, path = source.get_source_info()
        return sheets, filename, path
    raise NotImplementedError(MESSAGE_ERROR_NO_HANDLER)
