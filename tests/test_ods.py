import os
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
        self.testfile = os.path.join("tests", "testods.ods")
        self.rows = 3

    def tearDown(self):
        pass
