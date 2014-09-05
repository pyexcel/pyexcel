import os
from base import PyexcelXlsBase

class TestXLSReader(PyexcelXlsBase):
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