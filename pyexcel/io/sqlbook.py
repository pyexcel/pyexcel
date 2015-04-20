"""
    pyexcel.io.sqlbook
    ~~~~~~~~~~~~~~~~~~~

    The lower level handler for database import and export

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io import (BookReaderBase, SheetReaderBase, BookWriter, SheetWriter)
from .._compact import OrderedDict
from ..constants import MESSAGE_INVALID_PARAMETERS


class SQLTableReader(SheetReaderBase):
    """Read a table
    """
    def __init__(self, session, table):
        self.session = session
        self.table = table

    @property
    def name(self):
        return getattr(self.table, '__tablename__', None)

    def to_array(self):
        from ..utils import from_query_sets
        objects = self.session.query(self.table).all()
        if len(objects) == 0:
            return []
        else:
            column_names = sorted([column for column in objects[0].__dict__
                                   if column != '_sa_instance_state'])
            
            return from_query_sets(column_names, objects)


class SQLBookReader(BookReaderBase):
    """Read a list of tables
    """
    def __init__(self, session=None, tables=None):
        self.my_sheets = OrderedDict()
        for table in tables:
            sqltablereader = SQLTableReader(session, table)
            self.my_sheets[sqltablereader.name]=sqltablereader.to_array()
            
    def sheets(self):
        return self.my_sheets

        
class SQLTableWriter(SheetWriter):
    """Write to a table
    """
    def __init__(self, session, table_params):
        self.session = session
        self.table = None
        self.initializer = None
        self.mapdict = None
        self.column_names = None
        if len(table_params) == 4:
            self.table, self.column_names, self.mapdict, self.initializer = table_params
        else:
            raise ValueError(MESSAGE_INVALID_PARAMETERS)

        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None

    def set_sheet_name(self, name):
        pass

    def write_row(self, array):
        row = dict(zip(self.column_names, array))
        if self.initializer:
            o = self.initializer(row)
        else:
            o = self.table()
            for name in self.column_names:
                if self.mapdict is not None:
                    key = self.mapdict[name]
                else:
                    key = name
                setattr(o, key, row[name])
        self.session.add(o)

    def write_array(self, table):
        SheetWriter.write_array(self, table)
        self.session.commit()

        
class SQLBookWriter(BookWriter):
    """Write to alist of tables
    """
    def __init__(self, file, session=None, tables=None, **keywords):
        BookWriter.__init__(self, file, **keywords)
        self.session = session
        self.tables = tables

    def create_sheet(self, name):
        table_params = self.tables[name]
        return SQLTableWriter(self.session, table_params)

    def close(self):
        pass