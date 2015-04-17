"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .nominablesheet import NominableSheet


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
        """Save the content to a named file"""
        from ..source import SingleSheetFileSource
        source = SingleSheetFileSource(file_name=filename, **keywords)
        return self.save_to(source)

    def save_to_memory(self, file_type, stream, **keywords):
        """Save the content to memory

        :param str file_type: any value of 'csv', 'tsv', 'csvz',
        'tsvz', 'xls', 'xlsm', 'xslm', 'ods'
        :param iostream stream: the memory stream to be written to
        """
        self.save_as((file_type, stream), **keywords)
        return stream

    def save_to_django_model(self, model, initializer=None, mapdict=None, batch_size=None):
        """Save to database table through django model
        
        :param table: a database model or a tuple of (model, column_names, name_columns_by_row, name_rows_by_column).
                      initializer is needed when the supplied table had a custom initialization function.
                      mapdict is needed when the column headers of your sheet does not match the column names of the supplied table.
                      name_column_by_row indicates which row has column headers and by default it is the first row of the supplied sheet
        """
        from ..source import SingleSheetOutDjangoModel
        source = SingleSheetOutDjangoModel(model=model, initializer=initializer, mapdict=mapdict, batch_size=batch_size)
        self.save_to(source)

    def save_to_database(self, session, table, initializer=None, mapdict=None):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table or a tuple of (table, initializer, mapdict, name_columns_by_row, name_rows_by_column).
                      initializer is needed when the supplied table had a custom initialization function.
                      mapdict is needed when the column headers of your sheet does not match the column names of the supplied table.
                      name_column_by_row indicates which row has column headers and by default it is the first row of the supplied sheet
        """
        from ..source import SingleSheetOutSQLTable        
        source = SingleSheetOutSQLTable(
            session=session,
            table=table,
            initializer=initializer,
            mapdict=mapdict
        )
        self.save_to(source)



