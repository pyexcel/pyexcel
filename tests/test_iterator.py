import os
import pyexcel
from base import PyexcelIteratorBase, create_sample_file2


class TestIteratableArray(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.array = []
        for i in [0, 4, 8]:
            array = [i+1, i+2, i+3, i+4]
            self.array.append(array)
        self.iteratable = pyexcel.iterators.Matrix(self.array)


class TestIteratorWithPlainReader(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        create_sample_file2(self.testfile)
        self.iteratable = pyexcel.PlainReader(self.testfile)

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        

class TestIterator(PyexcelIteratorBase):
    def setUp(self):
        """
        Make a test csv file as:

        1, 2,3,4
        5,6,7,8
        9,10,11,12
        """
        self.testfile = "testcsv.csv"
        create_sample_file2(self.testfile)
        self.iteratable = pyexcel.Reader(self.testfile)
        
    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestHatIterators:
    def setUp(self):
        self.testfile = "test.csv"
        self.content = [
            ["X", "Y", "Z"],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]
        ]
        w = pyexcel.Writer(self.testfile)
        w.write_array(self.content)
        w.close()

    def test_hat_column_iterator(self):
        r = pyexcel.SeriesReader(self.testfile)
        result = pyexcel.utils.to_dict(r)
        actual = {
            "X": [1, 1, 1, 1, 1],
            "Y": [2, 2, 2, 2, 2],
            "Z": [3, 3, 3, 3, 3],
        }
        assert result == actual

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
