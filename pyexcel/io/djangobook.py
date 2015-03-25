"""
    pyexcel.io.djangobook
    ~~~~~~~~~~~~~~~~~~~

    The lower level handler for django import and export

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io import (BookReaderBase, SheetReaderBase, BookWriter, SheetWriter)
from .._compact import OrderedDict
from .sqlbook import to_array_from_query_sets
    

class DjangoModelReader(SheetReaderBase):
    """Read from django model
    """
    def __init__(self, model):
        self.model = model

    @property
    def name(self):
        return self.model._meta.model_name

    def to_array(self):
        objects = self.model.objects.all()
        if len(objects) == 0:
            return []
        else:
            column_names = sorted([field.attname for field in self.model._meta.concrete_fields])
            return to_array_from_query_sets(column_names, objects)


class DjangoBookReader(BookReaderBase):
    """Read from a list of django models
    """
    def __init__(self, models):
        self.my_sheets = OrderedDict()
        for model in models:
            djangomodelreader = DjangoModelReader(model)
            self.my_sheets[djangomodelreader.name]=djangomodelreader.to_array()
            
    def sheets(self):
        return self.my_sheets


class DjangoModelWriter(SheetWriter):
    def __init__(self, model, batch_size=None):
        self.batch_size = batch_size
        self.mymodel = None
        self.column_names = None
        self.mapdict = None
        self.data_wrapper = None

        self.mymodel, self.column_names, self.mapdict, self.data_wrapper = model

        if self.data_wrapper is None:
            self.data_wrapper = lambda row: row
        if isinstance(self.mapdict, list):
            self.column_names = self.mapdict
            self.mapdict = None
        elif isinstance(self.mapdict, dict):
            self.column_names = [self.mapdict[name] for name in self.column_names]

        self.objs = []

    def set_sheet_name(self, name):
        pass
        
    def write_row(self, array):
        self.objs.append(self.mymodel(**dict(zip(self.column_names, self.data_wrapper(array)))))

    def close(self):
        self.mymodel.objects.bulk_create(self.objs, batch_size=self.batch_size)


class DjangoBookWriter(BookWriter):
    """Write to alist of tables
    """
    def __init__(self, file, models=None, batch_size=None, **keywords):
        BookWriter.__init__(self, file, **keywords)
        self.models = models
        self.batch_size = batch_size

    def create_sheet(self, name):
        model_params = self.models[name]
        return DjangoModelWriter(model_params, batch_size=self.batch_size)

    def close(self):
        pass