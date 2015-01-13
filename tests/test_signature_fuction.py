import pyexcel as pe
import pyexcel.ext.xls
import os
from db import Session, Base, Signature, engine
from _compact import OrderedDict


class TestGetSheet:
    def test_get_sheet_from_file(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        sheet = pe.get_sheet(file_name=testfile)
        assert sheet.to_array() == data
        os.unlink(testfile)
        
    def test_get_sheet_from_memory(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        content = pe.save_as(file_type="xls", array=data)
        sheet = pe.get_sheet(content=content.getvalue(), file_type="xls")
        assert sheet.to_array() == data
        
    def test_get_sheet_from_array(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.get_sheet(array=data)
        result = sheet.to_array()
        assert data == result

    def test_get_sheet_from_dict(self):
        adict = {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        sheet = pe.get_sheet(adict=adict)
        expected = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        assert expected == sheet.to_array()

    def test_get_sheet_from_records(self):
        records = [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]
        sheet = pe.get_sheet(records=records)
        expected = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        assert expected == sheet.to_array()

class TestGetArray:
    def test_get_array_from_file(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.get_array(file_name=testfile)
        assert result == data
        os.unlink(testfile)
        
    def test_get_array_from_memory(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        content = pe.save_as(file_type="xls", array=data)
        array = pe.get_array(content=content.getvalue(), file_type="xls")
        assert array == [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        
    def test_get_array_from_array(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        result = pe.get_array(array=data)
        assert result == data

    def test_get_array_from_dict(self):
        adict = {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        result = pe.get_array(adict=adict)
        expected = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        assert expected == result

    def test_get_sheet_from_recrods(self):
        records = [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]
        result = pe.get_array(records=records)
        expected = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        assert expected == result

class TestGetDict:
    def test_get_dict_from_file(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.get_dict(file_name=testfile)
        assert result == {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        os.unlink(testfile)
        
    def test_get_dict_from_memory(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        content = pe.save_as(file_type="xls", array=data)
        adict = pe.get_dict(content=content.getvalue(), file_type="xls")
        assert adict == {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        
    def test_get_dict_from_array(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        result = pe.get_dict(array=data)
        assert result == {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }

    def test_get_dict_from_dict(self):
        data = {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        result = pe.get_dict(adict=data)
        assert result == data

    def test_get_records_from_dict(self):
        data = [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]
        expected = {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        result = pe.get_dict(records=data)
        assert result == expected


class TestGetRecords:
    def test_get_dict_from_file(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.get_records(file_name=testfile)
        assert result == [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]
        os.unlink(testfile)
        
    def test_get_records_from_memory(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        content = pe.save_as(file_type="xls", array=data)
        records = pe.get_records(content=content.getvalue(), file_type="xls")
        assert records == [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]
        
    def test_get_records_from_array(self):
        data = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]
        result = pe.get_records(array=data)
        assert result == [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]

    def test_get_records_from_dict(self):
        data = {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
        result = pe.get_records(adict=data)
        assert result == [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]

    def test_get_records_from_records(self):
        data = [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]
        result = pe.get_records(records=data)
        assert result == [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]

class TestSQL:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        row1 = Signature(X=1,Y=2, Z=3)
        row2 = Signature(X=4, Y=5, Z=6)
        session =Session()
        session.add(row1)
        session.add(row2)
        session.commit()
        
    def test_get_sheet_from_sql(self):
        sheet = pe.get_sheet(session=Session(), table=Signature)
        assert sheet.to_array() == [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]

    def test_get_array_from_sql(self):
        array = pe.get_array(session=Session(), table=Signature)
        assert array == [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [4, 5, 6]
        ]

    def test_get_dict_from_sql(self):
        adict = pe.get_dict(session=Session(), table=Signature)
        assert adict == {
            "X": [1, 4],
            "Y": [2, 5],
            "Z": [3, 6]
        }
    
    def test_get_records_from_sql(self):
        records = pe.get_records(session=Session(), table=Signature)
        assert records == [
            {"X": 1, "Y": 2, "Z": 3},
            {"X": 4, "Y": 5, "Z": 6}
        ]

class TestGetBook:
    def test_get_book_from_book_dict(self):
        content = OrderedDict()
        content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        book = pe.get_book(bookdict=content)
        assert book.to_dict() == content

    def test_get_book_from_file(self):
        test_file = "test_get_book.xls"
        content = OrderedDict()
        content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        book = pe.Book(content)
        book.save_as(test_file)
        book2 = pe.get_book(file_name=test_file)
        assert book2.to_dict() == content
        os.unlink(test_file)

    def test_get_book_from_memory(self):
        content = OrderedDict()
        content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        io = pe.save_book_to_memory("xls", bookdict=content)
        book2 = pe.get_book(content=io.getvalue(), file_type="xls")
        assert book2.to_dict() == content

    def test_get_book_dict(self):
        content = OrderedDict()
        content.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
        content.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
        content.update({"Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]})
        io = pe.save_book_to_memory("xls", bookdict=content)
        adict = pe.get_book_dict(content=io.getvalue(), file_type="xls")
        assert adict == content
