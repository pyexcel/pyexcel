"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
import datetime
from ..io import load_file
from .nominablesheet import NominableSheet


def load(file, sheetname=None,
         name_columns_by_row=-1,
         name_rows_by_column=-1,
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
    book = load_file(file, **keywords)
    sheets = book.sheets()
    if sheetname:
        if sheetname not in sheets:
            raise KeyError("%s is not found" % sheetname)
    else:
        keys = list(sheets.keys())
        sheetname = keys[0]
    return Sheet(sheets[sheetname],
                 sheetname,
                 name_columns_by_row=name_columns_by_row,
                 name_rows_by_column=name_rows_by_column)


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


def load_from_sql(session, table):
    """Constructs from database table

    :param sqlalchemy.orm.Session session: SQLAlchemy session object
    :param sqlalchemy orm table table: SQLAlchemy database table
    :returns: :class:`Sheet`
    """
    array = []
    sheet_name = getattr(table, '__tablename__', None)
    objects = session.query(table).all()
    column_names = sorted([column for column in objects[0].__dict__
                           if column != '_sa_instance_state'])
    array.append(column_names)
    for o in objects:
        new_array = []
        for column in column_names:
            value = getattr(o, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        array.append(new_array)
    return Sheet(array, name=sheet_name, name_columns_by_row=0)


def load_from_dict(the_dict, with_keys=True):
    """Return a sheet from a dictionary of one dimensional arrays

    :param dict the_dict: its value should be one dimensional array
    :param bool with_keys: indicate if dictionary keys should be appended or not
    """
    from ..utils import dict_to_array
    tmp_array = dict_to_array(the_dict, with_keys)
    sheet = Sheet(tmp_array)
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
    from ..utils import from_records
    tmp_array = from_records(records)
    sheet = Sheet(tmp_array, name_columns_by_row=0)
    return sheet


def get_sheet(file_name=None, content=None, file_type=None,
              session=None, table=None,
              adict=None, with_keys=True,
              records=None,
              array=None,
              **keywords):
    """Get an instance of :class:`Sheet` from an excel source

    :param file_name: a file with supported file extension
    :param content: the file content
    :param file_type: the file type in *content*
    :param session: database session
    :param table: database table
    :param adict: a dictionary of one dimensional arrays
    :param with_keys: load with previous dictionary's keys, default is True
    :param records: a list of dictionaries that have the same keys
    :param array: a two dimensional array, a list of lists
    :param keywords: additional parameters, see :meth:`Sheet.__init__`
    see also :ref:`a-list-of-data-structures`
    """
    sheet = None
    if file_name:
        sheet = load(file_name, **keywords)
    elif content and file_type:
        sheet = load_from_memory(file_type, content, **keywords)
    elif session and table:
        sheet = load_from_sql(session, table)
    elif adict:
        sheet = load_from_dict(adict, with_keys)
    elif records:
        sheet = load_from_records(records)
    elif array:
        sheet = Sheet(array, **keywords)
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

    def save_to_database(self, session, table, mapdict=None):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table
        :param mapdict: provide key mapping if default ones are different
        """
        if len(self.colnames) > 0:
            self._save_to_database(session, table, mapdict,
                                   self.named_rows(), self.colnames)
        elif len(self.rownames) > 0:
            self._save_to_database(session, table, mapdict,
                                   self.named_columns(), self.rownames)

    def _save_to_database(self, session, table, mapdict, iterator, keys):
        for row in iterator:
            o = table()
            for name in keys:
                if mapdict:
                    key = mapdict[name]
                else:
                    key = name
                setattr(o, key, row[name])
            session.add(o)
        session.commit()


def Reader(file=None, sheetname=None, **keywords):
    """
    A single sheet excel file reader

    Default is the sheet at index 0. Or you specify one using sheet index
    or sheet name. The short coming of this reader is: column filter is
    applied first then row filter is applied next

    use as class would fail though
    changed since 0.0.7
    """
    return load(file, sheetname, **keywords)


def SeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has column headers in a selected row

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname, name_columns_by_row=series, **keywords)


def ColumnSeriesReader(file=None, sheetname=None, series=0, **keywords):
    """A single sheet excel file reader and it has row headers in a selected column

    use as class would fail
    changed since 0.0.7
    """
    return load(file, sheetname, name_rows_by_column=series, **keywords)
