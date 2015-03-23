from pyexcel_io import (BookReaderBase, SheetReaderBase, BookWriter, SheetWriter)
from .._compact import OrderedDict
import datetime


def to_array_from_query_sets(column_names, query_sets):
    array = []
    array.append(column_names)
    for o in query_sets:
        new_array = []
        for column in column_names:
            value = getattr(o, column)
            if isinstance(value, (datetime.date, datetime.time)):
                value = value.isoformat()
            new_array.append(value)
        array.append(new_array)
    return array
    

class SQLTableReader(SheetReaderBase):
    def __init__(self, session, table):
        self.session = session
        self.table = table

    @property
    def name(self):
        return getattr(self.table, '__tablename__', None)

    def to_array(self):
        objects = self.session.query(self.table).all()
        if len(objects) == 0:
            return []
        else:
            column_names = sorted([column for column in objects[0].__dict__
                                   if column != '_sa_instance_state'])
            
            return to_array_from_query_sets(column_names, objects)


class SQLBookReader(BookReaderBase):
    def __init__(self, session=None, tables=None):
        self.my_sheets = OrderedDict()
        for table in tables:
            sqltablereader = SQLTableReader(session, table)
            self.my_sheets[sqltablereader.name]=sqltablereader.to_array()
            
    def sheets(self):
        return self.my_sheets

        
class SQLTableWriter(SheetWriter):
    def __init__(self, session, table_params):
        self.session = session
        self.table = None
        self.table_init_func = None
        self.mapdict = None
        self.column_names = None
        if len(table_params) == 2:
            self.table, self.column_names = table_params
        elif len(table_params) == 3:
            self.table, self.column_names, self.table_init_func = table_params
        elif len(table_params) == 4:
            self.table, self.column_names, self.table_init_func, self.mapdict = table_params
        else:
            raise ValueError("Invalid params")

        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None

    def set_sheet_name(self, name):
        pass

    def write_row(self, array):
        row = dict(zip(self.column_names, array))
        if self.table_init_func:
            o = self.table_init_func(row)
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
    def __init__(self, file, session=None, tables=None, **keywords):
        BookWriter.__init__(self, file, **keywords)
        self.session = session
        self.tables = tables

    def create_sheet(self, name):
        table_params = self.tables[name]
        return SQLTableWriter(self.session, table_params)

    def close(self):
        pass