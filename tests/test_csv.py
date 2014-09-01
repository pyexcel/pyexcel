import unittest
import os
from base import PyexcelBase


class TestCSVReader(unittest.TestCase, PyexcelBase):
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

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)