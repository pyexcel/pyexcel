import unittest
import pyexcel
import os


class TestODSReader(unittest.TestCase):
    def setUp(self):
        """
        Declare the test xls file.

        It is pre-made as csv file:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = os.path.join("tests", "testods.ods")
        self.rows = 3

    def test_number_of_rows(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert str(row) == r.cell_value(i,1)
        for i in r.row_range():
            print r.cell_value(i,1)
            assert str(i+1) == r.cell_value(i,1)
        assert "3" == r.cell_value(2, 3)

    def test_row_range(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == len(r.row_range())
            
    def test_number_of_columns(self):
        r = pyexcel.Reader(self.testfile)
        assert 4 == r.number_of_columns()
