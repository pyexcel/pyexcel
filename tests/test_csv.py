import unittest
import pyexcel
import os


class TestCSVReader(unittest.TestCase):
    def setUp(self):
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
            
    def test_first_row(self):
        r = pyexcel.Reader(self.testfile)
        assert "1" == r.cell_value(r.first_row(),0)

    def test_row_index(self):
        r = pyexcel.Reader(self.testfile)
        assert 2 == r.row_index(r.first_row()+1)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)