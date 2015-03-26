"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from .nominablesheet import NominableSheet
from ..source import (SingleSheetFile,
                      SingleSheetRecrodsSource,
                      SingleSheetDictSource,
                      SingleSheetQuerySetSource,
                      SingleSheetSQLAlchemySource,
                      SingleSheetDjangoSource)

def load(file, sheetname=None,
         name_columns_by_row=-1,
         name_rows_by_column=-1,
         colnames=None,
         rownames=None,
         **keywords):
    """Constructs an instance :class:`Sheet` from a sheet of an excel file

    except csv, most excel files has more than one sheet.
    Hence sheetname is required here to indicate from which sheet the instance
    should be constructed. If this parameter is omitted, the first sheet, which
    is indexed at 0, is used. For csv, sheetname is always omitted because csv
    file contains always one sheet.
    :param str sheetname: which sheet to be used for construction
    :param int name_colmns_by_row: which row to give column names
    :param int name_rows_by_column: which column to give row names
    :param dict keywords: other parameters
    """
    ssf = SingleSheetFile(file, sheet_name=sheetname)
    sheet_name, content = ssf.get_data(**keywords)
    return Sheet(content,
                 sheet_name,
                 name_columns_by_row=name_columns_by_row,
                 name_rows_by_column=name_rows_by_column,
                 colnames=colnames,
                 rownames=rownames
             )


def load_from_memory(file_type,
                     file_content,
                     sheetname=None,
                     **keywords):
    """Constructs an instance :class:`Sheet` from memory

    :param str file_type: one value of these: 'csv', 'tsv', 'csvz',
    'tsvz', 'xls', 'xlsm', 'xslm', 'ods'
    :param iostream file_content: file content
    :param str sheetname: which sheet to be used for construction
    :param dict keywords: any other parameters
    """
    return load((file_type, file_content), sheetname, **keywords)

def load_from_query_sets(column_names, query_sets):
    """Constructs an instance :class:`Sheet` from a database query sets
    :param column_names: the field names
    :param query_sets: the values
    :returns: :class:`Sheet`
    """
    ssqss = SingleSheetQuerySetSource(column_names, query_sets)
    sheet_name, content = ssqss.get_data()
    return Sheet(content, sheet_name, name_columns_by_row=0)

def load_from_sql(session, table):
    """Constructs an instance :class:`Sheet` from database table

    :param session: SQLAlchemy session object
    :param table: SQLAlchemy database table
    :returns: :class:`Sheet`
    """
    sssqls = SingleSheetSQLAlchemySource(session, table)
    sheet_name, content = sssqls.get_data()
    if sheet_name:
        return Sheet(content,
                     sheet_name,
                     name_columns_by_row=0)
    else:
        return None


def load_from_django_model(model):
    """Constructs an instance :class:`Sheet` from a django model

    :param model: Django model
    :returns: :class:`Sheet`
    """
    ssds = SingleSheetDjangoSource(model)
    sheet_name, content = ssds.get_data()
    return Sheet(content,
                 sheet_name,
                 name_columns_by_row=0
    )


def load_from_dict(the_dict, with_keys=True):
    """Return a sheet from a dictionary of one dimensional arrays

    :param dict the_dict: its value should be one dimensional array
    :param bool with_keys: indicate if dictionary keys should be appended or not
    """
    ssds = SingleSheetDictSource(the_dict)
    sheet_name, content = ssds.get_data()
    sheet = Sheet(content, sheet_name)
    if with_keys:
        sheet.name_columns_by_row(0)
    return sheet


def load_from_records(records):
    """Return a sheet from a list of records

    Sheet.to_records() would produce a list of dictionaries. All dictionaries
    share the same keys.
    :params list records: records are likely to be produced by Sheet.to_records()
    method.
    """
    ssrs = SingleSheetRecrodsSource(records)
    sheet_name, content = ssrs.get_data()
    return Sheet(content, sheet_name, name_columns_by_row=0)


#def get_sheet(file_name=None, content=None, file_type=None,
#              session=None, table=None,
#              model=None,
#              adict=None, with_keys=True,
#              column_names=None, query_sets=None,
#              records=None,
#              array=None,
#              sheet_name=None,
    #              **keywords):
def get_sheet(**keywords):
    """Get an instance of :class:`Sheet` from an excel source

    :param file_name: a file with supported file extension
    :param content: the file content
    :param file_type: the file type in *content*
    :param session: database session
    :param table: database table
    :param model: a django model
    :param adict: a dictionary of one dimensional arrays
    :param with_keys: load with previous dictionary's keys, default is True
    :param records: a list of dictionaries that have the same keys
    :param array: a two dimensional array, a list of lists
    :param keywords: additional parameters, see :meth:`Sheet.__init__`
    :param sheet_name: sheet name. if sheet_name is not given, the default sheet
                       at index 0 is loaded

    Not all parameters are needed. Here is a table

    ========================== =========================================
    loading from file          file_name, sheet_name, keywords
    loading from memory        file_type, content, sheet_name, keywords
    loading from sql           session ,table
    loading from sql in django django model
    loading from query sets    any query sets(sqlalchemy or django)
    loading from dictionary    adict, with_keys
    loading from records       records
    loading from array         array
    ========================== =========================================

    see also :ref:`a-list-of-data-structures`
    """
    sheet = None
    sheet_name = keywords.get('sheet_name', None)
    def has_field(field, keywords):
        return field in keywords and keywords[field]
    if has_field('file_name', keywords):
        if sheet_name is not None:
            keywords.pop('sheet_name')
        sheet = load(keywords.pop('file_name'), sheet_name, **keywords)
    elif has_field('content', keywords) and has_field('file_type', keywords):
        if sheet_name is not None:
            keywords.pop('sheet_name')
        sheet = load_from_memory(keywords.pop('file_type'), keywords.pop('content'), sheet_name, **keywords)
    elif has_field('session', keywords) and has_field('table', keywords):
        sheet = load_from_sql(keywords.pop('session'), keywords.pop('table'))
    elif has_field('column_names', keywords) and has_field('query_sets', keywords):
        sheet = load_from_query_sets(keywords.pop('column_names'), keywords.pop('query_sets'), **keywords)
    elif has_field('model', keywords):
        sheet = load_from_django_model(keywords.pop('model'))
    elif has_field('adict', keywords):
        sheet = load_from_dict(keywords.pop('adict'), keywords.get('with_key', True))
    elif has_field('records', keywords):
        sheet = load_from_records(keywords.pop('records'))
    elif has_field('array', keywords):
        sheet = Sheet(keywords.pop('array'), **keywords)
    return sheet


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
    def save_as(self, filename, **keywords):
        """Save the content to a named file"""
        from ..writers import Writer
        w = Writer(filename, sheet_name=self.name, **keywords)
        w.write_reader(self)
        w.close()


    def save_to_memory(self, file_type, stream, **keywords):
        """Save the content to memory

        :param str file_type: any value of 'csv', 'tsv', 'csvz',
        'tsvz', 'xls', 'xlsm', 'xslm', 'ods'
        :param iostream stream: the memory stream to be written to
        """
        self.save_as((file_type, stream), **keywords)


    def save_to_django_model(self, model, data_wrapper=None, mapdict=None, batch_size=None):
        """Save to database table through django model
        
        :param table: a database model or a tuple of (model, column_names, name_columns_by_row, name_rows_by_column).
                      table_init_func is needed when the supplied table had a custom initialization function.
                      mapdict is needed when the column headers of your sheet does not match the column names of the supplied table.
                      name_column_by_row indicates which row has column headers and by default it is the first row of the supplied sheet
        """
        from ..writers import Writer
        if len(self.colnames) == 0:
            self.name_columns_by_row(0)
        w = Writer('django', sheet_name=self.name, models={self.name:(model, self.colnames, mapdict, data_wrapper)}, batch_size=batch_size)
        w.write_array(self.array)
        w.close()

    def save_to_database(self, session, table, table_init_func=None, mapdict=None):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table or a tuple of (table, table_init_func, mapdict, name_columns_by_row, name_rows_by_column).
                      table_init_func is needed when the supplied table had a custom initialization function.
                      mapdict is needed when the column headers of your sheet does not match the column names of the supplied table.
                      name_column_by_row indicates which row has column headers and by default it is the first row of the supplied sheet
        """
        from ..writers import Writer
        w = Writer('sql', sheet_name=self.name, session=session, tables={self.name: (table, self.colnames, table_init_func, mapdict)})
        w.write_array(self.array)
        w.close()


def Reader(file=None, sheetname=None, **keywords):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next

    use as class would fail though
    changed since 0.0.7
    """
    return load(file, sheetname=sheetname, **keywords)


def SeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has column headers in a selected row

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname=sheetname, name_columns_by_row=series, **keywords)


def ColumnSeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has row headers in a selected column

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname=sheetname, name_rows_by_column=series, **keywords)
