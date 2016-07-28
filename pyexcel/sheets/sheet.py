"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io.sheet import NamedContent
from .nominablesheet import NominableSheet, VALID_SHEET_PARAMETERS
import pyexcel.params as params
from pyexcel.factory import SourceFactory
from pyexcel.constants import (
    MESSAGE_DEPRECATED_CONTENT,
    MESSAGE_ERROR_NO_HANDLER,
    _IO_FILE_TYPE_DOC_STRING,
    _OUT_FILE_TYPE_DOC_STRING
)
from pyexcel._compact import PY2


class SheetStream(NamedContent):
    """
    A container to hold generator as sheet content
    """
    def __init__(self, name, payload):
        NamedContent.__init__(self, name, payload)
        self.colnames = []

    def save_to(self, source):
        """Save to a writeable data source"""
        source.write_data(self)

    def to_array(self):
        """
        Simply return the generator
        """
        return self.payload


class Sheet(NominableSheet):
    """Two dimensional data container for filtering, formatting and iteration

    :class:`Sheet` is a container for a two dimensional array, where individual
    cell can be any Python types. Other than numbers, value of thsee
    types: string, date, time and boolean can be mixed in the array. This
    differs from Numpy's matrix where each cell are of the same number type.

    In order to prepare two dimensional data for your computation, formatting
    functions help convert array cells to required types. Formatting can be
    applied not only to the whole sheet but also to selected rows or columns.
    Custom conversion function can be passed to these formatting functions. For
    example, to remove extra spaces surrounding the content of a cell, a custom
    function is required.

    Filtering functions are used to reduce the information contained in the
    array.
    """
    class _RepresentedString:
        def __init__(self, text):
            self.text = text

        def __repr__(self):
            return self.text

        def __str__(self):
            return self.text

    @classmethod
    def register_presentation(cls, file_type):
        getter = presenter(file_type)
        file_type_property = property(
            getter,
            doc=_OUT_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)

    @classmethod
    def register_io(cls, file_type):
        getter = presenter(file_type)
        setter = importer(file_type)
        file_type_property = property(
            getter, setter,
            doc=_IO_FILE_TYPE_DOC_STRING.format(file_type, "Sheet"))
        setattr(cls, file_type, file_type_property)
        setattr(cls, 'get_%s' % file_type, getter)
        setattr(cls, 'set_%s' % file_type, setter)

    def __repr__(self):
        return self.texttable

    def __str__(self):
        return self.texttable

    @property
    def content(self):
        """
        Plain representation without headers
        """
        content = self.get_texttable(write_title=False)
        return self._RepresentedString(content)

    def save_to(self, source):
        """Save to a writeable data source"""
        source.write_data(self)

    def save_as(self, filename, **keywords):
        """Save the content to a named file

        Heywords may vary depending on your file type, because the associated
        file type employs different library.

        for csv, `fmtparams <https://docs.python.org/release/3.1.5/
        library/csv.html#dialects-and-formatting-parameters>`_ are accepted

        for xls, 'auto_detect_int', 'encoding' and 'style_compression' are
        supported

        for ods, 'auto_dtect_int' is supported
        """
        from ..factory import SourceFactory
        out_source = SourceFactory.get_writeable_source(
            file_name=filename, **keywords)
        return self.save_to(out_source)

    def save_to_memory(self, file_type, stream=None, **keywords):
        """Save the content to memory

        :param str file_type: any value of 'csv', 'tsv', 'csvz',
                              'tsvz', 'xls', 'xlsm', 'xslm', 'ods'
        :param iostream stream: the memory stream to be written to. Note in
                                Python 3, for csv  and tsv format, please
                                pass an instance of StringIO. For xls, xlsx,
                                and ods, an instance of BytesIO.
        """
        from ..factory import SourceFactory
        out_source = SourceFactory.get_writeable_source(
            file_type=file_type,
            file_stream=stream,
            **keywords)
        self.save_to(out_source)
        return out_source.content

    def save_to_django_model(self,
                             model,
                             initializer=None,
                             mapdict=None,
                             batch_size=None):
        """Save to database table through django model

        :param model: a database model
        :param initializer: a intialization functions for your model
        :param mapdict: custom map dictionary for your data columns
        :param batch_size: a parameter to Django concerning the size
                           of data base set
        """
        from ..factory import SourceFactory
        source = SourceFactory.get_writeable_source(
            model=model, initializer=initializer,
            mapdict=mapdict, batch_size=batch_size)
        self.save_to(source)

    def save_to_database(self, session, table,
                         initializer=None,
                         mapdict=None,
                         auto_commit=True):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table
        :param initializer: a intialization functions for your table
        :param mapdict: custom map dictionary for your data columns
        :param auto_commit: by default, data is committed.

        """
        from ..factory import SourceFactory
        source = SourceFactory.get_writeable_source(
            session=session,
            table=table,
            initializer=initializer,
            mapdict=mapdict,
            auto_commit=auto_commit
        )
        self.save_to(source)


def presenter(file_type=None):
    def custom_presenter(self, **keywords):
        from ..factory import SourceFactory
        memory_source = SourceFactory.get_writeable_source(file_type=file_type,
                                                           **keywords)
        self.save_to(memory_source)
        return memory_source.content.getvalue()
    return custom_presenter


def importer(file_type=None):
    def custom_presenter1(self, content, **keywords):
        sheet_params = {}
        for field in VALID_SHEET_PARAMETERS:
            if field in keywords:
                sheet_params[field] = keywords.pop(field)
        named_content = _get_content(file_type=file_type, file_content=content,
                                     **keywords)
        self.init(named_content.payload,
                  named_content.name, **sheet_params)

    return custom_presenter1


def _get_content(**keywords):
    if params.DEPRECATED_CONTENT in keywords:
        print(MESSAGE_DEPRECATED_CONTENT)
        keywords[params.FILE_CONTENT] = keywords.pop(
            params.DEPRECATED_CONTENT)
    source = SourceFactory.get_source(**keywords)
    if source is not None:
        sheets = source.get_data()
        sheet_name, data = _one_sheet_tuple(sheets.items())
        return SheetStream(sheet_name, data)
    raise NotImplementedError(MESSAGE_ERROR_NO_HANDLER)


def _one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    return items[0][0], items[0][1]
