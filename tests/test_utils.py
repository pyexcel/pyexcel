import os
from unittest import TestCase
import pyexcel as pe
from nose.tools import raises, eq_


class TestToRecord(TestCase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "test.xls"
        self.content = {"X": [1, 2, 3], "Y": [4, 5, 6], "Z": [7, 8, 9]}
        pe.save_as(dest_file_name=self.testfile, adict=self.content)

    def test_book_reader_to_records(self):
        r = pe.SeriesReader(self.testfile)
        result = [
            {u"Y": 4.0, u"X": 1.0, u"Z": 7.0},
            {u"Y": 5.0, u"X": 2.0, u"Z": 8.0},
            {u"Y": 6.0, u"X": 3.0, u"Z": 9.0},
        ]
        eq_(result, list(r.records))

    @raises(ValueError)
    def test_index_sheet1(self):
        """Invalid input"""
        s = pe.Sheet([[1, 2, 3]], "test")
        list(s.to_records())

    def test_index_sheet2(self):
        s = pe.ColumnSeriesReader(self.testfile, series=0)
        result = [
            {"1": 4, "X": "Y", "3": 6, "2": 5},
            {"1": 7, "X": "Z", "3": 9, "2": 8},
        ]
        eq_(result, list(s.records))

    def test_index_sheet3(self):
        s = pe.ColumnSeriesReader(self.testfile, series=0)
        headers = ["Row 1", "Row 2", "Row 3", "Row 4"]
        actual = s.to_records(headers)
        result = [
            {"Row 4": 6.0, "Row 2": 4.0, "Row 1": "Y", "Row 3": 5.0},
            {"Row 4": 9.0, "Row 2": 7.0, "Row 1": "Z", "Row 3": 8.0},
        ]
        eq_(result, list(actual))

    def test_book_reader_to_records_custom(self):
        """use custom header
        """
        r = pe.SeriesReader(self.testfile)
        custom_headers = ["O", "P", "Q"]
        result = [
            {u"P": 4.0, u"O": 1.0, u"Q": 7.0},
            {u"P": 5.0, u"O": 2.0, u"Q": 8.0},
            {u"P": 6.0, u"O": 3.0, u"Q": 9.0},
        ]
        actual = r.to_records(custom_headers)
        eq_(result, list(actual))

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
