import os
import pyexcel
from base import PyexcelBase


class TestODSReader(PyexcelBase):
    def setUp(self):
        """
        Declare the test xls file.

        It is pre-made as csv file:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = "test.ods"
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

