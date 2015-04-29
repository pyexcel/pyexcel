import pyexcel as pe
import pyexcel.ext.xls
from _compact import OrderedDict
from nose.tools import raises

class Attributable:
    def __init__(self, adict):
        self.mydict = adict
        
    def __getattr__(self, field):
        return self.mydict[field]

class Objects:
    def __init__(self):
        self.objs = None
        
    def bulk_create(self, objs, batch_size):
        self.objs = objs
        self.batch_size = batch_size

    def all(self):
        return [Attributable(o) for o in self.objs]

class Field:
    def __init__(self, name):
        self.attname = name

class Meta:
    def __init__(self):
        self.model_name = "test"
        self.concrete_fields = []

    def update(self, data):
        for f in data:
            self.concrete_fields.append(Field(f))

class FakeDjangoModel:
    def __init__(self):
        self.objects = Objects()
        self._meta = Meta()

    def __call__(self, **keywords):
        return keywords

class TestVerticalSheet:
    def setUp(self):
        self.data = [
            ["X", 1, 4],
            ["Y", 2, 5],
            ["Z", 3, 6]
        ]
        self.result = [
            {'Y': 2, 'X': 1, 'Z': 3},
            {'Y': 5, 'X': 4, 'Z': 6}
        ]

    def test_model_save_to_django_model(self):
        model=FakeDjangoModel()
        pe.save_as(array=self.data, dest_model=model, transpose_before=True)
        assert model.objects.objs == self.result

    def test_mapping_array(self):
        data2 = [
            ["A", 1, 4],
            ["B", 2, 5],
            ["C", 3, 6]
        ]
        mapdict = ["X", "Y", "Z"]
        model=FakeDjangoModel()
        pe.save_as(array=data2, dest_model=model, dest_mapdict=mapdict, transpose_before=True)
        assert model.objects.objs == self.result

    def test_mapping_dict(self):
        data2 = [
            ["A", 1, 4],
            ["B", 2, 5],
            ["C", 3, 6]
        ]
        mapdict = {
            "C": "Z",
            "A": "X",
            "B": "Y"
        }
        model=FakeDjangoModel()
        pe.save_as(array=data2, dest_model=model, dest_mapdict=mapdict, transpose_after=True)
        assert model.objects.objs == self.result


class TestSheet:
    def setUp(self):
        self.data  = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        self.result = [
            {'Y': 2, 'X': 1, 'Z': 3},
            {'Y': 5, 'X': 4, 'Z': 6}
        ]
        
    def test_sheet_save_to_django_model(self):
        model=FakeDjangoModel()
        sheet = pe.Sheet(self.data, name_columns_by_row=0)
        sheet.save_to_django_model(model)
        assert model.objects.objs == self.result

    def test_sheet_save_to_django_model_3(self):
        model=FakeDjangoModel()
        sheet = pe.Sheet(self.data)
        sheet.name_columns_by_row(0)
        def wrapper(row):
            row[0] = row[0] + 1
            return row
        sheet.save_to_django_model(model, initializer=wrapper)
        assert model.objects.objs == [
            {'Y': 2, 'X': 2, 'Z': 3},
            {'Y': 5, 'X': 5, 'Z': 6}
        ]

    def test_model_save_to_django_model(self):
        model=FakeDjangoModel()
        pe.save_as(array=self.data, name_columns_by_row=0, dest_model=model)
        assert model.objects.objs == self.result

    def test_model_save_to_django_model_2(self):
        model=FakeDjangoModel()
        pe.save_as(array=self.data, dest_model=model)
        assert model.objects.objs == self.result

    def test_load_sheet_from_django_model(self):
        model=FakeDjangoModel()
        sheet = pe.Sheet(self.data, name_columns_by_row=0)
        sheet.save_to_django_model(model)
        assert model.objects.objs == self.result
        model._meta.update(["X", "Y", "Z"])
        sheet2 = pe.get_sheet(model=model)
        sheet2.name_columns_by_row(0)
        assert sheet2.to_records() == sheet.to_records()

    def test_mapping_array(self):
        data2 = [
            ["A", "B", "C"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        mapdict = ["X", "Y", "Z"]
        model=FakeDjangoModel()
        pe.save_as(array=data2, dest_model=model, dest_mapdict=mapdict)
        assert model.objects.objs == self.result

    def test_mapping_dict(self):
        data2 = [
            ["A", "B", "C"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        mapdict = {
            "C": "Z",
            "A": "X",
            "B": "Y"
        }
        model=FakeDjangoModel()
        pe.save_as(array=data2, dest_model=model, dest_mapdict=mapdict)
        assert model.objects.objs == self.result


class TestBook:
    def setUp(self):
        self.content = OrderedDict()
        self.content.update({"Sheet1": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        self.content.update({"Sheet2": [[u'A', u'B', u'C'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        self.result1 = [{'Y': 4, 'X': 1, 'Z': 7}, {'Y': 5, 'X': 2, 'Z': 8}, {'Y': 6, 'X': 3, 'Z': 9}]
        self.result2 = [{'B': 4, 'A': 1, 'C': 7}, {'B': 5, 'A': 2, 'C': 8}, {'B': 6, 'A': 3, 'C': 9}]

    def test_book_save_to_models(self):
        model1=FakeDjangoModel()
        model2=FakeDjangoModel()
        book = pe.Book(self.content)
        book.save_to_django_models([model1, model2])
        assert model1.objects.objs == self.result1
        assert model2.objects.objs == self.result2

    def test_module_save_to_models(self):
        model=FakeDjangoModel()
        pe.save_book_as(dest_models=[model, None, None], bookdict=self.content)
        assert model.objects.objs == self.result1

    def test_load_book_from_django_model(self):
        model=FakeDjangoModel()
        book = pe.Book(self.content)
        book.save_to_django_models([model])
        assert model.objects.objs == self.result1
        model._meta.update(["X", "Y", "Z"])
        book2 = pe.get_book(models=[model])
        assert book2[0].to_array() == book[0].to_array()
        
    def test_more_sheets_than_models(self):
        self.content.update({"IgnoreMe":[[1,2,3]]})
        model=FakeDjangoModel()
        pe.save_book_as(dest_models=[model], bookdict=self.content)
        assert model.objects.objs == self.result1

