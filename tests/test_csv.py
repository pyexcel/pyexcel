import unittest
import pyexcel
import os


class TestCSVReader(unittest.TestCase):
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        f = open(self.testfile, "w")
        for i in range(0,self.rows):
            row = i + 1
            f.write("%s,%s,%s,%s\n" % (row, row, row, row))
        f.close()

    def test_number_of_rows(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == r.number_of_rows()

    def test_cell_value(self):
        r = pyexcel.Reader(self.testfile)
        for i in range(0, self.rows):
            row = i + 1
            assert str(row) == r.cell_value(i,0)
        for i in r.row_range():
            print r.cell_value(i,1)
            assert str(i+1) == r.cell_value(i,1)
            assert str(r.row_index(i)) == r.cell_value(i,1)
            
    def test_row_range(self):
        r = pyexcel.Reader(self.testfile)
        assert self.rows == len(r.row_range())
            
    def test_first_row(self):
        r = pyexcel.Reader(self.testfile)
        assert "1" == r.cell_value(r.first_row(),0)

    def test_row_index(self):
        r = pyexcel.Reader(self.testfile)
        assert 2 == r.row_index(r.first_row()+1)

    def test_number_of_columns(self):
        r = pyexcel.Reader(self.testfile)
        assert 4 == r.number_of_columns()

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)