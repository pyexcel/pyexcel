"""
    pyexcel.sheets
    ~~~~~~~~~~~~~~~~~~~

    Representation of data sheets

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License
"""
from io import load_file
import datetime

FILE_STORAGE = 1
MEMORY_STORAGE = 2
DATABASE_STORAGE = 3

class SingleSheetDataSource:
    def __init__(self, storage):
        self.storage = storage

    def get_data(self):
        return []


class SingleSheetFile(SingleSheetDataSource):
    def __init__(self, file_name, sheet_name=None, sheet_index=None):
        SingleSheetDataSource.__init__(self, FILE_STORAGE)
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
        keys = sheets.keys()
        return {keys[0]: sheets[keys[0]]}


class SingleSheetRecrodsSource(SingleSheetDataSource):
    def __init__(self, records):
        SingleSheetDataSource.__init__(self, MEMORY_STORAGE)
        self.records = records

    def get_data(self, **keywords):
        from utils import from_records
        return {'pyexcel_sheet1': from_records(self.records)}


class SingleSheetDictSource(SingleSheetDataSource):
    def __init__(self, adict, with_keys=True):
        SingleSheetDataSource.__init__(self, MEMORY_STORAGE)
        self.adict = adict
        self.with_keys = with_keys

    def get_data(self, **keywords):
        from utils import dict_to_array
        tmp_array = dict_to_array(self.adict, self.with_keys)
        return {'pyexcel_sheet1': tmp_array}


class SingleSheetQuerySetSource(SingleSheetDataSource):
    def __init__(self, sheet_name, column_names, query_sets):
        SingleSheetDataSource.__init__(self, DATABASE_STORAGE)
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
        return {self.sheet_name: array}


class SingleSheetSQLAlchemySource(SingleSheetDataSource):
    def __init__(self, session, table):
        SingleSheetDataSource.__init__(self, DATABASE_STORAGE)
        self.session = session
        self.table = table

    def get_data(self, **keywords):
        sheet_name = getattr(self.table, '__tablename__', None)
        objects = self.session.query(self.table).all()
        if len(objects) == 0:
            return None
        else:
            column_names = sorted([column for column in objects[0].__dict__
                                   if column != '_sa_instance_state'])
            ssqss = SingleSheetQuerySetSource(sheet_name, column_names, objects)
            return ssqss.get_data()


class SingleSheetDjangoSource(SingleSheetDataSource):
    def __init__(self, model):
        SingleSheetDataSource.__init__(self, DATABASE_STORAGE)
        self.model = model

    def get_data(self, **keywords):
        sheet_name = self.model._meta.model_name
        objects = self.model.objects.all()
        column_names = sorted([field.attname for field in self.model._meta.concrete_fields])
        ssqss = SingleSheetQuerySetSource(sheet_name, column_names, objects)
        return ssqss.get_data()

