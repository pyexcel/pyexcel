import unittest
import os
import pyexcel

class TestIterator(unittest.TestCase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        f = open(self.testfile, "w")
        for i in [0,4,8]:
            f.write("%s,%s,%s,%s\n" % (i+1, i+2, i+3, i+4))
        f.close()

    def test_horizontal_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = []
        for v in r:
            actual.append(v)
        assert result == actual
        
    def test_row_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,2,3,4,5,6,7,8,9,10,11,12]
        actual = []
        for v in r.rows():
            actual += v
        print actual
        assert result == actual
        
    def test_horizontal_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [12,11,10,9,8,7,6,5,4,3,2,1]
        actual = []
        for v in r.reverse():
            actual.append(v)
        assert result == actual

    def test_row_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [9,10,11,12,5,6,7,8,1,2,3,4]
        actual = []
        for v in r.rrows():
            actual += v
        assert result == actual

    def test_vertical_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,5,9,2,6,10,3,7,11,4,8,12]
        actual = []
        for v in r.vertical():
            actual.append(v)
        assert result == actual
        
    def test_column_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,5,9,2,6,10,3,7,11,4,8,12]
        actual = []
        for v in r.columns():
            actual += v
        assert result == actual
        
    def test_vertical_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [12,8,4,11,7,3,10,6,2,9,5,1]
        actual = []
        for v in r.rvertical():
            actual.append(v)
        assert result == actual
        
    def test_column_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [4,8,12,3,7,11,2,6,10,1,5,9]
        actual = []
        for v in r.rcolumns():
            actual += v
        assert result == actual
        
    def test_horizontal_top_right_2_bottom_left_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [4,3,2,1,8,7,6,5,12,11,10,9]
        actual = []
        for v in pyexcel.iterators.HTRBLIterator(r):
            actual.append(v)
        print actual
        assert result == actual
        
    def test_horizontal_bottom_left_2_top_right_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [9,10,11,12,5,6,7,8,1,2,3,4]
        actual = []
        for v in pyexcel.iterators.HBLTRIterator(r):
            actual.append(v)
        print actual
        assert result == actual
        
    def test_vertical_bottom_left_2_top_right_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [9,5,1,10,6,2,11,7,3,12,8,4]
        actual = []
        for v in pyexcel.iterators.VBLTRIterator(r):
            actual.append(v)
        print actual
        assert result == actual
        
    def test_vertical_top_right_2_bottom_left_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [4,8,12,3,7,11,2,6,10,1,5,9]
        actual = []
        for v in pyexcel.iterators.VTRBLIterator(r):
            actual.append(v)
        print actual
        assert result == actual