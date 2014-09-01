import unittest
import os
from base import PyexcelXlsxBase


class TestXLSXReader(unittest.TestCase, PyexcelXlsxBase):
    def setUp(self):
        """
        Declare the test xlsx  file.

        It is pre-made as csv file:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.testfile = os.path.join("tests", "testxlsx.xlsx")
        self.rows = 3
