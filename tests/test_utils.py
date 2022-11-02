import os
from unittest import TestCase
from nose.tools import eq_, raises
import pyexcel as pe

v
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
            {"Y": 4.0, "X": 1.0, "Z": 7.0},
            {"Y": 5.0, "X": 2.0, "Z": 8.0},
            {"Y": 6.0, "X": 3.0, "Z": 9.0},
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
        """use custom header"""
        r = pe.SeriesReader(self.testfile)
        custom_headers = ["O", "P", "Q"]
        result = [
            {"P": 4.0, "O": 1.0, "Q": 7.0},
            {"P": 5.0, "O": 2.0, "Q": 8.0},
            {"P": 6.0, "O": 3.0, "Q": 9.0},
        ]
        actual = r.to_records(custom_headers)
        eq_(result, list(actual))

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
