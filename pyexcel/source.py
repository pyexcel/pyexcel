"""
    pyexcel.source
    ~~~~~~~~~~~~~~~~~~~

    Representation of incoming data source

    :copyright: (c) 2015 by Onni Software Ltd.
    :license: New BSD License
"""
from .io import load_file
import datetime
from ._compact import PY2
from sheets import Sheet


class SingleSheetDataSource:
    def get_data(self):
        return []


def one_sheet_tuple(items):
    if not PY2:
        items = list(items)
    if len(items[0][1]) == 0:
        return None, None
    else:
        return items[0][0], items[0][1]
    
        
class SingleSheetFile(SingleSheetDataSource):
    def __init__(self, file_name, sheet_name=None, sheet_index=None):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.sheet_index = sheet_index

    def get_data(self, **keywords):
        """
        Return a dictionary with only one key and one value
        """
        if self.sheet_name:
            io_book = load_file(self.file_name, sheet_name=self.sheet_name, **keywords)
            sheets = io_book.sheets()
        else:
            if self.sheet_index:
                sheet_index = self.sheet_index
            else:
                sheet_index = 0
            io_book = load_file(self.file_name, sheet_index=sheet_index, **keywords)
            sheets = io_book.sheets()
        return one_sheet_tuple(sheets.items())


class SingleSheetRecrodsSource(SingleSheetDataSource):
    def __init__(self, records):
        self.records = records

    def get_data(self, **keywords):
        from .utils import from_records
        return 'pyexcel_sheet1', from_records(self.records)


class SingleSheetDictSource(SingleSheetDataSource):
    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self, **keywords):
        from .utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return 'pyexcel_sheet1', tmp_array


class SingleSheetQuerySetSource(SingleSheetDataSource):
    def __init__(self, column_names, query_sets, sheet_name=None):
        self.sheet_name = sheet_name
        if self.sheet_name is None:
            self.sheet_name = 'pyexcel_sheet1'
        self.column_names = column_names
        self.query_sets = query_sets

    def get_data(self, **keywords):
        from .utils import from_query_sets
        return self.sheet_name, from_query_sets(self.column_names, self.query_sets)


class SingleSheetDatabaseSourceMixin(SingleSheetDataSource):
    def get_sql_book():
        pass
        
    def get_data(self, **keywords):
        sql_book = self.get_sql_book()
        sheets = sql_book.sheets()
        return one_sheet_tuple(sheets.items())


class SingleSheetSQLAlchemySource(SingleSheetDatabaseSourceMixin):
    def __init__(self, session, table):
        self.session = session
        self.table = table

    def get_sql_book(self):
        return load_file('sql', session=self.session, tables=[self.table])


class SingleSheetDjangoSource(SingleSheetDatabaseSourceMixin):
    def __init__(self, model):
        self.model = model

    def get_sql_book(self):
        return load_file('django', models=[self.model])


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


def Reader(file=None, sheetname=None, **keywords):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next

    use as class would fail though
    changed since 0.0.7
    """
    print("Deprecated. Please use class Sheet instead")
    return load(file, sheetname=sheetname, **keywords)


def SeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has column headers in a selected row

    use as class would fail
    changed since 0.0.7
    """
    print("Deprecated. Please use class Sheet(..., name_columns_by_row=0,..) instead")
    return load(file, sheetname=sheetname, name_columns_by_row=series, **keywords)


def ColumnSeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has row headers in a selected column

    use as class would fail
    changed since 0.0.7
    """
    print("Deprecated. Please use class Sheet(..., name_rows_by_column=0..) instead")
    return load(file, sheetname=sheetname, name_rows_by_column=series, **keywords)
