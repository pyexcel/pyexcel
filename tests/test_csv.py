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