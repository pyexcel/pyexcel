import os
from types import GeneratorType

import pyexcel as pe
from db import Base, Session, Signature, Signature2, engine
from _compact import OrderedDict

from nose.tools import eq_, raises


def test_unknown_file_type_exception():
    content = [[1]]
    msg = "File type 'hd5' is not supported for write."
    try:
        pe.save_as(array=content, dest_file_name="test.hd5")
    except pe.exceptions.FileTypeNotSupported as e:
        eq_(str(e), msg)


def test_unknown_parameter_exception():
    msg = "Please check if there were typos in "
    msg += "function parameters: %s. Otherwise "
    msg += "unrecognized parameters were given."

    unknown_parameter = dict(something="else")

    try:
        pe.get_sheet(**unknown_parameter)
    except pe.exceptions.UnknownParameters as e:
        eq_(str(e), msg % unknown_parameter)

    try:
        pe.save_as(**unknown_parameter)
    except pe.exceptions.UnknownParameters as e:
        eq_(str(e), msg % unknown_parameter)

    try:
        pe.save_book_as(**unknown_parameter)
    except pe.exceptions.UnknownParameters as e:
        eq_(str(e), msg % unknown_parameter)

    try:
        pe.isave_as(**unknown_parameter)
    except pe.exceptions.UnknownParameters as e:
        eq_(str(e), msg % unknown_parameter)
    pe.free_resources()


def test_out_file_parameter():
    try:
        pe.save_as(array=[[1]], out_file="b", colnames=["X", "Y", "Z"])
    except pe.exceptions.UnknownParameters as e:
        eq_(str(e), "No parameters found!")


def test_nominal_parameters():
    try:
        pe.get_records("something")
    except pe.exceptions.UnknownParameters as e:
        eq_(str(e), "No parameters found!")


class TestGetSheet:
    def test_get_sheet_from_file(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        sheet = pe.get_sheet(file_name=testfile)
        assert sheet.to_array() == data
        os.unlink(testfile)

    def test_get_sheet_from_file_stream(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        content = pe.save_as(dest_file_type="xls", array=data)
        sheet = pe.get_sheet(file_stream=content, file_type="xls")
        assert sheet.to_array() == data

    def test_get_sheet_from_memory(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        content = pe.save_as(dest_file_type="xls", array=data)
        sheet = pe.get_sheet(file_content=content.getvalue(), file_type="xls")
        assert sheet.to_array() == data

    @raises(IOError)
    def test_get_sheet_from_memory_compatibility(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        content = pe.save_as(dest_file_type="xls", array=data)
        pe.get_sheet(content=content.getvalue(), file_type="xls")

    def test_get_sheet_from_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.get_sheet(array=data)
        result = sheet.to_array()
        assert data == result

    def test_get_sheet_from_dict(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        sheet = pe.get_sheet(adict=adict)
        expected = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        assert expected == sheet.to_array()

    def test_get_sheet_from_records(self):
        records = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        sheet = pe.get_sheet(records=records)
        expected = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        assert expected == sheet.to_array()

    def test_get_sheet_from_txt(self):
        test_file = os.path.join("tests", "fixtures", "force_type.txt")
        sheet = pe.get_sheet(file_name=test_file, force_file_type="csv")
        expected = [[1, 2, 3]]
        eq_(sheet.to_array(), expected)


class TestGetArray:
    def setUp(self):
        self.test_data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]

    def test_get_array_from_file(self):
        sheet = pe.Sheet(self.test_data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.get_array(file_name=testfile)
        eq_(result, self.test_data)
        os.unlink(testfile)

    def test_get_array_from_memory(self):
        content = pe.save_as(dest_file_type="xls", array=self.test_data)
        array = pe.get_array(file_content=content.getvalue(), file_type="xls")
        eq_(array, self.test_data)

    def test_get_array_from_array(self):
        result = pe.get_array(array=self.test_data)
        eq_(result, self.test_data)

    def test_get_array_from_dict(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.get_array(adict=adict)
        eq_(result, self.test_data)

    def test_get_sheet_from_recrods(self):
        records = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        result = pe.get_array(records=records)
        eq_(result, self.test_data)


class TestiGetArray:
    def setUp(self):
        self.test_data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]

    def tearDown(self):
        pe.free_resources()

    def test_get_array_from_file(self):
        sheet = pe.Sheet(self.test_data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.iget_array(file_name=testfile)
        eq_(list(result), self.test_data)
        os.unlink(testfile)

    def test_get_array_from_memory(self):
        content = pe.save_as(dest_file_type="xls", array=self.test_data)
        array = pe.get_array(file_content=content.getvalue(), file_type="xls")
        eq_(array, self.test_data)

    def test_get_array_from_array(self):
        result = pe.iget_array(array=self.test_data)
        eq_(list(result), self.test_data)

    def test_get_array_from_dict(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.iget_array(adict=adict)
        eq_(list(result), self.test_data)

    def test_get_sheet_from_recrods(self):
        records = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        result = pe.iget_array(records=records)
        eq_(list(result), self.test_data)


class TestGetDict:
    def test_get_dict_from_file(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.get_dict(file_name=testfile)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        os.unlink(testfile)

    def test_get_dict_from_memory(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        content = pe.save_as(dest_file_type="xls", array=data)
        adict = pe.get_dict(file_content=content.getvalue(), file_type="xls")
        assert adict == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_get_dict_from_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = pe.get_dict(array=data)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_get_dict_from_dict(self):
        data = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.get_dict(adict=data)
        assert result == data

    def test_get_dict_from_records(self):
        data = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        expected = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.get_dict(records=data)
        assert result == expected


class TestGetRecords:
    def test_get_records_from_file(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.get_records(file_name=testfile)
        eq_(result, [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])
        os.unlink(testfile)

    def test_get_records_from_memory(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        content = pe.save_as(dest_file_type="xls", array=data)
        records = pe.get_records(
            file_content=content.getvalue(), file_type="xls"
        )
        eq_(records, [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])

    def test_get_records_from_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = pe.get_records(array=data)
        eq_(result, [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])

    def test_get_records_from_dict(self):
        data = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.get_records(adict=data)
        eq_(result, [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])

    def test_get_records_from_records(self):
        data = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        result = pe.get_records(records=data)
        eq_(result, [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])


class TestiGetRecords:
    def tearDown(self):
        pe.free_resources()

    def test_get_records_from_file(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        sheet.save_as(testfile)
        result = pe.iget_records(file_name=testfile)
        eq_(list(result), [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])
        os.unlink(testfile)

    def test_get_records_from_memory(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        content = pe.save_as(dest_file_type="xls", array=data)
        records = pe.get_records(
            file_content=content.getvalue(), file_type="xls"
        )
        eq_(
            list(records), [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        )

    def test_get_records_from_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = pe.iget_records(array=data)
        eq_(list(result), [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])

    def test_get_records_from_irregular_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5]]
        result = pe.iget_records(array=data)
        eq_(
            list(result), [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": ""}]
        )

    def test_get_records_from_dict(self):
        data = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.iget_records(adict=data)
        eq_(list(result), [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])

    def test_get_records_from_records(self):
        data = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        result = pe.iget_records(records=data)
        eq_(list(result), [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}])


class TestSavingToDatabase:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    def test_save_a_dict(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        sheet = pe.get_sheet(adict=adict, name_columns_by_row=0)
        sheet.save_to_database(self.session, Signature)
        result = pe.get_dict(session=self.session, table=Signature)
        assert adict == result

    def test_save_a_dict2(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        sheet = pe.get_sheet(adict=adict, name_columns_by_row=0)
        sheet.save_to_database(self.session, Signature)
        result = pe.get_dict(
            session=self.session, table=Signature, name_columns_by_row=0
        )
        print(result)
        assert adict == result

    def test_save_a_dict3(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        sheet = pe.get_sheet(adict=adict, name_columns_by_row=0)
        sheet.save_to_database(self.session, Signature)
        result = pe.get_dict(session=self.session, table=(Signature))
        assert adict == result

    def test_save_an_array(self):
        data = [[1, 4, "X"], [2, 5, "Y"], [3, 6, "Z"]]
        sheet = pe.Sheet(data)
        sheet.transpose()
        sheet.name_columns_by_row(2)
        sheet.save_to_database(self.session, Signature)
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_save_an_array2(self):
        data = [[1, 4, "A"], [2, 5, "B"], [3, 6, "C"]]
        sheet = pe.Sheet(data)
        sheet.transpose()
        sheet.name_columns_by_row(2)
        mapdict = {"A": "X", "B": "Y", "C": "Z"}
        sheet.save_to_database(self.session, Signature, mapdict=mapdict)
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_save_an_array3(self):
        data = [[1, 4, "A"], [2, 5, "B"], [3, 6, "C"]]
        sheet = pe.Sheet(data)
        sheet.transpose()
        sheet.name_columns_by_row(2)
        mapdict = ["X", "Y", "Z"]
        sheet.save_to_database(self.session, Signature, mapdict=mapdict)
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_save_an_array4(self):
        data = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        sheet.name_columns_by_row(0)
        mapdict = {"A": "X", "B": "Y", "C": "Z"}
        sheet.save_to_database(self.session, Signature, mapdict=mapdict)
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_save_an_array7(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        sheet.name_columns_by_row(0)

        def make_signature(row):
            return Signature(X=row["X"], Y=row["Y"], Z=row["Z"])

        sheet.save_to_database(
            self.session, Signature, initializer=make_signature
        )
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_book_save_a_dict(self):
        data = [[1, 4, "X"], [2, 5, "Y"], [3, 6, "Z"]]
        sheet1 = Signature.__tablename__
        sheet_dict = {sheet1: data}
        book = pe.Book(sheet_dict)
        book[sheet1].transpose()
        book[sheet1].name_columns_by_row(2)
        book.save_to_database(self.session, [Signature])
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_book_save_a_dict2(self):
        data = [[1, 4, "X"], [2, 5, "Y"], [3, 6, "Z"]]
        data1 = [[1, 4, "A"], [2, 5, "B"], [3, 6, "C"]]
        sheet1 = Signature.__tablename__
        sheet2 = Signature2.__tablename__
        sheet_dict = {sheet1: data, sheet2: data1}
        book = pe.Book(sheet_dict)
        book[sheet1].transpose()
        book[sheet1].name_columns_by_row(2)
        book[sheet2].transpose()
        book[sheet2].name_columns_by_row(2)
        book.save_to_database(self.session, [Signature, Signature2])
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.get_dict(session=self.session, table=Signature2)
        assert result == {"A": [1, 4], "B": [2, 5], "C": [3, 6]}

    def test_save_as_to_database(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        pe.save_as(
            adict=adict,
            dest_session=self.session,
            dest_table=Signature,
            name_columns_by_row=0,
        )
        result = pe.get_dict(session=self.session, table=Signature)
        assert adict == result

    def test_save_book_as_to_database(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        data1 = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
        sheet_dict = {
            Signature.__tablename__: data,
            Signature2.__tablename__: data1,
        }
        pe.save_book_as(
            bookdict=sheet_dict,
            dest_session=self.session,
            dest_tables=[Signature, Signature2],
        )
        result = pe.get_dict(session=self.session, table=Signature)
        assert result == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        result = pe.get_dict(session=self.session, table=Signature2)
        assert result == {"A": [1, 4], "B": [2, 5], "C": [3, 6]}


class TestSQL:
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        row1 = Signature(X=1, Y=2, Z=3)
        row2 = Signature(X=4, Y=5, Z=6)
        row3 = Signature2(A=1, B=2, C=3)
        row4 = Signature2(A=4, B=5, C=6)
        session = Session()
        session.add(row1)
        session.add(row2)
        session.add(row3)
        session.add(row4)
        session.commit()

    def test_get_sheet_from_query_sets(self):
        session = Session()
        objects = session.query(Signature).all()
        column_names = ["X", "Y", "Z"]
        sheet = pe.get_sheet(column_names=column_names, query_sets=objects)
        assert sheet.to_array() == [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]

    def test_get_sheet_from_sql(self):
        sheet = pe.get_sheet(session=Session(), table=Signature)
        assert sheet.to_array() == [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]

    def test_get_array_from_sql(self):
        array = pe.get_array(session=Session(), table=Signature)
        assert array == [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]

    def test_get_dict_from_sql(self):
        adict = pe.get_dict(session=Session(), table=Signature)
        assert adict == {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}

    def test_get_records_from_sql(self):
        records = pe.get_records(session=Session(), table=Signature)
        assert records == [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]

    def test_get_book_from_sql(self):
        book_dict = pe.get_book_dict(
            session=Session(), tables=[Signature, Signature2]
        )
        expected = OrderedDict()
        expected.update({"signature": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]})
        expected.update(
            {"signature2": [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]}
        )
        assert book_dict == expected

    @raises(pe.exceptions.UnknownParameters)
    def test_save_book_as_file_from_sql_compactibility(self):
        test_file = "book_from_sql.xls"
        pe.save_book_as(
            out_file=test_file,
            session=Session(),
            tables=[Signature, Signature2],
        )

    def test_save_book_as_file_from_sql(self):
        test_file = "book_from_sql.xls"
        pe.save_book_as(
            dest_file_name=test_file,
            session=Session(),
            tables=[Signature, Signature2],
        )
        book_dict = pe.get_book_dict(file_name=test_file)
        expected = OrderedDict()
        expected.update({"signature": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]})
        expected.update(
            {"signature2": [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]}
        )
        assert book_dict == expected
        os.unlink(test_file)

    def test_save_book_to_memory_from_sql(self):
        test_file = pe.save_book_as(
            dest_file_type="xls",
            session=Session(),
            tables=[Signature, Signature2],
        )
        book_dict = pe.get_book_dict(
            file_content=test_file.getvalue(), file_type="xls"
        )
        expected = OrderedDict()
        expected.update({"signature": [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]})
        expected.update(
            {"signature2": [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]}
        )
        assert book_dict == expected


class TestGetBook:
    def test_get_book_from_book_dict(self):
        content = _produce_ordered_dict()
        book = pe.get_book(bookdict=content)
        assert book.to_dict() == content

    def test_get_book_from_file(self):
        test_file = "test_get_book.xls"
        content = _produce_ordered_dict()

        book = pe.Book(content)
        book.save_as(test_file)
        book2 = pe.get_book(file_name=test_file)
        assert book2.to_dict() == content
        os.unlink(test_file)

    def test_get_book_from_memory(self):
        content = _produce_ordered_dict()
        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        book2 = pe.get_book(file_content=io.getvalue(), file_type="xls")
        assert book2.to_dict() == content

    def test_get_book_from_file_stream(self):
        content = _produce_ordered_dict()

        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        book2 = pe.get_book(file_stream=io, file_type="xls")
        assert book2.to_dict() == content

    @raises(IOError)
    def test_get_book_from_memory_compatibility(self):
        content = _produce_ordered_dict()
        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        pe.get_book(content=io.getvalue(), file_type="xls")

    def test_get_book_dict(self):
        content = _produce_ordered_dict()
        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        adict = pe.get_book_dict(file_content=io.getvalue(), file_type="xls")
        assert adict == content

    def test_get_sheet_from_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        test_sheet_name = "custom_sheet"
        book = pe.get_book(array=data, sheet_name=test_sheet_name)
        result = book.to_dict()
        eq_(data, result[test_sheet_name])

    def test_get_sheet_from_dict(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        test_sheet_name = "custom_sheet"
        book = pe.get_book(adict=adict, sheet_name=test_sheet_name)
        expected = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = book.to_dict()
        eq_(expected, result[test_sheet_name])

    def test_get_sheet_from_records(self):
        records = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        test_sheet_name = "custom_sheet"
        book = pe.get_book(records=records, sheet_name=test_sheet_name)
        expected = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = book.to_dict()
        eq_(expected, result[test_sheet_name])


class TestIGetBook:
    def test_get_book_from_book_dict(self):
        content = _produce_ordered_dict()
        book = pe.iget_book(bookdict=content)
        eq_(book.to_dict(), content)

    def test_get_book_from_file(self):
        test_file = "test_get_book.xls"
        content = _produce_ordered_dict()

        book = pe.Book(content)
        book.save_as(test_file)
        book_stream = pe.iget_book(file_name=test_file)
        assert book_stream.to_dict() != content
        book3 = pe.Book(book_stream.to_dict())
        eq_(book3.to_dict(), content)
        os.unlink(test_file)

    def test_get_book_from_memory(self):
        content = _produce_ordered_dict()
        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        book_stream = pe.iget_book(file_content=io.getvalue(), file_type="xls")
        assert book_stream.to_dict() != content
        book = pe.Book(book_stream.to_dict())
        eq_(book.to_dict(), content)

    def test_get_book_from_file_stream(self):
        content = _produce_ordered_dict()

        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        book_stream = pe.iget_book(file_stream=io, file_type="xls")
        assert book_stream.to_dict() != content
        book = pe.Book(book_stream.to_dict())
        eq_(book.to_dict(), content)

    @raises(IOError)
    def test_get_book_from_memory_compatibility(self):
        content = _produce_ordered_dict()
        io = pe.save_book_as(dest_file_type="xls", bookdict=content)
        pe.iget_book(content=io.getvalue(), file_type="xls")

    def test_get_sheet_from_array(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        test_sheet_name = "custom_sheet"
        book = pe.iget_book(array=data, sheet_name=test_sheet_name)
        result = book.to_dict()
        eq_(data, list(result[test_sheet_name]))

    def test_get_sheet_from_dict(self):
        adict = {"X": [1, 4], "Y": [2, 5], "Z": [3, 6]}
        test_sheet_name = "custom_sheet"
        book = pe.iget_book(adict=adict, sheet_name=test_sheet_name)
        expected = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = book.to_dict()
        eq_(expected, list(result[test_sheet_name]))

    def test_get_sheet_from_records(self):
        records = [{"X": 1, "Y": 2, "Z": 3}, {"X": 4, "Y": 5, "Z": 6}]
        test_sheet_name = "custom_sheet"
        book = pe.iget_book(records=records, sheet_name=test_sheet_name)
        expected = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        result = book.to_dict()
        eq_(expected, list(result[test_sheet_name]))

    def test_look_at_sheet_names_without_incurring_further_memory_cost(self):
        test_file = "test_get_book.xls"
        content = _produce_ordered_dict()

        book = pe.Book(content)
        book.save_as(test_file)
        book_stream = pe.iget_book(file_name=test_file)
        eq_(book_stream.sheet_names(), ["Sheet1", "Sheet2", "Sheet3"])
        assert isinstance(book_stream["Sheet1"].payload, GeneratorType)
        os.unlink(test_file)

    def test_look_at_sheet_names_decides_to_read_seond_one(self):
        test_file = "test_get_book.xls"
        content = _produce_ordered_dict()

        book = pe.Book(content)
        book.save_as(test_file)
        book_stream = pe.iget_book(file_name=test_file)
        data = pe.iget_array(sheet_stream=book_stream["Sheet1"])
        assert isinstance(data, GeneratorType)
        eq_(list(data), [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]])
        os.unlink(test_file)


class TestSaveAs:
    def test_force_file_type(self):
        pe.save_as(
            array=[[1, 2]], dest_file_name="a.txt", dest_force_file_type="csv"
        )
        actual = pe.get_array(file_name="a.txt", force_file_type="csv")
        eq_([[1, 2]], actual)
        os.unlink("a.txt")

    def test_force_file_type_for_save_book_as(self):
        pe.save_as(
            bookdict={"sheet1": [[1, 2]]},
            dest_file_name="a.bin",
            dest_force_file_type="xls",
        )
        actual = pe.get_book_dict(file_name="a.bin", force_file_type="xls")
        eq_({"sheet1": [[1, 2]]}, actual)
        os.unlink("a.bin")

    def test_save_file_as_another_one(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        testfile2 = "testfile2.csv"
        sheet.save_as(testfile)
        pe.save_as(file_name=testfile, dest_file_name=testfile2)
        sheet = pe.get_sheet(file_name=testfile2)
        sheet.format(int)
        eq_(sheet.to_array(), data)
        os.unlink(testfile)
        os.unlink(testfile2)

    def test_save_as_and_append_colnames(self):
        data = [[1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        testfile2 = "testfile.xls"
        sheet.save_as(testfile)
        pe.save_as(
            file_name=testfile,
            dest_file_name=testfile2,
            colnames=["X", "Y", "Z"],
        )
        array = pe.get_array(file_name=testfile2)
        eq_(array, [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]])


class TestiSaveAs:
    def tearDown(self):
        pe.free_resources()

    def test_save_file_as_another_one(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        testfile2 = "testfile2.csv"
        sheet.save_as(testfile)
        pe.isave_as(file_name=testfile, dest_file_name=testfile2)
        sheet = pe.get_sheet(file_name=testfile2)
        eq_(sheet.to_array(), data)
        os.unlink(testfile)
        os.unlink(testfile2)

    @raises(Exception)
    def test_save_as_invalid_params(self):
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        testfile2 = "testfile2.csv"
        sheet.save_as(testfile)
        pe.isave_as(
            file_name=testfile, dest_file_name=testfile2, name_columns_by_row=0
        )

    def test_save_file_as_texttable(self):
        """
        test if _texttable can render generator or not
        """
        data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
        sheet = pe.Sheet(data)
        testfile = "testfile.xls"
        testfile2 = "testfile2.texttable"
        sheet.save_as(testfile)
        pe.isave_as(file_name=testfile, dest_file_name=testfile2)
        os.unlink(testfile)
        os.unlink(testfile2)


def _produce_ordered_dict():
    data_dict = OrderedDict()
    data_dict.update({"Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]})
    data_dict.update({"Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]]})
    data_dict.update(
        {"Sheet3": [[u"X", u"Y", u"Z"], [1, 4, 7], [2, 5, 8], [3, 6, 9]]}
    )
    return data_dict


def test_get_io_type():
    file_type = pe.core.get_io_type("csv")
    eq_(file_type, "string")
    file_type = pe.core.get_io_type("strange")
    eq_(file_type, "string")


def test_isave_book_as():
    content = _produce_ordered_dict()
    io = pe.isave_book_as(dest_file_type="xls", bookdict=content)
    book2 = pe.get_book(file_content=io.getvalue(), file_type="xls")
    assert book2.to_dict() == content
    pe.free_resources()


@raises(Exception)
def test_parser_library_parameter():
    pe.get_sheet(file_name="test", parser_library="pyexcel-unknown")


@raises(Exception)
def test_renderer_library_parameter():
    data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
    sheet = pe.Sheet(data)
    testfile = "testfile.xls"
    sheet.save_as(testfile, renderer_library="pyexcel-unknown")


@raises(Exception)
def test_renderer_library_parameter_2():
    data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
    pe.save_as(
        array=data,
        dest_file_name="test_file.xls",
        dest_renderer_library="pyexcel-unknown",
    )


@raises(Exception)
def test_source_library_parameter():
    pe.get_sheet(file_name="test", source_library="pyexcel-unknown")


@raises(Exception)
def test_source_library_parameter_1():
    data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
    pe.save_as(
        array=data,
        dest_file_name="test_file.xls",
        dest_source_library="pyexcel-unknown",
    )


@raises(Exception)
def test_source_library_parameter_2():
    data = [["X", "Y", "Z"], [1, 2, 3], [4, 5, 6]]
    pe.save_as(
        array=data,
        dest_file_name="test_file.xls",
        source_library="pyexcel-unknown",
    )
