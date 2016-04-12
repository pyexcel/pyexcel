"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .nominablesheet import NominableSheet
from pyexcel_io.sheet import NamedContent


class SheetStream(NamedContent):
    """
    A container to hold generator as sheet content
    """
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
    def save_to(self, source):
        """Save to a writeable data source"""
        source.write_data(self)

    def save_as(self, filename, **keywords):
        """Save the content to a named file

        Heywords may vary depending on your file type, because the associated
        file type employs different library.

        for csv, `fmtparams <https://docs.python.org/release/3.1.5/
                  library/csv.html#dialects-and-formatting-parameters>`_
                  are accepted
        for xls, 'encoding' and 'style_compression' are supported
        """
        from ..sources import SourceFactory
        out_source = SourceFactory.get_writeable_source(
            file_name=filename, **keywords)
        return self.save_to(out_source)

    def save_to_memory(self, file_type, stream, **keywords):
        """Save the content to memory

        :param str file_type: any value of 'csv', 'tsv', 'csvz',
                              'tsvz', 'xls', 'xlsm', 'xslm', 'ods'
        :param iostream stream: the memory stream to be written to. Note in
                                Python 3, for csv  and tsv format, please
                                pass an instance of StringIO. For xls, xlsx,
                                and ods, an instance of BytesIO.
        """
        from ..sources import SourceFactory
        out_source = SourceFactory.get_writeable_source(
            file_type=file_type,
            file_stream=stream,
            **keywords)
        self.save_to(out_source)

    def save_to_django_model(self,
                             model,
                             initializer=None,
                             mapdict=None,
                             batch_size=None):
        """Save to database table through django model
        
        :param model: a database model
        :param initializer: a intialization functions for your model
        :param mapdict: custom map dictionary for your data columns
        :param batch_size: a parameter to Django concerning the size of data base
                           set
        """
        from ..sources import SourceFactory
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
        from ..sources import SourceFactory
        source = SourceFactory.get_writeable_source(
            session=session,
            table=table,
            initializer=initializer,
            mapdict=mapdict,
            auto_commit=auto_commit
        )
        self.save_to(source)
