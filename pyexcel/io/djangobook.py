"""
    pyexcel.io.djangobook
    ~~~~~~~~~~~~~~~~~~~

    The lower level handler for django import and export

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
"""
from pyexcel_io import (BookReaderBase, SheetReaderBase, BookWriter, SheetWriter)
from .._compact import OrderedDict
import datetime
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

