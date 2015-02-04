import pyexcel as pe
import pyexcel.ext.xls
import os
from db import Session, Base, Signature, Signature2, engine
from _compact import OrderedDict
from nose.tools import raises


class Objects:
    def __init__(self):
        self.objs = None
        
    def bulk_create(self, objs, batch_size):
        print("called")
        self.objs = objs
        self.batch_size = batch_size

class FakeDjangoModel:
    def __init__(self):
        self.objects = Objects()

class TestDjango:
    @raises(NameError)
    def test_get_array(self):
        model=FakeDjangoModel()
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.Sheet(data)
        sheet.save_to_django_model(model)
        import pdb; pdb.set_trace()
        assert model.objects.objs == data
