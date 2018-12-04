from base import (
    PyexcelSheetRWBase,
    clean_up_files,
    create_sample_file1,
    create_sample_file1_series,
)
from _compact import OrderedDict

import pyexcel as pe
from nose.tools import eq_, raises


class TestReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testfile = "testcsv.csv"
        create_sample_file1(self.testfile)

    def test_set_named_column_at(self):
        r = pe.SeriesReader(self.testfile)
        r.set_named_column_at("b", [11, 1])
        eq_(r.column_at(1), [11, 1])

    def tearDown(self):
        clean_up_files([self.testfile])


class TestReader2(PyexcelSheetRWBase):
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testclass = pe.Reader
        self.testfile = "testcsv.xls"
        create_sample_file1(self.testfile)

    def tearDown(self):
        clean_up_files([self.testfile])


class TestSeriesReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testclass = pe.SeriesReader
        self.testfile = "testcsv.xls"
        create_sample_file1_series(self.testfile)

    @raises(TypeError)
    def test_extend_columns(self):
        r = self.testclass(self.testfile)
        columns = [["p", "a", "d"], ["c1", "c2", "c3"], ["x1", "x2", "x4"]]
        r.extend_columns(columns)

    def test_extend_columns2(self):
        r = self.testclass(self.testfile)
        columns = OrderedDict()
        columns.update({"p": ["c1", "x1"]})
        columns.update({"a": ["c2", "x2"]})
        columns.update({"d": ["c3", "x4"]})
        r.extend_columns(columns)
        assert r.row[0] == ["a", "b", "c", "d", "c1", "c2", "c3"]
        assert r.row[1] == ["e", "f", "g", "h", "x1", "x2", "x4"]
        assert r.row[2] == ["i", "j", 1.1, 1, "", "", ""]
        r2 = self.testclass(self.testfile)
        columns = OrderedDict()
        columns.update({"p": ["c1", "x1", "y1", "z1"]})
        columns.update({"a": ["c2", "x2", "y2"]})
        columns.update({"d": ["c3", "x4"]})
        r2.extend_columns(columns)

        assert r2.row[0] == ["a", "b", "c", "d", "c1", "c2", "c3"]
        assert r2.row[1] == ["e", "f", "g", "h", "x1", "x2", "x4"]
        assert r2.row[2] == ["i", "j", 1.1, 1, "y1", "y2", ""]
        assert r2.row[3] == ["", "", "", "", "z1", "", ""]

    def tearDown(self):
        clean_up_files([self.testfile])
