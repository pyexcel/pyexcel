"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by C. W.
    :license: GPL v3
"""
import datetime
from ..io import load_file
from .nominablesheet import NominableSheet


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
    if sheetname:
        io_book = load_file(file, sheet_name=sheetname, **keywords)
        sheets = io_book.sheets()
    else:
        io_book = load_file(file, sheet_index=0, **keywords)
        sheets = io_book.sheets()
        keys = list(sheets.keys())
        sheetname = keys[0]
    return Sheet(sheets[sheetname],
                 sheetname,
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


def load_from_query_sets(column_names, querysets, sheet_name=None):
    array = []
    array.append(column_names)
    for o in querysets:
        new_array = []
        for column in column_names:
            value = getattr(o, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        array.append(new_array)
    return Sheet(array, name=sheet_name, name_columns_by_row=0)


def load_from_sql(session, table):
    """Constructs an instance :class:`Sheet` from database table

    :param session: SQLAlchemy session object
    :param table: SQLAlchemy database table
    :returns: :class:`Sheet`
    """
    sheet_name = getattr(table, '__tablename__', None)
    objects = session.query(table).all()
    if len(objects) == 0:
        return None
    else:
        column_names = sorted([column for column in objects[0].__dict__
                               if column != '_sa_instance_state'])
        return load_from_query_sets(column_names, objects, sheet_name)


def load_from_django_model(model):
    """Constructs an instance :class:`Sheet` from a django model

    :param model: Django model
    :returns: :class:`Sheet`
    """
    sheet_name = model._meta.model_name
    objects = model.objects.all()
    column_names = sorted([field.attname for field in model._meta.concrete_fields])
    return load_from_query_sets(column_names, objects, sheet_name)


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
              model=None,
              adict=None, with_keys=True,
              records=None,
              array=None,
              sheet_name=None,
              **keywords):
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
    loading from dictionary    adict, with_keys
    loading from records       records
    loading from array         array
    ========================== =========================================

    see also :ref:`a-list-of-data-structures`
    """
    sheet = None
    if file_name:
        sheet = load(file_name, sheet_name, **keywords)
    elif content and file_type:
        sheet = load_from_memory(file_type, content, sheet_name, **keywords)
    elif session and table:
        sheet = load_from_sql(session, table)
    elif model:
        sheet = load_from_django_model(model)
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


    def save_to_django_model(self, model, batch_size=None):
        """Save to database table through django model
        
        :param table: a database model or a tuple of (model, column_names, name_columns_by_row, name_rows_by_column).
                      table_init_func is needed when the supplied table had a custom initialization function.
                      mapdict is needed when the column headers of your sheet does not match the column names of the supplied table.
                      name_column_by_row indicates which row has column headers and by default it is the first row of the supplied sheet
        """
        mymodel = None
        column_names = None
        mapdict = None
        data_wrapper = None
        name_columns_by_row = -1
        name_rows_by_column = -1
        objs = None
        using_rows = False

        if isinstance(model, tuple):
            if len(model) == 1:
                mymodel = model[0]
            elif len(model) == 2:
                mymodel, mapdict = model
            elif len(model) == 3:
                mymodel, mapdict, data_wrapper = model
            elif len(model) == 4:
                mymodel, mapdict, data_wrapper, name_columns_by_row = model
            else:
                mymodel, mapdict, data_wrapper, name_columns_by_row, name_rows_by_column = model
        else:
            mymodel = model

        if data_wrapper is None:
            data_wrapper = lambda row: row
        if name_columns_by_row != -1:
            self.name_columns_by_row(name_columns_by_row)
        if name_rows_by_column != -1:
            self.name_rows_by_column(name_rows_by_column)

        if isinstance(mapdict, list):
            if len(self.colnames) == 0 and len(self.rownames) > 0:
                using_rows = True
            column_names = mapdict
        elif isinstance(mapdict, dict):
            if len(self.colnames) > 0:
                column_names = [mapdict[name] for name in self.colnames]
            elif len(self.rownames) > 0:
                column_names = [mapdict[name] for name in self.rownames]
                using_rows = True
        elif mapdict is None:
            if len(self.colnames) > 0:
                column_names = self.colnames
            elif len(self.rownames) > 0:
                column_names = self.rownames
                using_rows = True

        if column_names is not None:
            # by default, assume column_names for rows.
            if using_rows:
                objs = [ mymodel(**dict(zip(column_names, data_wrapper(row)))) for row in self.columns()]
            else:
                objs = [ mymodel(**dict(zip(column_names, data_wrapper(row)))) for row in self.rows()]
            mymodel.objects.bulk_create(objs, batch_size=batch_size)
        else:
            raise NameError("No column names or row names found!")
      

    def save_to_database(self, session, table):
        """Save data in sheet to database table

        :param session: database session
        :param table: a database table or a tuple of (table, table_init_func, mapdict, name_columns_by_row, name_rows_by_column).
                      table_init_func is needed when the supplied table had a custom initialization function.
                      mapdict is needed when the column headers of your sheet does not match the column names of the supplied table.
                      name_column_by_row indicates which row has column headers and by default it is the first row of the supplied sheet
        """
        mytable = None
        table_init_func = None
        mapdict = None
        name_columns_by_row = -1
        name_rows_by_column = -1
        if isinstance(table, tuple):
            if len(table) == 1:
                mytable = table[0]
            elif len(table) == 2:
                mytable, table_init_func = table
            elif len(table) == 3:
                mytable, table_init_func, mapdict = table
            elif len(table) == 4:
                mytable, table_init_func, mapdict, name_columns_by_row = table
            else:
                mytable, table_init_func, mapdict, name_columns_by_row, name_rows_by_column = table
        else:
            mytable = table
        if name_columns_by_row != -1:
            self.name_columns_by_row(name_columns_by_row)
        if name_rows_by_column != -1:
            self.name_rows_by_column(name_rows_by_column)

        if isinstance(mapdict, dict):
            if len(self.colnames) > 0:
                self._save_to_database(session, mytable, table_init_func, mapdict,
                                       self.named_rows(), self.colnames)
            elif len(self.rownames) > 0:
                self._save_to_database(session, mytable, table_init_func, mapdict,
                                       self.named_columns(), self.rownames)
            else:
                raise ValueError("No column names!")
        elif isinstance(mapdict, list):
            self._save_to_database(session, mytable, table_init_func, None,
                                   self.to_records(mapdict), mapdict)
        else:
            if len(self.colnames) > 0:
                self._save_to_database(session, mytable, table_init_func, mapdict,
                                       self.named_rows(), self.colnames)
            elif len(self.rownames) > 0:
                self._save_to_database(session, mytable, table_init_func, mapdict,
                                       self.named_columns(), self.rownames)
            else:
                self.name_columns_by_row(0)
                self._save_to_database(session, mytable, table_init_func, mapdict,
                                       self.named_rows(), self.colnames)

    def _save_to_database(self, session, table, table_init_func,
                          mapdict, iterator, keys):
        for row in iterator:
            if table_init_func:
                o = table_init_func(row)
            else:
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
