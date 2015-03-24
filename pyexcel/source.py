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
        from utils import from_records
        return 'pyexcel_sheet1', from_records(self.records)


class SingleSheetDictSource(SingleSheetDataSource):
    def __init__(self, adict, with_keys=True):
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self, **keywords):
        from utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return 'pyexcel_sheet1', tmp_array


class SingleSheetQuerySetSource(SingleSheetDataSource):
    def __init__(self, sheet_name, column_names, query_sets):
        self.sheet_name = sheet_name
        self.column_names = column_names
        self.query_sets = query_sets

    def get_data(self, **keywords):
        array = []
        array.append(self.column_names)
        for o in self.query_sets:
            new_array = []
            for column in self.column_names:
                value = getattr(o, column)
                if isinstance(value, (datetime.date, datetime.time)):
                    value = value.isoformat()
                new_array.append(value)
            array.append(new_array)
        return self.sheet_name, array


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
