"""
    pyexcel.internal.meta
    ~~~~~~~~~~~~~~~~~~~~~~

    Annotate sheet and book class' attributes

    :copyright: (c) 2015-2017 by Onni Software Ltd.
    :license: New BSD License
"""
import sys
from functools import partial

from pyexcel._compact import PY2
from pyexcel.internal import SOURCE
import pyexcel.constants as constants
from pyexcel.internal.core import get_sheet_stream
from pyexcel.internal.core import save_sheet
from pyexcel.internal.core import save_book


def make_presenter(source_getter, attribute=None):
    """make a custom presentation method for each file types
    """
    def custom_presenter(self, **keywords):
        """docstring is assigned a few lines down the line"""
        keyword = SOURCE.get_keyword_for_parameter(attribute)
        keywords[keyword] = attribute
        memory_source = source_getter(**keywords)
        memory_source.write_data(self)
        try:
            content_stream = memory_source.get_content()
            content = content_stream.getvalue()
        except AttributeError:
            # python 3 _io.TextWrapper
            content = None

        return content
    custom_presenter.__doc__ = "Get data in %s format" % attribute
    return custom_presenter


def sheet_presenter(attribute=None):
    """make a custom presentation method for sheet
    """
    source_getter = SOURCE.get_writable_source
    return make_presenter(source_getter, attribute)


def book_presenter(attribute=None):
    """make a custom presentation method for book
    """
    source_getter = SOURCE.get_writable_book_source
    return make_presenter(source_getter, attribute)


def importer(attribute=None):
    """make a custom input method for sheet
    """
    def custom_importer1(self, content, **keywords):
        """docstring is assigned a few lines down the line"""
        sheet_params = {}
        for field in constants.VALID_SHEET_PARAMETERS:
            if field in keywords:
                sheet_params[field] = keywords.pop(field)
        keyword = SOURCE.get_keyword_for_parameter(attribute)
        if keyword == "file_type":
            keywords[keyword] = attribute
            keywords["file_content"] = content
        else:
            keywords[keyword] = content
        named_content = get_sheet_stream(**keywords)
        self.init(named_content.payload,
                  named_content.name, **sheet_params)
    custom_importer1.__doc__ = "Set data in %s format" % attribute
    return custom_importer1


def book_importer(attribute=None):
    """make a custom input method for book
    """
    def custom_book_importer(self, content, **keywords):
        """docstring is assigned a few lines down the line"""
        keyword = SOURCE.get_keyword_for_parameter(attribute)
        if keyword == "file_type":
            keywords[keyword] = attribute
            keywords["file_content"] = content
        else:
            keywords[keyword] = content
        sheets, filename, path = _get_book(**keywords)
        self.init(sheets=sheets, filename=filename, path=path)
    custom_book_importer.__doc__ = "Set data in %s format" % attribute
    return custom_book_importer


def default_presenter(attribute=None):
    """a default method for missing renderer method

    for example, the support to write data in a specific file type
    is missing but the support to read data exists
    """
    def none_presenter(_, **__):
        """docstring is assigned a few lines down the line"""
        raise NotImplementedError("%s getter is not defined." % attribute)
    none_presenter.__doc__ = "%s getter is not defined." % attribute
    return none_presenter


def default_importer(attribute=None):
    """a default method for missing parser method

    for example, the support to read data in a specific file type
    is missing but the support to write data exists
    """
    def none_importer(_, __, **___):
        """docstring is assigned a few lines down the line"""
        raise NotImplementedError("%s setter is not defined." % attribute)
    none_importer.__doc__ = "%s setter is not defined." % attribute
    return none_importer


def _annotate_pyexcel_object_attribute(
        cls, file_type, presenter_func=sheet_presenter,
        input_func=default_importer,
        instance_name="Sheet",
        description=constants.OUT_FILE_TYPE_DOC_STRING):
    getter = presenter_func(file_type)
    setter = input_func(file_type)
    file_type_property = property(
        # note:
        # without fget, fset, pypy 5.4.0 crashes randomly.
        fget=getter, fset=setter,
        doc=description.format(file_type,
                               instance_name))
    if '.' in file_type:
        attribute = file_type.replace('.', '_')
    else:
        attribute = file_type
    setattr(cls, attribute, file_type_property)
    setattr(cls, 'get_%s' % attribute, getter)
    setattr(cls, 'set_%s' % attribute, setter)


REGISTER_PRESENTATION = _annotate_pyexcel_object_attribute
REGISTER_BOOK_PRESENTATION = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=book_presenter,
    instance_name="Book")
REGISTER_INPUT = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=default_presenter,
    input_func=importer,
    description=constants.IN_FILE_TYPE_DOC_STRING)
REGISTER_BOOK_INPUT = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=default_presenter,
    input_func=book_importer,
    instance_name="Book",
    description=constants.IN_FILE_TYPE_DOC_STRING)
REGISTER_IO = partial(
    _annotate_pyexcel_object_attribute,
    input_func=importer,
    description=constants.IO_FILE_TYPE_DOC_STRING)
REGISTER_BOOK_IO = partial(
    _annotate_pyexcel_object_attribute,
    presenter_func=book_presenter,
    input_func=book_importer,
    instance_name="Book",
    description=constants.IO_FILE_TYPE_DOC_STRING)


class StreamAttribute(object):
    """Provide access to get_*_stream methods"""
    def __init__(self, cls):
        self.cls = cls

    def __getattr__(self, name):
        getter = getattr(self.cls, 'save_to_memory')
        return getter(file_type=name)


class PyexcelObject(object):
    """parent class for pyexcel.Sheet and pyexcel.Book"""
    @property
    def stream(self):
        """Return a stream in which the content is properly encoded

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

        Sheet examples::

            >>> import pyexcel as p
            >>> s = p.Sheet([[1]], 'A')
            >>> csv_stream = s.stream.texttable
            >>> print(csv_stream.getvalue())
            A:
            +---+
            | 1 |
            +---+

        Where s.stream.xls.getvalue() is equivalent to s.xls. In some situation
        s.stream.xls is prefered than s.xls.

        It is similar to :meth:`~pyexcel.Book.save_to_memory`.
        """
        return StreamAttribute(self)

    def __repr__(self):
        if PY2:
            default_encoding = sys.getdefaultencoding()
            if default_encoding == "ascii":
                result = self.texttable
                return result.encode('utf-8')

        return self.texttable

    def __str__(self):
        return self.__repr__()

    def save_to_memory(self):
        """Save the content to memory

        :param file_type: any value of 'csv', 'tsv', 'csvz',
                          'tsvz', 'xls', 'xlsm', 'xlsm', 'ods'
        :param stream: the memory stream to be written to. Note in
                       Python 3, for csv  and tsv format, please
                       pass an instance of StringIO. For xls, xlsx,
                       and ods, an instance of BytesIO.
        """
        raise NotImplementedError("save to memory is not implemented")

    def plot(self, file_type='svg', **keywords):
        io = self.save_to_memory(file_type, **keywords)
        if file_type in ['png', 'svg', 'jpeg']:
            def get_content(self):
                return self.getvalue().decode('utf-8')

            setattr(io, '_repr_%s_' % file_type, get_content)
        return io

    def _repr_html_(self):
        return self.html

    def _repr_json_(self):
        return self.json


class SheetMeta(PyexcelObject):
    """Annotate sheet attributes"""
    def save_as(self, filename, **keywords):
        """Save the content to a named file

        Keywords may vary depending on your file type, because the associated
        file type employs different library.

        for csv, `fmtparams <https://docs.python.org/release/3.1.5/
        library/csv.html#dialects-and-formatting-parameters>`_ are accepted

        for xls, 'auto_detect_int', 'encoding' and 'style_compression' are
        supported

        for ods, 'auto_detect_int' is supported
        """
        return save_sheet(self, file_name=filename,
                          **keywords)

    def save_to_memory(self, file_type, stream=None, **keywords):
        stream = save_sheet(self, file_type=file_type, file_stream=stream,
                            **keywords)
        return stream

    def save_to_django_model(self,
                             model,
                             initializer=None,
                             mapdict=None,
                             batch_size=None):
        """Save to database table through django model

        :param model: a database model
        :param initializer: a initialization functions for your model
        :param mapdict: custom map dictionary for your data columns
        :param batch_size: a parameter to Django concerning the size
                           for bulk insertion
        """
        save_sheet(self,
                   model=model, initializer=initializer,
                   mapdict=mapdict, batch_size=batch_size)

    def save_to_database(self, session, table,
                         initializer=None,
                         mapdict=None,
                         auto_commit=True):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table
        :param initializer: a initialization functions for your table
        :param mapdict: custom map dictionary for your data columns
        :param auto_commit: by default, data is auto committed.

        """
        save_sheet(self,
                   session=session,
                   table=table,
                   initializer=initializer,
                   mapdict=mapdict,
                   auto_commit=auto_commit)


setattr(SheetMeta, "register_io", classmethod(REGISTER_IO))
setattr(SheetMeta, "register_presentation", classmethod(REGISTER_PRESENTATION))
setattr(SheetMeta, "register_input", classmethod(REGISTER_INPUT))


class BookMeta(PyexcelObject):
    """Annotate book attributes"""
    def save_as(self, filename, **keywords):
        """
        Save the content to a new file

        :param filename: a file path
        """
        return save_book(self, file_name=filename, **keywords)

    def save_to_memory(self, file_type, stream=None, **keywords):
        """
        Save the content to a memory stream

        :param file_type: what format the stream is in
        :param stream: a memory stream.  Note in Python 3, for csv and tsv
                       format, please pass an instance of StringIO. For xls,
                       xlsx, and ods, an instance of BytesIO.
        """
        stream = save_book(self, file_type=file_type, file_stream=stream,
                           **keywords)
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


setattr(BookMeta, "register_io", classmethod(REGISTER_BOOK_IO))
setattr(BookMeta, "register_presentation",
        classmethod(REGISTER_BOOK_PRESENTATION))
setattr(BookMeta, "register_input",
        classmethod(REGISTER_BOOK_INPUT))


def _get_book(**keywords):
    """Get an instance of :class:`Book` from an excel source

    Where the dictionary should have text as keys and two dimensional
    array as values.
    """
    a_source = SOURCE.get_book_source(**keywords)
    sheets = a_source.get_data()
    filename, path = a_source.get_source_info()
    return sheets, filename, path
