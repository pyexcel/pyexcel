import unittest
import os
import pyexcel

class TestIterator(unittest.TestCase):
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

    def test_horizontal_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,1,1,1,2,2,2,2,3,3,3,3]
        actual = []
        for v in r:
            actual.append(v)
        assert result == actual
        
    def test_horizontal_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [3,3,3,3,2,2,2,2,1,1,1,1]
        actual = []
        for v in r.reverse():
            actual.append(v)
        assert result == actual

    def test_vertical_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [1,2,3,1,2,3,1,2,3,1,2,3]
        actual = []
        for v in r.vertical():
            actual.append(v)
        assert result == actual
        
    def test_vertical_reverse_iterator(self):
        r = pyexcel.Reader(self.testfile)
        result = [3,2,1,3,2,1,3,2,1,3,2,1]
        actual = []
        for v in r.rvertical():
            actual.append(v)
        assert result == actual

