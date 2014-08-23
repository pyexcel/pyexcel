import unittest
import pyexcel
import os


class TestXLSReader(unittest.TestCase):
    def setUp(self):
        """
        Declare the test xls file.

        It is pre-made as csv file:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = os.path.join("tests", "testxls.xls")
        self.rows = 3

    def test_number_of_rows(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert row == r.cell_value(i,0)
        for i in r.row_range():
            print r.cell_value(i,1)
            assert i+1 == r.cell_value(i,1)
            assert r.row_index(i) == r.cell_value(i,1)
            
    def test_row_range(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == len(r.row_range())
            
    def test_first_row(self):
        r = pyexcel.Reader(self.testfile)
        assert 1 == r.cell_value(r.first_row(),0)

    def test_row_index(self):
        r = pyexcel.Reader(self.testfile)
        assert 2 == r.row_index(r.first_row()+1)

