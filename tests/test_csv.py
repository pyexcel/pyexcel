import os
from base import PyexcelBase
import pyexcel


class TestCSVReader(PyexcelBase):
    def setUp(self):
        """
        Make a test csv file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        w = pyexcel.Writer(self.testfile)
        for i in range(0,self.rows):
            row = i + 1
            array = [row, row, row, row]
            w.write_row(array)
        w.close()

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestCSVReader2:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,k,l
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        w = pyexcel.Writer(self.testfile)
        data=['a','b','c','d','e','f','g','h','i','j',1.1,1]
        w.write_row(data[:4])
        w.write_row(data[4:8])
        w.write_row(data[8:12])
        w.close()

    def test_data_types(self):
        r = pyexcel.Reader(self.testfile)
        result=['a','b','c','d','e','f','g','h','i','j',1.1,1]
        actual = pyexcel.utils.to_array(r)
        assert result == actual        

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
